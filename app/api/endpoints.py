from fastapi import APIRouter, HTTPException, Header, Depends
from sqlalchemy.orm import Session
from app.schemas.request_schema import ChatRequest, ChatResponse, StartChatRequest
from app.services.langchain_service import run_agent
from app.utils.context import request_token, request_program_id, request_session_id, request_user_id
from app.config.postgres_db import get_session
from app.services.session_service import SessionService, ensure_session
from app.services.redis_service import redis_service
from app.utils.job_draft_schema import save_job_draft
from typing import Optional, Dict, Any
from pydantic import BaseModel
from app.services.vms_service import create_job_vms

router = APIRouter()

from fastapi.responses import StreamingResponse

@router.post("/chat")
async def chat(
    request: ChatRequest,
    token: str = Header(...),
    programId: str = Header(...)
):
    try:
        # Extract userId and sessionId from request body
        user_id = request.userId
        session_id = request.sessionId
        
        # Set the context for tools to access
        request_token.set(token)
        request_program_id.set(programId)
        request_session_id.set(session_id)
        request_user_id.set(user_id)
        
        # Initialize session in database (ensure_session might need updates, but user only asked for payload change here. 
        # Ideally, we should ensure the session actually exists or log it.)
        ensure_session(session_id=session_id, user_id=user_id)
        
        print(f"Executing request for User: {user_id}, Session: {session_id}, Program: {programId}")
        
        # Stream the response
        # We pass session_id as the 'user_id' for run_agent so that history is isolated per session
        return StreamingResponse(
            run_agent(request.message, session_id),
            media_type="text/event-stream"
        )
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


class ResetRequest(BaseModel):
    sessionId: str

@router.post("/reset")
async def reset_session(request: ResetRequest):
    try:
        session_id = request.sessionId
        
        # 1. Clear Memory (Redis History)
        redis_service.clear_history(session_id)
            
        # 2. Clear Draft (Redis Draft)
        redis_service.clear_draft(session_id)
            
        print(f"Resetting session history and draft for Session: {session_id}")
        return {"message": f"Session {session_id} reset successfully. Memory and drafts cleared."}
    except Exception as e:
        print(f"Error in reset endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ----------------------------
# Session Management Endpoints
# ----------------------------

@router.post("/start-chat")
async def start_chat(request: StartChatRequest, db: Session = Depends(get_session)):
    """Creates a new session for the user (e.g. 'user_s1')."""
    service = SessionService(db)
    session_id = service.create_new_session(request.user_id)
    return {"session_id": session_id}

@router.get("/sessions/{user_id}")
async def get_sessions(user_id: str, db: Session = Depends(get_session)):
    """returns list of all sessions for a user."""
    service = SessionService(db)
    sessions = service.get_user_sessions(user_id)
    return {"sessions": sessions}

@router.delete("/sessions/{session_id}")
async def delete_session(session_id: str, db: Session = Depends(get_session)):
    """Deletes a specific chat session from Postgres and Redis."""
    # 1. Clear Redis History
    redis_service.clear_history(session_id)
    
    # 2. Delete from DB
    service = SessionService(db)
    success = service.delete_session(session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"status": "success", "message": f"Session {session_id} deleted"}

@router.get("/history/{session_id}")
async def get_history(session_id: str):
    """
    Fetches the full chat history for a specific session directly from Redis.
    """
    messages = redis_service.get_history(session_id)
    
    # Format messages into User/AI pairs as requested
    formatted_history = []
    current_pair = {}
    
    for msg in messages:
        role = msg.get("role")
        content = msg.get("content")
        
        if role == "user":
            # If we already have a user in the current pair, push it and start new
            if "user" in current_pair:
                formatted_history.append(current_pair)
                current_pair = {}
            current_pair["user"] = content
            
        elif role == "ai":
            current_pair["ai"] = content
            # Complete the pair
            formatted_history.append(current_pair)
            current_pair = {}
            
    # Append any remaining incomplete pair
    if current_pair:
        formatted_history.append(current_pair)
        
    return {"session_id": session_id, "messages": formatted_history}


