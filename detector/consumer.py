from aiokafka import AIOKafkaConsumer
import json
import os
import logging
from db_services import *

KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
MESSAGE_DB = os.environ.get('MESSAGE_DB')
OFFSET_DB = os.environ.get('OFFSET_DB')


class AIOConsumer:

    number_of_messages = 0
    time_last_commit = 0
    consumer: AIOKafkaConsumer

    @classmethod
    async def init(cls):
        cls.consumer = AIOKafkaConsumer(
            'my-topic',
            bootstrap_servers=KAFKA_BROKER_URL,
            loop=asyncio.get_event_loop(),
            value_deserializer=lambda value: json.loads(value),
            enable_auto_commit=False,
            group_id="my-group"
        )

        while True:
            try:
                await cls.consumer.start()
                break
            except Exception as e:
                asyncio.sleep(1)
        try:
            asyncio.ensure_future(cls.commit_per_second())

            async for msg in cls.consumer:
                cls.number_of_messages += 1
                # await cls.write_to_db(msg.offset, msg.value)
                if cls.number_of_messages >= 10:
                    cls.consumer.commit()
                    cls.number_of_messages = 0
                    cls.time_last_commit = time.time()
                    print('consumer' + str(msg.value))
                    logging.info('kafka consumer commit')
        finally:
            logging.info('kafka consumer stop')
            await cls.consumer.stop()

    @classmethod
    async def commit_per_second(cls):
        while True:
            time_diff = time.time() - cls.time_last_commit
            if time_diff > 10:
                cls.consumer.commit()
                cls.number_of_messages = 0
                cls.time_last_commit = time.time()
                logging.info('kafka consumer commit')
            else:
                await asyncio.sleep(10 - time_diff)

    @classmethod
    async def write_to_db(cls, offset, msg):

        if MESSAGE_DB == 'cassandra':
            await cassandra_insert(str(offset), msg)
            logging.info('write message to cassandra')
        else:
            await pg_insert(offset, msg)
            logging.info('write message to postgres')

        if OFFSET_DB == 'zookeeper':
            await zookeeper_insert(offset)
            logging.info('write offset to zookeeper')
        else:
            logging.info('write offset to redis')
            await redis_set(offset)




