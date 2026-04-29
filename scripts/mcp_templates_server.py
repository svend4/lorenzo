"""
mcp_templates_server.py — MCP-сервер lorenzo-templates.

Шаблоны и манифесты задач: list/init/validate/migrate.

Инструменты:
  list_templates()                      — список доступных шаблонов
  show_template(name)                   — сырой шаблон
  init_doc(template, slug, vars)        — создать документ из шаблона
  validate_doc(file_path)               — валидация одного документа
  validate_all()                        — валидация всего корпуса
  list_tasks()                          — манифесты из tasks/
  show_task(task_id)                    — JSON-копия манифеста

Запуск:
  python scripts/mcp_templates_server.py
"""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from mcp_common import ROOT, DOCS, build_server, run_stdio

try:
    from mcp.types import Tool, Resource, Prompt, PromptArgument
except ImportError:
    class _MCPStub:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
    Tool = Resource = Prompt = PromptArgument = _MCPStub  # type: ignore


TEMPLATES_DIR = DOCS / "templates"
SCHEMAS_DIR = TEMPLATES_DIR / "_schemas"
TASKS_DIR = ROOT / "tasks"
GENERATED = TASKS_DIR / "_generated"


def tool_list_templates() -> str:
    if not TEMPLATES_DIR.exists():
        return "docs/templates/ не найден."
    items = []
    for path in sorted(TEMPLATES_DIR.glob('*.md')):
        if path.name == 'README.md':
            continue
        schema_path = SCHEMAS_DIR / f'{path.stem}.json'
        desc = ''
        if schema_path.exists():
            try:
                desc = json.loads(schema_path.read_text(encoding='utf-8')).get('description', '')
            except Exception:
                pass
        items.append(f"- **`{path.stem}`** — {desc}")
    return f"## Шаблоны ({len(items)})\n\n" + "\n".join(items)


def tool_show_template(name: str) -> str:
    path = TEMPLATES_DIR / f'{name}.md'
    if not path.exists():
        return f"❌ Шаблон {name} не найден."
    return path.read_text(encoding='utf-8')[:5000]


def tool_init_doc(template: str, slug: str, vars_dict: dict) -> str:
    if not template or not slug:
        return "❌ Укажите template и slug."
    cmd = [sys.executable, str(ROOT / "scripts" / "improve_template_init.py"),
           "--type", template, "--slug", slug]
    if vars_dict:
        cmd.append("--vars")
        for k, v in vars_dict.items():
            cmd.append(f"{k}={v}")
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT, timeout=30)
    return (result.stdout or result.stderr).strip()[:2000]


def tool_validate_doc(file_path: str) -> str:
    if not file_path:
        return "❌ Укажите file_path."
    cmd = [sys.executable, str(ROOT / "scripts" / "improve_validate_templates.py"),
           "--file", file_path]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT, timeout=30)
    return (result.stdout or result.stderr).strip()[:2000]


def tool_validate_all() -> str:
    cmd = [sys.executable, str(ROOT / "scripts" / "improve_validate_templates.py"), "--report"]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT, timeout=60)
    return (result.stdout or result.stderr).strip()[:3000]


def tool_list_tasks() -> str:
    if not TASKS_DIR.exists():
        return "tasks/ не найден."
    items = []
    for path in sorted(TASKS_DIR.glob('*.task.yaml')):
        text = path.read_text(encoding='utf-8')
        # Извлечь description
        for line in text.splitlines():
            if line.startswith('description:'):
                desc = line.split(':', 1)[1].strip()
                items.append(f"- **`{path.stem.replace('.task', '')}`** — {desc}")
                break
    return f"## Задачи ({len(items)})\n\n" + "\n".join(items)


def tool_show_task(task_id: str) -> str:
    if not task_id:
        return "❌ Укажите task_id."
    json_path = GENERATED / f"{task_id}.json"
    if not json_path.exists():
        return f"❌ Манифест {task_id} не сгенерирован. Запустите improve_task_codegen.py"
    return json_path.read_text(encoding='utf-8')


