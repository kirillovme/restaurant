from __future__ import annotations

import aioredis

from config import REDIS_HOST, REDIS_PORT


class RedisClient:

    def __init__(self):
        self.redis_conn = None

    async def setup(self) -> None:
        self.redis_conn = await aioredis.from_url(f'redis://{REDIS_HOST}:{REDIS_PORT}')

    async def clear_cache(self) -> None:
        await self.redis_conn.flushall()
        await self.redis_conn.close()


redis_client = RedisClient()
