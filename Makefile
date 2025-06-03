.PHONY: start stop build shell migrate createsuperuser

start:
	docker compose up

stop:
	docker compose down

build:
	docker compose build

shell:
	docker compose exec web bash

migrate:
	docker compose exec web python _360groundproject/manage.py migrate

createsuperuser:
	docker compose exec web python _360groundproject/manage.py createsuperuser
