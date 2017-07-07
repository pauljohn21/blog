import asyncio
import asyncpg
import json


async def main():
    conn = await asyncpg.connect(user="yjgao",password="123456",database="test")

    try:
        def _encoder(value):
            return json.dumps(value).encode('utf-8')

        def _decoder(value):
            return json.loads(value.decode('utf-8'))

        await conn.set_type_codec(
            'json', encoder=_encoder, decoder=_decoder,
            schema='pg_catalog', binary=True
        )

        data = {'foo': 'bar', 'spam': 1}
        res = await conn.fetchval('SELECT * from', data)

    finally:
        await conn.close()

asyncio.get_event_loop().run_until_complete(main())