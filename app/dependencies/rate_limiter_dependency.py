from upstash_ratelimit import Ratelimit, FixedWindow
from fastapi import Request, HTTPException, status
from app.redis_connection import sync_redis
from typing import Callable


RATE_LIMIT_CONFIGS = {
    "standard": {
        "limiter": FixedWindow(max_requests=100, window=60),
        "prefix": "@upstash/ratelimit",
        "error_message": "Rate limit exceeded. Try again in {seconds} seconds.",
        "format_time": lambda seconds: seconds
    },
    "auth": {
        "limiter": FixedWindow(max_requests=5, window=60),
        "prefix": "@upstash/ratelimit/auth",
        "error_message": "Too many login attempts. Try again in {seconds} seconds.",
        "format_time": lambda seconds: seconds
    },
    "register": {
        "limiter": FixedWindow(max_requests=3, window=3600),
        "prefix": "@upstash/ratelimit/register",
        "error_message": "Registration limit exceeded. Try again in {seconds} minutes.",
        "format_time": lambda seconds: int(seconds / 60)
    }
}


rate_limiters = {
    name: Ratelimit(
        redis=sync_redis,
        limiter=config["limiter"],
        prefix=config["prefix"]
    )
    for name, config in RATE_LIMIT_CONFIGS.items()
}


async def _rate_limit_handler(req: Request, limiter_name: str):
    identifier = req.client.host
    limiter = rate_limiters[limiter_name]
    config = RATE_LIMIT_CONFIGS[limiter_name]
    
    response = limiter.limit(identifier=identifier)
    
    if not response.allowed:
        remaining_time = response.reset - response.current
        formatted_time = config["format_time"](remaining_time)
        error_message = config["error_message"].format(seconds=formatted_time)
        
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=error_message
        )
    
    return response


def get_rate_limiter(limiter_name: str) -> Callable:
    """Factory function to get a rate limiter dependency for a specific limiter type"""
    async def rate_limit_dependency(req: Request) -> None:
        await _rate_limit_handler(req, limiter_name)
    return rate_limit_dependency


# Create dependency functions for use in Depends()
rate_limiter = get_rate_limiter("standard")
auth_rate_limiter = get_rate_limiter("auth")
register_rate_limiter = get_rate_limiter("register")
