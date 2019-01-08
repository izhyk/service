from aiopg.sa import create_engine
from app import APP, SESSION
import asyncio
import time
import aiozk
import aioredis
import asyncio
from tables import messages_pg


KEYSPACE = "service"


async def pg_create_engine():
    return await create_engine(**APP.config.postgres)


async def pg_init_table():
    engine = await pg_create_engine()
    async with engine.acquire() as conn:
        await conn.execute('DROP TABLE IF EXISTS messages')
        await conn.execute('''CREATE TABLE messages (
                                  id serial PRIMARY KEY,
                                  message varchar(255),
                                  date timestamp)''')


async def pg_insert(offset, msg):
    engine = await pg_create_engine()
    async with engine.acquire() as conn:
        await conn.execute(messages_pg.insert().values(id=offset, message=msg,))


async def cassandra_init_table():
    SESSION.execute("""
            CREATE KEYSPACE IF NOT EXISTS %s
            WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
            """ % KEYSPACE)

    SESSION.set_keyspace(KEYSPACE)
    SESSION.execute("""CREATE TABLE IF NOT EXISTS cassandra_table ( id text PRIMARY KEY, message text)""")


async def cassandra_insert(id_offset, msg):
    SESSION.execute("INSERT INTO cassandra_table (id, message) VALUES (%s, %s)", [id_offset, msg,])


async def redis_set(offset):
    redis = await aioredis.create_redis(
        'redis://redis:6379', loop=asyncio.get_event_loop())
    await redis.set('offset_id', offset)
    redis.close()
    await redis.wait_closed()


async def zookeeper_init():
    while True:
        try:
            zkp = aiozk.ZKClient("zookeeper:2181", loop=asyncio.get_event_loop())
            break
        except Exception as e:
            print(e)
            time.sleep(1)
    await zkp.start()
    try:
        await zkp.ensure_path("/offset")
    except Exception as err:
        await zkp.create(path="/offset", data=b"null", ephemeral=True)
        zkp.close()


async def zookeeper_insert(offset_id):
    zkp = aiozk.ZKClient("zookeeper:2181", loop=asyncio.get_event_loop())
    await zkp.start()
    try:
        await zkp.set_data(path="/offset", data=str(offset_id).encode())
    finally:
        zkp.close()
