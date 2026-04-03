# ---
# Stage 1: Build
# ---
ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB:-}astral/uv:python3.14-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_NO_DEV=1 \
    UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Create virtual environment
RUN uv venv

# Install nanobot-ai from URL first
ENV VIRTUAL_ENV=/app/.venv PATH="/app/.venv/bin:$PATH"
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install "nanobot-ai @ https://github.com/HKUDS/nanobot/archive/e7d371ec1e6531b28898ec2c869ef338e8dd46ec.zip"

# Copy and install workspace packages in dependency order
# 1. nanobot-channel-protocol (no internal dependencies)
COPY nanobot-websocket-channel/nanobot-channel-protocol/ ./nanobot-channel-protocol/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install ./nanobot-channel-protocol

# 2. nanobot-webchat (depends on protocol, already installed)
COPY nanobot-websocket-channel/nanobot-webchat/ ./nanobot-webchat/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install ./nanobot-webchat

# 3. mcp-webchat (depends on protocol, already installed)
COPY nanobot-websocket-channel/mcp-webchat/ ./mcp-webchat/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install ./mcp-webchat

# 4. mcp-lms (no internal dependencies)
COPY mcp/mcp-lms/ ./mcp-lms/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install ./mcp-lms

# Copy nanobot source
COPY nanobot/ ./nanobot/

# ---
# Stage 2: Final Image
# ---
ARG REGISTRY_PREFIX_DOCKER_HUB
ARG APP_UID=1000
ARG APP_GID=1000

FROM ${REGISTRY_PREFIX_DOCKER_HUB:-}python:3.14.2-slim-bookworm

# Re-declare ARGs after FROM to make them available in this stage
ARG APP_UID=1000
ARG APP_GID=1000

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    LANG=C.UTF-8 \
    PATH="/app/.venv/bin:$PATH"

# Create non-root user with configurable UID/GID
RUN groupadd --system --gid ${APP_GID} nonroot \
    && useradd --system --gid ${APP_GID} --uid ${APP_UID} --create-home nonroot

# Copy the built application from builder
COPY --from=builder --chown=nonroot:nonroot /app /app

# Create workspace directory structure with correct ownership
RUN mkdir -p /app/nanobot/workspace/{cron,memory,sessions,skills} \
    && chown -R nonroot:nonroot /app/nanobot/workspace

# Switch to non-root user
USER nonroot
WORKDIR /app

# Health check - verify nanobot gateway port is listening
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD wget --spider -q http://localhost:18790/ 2>/dev/null || ss -tln | grep -q 18790 || exit 1

# Run entrypoint script which resolves config and launches nanobot gateway
CMD ["python", "/app/nanobot/entrypoint.py"]
