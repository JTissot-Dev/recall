# Après la commande, ajouter name="Nom_migration"
generate-migration:
	docker exec -it recall-backend-dev sh -c "alembic revision --autogenerate -m \"$(name)\""

migration-up-dev:
	docker exec -it recall-backend-dev sh -c "alembic upgrade head"

migration-down-dev:
	docker exec -it recall-backend-dev sh -c "alembic downgrade -1"

format:
	ruff format --line-length 80 .

lint:
	ruff check .

test:
	pytest
