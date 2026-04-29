"""
mcp_runner_server.py — MCP-сервер lorenzo-runner.

Запуск improve_*.py скриптов с разрешением только на whitelisted-команды.

Инструменты:
  list_scripts(group)              — список скриптов с фильтром
  describe_script(name)            — docstring + флаги
  run_improve(script, dry_run, args)  — запустить скрипт
  run_group(group, dry_run)        — запустить группу скриптов

Запуск:
  python scripts/mcp_runner_server.py
"""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from mcp_common import ROOT, DOCS, build_server, run_stdio, list_improve_scripts

try:
    from mcp.types import Tool, Prompt, PromptArgument
except ImportError:
    class _MCPStub:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
    Tool = Resource = Prompt = PromptArgument = _MCPStub  # type: ignore


def _load_catalog() -> list[dict]:
    p = DOCS / "scripts_catalog.json"
    if not p.exists():
        return []
    return json.loads(p.read_text(encoding="utf-8"))


def tool_list_scripts(group: str = "all") -> str:
    catalog = _load_catalog()
    if not catalog:
        scripts = list_improve_scripts()
        return f"Каталог не найден (запустите improve_scripts_catalog.py).\nНайдено {len(scripts)} файлов.\n" + \
               "\n".join(f"- `{s}`" for s in scripts[:30])
    if group != "all":
        catalog = [c for c in catalog if c.get("group") == group]
    by_group: dict[str, list] = {}
    for c in catalog:
        by_group.setdefault(c.get("group", "?"), []).append(c)

    lines = [f"**Скриптов: {len(catalog)}** (групп: {len(by_group)})\n"]
    for g in sorted(by_group):
        items = by_group[g]
        lines.append(f"\n### {g} ({len(items)})")
        for it in sorted(items, key=lambda x: x['name']):
            summary = it.get('summary', '')[:80]
            lines.append(f"- `{it['name']}` — {summary}")
    return "\n".join(lines)


def tool_describe_script(name: str) -> str:
    if not name.endswith('.py'):
        name += '.py'
    catalog = _load_catalog()
    entry = next((c for c in catalog if c['name'] == name), None)
    if not entry:
        return f"❌ Скрипт {name} не найден в каталоге."
    lines = [f"# `{entry['name']}`"]
    if entry.get('group'):
        lines.append(f"**Группа:** {entry['group']}")
    if entry.get('summary'):
        lines.append(f"**Описание:** {entry['summary']}")
    if entry.get('description'):
        lines.append(f"\n{entry['description']}")
    if entry.get('flags'):
        lines.append("\n**Флаги:** " + ", ".join(f"`{f}`" for f in entry['flags']))
    return "\n".join(lines)


def tool_run_improve(script: str, dry_run: bool = True, extra_args: list[str] | None = None) -> str:
    if not script:
        return "❌ Укажите script."
    if not script.endswith('.py'):
        script += '.py'
    if not script.startswith('improve_'):
        return f"❌ Только improve_*.py разрешены. Получено: {script}"

    script_path = ROOT / "scripts" / script
    if not script_path.exists():
        available = [s for s in list_improve_scripts() if script.lower() in s.lower()][:5]
        return f"❌ Не найден.\nПохожие: {', '.join(available)}"

    cmd = [sys.executable, str(script_path)]
    if dry_run:
        cmd.append("--dry-run")
    if extra_args:
        cmd.extend(extra_args)

    result = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT, timeout=120)
    output = result.stdout[-3000:] if result.stdout else ""
    errors = result.stderr[-1000:] if result.stderr else ""
    status = "✅" if result.returncode == 0 else "❌"
    mode = "[dry-run]" if dry_run else "[apply]"
    return f"{status} {mode} {script}\n\n{output}\n{errors}".strip()


def tool_run_group(group: str, dry_run: bool = True) -> str:
    if not group:
        return "❌ Укажите group."
    runner = ROOT / "scripts" / "improve_run_all.py"
    if not runner.exists():
        return "improve_run_all.py не найден."
    cmd = [sys.executable, str(runner), "--group", group]
    if dry_run:
        cmd.append("--dry-run")
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT, timeout=600)
    out = result.stdout[-4000:] or result.stderr[-1000:]
    status = "✅" if result.returncode == 0 else "❌"
    return f"{status} Группа `{group}` ({'dry-run' if dry_run else 'apply'})\n\n{out}"


def dispatch(name: str, args: dict) -> str:
    if name == "list_scripts":
        return tool_list_scripts(args.get("group", "all"))
    if name == "describe_script":
        return tool_describe_script(args.get("name", ""))
    if name == "run_improve":
        return tool_run_improve(
            args.get("script", ""),
            args.get("dry_run", True),
            args.get("extra_args", []),
        )
    if name == "run_group":
        return tool_run_group(args.get("group", ""), args.get("dry_run", True))
    return f"Неизвестный инструмент: {name}"


TOOLS = [
    Tool(
        name="list_scripts",
        description="Список всех improve_*.py с фильтром по группе.",
        inputSchema={
            "type": "object",
            "properties": {
                "group": {
                    "type": "string",
                    "description": "Группа: structure, index, analysis, extract, quality, graph, generate, reports, export, cicd, analytics, textwork, deeptext, nlpplus, content, all",
                },
            },
        },
    ),
    Tool(
        name="describe_script",
        description="Подробное описание одного скрипта: docstring, флаги, группа.",
        inputSchema={
            "type": "object",
            "properties": {"name": {"type": "string"}},
            "required": ["name"],
        },
    ),
    Tool(
        name="run_improve",
        description="Запустить improve_*.py. По умолчанию dry_run=true (не меняет файлы).",
        inputSchema={
            "type": "object",
            "properties": {
                "script": {"type": "string"},
                "dry_run": {"type": "boolean", "default": True},
                "extra_args": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["script"],
        },
    ),
    Tool(
        name="run_group",
        description="Запустить целую группу скриптов через improve_run_all.py --group.",
        inputSchema={
            "type": "object",
            "properties": {
                "group": {"type": "string"},
                "dry_run": {"type": "boolean", "default": True},
            },
            "required": ["group"],
        },
    ),
]


PROMPTS = [
    Prompt(
        name="lorenzo-quality-pass",
        description="Прогон quality-группы скриптов с отчётом",
        arguments=[],
    ),
    Prompt(
        name="lorenzo-find-script",
        description="Найти подходящий скрипт под задачу",
        arguments=[PromptArgument(name="task", description="Что нужно сделать", required=True)],
    ),
]


def get_prompt(name: str, args: dict) -> str:
    if name == "lorenzo-quality-pass":
        return (
            "1. Вызови `run_group` с group='quality' dry_run=true для предпросмотра. "
            "2. Если план разумный, спроси подтверждение, затем dry_run=false. "
            "3. После прогона вызови `run_improve` script='improve_health.py' и покажи новый балл."
        )
    if name == "lorenzo-find-script":
        task = args.get("task", "")
        return (
            f"Задача пользователя: «{task}». "
            f"1. Вызови `list_scripts` с group='all'. "
            f"2. Найди скрипты, имена/описания которых матчат задачу. "
            f"3. Для топ-3 кандидатов вызови `describe_script` для деталей. "
            f"4. Предложи лучший вариант с командой запуска."
        )
    return f"Промпт {name} не определён."


if __name__ == "__main__":
    server = build_server(
        "lorenzo-runner",
        TOOLS,
        dispatch,
        prompts_spec=PROMPTS,
        prompt_getter=get_prompt,
    )
    run_stdio(server)
