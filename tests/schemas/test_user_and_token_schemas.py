from datetime import datetime

from app.schemas.token_model import Token, TokenPayload
from app.schemas.user_model import UserCreate, UserRead


def test_user_create_accepts_expected_payload():
    payload = UserCreate(email="user@example.com", password="secret123", full_name="User")
    assert payload.email == "user@example.com"
    assert payload.full_name == "User"


def test_user_read_requires_identifier_and_created_at():
    user = UserRead(
        id=1,
        email="user@example.com",
        full_name="User",
        created_at=datetime(2025, 1, 1),
    )
    assert user.id == 1
    assert user.is_active is True


def test_token_payload_defaults_to_optional_fields():
    token = Token(access_token="a", refresh_token="b")
    payload = TokenPayload()

    assert token.token_type == "bearer"
    assert payload.sub is None
