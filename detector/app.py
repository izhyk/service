import logging
from cassandra.cluster import Cluster
from sanic import Sanic
import yaml
import asyncio
import consumer
import os
from db_services import *

CLUSTER = Cluster(['cassandra'],  port=9042)
MESSAGE_DB = os.environ.get('MESSAGE_DB')
OFFSET_DB = os.environ.get('OFFSET_DB')

# create logger with 'spam_application'
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('consumer.txt')
fh.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.error('test error')


while True:
    try:
        SESSION = CLUSTER.connect()
        break
    except Exception as e:
        asyncio.sleep(2)

APP = Sanic(__name__)

with open('config.yaml', 'r') as stream:
    config = yaml.load(stream)

APP.config.update(config)


@APP.listener('before_server_start')
async def init_db(app, loop):
    if MESSAGE_DB == 'cassandra':
        try:
            await cassandra_init_table()
            logging.info('cassandra table initialized')
        except Exception as e:
            logging.error('cassandra error ' + str(e))
    else:
        try:
            await pg_init_table()
            logging.info('postgres table initialized')
        except Exception as e:
            logging.error('postgres error ' + str(e))

    if OFFSET_DB == 'zookeeper':
        try:
            # await zookeeper_init()
            logging.info('zookeeper initialized')
        except Exception as e:
            logging.error('zookeeper error ' + str(e))


@APP.listener('after_server_start')
async def start_consumer(app, loop):
    await consumer.AIOConsumer.init()


if __name__ == '__main__':
    APP.run(host="0.0.0.0", port=5070)


