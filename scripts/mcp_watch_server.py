"""
mcp_watch_server.py — MCP-сервер lorenzo-watch.

Мониторинг изменений в docs/ и автозапуск релевантных скриптов.

Инструменты:
  recent_changes(hours)         — что изменилось за N часов (git log)
  pending_actions()             — что нужно перезапустить из-за изменений
  watch_status()                — статус watch-демона (если запущен)
  trigger_recompute(section)    — запустить пересчёт связанной секции

Запуск:
  python scripts/mcp_watch_server.py
"""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from mcp_common import ROOT, build_server, run_stdio

try:
    from mcp.types import Tool
except ImportError:
    class _MCPStub:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
    Tool = Resource = Prompt = PromptArgument = _MCPStub  # type: ignore


def tool_recent_changes(hours: int = 24) -> str:
    cmd = ["git", "log", f"--since={hours} hours ago",
           "--name-only", "--pretty=format:%n%h %s"]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT, timeout=15)
    out = result.stdout.strip()
    if not out:
        return f"Нет изменений за последние {hours} часов."
    return f"## Изменения за {hours} ч\n\n```\n{out[:3000]}\n```"


def tool_pending_actions() -> str:
    """git diff --name-only HEAD — что в working tree изменилось."""
    cmd = ["git", "diff", "--name-only", "HEAD"]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT, timeout=15)
    files = result.stdout.strip().splitlines()

    cmd2 = ["git", "diff", "--name-only", "--cached"]
    result2 = subprocess.run(cmd2, capture_output=True, text=True, cwd=ROOT, timeout=15)
    files += result2.stdout.strip().splitlines()

    if not files:
        return "✓ Нет несохранённых изменений."

    docs_files = [f for f in files if f.startswith('docs/')]
    scripts_files = [f for f in files if f.startswith('scripts/')]
    template_files = [f for f in files if 'templates' in f]

    sections: dict[str, int] = {}
    for f in docs_files:
        parts = f.split('/')
        if len(parts) >= 2:
            sections[parts[1]] = sections.get(parts[1], 0) + 1

    lines = [f"## Pending: {len(files)} файлов"]
    if docs_files:
        lines.append(f"\n**docs/**: {len(docs_files)}")
        for sec, cnt in sorted(sections.items(), key=lambda x: -x[1]):
            lines.append(f"  - {sec}: {cnt}")
    if scripts_files:
        lines.append(f"\n**scripts/**: {len(scripts_files)}")
    if template_files:
        lines.append(f"\n**шаблоны:** {len(template_files)} — рекомендуется validate_all")

    lines.append("\n## Рекомендуемые действия")
    if scripts_files:
        lines.append("- `improve_run_all.py --group quality` — скрипты изменились, нужна валидация")
    if template_files:
        lines.append("- `improve_validate_templates.py --report` — шаблоны изменились")
    if docs_files:
        lines.append("- `improve_run_all.py --changed --smart` — обработать изменённые файлы")
    return "\n".join(lines)


def tool_watch_status() -> str:
    cmd = ["pgrep", "-fa", "improve_watch.py"]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
    if result.returncode == 0 and result.stdout.strip():
        return f"## Watch-демон запущен\n\n```\n{result.stdout.strip()}\n```"
    return "Watch-демон не запущен. Команда: `python scripts/improve_watch.py &`"


def tool_trigger_recompute(section: str) -> str:
    if not section:
        return "❌ Укажите section."
    cmd = [sys.executable, str(ROOT / "scripts" / "improve_run_all.py"),
           "--changed", "--smart"]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT, timeout=300)
    return (result.stdout or result.stderr)[-3000:]


def dispatch(name: str, args: dict) -> str:
    if name == "recent_changes":
        return tool_recent_changes(args.get("hours", 24))
    if name == "pending_actions":
        return tool_pending_actions()
    if name == "watch_status":
        return tool_watch_status()
    if name == "trigger_recompute":
        return tool_trigger_recompute(args.get("section", ""))
    return f"Неизвестный инструмент: {name}"


TOOLS = [
    Tool(name="recent_changes", description="Что изменилось за последние N часов (git log).",
         inputSchema={"type": "object",
                      "properties": {"hours": {"type": "integer", "default": 24}}}),
    Tool(name="pending_actions", description="Несохранённые изменения и рекомендуемые действия.",
         inputSchema={"type": "object", "properties": {}}),
    Tool(name="watch_status", description="Статус watch-демона.",
         inputSchema={"type": "object", "properties": {}}),
    Tool(name="trigger_recompute", description="Запустить пересчёт связанной секции.",
         inputSchema={"type": "object", "properties": {"section": {"type": "string"}},
                      "required": ["section"]}),
]


if __name__ == "__main__":
    server = build_server("lorenzo-watch", TOOLS, dispatch)
    run_stdio(server)
