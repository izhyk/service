import json
from kafka import KafkaProducer
from aiopg.sa import create_engine
from sanic.response import json as s_json
from producer import APP, KAFKA_BROKER_URL
from producer.tables import messages


@APP.route("/producer")
async def test(request):
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        value_serializer=lambda value: json.dumps(value).encode(),
        batch_size=0,
        linger_ms=10
    )

    for i in range(100):
        producer.send('my-topic', value='version ' + str(i) + '.0')

    producer.flush()

    return s_json({'hello world'})


@APP.route("/write")
async def write(request):
    async with create_engine(**APP.config.POSTGRES) as engine:
        async with engine.acquire() as conn:
            await conn.execute(messages.insert().values(message='new message'))
    return s_json({'writed'})


