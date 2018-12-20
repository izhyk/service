import os
import json
from sanic import Sanic
from kafka import KafkaProducer
from sanic_redis import SanicRedis


TRANSACTIONS_TOPIC = os.environ.get('TRANSACTIONS_TOPIC')
KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
TRANSACTIONS_PER_SECOND = float(os.environ.get('TRANSACTIONS_PER_SECOND'))

APP = Sanic()

APP.config.producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        value_serializer=lambda value: json.dumps(value).encode(),
    )
APP.config.update(
    {
        'REDIS': {
            'address': ('redis', 6379),
            'db': 1,
        }
    }
)
redis = SanicRedis(APP)

from .routers import *
