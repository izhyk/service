all:run

run:
	docker-compose -f docker-compose.kafka.yml up -d
	sleep 3
	docker-compose up --build

migrate:
	@docker exec -it generator python producer/db.py

