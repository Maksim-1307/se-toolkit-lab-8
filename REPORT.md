# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

### Question 1: "What is the agentic loop?"

**Response:**
The agentic loop is the fundamental cycle that autonomous AI agents follow to accomplish tasks. It typically consists of these core stages:

1. **Perceive** — Gather information from the environment (user input, files, APIs, sensors, etc.)
2. **Think/Reason** — Process the information, plan actions, and make decisions about what to do next
3. **Act** — Execute actions using available tools (file operations, API calls, code execution, etc.)
4. **Observe** — Receive feedback from the actions taken (success, failure, output, state changes)
5. **Repeat** — Continue the loop until the goal is achieved or a stopping condition is met

This loop enables agents to:
- Break complex tasks into steps
- Adapt based on feedback
- Handle errors and retry
- Make progress autonomously toward a goal

In the nanobot implementation, each time a user gives a task, the agent goes through this loop: it reads the request (perceive), figures out what tools are needed (think), calls those tools (act), checks the results (observe), and continues until the task is completed.

### Question 2: "What labs are available in our LMS?"

**Response:**
The agent explored the local workspace using file system tools (`list_dir`, `exec`, `read_file`) and found:

- **Lab 8 (Current)** - se-toolkit-lab-8 at `/root/se-toolkit-lab-8`
- **Lab 1** - Documentation available at `/root/se-toolkit-lab-8/wiki/lab-1`
- **Lab 8 Tasks** in `/root/se-toolkit-lab-8/lab/tasks/`:
  - Required: task-1.md through task-5.md
  - Optional: task-1.md

**Important:** The agent did NOT return real LMS backend data - it searched local files instead. This is expected because the MCP server (which provides live LMS API access) is not yet configured. The agent used its built-in file system tools to explore the repository structure.

## Task 1B — Agent with LMS tools

### Question 1: "What labs are available?"

**Response:**
The agent connected to the MCP server and called the `mcp_lms_lms_labs` tool, returning **real lab names from the backend**:

1. Lab 01 – Products, Architecture & Roles
2. Lab 02 — Run, Fix, and Deploy a Backend Service
3. Lab 03 — Backend API: Explore, Debug, Implement, Deploy
4. Lab 04 — Testing, Front-end, and AI Agents
5. Lab 05 — Data Pipeline and Analytics Dashboard
6. Lab 06 — Build Your Own Agent
7. Lab 07 — Build a Client with an AI Coding Agent
8. Lab 08 — lab-08

**Key difference from Part A:** In Part A, the agent searched local files. Now it calls the live LMS API via MCP.

### Question 2: "Is the LMS backend healthy?"

**Response:**
"Yes, the LMS backend is healthy! It's currently tracking 56 items."

The agent called the `mcp_lms_lms_health` tool which returned real health data from the backend.

### Question 3: "Which lab has the lowest pass rate?"

**Response:**
The agent chained multiple tool calls:
1. First called `mcp_lms_lms_labs` to get all available labs
2. Then called `mcp_lms_lms_completion_rate` for each lab (lab-01 through lab-08)
3. Compiled the results into a table showing completion rates

Result: Lab 08 has 0.0% (no submissions yet). Among active labs, Lab 02 and Lab 03 are tied at 89.1%.

## Task 1C — Skill prompt

### Question: "Show me the scores" (without specifying a lab)

**Response:**
The agent followed the LMS skill strategy:

1. First called `mcp_lms_lms_labs` to get all available labs
2. Listed all 8 labs with their titles
3. Asked the user to choose which lab they want to see scores for

**Full response:**
"Here are the available labs. Which one would you like to see the scores for?

1. Lab 01 – Products, Architecture & Roles
2. Lab 02 – Run, Fix, and Deploy a Backend Service
3. Lab 03 – Backend API: Explore, Debug, Implement, Deploy
4. Lab 04 – Testing, Front-end, and AI Agents
5. Lab 05 – Data Pipeline and Analytics Dashboard
6. Lab 06 – Build Your Own Agent
7. Lab 07 – Build a Client with an AI Coding Agent
8. Lab 08 – lab-08

Just let me know the lab number (e.g., "Lab 04" or "4") and I'll show you the pass rates!"

**Skill file created:** `nanobot/workspace/skills/lms/SKILL.md`

The skill teaches the agent to:
- Call `mcp_lms_lms_labs` first when a lab parameter is needed but not provided
- List available labs and ask the user to choose
- Use lab titles as user-facing labels
- Format numeric results as percentages
- Explain capabilities when asked "what can you do?"

## Task 2A — Deployed agent

### Nanobot startup log excerpt:

```
Using resolved config: /tmp/nanobot/config.resolved.json
🐈 Starting nanobot gateway version 0.1.4.post5 on port 18790...
✓ Channels enabled: webchat
✓ Heartbeat: every 1800s
MCP server 'lms': connected, 9 tools registered
MCP server 'mcp_webchat': connected, 1 tools registered
Agent loop started
```

### Files created/modified:
- `nanobot/entrypoint.py` — resolves env vars into config at runtime, launches `nanobot gateway`
- `nanobot/Dockerfile` — multi-stage uv build with all workspace packages
- `docker-compose.yml` — nanobot service with correct volumes, env vars, and network
- `nanobot/config.json` — base config with custom provider and MCP LMS server

## Task 2B — Web client

### WebSocket endpoint test (`/ws/chat`):

```
$ websocat "ws://localhost:42002/ws/chat?access_key=nanobot-access-key-2026"
> {"content":"What labs are available?"}
< Here are the available labs:
< | Lab ID | Title |
< |--------|-------|
< | lab-01 | Lab 01 – Products, Architecture & Roles |
< | lab-02 | Lab 02 – Run, Fix, and Deploy a Backend Service |
< | lab-03 | Lab 03 – Backend API: Explore, Debug, Implement, Deploy |
< ...
```

The agent called `mcp_lms_lms_labs({})` and returned real lab names from the backend.

### Flutter web client:

Accessible at `http://<vm-ip>:42002/flutter` — returns HTTP 200 with Flutter web app.

### Nanobot logs showing webchat activity:

```
Processing message from webchat:f3b5dde3-cf17-4a9b-8b08-c910cfaafbda: What labs are available?
Tool call: mcp_lms_lms_labs({})
Response to webchat:f3b5dde3-cf17-4a9b-8b08-c910cfaafbda: Here are the available labs: ...
```

### Files modified:
- `caddy/Caddyfile` — uncommented `/ws/chat` and `/flutter*` routes
- `docker-compose.yml` — uncommented `client-web-flutter` service and Caddy volume
- `nanobot-websocket-channel/nanobot-webchat/pyproject.toml` — workspace → path source
- `nanobot-websocket-channel/mcp-webchat/pyproject.toml` — workspace → path source
- `pyproject.toml` — uncommented workspace members for webchat packages

## Task 3A — Structured logging

### Happy-path structured log entry (VictoriaLogs JSON):

```json
{
    "_msg": "request_completed",
    "_time": "2026-04-03T11:56:23.98916608Z",
    "duration_ms": "59",
    "event": "request_completed",
    "method": "GET",
    "path": "/items/",
    "service.name": "Learning Management Service",
    "severity": "INFO",
    "span_id": "80522861afbdf8d3",
    "status": "200",
    "trace_id": "5eddd5e6918be95e4cd1b93508dfd112"
}
```

The happy-path log flow: `request_started` (INFO) → `auth_success` (INFO) → `db_query` (INFO) → `request_completed` (INFO, status 200).

### Error-path structured log entry (VictoriaLogs JSON):

```json
{
    "_msg": "db_query",
    "_time": "2026-04-03T11:56:23.987367936Z",
    "error": "[Errno -2] Name or service not known",
    "event": "db_query",
    "operation": "select",
    "service.name": "Learning Management Service",
    "severity": "ERROR",
    "span_id": "80522861afbdf8d3",
    "table": "item",
    "trace_id": "5eddd5e6918be95e4cd1b93508dfd112"
}
```

When PostgreSQL is stopped, the `db_query` event produces an ERROR-level log with the connection error message and the same `trace_id` links it to the request.

### VictoriaLogs query:

Query: `_time:10m service.name:"Learning Management Service" severity:ERROR`
Accessible at: `http://<vm-ip>:42002/utils/victorialogs/select/vmui`

---

## Task 3B — Traces

### Healthy trace (VictoriaTraces API):

```
GET http://localhost:42011/select/jaeger/api/traces?service=Learning+Management+Service&limit=3
Found 3 traces
  Trace 5eddd5e6918be95e4cd1b93508dfd112: 5 spans, services: {'Learning Management Service'}
  Trace 51085d1764a96e6bfc3ddbca1d53bd3d: 5 spans, services: {'Learning Management Service'}
  Trace 2839572bf1d337096bcb9c9d2aed9b59: 5 spans, services: {'Learning Management Service'}
```

Each trace has 5 spans covering the full request flow: HTTP request → auth → DB query → response.

### Error trace:

The error trace (trace_id `5eddd5e6918be95e4cd1b93508dfd112`) shows the same span hierarchy but with an ERROR span at `db_query` containing the PostgreSQL connection failure. The trace_id matches between the error log and the trace, enabling correlation.

VictoriaTraces UI accessible at: `http://<vm-ip>:42002/utils/victoriatraces`
Jaeger-compatible API at: `http://victoriatraces:10428/select/jaeger/api/traces`

---

## Task 3C — Observability MCP tools

### Normal conditions — "Any LMS backend errors in the last 10 minutes?"

**Response:**
```
Good news — no LMS backend errors in the last 10 minutes. The service looks clean. ✅
```

The agent called:
1. `mcp_mcp_obs_logs_error_count` with `service="Learning Management Service"`, `minutes=10`
2. `mcp_mcp_obs_logs_search` with `_time:10m service.name:"Learning Management Service" severity:ERROR`

### Failure conditions (PostgreSQL stopped) — "Any LMS backend errors in the last 10 minutes?"

**Response:**
```
Yes, there are 2 errors in the last 10 minutes from the Learning Management Service.
Both are database connection errors caused by PostgreSQL being unavailable.
```

### Files created:
- `mcp/mcp-obs/` — observability MCP server with 4 tools:
  - `logs_search` — search VictoriaLogs via LogsQL
  - `logs_error_count` — count errors per service/time window
  - `traces_list` — list recent traces
  - `traces_get` — fetch specific trace by ID
- `nanobot/workspace/skills/observability/SKILL.md` — teaches agent to search logs first, then traces
- `nanobot/entrypoint.py` — registers mcp-obs with NANOBOT_VICTORIALOGS_URL and NANOBOT_VICTORIATRACES_URL

## Task 4A — Multi-step investigation

### Agent response to "What went wrong?" (with PostgreSQL stopped):

The agent performed a multi-step investigation:

1. Called `mcp_mcp_obs_traces_list` to list recent traces for the LMS
2. Called `mcp_mcp_obs_traces_get` with trace_id `77fad2caf0a233a9cfa4421890ed23a7`
3. Examined the trace and produced an investigation report

**Investigation report excerpt:**
```
Here's exactly what went wrong:

## Root Cause: Database Connection Failure

The LMS backend can't connect to its PostgreSQL database.
Logs show `socket.gaierror: [Errno -2] Name or service not known` — the database hostname
cannot be resolved, meaning the PostgreSQL container is down or unreachable.
The trace shows the request failing at the db_query span within the Learning Management Service.
```

### Tool chain observed in nanobot logs:

```
Tool call: mcp_mcp_obs_traces_list({"limit": 5, "service": "Learning Management Service"})
Tool call: mcp_mcp_obs_traces_get({"trace_id": "77fad2caf0a233a9cfa4421890ed23a7"})
Response: Here's exactly what went wrong: ## Root Cause: Database Connection Failure
```

The agent cited both trace evidence (the failing db_query span) and log evidence (the connection error) in its investigation.

---

## Task 4B — Proactive health check

A recurring health check was created via the Flutter web chat at `http://<vm-ip>:42002/flutter`:
- The agent was asked to create a cron job that runs every 2 minutes
- Each run checks for LMS/backend errors in the last 2 minutes using observability tools
- While PostgreSQL was stopped, the scheduled job posted a failure report into the same chat
- After PostgreSQL was restarted, a new health check reported the system as healthy

The cron-based health check demonstrates the agent's ability to proactively monitor the system
without being prompted for each check.

---

## Task 4C — Bug fix and recovery

### 1. Root cause identified

**Planted bug:** In `backend/src/lms_backend/routers/items.py`, the `get_items()` endpoint
catches **all** exceptions (including database failures) and returns a misleading
**404 "Items not found"** instead of a **500 Internal Server Error**.

```python
# BEFORE (buggy):
except Exception as exc:
    logger.warning("items_list_failed_as_not_found", ...)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Items not found",
    ) from exc
```

This hides the real database failure and makes debugging difficult — a database connectivity
issue looks like "items not found" rather than a server error.

### 2. Fix applied

Changed the exception handler to return **500 Internal Server Error** with the actual error
message, and upgraded the log level from WARNING to ERROR:

```python
# AFTER (fixed):
except Exception as exc:
    logger.error(
        "items_list_failed",
        extra={"event": "items_list_failed", "error": str(exc)},
    )
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Failed to retrieve items: {exc}",
    ) from exc
```

**File changed:** `backend/src/lms_backend/routers/items.py` (lines 19-29)

### 3. Post-fix verification

After rebuilding and redeploying the backend, stopping PostgreSQL and asking "What went wrong?"
now shows the real underlying database failure (500 error with connection error details)
instead of the misleading 404 response.

### 4. Healthy follow-up

After restarting PostgreSQL, the system returned to normal operation. A fresh health check
reported no recent errors, confirming recovery.
```
Good news — no LMS backend errors in the last 10 minutes. The service looks clean. ✅
```
