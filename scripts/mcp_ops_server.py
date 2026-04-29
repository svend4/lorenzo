"""
mcp_ops_server.py — MCP-сервер lorenzo-ops.

Операционные инструменты: диагностика, аудит, perf метрики.

Инструменты:
  doctor()                          — проверка всей системы (docstoolkit doctor)
  audit_query(sql)                  — SELECT на SQLite audit DB (read-only)
  audit_top_tools(n)                — топ-N MCP инструментов
  audit_slow_calls(threshold_ms)    — медленные вызовы
  workflow_history(task_id, limit)  — история запусков workflow
  workflow_stats()                  — агрегаты по задачам
  rebuild_audit_db()                — пересоздать audit.sqlite из jsonl

Read-only для audit (только SELECT). Mutating только rebuild.

Запуск:
  python scripts/mcp_ops_server.py
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(Path(__file__).parent))

from mcp_common import build_server, run_stdio, ROOT

try:
    from mcp.types import Tool, Resource, Prompt, PromptArgument
except ImportError:
    class _MCPStub:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
    Tool = Resource = Prompt = PromptArgument = _MCPStub  # type: ignore


SQL_READ_ONLY_RE = re.compile(r'^\s*select\s', re.IGNORECASE)


def tool_doctor() -> str:
    """Запускает docstoolkit doctor и возвращает отчёт."""
    sys.path.insert(0, str(ROOT / "docs-toolkit"))
    try:
        from docstoolkit.doctor import run_all_checks, render_text
    except ImportError:
        return "❌ docs-toolkit недоступен"
    results = run_all_checks()
    return render_text(results)


def _audit_db():
    sys.path.insert(0, str(Path(__file__).parent))
    from improve_audit_db import get_db
    return get_db()


def tool_audit_query(sql: str) -> str:
    """SELECT-only запрос к audit DB."""
    if not sql:
        return "❌ Укажите sql."
    if not SQL_READ_ONLY_RE.match(sql):
        return "❌ Разрешены только SELECT-запросы."
    if any(kw in sql.lower() for kw in ['insert', 'update', 'delete', 'drop', 'alter']):
        return "❌ Mutating SQL запрещён."

    try:
        conn = _audit_db()
        rows = conn.execute(sql).fetchall()
    except Exception as e:
        return f"❌ {e}"

    if not rows:
        return "(пусто)"
    cols = rows[0].keys()
    widths = [max(len(c), max(len(str(r[c])) for r in rows)) for c in cols]
    lines = [" | ".join(c.ljust(w) for c, w in zip(cols, widths))]
    lines.append("-+-".join('-' * w for w in widths))
    for r in rows[:50]:  # ограничение
        lines.append(" | ".join(str(r[c]).ljust(w) for c, w in zip(cols, widths)))
    if len(rows) > 50:
        lines.append(f"... (показано 50 из {len(rows)})")
    return "```\n" + "\n".join(lines) + "\n```"


def tool_audit_top_tools(n: int = 10) -> str:
    return tool_audit_query(
        f"SELECT server, tool, COUNT(*) AS calls, "
        f"AVG(duration_ms) AS avg_ms, MAX(duration_ms) AS max_ms "
        f"FROM mcp_calls GROUP BY server, tool ORDER BY calls DESC LIMIT {n}"
    )


def tool_audit_slow_calls(threshold_ms: int = 100) -> str:
    return tool_audit_query(
        f"SELECT ts, server, tool, duration_ms, status FROM mcp_calls "
        f"WHERE duration_ms > {threshold_ms} ORDER BY duration_ms DESC LIMIT 20"
    )


def tool_workflow_history(task_id: str = "", limit: int = 10) -> str:
    where = f"WHERE task_id = '{task_id}'" if task_id else ""
    return tool_audit_query(
        f"SELECT run_id, task_id, started, duration_ms, summary_json "
        f"FROM workflow_runs {where} ORDER BY id DESC LIMIT {limit}"
    )


def tool_workflow_stats() -> str:
    return tool_audit_query(
        "SELECT task_id, COUNT(*) AS runs, "
        "AVG(duration_ms) AS avg_ms, "
        "SUM(CASE WHEN dry_run = 0 THEN 1 ELSE 0 END) AS real_runs "
        "FROM workflow_runs GROUP BY task_id ORDER BY runs DESC"
    )


def tool_rebuild_audit_db() -> str:
    """Пересоздать audit DB из jsonl логов."""
    cmd = [sys.executable, str(ROOT / "scripts" / "improve_audit_db.py"), "--rebuild"]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT, timeout=60)
    return (result.stdout or result.stderr).strip()[:1500]


def dispatch(name: str, args: dict) -> str:
    if name == "doctor":
        return tool_doctor()
    if name == "audit_query":
        return tool_audit_query(args.get("sql", ""))
    if name == "audit_top_tools":
        return tool_audit_top_tools(args.get("n", 10))
    if name == "audit_slow_calls":
        return tool_audit_slow_calls(args.get("threshold_ms", 100))
    if name == "workflow_history":
        return tool_workflow_history(args.get("task_id", ""), args.get("limit", 10))
    if name == "workflow_stats":
        return tool_workflow_stats()
    if name == "rebuild_audit_db":
        return tool_rebuild_audit_db()
    return f"Неизвестный инструмент: {name}"


TOOLS = [
    Tool(name="doctor",
         description="Полная диагностика системы: Python, конфиг, шаблоны, плагины, deps.",
         inputSchema={"type": "object", "properties": {}}),
    Tool(name="audit_query",
         description="Read-only SELECT по SQLite audit DB (mcp_calls, workflow_runs, skill_metrics).",
         inputSchema={"type": "object",
                      "properties": {"sql": {"type": "string"}},
                      "required": ["sql"]}),
    Tool(name="audit_top_tools",
         description="Топ-N MCP инструментов по числу вызовов.",
         inputSchema={"type": "object",
                      "properties": {"n": {"type": "integer", "default": 10}}}),
    Tool(name="audit_slow_calls",
         description="MCP-вызовы превышающие порог (мс).",
         inputSchema={"type": "object",
                      "properties": {"threshold_ms": {"type": "integer", "default": 100}}}),
    Tool(name="workflow_history",
         description="История запусков workflow с опц. фильтром по task_id.",
         inputSchema={"type": "object",
                      "properties": {"task_id": {"type": "string"},
                                     "limit": {"type": "integer", "default": 10}}}),
    Tool(name="workflow_stats",
         description="Агрегированная статистика по workflow задачам.",
         inputSchema={"type": "object", "properties": {}}),
    Tool(name="rebuild_audit_db",
         description="Пересоздать SQLite audit DB из jsonl логов.",
         inputSchema={"type": "object", "properties": {}}),
]


PROMPTS = [
    Prompt(name="lorenzo-ops-health",
           description="Полный health check: doctor + audit + workflow stats",
           arguments=[]),
    Prompt(name="lorenzo-ops-perf",
           description="Performance аудит: топ-инструментов + медленные вызовы",
           arguments=[]),
]


def get_prompt(name: str, args: dict) -> str:
    if name == "lorenzo-ops-health":
        return ("1. Вызови `doctor` для проверки системы. "
                "2. Если 0 errors — вызови `workflow_stats`. "
                "3. Вызови `audit_top_tools` с n=10. "
                "4. Сделай сводный отчёт.")
    if name == "lorenzo-ops-perf":
        return ("1. Вызови `audit_top_tools` с n=15 для активных. "
                "2. Вызови `audit_slow_calls` с threshold_ms=200 для медленных. "
                "3. Сравни: какие инструменты часто и медленно?")
    return f"Промпт {name} не определён."


if __name__ == "__main__":
    server = build_server(
        "lorenzo-ops", TOOLS, dispatch,
        prompts_spec=PROMPTS, prompt_getter=get_prompt,
    )
    run_stdio(server)
