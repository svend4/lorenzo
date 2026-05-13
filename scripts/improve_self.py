"""
improve_self.py — метаскрипт: читает все скрипты, строит каталог, обогащает, генерирует.

Режимы:
  --audit             аудит всех скриптов: нет docstring, нет dry-run, риск
  --catalog           построить docs/scripts_catalog.json
  --enrich <файл>     обогатить конкретный скрипт (docstring, типизация, dry-run)
  --enrich --batch    пакетное обогащение всех скриптов
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
# Вспомогательные функции
# ─────────────────────────────────────────────

def _is_inplace_writer(source: str) -> bool:
    """True если скрипт модифицирует файлы которые сам и читает через glob.

    Отличие от «безопасных» скриптов: вызывает write_text() внутри тела
    for-цикла по rglob/glob, а не снаружи (на отдельном output-файле).

    Пример RED:    for f in DOCS.rglob("*.md"):
                       ...
                       f.write_text(new_text)      ← внутри цикла

    Пример YELLOW: for f in DOCS.rglob("*.md"):
                       ...                         ← только чтение
                   out = DOCS / "REPORT.md"
                   out.write_text(report)           ← снаружи цикла
    """
    lines = source.split("\n")
    # Stack of (for_indent,) — indent of the "for" keyword line
    for_stack: list[int] = []

    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        current_indent = len(line) - len(line.lstrip())

        # Убрать for-циклы, которые уже закончились
        for_stack = [ind for ind in for_stack if current_indent > ind]

        # Обнаружить for-цикл по rglob/glob
        if re.match(r"for\s+\w+\s+in\s+.+(?:rglob|glob)\s*\(", stripped):
            for_stack.append(current_indent)
            continue

        # Если мы внутри хотя бы одного glob-цикла и встречаем write_text → RED
        if for_stack and re.search(r"\.(write_text|write_bytes)\s*\(", stripped):
            return True

    # Secondary signal: scripts with SKIP/ALREADY_HAS marker constants + write_text
    # are in-place writers even if write_text is delegated to a helper function.
    # Must appear as a top-level assignment (not inside a string/regex).
    marker_pattern = re.search(
        r'^(?:SKIP_MARKERS|ALREADY_HAS\w*|MARKER)\s*=\s*["\'\(]',
        source, re.MULTILINE
    )
    if marker_pattern and re.search(r'\.write_text\s*\(', source):
        return True

    return False


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

    # Риск: различаем три уровня
    # 🟢 GREEN:  только чтение / stdout
    # 🟡 YELLOW: пишет в один выделенный output-файл (HEALTH.md, METRICS.md и т.д.)
    # 🔴 RED:    модифицирует входные файлы in-place (write_text на loop-переменной)
    writes_docs = "write_text" in info.writes or "write_bytes" in info.writes

    if not writes_docs:
        info.risk = "green"
    elif _is_inplace_writer(source):
        info.risk = "red"
    else:
        info.risk = "yellow"

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
# Режим: --enrich --batch
# ─────────────────────────────────────────────

def cmd_enrich_batch(dry_run: bool) -> None:
    """Пакетное обогащение всех скриптов: docstring + main-блок."""
    scripts = sorted(SCRIPTS.glob("improve_*.py"))
    infos   = [(p, analyze_script(p)) for p in scripts]

    # Отбираем только те, которым нужны изменения
    needs_work = []
    for path, info in infos:
        missing = []
        if not info.doc:
            missing.append("docstring")
        if not info.has_main_block and "def main" in path.read_text(encoding="utf-8"):
            missing.append("main-блок")
        if info.writes and not info.has_dry_run:
            missing.append("⚠ нет --dry-run")
        if missing:
            needs_work.append((path, info, missing))

    print(f"\n{'='*60}")
    print(f" ПАКЕТНОЕ ОБОГАЩЕНИЕ: {len(needs_work)} / {len(scripts)} скриптов")
    print(f"{'='*60}\n")

    if not needs_work:
        print("✅ Все скрипты уже в хорошем состоянии.")
        return

    # Статистика
    need_doc  = sum(1 for _, _, m in needs_work if "docstring" in m)
    need_main = sum(1 for _, _, m in needs_work if "main-блок" in m)
    need_dry  = sum(1 for _, _, m in needs_work if "⚠ нет --dry-run" in m)
    print(f"  Нужен docstring:          {need_doc:>3}")
    print(f"  Нужен main-блок:          {need_main:>3}")
    print(f"  Нет --dry-run (инфо):     {need_dry:>3}")
    print(f"  Всего к изменению:        {need_doc + need_main:>3}  (dry-run — только информация)\n")

    applied   = 0
    skipped   = 0

    for path, info, missing in needs_work:
        source   = path.read_text(encoding="utf-8")
        changes  = []
        new_src  = source

        # 1. Добавить docstring
        if "docstring" in missing:
            description = path.stem.replace("improve_", "").replace("_", " ")
            reads_str   = "docs/**/*.md"
            writes_str  = f"docs/{path.stem.upper().replace('IMPROVE_','')}.md"
            args_ex     = "--dry-run" if not info.has_dry_run else ""
            doc_block   = SCRIPT_TEMPLATE_DOC.format(
                name=path.name,
                description=description,
                reads=reads_str,
                writes=writes_str,
                args_example=args_ex,
            )
            new_src = doc_block + "\n" + new_src
            changes.append("+ docstring")

        # 2. Добавить main-блок
        if "main-блок" in missing:
            main_block = '\n\nif __name__ == "__main__":\n    main()\n'
            new_src = new_src.rstrip() + main_block
            changes.append('+ if __name__ == "__main__"')

        # 3. Только инфо-предупреждение о dry-run (не меняем код)
        if "⚠ нет --dry-run" in missing:
            changes.append("⚠  нет --dry-run (добавить вручную)")

        real_changes = [c for c in changes if c.startswith("+")]

        label = path.name
        changes_str = ", ".join(changes)

        if dry_run:
            print(f"  {'✏' if real_changes else 'ℹ'} {label}")
            print(f"      {changes_str}")
        else:
            if real_changes:
                path.write_text(new_src, encoding="utf-8")
                print(f"  ✅ {label}: {', '.join(real_changes)}")
                applied += 1
            else:
                skipped += 1

    if dry_run:
        print(f"\n[dry-run] {need_doc + need_main} изменений не применено.")
        print("[dry-run] Добавьте --apply чтобы применить.")
    else:
        print(f"\nИтог: изменено {applied}, пропущено {skipped} (только ⚠-предупреждения).")


# ─────────────────────────────────────────────
# Режим: --generate
# ─────────────────────────────────────────────

PATTERNS = {
    # ── Отчёт: читает docs/, пишет один выходной файл ─────────────
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

    # ── Обогащение: читает docs/, модифицирует файлы in-place ──────
    "ENRICHER": """\
