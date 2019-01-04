from aiokafka import AIOKafkaConsumer
import asyncio
import json
import os
from time import time

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
            auto_offset_reset='earliest',
            group_id="my-group"
        )

        await cls.consumer.start()
        try:
            await asyncio.ensure_future(cls.commit_per_second())

            async for msg in cls.consumer:
                cls.number_of_messages += 1
                if cls.number_of_messages >= 10:
                    cls.consumer.commit()
                    cls.number_of_messages = 0
                    cls.time_last_commit = time()
                print("consumed: ", msg.topic, msg.partition, msg.offset,
                      msg.key, msg.value, msg.timestamp)
        finally:
            await cls.consumer.stop()

    @classmethod
    async def commit_per_second(cls):
        while True:
            print('I am in second func')
            time_diff = time() - cls.time_last_commit
            if time_diff > 10:
                cls.consumer.commit()
                cls.number_of_messages = 0
                cls.time_last_commit = time()
            await asyncio.sleep(10 - time_diff)


