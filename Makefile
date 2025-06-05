.PHONY: install test lint run migrate

install:
	poetry install
	poetry run pre-commit install

test:
	poetry run pytest tests/ -v --cov=src

lint:
	poetry run ruff check src/
	poetry run ruff format src/ --check

run:
	docker-compose up --build

migrate:
	docker-compose exec web python manage.py migrate

createsuperuser:
	docker-compose exec web python manage.py createsuperuser
