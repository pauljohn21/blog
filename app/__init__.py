from sanic import Sanic

from .auth import auth
from .main import main

def create_app():
    app = Sanic(__name__)
    app.blueprint(auth)
    app.blueprint(main)
    return app


