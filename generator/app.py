import os
import asyncio
from sanic import Sanic

KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')

APP = Sanic()

LOOP = asyncio.get_event_loop()

from routers import *

if __name__ == '__main__':
    APP.run(host="0.0.0.0", port=5050)



