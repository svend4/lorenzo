"""
improve_registry.py — единый реестр всех артефактов проекта в docs/REGISTRY.md.

Сводит в одну таблицу:
  - Скрипты (из docs/SCRIPTS_CATALOG.md)
  - Шаблоны (из docs/templates/_schemas/)
  - Скилы (из .claude/skills/)
  - MCP-серверы (из .claude/mcp.json)
  - Манифесты задач (из tasks/_generated/)
  - Контакты (из docs/contacts/)

Цель: одно место, чтобы понять что есть в проекте.

Запуск:
    python scripts/improve_registry.py
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
SCRIPTS_DIR = ROOT / "scripts"
TEMPLATES = DOCS / "templates"
SCHEMAS = TEMPLATES / "_schemas"
SKILLS = ROOT / ".claude" / "skills"
TASKS_GEN = ROOT / "tasks" / "_generated"
MCP_CONFIG = ROOT / ".claude" / "mcp.json"
CONTACTS = DOCS / "contacts"
OUT = DOCS / "REGISTRY.md"


def collect_scripts() -> list[dict]:
    catalog = DOCS / "scripts_catalog.json"
    if not catalog.exists():
        return []
    return json.loads(catalog.read_text(encoding='utf-8'))


def collect_templates() -> list[dict]:
    if not SCHEMAS.exists():
        return []
    items = []
    for path in sorted(SCHEMAS.glob('*.json')):
        try:
            data = json.loads(path.read_text(encoding='utf-8'))
            items.append({
                'name': path.stem,
                'description': data.get('description', ''),
                'required_fields': data.get('required', []),
                'required_sections': data.get('required_sections', []),
            })
        except Exception:
            continue
    return items


def collect_skills() -> list[dict]:
    if not SKILLS.exists():
        return []
    items = []
    for path in sorted(SKILLS.glob('*.md')):
        text = path.read_text(encoding='utf-8')
        # Первая строка после заголовка
        lines = text.splitlines()
        desc = ''
        for line in lines[1:]:
            line = line.strip()
            if line and not line.startswith('#'):
                desc = line[:120]
                break
        items.append({'name': path.stem, 'description': desc})
    return items


def collect_mcp_servers() -> list[dict]:
    if not MCP_CONFIG.exists():
        return []
    cfg = json.loads(MCP_CONFIG.read_text(encoding='utf-8'))
    items = []
    for name, spec in cfg.get('mcpServers', {}).items():
        items.append({
            'name': name,
            'command': spec.get('command', ''),
            'args': spec.get('args', []),
            'description': spec.get('description', ''),
        })
    return items


def collect_tasks() -> list[dict]:
    if not TASKS_GEN.exists():
        return []
    items = []
    for path in sorted(TASKS_GEN.glob('*.json')):
        try:
            data = json.loads(path.read_text(encoding='utf-8'))
            items.append({
                'id': data.get('id', path.stem),
                'description': data.get('description', ''),
                'mcp_server': data.get('mcp_server', '—'),
                'mcp_tool': data.get('mcp_tool', '—'),
                'template': data.get('template', '—'),
            })
        except Exception:
            continue
    return items


def collect_contacts() -> list[dict]:
    if not CONTACTS.exists():
        return []
    items = []
    for path in sorted(CONTACTS.glob('*.md')):
        if path.name == 'README.md':
            continue
        text = path.read_text(encoding='utf-8')
        # Извлечь author из frontmatter
        m = re.search(r'^author:\s*"?([^"\n]+)"?$', text, re.MULTILINE)
        author = m.group(1) if m else path.stem
        # Status
        m2 = re.search(r'^status:\s*(\w+)', text, re.MULTILINE)
        status = m2.group(1) if m2 else 'unknown'
        items.append({'name': path.stem, 'author': author, 'status': status})
    return items


def main():
    scripts = collect_scripts()
    templates = collect_templates()
    skills = collect_skills()
    servers = collect_mcp_servers()
    tasks = collect_tasks()
    contacts = collect_contacts()

    lines = ['# REGISTRY — реестр артефактов Lorenzo\n',
             f'_Обновлено: {date.today().isoformat()}_\n']

    lines.append('## Сводка\n')
    lines.append('| Слой | Кол-во |')
    lines.append('|------|--------|')
    lines.append(f'| Скрипты `improve_*.py` | {len(scripts)} |')
    lines.append(f'| Шаблоны `docs/templates/*.md` | {len(templates)} |')
    lines.append(f'| Скилы `.claude/skills/*.md` | {len(skills)} |')
    lines.append(f'| MCP-серверы | {len(servers)} |')
    lines.append(f'| Манифесты задач | {len(tasks)} |')
    lines.append(f'| Контакты | {len(contacts)} |')

    # Скрипты по группам
    lines.append('\n## Скрипты по группам\n')
    by_group: dict = {}
    for s in scripts:
        by_group.setdefault(s.get('group', '?'), []).append(s)
    lines.append('| Группа | Скриптов |')
    lines.append('|--------|----------|')
    for group, items in sorted(by_group.items()):
        lines.append(f'| `{group}` | {len(items)} |')

    # Шаблоны
    lines.append('\n## Шаблоны\n')
    lines.append('| Шаблон | Описание | Обязательных секций |')
    lines.append('|--------|----------|---------------------|')
    for t in sorted(templates, key=lambda x: x['name']):
        sections = len(t.get('required_sections', []))
        desc = t.get('description', '')[:80].replace('|', '\\|')
        lines.append(f"| [`{t['name']}`](templates/{t['name']}.md) | {desc} | {sections} |")

    # Скилы
    lines.append('\n## Скилы\n')
    lines.append('| Скилл | Назначение |')
    lines.append('|-------|------------|')
    for s in sorted(skills, key=lambda x: x['name']):
        desc = s.get('description', '').replace('|', '\\|')
        lines.append(f"| [`{s['name']}`](../.claude/skills/{s['name']}.md) | {desc} |")

    # MCP серверы
    lines.append('\n## MCP-серверы\n')
    lines.append('| Сервер | Описание |')
    lines.append('|--------|----------|')
    for srv in sorted(servers, key=lambda x: x['name']):
        desc = srv.get('description', '').replace('|', '\\|')
        lines.append(f"| `{srv['name']}` | {desc} |")

    # Манифесты задач
    lines.append('\n## Манифесты задач\n')
    if tasks:
        lines.append('| ID | Описание | MCP сервер | MCP tool | Шаблон |')
        lines.append('|----|----------|------------|----------|--------|')
        for t in sorted(tasks, key=lambda x: x['id']):
            desc = t.get('description', '')[:60].replace('|', '\\|')
            lines.append(f"| `{t['id']}` | {desc} | `{t['mcp_server']}` | `{t['mcp_tool']}` | `{t['template']}` |")
    else:
        lines.append('_Манифесты не сгенерированы. Запустите improve_task_codegen.py._\n')

    # Контакты
    lines.append('\n## Контакты\n')
    lines.append('| Slug | Автор | Статус |')
    lines.append('|------|-------|--------|')
    for c in sorted(contacts, key=lambda x: x['name']):
        lines.append(f"| `{c['name']}` | {c['author']} | {c['status']} |")

    # Команды
    lines.append('\n## Полезные команды\n')
    lines.append('```bash')
    lines.append('# Создать документ из шаблона')
    lines.append('python scripts/improve_template_init.py --type rfc --slug docs/rfcs/RFC-NNNN.md')
    lines.append('')
    lines.append('# Валидация')
    lines.append('python scripts/improve_validate_templates.py --report')
    lines.append('')
    lines.append('# Запуск пайплайна задачи')
    lines.append('python scripts/improve_workflow_run.py --task audit-corpus')
    lines.append('')
    lines.append('# Каталог скриптов')
    lines.append('python scripts/improve_scripts_catalog.py')
    lines.append('')
    lines.append('# Генерация скилов из манифестов')
    lines.append('python scripts/improve_task_codegen.py')
    lines.append('')
    lines.append('# Реестр артефактов (этот файл)')
    lines.append('python scripts/improve_registry.py')
    lines.append('```')

    OUT.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f"→ {OUT.relative_to(ROOT)}")
    print(f"  Скриптов: {len(scripts)}, шаблонов: {len(templates)}, скилов: {len(skills)}")
    print(f"  MCP-серверов: {len(servers)}, манифестов: {len(tasks)}, контактов: {len(contacts)}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
