# ---------- Stage 1: build dependencies with uv ----------
FROM python:3.13-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:0.8.15 /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

WORKDIR /app

# Install dependencies first (cached unless pyproject/uv.lock change)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project --no-cache


# ---------- Stage 2: slim runtime image ----------
FROM python:3.13-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH" \
    APP_ENV=production \
    PORT=8080

RUN groupadd --system app && useradd --system --gid app --home /app app

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY app ./app
COPY static ./static
COPY templates ./templates

# Empty writable dirs for the SQLite audit DB (data/audit.db) and uploads,
# using the default paths from config.py (no local data is copied in)
RUN mkdir -p /app/data /app/uploads && chown -R app:app /app/data /app/uploads

USER app

EXPOSE 8080

# App Platform's HTTP port must be set to 8080; health check is
# configured in the App Platform settings (path: /api/health)
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8080 --proxy-headers --forwarded-allow-ips='*'"]
