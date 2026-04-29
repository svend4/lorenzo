"""
improve_source_map.py — строит карту происхождения текстов.

Для каждого файла определяет:
  - Дата первого появления (git log)
  - Автор коммита (git log --format=%an)
  - Источники в frontmatter (поле source:, url:, origin:)
  - Внешние URL, указанные в тексте
  - Паттерны импорта (нумерация, суффиксы -md.md, -part-N)

Создаёт docs/SOURCE_MAP.md.
Запуск:
    python scripts/improve_source_map.py
    python scripts/improve_source_map.py --section 02-anthropic-vacancies
    python scripts/improve_source_map.py --show-imported   # только авто-импортированные
    python scripts/improve_source_map.py --authors         # группировка по авторам
"""
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TODAY = date.today().isoformat()

SECTION_FILTER = None
if "--section" in sys.argv:
    idx = sys.argv.index("--section")
    if idx + 1 < len(sys.argv):
        SECTION_FILTER = DOCS / sys.argv[idx + 1]

SHOW_IMPORTED = "--show-imported" in sys.argv
BY_AUTHORS    = "--authors"       in sys.argv

SKIP_FILES = {
    "SOURCE_MAP.md", "SEARCH.md", "READABILITY.md", "SPELLCHECK.md",
    "CONTENT_GAPS.md", "LINK_PREVIEW.md", "BROKEN_LINKS.md",
}

# Признаки авто-импортированных файлов
IMPORT_PATTERNS = [
    re.compile(r'-md\.md$'),           # file-md.md
    re.compile(r'-part-\d+\.md$'),     # file-part-2.md
    re.compile(r'^\d{2,3}-'),          # 042-title.md
    re.compile(r'content-overview'),    # content-overview.md
    re.compile(r'appendix-[a-z]'),      # appendix-b-...
]


def _is_imported(path: Path) -> bool:
    name = path.name.lower()
    return any(p.search(name) for p in IMPORT_PATTERNS)


def _git_info(path: Path) -> dict:
    """Получает информацию о файле из git log."""
    rel = str(path.relative_to(ROOT))
    result = subprocess.run(
        ["git", "log", "--follow", "--format=%H|%an|%ae|%ai|%s", "--", rel],
        cwd=ROOT, capture_output=True, text=True,
    )
    if result.returncode != 0 or not result.stdout.strip():
        return {}

    lines = result.stdout.strip().split('\n')
    # Первый коммит = последняя строка (самый старый)
    first_line = lines[-1].split('|', 4)
    last_line  = lines[0].split('|', 4)

    if len(first_line) < 4:
        return {}

    return {
        "first_commit": first_line[0][:8],
        "first_author": first_line[1],
        "first_email":  first_line[2],
        "first_date":   first_line[3][:10],
        "first_subject": first_line[4].strip() if len(first_line) > 4 else "",
        "last_commit":  last_line[0][:8],
        "last_author":  last_line[1],
        "last_date":    last_line[3][:10],
        "total_commits": len(lines),
    }


def _extract_sources(text: str) -> dict:
    """Извлекает источники из frontmatter и текста."""
    sources = {}

    # YAML frontmatter
    fm_m = re.match(r'^---\s*\n(.*?)\n---', text, re.DOTALL)
    if fm_m:
        fm = fm_m.group(1)
        for field in ("source", "url", "origin", "from", "original"):
            m = re.search(rf'^{field}:\s*(.+)$', fm, re.MULTILINE | re.IGNORECASE)
            if m:
                sources[field] = m.group(1).strip().strip('"\'')

    # HTML-комментарии source
    for m in re.finditer(r'<!--\s*source:\s*(.+?)\s*-->', text):
        sources.setdefault("comment_source", m.group(1).strip())

    # Внешние URL в тексте
    urls = re.findall(r'https?://[^\s\)\]">]{10,}', text)
    external = [u.rstrip('.,;)') for u in urls
                if any(d in u for d in ('habr.com', 'github.com', 'arxiv.org'))]
    if external:
        sources["external_urls"] = external[:3]

    return sources


