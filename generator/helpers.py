from aiokafka import AIOKafkaProducer
from app import KAFKA_BROKER_URL
import json


async def send_one(loop, message):
    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        value_serializer=lambda value: json.dumps(value).encode(),
        loop=loop,
    )
    await producer.start()
    try:
        for i in range(100):
            await producer.send_and_wait("my-topic", message)
            print(message)
    finally:
        await producer.stop()
