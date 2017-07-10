from sanic import Sanic

from .auth import auth
from .main import main
from .api_v01 import api_v01

def create_app():
    app = Sanic(__name__)
    app.blueprint(auth)
    app.blueprint(main)
    app.blueprint(api_v01,url_prefix="api_v01")
    return app


