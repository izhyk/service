from aiopg.sa import create_engine
from consumer import APP, SESSION
from consumer.tables import messages_pg


KEYSPACE = "service"


async def pg_create_engine():
    return await create_engine(**APP.config.POSTGRES)


async def pg_init_table():
    engine = await pg_create_engine()
    async with engine.acquire() as conn:
        await conn.execute('DROP TABLE IF EXISTS messages')
        await conn.execute('''CREATE TABLE messages (
                                  id serial PRIMARY KEY,
                                  message varchar(255),
                                  date timestamp)''')


async def pg_insert(msg):
    engine = await pg_create_engine()
    async with engine.acquire() as conn:
        await conn.execute(messages_pg.insert().values(message=msg))


async def cassandra_init_table():
    SESSION.execute("""
            CREATE KEYSPACE IF NOT EXISTS %s
            WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
            """ % KEYSPACE)

    SESSION.set_keyspace(KEYSPACE)
    SESSION.execute("""CREATE TABLE IF NOT EXISTS cassandra_table ( id text PRIMARY KEY, message text)""")


async def cassandra_insert(id_offset, msg):
    SESSION.execute("INSERT INTO cassandra_table (id, message) VALUES (%s, %s)", [id_offset, msg,])


