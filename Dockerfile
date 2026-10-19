# syntax=docker/dockerfile:1

FROM python:3.15.0-slim

# Keep the uv environment outside the source bind mount used by Compose.
ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_PYTHON_DOWNLOADS=never \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
  wget unzip curl vim \
  chromium chromium-driver

COPY pyproject.toml uv.lock .python-version ./
RUN --mount=from=ghcr.io/astral-sh/uv:0.13.2,source=/uv,target=/bin/uv \
    --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-install-project

RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid 1001 appuser

USER 1001
# Set environment variables

ENV DISPLAY=:99

# Copy app files
COPY --chown=1001:1001 ./src/ /app
# Python resolves to the environment installed by uv.
CMD ["python", "app.py"]
