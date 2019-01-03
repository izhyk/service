from sanic import Sanic
from .config import Configs
from cassandra.cluster import Cluster

CLUSTER = Cluster(contact_points=['cassandra'],
                  port=9042)

SESSION = CLUSTER.connect()

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

