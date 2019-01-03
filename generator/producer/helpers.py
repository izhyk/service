from aiokafka import AIOKafkaProducer
from producer import KAFKA_BROKER_URL
import json


async def send_one(loop, message):
    # TODO: remove producer from this place
    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        value_serializer=lambda value: json.dumps(value).encode(),
        loop=loop,
    )
    await producer.start()
    try:
        await producer.send_and_wait("my-topic", message)
    finally:
        await producer.stop()
