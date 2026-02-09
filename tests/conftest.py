import base64
import hashlib
import json
import os
import sys
import types

required_env = {
    "ACCESS_TOKEN_EXPIRE_MINUTES": "15",
    "REFRESH_TOKEN_EXPIRE_DAYS": "7",
    "ALGORITHM": "HS256",
    "SECRET_KEY": "secret",
    "REFRESH_SECRET_KEY": "refresh-secret",
    "DB_PASSWORD": "pwd",
    "CLOUD_SERVER_ADMIN": "admin",
    "SERVER": "server",
    "DATABASE": "db",
    "UPSTASH_REDIS_REST_URL": "url",
    "UPSTASH_REDIS_REST_TOKEN": "token",
    "FMP_API_KEY": "fmp",
    "MASSIVE_API_KEY": "massive",
    "ALPHA_VANTAGE_API_KEY": "alpha",
    "CLAUDE_API_KEY": "claude",
    "EMAIL_PROVIDER": "mailersend",
    "MAILERSEND_API_KEY": "mailer-key",
    "EMAIL_FROM": "noreply@example.com",
    "FRONTEND_RESET_URL": "https://app/reset",
    "EMAIL_FROM_NAME": "Support",
    "RESET_PASSWORD_SECRET_KEY": "reset-secret",
}
for key, value in required_env.items():
    os.environ.setdefault(key, value)


if "pydantic_settings" not in sys.modules:
    module = types.ModuleType("pydantic_settings")

    class SettingsConfigDict(dict):
        pass

    class BaseSettings:
        def __init__(self, **kwargs):
            annotations = getattr(self.__class__, "__annotations__", {})
            for name in annotations:
                if name in kwargs:
                    value = kwargs[name]
                elif hasattr(self.__class__, name):
                    default_value = getattr(self.__class__, name)
                    value = default_value if default_value is not None else os.environ.get(name)
                else:
                    value = os.environ.get(name)
                if value is None:
                    raise ValueError(f"Missing required setting: {name}")
                field_type = annotations.get(name)
                if field_type is int and isinstance(value, str):
                    value = int(value)
                setattr(self, name, value)

    module.BaseSettings = BaseSettings
    module.SettingsConfigDict = SettingsConfigDict
    sys.modules["pydantic_settings"] = module


if "fastapi" not in sys.modules:
    fastapi_module = types.ModuleType("fastapi")

    class HTTPException(Exception):
        def __init__(self, status_code: int, detail: str, headers=None):
            super().__init__(detail)
            self.status_code = status_code
            self.detail = detail
            self.headers = headers or {}

    class APIRouter:
        def __init__(self, *args, **kwargs):
            pass

        def get(self, *args, **kwargs):
            def decorator(func):
                return func
            return decorator

        def post(self, *args, **kwargs):
            def decorator(func):
                return func
            return decorator

    class _Status:
        HTTP_200_OK = 200
        HTTP_201_CREATED = 201
        HTTP_401_UNAUTHORIZED = 401
        HTTP_403_FORBIDDEN = 403
        HTTP_500_INTERNAL_SERVER_ERROR = 500
        HTTP_502_BAD_GATEWAY = 502

    fastapi_module.HTTPException = HTTPException
    fastapi_module.APIRouter = APIRouter
    fastapi_module.status = _Status()
    sys.modules["fastapi"] = fastapi_module


if "passlib.context" not in sys.modules:
    passlib_module = types.ModuleType("passlib")
    context_module = types.ModuleType("passlib.context")

    class CryptContext:
        def __init__(self, *args, **kwargs):
            pass

        def hash(self, password: str) -> str:
            digest = hashlib.sha256(password.encode()).hexdigest()
            return f"hashed::{digest}"

        def verify(self, password: str, hashed_password: str) -> bool:
            if not hashed_password.startswith("hashed::"):
                raise ValueError("invalid hash")
            return self.hash(password) == hashed_password

    context_module.CryptContext = CryptContext
    passlib_module.context = context_module
    sys.modules["passlib"] = passlib_module
    sys.modules["passlib.context"] = context_module


if "jwt" not in sys.modules:
    jwt_module = types.ModuleType("jwt")

    class ExpiredSignatureError(Exception):
        pass

    class InvalidTokenError(Exception):
        pass

    def encode(payload, secret, algorithm=None, headers=None):
        token_data = {"payload": payload, "secret": secret}
        raw = json.dumps(token_data).encode()
        return base64.urlsafe_b64encode(raw).decode()

    def decode(token, secret, algorithms=None):
        try:
            raw = base64.urlsafe_b64decode(token.encode()).decode()
            token_data = json.loads(raw)
        except Exception as exc:
            raise InvalidTokenError("bad token") from exc
        if token_data.get("secret") != secret:
            raise InvalidTokenError("wrong secret")
        return token_data.get("payload", {})

    jwt_module.encode = encode
    jwt_module.decode = decode
    jwt_module.ExpiredSignatureError = ExpiredSignatureError
    jwt_module.InvalidTokenError = InvalidTokenError
    sys.modules["jwt"] = jwt_module


if "httpx" not in sys.modules:
    module = types.ModuleType("httpx")

    class HTTPError(Exception):
        pass

    class HTTPStatusError(HTTPError):
        def __init__(self, response):
            self.response = response

    class RequestError(HTTPError):
        pass

    class AsyncClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        async def get(self, url, params=None):
            raise NotImplementedError

    module.AsyncClient = AsyncClient
    module.HTTPError = HTTPError
    module.HTTPStatusError = HTTPStatusError
    module.RequestError = RequestError
    sys.modules["httpx"] = module


if "mailersend" not in sys.modules:
    module = types.ModuleType("mailersend")

    class EmailBuilder:
        def from_email(self, *args, **kwargs): return self
        def to_many(self, *args, **kwargs): return self
        def subject(self, *args, **kwargs): return self
        def html(self, *args, **kwargs): return self
        def text(self, *args, **kwargs): return self
        def build(self): return {"ok": True}

    class MailerSendClient:
        def __init__(self, api_key):
            self.api_key = api_key
            self.emails = types.SimpleNamespace(send=lambda email: None)

    module.EmailBuilder = EmailBuilder
    module.MailerSendClient = MailerSendClient
    sys.modules["mailersend"] = module

if "sqlalchemy" not in sys.modules:
    sqlalchemy_module = types.ModuleType("sqlalchemy")

    def select(*args, **kwargs):
        return None

    def update(*args, **kwargs):
        return None

    def and_(*args, **kwargs):
        return None

    sqlalchemy_module.select = select
    sqlalchemy_module.update = update
    sqlalchemy_module.and_ = and_
    sqlalchemy_module.func = types.SimpleNamespace(max=lambda *args, **kwargs: None)

    ext_module = types.ModuleType("sqlalchemy.ext")
    asyncio_module = types.ModuleType("sqlalchemy.ext.asyncio")

    class AsyncSession:
        pass

    asyncio_module.AsyncSession = AsyncSession
    ext_module.asyncio = asyncio_module

    sys.modules["sqlalchemy"] = sqlalchemy_module
    sys.modules["sqlalchemy.ext"] = ext_module
    sys.modules["sqlalchemy.ext.asyncio"] = asyncio_module
