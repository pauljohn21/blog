from sanic import request,response
from . import main
from sanic.views import HTTPMethodView


class homeView(HTTPMethodView):
    async def get(self,request):
        pass



    async def post(self,request):
        pass






