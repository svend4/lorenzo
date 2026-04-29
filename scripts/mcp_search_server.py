"""
mcp_search_server.py — MCP-сервер lorenzo-search.

Read-only поиск по корпусу. Безопасен для подключения любому клиенту.

Инструменты:
  search_docs(query, top_k)        — полнотекстовый поиск
  bm25_passages(query, top_k)      — поиск по абзацам (если есть passages.json)
  find_similar(file_path, top_k)   — похожие документы из SIMILAR.md
  faceted_search(query, entity, type, section) — фасетный поиск через скрипт

Ресурсы:
  lorenzo://search-index           — search_index.json как Resource

Запуск:
  python scripts/mcp_search_server.py
"""
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from mcp_common import (
    ROOT, DOCS, build_server, run_stdio, search, load_search_index,
    read_doc, list_improve_scripts,
)
try:
    from mcp.types import Tool, Resource, Prompt, PromptArgument
except ImportError:
    class _MCPStub:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
    Tool = Resource = Prompt = PromptArgument = _MCPStub  # type: ignore


def tool_search_docs(query: str, top_k: int = 5) -> str:
    if not query:
        return "Укажите query."
    hits = search(query, top_k)
    if not hits:
        return f"Ничего не найдено по «{query}»"
    lines = [f"Найдено {len(hits)} документов по запросу «{query}»:\n"]
    for h in hits:
        title = h.get("title", h.get("path", "?"))
        path = h.get("path", "")
        snippet = h.get("content", h.get("preview", ""))[:200].replace("\n", " ")
        lines.append(f"**{title}**\n`{path}`\n> {snippet}…\n")
    return "\n".join(lines)


def tool_bm25_passages(query: str, top_k: int = 10) -> str:
    """BM25 по абзацам. Использует improve_passage_retrieval.py."""
    if not query:
        return "Укажите query."
    script = ROOT / "scripts" / "improve_passage_retrieval.py"
    if not script.exists():
        return "improve_passage_retrieval.py не найден."
    cmd = [sys.executable, str(script), "--query", query, "--top", str(top_k)]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT, timeout=30)
    out = result.stdout.strip() or result.stderr.strip()
    return out[:3000]


def tool_find_similar(file_path: str, top_k: int = 5) -> str:
    """Похожие документы из docs/SIMILAR.md."""
    text = read_doc("SIMILAR.md")
    if not text:
        return "SIMILAR.md не найден. Запустите improve_similar.py"
    fname = Path(file_path).name.lower()
    lines = text.splitlines()
    relevant = []
    in_block = False
    for line in lines:
        if fname in line.lower():
            in_block = True
        if in_block:
            relevant.append(line)
            if line.strip().startswith('## ') and len(relevant) > 1:
                break
            if len(relevant) > top_k * 3:
                break
    return "\n".join(relevant) if relevant else f"Похожие для {file_path} не найдены."


def tool_faceted_search(query: str = "", entity: str = "",
                        type_: str = "", section: str = "") -> str:
    script = ROOT / "scripts" / "improve_faceted_search.py"
    if not script.exists():
        return "improve_faceted_search.py не найден."
    cmd = [sys.executable, str(script)]
    if query:
        cmd.extend(["--query", query])
    if entity:
        cmd.extend(["--entity", entity])
    if type_:
        cmd.extend(["--type", type_])
    if section:
        cmd.extend(["--section", section])
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT, timeout=30)
    return (result.stdout or result.stderr).strip()[:3000]


def dispatch(name: str, args: dict) -> str:
    if name == "search_docs":
        return tool_search_docs(args.get("query", ""), args.get("top_k", 5))
    if name == "bm25_passages":
        return tool_bm25_passages(args.get("query", ""), args.get("top_k", 10))
    if name == "find_similar":
        return tool_find_similar(args.get("file_path", ""), args.get("top_k", 5))
    if name == "faceted_search":
        return tool_faceted_search(
            args.get("query", ""),
            args.get("entity", ""),
            args.get("type", ""),
            args.get("section", ""),
        )
    return f"Неизвестный инструмент: {name}"


TOOLS = [
    Tool(
        name="search_docs",
        description="Полнотекстовый поиск по всем документам Lorenzo. Топ-K релевантных файлов.",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Поисковый запрос"},
                "top_k": {"type": "integer", "default": 5},
            },
            "required": ["query"],
        },
    ),
    Tool(
        name="bm25_passages",
        description="BM25-поиск по абзацам. Выдаёт самые релевантные пассажи, не файлы целиком.",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "top_k": {"type": "integer", "default": 10},
            },
            "required": ["query"],
        },
    ),
    Tool(
        name="find_similar",
        description="Документы похожие на указанный файл (из docs/SIMILAR.md).",
        inputSchema={
            "type": "object",
            "properties": {
                "file_path": {"type": "string"},
                "top_k": {"type": "integer", "default": 5},
            },
            "required": ["file_path"],
        },
    ),
    Tool(
        name="faceted_search",
        description="Фасетный поиск с фильтрами по сущности, типу, секции.",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "entity": {"type": "string", "description": "Имя проекта/автора/термина"},
                "type": {"type": "string", "description": "projects | people | concepts | dates"},
                "section": {"type": "string", "description": "01-svyazi | nautilus | …"},
            },
        },
    ),
]


RESOURCES = [
    Resource(
        uri="lorenzo://search-index",
        name="Lorenzo search index",
        description="JSON-индекс всех документов с тегами и превью",
        mimeType="application/json",
    ),
    Resource(
        uri="lorenzo://docs/INDEX.md",
        name="Главный индекс",
        description="Навигационный хаб документации",
        mimeType="text/markdown",
    ),
    Resource(
        uri="lorenzo://docs/SCRIPTS_CATALOG.md",
        name="Каталог скриптов",
        description="Все improve_*.py с описаниями и группами",
        mimeType="text/markdown",
    ),
]


def read_resource(uri: str) -> str:
    if uri == "lorenzo://search-index":
        path = DOCS / "search_index.json"
        return path.read_text(encoding="utf-8") if path.exists() else "[]"
    if uri.startswith("lorenzo://docs/"):
        rel = uri[len("lorenzo://docs/"):]
        return read_doc(rel)
    return ""


PROMPTS = [
    Prompt(
        name="lorenzo-search-topic",
        description="Полный поиск по теме с топ-10 пассажами и резюме",
        arguments=[PromptArgument(name="topic", description="Тема для поиска", required=True)],
    ),
    Prompt(
        name="lorenzo-find-similar-to",
        description="Найти документы похожие на указанный",
        arguments=[PromptArgument(name="file", description="Путь к файлу", required=True)],
    ),
]


def get_prompt(name: str, args: dict) -> str:
    if name == "lorenzo-search-topic":
        topic = args.get("topic", "")
        return (
            f"Используй инструмент `bm25_passages` с query='{topic}' top_k=10, "
            f"затем для топ-3 пассажей вызови `search_docs` чтобы получить полный контекст. "
            f"Сделай резюме найденного и предложи 3 follow-up вопроса."
        )
    if name == "lorenzo-find-similar-to":
        f = args.get("file", "")
        return f"Вызови `find_similar` с file_path='{f}' top_k=8 и сравни с оригиналом по структуре."
    return f"Промпт {name} не определён."


if __name__ == "__main__":
    server = build_server(
        "lorenzo-search",
        TOOLS,
        dispatch,
        resources_spec=RESOURCES,
        resource_reader=read_resource,
        prompts_spec=PROMPTS,
        prompt_getter=get_prompt,
    )
    run_stdio(server)
