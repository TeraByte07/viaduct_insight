from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "Viaduct Insight"
    DEBUG: bool = True

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: str
    REFRESH_TOKEN_EXPIRE_DAYS: str
    AHREFS_API_KEY: str
    DATABASE_URL: str
    SERPAPI_KEY: str
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()