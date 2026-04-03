---
name: observability
description: Use observability MCP tools to search logs and traces for debugging
always: true
---

# Observability Skill

You have access to observability tools that let you query structured logs and distributed traces from the system. Use these to diagnose errors and understand request flows.

## Available Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `mcp_obs_logs_search` | Search structured logs using LogsQL | `query` (LogsQL), `limit` (default 50) |
| `mcp_obs_logs_error_count` | Count error-level log entries | `service` (optional), `minutes` (default 60) |
| `mcp_obs_traces_list` | List recent traces | `service` (optional), `limit` (default 10) |
| `mcp_obs_traces_get` | Fetch a specific trace | `trace_id` (required) |

## Strategy

### When the user asks about errors or failures:

1. First call `mcp_obs_logs_error_count` with `service="Learning Management Service"` and `minutes=10` to check for recent errors
2. If errors exist, call `mcp_obs_logs_search` with a query like:
   ```
   _time:10m service.name:"Learning Management Service" severity:ERROR
   ```
3. From the log results, look for a `trace_id` field in any error record
4. If you find a `trace_id`, call `mcp_obs_traces_get` with that ID to see the full span hierarchy
5. Summarize what you found — don't dump raw JSON

### When the user asks "what went wrong?" or "any errors?":

1. Start with `mcp_obs_logs_error_count` scoped to the LMS backend and a narrow time window (10 minutes)
2. If errors found, search for details with `mcp_obs_logs_search`
3. If a trace_id is available, fetch the trace with `mcp_obs_traces_get`
4. Provide a concise summary: what failed, where, and why

### When the user asks about a specific trace:

1. Call `mcp_obs_traces_get` with the trace ID
2. Explain the span hierarchy — which services were involved and how long each step took
3. Point out any errors or unusually slow spans

### Formatting results:

- Keep responses concise — lead with the answer, then provide details
- Summarize log entries rather than dumping raw JSON
- When showing traces, list spans in order with service name, operation, and duration
- If no errors found, say so clearly: "No errors found in the last 10 minutes for the LMS backend."

### Key field names in logs:

- `service.name` — the service that emitted the log (e.g., "Learning Management Service")
- `severity` — log level (INFO, WARNING, ERROR)
- `event` — what happened (e.g., "request_started", "db_query", "auth_failure")
- `trace_id` — links to distributed traces
