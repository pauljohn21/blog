from app import create_app
from app.models import connect_db,close_db
from sanic_session import InMemorySessionInterface


app = create_app()
redis_interface = InMemorySessionInterface()


@app.listener("before_server_start")
async def connect_database(app,loop):
    app.pool = await connect_db(app,loop)

@app.listener("after_server_stop")
async def stop_db(app,loop):
    await close_db(app,loop)

@app.middleware("request")
async def session_create(request):
    await redis_interface.open(request)

@app.middleware("response")
async def session_save(request,response):
    await redis_interface.save(request,response)

if __name__ == "__main__":
    app.run(debug=True)





