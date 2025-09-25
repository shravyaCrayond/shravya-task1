import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
import redis.asyncio as redis
from .api.routes import router
from .core.config import settings
from .core.logging import configure_logging, logger

configure_logging()

app = FastAPI(title="FastAPI LangGraph Gemini Boilerplate")

origins = (
    [o.strip() for o in settings.ALLOWED_ORIGINS.split(",")]
    if settings.ALLOWED_ORIGINS
    else ["*"]
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/healthz")
def health():
    logger.info("Health check called")
    return {"status": "ok"}


# deprecated but is still here, i will figure out a better way to do this later
@app.on_event("startup")
async def startup():
    redis_conn = redis.from_url(
        settings.REDIS_URL, encoding="utf8", decode_responses=True
    )
    await FastAPILimiter.init(redis_conn)
    logger.info("FastAPILimiter connected to Redis ✅")


if __name__ == "__main__":
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=True)
