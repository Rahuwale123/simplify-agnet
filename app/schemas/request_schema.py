from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    userId: str

class ChatResponse(BaseModel):
    content: str
