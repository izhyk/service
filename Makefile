all:run

run:
	docker-compose up --build

migrate:
	@docker exec -it generator python producer/db.py

