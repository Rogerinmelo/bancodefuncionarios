.PHONY: up down logs install env migrate run test smoke

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f --tail=100

install:
	python -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt -r requirements-dev.txt

env:
	cp -n .env.example .env || true

migrate:
	. .venv/bin/activate && alembic upgrade head

run:
	. .venv/bin/activate && uvicorn app.main:app --reload

test:
	. .venv/bin/activate && pytest -q

smoke:
	bash scripts/smoke_api.sh
