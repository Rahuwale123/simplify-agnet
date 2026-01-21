from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    userId: str
    sessionId: str

class ChatResponse(BaseModel):
    content: str

class StartChatRequest(BaseModel):
    user_id: str
