import asyncio_redis
from sanic_session import RedisSessionInterface


class Redis:
    _redis_pool = None

    async def create_redis_pool(self):
        if not self._redis_pool:
            self._redis_pool = await asyncio_redis.Pool.create(host='127.0.0.1',port=6379,poolsize=10)
        return self._redis_pool

redis = Redis()
redis_interface = RedisSessionInterface(redis.create_redis_pool)



