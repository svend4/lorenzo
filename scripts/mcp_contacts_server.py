"""
mcp_contacts_server.py — MCP-сервер lorenzo-contacts.

Изменяющий сервер: обновляет файлы контактов, синхронизирует PROGRESS.md.

Инструменты:
  get_contacts(project)             — read из CONTACTS.md
  get_contact(author)               — read одного docs/contacts/<slug>.md
  list_contacts(status)             — список с фильтром по статусу
  update_contact_status(author, status, note) — write
  propose_outreach(author)          — генерирует первое сообщение по шаблону

Запуск:
  python scripts/mcp_contacts_server.py
"""
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from mcp_common import ROOT, DOCS, build_server, run_stdio, read_doc

try:
    from mcp.types import Tool, Prompt, PromptArgument
except ImportError:
    class _MCPStub:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
    Tool = Resource = Prompt = PromptArgument = _MCPStub  # type: ignore


CONTACT_CHECKBOXES = {
    "studied": "Изучили профиль",
    "messaged": "Написали первое сообщение",
    "replied": "Получили ответ",
    "agreed": "Договорились о сотрудничестве",
}


def tool_get_contacts(project: str) -> str:
    text = read_doc("CONTACTS.md")
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

    contact_dir = DOCS / "contacts"
    contact_files = []
    if contact_dir.exists():
        for f in sorted(contact_dir.glob("*.md")):
            if proj_lower in f.read_text(encoding="utf-8").lower():
                contact_files.append(str(f.relative_to(ROOT)))

    result = f"## Контакты: «{project}»\n\n" + "\n".join(relevant[:15])
    if contact_files:
        result += "\n\n**Контактные файлы:**\n" + "\n".join(f"- `{p}`" for p in contact_files)
    return result


def _find_contact_file(author: str) -> Path | None:
    contact_dir = DOCS / "contacts"
    if not contact_dir.exists():
        return None
    query = author.lower()
    candidates = [f for f in contact_dir.glob("*.md") if query in f.stem.lower()]
    if len(candidates) == 1:
        return candidates[0]
    if len(candidates) > 1:
        # Точное совпадение слага
        exact = [f for f in candidates if f.stem.lower() == query]
        return exact[0] if len(exact) == 1 else None
    slug = re.sub(r'[^a-z0-9]', '-', query)
    direct = contact_dir / f"{slug}.md"
    return direct if direct.exists() else None


def tool_get_contact(author: str) -> str:
    path = _find_contact_file(author)
    if not path:
        contact_dir = DOCS / "contacts"
        available = sorted(f.stem for f in contact_dir.glob("*.md")) if contact_dir.exists() else []
        return f"❌ Контакт '{author}' не найден.\nДоступные: {', '.join(available[:20])}"
    text = path.read_text(encoding='utf-8')
    return f"# {path.stem}\n\n{text[:3000]}"


def tool_list_contacts(status: str = "") -> str:
    contact_dir = DOCS / "contacts"
    if not contact_dir.exists():
        return "docs/contacts/ не найден."
    files = sorted(contact_dir.glob("*.md"))
    rows = []
    for f in files:
        text = f.read_text(encoding="utf-8")
        statuses = []
        for key, label in CONTACT_CHECKBOXES.items():
            if re.search(rf'\[x\].*{re.escape(label)}', text, re.IGNORECASE):
                statuses.append(key)
        last_status = statuses[-1] if statuses else "not_started"
        if status and last_status != status:
            continue
        rows.append((f.stem, last_status))

    if not rows:
        return f"Нет контактов{' со статусом ' + status if status else ''}."
    lines = [f"**Контактов: {len(rows)}**\n", "| Автор | Статус |", "|-------|--------|"]
    for name, st in rows:
        lines.append(f"| `{name}` | {st} |")
    return "\n".join(lines)


def tool_update_contact(author: str, status: str = "", note: str = "") -> str:
    if not author:
        return "❌ Укажите author."
    path = _find_contact_file(author)
    if not path:
        return f"❌ Контакт '{author}' не найден."
    text = path.read_text(encoding="utf-8")
    changes = []

    if status and status in CONTACT_CHECKBOXES:
        label = CONTACT_CHECKBOXES[status]
        pattern = rf'(\[[ x]\])(\s*{re.escape(label)})'
        new_text, count = re.subn(pattern, r'[x]\2', text, flags=re.IGNORECASE)
        if count > 0:
            text = new_text
            changes.append(f"✅ Отмечено: {label}")
        else:
            changes.append(f"⚠️ Строка '{label}' не найдена")

    if note:
        today = date.today().isoformat()
        note_line = f"- {today}: {note}"
        if "## Заметки" in text:
            text = text.replace("## Заметки\n", f"## Заметки\n{note_line}\n")
        else:
            footer = re.search(r'\n---\n', text)
            if footer:
                pos = footer.start()
                text = text[:pos] + f"\n## Заметки\n\n{note_line}\n" + text[pos:]
            else:
                text += f"\n## Заметки\n\n{note_line}\n"
        changes.append(f"📝 Заметка: {note}")

    if not changes:
        lines = [f"## Статус контакта: {path.stem}\n"]
        for key, label in CONTACT_CHECKBOXES.items():
            checked = bool(re.search(rf'\[x\].*{re.escape(label)}', text, re.IGNORECASE))
            lines.append(f"{'✅' if checked else '⬜'} {label}")
        return "\n".join(lines)

    path.write_text(text, encoding="utf-8")

    sync = ROOT / "scripts" / "improve_progress_sync.py"
    if sync.exists():
        result = subprocess.run([sys.executable, str(sync)],
                                capture_output=True, text=True, cwd=ROOT)
        if result.returncode == 0:
            changes.append("📊 PROGRESS.md синхронизирован")
    return f"**{path.stem}** обновлён:\n" + "\n".join(changes)


