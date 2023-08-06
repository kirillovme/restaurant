from __future__ import annotations

import redis

from config import REDIS_HOST, REDIS_PORT


def get_redis_connection(host: str | None, port: str | None) -> redis.Redis:
    if host is None or port is None:
        raise ValueError('REDIS_HOST and REDIS_PORT must be configured')

    return redis.Redis(host=host, port=int(port))


redis_connect = get_redis_connection(REDIS_HOST, REDIS_PORT)


def clear_cache() -> None:
    redis_connect.flushall()
