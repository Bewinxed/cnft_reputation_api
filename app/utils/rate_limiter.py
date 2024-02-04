from functools import wraps
import time
import aioredis
from fastapi import HTTPException, Request
import fastapi


class RateLimiter:
    async def init_redis(self):
        self.redis: aioredis.Redis = await aioredis.from_url("redis://localhost:6379")

    async def is_rate_limited(self, key: str, max_requests: int, window: int) -> bool:
        current = int(time.time())
        window_start = current - window
        async with self.redis.pipeline(transaction=True) as pipe:
            try:
                pipe.zremrangebyscore(key, 0, window_start)
                pipe.zcard(key)
                pipe.zadd(key, {current: current})
                pipe.expire(key, window)
                results: list[int] = await pipe.execute()
            except aioredis.RedisError as e:
                raise HTTPException(
                    status_code=500, detail=f"Redis error: {str(e)}"
                ) from e
        return results[1] > max_requests


rate_limiter = RateLimiter()


def rate_limit(max_requests: int, window: int):
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            key = f"rate_limit:{request.client.host}:{request.url.path}"
            if await rate_limiter.is_rate_limited(key, max_requests, window):
                raise HTTPException(
                    status_code=fastapi.status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Too many requests",
                )
            return await func(*args, **kwargs)

        return wrapper

    return decorator
