from typing import Optional, Tuple
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.security import verify_access_token
from app.db_connection import get_db
from app.models.user import User
from app.services.auth_service import get_user_by_email
from app.redis_connection import redis
import json


security = HTTPBearer()


async def get_current_user_and_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Tuple[User, str]:
    """
    Dependency to get the current authenticated user and token from JWT.
    Returns both user and the token string for operations like logout.
    """
    token = credentials.credentials
    
    # Check if token is blacklisted (user logged out)
    try:
        blacklisted = await redis.get(f"blacklist:{token}")
        if blacklisted:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has been revoked",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except Exception as e:
        # If Redis is down, we still allow authentication (graceful degradation)
        print(f"WARNING: Redis error checking blacklist: {e}")
    
    # Verify and decode the token
    payload = verify_access_token(token)
    email: str = payload.get("sub")
    
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user data is cached in Redis
    try:
        cached_user = await redis.get(f"user:{email}")
        if cached_user:
            user_data = json.loads(cached_user)
            # Reconstruct User object
            user = User(
                id=user_data["id"],
                email=user_data["email"],
                full_name=user_data.get("full_name"),
                is_active=user_data["is_active"],
                is_superuser=user_data["is_superuser"],
                hashed_password=user_data["hashed_password"]
            )
            return user, token
    except Exception as e:
        print(f"WARNING: Redis error retrieving user: {e}")
    
    # Get user from database
    user = await get_user_by_email(db, email=email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Cache user data in Redis for 15 minutes
    try:
        user_data = {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "is_active": user.is_active,
            "is_superuser": user.is_superuser,
            "hashed_password": user.hashed_password
        }
        await redis.set(f"user:{email}", json.dumps(user_data), ex=900)  # 15 minutes
    except Exception as e:
        print(f"WARNING: Redis error caching user: {e}")
    
    return user, token


async def get_current_user(
    user_and_token: Tuple[User, str] = Depends(get_current_user_and_token)
) -> User:
    """
    Dependency to get the current authenticated user from JWT token.
    """
    return user_and_token[0]


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency to ensure the current user is active.
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user


async def get_current_superuser(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency to ensure the current user is a superuser.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough privileges"
        )
    return current_user
