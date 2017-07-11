from sanic.response import json
from sanic.views import HTTPMethodView

from . import api_v01
from ..utils.to_dict import user_to_dict
from ..utils.sql import API



class usersView(HTTPMethodView):

    async def get(self,request):
        _pool = request.app.pool
        async with _pool.acquire() as con:
            select_users = await con.fetch(API.get("get_users"))
            users = user_to_dict(select_users)
            return json(users)
        await _pool.release(con)

api_v01.add_route(usersView.as_view(),"/users/")


class userpostView(HTTPMethodView):

    async def get(self,request,id):
        _pool = request.app.pool
        async with _pool.acquire() as con:
            select_users = await con.fetch(API.get("get_users"))
            users = user_to_dict(select_users)
            return json(users)
        await _pool.release(con)



api_v01.add_route(userpostView.as_view(),"/user/<id:int>/posts")