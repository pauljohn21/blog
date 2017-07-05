from sanic import Blueprint
from ..utils.redis import create_redis_pool
from sanic_session.redis_session_interface import RedisSessionInterface

auth = Blueprint("auth")

create_redis = create_redis_pool(auth)
session_inter = RedisSessionInterface(redis_getter=create_redis)

@auth.middleware("request")
async def session_create(request):
    await session_inter.open(request)

@auth.middleware("response")
async def session_save(request,response):
    await session_inter.save(request,response)

from . import views