"""
improve_self.py — метаскрипт: читает все скрипты, строит каталог, обогащает, генерирует.

Режимы:
  --audit             аудит всех скриптов: нет docstring, нет dry-run, риск
  --catalog           построить docs/scripts_catalog.json
  --enrich <файл>     обогатить конкретный скрипт (docstring, типизация, dry-run)
  --generate          сгенерировать новый скрипт по шаблону
  --cross-read        найти расхождения между скриптами и docs/CLAUDE.md
  --dry-run           показать что изменится, не применять
  --apply             применить изменения

Запуск:
  python scripts/improve_self.py --audit
  python scripts/improve_self.py --catalog
  python scripts/improve_self.py --enrich scripts/improve_health.py --dry-run
  python scripts/improve_self.py --cross-read
"""
import ast
import argparse
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

ROOT   = Path(__file__).parent.parent
DOCS   = ROOT / "docs"
SCRIPTS = ROOT / "scripts"
CATALOG_PATH = DOCS / "scripts_catalog.json"
GENERATED_DIR = SCRIPTS / "generated"

RISK_COLORS = {"green": "🟢", "yellow": "🟡", "red": "🔴"}


# ─────────────────────────────────────────────
# Структура данных одного скрипта
# ─────────────────────────────────────────────

@dataclass
class ScriptInfo:
    name: str
    doc: str = ""
    functions: list = field(default_factory=list)
    imports: list = field(default_factory=list)
    reads: list = field(default_factory=list)
    writes: list = field(default_factory=list)
    args: list = field(default_factory=list)
    has_dry_run: bool = False
    has_main_block: bool = False
    risk: str = "green"
    lines: int = 0
    group: str = ""


# ─────────────────────────────────────────────
# AST-анализ одного скрипта
# ─────────────────────────────────────────────

def analyze_script(path: Path) -> ScriptInfo:
    """Разбирает .py файл через AST и возвращает ScriptInfo."""
    info = ScriptInfo(name=path.name)
    try:
        source = path.read_text(encoding="utf-8")
    except Exception:
        return info

    info.lines = source.count("\n") + 1

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return info

    # Docstring модуля
    if (tree.body and isinstance(tree.body[0], ast.Expr)
            and isinstance(tree.body[0].value, ast.Constant)):
        info.doc = tree.body[0].value.value.strip().split("\n")[0]

    for node in ast.walk(tree):
        # Функции
        if isinstance(node, ast.FunctionDef):
            info.functions.append(node.name)

        # Импорты
        elif isinstance(node, ast.Import):
            for alias in node.names:
                info.imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                info.imports.append(node.module)

        # Вызовы: ищем open(), write_text(), read_text(), rglob()
        elif isinstance(node, ast.Call):
            func_name = ""
            if isinstance(node.func, ast.Attribute):
                func_name = node.func.attr
            elif isinstance(node.func, ast.Name):
                func_name = node.func.id

            if func_name in ("read_text", "read_bytes", "open"):
                info.reads.append(func_name)
            if func_name in ("write_text", "write_bytes", "write"):
                info.writes.append(func_name)

    # argparse: ищем add_argument
    for line in source.split("\n"):
        stripped = line.strip()
        if "add_argument" in stripped:
            m = re.search(r'add_argument\(["\']([^"\']+)["\']', stripped)
            if m:
                info.args.append(m.group(1))

    info.has_dry_run = "--dry-run" in info.args or "dry_run" in source
    info.has_main_block = 'if __name__ == "__main__"' in source

    # Риск: если пишет в docs/**/*.md — жёлтый/красный
    writes_docs = "write_text" in info.writes or "write_bytes" in info.writes
    reads_glob = "rglob" in source or "glob" in source

    if writes_docs and reads_glob:
        # Пишет в те же файлы что читает → красный
        if ".md" in source and "write_text" in source:
            info.risk = "red"
        else:
            info.risk = "yellow"
    elif writes_docs:
        info.risk = "yellow"
    else:
        info.risk = "green"

    # Группа из CLAUDE.md (простая эвристика)
    group_keywords = {
        "quality": ["metrics", "health", "spellcheck", "readability", "broken_links"],
        "deeptext": ["toc", "abstract", "paragraph", "vocabulary", "named_entity",
                     "timeline", "concept_graph", "keyword_index", "passage", "chunk"],
        "analytics": ["citation", "reading_time", "version_diff", "topic_model",
                      "cross_section", "digest"],
        "export": ["obsidian", "epub", "rss", "confluence", "export"],
        "meta": ["tech_radar", "onboarding", "risk_register", "component_matrix",
                 "kpi", "changelog", "index_master", "dependency_map"],
        "content": ["auto_linker", "gap_filler"],
        "textwork": ["reclassify", "merge_by_topic", "outline", "compare_docs",
                     "subtopic", "crosslink", "source_map", "duplicate"],
        "cicd": ["ci_config", "pre_commit", "dependabot", "github_issues"],
        "nlpplus": ["textrank", "heading_audit", "language_split", "question",
                    "passive_voice", "empty_sections", "faceted_search",
                    "similar_passages", "knowledge_map", "reading_list"],
    }
    stem = path.stem
    for group, keywords in group_keywords.items():
        if any(kw in stem for kw in keywords):
            info.group = group
            break

    return info


