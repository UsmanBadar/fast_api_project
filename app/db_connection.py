from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from urllib.parse import quote_plus
from typing import AsyncGenerator
from app.core.config import settings

class Base(DeclarativeBase):
    pass

# Read environment variables
username = settings.CLOUD_SERVER_ADMIN
raw_password = settings.DB_PASSWORD
server = settings.SERVER
database = settings.DATABASE

# Encode password
password = quote_plus(raw_password)

# Create the asynchronous engine
connection_url = (
    f"mssql+aioodbc://{username}:{password}"
    f"@{server}.database.windows.net:1433/{database}"
    "?driver=ODBC+Driver+18+for+SQL+Server"
    "&Encrypt=yes"
    "&TrustServerCertificate=no"
)


engine = create_async_engine(
    connection_url,
    echo=True,    
    pool_pre_ping=True
)


AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# 4. CHANGE: Convert the generator to an AsyncGenerator
async def get_db():
    async with AsyncSessionLocal() as db:

        yield db
        # This automatically handles closing the connection
