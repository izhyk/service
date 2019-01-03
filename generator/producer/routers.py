import json
from kafka import KafkaProducer
from aiopg.sa import create_engine
from sanic.response import json as s_json
from producer import APP, KAFKA_BROKER_URL
from producer.tables import messages
from aiokafka import AIOKafkaProducer
import asyncio

loop = asyncio.get_event_loop()


@APP.route("/producer")
async def test(request):
    loop = asyncio.get_event_loop()
    await send_one(loop)
    return s_json({'hello world'})


async def send_one(loop):
        producer = AIOKafkaProducer(
            loop=loop, bootstrap_servers='kafka:9092',
            )
        await producer.start()
        try:
            await producer.send_and_wait("my-topic", b"Super message")
            print('sended')
        finally:
            await producer.stop()


@APP.route("/write")
async def write(request):
    async with create_engine(**APP.config.POSTGRES) as engine:
        async with engine.acquire() as conn:
            await conn.execute(messages.insert().values(message='new message'))
    return s_json({'writed'})


