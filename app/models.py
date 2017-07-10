import asyncpg
from .utils.security import generate_password_hash,verify_password

async def connect_db(app,loop):
    global _pool
    _pool = await asyncpg.create_pool(user="yjgao",password="123456",database="test")
    return _pool


async def close_db(app,loop):
    await _pool.close()

async def pool(app):
    con = await app.pool.require()
    return con

async def release(app,con):
    await app.pool.release(con)


@property
def password():
    raise AttributeError("password cannot read")

@password.setter
def password(password):
        return generate_password_hash(password=password)


def verify(password,password_hash):
    return verify_password(password=password,password_hash=password_hash)


