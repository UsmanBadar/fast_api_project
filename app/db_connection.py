from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from dotenv import load_dotenv
from urllib.parse import quote_plus
from pathlib import Path
from typing import Generator
import os

from app.core.config import settings



# Base class for ORM models
class Base(DeclarativeBase):
    pass


# Read environment variables
username = settings.CLOUD_SERVER_ADMIN
raw_password = settings.DB_PASSWORD
server = settings.SERVER
database = settings.DATABASE


if not all([username, raw_password, server, database]):
    raise RuntimeError("Database environment variables are not set correctly")

# Encode password for safe use in URL
password = quote_plus(raw_password)

# Azure SQL connection URL for SQLAlchemy ORM with pyodbc
connection_url = (
    f"mssql+pyodbc://{username}:{password}"
    f"@{server}.database.windows.net:1433/{database}"
    "?driver=ODBC+Driver+18+for+SQL+Server"
    "&Encrypt=yes"
    "&TrustServerCertificate=no"
)

# Global engine object
engine = create_engine(
    connection_url,
    echo=True,    
    pool_pre_ping=True
)

# Factory that creates Session instances
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Generator[Session, None, None]:
    """
    Yield a SQLAlchemy ORM Session for use in routes or services.
    Each call creates a new Session that is closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

