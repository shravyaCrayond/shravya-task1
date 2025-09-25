from pydantic_settings import BaseSettings
from pydantic import AnyUrl

class Settings(BaseSettings):
    DATABASE_URL: AnyUrl
    REDIS_URL: str
    GEMINI_API_KEY: str
    ALLOWED_ORIGINS: str = "*"
    RATE_LIMIT: str = "5/minute"

    class Config:
        env_file = ".env"

settings = Settings()