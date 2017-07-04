import time
from sanic import response
from sanic.views import HTTPMethodView

from . import auth
from ..models import verify,generate_password_hash

class loginView(HTTPMethodView):

    async def get(self,request):
        return await response.file("app/templates/auth/login.html")


    async def post(self,request):
        async with request.app.pool.acquire() as con:
            if request.form['username'][0] != '' and request.form['password'][0] != '':
                try:
                    user = await con.fetch("select * from users where username = $1",request.form['username'][0])
                    user_dict = dict(user[0])
                    if user and verify(password=request.form['password'][0],password_hash=user_dict['password_hash']):
                        return response.json({"message":"Success","status":200,"resault":{"user":user_dict['username']}})
                    else:
                        return response.json({"message":"Fail"})
                except:
                    return response.json({"message":"Not Exist"})
                await request.app.release()
            else:
                return response.json({"message":"Empty"})


auth.add_route(loginView.as_view(),"/login")

class registerView(HTTPMethodView):
    async def get(self,request):
        return response.file("app/templates/auth/register.html")

    async def post(self,request):
        async with request.app.pool.acquire() as con:
            if request.form['username'][0] != '' and request.form['password'][0] != '':
                try:
                    user = await con.fetchval("select * from users where username = $1", request.form['username'][0])
                    if len(user) > 0:
                        return response.json({"message":"User Exist"})
                    else:
                        password = generate_password_hash(request.form['password'][0])
                        message =await con.execute("insert into users (username,password_hash) values ($1,$2)",(request.form['username'][0],password))
                        if message == "INSERT 0 1":
                            return response.json({"message":"Success"})
                        else:
                            return response.json({"message","Fail"})
                except:
                    return response.json({"message":"Error"})
            else:
                return response.json({"message":"Empty"})

