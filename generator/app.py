"""Produce fake transactions into a Kafka topic."""

import os
import json
from sanic import Sanic

from kafka import KafkaProducer
from sanic.response import json as s_json
from sanic_redis import SanicRedis

from transactions import create_random_transaction

TRANSACTIONS_TOPIC = os.environ.get('TRANSACTIONS_TOPIC')
KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
TRANSACTIONS_PER_SECOND = float(os.environ.get('TRANSACTIONS_PER_SECOND'))

app = Sanic()
app.config.producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        value_serializer=lambda value: json.dumps(value).encode(),
    )
app.config.update(
    {
        'REDIS': {
            'address': ('redis', 6379),
            'db': 1,
        }
    }
)

redis = SanicRedis(app)


@app.route("/")
async def test(request):
    with await redis.conn as r:
        await r.set('key', 'value1')
        result = await r.get('key')
    return result
    producer = request.app.config.producer
    transaction: dict = create_random_transaction()
    producer.send(TRANSACTIONS_TOPIC, value=transaction)
    return s_json(transaction)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5050)
    # for i in range(5):
    #     transaction: dict = create_random_transaction()
    #     producer.send(TRANSACTIONS_TOPIC, value=transaction)
    #     print(transaction)  # DEBUG


