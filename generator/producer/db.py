import asyncio
from aiopg.sa import create_engine


async def main():
    async with create_engine(user='postgres',
                             database='postgres',
                             host='postgres',
                             password='postgres') as engine:
        await create_table(engine)


async def create_table(engine):
    async with engine.acquire() as conn:
        await conn.execute('DROP TABLE IF EXISTS messages')
        await conn.execute('''CREATE TABLE messages (
                                  id serial PRIMARY KEY,
                                  message varchar(255))''')

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
