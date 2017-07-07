import asyncpg,json
import asyncio
import datetime
async def poast():
    try:
        con = await asyncpg.connect(user="yjgao",password="123456",database="test")
        a = await  con.fetch("select id from users where username = 'uu'")
        c = len(a)
        print(a)
    except asyncpg.CannotConnectNowError as e:
        print(e)

asyncio.get_event_loop().run_until_complete(poast())



