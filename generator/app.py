"""Produce fake transactions into a Kafka topic."""

import os
import json
from time import sleep

from kafka import KafkaProducer

from producer import APP
from transactions import create_random_transaction

TRANSACTIONS_TOPIC = os.environ.get('TRANSACTIONS_TOPIC')
KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')


if __name__ == '__main__':
    # producer = KafkaProducer(
    #     bootstrap_servers=KAFKA_BROKER_URL,
    #     # Encode all values as JSON
    #     value_serializer=lambda value: json.dumps(value).encode(),
    # )
    # while True:
    #     transaction: dict = create_random_transaction()
    #     producer.send(TRANSACTIONS_TOPIC, value=transaction)
    #     print(transaction)  # DEBUG
    #     sleep(1/50)
    APP.run(host="0.0.0.0", port=5050)
    # for i in range(5):
    #     transaction: dict = create_random_transaction()
    #     producer.send(TRANSACTIONS_TOPIC, value=transaction)
    #     print(transaction)  # DEBUG


