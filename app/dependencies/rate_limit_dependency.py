from upstash_ratelimit import Ratelimit, FixedWindow
from fastapi import Request
from app.redis_connection import sync_redis


rate_limit = Ratelimit(
    redis=sync_redis,
    limiter=FixedWindow(max_requests=10, window=10),
    prefix="@upstash/ratelimit"
)

async def rate_limiter(req: Request):
    identifier = req.client.host
    return rate_limit.limit(identifier=identifier)