\"\"\"
{name}.py — {description}.
Читает и модифицирует: docs/**/*.md (добавляет блок в конец файла)
Маркер: <!-- {OUTPUT_LOWER} --> (идемпотентность)
Запуск:  python scripts/{name}.py [--dry-run] [--section РАЗДЕЛ]
\"\"\"
import argparse
from pathlib import Path

ROOT   = Path(__file__).parent.parent
DOCS   = ROOT / "docs"
MARKER = "<!-- {OUTPUT_LOWER} -->"
SKIP   = {{"README.md", "SUMMARIES.md"}}


def enrich(path: Path, dry_run: bool = False) -> bool:
    \"\"\"Добавить блок в конец файла. Возвращает True если изменён.\"\"\"
    text = path.read_text(encoding="utf-8")
    if MARKER in text or len(text) < 100:
        return False

    # TODO: реализовать логику обогащения
    block = f"\\n{{MARKER}}\\n\\n---\\n\\n**{description}:** _TODO_\\n"

    if dry_run:
        return True
    path.write_text(text + block, encoding="utf-8")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="{description}")
    parser.add_argument("--dry-run",  action="store_true",
                        help="Показать план без изменений")
    parser.add_argument("--section",  metavar="РАЗДЕЛ",
                        help="Обработать только один раздел docs/")
    args = parser.parse_args()

    root = DOCS / args.section if args.section else DOCS
    updated = skipped = 0
    for f in sorted(root.rglob("*.md")):
        if f.name in SKIP:
            continue
        if enrich(f, dry_run=args.dry_run):
            if args.dry_run:
                print(f"  [dry-run] {{f.relative_to(ROOT)}}")
            updated += 1
        else:
            skipped += 1

    label = "[dry-run] " if args.dry_run else ""
    print(f"{{label}}обновлено: {{updated}}, пропущено: {{skipped}}")