# ─────────────────────────────────────────────
# Режим: --audit
# ─────────────────────────────────────────────

def cmd_audit() -> None:
    """Аудит всех скриптов: проблемы, статистика, риски."""
    scripts = sorted(SCRIPTS.glob("improve_*.py"))
    infos = [analyze_script(p) for p in scripts]

    no_doc       = [i for i in infos if not i.doc]
    no_dry_run   = [i for i in infos if i.risk in ("yellow","red") and not i.has_dry_run]
    no_main      = [i for i in infos if not i.has_main_block]
    red_scripts  = [i for i in infos if i.risk == "red"]
    no_group     = [i for i in infos if not i.group]

    print(f"\n{'='*60}")
    print(f" АУДИТ СКРИПТОВ — {len(infos)} файлов")
    print(f"{'='*60}\n")

    print(f"🔴 Без docstring:                  {len(no_doc):>3}")
    print(f"🟡 Контентные без --dry-run:        {len(no_dry_run):>3}")
    print(f"⬜ Без if __name__ == '__main__':   {len(no_main):>3}")
    print(f"🔴 Деструктивные (risk=red):        {len(red_scripts):>3}")
    print(f"⬜ Без группы в run_all:            {len(no_group):>3}")

    print(f"\n{'─'*60}")
    print(" СКРИПТЫ БЕЗ DOCSTRING:")
    for i in no_doc[:20]:
        print(f"  {i.name}")
    if len(no_doc) > 20:
        print(f"  ... ещё {len(no_doc)-20}")

    print(f"\n{'─'*60}")
    print(" ДЕСТРУКТИВНЫЕ БЕЗ --DRY-RUN (опасно!):")
    for i in no_dry_run:
        print(f"  {RISK_COLORS[i.risk]} {i.name}")

    print(f"\n{'─'*60}")
    print(" РАСПРЕДЕЛЕНИЕ ПО РИСКУ:")
    for risk in ("green", "yellow", "red"):
        count = sum(1 for i in infos if i.risk == risk)
        bar = "█" * (count // 3)
        print(f"  {RISK_COLORS[risk]} {risk:8} {count:>3}  {bar}")

    print()


# ─────────────────────────────────────────────
# Режим: --catalog
# ─────────────────────────────────────────────

def cmd_catalog() -> None:
    """Строит docs/scripts_catalog.json из всех скриптов."""
    scripts = sorted(SCRIPTS.glob("improve_*.py"))
    catalog = {}

    for path in scripts:
        info = analyze_script(path)
        catalog[info.name] = {
            "doc":          info.doc,
            "functions":    info.functions[:10],
            "imports":      list(set(info.imports))[:10],
            "args":         info.args,
            "has_dry_run":  info.has_dry_run,
            "has_main":     info.has_main_block,
            "risk":         info.risk,
            "group":        info.group,
            "lines":        info.lines,
        }

    CATALOG_PATH.write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"✅ Каталог записан: {CATALOG_PATH.relative_to(ROOT)}")
    print(f"   Скриптов: {len(catalog)}")

    risk_counts = {"green": 0, "yellow": 0, "red": 0}
    for v in catalog.values():
        risk_counts[v["risk"]] += 1
    for risk, count in risk_counts.items():
        print(f"   {RISK_COLORS[risk]} {risk}: {count}")


# ─────────────────────────────────────────────
# Режим: --enrich
# ─────────────────────────────────────────────

SCRIPT_TEMPLATE_DOC = '''\
"""
{name} — {description}
Читает:  {reads}
Пишет:   {writes}
Запуск:  python scripts/{name} {args_example}
"""'''

