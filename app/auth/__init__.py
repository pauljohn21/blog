from sanic import Blueprint

auth = Blueprint("auth")

from . import views