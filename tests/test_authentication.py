import pytest

from app.core.security import app_crypto_context, verify_password


def test_verify_password_returns_true_for_correct_password():
    plain = "Str0ngP@ssw0rd!"
    hashed = app_crypto_context.hash(plain)

    assert verify_password(plain, hashed) is True


def test_verify_password_returns_false_for_wrong_password():
    plain = "Str0ngP@ssw0rd!"
    hashed = app_crypto_context.hash(plain)

    assert verify_password("wrong-password", hashed) is False


def test_verify_password_raises_for_invalid_hash():
    with pytest.raises(Exception):
        verify_password("any-password", "not-a-valid-hash")