def cmd_enrich(target: str, dry_run: bool) -> None:
    """Обогащает скрипт: добавляет docstring, dry-run, main-блок."""
    path = Path(target)
    if not path.exists():
        path = SCRIPTS / target
    if not path.exists():
        print(f"❌ Файл не найден: {target}")
        sys.exit(1)

    source = path.read_text(encoding="utf-8")
    info = analyze_script(path)
    changes = []
    new_source = source

    # 1. Добавить docstring если нет
    if not info.doc:
        description = path.stem.replace("improve_", "").replace("_", " ")
        reads_str  = "docs/**/*.md"
        writes_str = f"docs/{path.stem.upper().replace('IMPROVE_','')}.md"
        args_ex    = "--dry-run" if not info.has_dry_run else ""
        doc_block  = SCRIPT_TEMPLATE_DOC.format(
            name=path.name,
            description=description,
            reads=reads_str,
            writes=writes_str,
            args_example=args_ex,
        )
        new_source = doc_block + "\n" + new_source
        changes.append("+ добавлен docstring")

    # 2. Добавить if __name__ == "__main__" если нет
    if not info.has_main_block and "def main" in source:
        main_block = '\n\nif __name__ == "__main__":\n    main()\n'
        new_source = new_source.rstrip() + main_block
        changes.append('+ добавлен if __name__ == "__main__"')

    # 3. Добавить --dry-run предупреждение если скрипт пишет файлы
    if info.writes and not info.has_dry_run:
        changes.append("⚠  скрипт пишет файлы, но нет --dry-run (добавить вручную)")

    if not changes:
        print(f"✅ {path.name}: уже в хорошем состоянии, изменений нет")
        return

    print(f"\nФайл: {path.name}")
    print("Изменения:")
    for c in changes:
        print(f"  {c}")

    if dry_run:
        print("\n[dry-run] Изменения не применены. Добавьте --apply чтобы применить.")
        return

    path.write_text(new_source, encoding="utf-8")
    print(f"✅ Сохранено: {path}")


# ─────────────────────────────────────────────
# Режим: --generate
# ─────────────────────────────────────────────

PATTERNS = {
    "REPORT": """\
\"\"\"
{name}.py — {description}.
Читает:  docs/**/*.md
Пишет:   docs/{OUTPUT}.md
Запуск:  python scripts/{name}.py [--dry-run]
\"\"\"
import argparse
from pathlib import Path

ROOT   = Path(__file__).parent.parent
DOCS   = ROOT / "docs"
OUTPUT = DOCS / "{OUTPUT}.md"


def collect(docs: Path) -> list:
    \"\"\"Собрать данные из всех .md файлов.\"\"\"
    results = []
    for f in sorted(docs.rglob("*.md")):
        text = f.read_text(encoding="utf-8")
        # TODO: реализовать логику сбора
        results.append({{"file": str(f.relative_to(docs)), "text": text[:200]}})
    return results


def render(results: list) -> str:
    \"\"\"Отрендерить отчёт в Markdown.\"\"\"
    lines = ["# {description}\\n", f"_Файлов: {{len(results)}}_\\n"]
    for r in results:
        lines.append(f"- {{r['file']}}")
    return "\\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="{description}")
    parser.add_argument("--dry-run", action="store_true",
                        help="Показать план без записи")
    args = parser.parse_args()

    results = collect(DOCS)
    report  = render(results)

    if args.dry_run:
        print(f"[dry-run] {{len(results)}} файлов → {{OUTPUT.relative_to(ROOT)}}")
        print(report[:500])
        return

    OUTPUT.write_text(report, encoding="utf-8")
    print(f"✅ {{OUTPUT.relative_to(ROOT)}}")


if __name__ == "__main__":
    main()
""",
}

def cmd_generate(name: str, pattern: str, description: str, dry_run: bool) -> None:
    """Генерирует новый скрипт по шаблону."""
    if pattern not in PATTERNS:
        print(f"❌ Неизвестный паттерн: {pattern}")
        print(f"   Доступные: {', '.join(PATTERNS)}")
        sys.exit(1)

    script_name = name if name.startswith("improve_") else f"improve_{name}"
    output_name = script_name.replace("improve_", "").upper()
    content = PATTERNS[pattern].format(
        name=script_name,
        description=description,
        OUTPUT=output_name,
    )

    GENERATED_DIR.mkdir(exist_ok=True)
    out_path = GENERATED_DIR / f"{script_name}.py"

    header = f"# GENERATED by improve_self.py — проверить перед использованием\n"
    content = header + content

    print(f"\nПаттерн:  {pattern}")
    print(f"Файл:     scripts/generated/{script_name}.py")
    print(f"Описание: {description}")
    print(f"\n{'─'*50}")
    print(content[:600])
    print(f"{'─'*50}")

    if dry_run:
        print("\n[dry-run] Файл не создан. Добавьте --apply.")
        return

    out_path.write_text(content, encoding="utf-8")
    print(f"\n✅ Создан: {out_path.relative_to(ROOT)}")
    print(f"   Следующий шаг: проверить, потом:")
    print(f"   mv {out_path} {SCRIPTS / out_path.name}")


