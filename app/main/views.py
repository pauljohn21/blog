import datetime
from sanic.views import HTTPMethodView
from sanic.response import json,file,redirect

from . import main
from ..utils.to_dict import posts_to_dict
from ..models import pool,release
from ..utils.sql import Main

now = datetime.datetime.now()

class homeView(HTTPMethodView):
    async def get(self,request):
        con = await pool(request.app)
        posts = await con.fetch(Main.get("home_select"))
        posts = posts_to_dict(posts)
        if posts:
            response = json(posts)
            return response
        else:
            return json({"message":"no post"})
        await release(request.app,con)


main.add_route(homeView.as_view(),"/")


class postView(HTTPMethodView):
    async def get(self,request,id):
        con = await pool(request.app)
        post = await con.fetch(Main.get("post_select"),id)
        post = posts_to_dict(post)
        if post:
            return json(post)
        else:
            return json({"message":"post no exist"})
        await release(request.app,con)


    async def put(self,request,id):
            user = request['session'].get('user')
            if user:
                user_id = user.get('id')
                con = await pool(request.app)
                author_id = await con.fetch(Main.get("select_author"),id)
                if len(author_id):
                    if tuple(author_id[0])[0] == user_id:
                        post = request.form.get('post')
                        post_title = request.form.get("post_title")
                        tag = request.form.get("tag")
                        await con.fetch(Main.get("post_update"),post,post_title,tag,now,id)
                        return json({"message":"Success"})
                    else:
                        return json({"message":"Forbid"})

                else:
                    return json({"message":"post not exist"})
                await release(request.app, con)
            else:
                return json({"message":"forbid"})


    async def delete(self, request,id):
        user = request['session'].get('user')
        if user:
            user_id = user.get('id')
            con = await pool(request.app)
            post = await con.fetch(Main.get('post_select'),id)
            if post:
                post = posts_to_dict(post)
                author_id = post['posts'][0].get("author_id")
                if user_id == author_id:
                    await con.fetch(Main.get("post_del"),id)
                else:
                    return json({"messsage":"forbid"})
            else:
                return json({"message":"no post"})
            await release(request.app,con)
        else:
            return json({"message":"please login"})

main.add_route(postView.as_view(),"/post/<id:int>")


class createPostView(HTTPMethodView):
    async def get(self,request):
        user = request['session'].get('user')
        if user:
            return await file("app/templates/posts/post_create.html")
        else:
            return redirect("/login")

    async def post(self,request):
            user = request['session'].get('user')
            if user:
                form = request.form
                _post_title = form.get("post_title")
                _post = form.get("post")
                _user_id = user.get('id')
                _tag = user.get("tag")
                if _post and _post_title and _user_id:
                    con = await pool(request.app)
                    await con.fetch(Main.get("create_post"),_post_title,_post,_user_id,now,now,_tag)
                    return json({"message":"Success"})
                    await release(request.app,con)
                else:
                    return json({"message":"post is null"})
            else:
                return redirect("/login")

main.add_route(createPostView.as_view(),"/post/create")


