import redis
from config import REDIS_HOST, REDIS_PORT

redis_connect = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)


def clear_cache():
    redis_connect.flushall()
