import asyncpg,json
import asyncio,datetime


async def poast():
    try:
        con = await asyncpg.connect(user="yjgao",password="123456",database="test")
        a = await  con.execute("update users set last_login_time = $1 where id = $2",
                               datetime.datetime.now(),1)
        b = a.split(" ")
        print(a)
    except asyncpg.CannotConnectNowError as e:
        print(e)

asyncio.get_event_loop().run_until_complete(poast())