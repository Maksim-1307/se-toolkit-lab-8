---
name: lms
description: Use LMS MCP tools for live course data
always: true
---

# LMS Skill

You have access to LMS MCP tools that provide live data from the Learning Management System backend. Use these tools to answer questions about labs, learners, pass rates, and completion statistics.

## Available Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `mcp_lms_lms_health` | Check if LMS backend is healthy | None |
| `mcp_lms_lms_labs` | List all available labs | None |
| `mcp_lms_lms_learners` | List all registered learners | None |
| `mcp_lms_lms_pass_rates` | Get pass rates for a lab | `lab` (required) |
| `mcp_lms_lms_timeline` | Get submission timeline for a lab | `lab` (required) |
| `mcp_lms_lms_groups` | Get group performance for a lab | `lab` (required) |
| `mcp_lms_lms_top_learners` | Get top learners by score for a lab | `lab` (required), `limit` (optional, default 5) |
| `mcp_lms_lms_completion_rate` | Get completion rate for a lab | `lab` (required) |
| `mcp_lms_lms_sync_pipeline` | Trigger the LMS sync pipeline | None |

## Strategy

### When user asks about scores, pass rates, completion, groups, timeline, or top learners without naming a lab:

1. Call `mcp_lms_lms_labs` first to get the list of available labs
2. Use the shared `structured-ui` skill to present a choice to the user
3. For each lab, use the lab's `title` field as the user-facing label
4. Pass the lab's `id` field (e.g., "lab-01") as the `lab` parameter to the tool

Example flow for "Show me the scores":
```
1. Call mcp_lms_lms_labs() → get list of labs
2. Present choice UI with lab titles as labels, lab IDs as values
3. After user selects, call mcp_lms_lms_pass_rates(lab="selected-lab-id")
4. Format the results nicely
```

### When user asks which lab has the lowest/highest metric:

1. Call `mcp_lms_lms_labs` to get all labs
2. Call the relevant metric tool for each lab (e.g., `mcp_lms_lms_completion_rate`)
3. Compare results and report the answer with a summary table

### Formatting numeric results:

- Percentages: Show as "XX.X%" (e.g., "89.1%")
- Counts: Show as plain numbers (e.g., "131 passed out of 147 total")
- Always include context: what the number means, not just the value

### Response style:

- Keep responses concise — lead with the answer, then provide details
- Use tables for comparing multiple labs
- When a lab has 0 submissions or 0% pass rate, mention this explicitly (it may mean no data yet)

### When user asks "what can you do?":

Explain your current capabilities:
- "I can query the LMS backend for live data about labs, learners, and performance metrics."
- "I can show you pass rates, completion rates, submission timelines, group performance, and top learners for any lab."
- "I can check if the backend is healthy and trigger the sync pipeline if needed."
- "I need you to specify which lab you're interested in for most queries."

## Integration with structured-ui

When presenting lab choices, use the `structured-ui` skill's `choice` type:
- `chat_id`: Pass the current chat ID from runtime context
- `labels`: Use lab titles (e.g., "Lab 01 – Products, Architecture & Roles")
- `values`: Use lab IDs (e.g., "lab-01")
- `question`: "Which lab would you like to see?"

This enables interactive selection on supported chat channels (WebSocket web client).
