import os
import datetime
import binascii
from sanic.response import json,file,redirect
from sanic.views import HTTPMethodView

from . import auth
from ..models import verify,generate_password_hash

class loginView(HTTPMethodView):

    async def get(self,request):
        return await file("app/templates/auth/login.html")


    async def post(self,request):
        async with request.app.pool.acquire() as con:
            if request.form['username'][0] != '' and request.form['password'][0] != '':
                try:
                    user = await con.fetch("select * from users where username = $1",request.form['username'][0])
                    user_dict = dict(user[0])
                    if user and verify(password=request.form.get('password'),password_hash=user_dict['password_hash']):
                        await con.execute("update users set last_login_time = $1,is_active = bool(1) where id = $2",
                                          datetime.datetime.now(),user_dict['id'])
                        _token = binascii.hexlify(os.urandom(16)).decode()
                        response = json(_token + ":" + str(user_dict['id']) )
                        if not request.get('session'):
                            request['session']['session'] = _token
                        return response
                    else:
                        return json({"message":"Fail"})
                except:
                    return json({"message":"Not Exist"})
            else:
                return json({"message":"Empty"})
        await request.app.pool.release()


auth.add_route(loginView.as_view(),"/login")

class registerView(HTTPMethodView):
    async def get(self,request):
        return await file("app/templates/auth/register.html")

    async def post(self,request):
        async with request.app.pool.acquire() as con:
            if request.form['username'][0] != '' and request.form['password'][0] != '':
                try:
                    user = await con.fetchval("select * from users where username = $1", request.form['username'][0])
                    if len(user) > 0:
                        return json({"message":"User Exist"})
                    else:
                        password = generate_password_hash(request.form['password'][0])
                        message =await con.execute("insert into users (username,password_hash) values ($1,$2)",(request.form['username'][0],password))
                        if message == "INSERT 0 1":
                            return json({"message":"Success"})
                        else:
                            return json({"message","Fail"})
                except:
                    return json({"message":"Error"})
            else:
                return json({"message":"Empty"})
        await request.app.pool.release()

auth.add_route(registerView.as_view(),"/register")


class logoutView(HTTPMethodView):
    async def get(self,request):
        async with request.app.pool.acquire() as con:
            user = await con.fetch("select * from users where username = $1",request.form['username'][0])
            await con.execute("update users set is_active = bool(0) where id = $2",id)
        request['session'].pop('session',None)
        url = request.app.url_for('.loginView')
        return redirect(url)


auth.add_route(logoutView.as_view(),"/logout")









