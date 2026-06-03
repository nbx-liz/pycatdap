.PHONY: install test test-slow test-all r-reference lint format format-check typecheck ci build clean

PACKAGE = src/pycatdap

install:
	uv sync --frozen --dev

# Mirrors the develop-PR CI gate. Slow tests are excluded: the D4 dataset
# fetchers are network-bound (OpenML) and hang for hours when scikit-learn is
# installed locally — run them explicitly via ``make test-slow``.
test:
	uv run pytest -m "not slow" --cov=$(PACKAGE) --cov-fail-under=80 -q

test-slow:
	uv run pytest -m slow -v

# Full suite (slow included). Run in a network-available, sklearn-free env to
# match the release-PR CI path; otherwise the network-bound fetchers may hang.
test-all:
	uv run pytest --cov=$(PACKAGE) --cov-fail-under=80 -q

r-reference:
	@command -v Rscript >/dev/null 2>&1 || { \
		echo "Error: Rscript not found. Install R: 'sudo apt install r-base' (Linux) or 'brew install r' (macOS)." >&2; \
		exit 1; \
	}
	@Rscript -e 'if (!"catdap" %in% installed.packages()[,1]) stop("R catdap package not installed. Run: install.packages(\"catdap\")")'
	Rscript docs/r_reference/generate_reference.R

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