if __name__ == "__main__":
    main()
""",

    # ── Анализатор: читает docs/, пишет JSON + MD ──────────────────
    "ANALYZER": """\
\"\"\"
{name}.py — {description}.
Читает:  docs/**/*.md
Пишет:   docs/{OUTPUT}.md  и  docs/{OUTPUT}.json
Запуск:  python scripts/{name}.py [--dry-run] [--section РАЗДЕЛ] [--top N]
\"\"\"
import argparse
import json
import re
from pathlib import Path

ROOT   = Path(__file__).parent.parent
DOCS   = ROOT / "docs"
OUT_MD = DOCS / "{OUTPUT}.md"
OUT_JS = DOCS / "{OUTPUT}.json"
SKIP   = {{"README.md", "SUMMARIES.md", "{OUTPUT}.md"}}


def analyze_file(path: Path) -> dict | None:
    \"\"\"Анализировать один файл. None если файл не подходит.\"\"\"
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return None
    if len(text) < 50:
        return None
    # TODO: реализовать анализ
    return {{
        "file":  str(path.relative_to(ROOT)),
        "lines": text.count("\\n") + 1,
        "words": len(text.split()),
    }}


def render_md(results: list[dict]) -> str:
    lines = [
        "# {description}\\n",
        f"_Файлов: {{len(results)}}_\\n",
        "| Файл | Строк | Слов |",
        "|------|-------|------|",
    ]
    for r in results[:50]:
        short = "/".join(r["file"].split("/")[-2:])
        lines.append(f"| {{short}} | {{r['lines']}} | {{r['words']}} |")
    return "\\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="{description}")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--section", metavar="РАЗДЕЛ")
    parser.add_argument("--top",     type=int, default=50)
    args = parser.parse_args()

    root = DOCS / args.section if args.section else DOCS
    results = []
    for f in sorted(root.rglob("*.md")):
        if f.name in SKIP:
            continue
        r = analyze_file(f)
        if r:
            results.append(r)

    results = results[:args.top]
    md = render_md(results)
    print(f"Проанализировано: {{len(results)}} файлов")
    print(md[:300])

    if args.dry_run:
        print(f"\\n[dry-run] {{OUT_MD.name}} и {{OUT_JS.name}} не записаны.")
        return

    OUT_MD.write_text(md, encoding="utf-8")
    OUT_JS.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ {{OUT_MD.relative_to(ROOT)}}  {{OUT_JS.relative_to(ROOT)}}")


if __name__ == "__main__":
    main()
""",

    # ── Поисковый инструмент: интерактивный CLI-поиск ──────────────
    "SEARCHER": """\
\"\"\"
{name}.py — {description}.
Читает:  docs/**/*.md (live-индекс при запуске)
Режимы:  интерактивный REPL или разовый --query
Запуск:  python scripts/{name}.py
         python scripts/{name}.py --query "агент память" --top 10
\"\"\"
import argparse
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
STOP = {{"и","в","не","на","с","по","к","из","для","это","как","но",
         "the","a","an","is","of","in","to","for","with","by","and"}}


def tokenize(text: str) -> list[str]:
    return [t for t in re.findall(r'[а-яёa-z]{{3,}}', text.lower()) if t not in STOP]


def build_index() -> list[dict]:
    \"\"\"Строит простой инвертированный индекс.\"\"\"
    print("  Индексирую...", end="", flush=True)
    docs = []
    for f in sorted(DOCS.rglob("*.md")):
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue
        docs.append({{"file": str(f.relative_to(ROOT)), "tokens": tokenize(text)}})
    print(f" {{len(docs)}} файлов")
    return docs


