"""
mcp_server.py — MCP-сервер Lorenzo: инструменты для работы с базой знаний.
Stage 5: постоянный сервис, доступный любому MCP-совместимому LLM-агенту.

Инструменты:
  search_docs(query)         — полнотекстовый поиск по search_index.json
  get_decisions(topic)       — решения по теме из DECISIONS.md
  get_contacts(project)      — контакты авторов из CONTACTS.md
  get_project_status(name)   — теги, упоминания, связи проекта
  run_improve(script, dry_run) — запустить скрипт обработки
  get_health()               — общий балл здоровья репозитория
  list_scripts()             — список доступных скриптов

Установка:
  pip install mcp

Запуск (stdio режим для Claude Desktop):
  python scripts/mcp_server.py

Конфигурация для Claude Desktop (~/.claude/claude_desktop_config.json):
  {
    "mcpServers": {
      "lorenzo": {
        "command": "python",
        "args": ["/path/to/lorenzo/scripts/mcp_server.py"],
        "env": {}
      }
    }
  }
"""
import re
import sys
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

# ---------------------------------------------------------------------------
# Утилиты: чтение данных из docs/
# ---------------------------------------------------------------------------

def _load_index() -> list[dict]:
    path = DOCS / "search_index.json"
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, list) else data.get("docs", [])


def _tokenize(text: str) -> list[str]:
    words = re.findall(r'[а-яёa-z][а-яёa-z\-]{1,}', text.lower())
    stop = {"и", "в", "на", "что", "как", "это", "для", "или", "но",
            "the", "a", "an", "of", "in", "to", "is", "are", "for"}
    return [w for w in words if w not in stop]


def _doc_text(doc: dict) -> str:
    """search_index.json uses 'content' (new) or 'preview' (old) — 356/460 files
    have empty 'content' but populated 'preview'. Use the best available field."""
    return " ".join(filter(None, [
        doc.get("content", ""),
        doc.get("preview", ""),
        doc.get("summary", ""),
    ]))


def _search(query: str, top_k: int = 8) -> list[dict]:
    index = _load_index()
    tokens = _tokenize(query)
    scored = []
    for doc in index:
        body  = _doc_text(doc).lower()
        title = doc.get("title", "").lower()
        path  = doc.get("path", "").lower()
        tags  = " ".join(doc.get("tags", [])).lower()

        score = 0.0
        for t in tokens:
            if t in title: score += 5.0 + title.count(t) * 0.5
            if t in path:  score += 3.0
            if t in tags:  score += 2.0
            if t in body:  score += 1.0 + body.count(t) * 0.05

        if score > 0:
            scored.append((score, doc))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [d for _, d in scored[:top_k]]


def _extract_section(text: str, keyword: str, lines_after: int = 30) -> str:
    keyword_lower = keyword.lower()
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if keyword_lower in line.lower():
            return "\n".join(lines[i:i + lines_after])
    return ""


def _read_doc(filename: str) -> str:
    path = DOCS / filename
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _list_improve_scripts() -> list[str]:
    return sorted(p.name for p in (ROOT / "scripts").glob("improve_*.py"))


# ---------------------------------------------------------------------------
# MCP сервер
# ---------------------------------------------------------------------------

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import TextContent, Tool
    import asyncio
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False

if not MCP_AVAILABLE:
    print("MCP не установлен. Запустите: pip install mcp", file=sys.stderr)
    print("\nДоступные инструменты (демо-режим):", file=sys.stderr)
    print("  search_docs, get_decisions, get_contacts,", file=sys.stderr)
    print("  get_project_status, run_improve, get_health, list_scripts", file=sys.stderr)
    sys.exit(1)

