import os
import json
from kafka import KafkaConsumer
from sanic import Sanic

KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')

app = Sanic()


if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=5070)
    while True:
        consumer = KafkaConsumer(
            'my-topic',
            auto_offset_reset='earliest',
            bootstrap_servers=KAFKA_BROKER_URL,
            value_deserializer=lambda value: json.loads(value),
        )
        for message in consumer:
            print('my-topic', message.value)  # DEBUG
