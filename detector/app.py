import asyncio
from cassandra.cluster import Cluster
from sanic import Sanic
from consumer import AIOConsumer
from db_services import *


CLUSTER = Cluster(['cassandra'],  port=9042)

while True:
    try:
        SESSION = CLUSTER.connect()
        break
    except Exception as e:
        asyncio.sleep(2)

APP = Sanic(__name__)


@APP.listener('before_server_start')
async def init_db(app, loop):
    if True:
        try:
            await zookeeper_init()
        except Exception as e:
            print("Exception" + str(e))
    # else:
    #     try:
    #         await cassandra_init_table()
    #     except Exception as e:
    #         print("Exception" + str(e))

    # if Configs['OFFSET_DATABASE'] == 'Redis':
    #     pass
    # else:
    #     pass


@APP.listener('after_server_start')
async def start_consumer(app, loop):
    await AIOConsumer.init()


if __name__ == '__main__':
    APP.run(host="0.0.0.0", port=5070)


