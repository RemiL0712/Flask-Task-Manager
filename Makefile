.PHONY: init run docker-up docker-build migrate upgrade clean fmt lint

init:
	python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt && cp -n .env.example .env || true
	flask db init || true
	flask db migrate -m "init" || true
	flask db upgrade

run:
	python wsgi.py

migrate:
	flask db migrate -m "$(m)"

upgrade:
	flask db upgrade

docker-up:
	docker compose up --build

docker-build:
	docker compose build

fmt:
	python -m pip install ruff black || true
	ruff check --fix . || true
	black . || true

lint:
	ruff check . || true

clean:
	rm -rf .venv __pycache__ .pytest_cache instance *.db
