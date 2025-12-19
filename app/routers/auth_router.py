from fastapi import Depends, status, HTTPException, APIRouter, Response
from app.schemas.user_model import UserCreate, UserRead, UserLogin
import json
from app.schemas.token_model import Token
from app.services.auth_service import (get_user_by_email, create_user, 
                                       authenticate_user, create_access_and_refresh_token)
from sqlalchemy.orm import Session
from app.db_connection import get_db


auth_router = APIRouter(prefix="/auth")



@auth_router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)) -> UserRead:
    try:
      existing = get_user_by_email(db, email=user_in.email)
      if existing:
         return Response(content=json.dumps("Email already registered"), status_code=status.HTTP_400_BAD_REQUEST, media_type="json")

      user = create_user(db, user_in=user_in)
      return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Internal Server error {e}")


@auth_router.post("/login")
def login(user_login: UserLogin, db: Session = Depends(get_db)) -> Token:
    try:
        if authenticate_user(db, user_login.email, user_login.password):
            return create_access_and_refresh_token(user_login.email)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Incorrect Email or password")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Internal Server error {e}")
