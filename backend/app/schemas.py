from pydantic import BaseModel, Field
from typing import Optional

class ChatRequest(BaseModel):
    session_id: Optional[str] = Field(None, description="Optional session id")
    prompt: str = Field(..., min_length=1, max_length=5000)

class ChatStreamEvent(BaseModel):
    chunk: str
    done: bool = False
