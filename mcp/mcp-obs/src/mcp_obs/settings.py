"""Settings for the observability MCP server."""

import os


def resolve_victorialogs_url() -> str:
    return os.environ.get("NANOBOT_VICTORIALOGS_URL", "http://localhost:9428")


def resolve_victoriatraces_url() -> str:
    return os.environ.get("NANOBOT_VICTORIATRACES_URL", "http://localhost:10428")
