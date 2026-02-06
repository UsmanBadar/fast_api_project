from typing import Optional
import json
from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.security import (
    get_password_hash, 
    verify_password, 
    create_access_token, 
    create_refresh_token,
    verify_refresh_token,
    create_password_reset_token,
    verify_password_reset_token
)
from app.models.user import User
from app.schemas.user_model import UserCreate
from app.schemas.token_model import Token
from app.redis_connection import redis
from app.core.config import settings


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    resp = await db.execute(select(User).filter(User.email == email))
    result = resp.scalars().first()
    return result


async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalars().first()


async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    db_user = User(
        email=user_in.email,
        full_name=user_in.full_name,
        hashed_password=get_password_hash(user_in.password),
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def authenticate_user(db: AsyncSession, email: str, password: str) -> Optional[User]:
    user = await get_user_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


async def create_access_and_refresh_token(email: str, user_id: int) -> Token:
    """Create access and refresh tokens and store them in Redis"""
    access_token = create_access_token(email)
    refresh_token = create_refresh_token(email)

    try:
        await redis.set(
            f"access_token:{user_id}",
            access_token,
            ex=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
        
        await redis.set(
            f"refresh_token:{user_id}",
            refresh_token,
            ex=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
        )

        await redis.set(
            f"refresh_token_user:{refresh_token}",
            email,
            ex=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
        )
        
        print(f"Tokens stored in Redis for user {email}")
    except Exception as e:
        print(f"WARNING: Redis error storing tokens: {e}")
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token
    )


async def refresh_access_token(refresh_token: str, db: AsyncSession) -> Token:
    """Generate new access token from valid refresh token"""
    payload = verify_refresh_token(refresh_token)
    email: str = payload.get("sub")
    
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    
    try:
        stored_email = await redis.get(f"refresh_token_user:{refresh_token}")
        if not stored_email or stored_email!= email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has been revoked or is invalid",
            )
    except Exception as e:
        print(f"WARNING: Redis error validating refresh token: {e}")
    
    # Get user from database
    user = await get_user_by_email(db, email=email)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )
    
    # Create new tokens
    return await create_access_and_refresh_token(email, user.id)


async def blacklist_tokens(user_id: int, access_token: str) -> None:
    """Blacklist user tokens during logout"""
    try:
        # Blacklist the access token for remaining validity period
        await redis.set(
            f"blacklist:{access_token}",
            "true",
            ex=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
        
        # Delete stored tokens
        await redis.delete(f"access_token:{user_id}")
        await redis.delete(f"refresh_token:{user_id}")
        
        # Delete user cache
        user = await redis.get(f"user:{user_id}")
        if user:
            user_data = json.loads(user)
            await redis.delete(f"user:{user_data.get('email')}")
        
        print(f"Tokens blacklisted for user {user_id}")
    except Exception as e:
        print(f"WARNING: Redis error blacklisting tokens: {e}")


async def create_password_reset_token_for_email(db: AsyncSession, email: str) -> str:
    user = await get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive. Please contact support.",
        )
    return create_password_reset_token(user.email)


async def reset_password_with_token(
    db: AsyncSession,
    token: str,
    new_password: str
) -> User:
    if len(new_password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long",
        )

    payload = verify_password_reset_token(token)
    email: str | None = payload.get("sub")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid reset token",
        )

    user = await get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    user.hashed_password = get_password_hash(new_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)

    try:
        await redis.delete(f"user:{email}")
    except Exception as e:
        print(f"WARNING: Redis error clearing user cache: {e}")

    return user
