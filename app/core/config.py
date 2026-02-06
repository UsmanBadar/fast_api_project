from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


ENV_PATH = Path('/Users/usman/Documents/.env_secrets/.env').resolve()



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
    EMAIL_PROVIDER: str | None = None
    MAILERSEND_API_KEY: str | None = None
    EMAIL_FROM: str | None = None
    EMAIL_FROM_NAME: str | None = None
    FRONTEND_RESET_URL: str | None = None
    PASSWORD_RESET_TOKEN_EXPIRE_MINUTES: int = 60
    RESET_PASSWORD_SECRET_KEY: str | None = None

    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH),
        env_file_encoding="utf-8",
    )

settings = Settings()
