import asyncpg,json
import asyncio,datetime


async def poast():
    try:
        con = await asyncpg.connect(user="yjgao",password="123456",database="test")
        a = await con.execute("insert into users (username,password_hash) values ('xiezhaowei','123456')")
        b = a.split(" ")
        print(a)
    except asyncpg.CannotConnectNowError as e:
        print(e)

asyncio.get_event_loop().run_until_complete(poast())