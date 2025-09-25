from pydantic import BaseModel, Field
from typing import Optional


class ChatRequest(BaseModel):
    session_id: Optional[str] = Field(None, description="Optional session id")
    prompt: str = Field(..., min_length=1, max_length=500)


#  for input validation


class ChatStreamEvent(BaseModel):
    chunk: str
    done: bool = False


class ChatResponse(BaseModel):
    response: str
