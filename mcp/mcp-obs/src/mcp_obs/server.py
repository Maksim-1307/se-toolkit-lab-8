"""Stdio MCP server for observability (VictoriaLogs + VictoriaTraces)."""

from __future__ import annotations

import asyncio
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from pydantic import BaseModel, Field

from mcp_obs.observability import VictoriaLogsClient, VictoriaTracesClient
from mcp_obs.settings import resolve_victorialogs_url, resolve_victoriatraces_url


# --- Tool schemas ---

class LogsSearchArgs(BaseModel):
    query: str = Field(description="LogsQL query, e.g. '_time:10m service.name:\"Learning Management Service\" severity:ERROR'")
    limit: int = Field(default=50, description="Max log entries to return")


class LogsErrorCountArgs(BaseModel):
    service: str | None = Field(default=None, description="Service name to filter (e.g. 'Learning Management Service')")
    minutes: int = Field(default=60, description="Time window in minutes")


class TracesListArgs(BaseModel):
    service: str | None = Field(default=None, description="Service name to filter")
    limit: int = Field(default=10, description="Max traces to return")


class TracesGetArgs(BaseModel):
    trace_id: str = Field(description="Trace ID to fetch")


# --- Server creation ---

def create_server(
    logs_client: VictoriaLogsClient,
    traces_client: VictoriaTracesClient,
) -> Server:
    server = Server("observability")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name="logs_search",
                description="Search structured logs using LogsQL. Use _time: for time windows, severity:ERROR for errors, service.name: for service.",
                inputSchema=LogsSearchArgs.model_json_schema(),
            ),
            Tool(
                name="logs_error_count",
                description="Count error-level log entries over a time window. Optionally filter by service name.",
                inputSchema=LogsErrorCountArgs.model_json_schema(),
            ),
            Tool(
                name="traces_list",
                description="List recent traces. Optionally filter by service name.",
                inputSchema=TracesListArgs.model_json_schema(),
            ),
            Tool(
                name="traces_get",
                description="Fetch a specific trace by its trace ID to see the full span hierarchy.",
                inputSchema=TracesGetArgs.model_json_schema(),
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any] | None) -> list[TextContent]:
        args = arguments or {}
        try:
            match name:
                case "logs_search":
                    parsed = LogsSearchArgs(**args)
                    result = await logs_client.search_logs(parsed.query, parsed.limit)
                case "logs_error_count":
                    parsed = LogsErrorCountArgs(**args)
                    result = await logs_client.count_errors(parsed.service, parsed.minutes)
                case "traces_list":
                    parsed = TracesListArgs(**args)
                    result = await traces_client.list_traces(parsed.service, parsed.limit)
                case "traces_get":
                    parsed = TracesGetArgs(**args)
                    result = await traces_client.get_trace(parsed.trace_id)
                case _:
                    result = f"Unknown tool: {name}"
        except Exception as exc:
            result = f"Error: {type(exc).__name__}: {exc}"
        return [TextContent(type="text", text=result)]

    return server


async def main() -> None:
    logs_url = resolve_victorialogs_url()
    traces_url = resolve_victoriatraces_url()

    logs_client = VictoriaLogsClient(logs_url)
    traces_client = VictoriaTracesClient(traces_url)

    server = create_server(logs_client, traces_client)

    async with stdio_server() as (read_stream, write_stream):
        init_options = server.create_initialization_options()
        await server.run(read_stream, write_stream, init_options)


if __name__ == "__main__":
    asyncio.run(main())
