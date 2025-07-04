build-dev:
	docker compose -f docker-compose.dev.yaml up --build --detach

run-dev:
	docker compose -f docker-compose.dev.yaml up --detach
