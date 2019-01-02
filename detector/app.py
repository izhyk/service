import os
import json
from kafka import KafkaConsumer
from aiokafka import AIOKafkaConsumer
from sanic import Sanic
import asyncio

KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()


    async def consume():
        consumer = AIOKafkaConsumer(
            'my-topic',
            loop=loop, bootstrap_servers='kafka:9092',
            )
        # Get cluster layout and join group `my-group`
        await consumer.start()
        try:
            # Consume messages
            async for msg in consumer:
                print("consumed: ", msg.topic, msg.partition, msg.offset,
                      msg.key, msg.value, msg.timestamp)
        finally:
            # Will leave consumer group; perform autocommit if enabled.
            await consumer.stop()


    loop.run_until_complete(consume())

