import datetime
from sanic.response import json,file,redirect,html
from sanic.views import HTTPMethodView

from . import auth
from ..models import verify,generate_password_hash,pool,release
from ..utils.to_dict import user_to_dict
from ..utils.sql import Auth
from ..utils.transfer_verify import user_verify

now_time = datetime.datetime.now()

class loginView(HTTPMethodView):

    async def get(self,request):
        try:
            user = request['session']['user']
            if user:
                return redirect('/')
        except:
            return await file("app/templates/auth/login.html")


    async def post(self,request):
        try:
            username = request.form.get('username')
            password = request.form.get('password')
            if username and password :
                con = await pool(request.app)
                get_user = await con.fetch(Auth.get('select_user'),username)
                user = user_to_dict(get_user)
                password_hash = user['users'][0].get('password_hash')
                id = user['users'][0].get('id')
                if user and verify(password=password,password_hash=password_hash):
                    await con.execute(Auth.get('login_update'),now_time,id)
                else:
                    return json({"message": "Fail"})
                await release(request.app,con)
        except Exception as e:
            return json({"message":e})
        if not request['session'].get('user'):
            request['session']['user'] =  {"id":id,"username":username}
            return json({"message":"success"})


auth.add_route(loginView.as_view(),"/login")

class registerView(HTTPMethodView):
    async def get(self,request):
        return await file("app/templates/auth/register.html")

    async def post(self,request):
        try:
            username = request.form['username'][0]
            password = request.form['password'][0]
            if password and username :
                con = await pool(request.app)
                select_user = await con.fetchval(Auth.get('select_user'),username)
                if select_user:
                    return json({"message":"Exist"})
                else:
                    password_hash = generate_password_hash(password)
                    await con.execute(Auth.get('register_insert'),username,password_hash,now_time,now_time)
                    return json({"message":"Success"})
                await release(request.app, con)
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

class userprofileView(HTTPMethodView):
    async def get(self,request):
        if request['session'].get('user'):
            id = request['session']['user'].get('id')
            con = await pool(request.app)
            get_user  = con.fetch(Auth.get("select_user_profile"),id)
            users = user_to_dict(get_user)
            return json(users)
            await release(request.app,con)
        else:
            return json({"message":"please login"})

    async def post(self,request):
        if request['session'].get('user'):
            id = request['session']['user'].get('id')
            con = await pool(request.app)
            user = user_verify(request.form)
            location = user.get('location')
            levemessage = user.get('levemessage')
            await con.fetch(Auth.get("update_user_profile"),location,levemessage,id)
            return json({"message":"update success"})
        else:
            return json({"message":"please login"})

auth.add_route(userprofileView.as_view(),"/user/profile/")




