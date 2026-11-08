install:
	uv sync

run:
	uv run project

lint:
	uv run ruff check .