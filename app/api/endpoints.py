from fastapi import APIRouter, HTTPException, Header
from app.schemas.request_schema import ChatRequest, ChatResponse
from app.services.langchain_service import run_agent
from app.utils.context import request_token, request_program_id, request_session_id
from app.services.db_service import DBService
from typing import Optional, Dict, Any
from app.tools.memory_tools import JOB_DRAFTS
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
        # Extract userId from request body
        user_id = request.userId
        
        # Set the context for tools to access
        request_token.set(token)
        request_program_id.set(programId)
        request_session_id.set(user_id)
        
        # Initialize session and job draft in database
        DBService.upsert_session(session_id=user_id, user_id=user_id, program_id=programId)
        
        print(f"Executing request for User: {user_id}, Program: {programId}")
        
        # Stream the response
        return StreamingResponse(
            run_agent(request.message, user_id),
            media_type="text/event-stream"
        )
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/jobs/create")
async def create_job(
    request: Dict[str, Any],
    token: str = Header(...),
    programId: str = Header(...)
):
    try:
        user_id = request.get("userId")
        if not user_id:
            raise HTTPException(status_code=400, detail="UserId is required")
            
        # Retrieve draft from internal memory
        # Note: In production, this should come from a DBService, not in-memory global
        draft = JOB_DRAFTS.get(user_id) or JOB_DRAFTS.get("default")
        
        if not draft:
            raise HTTPException(status_code=404, detail="No active job draft found for this user.")

        print(f"Creating job for Program: {programId} using Internal Draft")
        
        # Call the VMS Service
        result = create_job_vms(programId, token, draft)
        
        return {"message": "Job created successfully", "vms_response": result}
    except Exception as e:
        print(f"Error in create_job endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
