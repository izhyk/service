import json
from kafka import KafkaProducer
from aiopg.sa import create_engine
from sanic.response import json as s_json
from producer import APP, KAFKA_BROKER_URL
from producer.tables import messages
from aiokafka import AIOKafkaProducer
import asyncio


@APP.route("/producer")
async def test(request):
    async def send_one():
        producer = AIOKafkaProducer(
            loop=asyncio.get_event_loop(), bootstrap_servers='kafka:9092')
        await producer.start()
        try:
            await producer.send_and_wait("my-topic", b"Super message")
        finally:
            await producer.stop()

    asyncio.get_event_loop().run_until_complete(send_one())

    return s_json({'hello world'})


@APP.route("/write")
async def write(request):
    async with create_engine(**APP.config.POSTGRES) as engine:
        async with engine.acquire() as conn:
            await conn.execute(messages.insert().values(message='new message'))
    return s_json({'writed'})