server = Server("lorenzo-knowledge")


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="search_docs",
            description="Полнотекстовый поиск по всем документам Lorenzo. "
                        "Возвращает топ-8 релевантных файлов с выдержками.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Поисковый запрос"},
                    "top_k": {"type": "integer", "default": 5, "description": "Число результатов"},
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="get_decisions",
            description="Возвращает ключевые решения по теме из DECISIONS.md.",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "Тема: архитектура, память, RAG, и т.п."},
                },
                "required": ["topic"],
            },
        ),
        Tool(
            name="get_contacts",
            description="Контакты авторов проектов из CONTACTS.md. "
                        "project — название проекта или слой (memory, rag, orchestration).",
            inputSchema={
                "type": "object",
                "properties": {
                    "project": {"type": "string", "description": "Проект или слой"},
                },
                "required": ["project"],
            },
        ),
        Tool(
            name="get_project_status",
            description="Статус проекта: теги, число упоминаний, похожие документы, контакт.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Название проекта (Yodoca, NGT, AgentFS...)"},
                },
                "required": ["name"],
            },
        ),
        Tool(
            name="run_improve",
            description="Запустить скрипт обработки документов. "
                        "По умолчанию dry_run=true — не меняет файлы, только показывает план.",
            inputSchema={
                "type": "object",
                "properties": {
                    "script": {"type": "string", "description": "Имя скрипта (improve_metrics.py)"},
                    "dry_run": {"type": "boolean", "default": True},
                },
                "required": ["script"],
            },
        ),
        Tool(
            name="get_health",
            description="Общий балл здоровья репозитория из HEALTH.md и SCORING.md.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="list_scripts",
            description="Список всех доступных скриптов обработки (improve_*.py).",
            inputSchema={
                "type": "object",
                "properties": {
                    "group": {
                        "type": "string",
                        "description": "Фильтр по группе: structure, index, analysis, extract, quality, graph, reports, export, llm",
                        "enum": ["structure", "index", "analysis", "extract",
                                 "quality", "graph", "reports", "export", "llm", "all"],
                    },
                },
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    try:
        result = _dispatch(name, arguments)
    except Exception as e:
        result = f"❌ Ошибка: {e}"
    return [TextContent(type="text", text=result)]


def _dispatch(name: str, args: dict) -> str:
    if name == "search_docs":
        return _tool_search(args.get("query", ""), args.get("top_k", 5))
    if name == "get_decisions":
        return _tool_decisions(args.get("topic", ""))
    if name == "get_contacts":
        return _tool_contacts(args.get("project", ""))
    if name == "get_project_status":
        return _tool_project_status(args.get("name", ""))
    if name == "run_improve":
        return _tool_run_improve(args.get("script", ""), args.get("dry_run", True))
    if name == "get_health":
        return _tool_health()
    if name == "list_scripts":
        return _tool_list_scripts(args.get("group", "all"))
    return f"Неизвестный инструмент: {name}"


# ---------------------------------------------------------------------------
# Реализации инструментов
# ---------------------------------------------------------------------------

def _tool_search(query: str, top_k: int) -> str:
    if not query:
        return "Укажите поисковый запрос."
    hits = _search(query, top_k)
    if not hits:
        return f"Ничего не найдено по запросу: «{query}»"
    lines = [f"Найдено {len(hits)} результатов для «{query}»:\n"]
    for h in hits:
        title = h.get("title", h.get("path", "?"))
        path  = h.get("path", "")
        snippet = h.get("content", "")[:200].replace("\n", " ")
        lines.append(f"**{title}**\n`{path}`\n> {snippet}...\n")
    return "\n".join(lines)


def _tool_decisions(topic: str) -> str:
    text = _read_doc("DECISIONS.md")
    if not text:
        return "DECISIONS.md не найден. Запустите improve_decisions.py"
    section = _extract_section(text, topic, lines_after=40)
    if not section:
        # Общий поиск по всему файлу
        lines = [l for l in text.splitlines() if topic.lower() in l.lower()]
        if not lines:
            return f"Решения по теме «{topic}» не найдены."
        section = "\n".join(lines[:20])
    return f"## Решения по теме «{topic}»\n\n{section}"


def _tool_contacts(project: str) -> str:
    text = _read_doc("CONTACTS.md")
    if not text:
        return "CONTACTS.md не найден. Запустите improve_contacts.py"
    proj_lower = project.lower()
    lines = text.splitlines()
    relevant = []
    in_section = False
    for line in lines:
        if proj_lower in line.lower():
            in_section = True
        if in_section:
            relevant.append(line)
            if len(relevant) > 15:
                break
    if not relevant:
        return f"Контакты для «{project}» не найдены."

    # Также ищем файл в docs/contacts/
    contact_dir = DOCS / "contacts"
    contact_files = []
    if contact_dir.exists():
        for f in sorted(contact_dir.glob("*.md")):
            if proj_lower in f.read_text(encoding="utf-8").lower():
                contact_files.append(str(f.relative_to(ROOT)))

    result = f"## Контакты: «{project}»\n\n" + "\n".join(relevant[:15])
    if contact_files:
        result += f"\n\n**Контактные файлы:**\n" + "\n".join(f"- `{p}`" for p in contact_files)
    return result


def _tool_project_status(name: str) -> str:
    name_lower = name.lower()
    lines_out = [f"## Статус проекта: {name}\n"]

    # Упоминания из ENTITIES.md
    ent = _read_doc("ENTITIES.md")
    for line in ent.splitlines():
        if name_lower in line.lower() and re.search(r'\d+', line):
            lines_out.append(f"**Упоминания:** {line.strip()}")
            break

    # Теги из TAGS.md
    tags_text = _read_doc("TAGS.md")
    found_tags = []
    for line in tags_text.splitlines():
        tag_m = re.match(r'##\s*#(\w+)', line)
        if tag_m:
            current_tag = tag_m.group(1)
        elif name_lower in line.lower() and '`docs/' in line:
            found_tags.append(current_tag)
    if found_tags:
        lines_out.append(f"**Теги:** {', '.join(set(found_tags))}")

    # Похожие документы из SIMILAR.md
    similar_text = _read_doc("SIMILAR.md")
    similar_hits = []
    for line in similar_text.splitlines():
        if name_lower in line.lower() and re.search(r'[\d.]+', line):
            similar_hits.append(line.strip())
            if len(similar_hits) >= 3:
                break
    if similar_hits:
        lines_out.append("\n**Похожие документы:**")
        lines_out.extend(similar_hits)

    # Контакт
    contacts_text = _read_doc("CONTACTS.md")
    for line in contacts_text.splitlines():
        if name_lower in line.lower() and '|' in line:
            lines_out.append(f"\n**Контакт:** {line.strip()}")
            break

    return "\n".join(lines_out) if len(lines_out) > 1 else f"Проект «{name}» не найден в базе."


def _tool_run_improve(script: str, dry_run: bool) -> str:
    if not script:
        return "Укажите имя скрипта."
    script_path = ROOT / "scripts" / script
    if not script_path.exists():
        available = [s for s in _list_improve_scripts() if script.lower() in s.lower()]
        hint = f"\nПохожие: {', '.join(available)}" if available else ""
        return f"Скрипт {script} не найден.{hint}"

    # Проверка безопасности: разрешаем только improve_*.py
    if not script.startswith("improve_"):
        return f"Разрешены только скрипты improve_*.py. Получено: {script}"

    cmd = [sys.executable, str(script_path)]
    if dry_run:
        cmd.append("--dry-run")

    result = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT, timeout=60)
    output = result.stdout[-3000:] if result.stdout else ""
    errors = result.stderr[-1000:] if result.stderr else ""

    status = "✅ Успешно" if result.returncode == 0 else "❌ Ошибка"
    mode   = "[dry-run]" if dry_run else "[реальный запуск]"
    return f"{status} {mode} {script}\n\n{output}\n{errors}".strip()


def _tool_health() -> str:
    health_text  = _read_doc("HEALTH.md")
    scoring_text = _read_doc("SCORING.md")
    metrics_text = _read_doc("METRICS.md")

    lines = ["## Здоровье репозитория Lorenzo\n"]

    for text, fname in [(health_text, "HEALTH.md"), (scoring_text, "SCORING.md"),
                        (metrics_text, "METRICS.md")]:
        if not text:
            continue
        # Берём первые 10 значимых строк
        relevant = [l for l in text.splitlines()
                    if l.strip() and not l.startswith("<!--") and not l.startswith("_")][:12]
        lines.append(f"**{fname}:**\n" + "\n".join(relevant[:10]))
        lines.append("")

    return "\n".join(lines)


def _tool_list_scripts(group: str) -> str:
    group_map = {
        "structure": ["merge_short", "readmes", "summaries", "tags", "toc", "autocorrect"],
        "index":     ["glossary", "crossrefs", "search_index", "index_update", "timeline", "backlinks"],
        "analysis":  ["dedup", "clusters", "word_freq", "priorities", "similar", "complexity",
                      "sentiment", "density", "heatmap"],
        "extract":   ["action_items", "decisions", "questions", "kpi", "entities", "concepts",
                      "abbreviations", "extract_tables", "extract_code"],
        "quality":   ["consistency", "broken_links", "missing", "orphans", "validate",
                      "metrics", "alerts"],
        "graph":     ["graph", "mindmap", "network", "narrative"],
        "reports":   ["qa", "contacts", "changelog", "reading_order", "stats", "health",
                      "compare", "sitemap", "report"],
        "export":    ["export_csv", "export_json", "export_html"],
        "llm":       ["llm_enrich", "llm_summary", "llm_qa", "autofill"],
    }

    all_scripts = _list_improve_scripts()

    if group == "all" or group not in group_map:
        result = f"Всего скриптов: {len(all_scripts)}\n\n"
        for g, keywords in group_map.items():
            matched = [s for s in all_scripts if any(k in s for k in keywords)]
            result += f"**{g}** ({len(matched)}): {', '.join(matched)}\n"
        return result

    keywords = group_map[group]
    matched = [s for s in all_scripts if any(k in s for k in keywords)]
    return f"**Группа {group}** ({len(matched)} скриптов):\n" + "\n".join(f"- `{s}`" for s in matched)


# ---------------------------------------------------------------------------
# Запуск
# ---------------------------------------------------------------------------

async def main_async():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, write_stream,
            server.create_initialization_options(),
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main_async())
