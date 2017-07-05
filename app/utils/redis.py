import asyncio_redis

async def create_redis_pool(blue):
    _redis_pool = await asyncio_redis.Pool.create(host='127.0.0.1',port=6379,poolsize=10)
    blue._redis_pool = _redis_pool
    return _redis_pool