def dispatch(name: str, args: dict) -> str:
    if name == "list_templates":
        return tool_list_templates()
    if name == "show_template":
        return tool_show_template(args.get("name", ""))
    if name == "init_doc":
        return tool_init_doc(args.get("template", ""), args.get("slug", ""), args.get("vars", {}))
    if name == "validate_doc":
        return tool_validate_doc(args.get("file_path", ""))
    if name == "validate_all":
        return tool_validate_all()
    if name == "list_tasks":
        return tool_list_tasks()
    if name == "show_task":
        return tool_show_task(args.get("task_id", ""))
    return f"Неизвестный инструмент: {name}"


TOOLS = [
    Tool(
        name="list_templates",
        description="Список всех доступных шаблонов с описаниями.",
        inputSchema={"type": "object", "properties": {}},
    ),
    Tool(
        name="show_template",
        description="Сырой контент шаблона.",
        inputSchema={
            "type": "object",
            "properties": {"name": {"type": "string"}},
            "required": ["name"],
        },
    ),
    Tool(
        name="init_doc",
        description="Создать документ из шаблона. Передайте template, slug и vars.",
        inputSchema={
            "type": "object",
            "properties": {
                "template": {"type": "string"},
                "slug": {"type": "string"},
                "vars": {"type": "object"},
            },
            "required": ["template", "slug"],
        },
    ),
    Tool(
        name="validate_doc",
        description="Валидация одного документа по схеме его шаблона.",
        inputSchema={
            "type": "object",
            "properties": {"file_path": {"type": "string"}},
            "required": ["file_path"],
        },
    ),
    Tool(
        name="validate_all",
        description="Валидация всего корпуса с записью отчёта в docs/VALIDATION.md.",
        inputSchema={"type": "object", "properties": {}},
    ),
    Tool(
        name="list_tasks",
        description="Список манифестов задач из tasks/*.task.yaml.",
        inputSchema={"type": "object", "properties": {}},
    ),
    Tool(
        name="show_task",
        description="JSON-копия манифеста задачи.",
        inputSchema={
            "type": "object",
            "properties": {"task_id": {"type": "string"}},
            "required": ["task_id"],
        },
    ),
]


RESOURCES = [
    Resource(uri="lorenzo://docs/TASKS_INDEX.md", name="Tasks index",
             description="Каталог задач из tasks/", mimeType="text/markdown"),
    Resource(uri="lorenzo://docs/VALIDATION.md", name="Validation report",
             description="Отчёт валидации шаблонов", mimeType="text/markdown"),
]


def read_resource(uri: str) -> str:
    if uri.startswith("lorenzo://docs/"):
        rel = uri[len("lorenzo://docs/"):]
        path = DOCS / rel
        return path.read_text(encoding="utf-8") if path.exists() else ""
    return ""


PROMPTS = [
    Prompt(
        name="lorenzo-create-rfc",
        description="Создать RFC через шаблон с предзаполнением",
        arguments=[
            PromptArgument(name="topic", description="Тема RFC", required=True),
            PromptArgument(name="rfc_id", description="RFC-NNNN", required=False),
        ],
    ),
    Prompt(
        name="lorenzo-validate-corpus",
        description="Прогнать валидацию шаблонов и показать топ ошибок",
        arguments=[],
    ),
]


def get_prompt(name: str, args: dict) -> str:
    if name == "lorenzo-create-rfc":
        topic = args.get("topic", "")
        rfc_id = args.get("rfc_id", "RFC-NNNN")
        return (
            f"1. Вызови `init_doc` с template='rfc', slug='docs/rfcs/{rfc_id}.md', "
            f"vars={{rfc_id: '{rfc_id}', title: '{topic}'}}. "
            f"2. После создания вызови `validate_doc` для проверки. "
            f"3. Если есть ошибки — покажи их пользователю."
        )
    if name == "lorenzo-validate-corpus":
        return (
            "1. Вызови `validate_all`. "
            "2. Проанализируй отчёт: сколько файлов с ошибками, по каким шаблонам. "
            "3. Покажи топ-5 типов ошибок и предложи их исправление."
        )
    return f"Промпт {name} не определён."


if __name__ == "__main__":
    server = build_server(
        "lorenzo-templates",
        TOOLS,
        dispatch,
        resources_spec=RESOURCES,
        resource_reader=read_resource,
        prompts_spec=PROMPTS,
        prompt_getter=get_prompt,
    )
    run_stdio(server)
