import datetime
from sanic.response import json,file,redirect,html
from sanic.views import HTTPMethodView

from . import auth
from ..models import verify,generate_password_hash
from ..utils.to_dict import user_to_dict
from ..utils.sql import Auth

class loginView(HTTPMethodView):

    async def get(self,request):
        try:
            user = request['session']['user']
            if user:
                return redirect('/')
        except:
            filename = await file("app/teplates/auth/login.html")
            return html(filename)


    async def post(self,request):
        try:
            username = request.form['username'][0]
            password = request.form['password'][0]
            if username and password :
                _pool =request.app.pool
                async with _pool.acquire() as con:
                    user = await con.fetch(Auth.get('login_post'),username)
                    user_dict = user_to_dict(user)
                    if user and verify(password=password,
                                       password_hash=user_dict['users'][0].get('password_hash')):
                        await con.execute("update users set last_login_time = $1 where id = $2",
                                          datetime.datetime.now(), user_dict['users'][0].get('id'))
                    else:
                        return json({"message": "Fail"})
                await _pool.release(con)
        except Exception as e:
            return json({"message":e})
        if not request['session'].get('user'):
            request['session']['user'] =  {"id":user_dict['users'][0].get('id'),
                                           "username":username}
            return redirect('/')


auth.add_route(loginView.as_view(),"/login")

class registerView(HTTPMethodView):
    async def get(self,request):
        return await file("app/templates/auth/register.html")

    async def post(self,request):
        try:
            username = request.form['username'][0]
            password = request.form['password'][0]
            if password and username :
                _pool = request.app.pool
                async with _pool.acquire() as con:
                    user_b = await con.fetchval("select * from users where username = $1",username)
                    if user_b:
                        return json({"message":"Exist"})
                    else:
                        password_hash = generate_password_hash(password)
                        await con.execute("insert into users (username,password_hash) values ($1,$2)",username,password_hash)
                        return json({"message":"Success"})
                await _pool.release(con)
            else:
                return json({"message": "Empty"})
        except Exception as e:
            return json({"message":e})

auth.add_route(registerView.as_view(),"/register")


class logoutView(HTTPMethodView):
    async def get(self,request):
        if request['session'].get('user'):
            request['session'].pop("user")
            return redirect("/login")
        else:
            return json({"message":"No Login"})


auth.add_route(logoutView.as_view(),"/logout")


class userProfileView(HTTPMethodView):
    async def get(self,request):
        pass
