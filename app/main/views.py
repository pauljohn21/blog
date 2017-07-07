from sanic.views import HTTPMethodView
from sanic.response import json


from . import main
from ..utils.to_dict import posts_to_dict


class homeView(HTTPMethodView):
    async def get(self,request):
        try:
            with request.sessions.get['user'] as sessions:
                async with request.app.pool.acquire() as con:
                    id = await con.fetch("select id from users where username = $1",
                                               sessions.get('username'))
                    if tuple(id[0])[0] == sessions.get('id'):
                        posts = await con.fetch("select * from posts,users where author_id = $1",
                                                  sessions.get('id'))
                        response = json.dumps(posts_to_dict(posts))
                        return response
                    else:
                        return json({"message":"Id Not Match Username"})
                await request.app.pool.release(con)
        except Exception as e:
            return json({"message":e})



    async def post(self,request):
        if request.form.get('post_title') == '' or request.form.get('post') == '':
            async with request.app.pool.acquire() as con:
                await con.execute("insert into posts (post_title,post,author_id",
                                  request.form.get("post_title"),request.form.get("post"),request.sessions['user'].get('id'))
                return json({"message":"Success"})
            await request.app.pool.release(con)
        else:
            return json({"message":"Empty"})


main.add_route(homeView.as_view(),"/")


class postView(HTTPMethodView):
    async def get(self,request,id):
        if request.sessions.get['user']:
            async with request.app.pool.acquire() as con:
                post = await con.fetch("select * from posts where id = $1",id)
                post_dict = posts_to_dict(post)
                response = json.dumps(post_dict)
                return response
            await request.app.pool.release(con)




main.add_route(postView.as_view(),"/post/<id:int>")
