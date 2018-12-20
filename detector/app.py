"""Example Kafka consumer."""

import os
import json

from kafka import KafkaConsumer
from consumer import run_consumer
from sanic import Sanic


KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
TRANSACTIONS_TOPIC = os.environ.get('TRANSACTIONS_TOPIC')
LEGIT_TOPIC = os.environ.get('LEGIT_TOPIC')
FRAUD_TOPIC = os.environ.get('FRAUD_TOPIC')

app = Sanic()

# run_consumer()

if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=5070)
    while True:
        consumer = KafkaConsumer(
            TRANSACTIONS_TOPIC,
            auto_offset_reset='earliest',
            bootstrap_servers=KAFKA_BROKER_URL,
            value_deserializer=lambda value: json.loads(value),
        )
        for message in consumer:
            transaction: dict = message.value
            print(LEGIT_TOPIC, transaction)  # DEBUG
