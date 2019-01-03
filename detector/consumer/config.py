import os

KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')

Configs = {
    'DATABASE': os.environ.get('DATABASE') or 'Postgres',
    'CASSANDRA_HOST': os.environ.get('CASSANDRA_HOST') or 'cassandra',
    'MESSAGE_DATABASE': 'Postgres'
}
