from consumer import APP
from consumer.config import Configs
from consumer.consumer import AIOConsumer
from consumer.db_services import *


@APP.listener('before_server_start')
async def init_db(app, loop):
    if Configs['MESSAGE_DATABASE'] == 'Postgresewwer':
        try:
            await pg_init_table()
        except Exception as e:
            print("Exception" + str(e))
    else:
        try:
            await cassandra_init_table()
        except Exception as e:
            print("Exception" + str(e))

    # if Configs['OFFSET_DATABASE'] == 'Redis':
    #     pass
    # else:
    #     pass


@APP.listener('after_server_start')
async def start_consumer(app, loop):
    await AIOConsumer.init()
