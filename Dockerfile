FROM python:3.13-alpine AS base
WORKDIR /app

FROM base AS builder
RUN \
  --mount=from=ghcr.io/astral-sh/uv,source=/uv,target=/bin/uv \
  --mount=type=cache,target=/root/.cache/uv \
  --mount=source=pyproject.toml,target=/app/pyproject.toml \
  --mount=source=uv.lock,target=/app/uv.lock \
  --mount=source=.python-version,target=/app/.python-version \
  --mount=source=README.md,target=/app/README.md \
  --mount=source=src,target=/app/src \
  UV_LINK_MODE=copy uv sync --locked --compile-bytecode --no-editable

FROM base AS final
COPY --from=builder /app /app
WORKDIR /app
ENTRYPOINT ["/app/.venv/bin/discord-mcp"]
