"""
improve_search_index.py — строит полнотекстовый JSON-индекс всех docs/.
Создаёт docs/search_index.json для быстрого поиска по проекту.
Запуск: python scripts/improve_search_index.py
"""
import re
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

TAG_RE = re.compile(r'<!--\s*tags:\s*([^-]+)\s*-->')
SUMMARY_RE = re.compile(r'<!--\s*summary\s*-->\s*\n>\s*(.+?)(?:\n|$)')
PROJ_LINE_RE = re.compile(r'\*\*Проекты:\*\*\s*(.+)')


def extract_meta(text: str) -> dict:
    tags = []
    m = TAG_RE.search(text)
    if m:
        tags = [t.strip() for t in m.group(1).split(',')]

    summary = ""
    m = SUMMARY_RE.search(text)
    if m:
        summary = m.group(1).strip()[:300]

    projects = []
    m = PROJ_LINE_RE.search(text)
    if m:
        projects = [p.strip() for p in m.group(1).split(',')]

    # Заголовок — первая строка начинающаяся с #
    title = ""
    for line in text.split('\n'):
        if line.startswith('# '):
            title = line[2:].strip()
            break

    # Чистый текст без Markdown-разметки
    clean = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    clean = re.sub(r'[#*`>\[\]|]', ' ', clean)
    clean = re.sub(r'\s+', ' ', clean).strip()

    return {
        "title": title,
        "summary": summary,
        "tags": tags,
        "projects": projects,
        "text_length": len(clean),
        "words": len(clean.split()),
    }


def build_index() -> list[dict]:
    index = []
    for f in sorted(DOCS.rglob("*.md")):
        if f.name in ("search_index.json",):
            continue
        text = f.read_text(encoding="utf-8")
        if len(text) < 50:
            continue

        meta = extract_meta(text)
        meta["path"] = str(f.relative_to(ROOT))
        meta["section"] = f.parts[f.parts.index("docs") + 1] if "docs" in f.parts else ""

        # Полный чистый текст для поиска (поле "content")
        content = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
        content = re.sub(r'[#*`>\[\]|]', ' ', content)
        content = re.sub(r'\s+', ' ', content).strip()
        meta["content"] = content[:3000]   # лимит 3000 символов для баланса размера/качества
        meta["preview"] = content[:500]    # обратная совместимость со старым форматом

        index.append(meta)

    return index


def main():
    print("Строю поисковый индекс...")
    index = build_index()

    out = DOCS / "search_index.json"
    out.write_text(
        json.dumps(index, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    total_words = sum(e["words"] for e in index)
    print(f"  файлов в индексе: {len(index)}")
    print(f"  всего слов: {total_words:,}")
    print(f"  wrote: {out.relative_to(ROOT)} ({out.stat().st_size // 1024} KB)")

    # Также создаём упрощённый Markdown-индекс для чтения
    md_lines = [
        "# Поисковый индекс\n",
        f"**Файлов:** {len(index)}  ",
        f"**Слов:** {total_words:,}\n",
        "| Файл | Теги | Проекты | Слов |",
        "|------|------|---------|------|",
    ]
    for e in index:
        if e["name"] if "name" in e else True:
            tags = ", ".join(e["tags"][:3])
            projs = ", ".join(e["projects"][:3])
            md_lines.append(
                f"| `{e['path']}` | {tags} | {projs} | {e['words']} |"
            )

    (DOCS / "SEARCH.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    print(f"  wrote: docs/SEARCH.md")


if __name__ == "__main__":
    main()
