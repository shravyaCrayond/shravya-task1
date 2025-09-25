from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from ..schemas import ChatRequest
from ..langgraph_integration import event_stream

router = APIRouter()

@router.post("/v1/chat/stream")
async def chat_stream(req: ChatRequest):
    return StreamingResponse(
        event_stream(req.prompt),
        media_type="text/event-stream"
    )
