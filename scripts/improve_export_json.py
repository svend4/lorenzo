"""
improve_export_json.py — экспортирует всю структуру docs/ в structured JSON.
Каждый файл: путь, заголовок, слова, теги, summary, первые 500 символов.
Создаёт docs/export_full.json (для API/программного доступа).
Запуск: python scripts/improve_export_json.py
"""
import re
import json
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

SKIP = {"export_full.json", "search_index.json", "sitemap.xml"}


def get_title(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()[:80]
    return fallback


def get_summary(text: str) -> str:
    m = re.search(r'<!--\s*summary\s*-->(.*?)<!--', text, re.DOTALL)
    if m:
        return m.group(1).strip()[:200]
    # Первый абзац без разметки
    clean = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    clean = re.sub(r'^#{1,6}\s+.*$', '', clean, flags=re.MULTILINE)
    clean = re.sub(r'[*_`\[\]|>]', '', clean)
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean[:200]


def get_tags(text: str) -> list[str]:
    m = re.search(r'<!--\s*tags:\s*([^-]+?)-->', text)
    if m:
        return [t.strip() for t in m.group(1).split(',') if t.strip()]
    return []


def get_h2_sections(text: str) -> list[str]:
    return [m.group(1).strip() for m in re.finditer(r'^## (.+)$', text, re.MULTILINE)]


def main():
    print("Экспорт в JSON...")

    docs_list = []
    sections: dict[str, list] = {}

    for f in sorted(DOCS.rglob("*")):
        if f.name in SKIP or f.suffix not in (".md",):
            continue
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue

        rel  = str(f.relative_to(ROOT))
        rel_docs = f.relative_to(DOCS)
        sec  = rel_docs.parts[0] if len(rel_docs.parts) > 1 else "root"
        stem = f.stem

        words   = len(text.split())
        title   = get_title(text, stem)
        summary = get_summary(text)
        tags    = get_tags(text)
        h2s     = get_h2_sections(text)

        has_code  = "```" in text
        has_table = "|---|" in text or "|--" in text
        links_count = len(re.findall(r'\[.+?\]\(.+?\)', text))

        entry = {
            "path":     rel,
            "section":  sec,
            "filename": f.name,
            "title":    title,
            "words":    words,
            "chars":    len(text),
            "summary":  summary,
            "tags":     tags,
            "sections": h2s[:10],
            "has_code":  has_code,
            "has_table": has_table,
            "links":    links_count,
            "preview":  text[:500].replace("\n", " "),
        }

        docs_list.append(entry)
        sections.setdefault(sec, []).append(rel)

    # Статистика
    total_words = sum(d["words"] for d in docs_list)
    meta = {
        "generated":    date.today().isoformat(),
        "total_files":  len(docs_list),
        "total_words":  total_words,
        "sections":     {k: len(v) for k, v in sections.items()},
        "schema_version": "1.0",
    }

    output = {
        "meta":  meta,
        "docs":  docs_list,
    }

    out = DOCS / "export_full.json"
    out.write_text(
        json.dumps(output, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    size_kb = out.stat().st_size // 1024
    print(f"  wrote: {out.relative_to(ROOT)} ({size_kb} KB)")
    print(f"  файлов: {len(docs_list)}, слов: {total_words:,}")


if __name__ == "__main__":
    main()
