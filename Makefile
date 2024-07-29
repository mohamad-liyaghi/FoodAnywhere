.PHONY: help build run deploy stop test migrations migrate admin

help:
	@echo "Available targets:"
	@echo "  help    - Show this help message."
	@echo "  build   - Build the docker image."
	@echo "  run     - Run the docker container."
	@echo "  deploy - Run the docker container in production mode."
	@echo "  stop    - Stop the docker container."
	@echo "  test    - Run the tests."
	@echo "  migrations - Create migrations."
	@echo "  migrate - Run migrations."
	@echo "  admin   - Create admin user."

build:
	docker compose build

run:
ifeq ($(DETACHED),true)
	docker compose up -d
else
	docker compose up
endif

deploy:
	docker compose -f docker-compose.prod.yaml up -d

stop:
	docker compose down

test:
	docker exec food-anywhere-backend pytest

migrations:
	docker exec food-anywhere-backend python manage.py makemigrations

migrate:
	docker exec food-anywhere-backend python manage.py migrate

admin:
	docker exec -it food-anywhere-backend python manage.py createsuperuser
