from consumer import APP

if __name__ == '__main__':
    APP.run(host="0.0.0.0", port=5070)
    # loop = asyncio.get_event_loop()
    #
    #
    # async def consume():
    #     consumer = AIOKafkaConsumer(
    #         'my-topic',
    #         loop=loop, bootstrap_servers=KAFKA_BROKER_URL,
    #         value_deserializer=lambda value: json.loads(value),
    #         group_id="my-group"
    #         )
    #     # Get cluster layout and join group `my-group`
    #     await consumer.start()
    #     try:
    #         # Consume messages
    #         async for msg in consumer:
    #             assert False, print(msg.value)
    #             print("consumed: ", msg.topic, msg.partition, msg.offset,
    #                   msg.key, msg.value, msg.timestamp)
    #     finally:
    #         # Will leave consumer group; perform autocommit if enabled.
    #         await consumer.stop()
    #
    #
    # loop.run_until_complete(consume())

