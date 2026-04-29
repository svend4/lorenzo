"""CLI точка входа: docstoolkit ..."""
import argparse
import json
import sys
from datetime import date
from pathlib import Path

from docstoolkit.config import load_config
from docstoolkit.frontmatter import extract_frontmatter


def cmd_init(args):
    """Создать docstoolkit.toml в текущей папке."""
    config_path = Path("docstoolkit.toml")
    if config_path.exists() and not args.force:
        print(f"❌ {config_path} уже существует. --force для перезаписи.")
        return 1
    config_path.write_text(EXAMPLE_CONFIG, encoding="utf-8")
    print(f"✅ Создан {config_path}")
    return 0


def cmd_doc_new(args):
    """Создать документ из шаблона."""
    cfg = load_config()
    template_path = cfg.templates_dir / f"{args.type}.md"
    if not template_path.exists():
        print(f"❌ Шаблон '{args.type}' не найден в {cfg.templates_dir}")
        return 1

    content = template_path.read_text(encoding="utf-8")

    # Применить переменные
    vars_dict: dict[str, str] = {}
    for kv in args.vars or []:
        if "=" in kv:
            k, v = kv.split("=", 1)
            vars_dict[k.strip()] = v.strip()

    # Заменить frontmatter поля
    import re
    today = date.today().isoformat()
    fm_match = re.match(r'\A---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if fm_match:
        fm_text = fm_match.group(1)
        for k, v in vars_dict.items():
            yaml_v = f'"{v}"' if not v.lstrip("-").isdigit() else v
            fm_text = re.sub(
                rf'^({re.escape(k)})\s*:\s*.+$',
                lambda m, val=yaml_v: f"{m.group(1)}: {val}",
                fm_text, count=1, flags=re.MULTILINE
            )
        fm_text = re.sub(r'^created:\s*[\d-]+$', f'created: {today}', fm_text, flags=re.MULTILINE)
        fm_text = re.sub(r'^date:\s*[\d-]+$', f'date: {today}', fm_text, flags=re.MULTILINE)
        content = content[:fm_match.start(1)] + fm_text + content[fm_match.end(1):]

    # Body placeholders
    for k, v in vars_dict.items():
        content = content.replace(f"[{k}]", v)

    out_path = Path(args.slug)
    if not out_path.suffix:
        out_path = out_path.with_suffix(".md")
    if out_path.exists() and not args.force:
        print(f"❌ {out_path} существует. --force для перезаписи.")
        return 1

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding="utf-8")
    print(f"✅ Создан {out_path}")
    return 0


def cmd_doc_validate(args):
    """Валидация документов по JSON-схемам."""
    cfg = load_config()
    schemas_dir = cfg.schemas_dir
    if not schemas_dir.exists():
        print(f"❌ Нет схем в {schemas_dir}")
        return 1

    schemas: dict[str, dict] = {}
    for sp in schemas_dir.glob("*.json"):
        try:
            schemas[sp.stem] = json.loads(sp.read_text(encoding="utf-8"))
        except Exception:
            continue

    base = Path(args.section) if args.section else cfg.docs_dir
    if not base.is_absolute():
        base = cfg.root / base

    files = sorted(base.rglob("*.md"))
    skip_dirs = set(cfg.validation.get("skip_dirs", []))

    valid = 0
    errors_count = 0
    for f in files:
        if any(d in f.parts for d in skip_dirs):
            continue
        text = f.read_text(encoding="utf-8")
        fm, _ = extract_frontmatter(text)
        if not fm or "template" not in fm:
            continue
        template = fm["template"]
        if template not in schemas:
            print(f"⚠️  {f.relative_to(cfg.root)}: схема '{template}' не найдена")
            continue
        # Простая проверка: required-поля
        schema = schemas[template]
        errs: list[str] = []
        for req in schema.get("required", []):
            if req not in fm:
                errs.append(f"missing required: {req}")
        if errs:
            errors_count += 1
            print(f"❌ {f.relative_to(cfg.root)}")
            for e in errs:
                print(f"   — {e}")
        else:
            valid += 1

    print(f"\nВалидно: {valid}, с ошибками: {errors_count}")
    return 1 if errors_count and cfg.validation.get("strict") else 0


def cmd_doc_list_templates(args):
    """Список доступных шаблонов."""
    cfg = load_config()
    if not cfg.templates_dir.exists():
        print(f"Templates dir не найден: {cfg.templates_dir}")
        return 1
    items = []
    for p in sorted(cfg.templates_dir.glob("*.md")):
        if p.name == "README.md":
            continue
        schema = cfg.schemas_dir / f"{p.stem}.json"
        desc = ""
        if schema.exists():
            try:
                desc = json.loads(schema.read_text(encoding="utf-8")).get("description", "")
            except Exception:
                pass
        items.append((p.stem, desc))
    print(f"Доступных шаблонов: {len(items)}")
    for name, desc in items:
        print(f"  {name:25s} {desc[:60]}")
    return 0


EXAMPLE_CONFIG = """# docstoolkit configuration

[paths]
docs = "docs"
templates = "docs/templates"
schemas = "docs/templates/_schemas"
tasks = "tasks"
skills = ".claude/skills"

[validation]
strict = false
skip_dirs = ["templates", "_schemas", "node_modules", ".git"]

[language]
primary = "en"

[sections]
# Секции монорепо: имя папки → читаемое название
# "01-svyazi" = "Svyazi 2.0"
"""


def main():
    parser = argparse.ArgumentParser(prog="docstoolkit",
                                     description="Universal markdown documentation toolkit")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init", help="Создать docstoolkit.toml")
    p_init.add_argument("--force", action="store_true")
    p_init.set_defaults(func=cmd_init)

    p_doc = sub.add_parser("doc", help="Документы")
    p_doc_sub = p_doc.add_subparsers(dest="doc_cmd", required=True)

    p_new = p_doc_sub.add_parser("new", help="Создать из шаблона")
    p_new.add_argument("--type", required=True)
    p_new.add_argument("--slug", required=True)
    p_new.add_argument("--vars", nargs="*", default=[])
    p_new.add_argument("--force", action="store_true")
    p_new.set_defaults(func=cmd_doc_new)

    p_val = p_doc_sub.add_parser("validate", help="Валидация документов")
    p_val.add_argument("--section", default="")
    p_val.set_defaults(func=cmd_doc_validate)

    p_list = p_doc_sub.add_parser("list-templates", help="Список шаблонов")
    p_list.set_defaults(func=cmd_doc_list_templates)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
