import os
import datetime
import binascii
from sanic.response import json,file,redirect
from sanic.views import HTTPMethodView

from . import auth
from ..models import verify,generate_password_hash
from ..utils.to_dict import user_to_dict

class loginView(HTTPMethodView):

    async def get(self,request):
        try:
            if request['sessions']['user'].get('ip') == request.ip:
                return json({"message":"Login"})
            else:
                return json({"message":"danger"})
        except:
            return await file("app/templates/auth/login.html")


    async def post(self,request):
        try:
            if request.form['username'] and request.form['password']:
                async with request.app.pool.acquire() as con:
                    user = await con.fetch("select * from users where username = $1", request.form['username'][0])
                    user_dict = user_to_dict(user)
                    if user and verify(password=request.form.get('password'),
                                       password_hash=user_dict['users'][0].get('password_hash')):
                        await con.execute("update users set last_login_time = $1 where id = $2",
                                          datetime.datetime.now(), user_dict['users'][0].get('id'))
                    else:
                        return json({"message": "Fail"})
                await request.app.pool.release(con)
        except Exception as e:
            return json({"message":e})
        if not request['session'].get('user'):
            request['session']['user'] =  {"id":user_dict['users'][0].get('id'),
                                           "username":request.form['username'][0],"ip":request.ip}
            return json({"message":"Success"})


auth.add_route(loginView.as_view(),"/login")

class registerView(HTTPMethodView):
    async def get(self,request):
        return await file("app/templates/auth/register.html")

    async def post(self,request):
        try:
            if request.form['username'][0] and request.form['password'][0]:
                async with request.app.pool.acquire() as con:
                    user = await con.fetchval("select * from users where username = $1", request.form['username'][0])
                    if len(user) > 0:
                        return json({"message":"Exist"})
                    else:
                        await con.execute("insert into users (username,password_hash) values ($1,$2)",
                                          (request.form['username'][0],generate_password_hash(request.form['password'][0])))
                        return json({"message":"Success"})
                await request.app.pool.release(con)
            else:
                return json({"message": "Empty"})
        except Exception as e:
            return json({"message":e})



auth.add_route(registerView.as_view(),"/register")


class logoutView(HTTPMethodView):
    async def get(self,request):
        if request['session'].get('user'):
            request['session'].pop('session',None)
            return json({'session':request['session'].get('session')})
        else:
            return json({"message":"No Login"})


auth.add_route(logoutView.as_view(),"/logout")


class userProfileView(HTTPMethodView):
    async def get(self,request):
        pass








