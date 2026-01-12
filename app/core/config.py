from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / ".env"


class Settings(BaseSettings):
    PROJECT_NAME: str = "Realtime Analytics API"

    ACCESS_TOKEN_EXPIRE_MINUTES: int 
    REFRESH_TOKEN_EXPIRE_DAYS: int 
    ALGORITHM: str
    SECRET_KEY: str
    REFRESH_SECRET_KEY: str
    DB_PASSWORD: str
    CLOUD_SERVER_ADMIN: str
    SERVER: str
    DATABASE: str
    UPSTASH_REDIS_REST_URL: str
    UPSTASH_REDIS_REST_TOKEN: str
    FMP_API_KEY: str
    MASSIVE_API_KEY: str
    ALPHA_VANTAGE_API_KEY: str
    CLAUDE_API_KEY: str

    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH),
        env_file_encoding="utf-8",
    )

settings = Settings()