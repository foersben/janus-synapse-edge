default:
    @just --list

# Initialize the workspace
setup:
    uv sync
    uv run pre-commit install

install:
    @just setup

lint:
    uv run ruff check --fix scripts/
    uv run ruff format scripts/
    uv run mypy scripts/

# Format all utility scripts
format:
    uv run ruff format scripts/
    uv run ruff check --fix scripts/

# Mathematically validate all hardware constraints and run markdown linters
validate:
    uv run python scripts/validate_okf.py ./docs
    uv run pre-commit run markdownlint --all-files

# Build the documentation site (Output: ./site)
docs:
    uv run zensical build

# Run the Zensical local dev server
serve:
    uv run zensical serve --address localhost:9000
