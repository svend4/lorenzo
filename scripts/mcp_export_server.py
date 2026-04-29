"""
mcp_export_server.py — MCP-сервер lorenzo-export.

Экспорт корпуса в разные форматы (Obsidian / Confluence / EPUB / RSS).

Инструменты:
  export_obsidian(section)        — Obsidian vault
  export_confluence(section)      — Confluence Wiki
  export_rss(days)                — RSS/Atom фид
  export_epub(section)            — EPUB через pandoc
  export_csv()                    — CSV корпуса
  export_html(section)            — HTML рендер
  export_report()                 — единый Executive Summary
  list_formats()                  — какие форматы доступны

Запуск:
  python scripts/mcp_export_server.py
"""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from mcp_common import ROOT, build_server, run_stdio

try:
    from mcp.types import Tool, Prompt, PromptArgument
except ImportError:
    class _MCPStub:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
    Tool = Resource = Prompt = PromptArgument = _MCPStub  # type: ignore


def _run(script_name: str, args: list[str] | None = None, timeout: int = 120) -> str:
    script = ROOT / "scripts" / script_name
    if not script.exists():
        return f"❌ {script_name} не найден"
    cmd = [sys.executable, str(script)] + (args or [])
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT, timeout=timeout)
    out = result.stdout[-2500:] if result.stdout else ""
    err = result.stderr[-500:] if result.stderr else ""
    status = "✅" if result.returncode == 0 else "❌"
    return f"{status} {script_name}\n\n{out}\n{err}".strip()


def dispatch(name: str, args: dict) -> str:
    section = args.get("section", "")
    section_args = ["--section", section] if section else []
    if name == "export_obsidian":
        return _run("improve_obsidian.py", section_args)
    if name == "export_confluence":
        return _run("improve_confluence.py", section_args)
    if name == "export_rss":
        days = args.get("days", 7)
        return _run("improve_rss.py", ["--days", str(days)] if days else [])
    if name == "export_epub":
        return _run("improve_epub.py", section_args, timeout=300)
    if name == "export_csv":
        return _run("improve_export_csv.py")
    if name == "export_html":
        return _run("improve_export_html.py", section_args, timeout=300)
    if name == "export_report":
        title = args.get("title", "")
        return _run("improve_export_report.py", ["--title", title] if title else [])
    if name == "list_formats":
        return (
            "## Доступные форматы экспорта\n\n"
            "- **obsidian** — vault для Obsidian с wikilinks\n"
            "- **confluence** — Confluence Wiki Markup\n"
            "- **rss** — RSS/Atom фид из git-истории\n"
            "- **epub** — EPUB через pandoc\n"
            "- **csv** — таблица всего корпуса\n"
            "- **html** — статический HTML рендер\n"
            "- **report** — единый Executive Summary в docs/REPORT.md\n"
        )
    return f"Неизвестный инструмент: {name}"


TOOLS = [
    Tool(name="export_obsidian", description="Экспорт в Obsidian vault.",
         inputSchema={"type": "object", "properties": {"section": {"type": "string"}}}),
    Tool(name="export_confluence", description="Экспорт в Confluence Wiki Markup.",
         inputSchema={"type": "object", "properties": {"section": {"type": "string"}}}),
    Tool(name="export_rss", description="Сгенерировать RSS/Atom фид.",
         inputSchema={"type": "object", "properties": {"days": {"type": "integer"}}}),
    Tool(name="export_epub", description="Сгенерировать EPUB через pandoc.",
         inputSchema={"type": "object", "properties": {"section": {"type": "string"}}}),
    Tool(name="export_csv", description="Экспорт корпуса в CSV.",
         inputSchema={"type": "object", "properties": {}}),
    Tool(name="export_html", description="Сгенерировать HTML рендер.",
         inputSchema={"type": "object", "properties": {"section": {"type": "string"}}}),
    Tool(name="export_report", description="Сводный Executive Summary в docs/REPORT.md.",
         inputSchema={"type": "object", "properties": {"title": {"type": "string"}}}),
    Tool(name="list_formats", description="Список доступных форматов.",
         inputSchema={"type": "object", "properties": {}}),
]


PROMPTS = [
    Prompt(
        name="lorenzo-publish",
        description="Запустить полный экспорт во все форматы",
        arguments=[],
    ),
]


def get_prompt(name: str, args: dict) -> str:
    if name == "lorenzo-publish":
        return (
            "1. Вызови `list_formats` чтобы показать пользователю варианты. "
            "2. После выбора (по умолчанию all) — запусти `export_csv`, `export_rss`, `export_obsidian`, `export_confluence`, `export_report` параллельно. "
            "3. Покажи отчёт о статусе каждого."
        )
    return f"Промпт {name} не определён."


if __name__ == "__main__":
    server = build_server(
        "lorenzo-export",
        TOOLS,
        dispatch,
        prompts_spec=PROMPTS,
        prompt_getter=get_prompt,
    )
    run_stdio(server)
