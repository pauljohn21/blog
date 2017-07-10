from sanic import Blueprint

api_v01 = Blueprint("api",url_prefix="api_v01")

from . import users