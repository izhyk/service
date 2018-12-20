import os
import json
from kafka import KafkaConsumer

KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
TRANSACTIONS_TOPIC = os.environ.get('TRANSACTIONS_TOPIC')
LEGIT_TOPIC = os.environ.get('LEGIT_TOPIC')
FRAUD_TOPIC = os.environ.get('FRAUD_TOPIC')


async def run_consumer():
    while True:
        consumer = KafkaConsumer(
            TRANSACTIONS_TOPIC,
            auto_offset_reset='latest',
            bootstrap_servers=KAFKA_BROKER_URL,
            value_deserializer=lambda value: json.loads(value),
        )
        for message in consumer:
            transaction: dict = message.value
            print(LEGIT_TOPIC, transaction)  # DEBUG

