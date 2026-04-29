"""
improve_task_codegen.py — генератор слоёв (скилл / MCP-tool / index) из манифестов tasks/*.task.yaml.

Манифест — единый источник истины. По нему собираются:
  1. .claude/skills/<id>.md (если ещё нет — создаётся скелет; если есть — обновляется метаданными)
  2. docs/TASKS_INDEX.md — общий индекс задач
  3. tasks/_generated/<id>.json — машиночитаемая копия для MCP-инструментов
  4. (опционально) tasks/_validation.md — отчёт о невалидных манифестах

Без зависимостей: используется упрощённый YAML-парсер из manifest_parser.

Запуск:
    python scripts/improve_task_codegen.py
    python scripts/improve_task_codegen.py --task write-contact
    python scripts/improve_task_codegen.py --list
    python scripts/improve_task_codegen.py --validate
    python scripts/improve_task_codegen.py --dry-run
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent.parent
TASKS = ROOT / "tasks"
SKILLS = ROOT / ".claude" / "skills"
DOCS = ROOT / "docs"
GENERATED = TASKS / "_generated"


# ---------------------------------------------------------------------------
# Минимальный YAML-парсер с поддержкой вложенных mappings
# ---------------------------------------------------------------------------

def parse_yaml(text: str) -> dict:
    """Простой YAML-парсер: scalars, lists, nested mappings (один уровень).
    Не парсит multi-line strings/anchors. Достаточно для манифестов."""
    lines = text.splitlines()
    return _parse_block(lines, 0, 0)[0]


def _parse_block(lines: list[str], start: int, indent: int) -> tuple[dict | list, int]:
    result_dict: dict = {}
    result_list: list = []
    is_list = False
    i = start
    while i < len(lines):
        raw = lines[i]
        if not raw.strip() or raw.lstrip().startswith('#'):
            i += 1
            continue
        cur_indent = len(raw) - len(raw.lstrip())
        if cur_indent < indent:
            break
        line = raw[cur_indent:]

        if line.startswith('- '):
            is_list = True
            value = line[2:].strip()
            if ':' in value and not value.endswith(':'):
                m = re.match(r'^([\w-]+)\s*:\s*(.+)$', value)
                if m:
                    item: dict = {m.group(1): _coerce(m.group(2))}
                    j = i + 1
                    while j < len(lines):
                        nxt_raw = lines[j]
                        if not nxt_raw.strip() or nxt_raw.lstrip().startswith('#'):
                            j += 1
                            continue
                        nxt_indent = len(nxt_raw) - len(nxt_raw.lstrip())
                        if nxt_indent <= cur_indent:
                            break
                        m2 = re.match(r'^([\w-]+)\s*:\s*(.+)$', nxt_raw[nxt_indent:])
                        if m2:
                            item[m2.group(1)] = _coerce(m2.group(2))
                        j += 1
                    result_list.append(item)
                    i = j
                    continue
            result_list.append(_coerce(value))
            i += 1
            continue

        m = re.match(r'^([\w-]+)\s*:\s*(.*)$', line)
        if not m:
            i += 1
            continue
        key, value = m.group(1), m.group(2).strip()
        if value == '' or value == '{}':
            # Возможно, вложенный блок
            j = i + 1
            sub_indent = None
            while j < len(lines):
                nxt_raw = lines[j]
                if nxt_raw.strip() and not nxt_raw.lstrip().startswith('#'):
                    sub_indent = len(nxt_raw) - len(nxt_raw.lstrip())
                    break
                j += 1
            if sub_indent and sub_indent > cur_indent:
                sub, new_i = _parse_block(lines, i + 1, sub_indent)
                result_dict[key] = sub
                i = new_i
                continue
            result_dict[key] = {} if value == '{}' else None
            i += 1
            continue
        if value.startswith('[') and value.endswith(']'):
            inner = value[1:-1].strip()
            result_dict[key] = [_coerce(x.strip().strip('"\'')) for x in inner.split(',')] if inner else []
        else:
            result_dict[key] = _coerce(value)
        i += 1

    return (result_list if is_list else result_dict), i


def _coerce(s: str):
    s = s.strip()
    if s == '' or s in ('null', '~'):
        return None
    if s.lower() == 'true':
        return True
    if s.lower() == 'false':
        return False
    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        return s[1:-1]
    if re.fullmatch(r'-?\d+', s):
        return int(s)
    if re.fullmatch(r'-?\d+\.\d+', s):
        return float(s)
    return s


# ---------------------------------------------------------------------------
# Загрузка и валидация манифеста
# ---------------------------------------------------------------------------

REQUIRED_FIELDS = {"id", "version", "description"}


def load_manifest(path: Path) -> dict:
    text = path.read_text(encoding='utf-8')
    return parse_yaml(text)


def validate_manifest(manifest: dict, path: Path) -> list[str]:
    errors: list[str] = []
    for field in REQUIRED_FIELDS:
        if field not in manifest or manifest[field] in (None, ''):
            errors.append(f"отсутствует поле {field!r}")
    if 'id' in manifest and not re.match(r'^[a-z][a-z0-9-]+$', str(manifest['id'])):
        errors.append(f"id={manifest['id']!r} должен быть kebab-case (a-z0-9-)")
    if 'trigger_phrases' in manifest:
        if not isinstance(manifest['trigger_phrases'], list):
            errors.append("trigger_phrases должен быть list")
        elif len(manifest['trigger_phrases']) == 0:
            errors.append("trigger_phrases не может быть пустым")
    if 'mcp_server' in manifest:
        valid = {"lorenzo-search", "lorenzo-contacts", "lorenzo-runner", "lorenzo-graph"}
        if manifest['mcp_server'] not in valid:
            errors.append(f"mcp_server={manifest['mcp_server']!r} не в {valid}")
    if 'inputs' in manifest and isinstance(manifest['inputs'], dict):
        for key, spec in manifest['inputs'].items():
            if isinstance(spec, dict) and 'type' in spec:
                if spec['type'] not in ('string', 'integer', 'boolean', 'array', 'object'):
                    errors.append(f"inputs.{key}.type={spec['type']!r} не валиден")
    return errors


# ---------------------------------------------------------------------------
# Генераторы
# ---------------------------------------------------------------------------

def gen_skill_skeleton(manifest: dict) -> str:
    """Генерирует скелет .claude/skills/<id>.md если его ещё нет."""
    sid = manifest['id']
    desc = manifest.get('description', '')
    triggers = manifest.get('trigger_phrases', [])
    related_skills = (manifest.get('related', {}) or {}).get('skills', [])

    lines = [
        f"# {sid}",
        "",
        desc,
        "",
        "## Когда использовать",
        "",
    ]
    for t in triggers:
        lines.append(f'- "{t}"')
    lines.extend([
        "",
        "## Шаги",
        "",
        "[Описание шагов задачи. Сгенерировано из манифеста, заполните вручную.]",
        "",
        "См. манифест: [`tasks/" + sid + ".task.yaml`](../../tasks/" + sid + ".task.yaml)",
        "",
        "## Связанные скилы",
    ])
    for rs in related_skills:
        lines.append(f"- [`{rs}`]({rs}.md)")
    return "\n".join(lines) + "\n"


def gen_index(manifests: list[dict]) -> str:
    lines = ['# Каталог задач (TASKS_INDEX)\n', f'_Обновлено: {date.today().isoformat()}_\n']
    lines.append(f'**Всего задач:** {len(manifests)}\n')
    lines.append('\nЭтот файл автогенерируется из `tasks/*.task.yaml`. Не редактируйте вручную.\n')

    by_server: dict[str, list[dict]] = {}
    for m in manifests:
        srv = m.get('mcp_server', 'standalone')
        by_server.setdefault(srv, []).append(m)

    lines.append('\n## По MCP-серверу\n')
    for srv in sorted(by_server):
        items = by_server[srv]
        lines.append(f'\n### {srv} ({len(items)})\n')
        lines.append('| Task ID | Описание | Триггеры | Шаблон | MCP tool |')
        lines.append('|---------|----------|----------|--------|----------|')
        for m in sorted(items, key=lambda x: x['id']):
            tid = m['id']
            desc = m.get('description', '')[:80].replace('|', '\\|')
            triggers_s = ', '.join(f'"{t}"' for t in (m.get('trigger_phrases', []) or [])[:2])
            tpl = m.get('template', '—')
            tool = m.get('mcp_tool', '—')
            lines.append(f'| `{tid}` | {desc} | {triggers_s} | {tpl} | {tool} |')

    lines.append('\n## Подробно\n')
    for m in sorted(manifests, key=lambda x: x['id']):
        lines.append(f"\n### `{m['id']}`\n")
        lines.append(f"**Описание:** {m.get('description', '')}\n")
        if m.get('trigger_phrases'):
            lines.append("**Триггеры:**")
            for t in m['trigger_phrases']:
                lines.append(f'- "{t}"')
            lines.append("")
        if m.get('inputs'):
            lines.append("**Inputs:**")
            for k, v in m['inputs'].items():
                if isinstance(v, dict):
                    req = " (required)" if v.get('required') else ""
                    lines.append(f"- `{k}`: {v.get('type', 'string')}{req} — {v.get('description', '')}")
            lines.append("")
        if m.get('mcp_server'):
            lines.append(f"**MCP:** {m['mcp_server']} → `{m.get('mcp_tool', '?')}`\n")
        if m.get('template'):
            lines.append(f"**Шаблон:** [`{m['template']}`](templates/{m['template']}.md)\n")
        if m.get('related'):
            r = m['related']
            if r.get('skills'):
                lines.append(f"**Связанные скилы:** {', '.join(r['skills'])}")
            if r.get('templates'):
                lines.append(f"**Связанные шаблоны:** {', '.join(r['templates'])}")
            lines.append("")
    return '\n'.join(lines) + '\n'


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    args = sys.argv[1:]
    dry_run = '--dry-run' in args
    list_only = '--list' in args
    validate_only = '--validate' in args
    one_task: str | None = None

    if '--task' in args:
        idx = args.index('--task')
        if idx + 1 < len(args):
            one_task = args[idx + 1]

    if not TASKS.exists():
        print(f"❌ {TASKS} не найден")
        return 1

    manifests: list[dict] = []
    errors_per_file: dict[Path, list[str]] = {}

    for path in sorted(TASKS.glob('*.task.yaml')):
        try:
            m = load_manifest(path)
        except Exception as e:
            errors_per_file[path] = [f"parse error: {e}"]
            continue
        errs = validate_manifest(m, path)
        if errs:
            errors_per_file[path] = errs
        manifests.append(m)

    if list_only:
        print(f"Найдено манифестов: {len(manifests)}")
        for m in sorted(manifests, key=lambda x: x.get('id', '')):
            print(f"  {m.get('id', '?'):30s} {m.get('description', '')[:60]}")
        return 0

    if validate_only:
        if errors_per_file:
            for path, errs in errors_per_file.items():
                print(f"❌ {path.name}")
                for e in errs:
                    print(f"   — {e}")
            return 1
        print(f"✓ Все {len(manifests)} манифеста валидны")
        return 0

    if one_task:
        manifests = [m for m in manifests if m.get('id') == one_task]
        if not manifests:
            print(f"❌ Задача '{one_task}' не найдена")
            return 1

    GENERATED.mkdir(parents=True, exist_ok=True)
    SKILLS.mkdir(parents=True, exist_ok=True)

    skill_actions: list[str] = []
    json_actions: list[str] = []

    for m in manifests:
        sid = m['id']

        skill_path = SKILLS / f"{sid}.md"
        if not skill_path.exists():
            content = gen_skill_skeleton(m)
            if dry_run:
                skill_actions.append(f"[would create] {skill_path.relative_to(ROOT)}")
            else:
                skill_path.write_text(content, encoding='utf-8')
                skill_actions.append(f"[created] {skill_path.relative_to(ROOT)}")

        json_path = GENERATED / f"{sid}.json"
        if dry_run:
            json_actions.append(f"[would write] {json_path.relative_to(ROOT)}")
        else:
            json_path.write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding='utf-8')
            json_actions.append(f"[written] {json_path.relative_to(ROOT)}")

    index_path = DOCS / 'TASKS_INDEX.md'
    if dry_run:
        print(f"[would write] {index_path.relative_to(ROOT)}")
    else:
        index_path.write_text(gen_index(manifests), encoding='utf-8')
        print(f"→ {index_path.relative_to(ROOT)}")

    for line in skill_actions + json_actions:
        print(f"  {line}")

    if errors_per_file:
        print(f"\n⚠️ Невалидных манифестов: {len(errors_per_file)}")
        for path, errs in errors_per_file.items():
            print(f"   {path.name}: {errs}")
        return 1

    print(f"\n✅ Обработано: {len(manifests)} манифестов")
    return 0


if __name__ == '__main__':
    sys.exit(main())