def tool_propose_outreach(author: str) -> str:
    """Возвращает черновик первого сообщения из контактного файла."""
    path = _find_contact_file(author)
    if not path:
        return f"❌ Контакт '{author}' не найден."
    text = path.read_text(encoding="utf-8")
    m = re.search(r'## Первое сообщение\s*\n+```\n(.*?)\n```', text, re.DOTALL)
    if m:
        return f"## Черновик для {path.stem}\n\n```\n{m.group(1).strip()}\n```"
    return f"⚠️ В файле {path.stem}.md нет секции '## Первое сообщение'.\nВот шаблон:\n\n" + (DOCS / "templates" / "contact-outreach.md").read_text(encoding="utf-8")


def dispatch(name: str, args: dict) -> str:
    if name == "get_contacts":
        return tool_get_contacts(args.get("project", ""))
    if name == "get_contact":
        return tool_get_contact(args.get("author", ""))
    if name == "list_contacts":
        return tool_list_contacts(args.get("status", ""))
    if name == "update_contact_status":
        return tool_update_contact(
            args.get("author", ""),
            args.get("status", ""),
            args.get("note", ""),
        )
    if name == "propose_outreach":
        return tool_propose_outreach(args.get("author", ""))
    return f"Неизвестный инструмент: {name}"


TOOLS = [
    Tool(
        name="get_contacts",
        description="Контакты авторов из CONTACTS.md по проекту/слою.",
        inputSchema={
            "type": "object",
            "properties": {"project": {"type": "string"}},
            "required": ["project"],
        },
    ),
    Tool(
        name="get_contact",
        description="Полный контактный файл одного автора.",
        inputSchema={
            "type": "object",
            "properties": {"author": {"type": "string"}},
            "required": ["author"],
        },
    ),
    Tool(
        name="list_contacts",
        description="Список всех контактов с опциональным фильтром по статусу.",
        inputSchema={
            "type": "object",
            "properties": {
                "status": {"enum": ["", "not_started", "studied", "messaged", "replied", "agreed"]},
            },
        },
    ),
    Tool(
        name="update_contact_status",
        description="Обновляет чекбокс статуса и/или добавляет заметку в файл контакта.",
        inputSchema={
            "type": "object",
            "properties": {
                "author": {"type": "string"},
                "status": {"enum": ["studied", "messaged", "replied", "agreed"]},
                "note": {"type": "string"},
            },
            "required": ["author"],
        },
    ),
    Tool(
        name="propose_outreach",
        description="Возвращает черновик первого сообщения из секции 'Первое сообщение' контактного файла.",
        inputSchema={
            "type": "object",
            "properties": {"author": {"type": "string"}},
            "required": ["author"],
        },
    ),
]


PROMPTS = [
    Prompt(
        name="lorenzo-outreach-day",
        description="День аутрича: топ-3 кандидата + черновики писем",
        arguments=[],
    ),
    Prompt(
        name="lorenzo-write-message",
        description="Написать первое сообщение автору",
        arguments=[
            PromptArgument(name="author", description="Имя автора", required=True),
            PromptArgument(name="goal", description="Цель: коллаборация / вопрос / знакомство"),
        ],
    ),
]


def get_prompt(name: str, args: dict) -> str:
    if name == "lorenzo-outreach-day":
        return (
            "1. Вызови `list_contacts` со статусом 'studied' (изучили, но не писали). "
            "2. Для топ-3 вызови `get_contact` чтобы получить профиль. "
            "3. Для каждого вызови `propose_outreach` чтобы получить черновик. "
            "4. Покажи: автор, проект, синергия, готовый черновик. "
            "5. Спроси, какие отправлять — после подтверждения вызови "
            "`update_contact_status` с status='messaged'."
        )
    if name == "lorenzo-write-message":
        author = args.get("author", "")
        goal = args.get("goal", "коллаборация")
        return (
            f"1. Вызови `get_contact` с author='{author}' для профиля. "
            f"2. Цель сообщения: {goal}. "
            f"3. Вызови `propose_outreach` для базового черновика. "
            f"4. Адаптируй под цель ({goal}): уточни 1 технический вопрос, "
            f"добавь конкретную синергию с Lorenzo. Длина 5-7 предложений."
        )
    return f"Промпт {name} не определён."


if __name__ == "__main__":
    server = build_server(
        "lorenzo-contacts",
        TOOLS,
        dispatch,
        prompts_spec=PROMPTS,
        prompt_getter=get_prompt,
    )
    run_stdio(server)
