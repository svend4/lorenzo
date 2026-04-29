"""
improve_template_migrate.py — миграции frontmatter при изменении схемы шаблона.

Сравнивает frontmatter существующих документов со схемой и предлагает миграции:
  - добавить отсутствующие обязательные поля (с дефолтами)
  - удалить несуществующие в схеме поля
  - привести значения к допустимым enum

Использование:
    python scripts/improve_template_migrate.py --template contact-outreach --dry-run
    python scripts/improve_template_migrate.py --template contact-outreach --apply
    python scripts/improve_template_migrate.py --all --dry-run
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from improve_validate_templates import (
    extract_frontmatter, parse_yaml_simple, load_schemas,
    ROOT, DOCS, SCHEMAS_DIR,
)


def find_docs_with_template(template_name: str) -> list[Path]:
    """Все .md под docs/ с frontmatter, где template == template_name."""
    result: list[Path] = []
    for f in DOCS.rglob('*.md'):
        if 'templates' in f.parts and f.parent.name == 'templates':
            continue
        if '_schemas' in f.parts:
            continue
        text = f.read_text(encoding='utf-8')
        fm, _ = extract_frontmatter(text)
        if fm and fm.get('template') == template_name:
            result.append(f)
    return result


def default_for_type(field_schema: dict):
    if 'enum' in field_schema:
        return field_schema['enum'][0]
    if 'const' in field_schema:
        return field_schema['const']
    if 'type' in field_schema:
        t = field_schema['type'] if isinstance(field_schema['type'], str) else field_schema['type'][0]
        if t == 'string':
            if field_schema.get('format') == 'date':
                return date.today().isoformat()
            return ""
        if t == 'integer':
            return field_schema.get('minimum', 0)
        if t == 'array':
            return []
        if t == 'object':
            return {}
        if t == 'boolean':
            return False
        if t == 'null':
            return None
    return None


def suggest_migrations(file_path: Path, schema: dict) -> list[dict]:
    """Возвращает список предложений по миграции."""
    text = file_path.read_text(encoding='utf-8')
    fm, body = extract_frontmatter(text)
    if not fm:
        return []

    suggestions: list[dict] = []
    properties = schema.get('properties', {})
    required = set(schema.get('required', []))

    # Отсутствующие required
    for req in required:
        if req not in fm:
            field_schema = properties.get(req, {})
            suggestions.append({
                'type': 'add',
                'field': req,
                'value': default_for_type(field_schema),
                'reason': 'required',
            })

    # Поля не в схеме
    for field in fm:
        if field not in properties and properties:
            suggestions.append({
                'type': 'remove',
                'field': field,
                'reason': 'not in schema',
            })

    # Поля с enum, но значение не в enum
    for field, value in fm.items():
        field_schema = properties.get(field)
        if not field_schema or 'enum' not in field_schema:
            continue
        if value not in field_schema['enum']:
            suggestions.append({
                'type': 'fix_enum',
                'field': field,
                'value': value,
                'allowed': field_schema['enum'],
                'reason': 'value not in enum',
            })

    return suggestions


def apply_migrations(file_path: Path, suggestions: list[dict]) -> str:
    """Возвращает новый текст файла с применёнными миграциями."""
    text = file_path.read_text(encoding='utf-8')
    m = re.match(r'\A---\s*\n(.*?)\n---\s*\n', text, re.DOTALL)
    if not m:
        return text
    fm_text = m.group(1)

    for s in suggestions:
        if s['type'] == 'add':
            value_yaml = _to_yaml_value(s['value'])
            fm_text += f"\n{s['field']}: {value_yaml}"
        elif s['type'] == 'remove':
            fm_text = re.sub(rf'^{re.escape(s["field"])}\s*:.*$\n?', '', fm_text, flags=re.MULTILINE)
        elif s['type'] == 'fix_enum':
            new_val = s['allowed'][0]
            fm_text = re.sub(
                rf'^({re.escape(s["field"])})\s*:\s*.+$',
                lambda mm, v=new_val: f'{mm.group(1)}: {_to_yaml_value(v)}',
                fm_text, count=1, flags=re.MULTILINE
            )

    return f"---\n{fm_text.strip()}\n---\n" + text[m.end():]


def _to_yaml_value(v) -> str:
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, list):
        return "[" + ", ".join(_to_yaml_value(x) for x in v) + "]"
    if isinstance(v, str):
        if v in ('null', 'true', 'false') or re.fullmatch(r'-?\d+', v):
            return f'"{v}"'
        return f'"{v}"' if any(c in v for c in ': []{}#') or v == '' else v
    return str(v)


def main():
    args = sys.argv[1:]
    template_name: str | None = None
    apply = '--apply' in args
    dry_run = '--dry-run' in args or not apply
    do_all = '--all' in args

    if '--template' in args:
        idx = args.index('--template')
        if idx + 1 < len(args):
            template_name = args[idx + 1]

    schemas = load_schemas()
    if not schemas:
        print(f"❌ Нет схем в {SCHEMAS_DIR}")
        return 1

    template_names = [template_name] if template_name else (list(schemas) if do_all else [])
    if not template_names:
        print("❌ Укажите --template <имя> или --all")
        return 1

    total_files = 0
    total_changes = 0

    for tname in template_names:
        if tname not in schemas:
            print(f"⚠️ Схема {tname} не найдена")
            continue
        schema = schemas[tname]
        files = find_docs_with_template(tname)
        if not files:
            continue
        print(f"\n## {tname}: {len(files)} документов")
        for f in files:
            sugg = suggest_migrations(f, schema)
            if not sugg:
                continue
            total_files += 1
            total_changes += len(sugg)
            rel = f.relative_to(ROOT)
            print(f"\n  {rel}")
            for s in sugg:
                if s['type'] == 'add':
                    print(f"    + {s['field']} = {s['value']!r}  ({s['reason']})")
                elif s['type'] == 'remove':
                    print(f"    - {s['field']}  ({s['reason']})")
                elif s['type'] == 'fix_enum':
                    print(f"    ~ {s['field']}: {s['value']!r} → {s['allowed'][0]!r}  ({s['reason']})")

            if apply:
                new_text = apply_migrations(f, sugg)
                f.write_text(new_text, encoding='utf-8')

    print(f"\nИтого: {total_files} документов, {total_changes} изменений")
    if dry_run and total_changes:
        print("→ Запустите с --apply чтобы применить.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
