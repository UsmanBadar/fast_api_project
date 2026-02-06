import asyncio

from fastapi import HTTPException, status
from mailersend import EmailBuilder, MailerSendClient

from app.core.config import settings

def _build_reset_link(token: str) -> str:
    if not settings.FRONTEND_RESET_URL:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="FRONTEND_RESET_URL is not configured",
        )
    separator = "&" if "?" in settings.FRONTEND_RESET_URL else "?"
    return f"{settings.FRONTEND_RESET_URL}{separator}token={token}"


def _send_mailersend_email(to_email: str, subject: str, text_body: str, html_body: str) -> None:
    client = MailerSendClient(api_key=settings.MAILERSEND_API_KEY)
    email = (
        EmailBuilder()
        .from_email(settings.EMAIL_FROM, settings.EMAIL_FROM_NAME or "Support")
        .to_many([{"email": to_email}])
        .subject(subject)
        .html(html_body)
        .text(text_body)
        .build()
    )
    response = client.emails.send(email)

    # SDK response handling varies by version; normalize failure checks.
    if response is None:
        return
    if hasattr(response, "success") and not response.success:
        raise RuntimeError("MailerSend send returned unsuccessful response")
    if isinstance(response, dict) and response.get("status_code", 202) >= 400:
        raise RuntimeError("MailerSend send failed")


async def send_password_reset_email(to_email: str, reset_token: str) -> None:
    if (settings.EMAIL_PROVIDER or "").lower() != "mailersend":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="EMAIL_PROVIDER is not set to mailersend",
        )
    if not settings.MAILERSEND_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="MAILERSEND_API_KEY is not configured",
        )
    if not settings.EMAIL_FROM:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="EMAIL_FROM is not configured",
        )

    reset_link = _build_reset_link(reset_token)
    expires_minutes = settings.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES

    subject = "Reset your password"
    text_body = (
        "You requested a password reset.\n\n"
        f"Use this link to reset your password: {reset_link}\n\n"
        f"This link expires in {expires_minutes} minutes."
    )
    html_body = (
        "<p>You requested a password reset.</p>"
        f"<p><a href=\"{reset_link}\">Reset your password</a></p>"
        f"<p>This link expires in {expires_minutes} minutes.</p>"
    )

    try:
        await asyncio.to_thread(
            _send_mailersend_email,
            to_email,
            subject,
            text_body,
            html_body,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to send reset email",
        ) from exc
