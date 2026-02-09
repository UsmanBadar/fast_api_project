from app.core.security import (
    app_crypto_context,
    create_access_token,
    create_refresh_token,
    verify_access_token,
    verify_password,
    verify_refresh_token,
)


def test_verify_password_returns_true_for_correct_password():
    plain = "Str0ngP@ssw0rd!"
    hashed = app_crypto_context.hash(plain)
    assert verify_password(plain, hashed) is True


def test_verify_password_returns_false_for_wrong_password():
    plain = "Str0ngP@ssw0rd!"
    hashed = app_crypto_context.hash(plain)
    assert verify_password("wrong-password", hashed) is False


def test_verify_password_raises_for_invalid_hash():
    try:
        verify_password("any-password", "not-a-valid-hash")
    except Exception:
        assert True
    else:
        assert False


def test_access_token_round_trip_contains_subject_and_type():
    token = create_access_token("user@example.com")
    payload = verify_access_token(token)

    assert payload["sub"] == "user@example.com"
    assert payload["type"] == "access"


def test_refresh_token_round_trip_contains_subject_and_type():
    token = create_refresh_token("7")
    payload = verify_refresh_token(token)

    assert payload["sub"] == "7"
    assert payload["type"] == "refresh"
