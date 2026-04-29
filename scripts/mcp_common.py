"""
mcp_common.py — общие утилиты и заготовка MCP-сервера.

Используется четырьмя серверами:
  mcp_search_server.py     (lorenzo-search)
  mcp_contacts_server.py   (lorenzo-contacts)
  mcp_runner_server.py     (lorenzo-runner)
  mcp_graph_server.py      (lorenzo-graph)
  mcp_templates_server.py  (lorenzo-templates)
  mcp_export_server.py     (lorenzo-export)
  mcp_llm_server.py        (lorenzo-llm)
  mcp_watch_server.py      (lorenzo-watch)

Содержит:
  - Чтение search_index.json
  - BM25-ранжирование запросов
  - Чтение docs-файлов
  - MCP-обёртка с одной точкой инициализации (build_server)
  - Логирование вызовов в .claude/mcp_calls.jsonl

Если пакет `mcp` не установлен — модуль импортируется без ошибок, но
build_server/run_stdio выбрасывают MCPNotInstalled. Это позволяет тестировать
dispatch() и tools отдельно.
"""
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
LOG_PATH = ROOT / ".claude" / "mcp_calls.jsonl"


class MCPNotInstalled(Exception):
    pass


def load_search_index() -> list[dict]:
    path = DOCS / "search_index.json"
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, list) else data.get("docs", [])


def tokenize(text: str) -> list[str]:
    words = re.findall(r'[а-яёa-z][а-яёa-z\-]{1,}', text.lower())
    stop = {"и", "в", "на", "что", "как", "это", "для", "или", "но",
            "the", "a", "an", "of", "in", "to", "is", "are", "for"}
    return [w for w in words if w not in stop]


def doc_text(doc: dict) -> str:
    return " ".join(filter(None, [
        doc.get("content", ""),
        doc.get("preview", ""),
        doc.get("summary", ""),
    ]))


def search(query: str, top_k: int = 8) -> list[dict]:
    index = load_search_index()
    tokens = tokenize(query)
    scored = []
    for doc in index:
        body = doc_text(doc).lower()
        title = doc.get("title", "").lower()
        path = doc.get("path", "").lower()
        tags = " ".join(doc.get("tags", [])).lower()

        score = 0.0
        for t in tokens:
            if t in title:
                score += 5.0 + title.count(t) * 0.5
            if t in path:
                score += 3.0
            if t in tags:
                score += 2.0
            if t in body:
                score += 1.0 + body.count(t) * 0.05

        if score > 0:
            scored.append((score, doc))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [d for _, d in scored[:top_k]]


def read_doc(filename: str) -> str:
    path = DOCS / filename
    return path.read_text(encoding="utf-8") if path.exists() else ""


def extract_section(text: str, keyword: str, lines_after: int = 30) -> str:
    keyword_lower = keyword.lower()
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if keyword_lower in line.lower():
            return "\n".join(lines[i:i + lines_after])
    return ""


def list_improve_scripts() -> list[str]:
    return sorted(p.name for p in (ROOT / "scripts").glob("improve_*.py"))


def log_call(server: str, tool: str, args: dict, duration_ms: int, status: str):
    """Логирует вызов MCP-инструмента в .claude/mcp_calls.jsonl"""
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "ts": datetime.now().isoformat(timespec='seconds'),
        "server": server,
        "tool": tool,
        "args": args,
        "duration_ms": duration_ms,
        "status": status,
    }
    with LOG_PATH.open('a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')


# ---------------------------------------------------------------------------
# MCP server scaffolding (опциональный импорт mcp)
# ---------------------------------------------------------------------------

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import TextContent, Tool, Resource, Prompt
    import asyncio
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    Server = None
    stdio_server = None
    TextContent = None
    Tool = None
    Resource = None
    Prompt = None
    asyncio = None


def build_server(server_name: str, tools_spec: list, dispatcher, *,
                 resources_spec=None, resource_reader=None,
                 prompts_spec=None, prompt_getter=None):
    """Создаёт MCP-сервер с заданными инструментами/ресурсами/промптами.

    Если mcp не установлен — выбрасывает MCPNotInstalled.
    """
    if not MCP_AVAILABLE:
        raise MCPNotInstalled("pip install mcp")

    server = Server(server_name)

    @server.list_tools()
    async def list_tools():
        return tools_spec

    @server.call_tool()
    async def call_tool(name: str, arguments: dict):
        t0 = time.time()
        status = "ok"
        try:
            result = dispatcher(name, arguments)
        except Exception as e:
            result = f"❌ Ошибка: {e}"
            status = "error"
        duration_ms = int((time.time() - t0) * 1000)
        log_call(server_name, name, arguments, duration_ms, status)
        return [TextContent(type="text", text=result)]

    if resources_spec is not None and resource_reader is not None:
        @server.list_resources()
        async def list_resources():
            return resources_spec

        @server.read_resource()
        async def read_resource(uri: str) -> str:
            return resource_reader(uri)

    if prompts_spec is not None and prompt_getter is not None:
        @server.list_prompts()
        async def list_prompts():
            return prompts_spec

        @server.get_prompt()
        async def get_prompt(name: str, arguments: dict | None = None) -> str:
            return prompt_getter(name, arguments or {})

    return server


def run_stdio(server):
    if not MCP_AVAILABLE:
        raise MCPNotInstalled("pip install mcp")

    async def main_async():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream, write_stream,
                server.create_initialization_options(),
            )
    asyncio.run(main_async())
