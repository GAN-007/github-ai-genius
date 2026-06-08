.PHONY: install test lint api container

install:
	python -m pip install --upgrade pip
	pip install -e '.[dev]'

test:
	pytest

lint:
	ruff check github_ai_genius tests

api:
	uvicorn github_ai_genius.api_v2:app --host 0.0.0.0 --port 8080 --reload

container:
	docker compose -f compose.yml up --build
