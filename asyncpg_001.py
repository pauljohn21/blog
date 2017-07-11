import asyncpg,json
import asyncio
import datetime
async def poast():
    try:
        con = await asyncpg.connect(user="yjgao",password="123456",database="test")
        a = await con.fetch("select id from users where id = 2")
        print(len(a))
    except asyncpg.CannotConnectNowError as e:
        print(e)

asyncio.get_event_loop().run_until_complete(poast())



