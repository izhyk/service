import os
import json
from kafka import KafkaConsumer

KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
TRANSACTIONS_TOPIC = os.environ.get('TRANSACTIONS_TOPIC')


# async def run_consumer():
#     while True:
#         consumer = KafkaConsumer(
#             TRANSACTIONS_TOPIC,
#             auto_offset_reset='earliest',
#             bootstrap_servers=KAFKA_BROKER_URL,
#             value_deserializer=lambda value: json.loads(value),
#         )
#         for message in consumer:
#             transaction: dict = message.value
#             print(TRANSACTIONS_TOPIC, transaction)

