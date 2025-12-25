from upstash_redis.asyncio import Redis as async_redis
from upstash_redis import Redis as sync_redis_for_rate_limit
from app.core.config import settings


redis = async_redis(url=settings.UPSTASH_REDIS_REST_URL, 
              token=settings.UPSTASH_REDIS_REST_TOKEN)

sync_redis = sync_redis_for_rate_limit(url=settings.UPSTASH_REDIS_REST_URL, 
              token=settings.UPSTASH_REDIS_REST_TOKEN)