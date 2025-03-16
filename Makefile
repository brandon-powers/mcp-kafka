test:
	pytest tests/*

lint:
	uv run isort mcp_kafka/* tests/* ; uv run ruff check mcp_kafka/* tests/* --fix
