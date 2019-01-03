from aiokafka import AIOKafkaConsumer
import os
from consumer.config import Configs
import asyncio
import json

KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')

class Consumer:

    AIOConsumer: AIOKafkaConsumer = None
    message_number: int = 0

    @classmethod
    async def init(cls, seconds, count):
        cls.AIOConsumer = AIOKafkaConsumer(
            'my-topic',
            bootstrap_servers=KAFKA_BROKER_URL,
            loop=asyncio.get_event_loop(),
            value_deserializer=lambda value: json.loads(value),
            enable_auto_commit=False,
            group_id="my-group"
            )
        print('here')
        while True:
            try:
                await cls.AIOConsumer.start()
                cls._commit = asyncio.ensure_future(cls.commit_per_second(seconds))
                cls._commit = asyncio.ensure_future(cls.commit_per_message(count))
                break
            except Exception as e:
                print("Error " + str(e))
                await asyncio.sleep(1)

    @classmethod
    async def run_consumer(cls):
        print('run_consumer')
        await cls.init(seconds=10, count=10)
        async for msg in cls.AIOConsumer:
            cls.message_number += 1
            await cls.write_to_db('my-topic', message=msg.value, offset=msg.offset)

    @classmethod
    async def commit_per_second(cls, second):
        while True:
            await asyncio.sleep(second)
            cls.AIOConsumer.commit()
            cls.message_number = 0

    @classmethod
    async def commit_per_message(cls, count):
        while True:
            if cls.message_number >= count:
                cls.AIOConsumer.commit()
                cls.message_number = 0
            await asyncio.sleep(.2)

    @classmethod
    async def write_to_db(cls, topic, message, offset):
        if True:
            print(message)
        # else:
        #     print('57')

        # if Configs['OFFSET_DATABASE'] == 'Redis':
        #     print('57')
        # else:
        #     print('57')

