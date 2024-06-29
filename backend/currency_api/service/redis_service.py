import os

import redis.asyncio as redis

REDIS_URL = os.environ['REDIS_URL']


async def get_redis():
    return await redis.from_url(
        url=REDIS_URL,
        encoding="utf-8",
        decode_responses=True,
    )
