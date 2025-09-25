
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.middleware import SlowAPIMiddleware
from .api.routes import router
from .core.config import settings
from .middleware.rate_limiter import limiter
from .core.logging import configure_logging, logger


configure_logging()
app = FastAPI(title="FastAPI LangGraph Gemini Boilerplate")

# CORS
origins = [o.strip() for o in settings.ALLOWED_ORIGINS.split(",")] if settings.ALLOWED_ORIGINS else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

app.include_router(router)

@app.get("/healthz")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)