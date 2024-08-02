.PHONY: help build run deploy stop test migrations migrate admin local_confmap prod_confmap k8s

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
	@echo "  local_confmap - Make Kubernetes config maps for local stage"
	@echo "  prod_confmap - Make Kubernetes config maps for production stage"
	@echo "  k8s - Deploy to Kubernetes"

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

local_confmap:
	kubectl create configmap food-anywhere-env --from-env-file=envs/.env.local \
	&& kubectl create configmap food-anywhere-env-file --from-file=.env=envs/.env.local
	&& kubectl create configmap prometheus-config --from-file=prometheus.yml=./prometheus/config.yaml
	&& kubectl create configmap promtail-config --from-file=promtail.yaml=./promtail/config.yaml

prod_confmap:
	kubectl create configmap food-anywhere-env --from-env-file=.envs/.env.prod \
	&& kubectl create configmap food-anywhere-env-file --from-file=.env=envs/.env.prod
	&& kubectl create configmap prometheus-config --from-file=prometheus.yml=./prometheus/config.yaml
	&& kubectl create configmap promtail-config --from-file=promtail.yaml=./promtail/config.yaml


k8s:
	kubectl apply -f kubernetes/
