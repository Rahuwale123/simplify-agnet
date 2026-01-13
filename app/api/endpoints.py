from fastapi import APIRouter, HTTPException, Header
from app.schemas.request_schema import ChatRequest, ChatResponse
from app.services.langchain_service import run_agent
from app.utils.context import request_token, request_program_id, request_session_id
from app.services.db_service import DBService
from typing import Optional

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    token: str = Header(...),
    programId: str = Header(...)
):
    try:
        # Extract userId from request body
        user_id = request.userId
        
        # Set the context for tools to access
        request_token.set(token)
        request_program_id.set(programId)
        request_session_id.set(user_id)
        
        # Initialize session and job draft in database
        # We use userId as the session_id to maintain state for that user
        DBService.upsert_session(session_id=user_id, user_id=user_id, program_id=programId)
        
        # You can use token and userId here for logic/authentication
        print(f"Executing request for User: {user_id}, Program: {programId}")
        
        response = await run_agent(request.message, user_id)
        return ChatResponse(content=response)
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
