from typing import Optional

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password, create_access_token, create_refresh_token
from app.models.user import User
from app.schemas.user_model import UserCreate
from app.schemas.token_model import Token


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user_in: UserCreate) -> User:
    db_user = User(
        email=user_in.email,
        full_name=user_in.full_name,
        hashed_password=get_password_hash(user_in.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_and_refresh_token(email: str) -> Token:
    access_token = create_access_token(email)
    refresh_token = create_refresh_token(email)
    return Token(
        access_token=access_token,
        refresh_token=refresh_token
    )
