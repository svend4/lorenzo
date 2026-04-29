"""
improve_scripts_catalog.py — генератор каталога всех scripts/improve_*.py.

Извлекает первые 10 строк docstring из каждого скрипта и пишет docs/SCRIPTS_CATALOG.md
со структурой:
  - название скрипта
  - краткое описание (первая строка docstring)
  - подробное описание (остальные строки)
  - флаги командной строки (извлечены из docstring/argparse)
  - группа из improve_run_all.py (если есть)

Этот каталог автоматически обновляется и используется скилом `improve` для
auto-discovery вместо хардкода списка скриптов в markdown.

Запуск:
    python scripts/improve_scripts_catalog.py
"""
import ast
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent.parent
SCRIPTS_DIR = ROOT / "scripts"
DOCS = ROOT / "docs"


def extract_docstring(path: Path) -> str:
    """Извлекает module-level docstring."""
    try:
        tree = ast.parse(path.read_text(encoding='utf-8'))
        return ast.get_docstring(tree) or ""
    except Exception:
        return ""


def extract_flags(docstring: str) -> list[str]:
    """Ищет флаги вида --flag в docstring."""
    return sorted(set(re.findall(r'--[a-zA-Z][\w-]*', docstring)))


def extract_summary(docstring: str) -> str:
    """Первая строка docstring (после имени скрипта)."""
    lines = [ln.strip() for ln in docstring.strip().splitlines() if ln.strip()]
    if not lines:
        return ""
    first = lines[0]
    # Убрать «improve_X.py — »
    first = re.sub(r'^improve_\w+\.py\s*[—-]\s*', '', first)
    return first


def extract_description(docstring: str) -> str:
    """Все строки кроме первой и блока запуска."""
    lines = docstring.strip().splitlines()
    if len(lines) < 2:
        return ""
    desc_lines: list[str] = []
    for ln in lines[1:]:
        s = ln.strip()
        if not s:
            continue
        if s.lower().startswith('запуск') or s.lower().startswith('usage'):
            break
        if s.startswith('--') or s.startswith('python '):
            continue
        desc_lines.append(s)
    return ' '.join(desc_lines[:5])


def load_groups() -> dict[str, str]:
    """Парсит improve_run_all.py чтобы понять, в какой группе каждый скрипт."""
    runner = SCRIPTS_DIR / 'improve_run_all.py'
    if not runner.exists():
        return {}
    text = runner.read_text(encoding='utf-8')
    result: dict[str, str] = {}
    current_group: str | None = None
    in_groups = False
    for line in text.splitlines():
        if 'GROUPS = {' in line:
            in_groups = True
            continue
        if not in_groups:
            continue
        if line.startswith('}') or line.startswith('SLOW_SCRIPTS'):
            break
        # Группа: '"name": ['
        m = re.match(r'^\s*"([^"]+)":\s*\[', line)
        if m:
            current_group = m.group(1)
            continue
        # Скрипт: '"improve_X.py",'
        m = re.match(r'^\s*"(improve_\w+\.py)"', line)
        if m and current_group:
            result[m.group(1)] = current_group
    return result


def main():
    scripts = sorted(SCRIPTS_DIR.glob('improve_*.py'))
    groups = load_groups()

    catalog: list[dict] = []
    for path in scripts:
        if path.name == 'improve_scripts_catalog.py':
            continue
        ds = extract_docstring(path)
        catalog.append({
            'name': path.name,
            'summary': extract_summary(ds),
            'description': extract_description(ds),
            'flags': extract_flags(ds),
            'group': groups.get(path.name, 'без группы'),
        })

    # Группировка
    by_group: dict[str, list[dict]] = {}
    for entry in catalog:
        by_group.setdefault(entry['group'], []).append(entry)

    # Markdown
    lines = ['# Каталог скриптов\n', f'_Обновлено: {date.today().isoformat()}_\n']
    lines.append(f'**Всего скриптов:** {len(catalog)}\n')
    lines.append('\n## По группам\n')
    for group in sorted(by_group):
        items = by_group[group]
        lines.append(f'\n### {group} ({len(items)})\n')
        lines.append('| Скрипт | Описание | Флаги |')
        lines.append('|--------|----------|-------|')
        for entry in sorted(items, key=lambda e: e['name']):
            flags_s = ', '.join(f'`{f}`' for f in entry['flags'][:6])
            if len(entry['flags']) > 6:
                flags_s += ', …'
            summary = entry['summary'][:120].replace('|', '\\|')
            lines.append(f"| `{entry['name']}` | {summary} | {flags_s} |")

    lines.append('\n## Подробно\n')
    for entry in sorted(catalog, key=lambda e: e['name']):
        lines.append(f"\n### `{entry['name']}` _(группа: {entry['group']})_\n")
        if entry['summary']:
            lines.append(f"**{entry['summary']}**\n")
        if entry['description']:
            lines.append(f"{entry['description']}\n")
        if entry['flags']:
            lines.append(f"**Флаги:** {', '.join(f'`{f}`' for f in entry['flags'])}\n")

    out_md = DOCS / 'SCRIPTS_CATALOG.md'
    out_md.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f"→ {out_md.relative_to(ROOT)}")

    # JSON для машинного чтения скилами
    out_json = DOCS / 'scripts_catalog.json'
    out_json.write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"→ {out_json.relative_to(ROOT)}")
    print(f"  Скриптов: {len(catalog)}, групп: {len(by_group)}")


if __name__ == '__main__':
    main()