# ─────────────────────────────────────────────
# Режим: --cross-read
# ─────────────────────────────────────────────

def cmd_cross_read() -> None:
    """Находит расхождения между скриптами и документацией."""
    print(f"\n{'='*60}")
    print(" ПЕРЕКРЁСТНОЕ ЧТЕНИЕ: скрипты ↔ документация")
    print(f"{'='*60}\n")

    # Скрипты которые существуют
    existing = {p.name for p in SCRIPTS.glob("improve_*.py")}

    # Скрипты упомянутые в CLAUDE.md
    claude_md = ROOT / "CLAUDE.md"
    mentioned_in_claude = set()
    if claude_md.exists():
        text = claude_md.read_text(encoding="utf-8")
        mentioned_in_claude = set(re.findall(r'improve_\w+\.py', text))

    # Скрипты упомянутые в docs/
    mentioned_in_docs = set()
    for md in DOCS.rglob("*.md"):
        try:
            text = md.read_text(encoding="utf-8")
            found = re.findall(r'improve_\w+\.py', text)
            mentioned_in_docs.update(found)
        except Exception:
            pass

    # Анализ
    in_claude_not_exist = mentioned_in_claude - existing
    in_docs_not_exist   = mentioned_in_docs - existing
    exist_not_in_claude = existing - mentioned_in_claude
    exist_not_in_docs   = existing - mentioned_in_docs

    print(f"📋 Упомянуты в CLAUDE.md, но файл не существует ({len(in_claude_not_exist)}):")
    for s in sorted(in_claude_not_exist)[:10]:
        print(f"   ❌ {s}")

    print(f"\n📄 Упомянуты в docs/, но файл не существует ({len(in_docs_not_exist)}):")
    for s in sorted(in_docs_not_exist)[:10]:
        print(f"   ❌ {s}")

    print(f"\n⬜ Существуют, но не упомянуты в CLAUDE.md ({len(exist_not_in_claude)}):")
    for s in sorted(exist_not_in_claude)[:10]:
        print(f"   ⚠  {s}")

    print(f"\n{'─'*60}")
    print(f" Итог: {len(existing)} скриптов, "
          f"{len(in_claude_not_exist)} фантомных в CLAUDE.md, "
          f"{len(exist_not_in_claude)} незадокументированных")
    print()


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="improve_self.py — метаскрипт: аудит, каталог, обогащение, генерация"
    )
    parser.add_argument("--audit",      action="store_true", help="Аудит всех скриптов")
    parser.add_argument("--catalog",    action="store_true", help="Построить scripts_catalog.json")
    parser.add_argument("--enrich",     metavar="ФАЙЛ",      help="Обогатить конкретный скрипт")
    parser.add_argument("--cross-read", action="store_true", help="Сравнить скрипты и документацию")
    parser.add_argument("--generate",   action="store_true", help="Сгенерировать новый скрипт")
    parser.add_argument("--name",       metavar="ИМЯ",       help="Имя нового скрипта (для --generate)")
    parser.add_argument("--pattern",    default="REPORT",    help="Паттерн: REPORT (по умолчанию)")
    parser.add_argument("--description",metavar="ТЕКСТ",     help="Описание нового скрипта")
    parser.add_argument("--dry-run",    action="store_true", help="Показать план без изменений")
    parser.add_argument("--apply",      action="store_true", help="Применить изменения")

    args = parser.parse_args()

    # Если ничего не указано — показать аудит
    if not any([args.audit, args.catalog, args.enrich,
                getattr(args, "cross_read", False), args.generate]):
        args.audit = True

    dry_run = args.dry_run or not args.apply

    if args.audit:
        cmd_audit()

    if args.catalog:
        cmd_catalog()

    if args.enrich:
        cmd_enrich(args.enrich, dry_run=dry_run)

    if getattr(args, "cross_read", False):
        cmd_cross_read()

    if args.generate:
        if not args.name:
            print("❌ Для --generate нужно указать --name")
            sys.exit(1)
        desc = args.description or args.name.replace("_", " ")
        cmd_generate(args.name, args.pattern, desc, dry_run=dry_run)


if __name__ == "__main__":
    main()
