from app.redis_connection import redis
from functools import wraps
import json


def redis_cache(expiry: int):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            company_ticker = kwargs.get("company_ticker")
            cache_key = f"{func.__name__}:{company_ticker}"

            try:
                cached_value = await redis.get(cache_key)
                if cached_value:
                    print("Retrieved from cache")
                    return json.loads(cached_value)
            except Exception as e:
                print(f"WARNING: Redis error: {e}. Falling back to live data.")

            result = await func(*args, **kwargs)

            try:
                await redis.set(cache_key, json.dumps(result), ex=expiry)
                print(f"Data stored in Redis {cache_key}")
            except Exception as e:
                print(f"WARNING: Redis error: {e}. Data is not stored in Redis.")

            return result

        return wrapper
    return decorator




