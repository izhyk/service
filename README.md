# Kafka Service

## Install

This kafka service is fully containerised. You will need [Docker](https://docs.docker.com/install/) and [Docker Compose](https://docs.docker.com/compose/) to run it.

You simply need to create a Docker network called `kafka-network` to enable communication between the Kafka cluster and the apps:

```bash
$ docker network create kafka-network
```

All set!

## Quickstart

- Spin up the local single-node Kafka cluster (will run in the background):

```bash
$ docker-compose -f docker-compose.kafka.yml up -d
```

- Start the kafka Producer(http://0.0.0.0:5050/) and Consumer apps:

```bash
$ docker-compose up -d
```

- or just run ```make```

## Usage

- From this url `http://0.0.0.0:5050/producer` you can send message from Producer app to Consumer


## Teardown

To stop the transaction generator and fraud detector:

```bash
$ docker-compose down
```

To stop the Kafka cluster (use `down`  instead to also remove contents of the topics):

```bash
$ docker-compose -f docker-compose.kafka.yml stop
```

To remove the Docker network:

```bash
$ docker network rm kafka-network
```
