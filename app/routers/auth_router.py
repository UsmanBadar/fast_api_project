from fastapi import Depends, status, HTTPException, APIRouter
from app.schemas.user_model import UserCreate, UserRead, UserLogin
from app.schemas.password_reset_model import PasswordResetRequest, PasswordResetConfirm
from app.schemas.token_model import Token, RefreshTokenRequest
from app.services.auth_service import (
    get_user_by_email, 
    create_user, 
    authenticate_user, 
    create_access_and_refresh_token,
    refresh_access_token,
    blacklist_tokens,
    create_password_reset_token_for_email,
    reset_password_with_token
)
from app.services.email_service import send_password_reset_email
from app.dependencies.auth_dependency import (
    get_current_user, 
    get_current_active_user, 
    get_current_user_and_token
)
from app.dependencies.rate_limiter_dependency import (
    auth_rate_limiter, 
    register_rate_limiter
)
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.db_connection import get_db
from typing import Tuple


auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@auth_router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(
    user_in: UserCreate, 
    db: AsyncSession = Depends(get_db),
) -> UserRead:
    """
    Register a new user account.
    
    - **email**: Valid email address (must be unique)
    - **password**: Strong password (min 8 characters recommended)
    - **full_name**: user's full name
    
    Rate limited to 3 registrations per hour per IP.
    """
    existing = await get_user_by_email(db, email=user_in.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    if len(user_in.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long"
        )
    
    user = await create_user(db, user_in=user_in)
    return user


@auth_router.post("/login", response_model=Token)
async def login(
    user_login: UserLogin, 
    db: AsyncSession = Depends(get_db),
    _rate_limit: None = Depends(auth_rate_limiter)
) -> Token:
    """
    Authenticate user and return access and refresh tokens.
    
    - **email**: User's registered email
    - **password**: User's password
    
    Returns JWT access token (short-lived) and refresh token (long-lived).
    Rate limited to 5 attempts per minute per IP.
    """
    user = await authenticate_user(db, user_login.email, user_login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive. Please contact support."
        )
    
    return await create_access_and_refresh_token(user.email, user.id)


@auth_router.post("/refresh", response_model=Token)
async def refresh_token(
    token_request: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db)
) -> Token:
    """
    Refresh access token using a valid refresh token.
    
    - **refresh_token**: Valid refresh token from login
    
    Returns new access token and refresh token pair.
    """
    return await refresh_access_token(token_request.refresh_token, db)


@auth_router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    user_and_token: Tuple[User, str] = Depends(get_current_user_and_token)
):
    """
    Logout user by blacklisting their current access token.
    
    Requires valid authentication. Frontend should delete stored tokens after this call.
    """
    current_user, access_token = user_and_token
    await blacklist_tokens(current_user.id, access_token)
    return None


@auth_router.get("/me", response_model=UserRead)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
) -> UserRead:
    """
    Get current authenticated user information.
    
    Example of a protected endpoint. Requires valid access token in Authorization header.
    """
    return current_user


@auth_router.post("/password-reset/request", status_code=status.HTTP_200_OK)
async def request_password_reset(
    payload: PasswordResetRequest,
    db: AsyncSession = Depends(get_db)
) -> dict:
    """
    Request a password reset email.
    
    - **email**: User's registered email
    """
    token = await create_password_reset_token_for_email(db, payload.email)
    await send_password_reset_email(payload.email, token)
    return {"message": "Password reset email sent"}


@auth_router.post("/password-reset/confirm", status_code=status.HTTP_200_OK)
async def confirm_password_reset(
    payload: PasswordResetConfirm,
    db: AsyncSession = Depends(get_db)
) -> dict:
    """
    Reset password using a valid reset token.
    
    - **token**: Password reset token
    - **new_password**: New password (min 8 characters)
    """
    await reset_password_with_token(db, payload.token, payload.new_password)
    return {"message": "Password has been reset"}
