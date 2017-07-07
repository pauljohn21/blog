from sanic.views import HTTPMethodView
from sanic.response import json,file

from . import main
from ..utils.to_dict import posts_to_dict


class homeView(HTTPMethodView):
    async def get(self,request):
        try:
            user = request.sessions.get['user']
            _pool = request.app.pool
            async with _pool.acquire() as con:
                id = await con.fetch("select id from users where username = $1",
                                           user.get('username'))
                if tuple(id[0])[0] == user.get('id'):
                    posts = await con.fetch("select * from posts,users where author_id = $1",
                                              user.get('id'))
                    posts_dict = posts_to_dict(posts)
                    response = json.dumps(posts_dict)
                    return response
                else:
                    return json({"message":"Id Not Match Username"})
            await _pool.release(con)
        except Exception as e:
            return json({"message":e})

    async def delete(self,request):
        try:
            self.

main.add_route(homeView.as_view(),"/")


class postView(HTTPMethodView):
    async def get(self,request,id):

        '''这里还有问题
        '''
        try:
            self.user = request.sessions.get['user']
            Pool = request.app.pool
            async with Pool.acquire() as con:
                    post = await con.fetch("select * from posts where id = $1",id)
                    post_dict = posts_to_dict(post)
                    response = json.dumps(post_dict)
                    return response
            await request.app.pool.release(con)
        except Exception as e:
            return json({"message":e})

    async def put(self,request,id):
        try:
            if request.sessions.get('user'):
                user_id  = request.sessions.['user'].get('id')
                pool = request.app.pool
                async with pool.acquire() as con:
                    author = await con.fetch("select author_id from post where id = $1",id)
                    author_id = tuple(author[0])[0]
                    if author_id == user_id:
                        post = request.form.get('post')[0]
                        post_title = request.form.get("post_title")[0]
                        tag = request.form.get("tag")[0]
                        await con.fetch("update posts set post = $1,post_title = $2,tag = $3 where id = $4",
                                        post,post_title,tag,id)
                        return json({"message":"Success"})
                    else:
                        return json({"message":"Forbid"})
                await pool.release(con)
        except Exception as e:
            return json({"message":e})


main.add_route(postView.as_view(),"/post/<id:int>")


class createPostView(HTTPMethodView):
    async def get(self,request):
        return file("app/templates/post_create.html")

    async def post(self,request):
        try:
            user = request.sessions.get('user')
            form = request.form
            _post_title = form.get("post_title")
            _post = form.get("post")
            _user_id = user.get('id')
            _pool = request.app.pool
            async with _pool.acquire() as con:
                user = await con.fetch("select * from users where id = $1",_user_id)
                if len(user):
                    await con.fetch("insert into posts (post_title,post,author_id) values ($1,$2,$3)",
                                      _post_title,_post,_user_id)
                    return json({"message":"Success"})
                else:
                    return json({404})
            await _pool.release(con)
        except Exception as e:
            return json({"message":e})

main.add_route(createPostView.as_view(),"/post/create")