def _categorize(path: Path, git_info: dict, sources: dict) -> str:
    """Категория происхождения файла."""
    if sources.get("source") or sources.get("url") or sources.get("origin"):
        return "🔗 Из источника"
    if sources.get("comment_source"):
        return "📋 Из комментария"
    if _is_imported(path):
        return "🤖 Авто-импорт"
    if git_info.get("first_author") and "bot" in git_info.get("first_author", "").lower():
        return "🤖 Bot-коммит"
    return "✍️ Ручной"


def main() -> None:
    print("🗺️  improve_source_map.py — карта происхождения текстов\n")

    target = SECTION_FILTER or DOCS
    all_files = [
        f for f in sorted(target.rglob("*.md"))
        if f.name not in SKIP_FILES
    ]

    if SHOW_IMPORTED:
        all_files = [f for f in all_files if _is_imported(f)]
    print(f"   Файлов: {len(all_files)}\n")

    records = []
    author_files: dict[str, list[str]] = defaultdict(list)

    for f in all_files:
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue

        git_info = _git_info(f)
        sources  = _extract_sources(text)
        category = _categorize(f, git_info, sources)
        rel = str(f.relative_to(ROOT))

        records.append({
            "path": f,
            "rel": rel,
            "category": category,
            "git": git_info,
            "sources": sources,
            "words": len(text.split()),
        })

        author = git_info.get("first_author", "unknown")
        author_files[author].append(rel)

    # Статистика
    cat_counts = Counter(r["category"] for r in records)
    author_counts = Counter({a: len(files) for a, files in author_files.items()})

    lines = [
        "# Карта происхождения текстов\n",
        f"_Обновлено: {TODAY}_\n",
        f"Проанализировано: **{len(records)}** файлов\n",
        "## Категории\n",
        "| Категория | Файлов |",
        "|-----------|--------|",
    ]
    for cat, count in sorted(cat_counts.items(), key=lambda x: -x[1]):
        lines.append(f"| {cat} | {count} |")

    lines += ["\n## Авторы\n", "| Автор | Файлов |", "|-------|--------|"]
    for author, count in author_counts.most_common(20):
        lines.append(f"| {author} | {count} |")

    if BY_AUTHORS:
        lines += ["\n## Файлы по авторам\n"]
        for author, files in sorted(author_files.items(), key=lambda x: -len(x[1])):
            lines.append(f"### {author} ({len(files)} файлов)\n")
            for fp in sorted(files)[:10]:
                lines.append(f"- `{fp}`")
            if len(files) > 10:
                lines.append(f"- _...ещё {len(files)-10}_")
            lines.append("")

    # Авто-импортированные
    imported = [r for r in records if r["category"] == "🤖 Авто-импорт"]
    if imported:
        lines += [
            f"\n## 🤖 Авто-импортированные файлы ({len(imported)})\n",
            "> Эти файлы были созданы автоматически и могут требовать проверки.\n",
            "| Файл | Слов | Первый коммит |",
            "|------|------|--------------|",
        ]
        for r in sorted(imported, key=lambda x: x["words"]):
            date_str = r["git"].get("first_date", "—")
            lines.append(f"| `{r['rel']}` | {r['words']} | {date_str} |")

    # С внешними источниками
    with_source = [r for r in records if r["sources"].get("external_urls")]
    if with_source:
        lines += [f"\n## 🔗 Файлы с внешними ссылками ({len(with_source)})\n"]
        for r in with_source[:20]:
            urls = r["sources"]["external_urls"]
            lines.append(f"- `{r['rel']}` — {urls[0][:60]}")

    out = DOCS / "SOURCE_MAP.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  категории: {dict(cat_counts)}")
    print(f"  авторов: {len(author_counts)}")


if __name__ == "__main__":
    main()
