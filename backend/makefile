# Après la commande, ajouter name="Nom_migration"
generate-migration:
	docker exec -it pit-ws-backend-dev sh -c "cd app/infrastructure/database && alembic revision --autogenerate -m \"$(name)\""

migration-up-dev:
	docker exec -it pit-ws-backend-dev sh -c "cd app/infrastructure/database && alembic upgrade head"

migration-down-dev:
	docker exec -it pit-ws-backend-dev sh -c "cd app/infrastructure/database && alembic downgrade -1"

format:
	ruff format --line-length 80 .

lint:
	ruff check .

test:
	pytest
