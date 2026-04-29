"""
improve_validate_templates.py — валидация документов по схемам шаблонов.

Сканирует docs/, читает YAML-frontmatter каждого .md файла, ищет соответствующую
схему в docs/templates/_schemas/<template>.json и проверяет:

  1. Frontmatter присутствует и валиден по полям/типам схемы.
  2. Required-поля присутствуют.
  3. Enum-значения соответствуют допустимым.
  4. Required-секции присутствуют в теле документа (заголовки уровня ##).

Без зависимостей: используется упрощённый JSON-Schema-валидатор (не jsonschema).
Покрывает: const, enum, type (string/integer/array/object/null/boolean),
minimum/maximum, minLength, pattern, format=date, items.

Запуск:
    python scripts/improve_validate_templates.py
    python scripts/improve_validate_templates.py --section docs/contacts
    python scripts/improve_validate_templates.py --strict      # exit 1 если есть ошибки
    python scripts/improve_validate_templates.py --report      # пишет docs/VALIDATION.md
    python scripts/improve_validate_templates.py --file docs/contacts/kksudo.md
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
SCHEMAS_DIR = DOCS / "templates" / "_schemas"

FRONTMATTER_RE = re.compile(r'\A---\s*\n(.*?)\n---\s*\n', re.DOTALL)
HEADING_RE = re.compile(r'^##\s+(.+?)\s*$', re.MULTILINE)
DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')


def parse_yaml_simple(text: str) -> dict:
    """Минимальный YAML-парсер для frontmatter: scalars, lists, null, ints.
    Не поддерживает вложенные mappings — для шаблонов не нужны."""
    result: dict = {}
    current_key: str | None = None
    current_list: list | None = None

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line or line.lstrip().startswith('#'):
            continue

        # Элемент списка
        if line.lstrip().startswith('- ') and current_list is not None:
            value = line.lstrip()[2:].strip()
            current_list.append(_coerce_scalar(value))
            continue

        # Новый ключ
        m = re.match(r'^([A-Za-z_][\w-]*)\s*:\s*(.*)$', line)
        if not m:
            continue
        key, value = m.group(1), m.group(2).strip()
        current_key = key
        current_list = None

        if value == '' or value == '[]':
            # Пустой массив или ожидаем элементы списка ниже
            result[key] = [] if value == '[]' else None
            if value == '':
                # Подготовиться к возможному списку
                current_list = []
                result[key] = current_list
        elif value.startswith('[') and value.endswith(']'):
            # Inline-массив
            inner = value[1:-1].strip()
            if not inner:
                result[key] = []
            else:
                items = [s.strip().strip('"\'') for s in inner.split(',')]
                result[key] = [_coerce_scalar(x) for x in items]
        else:
            result[key] = _coerce_scalar(value)

    return result


def _coerce_scalar(s: str):
    if s == '' or s == 'null' or s == '~':
        return None
    if s.lower() == 'true':
        return True
    if s.lower() == 'false':
        return False
    # Кавычки — снять
    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        return s[1:-1]
    # Целое число
    if re.fullmatch(r'-?\d+', s):
        return int(s)
    # Float
    if re.fullmatch(r'-?\d+\.\d+', s):
        return float(s)
    return s


def extract_frontmatter(text: str) -> tuple[dict | None, str]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None, text
    try:
        fm = parse_yaml_simple(m.group(1))
    except Exception:
        return None, text
    body = text[m.end():]
    return fm, body


def extract_headings(body: str) -> set[str]:
    return {h.strip() for h in HEADING_RE.findall(body)}


def load_schemas() -> dict[str, dict]:
    schemas: dict[str, dict] = {}
    if not SCHEMAS_DIR.exists():
        return schemas
    for schema_path in SCHEMAS_DIR.glob('*.json'):
        try:
            data = json.loads(schema_path.read_text(encoding='utf-8'))
            schemas[schema_path.stem] = data
        except Exception as e:
            print(f"  ⚠️  не удалось загрузить {schema_path.name}: {e}")
    return schemas


def validate_value(name: str, value, schema: dict) -> list[str]:
    errors: list[str] = []
    if 'const' in schema:
        if value != schema['const']:
            errors.append(f"{name}: ожидалось {schema['const']!r}, получено {value!r}")
        return errors
    if 'enum' in schema:
        if value not in schema['enum']:
            errors.append(f"{name}: значение {value!r} не в enum {schema['enum']}")
            return errors
    if 'type' in schema:
        types = schema['type'] if isinstance(schema['type'], list) else [schema['type']]
        ok = False
        for t in types:
            if t == 'null' and value is None:
                ok = True
                break
            if t == 'string' and isinstance(value, str):
                ok = True
                break
            if t == 'integer' and isinstance(value, int) and not isinstance(value, bool):
                ok = True
                break
            if t == 'number' and isinstance(value, (int, float)) and not isinstance(value, bool):
                ok = True
                break
            if t == 'boolean' and isinstance(value, bool):
                ok = True
                break
            if t == 'array' and isinstance(value, list):
                ok = True
                break
            if t == 'object' and isinstance(value, dict):
                ok = True
                break
        if not ok:
            errors.append(f"{name}: тип {type(value).__name__} не соответствует {schema['type']}")
            return errors
    if isinstance(value, str):
        if 'minLength' in schema and len(value) < schema['minLength']:
            errors.append(f"{name}: длина {len(value)} < minLength={schema['minLength']}")
        if 'pattern' in schema and not re.search(schema['pattern'], value):
            errors.append(f"{name}: значение {value!r} не соответствует pattern={schema['pattern']!r}")
        if schema.get('format') == 'date' and not DATE_RE.match(value):
            errors.append(f"{name}: ожидался формат YYYY-MM-DD, получено {value!r}")
    if isinstance(value, int) and not isinstance(value, bool):
        if 'minimum' in schema and value < schema['minimum']:
            errors.append(f"{name}: {value} < minimum={schema['minimum']}")
        if 'maximum' in schema and value > schema['maximum']:
            errors.append(f"{name}: {value} > maximum={schema['maximum']}")
    if isinstance(value, list):
        if 'minItems' in schema and len(value) < schema['minItems']:
            errors.append(f"{name}: {len(value)} элементов < minItems={schema['minItems']}")
        if 'items' in schema:
            for i, item in enumerate(value):
                errors.extend(validate_value(f"{name}[{i}]", item, schema['items']))
    return errors


def validate_doc(file_path: Path, schemas: dict) -> list[str]:
    text = file_path.read_text(encoding='utf-8')
    fm, body = extract_frontmatter(text)
    if not fm:
        return []  # Файл без frontmatter — не валидируем (свободный формат)

    template = fm.get('template')
    if not template:
        return [f"frontmatter без поля template"]
    if template not in schemas:
        return [f"шаблон {template!r} не найден в _schemas/"]

    schema = schemas[template]
    errors: list[str] = []

    # Проверка required в frontmatter
    for req in schema.get('required', []):
        if req not in fm:
            errors.append(f"отсутствует обязательное поле {req!r}")

    # Проверка типов и значений
    for field, value in fm.items():
        field_schema = schema.get('properties', {}).get(field)
        if field_schema is None:
            continue  # Допустимы дополнительные поля
        errors.extend(validate_value(field, value, field_schema))

    # Проверка required-секций в теле
    headings = extract_headings(body)
    for req_section in schema.get('required_sections', []):
        if not any(req_section in h for h in headings):
            errors.append(f"отсутствует обязательная секция '## {req_section}'")

    return errors


def main():
    args = sys.argv[1:]
    section = None
    strict = '--strict' in args
    report = '--report' in args
    one_file: Path | None = None

    if '--section' in args:
        idx = args.index('--section')
        if idx + 1 < len(args):
            section = args[idx + 1]
    if '--file' in args:
        idx = args.index('--file')
        if idx + 1 < len(args):
            one_file = Path(args[idx + 1]).resolve()

    schemas = load_schemas()
    if not schemas:
        print(f"⚠️  Не найдено схем в {SCHEMAS_DIR}")
        return 1
    print(f"Загружено схем: {len(schemas)}")

    if one_file:
        files = [one_file]
    else:
        base = DOCS if not section else (Path(section) if Path(section).is_absolute() else ROOT / section)
        files = sorted(base.rglob('*.md'))

    total = 0
    valid = 0
    no_template = 0
    errors_per_file: dict[Path, list[str]] = {}

    for f in files:
        if '_schemas' in f.parts:
            continue
        # Сами шаблоны не валидируем — у них плейсхолдеры
        if 'templates' in f.parts and f.parent.name == 'templates':
            continue
        text = f.read_text(encoding='utf-8')
        fm, _ = extract_frontmatter(text)
        if not fm or 'template' not in fm:
            no_template += 1
            continue
        total += 1
        errs = validate_doc(f, schemas)
        if errs:
            errors_per_file[f] = errs
        else:
            valid += 1

    print(f"\nПроверено: {total} файлов с frontmatter (без frontmatter: {no_template})")
    print(f"Валидно: {valid}, с ошибками: {len(errors_per_file)}")

    for path, errs in sorted(errors_per_file.items()):
        rel = path.relative_to(ROOT) if ROOT in path.parents or ROOT == path.parent else path
        print(f"\n❌ {rel}")
        for e in errs:
            print(f"   — {e}")

    if report:
        report_path = DOCS / 'VALIDATION.md'
        lines = ['# Валидация шаблонов\n', f'_Обновлено: {date.today().isoformat()}_\n']
        lines.append(f'**Загружено схем:** {len(schemas)}\n')
        lines.append(f'**Документов с frontmatter:** {total}\n')
        lines.append(f'**Валидно:** {valid} | **С ошибками:** {len(errors_per_file)} | **Без шаблона:** {no_template}\n')

        if errors_per_file:
            lines.append('\n## Ошибки по файлам\n')
            for path, errs in sorted(errors_per_file.items()):
                rel = path.relative_to(ROOT) if ROOT in path.parents or ROOT == path.parent else path
                lines.append(f'\n### `{rel}`\n')
                for e in errs:
                    lines.append(f'- {e}')

        lines.append('\n## Шаблоны\n')
        for name in sorted(schemas):
            sch = schemas[name]
            lines.append(f'- **{name}** — {sch.get("description", "—")}')

        report_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
        print(f"\n→ Отчёт: {report_path.relative_to(ROOT)}")

    if strict and errors_per_file:
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
