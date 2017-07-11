import datetime
from sanic.views import HTTPMethodView
from sanic.response import json,file,redirect

from . import main
from ..utils.to_dict import posts_to_dict,comments_to_dict
from ..models import pool,release
from ..utils.sql import Main


class homeView(HTTPMethodView):

    async def get(self,request):
        con = await pool(request.app)
        posts = await con.fetch(Main.get("home_select"))
        posts = posts_to_dict(posts)
        await release(request.app,con)
        if posts:
            response = json(posts)
            return response
        else:
            return json({"message":"no post"})


main.add_route(homeView.as_view(),"/")


class postView(HTTPMethodView):

    async def get(self,request,id):
        con = await pool(request.app)
        post = await con.fetch(Main.get("post_select"),id)
        post = posts_to_dict(post)
        if post:
            comments = await con.fetch(Main.get("select_post_comments"), id)
            comments = comments_to_dict(comments)
            post.update(comments)
            await release(request.app, con)
            return json(post)
        else:
            return json({"message":"post no exist"})


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
                        now = datetime.datetime.now()
                        await con.fetch(Main.get("post_update"),post,post_title,tag,now,id)
                        await release(request.app, con)
                        return json({"message":"Success"})
                    else:
                        return json({"message":"Forbid"})

                else:
                    return json({"message":"post not exist"})
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
                    await release(request.app, con)

                else:
                    return json({"messsage":"forbid"})
            else:
                return json({"message":"no post"})
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
                    now = datetime.datetime.now()
                    await con.fetch(Main.get("create_post"),_post_title,_post,_user_id,now,now,_tag)
                    await release(request.app,con)
                    return json({"message":"Success"})
                else:
                    return json({"message":"post is null"})
            else:
                return redirect("/login")

main.add_route(createPostView.as_view(),"/post/create")


class createCommentView(HTTPMethodView):

    async def post(self,request,post_id):
        user = request['session'].get('user')
        if user:
            comment = request.form.get('comment')
            if comment:
                user_id = user.get("id")
                con = await pool(request.app)
                now = datetime.datetime.now()
                await con.fetch(Main.get('create_comment'),comment,post_id,user_id,now,now)
                await release(request.app,con)
                return json({"message":"success"})
            else:
                return json({"message":"comment is empty"})
        else:
            return redirect("/login")

main.add_route(createCommentView.as_view(),"/post/<post_id:int>/comment/")

class commentView(HTTPMethodView):

    async def put(self, request,com_id):
        user = request['session'].get('user')
        if user:
            comment = request.form.get('comment')
            if comment:
                con = await pool(request.app)
                author = await con.fetch(Main.get("select_comment_author"),com_id)
                user_id = user.get('id')
                if author:
                    if tuple(author[0])[0] == user_id:
                        now = datetime.datetime.now()
                        await con.fetch(Main.get("update_comment"),comment,now,com_id)
                        await release(request.app, con)
                        return json({"message":"success"})
                    else:
                        return json({"message":"forbid"})
                else:
                    return json({"message":"comment is delete"})
            else:
                return json({"message":"comment is empty"})
        else:
            return json({"message":"please to login"})

    async def delete(self, request,com_id):
        user = request['session'].get('user')
        if user:
            con = await pool(request.app)
            author = await con.fetch(Main.get("select_comment_author"),com_id)
            user_id = user.get('id')
            if len(author):
                if tuple(author[0])[0] == user_id:
                    await con.fetch(Main.get("delete_comment"),com_id)
                    await release(request.app, con)
                    return json({"message": "success"})
                else:
                    return json({"message": "forbid"})
            else:
                return json({"message":"already delete"})
        else:
            return json({"message":"please to login"})

main.add_route(commentView.as_view(),"/comment/<com_id:int>/")