def search(query: str, docs: list[dict], top: int = 10) -> list[dict]:
    tokens = tokenize(query)
    scored = []
    for doc in docs:
        score = sum(doc["tokens"].count(t) for t in tokens)
        if score > 0:
            scored.append({{"score": score, "file": doc["file"]}})
    return sorted(scored, key=lambda x: -x["score"])[:top]


def main() -> None:
    parser = argparse.ArgumentParser(description="{description}")
    parser.add_argument("--query", "-q", metavar="ЗАПРОС")
    parser.add_argument("--top",         type=int, default=10)
    args = parser.parse_args()

    docs = build_index()

    if args.query:
        results = search(args.query, docs, top=args.top)
        print(f"Результаты «{{args.query}}»: {{len(results)}}")
        for r in results:
            print(f"  [{{r['score']:4d}}] {{r['file']}}")
        return

    # REPL
    print("\\nПоиск (Ctrl+C для выхода):")
    while True:
        try:
            q = input("  > ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not q:
            continue
        results = search(q, docs, top=args.top)
        for i, r in enumerate(results, 1):
            print(f"  {{i:2}}. [{{r['score']:3d}}] {{r['file']}}")
        print()


if __name__ == "__main__":
    main()
""",

    # ── Экспортёр: docs/ → внешний формат ─────────────────────────
    "EXPORTER": """\
\"\"\"
{name}.py — {description}.
Читает:  docs/**/*.md
Пишет:   docs/{OUTPUT_LOWER}/ (каталог с преобразованными файлами)
Запуск:  python scripts/{name}.py [--dry-run] [--section РАЗДЕЛ]
\"\"\"
import argparse
from pathlib import Path

ROOT    = Path(__file__).parent.parent
DOCS    = ROOT / "docs"
OUT_DIR = DOCS / "{OUTPUT_LOWER}"
SKIP    = {{"README.md", "SUMMARIES.md"}}


def convert(text: str, path: Path) -> str:
    \"\"\"Конвертировать Markdown в целевой формат.\"\"\"
    # TODO: реализовать конвертацию
    return text


def export_file(src: Path, dry_run: bool = False) -> Path | None:
    \"\"\"Экспортировать один файл. Возвращает путь к результату.\"\"\"
    try:
        text = src.read_text(encoding="utf-8")
    except Exception:
        return None
    converted = convert(text, src)
    rel = src.relative_to(DOCS)
    dst = OUT_DIR / rel.with_suffix(".txt")  # TODO: поменять расширение
    if dry_run:
        return dst
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(converted, encoding="utf-8")
    return dst


def main() -> None:
    parser = argparse.ArgumentParser(description="{description}")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--section", metavar="РАЗДЕЛ")
    args = parser.parse_args()

    root = DOCS / args.section if args.section else DOCS
    done = skipped = 0
    for f in sorted(root.rglob("*.md")):
        if f.name in SKIP or f.is_relative_to(OUT_DIR):
            skipped += 1
            continue
        dst = export_file(f, dry_run=args.dry_run)
        if dst:
            if args.dry_run:
                print(f"  [dry-run] {{f.relative_to(DOCS)}} → {{dst.relative_to(DOCS)}}")
            done += 1

    label = "[dry-run] " if args.dry_run else ""
    print(f"{{label}}экспортировано: {{done}}, пропущено: {{skipped}}")
    if not args.dry_run:
        print(f"✅ {{OUT_DIR.relative_to(ROOT)}}/")


if __name__ == "__main__":
    main()
""",
}

PATTERN_DESCRIPTIONS = {
    "REPORT":   "Читает docs/, пишет один выходной .md файл (отчёт/дашборд)",
    "ENRICHER": "Читает и модифицирует docs/ in-place, добавляет блок с маркером",
    "ANALYZER": "Анализирует docs/, пишет .md + .json (статистика/метрики)",
    "SEARCHER": "Интерактивный REPL-поиск по docs/ с live-индексом",
    "EXPORTER": "Экспортирует docs/ во внешний формат (каталог с файлами)",
}


def cmd_generate(name: str, pattern: str, description: str, dry_run: bool) -> None:
    """Генерирует новый скрипт по шаблону."""
    if pattern == "list":
        print("Доступные паттерны:")
        for p, desc in PATTERN_DESCRIPTIONS.items():
            print(f"  {p:<12} — {desc}")
        return
    if pattern not in PATTERNS:
        print(f"❌ Неизвестный паттерн: {pattern}\n")
        print("Доступные паттерны:")
        for p, desc in PATTERN_DESCRIPTIONS.items():
            print(f"  {p:<12} — {desc}")
        sys.exit(1)

    script_name = name if name.startswith("improve_") else f"improve_{name}"
    output_name = script_name.replace("improve_", "").upper()
    content = PATTERNS[pattern].format(
        name=script_name,
        description=description,
        OUTPUT=output_name,
        OUTPUT_LOWER=output_name.lower(),
    )

    GENERATED_DIR.mkdir(exist_ok=True)
    out_path = GENERATED_DIR / f"{script_name}.py"

    header = f"# GENERATED by improve_self.py  pattern={pattern} — проверить перед использованием\n"
    content = header + content

    print(f"\nПаттерн:  {pattern}  ({PATTERN_DESCRIPTIONS[pattern]})")
    print(f"Файл:     scripts/generated/{script_name}.py")
    print(f"Описание: {description}")
    print(f"\n{'─'*55}")
    print(content[:700])
    print(f"{'─'*55}")

    if dry_run:
        print("\n[dry-run] Файл не создан. Добавьте --apply.")
        return

    out_path.write_text(content, encoding="utf-8")
    print(f"\n✅ Создан: {out_path.relative_to(ROOT)}")
    print(f"   Проверить синтаксис: python -m py_compile {out_path}")
    print(f"   Переместить:         mv {out_path} {SCRIPTS / out_path.name}")


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
    parser.add_argument("--enrich",     metavar="ФАЙЛ",      help="Обогатить конкретный скрипт (или --batch)")
    parser.add_argument("--batch",      action="store_true", help="Пакетное обогащение всех скриптов (с --enrich)")
    parser.add_argument("--cross-read", action="store_true", help="Сравнить скрипты и документацию")
    parser.add_argument("--generate",   action="store_true", help="Сгенерировать новый скрипт")
    parser.add_argument("--name",       metavar="ИМЯ",       help="Имя нового скрипта (для --generate)")
    parser.add_argument("--pattern",    default="REPORT",
                        help="Паттерн: REPORT|ENRICHER|ANALYZER|SEARCHER|EXPORTER|list")
    parser.add_argument("--description",metavar="ТЕКСТ",     help="Описание нового скрипта")
    parser.add_argument("--dry-run",    action="store_true", help="Показать план без изменений")
    parser.add_argument("--apply",      action="store_true", help="Применить изменения")

    args = parser.parse_args()

    # Если ничего не указано — показать аудит
    if not any([args.audit, args.catalog, args.enrich, args.batch,
                getattr(args, "cross_read", False), args.generate]):
        args.audit = True

    dry_run = args.dry_run or not args.apply

    if args.audit:
        cmd_audit()

    if args.catalog:
        cmd_catalog()

    if args.batch:
        cmd_enrich_batch(dry_run=dry_run)
    elif args.enrich:
        cmd_enrich(args.enrich, dry_run=dry_run)

    if getattr(args, "cross_read", False):
        cmd_cross_read()

    if args.generate:
        if not args.name and args.pattern != "list":
            print("❌ Для --generate нужно указать --name")
            print("   Или: --generate --pattern list  чтобы увидеть паттерны")
            sys.exit(1)
        name = args.name or "_list_"
        desc = args.description or (name.replace("_", " ") if name != "_list_" else "")
        cmd_generate(name, args.pattern, desc, dry_run=dry_run)


if __name__ == "__main__":
    main()
