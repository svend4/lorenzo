"""
improve_toc.py — добавляет Table of Contents в начало файлов длиннее 500 слов.
Генерирует TOC из H2/H3 заголовков с якорными ссылками.
Запуск: python scripts/improve_toc.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
MIN_WORDS = 500
TOC_MARKER = "<!-- toc -->"


def make_anchor(heading: str) -> str:
    h = heading.lower().strip()
    h = re.sub(r'[^\w\s\-а-яёa-z]', '', h)
    h = re.sub(r'\s+', '-', h.strip())
    return h


def build_toc(text: str) -> str:
    lines = []
    for m in re.finditer(r'^(#{2,3})\s+(.+)$', text, re.MULTILINE):
        level = len(m.group(1))
        title = m.group(2).strip()
        anchor = make_anchor(title)
        indent = "  " * (level - 2)
        lines.append(f"{indent}- [{title}](#{anchor})")
    return "\n".join(lines)


def add_toc(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if TOC_MARKER in text:
        return False
    words = len(text.split())
    if words < MIN_WORDS:
        return False

    toc = build_toc(text)
    if not toc or toc.count('\n') < 2:
        return False  # слишком мало заголовков

    toc_block = f"\n{TOC_MARKER}\n## Содержание\n\n{toc}\n\n---\n"

    # Вставляем после первого H1
    lines = text.split('\n')
    insert_at = 1
    for i, line in enumerate(lines):
        if line.startswith('# '):
            insert_at = i + 1
            # Пропускаем summary-блок если есть
            for j in range(i + 1, min(i + 12, len(lines))):
                if lines[j].strip() == '---':
                    insert_at = j + 1
                    break
            break

    lines.insert(insert_at, toc_block)
    path.write_text('\n'.join(lines), encoding="utf-8")
    return True


def main():
    print("Добавление Table of Contents...")
    added = 0
    skipped = 0

    for f in sorted(DOCS.rglob("*.md")):
        skip = {"README.md", "CHANGELOG.md", "TAGS.md", "GLOSSARY.md",
                "CROSSREFS.md", "CLUSTERS.md", "SEARCH.md", "LINKS.md"}
        if f.name in skip:
            continue
        if add_toc(f):
            print(f"  toc: {f.relative_to(ROOT)}")
            added += 1
        else:
            skipped += 1

    print(f"\nДобавлено TOC: {added}, пропущено: {skipped}")


if __name__ == "__main__":
    main()
