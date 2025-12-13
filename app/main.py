from fastapi import FastAPI, Depends, status, HTTPException
from app.schemas.user_model import UserCreate, UserRead
from app.services.auth_service import get_user_by_email, create_user
from sqlalchemy.orm import Session
from .db_connection import get_db

app = FastAPI()


@app.get("/")
async def home():
    return "Hello World!"


@app.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)) -> UserRead:
    existing = get_user_by_email(db, email=user_in.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    user = create_user(db, user_in=user_in)
    return user