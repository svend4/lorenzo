"""
improve_extract_tables.py — извлекает все Markdown-таблицы из docs/
в один файл docs/TABLES.md для быстрого просмотра.
Запуск: python scripts/improve_extract_tables.py
"""
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"


def extract_tables(text: str) -> list[str]:
    """Извлекает все Markdown-таблицы из текста."""
    tables = []
    lines = text.split('\n')
    in_table = False
    current = []

    for line in lines:
        if line.strip().startswith('|'):
            current.append(line)
            in_table = True
        else:
            if in_table and len(current) >= 2:
                tables.append('\n'.join(current))
            current = []
            in_table = False

    if in_table and len(current) >= 2:
        tables.append('\n'.join(current))

    return tables


def get_table_context(text: str, table: str) -> str:
    """Находит заголовок перед таблицей для контекста."""
    idx = text.find(table[:50])
    if idx < 0:
        return ""
    before = text[:idx]
    headers = re.findall(r'^#{1,3}\s+(.+)$', before, re.MULTILINE)
    return headers[-1] if headers else ""


def count_cols(table: str) -> int:
    first_row = table.split('\n')[0]
    return first_row.count('|') - 1


def main():
    print("Извлечение таблиц...")
    by_section: dict[str, list[dict]] = defaultdict(list)
    total = 0

    for f in sorted(DOCS.rglob("*.md")):
        skip = {"TABLES.md", "CROSSREFS.md", "GLOSSARY.md",
                "PRIORITIES.md", "SEARCH.md", "TAGS.md"}
        if f.name in skip:
            continue
        text = f.read_text(encoding="utf-8")
        tables = extract_tables(text)

        section = f.relative_to(DOCS).parts[0] if len(f.relative_to(DOCS).parts) > 1 else "root"

        for table in tables:
            context = get_table_context(text, table)
            cols = count_cols(table)
            rows = len([l for l in table.split('\n') if l.strip().startswith('|')]) - 2
            by_section[section].append({
                "file": str(f.relative_to(ROOT)),
                "context": context,
                "cols": cols,
                "rows": rows,
                "table": table,
            })
            total += 1

    lines = [
        "# Все таблицы репозитория\n",
        f"**Всего таблиц:** {total}\n",
    ]

    for section in sorted(by_section.keys()):
        tables = by_section[section]
        lines.append(f"\n## {section} ({len(tables)} таблиц)\n")

        for i, t in enumerate(tables, 1):
            ctx = t["context"] or t["file"].split("/")[-1].replace(".md", "")
            lines.append(f"\n### {i}. {ctx[:60]}")
            lines.append(f"_Файл: `{t['file']}` | {t['cols']} колонок, {t['rows']} строк_\n")
            lines.append(t["table"])
            lines.append("")

    out = DOCS / "TABLES.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)} ({total} таблиц)")


if __name__ == "__main__":
    main()
