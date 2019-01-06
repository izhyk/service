from aiokafka import AIOKafkaConsumer
import json
import os
from db_services import *


KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')


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
                # assert False, (msg.value)
                await cls.write_to_db(msg.offset, msg.value)
                if cls.number_of_messages >= 10:
                    cls.consumer.commit()
                    cls.number_of_messages = 0
                    cls.time_last_commit = time.time()
                print("consumed: ", msg.topic, msg.partition, msg.offset,
                      msg.key, msg.value, msg.timestamp)
        finally:
            await cls.consumer.stop()

    @classmethod
    async def commit_per_second(cls):
        while True:
            time_diff = time.time() - cls.time_last_commit
            if time_diff > 10:
                cls.consumer.commit()
                cls.number_of_messages = 0
                cls.time_last_commit = time.time()
            else:
                await asyncio.sleep(10 - time_diff)

    @classmethod
    async def write_to_db(cls, offset, msg):
        # await zookeeper_insert(offset)
        # await redis_set(offset)
        await pg_insert(offset, msg)
        # await cassandra_insert(str(offset), msg)



