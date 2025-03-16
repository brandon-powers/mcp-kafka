FROM python:3.13-slim-bookworm
# TODO
RUN uv sync

CMD ["python3", "mcp-kafka/mcp_kafka.py"]