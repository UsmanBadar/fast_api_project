from datetime import datetime, timedelta, timezone
from typing import Any, Union

import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status

from .config import settings

app_crypto_context = CryptContext(schemes=["scrypt"], deprecated="auto")


def verify_password(password: str, hashed_password: str) -> bool:
    return app_crypto_context.verify(password, hashed_password)


def get_password_hash(password: str) -> str:
    print(password)
    return app_crypto_context.hash(password)


def _create_token(
    subject: Union[str, int],
    secret_key: str,
    expires_delta: timedelta,
    token_type: str,
) -> str:
    now = datetime.now(timezone.utc)
    expire = now + expires_delta

    to_encode: dict[str, Any] = {
        "sub": str(subject),
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
        "type": token_type,
    }

    encoded_jwt =  jwt.encode(
        to_encode,
        secret_key,
        algorithm=settings.ALGORITHM,
        headers={"type": "JWT"},
    )
    return encoded_jwt


def create_access_token(subject: Union[str, int]) -> str:
    return _create_token(
        subject=subject,
        secret_key=settings.SECRET_KEY,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        token_type="access",
    )


def create_refresh_token(subject: Union[str, int]) -> str:
    return _create_token(
        subject=subject,
        secret_key=settings.REFRESH_SECRET_KEY,
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        token_type="refresh",
    )


def decode_token_or_401(token: str, secret_key: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            secret_key,
            algorithms=[settings.ALGORITHM],
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload

def verify_access_token(token: str) -> dict:
    payload = decode_token_or_401(
        token,
        secret_key=settings.SECRET_KEY
    )

    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload


def verify_refresh_token(token: str) -> dict:
    payload = decode_token_or_401(
        token,
        secret_key=settings.REFRESH_SECRET_KEY
    )

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload
