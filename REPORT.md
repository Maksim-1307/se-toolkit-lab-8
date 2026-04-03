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

<!-- Paste happy-path and error-path log excerpts, VictoriaLogs query screenshot -->

## Task 3B — Traces

<!-- Screenshots: healthy trace span hierarchy, error trace -->

## Task 3C — Observability MCP tools

<!-- Paste agent responses to "any errors in the last hour?" under normal and failure conditions -->

## Task 4A — Multi-step investigation

<!-- Paste the agent's response to "What went wrong?" showing chained log + trace investigation -->

## Task 4B — Proactive health check

<!-- Screenshot or transcript of the proactive health report that appears in the Flutter chat -->

## Task 4C — Bug fix and recovery

<!-- 1. Root cause identified
     2. Code fix (diff or description)
     3. Post-fix response to "What went wrong?" showing the real underlying failure
     4. Healthy follow-up report or transcript after recovery -->
