import os
from sanic import Sanic
from sanic_redis import SanicRedis

TRANSACTIONS_TOPIC = os.environ.get('TRANSACTIONS_TOPIC')
KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')

APP = Sanic()

APP.config.update(
    {
        'REDIS': {
            'address': ('redis', 6379),
            'db': 1,
        },

        'POSTGRES': {
            'user': 'postgres',
            'database': 'postgres',
            'host': 'postgres',
            'password': 'postgres'
        }
    }
)
redis = SanicRedis(APP)


from .routers import *
