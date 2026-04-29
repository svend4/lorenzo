"""
improve_template_init.py — инициализация нового документа из шаблона.

Создаёт файл по слаг-пути, подставляет переменные frontmatter и плейсхолдеры
в теле, делает базовую валидацию через improve_validate_templates.

Использование:
    python scripts/improve_template_init.py --type contact-outreach \\
        --slug docs/contacts/новый-автор --vars author="Иван" platform=GitHub

    python scripts/improve_template_init.py --type rfc \\
        --slug docs/svyazi-2-0/rfcs/new-rfc.md \\
        --vars title="My RFC" status=proposed

    python scripts/improve_template_init.py --list           # список шаблонов
    python scripts/improve_template_init.py --type rfc --show  # показать сырой шаблон
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TEMPLATES = DOCS / "templates"
SCHEMAS = TEMPLATES / "_schemas"

FRONTMATTER_RE = re.compile(r'\A---\s*\n(.*?)\n---\s*\n', re.DOTALL)


def list_templates() -> list[str]:
    return sorted(p.stem for p in TEMPLATES.glob('*.md') if p.name != 'README.md')


def load_template(name: str) -> str:
    path = TEMPLATES / f'{name}.md'
    if not path.exists():
        print(f"❌ Шаблон не найден: {path}")
        print(f"   Доступные: {', '.join(list_templates())}")
        sys.exit(1)
    return path.read_text(encoding='utf-8')


def parse_kv(items: list[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for item in items:
        if '=' not in item:
            continue
        k, v = item.split('=', 1)
        result[k.strip()] = v.strip()
    return result


def apply_vars(content: str, vars_dict: dict[str, str]) -> str:
    """Заменяет плейсхолдеры [имя] и YAML-значения в frontmatter."""
    today = date.today().isoformat()
    if 'created' not in vars_dict and 'date' not in vars_dict:
        vars_dict.setdefault('_today', today)

    fm_match = FRONTMATTER_RE.match(content)
    if fm_match:
        fm_text = fm_match.group(1)
        new_fm = fm_text
        for k, v in vars_dict.items():
            if k.startswith('_'):
                continue
            new_fm = re.sub(
                rf'^({re.escape(k)})\s*:\s*.+$',
                lambda m, val=v: f'{m.group(1)}: {_yaml_value(val)}',
                new_fm, count=1, flags=re.MULTILINE
            )
        # Подставить created/date на сегодня если не задан
        new_fm = re.sub(r'^created:\s*[\d-]+$', f'created: {today}', new_fm, flags=re.MULTILINE)
        new_fm = re.sub(r'^date:\s*[\d-]+$', f'date: {today}', new_fm, flags=re.MULTILINE)
        content = content[:fm_match.start(1)] + new_fm + content[fm_match.end(1):]

    # Body: подставить плейсхолдеры [name] из vars_dict
    for k, v in vars_dict.items():
        if k.startswith('_'):
            continue
        content = content.replace(f'[{k}]', v)

    # Заменить дату «_Создано: YYYY-MM-DD_»
    content = re.sub(r'_Создано:\s+\d{4}-\d{2}-\d{2}_', f'_Создано: {today}_', content)
    content = re.sub(r'_Дата:\s+\d{4}-\d{2}-\d{2}_', f'_Дата: {today}_', content)

    return content


def _yaml_value(v: str) -> str:
    """Сериализация значения для YAML-frontmatter."""
    if v in ('true', 'false', 'null'):
        return v
    if re.fullmatch(r'-?\d+', v) or re.fullmatch(r'-?\d+\.\d+', v):
        return v
    if re.fullmatch(r'\d{4}-\d{2}-\d{2}', v):
        return v
    if v.startswith('[') and v.endswith(']'):
        return v
    return f'"{v}"'


def main():
    args = sys.argv[1:]
    if '--list' in args:
        print('Доступные шаблоны:')
        for t in list_templates():
            schema_path = SCHEMAS / f'{t}.json'
            desc = ''
            if schema_path.exists():
                try:
                    desc = json.loads(schema_path.read_text(encoding='utf-8')).get('description', '')
                except Exception:
                    pass
            print(f'  {t:25s} {desc}')
        return 0

    if '--type' not in args:
        print(__doc__)
        return 1
    t_idx = args.index('--type')
    template_name = args[t_idx + 1]

    if '--show' in args:
        print(load_template(template_name))
        return 0

    if '--slug' not in args:
        print('❌ Требуется --slug путь/файл.md')
        return 1
    s_idx = args.index('--slug')
    slug_path = args[s_idx + 1]
    if not slug_path.endswith('.md'):
        slug_path += '.md'

    vars_list: list[str] = []
    if '--vars' in args:
        v_idx = args.index('--vars')
        for a in args[v_idx + 1:]:
            if a.startswith('--'):
                break
            vars_list.append(a)

    vars_dict = parse_kv(vars_list)
    content = load_template(template_name)
    content = apply_vars(content, vars_dict)

    out_path = Path(slug_path)
    if not out_path.is_absolute():
        out_path = ROOT / out_path

    if out_path.exists():
        print(f"❌ Файл уже существует: {out_path}")
        print(f"   Используйте --force чтобы перезаписать.")
        if '--force' not in args:
            return 1

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding='utf-8')
    rel = out_path.relative_to(ROOT) if ROOT in out_path.parents or ROOT == out_path.parent else out_path
    print(f"✅ Создан: {rel}")

    # Проверка валидности
    try:
        from improve_validate_templates import load_schemas, validate_doc  # type: ignore
        schemas = load_schemas()
        errs = validate_doc(out_path, schemas)
        if errs:
            print(f"\n⚠️  Документ создан, но есть ошибки валидации:")
            for e in errs:
                print(f"   — {e}")
            print(f"\n   Заполните недостающие поля и проверьте:")
            print(f"   python scripts/improve_validate_templates.py --file {rel}")
        else:
            print(f"   ✓ Прошёл валидацию по схеме {template_name}")
    except ImportError:
        pass

    return 0


if __name__ == '__main__':
    sys.path.insert(0, str(Path(__file__).parent))
    sys.exit(main())
