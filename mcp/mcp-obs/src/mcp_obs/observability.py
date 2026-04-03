"""HTTP clients for VictoriaLogs and VictoriaTraces APIs."""

from __future__ import annotations

import httpx


class VictoriaLogsClient:
    """Client for VictoriaLogs HTTP API."""

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    async def search_logs(self, query: str, limit: int = 50) -> str:
        """Search logs using LogsQL query."""
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(
                f"{self.base_url}/select/logsql/query",
                params={"query": query, "limit": limit},
            )
            resp.raise_for_status()
            # VictoriaLogs returns NDJSON (one JSON object per line)
            lines = resp.text.strip().split("\n")
            if not lines or lines == [""]:
                return "No logs found matching the query."
            return "\n".join(lines[:limit])

    async def count_errors(self, service: str | None = None, minutes: int = 60) -> str:
        """Count error-level logs over a time window."""
        time_filter = f"_time:{minutes}m"
        parts = [time_filter, "severity:ERROR"]
        if service:
            parts.append(f'service.name:"{service}"')
        query = " ".join(parts)
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(
                f"{self.base_url}/select/logsql/query",
                params={"query": query, "limit": 1000},
            )
            resp.raise_for_status()
            lines = [l for l in resp.text.strip().split("\n") if l.strip()]
            count = len(lines)
            return f"Found {count} error(s) in the last {minutes} minutes."


class VictoriaTracesClient:
    """Client for VictoriaTraces Jaeger-compatible API."""

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    async def list_traces(self, service: str | None = None, limit: int = 10) -> str:
        """List recent traces."""
        async with httpx.AsyncClient(timeout=30) as client:
            params: dict[str, str | int] = {"limit": limit}
            if service:
                params["service"] = service
            resp = await client.get(
                f"{self.base_url}/select/jaeger/api/traces",
                params=params,
            )
            resp.raise_for_status()
            data = resp.json()
            traces = data.get("data", [])
            if not traces:
                return "No traces found."
            results = []
            for t in traces[:limit]:
                tid = t.get("traceID", "unknown")
                spans = t.get("spans", [])
                svc_names = set()
                for s in spans:
                    proc = s.get("process", {})
                    svc = proc.get("serviceName", "unknown")
                    svc_names.add(svc)
                results.append(
                    f"Trace {tid}: {len(spans)} spans, services: {', '.join(sorted(svc_names))}"
                )
            return "\n".join(results)

    async def get_trace(self, trace_id: str) -> str:
        """Fetch a specific trace by ID."""
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(
                f"{self.base_url}/select/jaeger/api/traces/{trace_id}",
            )
            resp.raise_for_status()
            data = resp.json()
            traces = data.get("data", [])
            if not traces:
                return f"No trace found with ID: {trace_id}"
            trace = traces[0]
            spans = trace.get("spans", [])
            results = [f"Trace ID: {trace.get('traceID', 'unknown')}"]
            results.append(f"Total spans: {len(spans)}")
            results.append("")
            for s in spans:
                op = s.get("operationName", "?")
                proc = s.get("process", {})
                svc = proc.get("serviceName", "?")
                dur_ms = s.get("duration", 0) / 1000
                results.append(f"  [{svc}] {op} ({dur_ms:.1f}ms)")
            return "\n".join(results)
