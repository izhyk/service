from aiopg.sa import create_engine
from consumer import APP, SESSION
from consumer.tables import messages_pg
from consumer.config import Configs


class PostgresService:
    @classmethod
    async def create_engine(cls):
        return await create_engine(**APP.config.POSTGRES)

    @classmethod
    async def init_table(cls):
        engine = await cls.create_engine()
        async with engine.acquire() as conn:
            await conn.execute('DROP TABLE IF EXISTS messages')
            await conn.execute('''CREATE TABLE messages (
                                      id serial PRIMARY KEY,
                                      message varchar(255),
                                      date timestamp)''')

    @classmethod
    async def postgres_insert(cls, msg):
        engine = await cls.create_engine()
        async with engine.acquire() as conn:
            await conn.execute(messages_pg.insert().values(msg='new message'))


class CassandraService:
    @classmethod
    async def init_table(cls):
        SESSION.set_keyspace('service')
        SESSION.execute(""" CREATE TABLE IF NOT EXISTS cassandra_table (
                                id int,
                                message text,
                                date timestamp,
                                PRIMARY KEY (id)
                            )
                            """)

    @classmethod
    async def cassandra_insert(cls, id, message):
        try:
            SESSION.execute_async("INSERT INTO cassandra_table (id, message) VALUES (%s, %s)",
                                  (id, message)).result()
        except Exception as e:
            print('Exception' + str(e))
