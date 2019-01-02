import os
from producer import APP

KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')


if __name__ == '__main__':
    APP.run(host="0.0.0.0", port=5050)



