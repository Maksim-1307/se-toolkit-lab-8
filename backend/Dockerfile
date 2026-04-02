# ---
# Stage 1: Build
# ---
ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB}astral/uv:python3.14-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_NO_DEV=1 \
    UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# 1. Copy config files
COPY pyproject.toml uv.lock ./

# 2. Pre-install dependencies to leverage Docker cache
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-install-workspace

# 3. Copy the rest of the source code
COPY . ./

# 4. Install the current directory as a package
# We removed --no-editable because it's the default for 'pip install'
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install .

# ---
# Stage 2: Final Image
# ---
ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB}python:3.14.2-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    LANG=C.UTF-8

RUN groupadd --system --gid 999 nonroot \
    && useradd --system --gid 999 --uid 999 --create-home nonroot

COPY --from=builder --chown=nonroot:nonroot /app /app

# The venv created by uv defaults to /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

USER nonroot
WORKDIR /app

CMD ["opentelemetry-instrument", "uvicorn", "lms_backend.main:app"]
