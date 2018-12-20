import json
from time import sleep
from producer import APP, KAFKA_BROKER_URL, TRANSACTIONS_TOPIC
from kafka import KafkaProducer
from sanic.response import json as s_json
from transactions import create_random_transaction
from kafka.errors import KafkaError


@APP.route("/")
async def test(request):
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        value_serializer=lambda value: json.dumps(value).encode(),
    )

    # transaction: dict = create_random_transaction()
    producer.send(TRANSACTIONS_TOPIC, value='hello producer')
    Flush()

    print("hello producer")  # DEBUG
    return s_json({'hello producer'})


async def run_producer():
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        value_serializer=lambda value: json.dumps(value).encode(),
    )
    while True:
        transaction: dict = create_random_transaction()
        producer.send(TRANSACTIONS_TOPIC, value=transaction)
        print(transaction)  # DEBUG
        sleep(1/100)
