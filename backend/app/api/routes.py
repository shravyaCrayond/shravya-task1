from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from ..schemas import ChatRequest
from ..db.session import get_db
from ..db.models import Document
from ..langgraph_integration import event_stream
from ..core.logging import logger

router = APIRouter()


@router.post(
    "/v1/chat/stream",
    dependencies=[
        Depends(RateLimiter(times=5, seconds=60))
    ],  # 5 requests/minute per IP
)
async def chat_stream(req: ChatRequest, db: Session = Depends(get_db)):
    """
    Stream chat response from Google Gemini.
    After streaming is complete, store query and full response in PostgreSQL.
    """
    logger.info(f"Received chat prompt: {req.prompt[:50]}...")  # log first 50 chars

    full_response = ""

    async def response_generator():
        nonlocal full_response
        async for chunk in event_stream(req.prompt):
            full_response += chunk
            yield chunk

        try:
            doc = Document(query=req.prompt, content=full_response)
            db.add(doc)
            db.commit()
            db.refresh(doc)
            logger.info(f"Saved chat to database with ID: {doc.id}")
        except Exception as e:
            logger.error(f"Failed to save chat to database: {e}")
            db.rollback()

    return StreamingResponse(response_generator(), media_type="text/event-stream")
