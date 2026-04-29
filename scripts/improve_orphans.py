"""
improve_orphans.py — находит документы без входящих ссылок (orphan docs).
Такие файлы изолированы от навигации и могут быть потеряны.
Создаёт docs/ORPHANS.md.
Запуск: python scripts/improve_orphans.py
"""
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

# Файлы, которые могут не иметь входящих ссылок по дизайну
ALWAYS_OK = {
    "README.md", "GLOSSARY.md", "AUTHORS.md", "LINKS.md",
    "CROSSREFS.md", "TIMELINE.md", "TAGS.md", "SEARCH.md",
    "GRAPH.md", "MINDMAP.md", "QA.md", "PRIORITIES.md",
    "CONTACTS.md", "ACTION_ITEMS.md", "MISSING.md", "CLUSTERS.md",
    "CONSISTENCY.md", "BROKEN_LINKS.md", "CHANGELOG.md",
    "DECISIONS.md", "READING_ORDER.md", "HEALTH.md", "WORD_FREQ.md",
    "CODE_BLOCKS.md", "TABLES.md", "SIMILAR.md", "QUESTIONS.md",
    "KPI.md", "STATS.md", "DENSITY.md", "COMPLEXITY.md",
    "ENTITIES.md", "CONCEPTS.md", "COMPARE.md", "DUPLICATES.md",
    "ABBREVIATIONS.md", "SENTIMENT.md", "NARRATIVE.md",
    "NETWORK.md", "BACKLINKS.md", "HEATMAP.md", "VALIDATION.md",
    "REPORT.md", "SITEMAP.md", "ORPHANS.md", "export.csv",
    "search_index.json", "sitemap.xml", "export_full.json",
    "network.dot", "index.html",
}


def collect_all_links(files: list[Path]) -> set[str]:
    """Все нормализованные пути, на которые есть хоть одна ссылка."""
    linked: set[str] = set()
    for f in files:
        text = f.read_text(encoding="utf-8")
        for m in re.finditer(r'\[([^\]]+)\]\(([^)#]+\.md[^)]*)\)', text):
            href = m.group(2).split("#")[0].strip()
            if href.startswith("http"):
                continue
            target = (f.parent / href).resolve()
            try:
                linked.add(str(target.relative_to(ROOT)))
            except ValueError:
                pass
    return linked


def main():
    print("Поиск изолированных документов...")

    all_md = [f for f in sorted(DOCS.rglob("*.md")) if f.name not in ALWAYS_OK]
    linked = collect_all_links(list(DOCS.rglob("*.md")))

    orphans = []
    for f in all_md:
        rel = str(f.relative_to(ROOT))
        if rel not in linked:
            words = len(f.read_text(encoding="utf-8").split())
            orphans.append((rel, words))

    # Сортируем: сначала большие (важные) изолированные
    orphans.sort(key=lambda x: -x[1])

    by_section: dict[str, list] = defaultdict(list)
    for rel, words in orphans:
        parts = Path(rel).parts
        sec = parts[1] if len(parts) > 2 else "root"
        by_section[sec].append((rel, words))

    lines = [
        "# Изолированные документы (Orphans)\n",
        f"**Найдено:** {len(orphans)} файлов без входящих ссылок из {len(all_md)} проверено.\n",
        "_Эти документы не связаны с остальными — их легко потерять._\n",

        "## Топ-20 по объёму (важные и изолированные)\n",
        "| Файл | Слов | Раздел |",
        "|------|------|--------|",
    ]
    for rel, words in orphans[:20]:
        parts = Path(rel).parts
        sec = parts[1] if len(parts) > 2 else "root"
        short = Path(rel).name.replace(".md", "")[:40]
        lines.append(f"| `{short}` | {words} | `{sec}` |")

    lines += [f"\n## По разделам\n"]
    for sec in sorted(by_section.keys()):
        items = by_section[sec]
        lines.append(f"\n### {sec} ({len(items)} изолированных)\n")
        for rel, words in items[:15]:
            short = Path(rel).name
            lines.append(f"- `{short}` ({words} слов)")
        if len(items) > 15:
            lines.append(f"_...ещё {len(items)-15}_")

    lines += [
        "\n## Рекомендации\n",
        "1. Добавить ссылки на изолированные файлы из README.md соответствующего раздела",
        "2. Проверить, не являются ли они дублями других файлов",
        "3. Крупные изолированные файлы (>100 слов) — добавить в READING_ORDER.md",
        "4. Мелкие (<50 слов) — рассмотреть для удаления или слияния",
    ]

    out = DOCS / "ORPHANS.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  изолированных: {len(orphans)} из {len(all_md)}")


if __name__ == "__main__":
    main()
