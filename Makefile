.PHONY: setup test lint typecheck infra-up infra-down validate-contracts

setup:
	python -m venv .venv
	. .venv/bin/activate && pip install -U pip && pip install -e .[dev]

test:
	pytest

lint:
	ruff check .

typecheck:
	mypy apps packages

infra-up:
	docker compose -f infra/docker-compose.yml up -d

infra-down:
	docker compose -f infra/docker-compose.yml down

validate-contracts:
	python scripts/validate_contracts.py
