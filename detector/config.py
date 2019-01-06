import os
from app import APP

KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')

APP.config.update(
    {
        'POSTGRES': {
            'user': 'postgres',
            'database': 'postgres',
            'host': 'postgres',
            'password': 'postgres'
        }
    }
)
