.PHONY: install test lint format format-check typecheck ci build clean

PACKAGE = src/pycatdap

install:
	uv sync --frozen --dev

test:
	uv run pytest --cov=$(PACKAGE) --cov-fail-under=80 -q

lint:
	uv run ruff check .

format:
	uv run ruff format .

format-check:
	uv run ruff format --check .

typecheck:
	uv run mypy $(PACKAGE)/

ci: lint format-check typecheck test

build:
	uv build
	uv run twine check dist/*

clean:
	rm -rf dist/ build/ *.egg-info .pytest_cache .mypy_cache .ruff_cache coverage.json .coverage
