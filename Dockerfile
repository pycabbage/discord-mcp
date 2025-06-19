FROM python:3.13-alpine AS base
COPY --from=ghcr.io/astral-sh/uv:0.7.13 /uv /uvx /bin/
WORKDIR /app

FROM base AS builder
COPY pyproject.toml uv.lock .python-version README.md src /app/
RUN \
  uv sync --locked 

FROM base AS final
COPY --from=builder /app /app
ENTRYPOINT ["/bin/uv", "run", "discord-mcp"]
