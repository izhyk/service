from sanic import Sanic
from .config import Configs
import asyncio
from cassandra.cluster import Cluster

CLUSTER = Cluster(['cassandra'],
                  port=9042)

while True:
    try:
        SESSION = CLUSTER.connect()
        break
    except Exception as e:
        asyncio.sleep(2)

APP = Sanic(__name__)

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

from .routers import *

