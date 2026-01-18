from app.redis_connection import redis
from functools import wraps
import json
from fastapi.responses import JSONResponse


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
                    cached_data = json.loads(cached_value)
                    # Return cached data as JSONResponse
                    return JSONResponse(content=cached_data)
            except Exception as e:
                print(f"WARNING: Redis error: {e}. Falling back to live data.")

            result = await func(*args, **kwargs)

            try:
                # Extract actual data from JSONResponse if that's what was returned
                if isinstance(result, JSONResponse):
                    # JSONResponse.body contains the encoded JSON bytes
                    # We need to decode it first
                    data_to_cache = json.loads(result.body.decode('utf-8'))
                    json_data = json.dumps(data_to_cache)
                # Convert Pydantic model to dict before JSON serialization
                elif hasattr(result, 'model_dump'):
                    json_data = json.dumps(result.model_dump())
                else:
                    json_data = json.dumps(result)
                    
                await redis.set(cache_key, json_data, ex=expiry)
                print(f"Data stored in Redis {cache_key}")
            except Exception as e:
                print(f"WARNING: Redis error: {e}. Data is not stored in Redis.")

            return result

        return wrapper
    return decorator




