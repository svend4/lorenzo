# portal-mcp.py

<!-- abstract-auto -->
> **Абстракт** (авто)
>
> 🎯 **Проблема:** portal-mcp.py !IMPORTANT Ключевой документ для понимания архитектуры.
> 🔧 **Подход:** portal-mcp.py !IMPORTANT Ключевой документ для понимания архитектуры.
> 🏷️ **Ключевые слова:** `anthropic`, `vacancies`, `readme`, `appendix`, `minimal`, `working`, `example`, `portal`
>


> [!IMPORTANT]
> Ключевой документ для понимания архитектуры. Рекомендуется прочитать в первую очередь.

<!-- alert-added -->

<!-- summary -->
> Exposes Nautilus Portal as Model Context Protocol tools for LLM clients

---
<!-- tags: rag, ingestion, architecture, collaboration -->




## portal-mcp.py
python
```python
"""
Nautilus Portal MCP Wrapper
============================

Exposes Nautilus Portal as Model Context Protocol tools for LLM clients
(Claude Desktop, Cursor, etc).

MCP Tools Exposed:
- nautilus_query: Search across ecosystem with consensus awareness
- nautilus_query_repo: Search a single repository by name
- nautilus_list_repos: List all registered repositories with metadata
- nautilus_consensus_check: Validate concept agreement across repos
- nautilus_describe: Ecosystem philosophy, version, adapters overview
- nautilus_q6_neighbors: Find Q6-adjacent concepts by Hamming distance
- nautilus_health: Get ecosystem health score (0-100)

Protocol: Nautilus Portal Protocol v1.1
Dependencies: mcp>=1.0.0 (only external dep)
Python: 3.10+

Install:
    pip install mcp>=1.0.0

Run (stdio mode, for Claude Desktop):
    python portal-mcp.py

Run (HTTP mode, for debugging):
    python portal-mcp.py --http --port 8765

License: MIT
Author: svend4
Version: 0.1.0-draft
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import sys
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any

# ============================================================
# MCP SDK imports
# ============================================================
#
# We use the official MCP Python SDK. If not installed, user gets
# a clear error with install instructions.
#
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import (
        TextContent,
        Tool,
    )
except ImportError as e:
    print(
        "ERROR: MCP SDK not installed.\n"
        "  Install with: pip install mcp>=1.0.0\n"
        f"  Details: {e}",
        file=sys.stderr,
    )
    sys.exit(1)


# ============================================================
# Portal integration
# ============================================================
#
# We import NautilusPortal from the local `portal` module.
# The portal MUST be in the same directory as this file (or
# on PYTHONPATH) for the import to work.
#
# If the portal's actual class or method names differ, adjust the
# ADAPTER LAYER below (section "Portal adapter functions").
#
try:
    from portal import NautilusPortal  # type: ignore
except ImportError as e:
    print(
        "ERROR: Could not import NautilusPortal from portal.py.\n"
        "  Make sure portal-mcp.py is in the same directory as portal.py\n"
        "  (or adjust PYTHONPATH).\n"
        f"  Details: {e}",
        file=sys.stderr,
    )
    sys.exit(1)


# ============================================================
# Logging
# ============================================================
#
# MCP runs over stdio by default — we MUST NOT print to stdout
# (that's for JSON-RPC messages). All logs go to stderr.
#
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s %(name)s: %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("nautilus-mcp")


# ============================================================
# Portal instance (singleton)
# ============================================================
#
# We create one NautilusPortal instance and reuse it across tool
# calls. This matches how portal.py is typically used in CLI/API.
#
# If your portal requires special initialization (e.g. loading a
# specific config file), customize the factory below.
#
_portal_instance: NautilusPortal | None = None


def get_portal() -> NautilusPortal:
    """Lazy-initialize portal singleton."""
    global _portal_instance
    if _portal_instance is None:
        logger.info("Initializing NautilusPortal...")
        _portal_instance = NautilusPortal()
        logger.info("Portal initialized: %d adapters loaded",
                    len(_portal_instance.adapters))
    return _portal_instance


# ============================================================
# Portal adapter functions
# ============================================================
#
# These functions are the BRIDGE between MCP tool calls and the
# actual portal methods. If your portal's method names differ,
# adjust THESE functions — the MCP tool handlers below don't need
# to change.
#
# ASSUMPTIONS about portal.py interface (based on STATUS.md and
# INTEGRATION.md analysis):
#
#   NautilusPortal.query(q: str) -> dict
#       Returns dict with keys: entries, consensus, cross_links
#
#   NautilusPortal.adapters: dict[str, BaseAdapter]
#       Map of adapter name -> instance
#
#   BaseAdapter.fetch(query: str) -> list[PortalEntry]
#   BaseAdapter.describe() -> dict
#
#   PortalEntry is a dataclass with fields:
#       id, title, source, format_type, content,
#       metadata, links, is_fallback
#
# If any of these differ in your repo, adjust accordingly.
#


def portal_query_all(query: str, limit: int = 20) -> dict[str, Any]:
    """Query across all registered adapters."""
    portal = get_portal()
    result = portal.query(query)

    # Normalize to plain dict for JSON serialization
    entries = _entries_to_dicts(result.get("entries", [])[:limit])
    consensus = _normalize_consensus(result.get("consensus", {}))

    return {
        "query": query,
        "entries": entries,
        "consensus": consensus,
        "cross_links": result.get("cross_links", [])[:limit],
        "total_found": len(result.get("entries", [])),
    }


def portal_query_one(repo: str, query: str, limit: int = 20) -> dict[str, Any]:
    """Query a single adapter by name."""
    portal = get_portal()
    adapter = portal.adapters.get(repo)
    if adapter is None:
        available = list(portal.adapters.keys())
        return {
            "error": "repo_not_found",
            "message": f"Adapter '{repo}' not registered",
            "available_repos": available,
        }

    try:
        entries = adapter.fetch(query)[:limit]
    except Exception as e:
        logger.exception("Adapter %s failed on query %r", repo, query)
        return {
            "error": "adapter_failed",
            "message": f"Adapter '{repo}' raised: {type(e).__name__}: {e}",
            "repo": repo,
            "query": query,
        }

    return {
        "query": query,
        "repo": repo,
        "entries": _entries_to_dicts(entries),
        "total_found": len(entries),
    }


def portal_list_repos() -> dict[str, Any]:
    """List all registered adapters with metadata."""
    portal = get_portal()
    repos = []
    for name, adapter in portal.adapters.items():
        try:
            describe = adapter.describe()
        except Exception as e:
            logger.warning("Adapter %s .describe() failed: %s", name, e)
            describe = {"error": str(e)}
        repos.append({"name": name, **describe})
    return {"repos": repos, "count": len(repos)}


def portal_consensus_check(concept: str) -> dict[str, Any]:
    """Check if concept is present across repos; return attribution."""
    result = portal_query_all(concept, limit=100)
    consensus = result.get("consensus", {})
    return {
        "concept": concept,
        "agreed": consensus.get("agreed", False),
        "coverage": consensus.get("coverage", 0.0),
        "coverage_with_fallback": consensus.get("coverage_with_fallback", 0.0),
        "present_in": consensus.get("present_in", []),
        "present_in_fallback": consensus.get("present_in_fallback", []),
        "missing_in": consensus.get("missing_in", []),
        "total_entries_found": result.get("total_found", 0),
    }


def portal_describe_ecosystem() -> dict[str, Any]:
    """Return ecosystem philosophy, version, adapter summary."""
    portal = get_portal()
    adapter_names = list(portal.adapters.keys())
    return {
        "ecosystem_name": "svend4",
        "protocol_version": "1.1",
        "philosophy": (
            "Federation over merging: native formats preserved, "
            "consensus via adapters, Q6 as unified coordinate space."
        ),
        "angles": {
            "info1": "methodological (α-levels, how to apply)",
            "pro2": "semantic (Q6 graph, what it means)",
            "meta": "symbolic (CA rules + hexagrams, symbolic structure)",
        },
        "adapters": adapter_names,
        "adapter_count": len(adapter_names),
        "reference_repo": "github.com/svend4/nautilus",
        "specification": "PORTAL-PROTOCOL.md v1.1",
    }


def portal_q6_neighbors(q6_bits: str, distance: int = 1) -> dict[str, Any]:
    """Find Q6-adjacent concepts by Hamming distance."""
    # Validation
    if len(q6_bits) != 6 or not all(c in "01" for c in q6_bits):
        return {
            "error": "invalid_q6",
            "message": f"q6_bits must be 6 chars of '0'/'1', got {q6_bits!r}",
        }
    if not 0 <= distance <= 6:
        return {
            "error": "invalid_distance",
            "message": f"distance must be 0..6, got {distance}",
        }

    # BFS over 6-bit hypercube
    neighbors = _q6_bfs(q6_bits, distance)

    # Query portal for entries at each neighbor vertex
    portal = get_portal()
    neighbor_entries = []
    for vertex in neighbors:
        # Simple heuristic: search for entries with this q6 in metadata
        # (Assumes portal or adapters expose Q6 indexing; may need
        # adjustment based on actual portal API.)
        try:
            result = portal.query(vertex)
            matching = [
                _entry_to_dict(e)
                for e in result.get("entries", [])
                if _get_entry_q6(e) == vertex
            ]
            if matching:
                neighbor_entries.append({
                    "q6": vertex,
                    "hamming_distance": _hamming(q6_bits, vertex),
                    "entries": matching[:5],  # limit per vertex
                })
        except Exception as e:
            logger.debug("Query for %s failed: %s", vertex, e)

    return {
        "center_q6": q6_bits,
        "max_distance": distance,
        "total_neighbors": len(neighbors),
        "neighbors_with_entries": neighbor_entries,
    }


def portal_health() -> dict[str, Any]:
    """Get ecosystem health score (0-100)."""
    portal = get_portal()

    # Try calling health_check module if available
    try:
        import health_check  # type: ignore
        if hasattr(health_check, "compute_health"):
            return health_check.compute_health()  # type: ignore
    except ImportError:
        pass

    # Fallback: compute basic health from adapter counts
    adapters = portal.adapters
    total = len(adapters)
    real_count = 0
    fallback_count = 0
    errors = []

    for name, adapter in adapters.items():
        try:
            entries = adapter.fetch("")  # empty query → fallback usually
            real_in_adapter = sum(
                1 for e in entries if not getattr(e, "is_fallback", True)
            )
            fallback_in_adapter = len(entries) - real_in_adapter
            real_count += real_in_adapter
            fallback_count += fallback_in_adapter
            if real_in_adapter == 0:
                errors.append(f"{name}: 0 real entries")
        except Exception as e:
            errors.append(f"{name}: {type(e).__name__}: {e}")

    # Simple heuristic
    if total == 0:
        score = 0
    else:
        real_ratio = real_count / max(real_count + fallback_count, 1)
        error_penalty = min(len(errors) * 5, 30)
        score = int(100 * real_ratio) - error_penalty
        score = max(0, min(100, score))

    return {
        "score": score,
        "adapters_count": total,
        "real_entries": real_count,
        "fallback_entries": fallback_count,
        "issues": errors,
        "note": "Fallback-computed health. For authoritative score, "
                "call health_check.py directly.",
    }


# ============================================================
# Helper functions
# ============================================================


def _entries_to_dicts(entries: list[Any]) -> list[dict[str, Any]]:
    """Convert list of PortalEntry (dataclass) to list of dicts."""
    return [_entry_to_dict(e) for e in entries]


def _entry_to_dict(entry: Any) -> dict[str, Any]:
    """Convert a single PortalEntry to dict, handling dataclass and dict forms."""
    if is_dataclass(entry):
        return asdict(entry)
    if isinstance(entry, dict):
        return entry
    # Fallback: try to read common attributes
    return {
        "id": getattr(entry, "id", ""),
        "title": getattr(entry, "title", ""),
        "source": getattr(entry, "source", ""),
        "format_type": getattr(entry, "format_type", ""),
        "content": getattr(entry, "content", ""),
        "metadata": getattr(entry, "metadata", {}),
        "links": getattr(entry, "links", []),
        "is_fallback": getattr(entry, "is_fallback", False),
    }


def _normalize_consensus(c: Any) -> dict[str, Any]:
    """Normalize consensus object to dict."""
    if isinstance(c, dict):
        return c
    if is_dataclass(c):
        return asdict(c)
    return {}


def _get_entry_q6(entry: Any) -> str:
    """Extract q6 from entry metadata."""
    if is_dataclass(entry):
        md = getattr(entry, "metadata", {}) or {}
    elif isinstance(entry, dict):
        md = entry.get("metadata", {}) or {}
    else:
        md = {}
    return md.get("q6", "") if isinstance(md, dict) else ""


def _hamming(a: str, b: str) -> int:
    """Hamming distance between two equal-length bit strings."""
    return sum(x != y for x, y in zip(a, b))


def _q6_bfs(start: str, max_distance: int) -> list[str]:
    """BFS over 6-bit hypercube, return all vertices within max_distance."""
    visited: dict[str, int] = {start: 0}
    queue: list[str] = [start]
    while queue:
        current = queue.pop(0)
        dist = visited[current]
        if dist >= max_distance:
            continue
        for i in range(6):
            flipped = list(current)
            flipped[i] = "1" if current[i] == "0" else "0"
            neighbor = "".join(flipped)
            if neighbor not in visited:
                visited[neighbor] = dist + 1
                queue.append(neighbor)
    return list(visited.keys())


def _json_response(data: dict[str, Any]) -> list[TextContent]:
    """Wrap a dict as MCP TextContent response with pretty JSON."""
    return [
        TextContent(
            type="text",
            text=json.dumps(data, ensure_ascii=False, indent=2),
        )
    ]


# ============================================================
# MCP Server setup
# ============================================================

app = Server("nautilus-portal")


@app.list_tools()
async def handle_list_tools() -> list[Tool]:
    """Register all tools exposed by this MCP server."""
    return [
        Tool(
            name="nautilus_query",
            description=(
                "Search across the entire Nautilus ecosystem. "
                "Returns entries from all adapters with consensus "
                "analysis (which repos agree on the concept). "
                "Use this as the default search tool."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (case-insensitive).",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Max entries to return (default 20).",
                        "default": 20,
                    },
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="nautilus_query_repo",
            description=(
                "Search a specific repository by name. "
                "Use nautilus_list_repos first to see valid names. "
                "Returns entries only from that single adapter."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "repo": {
                        "type": "string",
                        "description": (
                            "Adapter name, e.g. 'info1', 'pro2', 'meta'."
                        ),
                    },
                    "query": {
                        "type": "string",
                        "description": "Search query.",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Max entries (default 20).",
                        "default": 20,
                    },
                },
                "required": ["repo", "query"],
            },
        ),
        Tool(
            name="nautilus_list_repos",
            description=(
                "List all registered repositories in the Nautilus "
                "ecosystem with metadata (format, total items, "
                "compatibility level, bridges)."
            ),
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="nautilus_consensus_check",
            description=(
                "Check if a concept is consensus-validated across "
                "the ecosystem. Returns coverage metrics and "
                "per-repo attribution (present/fallback/missing)."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "concept": {
                        "type": "string",
                        "description": "Concept to validate.",
                    }
                },
                "required": ["concept"],
            },
        ),
        Tool(
            name="nautilus_describe",
            description=(
                "Describe the Nautilus ecosystem: philosophy, "
                "protocol version, angles of each repo, adapter "
                "summary. Use this to understand the system before "
                "making queries."
            ),
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="nautilus_q6_neighbors",
            description=(
                "Find Q6-adjacent concepts by Hamming distance. "
                "Q6 is a 6-bit binary hypercube (64 vertices) used "
                "as unified coordinate space. Neighbors at distance "
                "1 differ in one bit; semantically 'close' concepts."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "q6_bits": {
                        "type": "string",
                        "description": (
                            "6-bit string of '0'/'1', e.g. '010100'."
                        ),
                        "pattern": "^[01]{6}$",
                    },
                    "distance": {
                        "type": "integer",
                        "description": (
                            "Max Hamming distance (0-6, default 1)."
                        ),
                        "default": 1,
                        "minimum": 0,
                        "maximum": 6,
                    },
                },
                "required": ["q6_bits"],
            },
        ),
        Tool(
            name="nautilus_health",
            description=(
                "Get ecosystem health score (0-100) with breakdown: "
                "adapter count, real vs fallback entries, known "
                "issues. Use to diagnose ecosystem state."
            ),
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


@app.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, Any]
) -> list[TextContent]:
    """Dispatch tool call to appropriate portal function."""
    logger.info("Tool call: %s with args %r", name, arguments)

    try:
        if name == "nautilus_query":
            result = portal_query_all(
                query=arguments["query"],
                limit=arguments.get("limit", 20),
            )
        elif name == "nautilus_query_repo":
            result = portal_query_one(
                repo=arguments["repo"],
                query=arguments["query"],
                limit=arguments.get("limit", 20),
            )
        elif name == "nautilus_list_repos":
            result = portal_list_repos()
        elif name == "nautilus_consensus_check":
            result = portal_consensus_check(concept=arguments["concept"])
        elif name == "nautilus_describe":
            result = portal_describe_ecosystem()
        elif name == "nautilus_q6_neighbors":
            result = portal_q6_neighbors(
                q6_bits=arguments["q6_bits"],
                distance=arguments.get("distance", 1),
            )
        elif name == "nautilus_health":
            result = portal_health()
        else:
            result = {
                "error": "unknown_tool",
                "message": f"Tool '{name}' not implemented",
            }
    except KeyError as e:
        result = {
            "error": "missing_argument",
            "message": f"Missing required argument: {e}",
        }
    except Exception as e:
        logger.exception("Tool %s raised unexpected exception", name)
        result = {
            "error": "internal_error",
            "message": f"{type(e).__name__}: {e}",
        }

    return _json_response(result)


# ============================================================
# Entry point
# ============================================================

async def run_stdio() -> None:
    """Run MCP server over stdio (default, for Claude Desktop)."""
    logger.info("Starting Nautilus MCP server on stdio")
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Nautilus Portal MCP Wrapper",
    )
    parser.add_argument(
        "--http",
        action="store_true",
        help="Run in HTTP mode instead of stdio (for debugging).",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8765,
        help="HTTP port (default 8765). Only used with --http.",
    )
    parser.add_argument(
        "--warmup",
        action="store_true",
        help="Initialize portal at startup (eager), not lazy.",
    )
    args = parser.parse_args()

    if args.warmup:
        logger.info("Warming up portal...")
        get_portal()

    if args.http:
        logger.error(
            "HTTP mode not yet implemented. Use stdio (default) for "
            "Claude Desktop integration."
        )
        sys.exit(1)

    try:
        asyncio.run(run_stdio())
    except KeyboardInterrupt:
        logger.info("Shutting down on keyboard interrupt")
    except Exception as e:
        logger.exception("Fatal error: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
```
---

<!-- similar-docs -->

---

**Похожие документы:**
- [03-portal-protocol-md](docs/02-anthropic-vacancies/03-portal-protocol-md.md) (сходство 0.22)
- [125-readme-mcp-md-инструкция-по-установке](docs/02-anthropic-vacancies/125-readme-mcp-md-инструкция-по-установке.md) (сходство 0.21)
- [28-appendix-a-minimal-working-example](docs/02-anthropic-vacancies/28-appendix-a-minimal-working-example.md) (сходство 0.17)


<!-- see-also -->

---

**Смотрите также:**
- [28-appendix-a-minimal-working-example](docs/02-anthropic-vacancies/28-appendix-a-minimal-working-example.md)
- [125-readme-mcp-md-инструкция-по-установке](docs/02-anthropic-vacancies/125-readme-mcp-md-инструкция-по-установке.md)
- [98-appendix-a-minimal-working-example](docs/02-anthropic-vacancies/98-appendix-a-minimal-working-example.md)
- [65-readme-md](docs/02-anthropic-vacancies/65-readme-md.md)

