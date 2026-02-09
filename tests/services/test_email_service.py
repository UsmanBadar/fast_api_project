import asyncio

from app.services import email_service


def test_build_reset_link_adds_query_parameter():
    link = email_service._build_reset_link("abc123")
    assert link.endswith("?token=abc123")


def test_send_password_reset_email_calls_sender(monkeypatch):
    captured = {}

    def fake_sender(to_email, subject, text_body, html_body):
        captured["to"] = to_email
        captured["subject"] = subject
        captured["text"] = text_body
        captured["html"] = html_body

    async def fake_to_thread(func, *args, **kwargs):
        func(*args, **kwargs)

    monkeypatch.setattr(email_service, "_send_mailersend_email", fake_sender)
    monkeypatch.setattr(email_service.asyncio, "to_thread", fake_to_thread)

    asyncio.run(email_service.send_password_reset_email("user@example.com", "token-1"))

    assert captured["to"] == "user@example.com"
    assert "Reset your password" in captured["subject"]
    assert "token=token-1" in captured["text"]
