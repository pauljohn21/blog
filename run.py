from app import create_app
from app.models import connect_db,close_db


app = create_app()


@app.listener("before_server_start")
async def connect_database(app,loop):
    app.pool = await connect_db(app,loop)


@app.listener("after_server_stop")
async def stop_db(app,loop):
    await close_db(app,loop)


if __name__ == "__main__":
    app.run(debug=True,host='172.20.3.206',port=8080)





