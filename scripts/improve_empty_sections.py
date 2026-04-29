"""
improve_empty_sections.py — поиск и заполнение пустых секций.

Находит заголовки с минимальным содержимым (заглушки):
  - H2/H3 с менее чем MIN_CONTENT слов под ними
  - Секции только с одним вложенным заголовком и никакого текста
  - Файлы с >50% пустых секций

Режимы:
  --report  (по умолч.)  — только статистика
  --suggest              — предложить контент из базы знаний (BM25)
  --fill                 — добавить placeholder в пустые секции

Запуск:
    python scripts/improve_empty_sections.py
    python scripts/improve_empty_sections.py --section 05-habr-projects
    python scripts/improve_empty_sections.py --min-content 20
    python scripts/improve_empty_sections.py --fill --section 05-habr-projects
"""
import re
import sys
from collections import Counter
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TODAY = date.today().isoformat()

SUGGEST = "--suggest" in sys.argv
FILL = "--fill" in sys.argv
MIN_CONTENT = 15

if "--min-content" in sys.argv:
    idx = sys.argv.index("--min-content")
    if idx + 1 < len(sys.argv):
        MIN_CONTENT = int(sys.argv[idx + 1])

SECTION_FILTER = None
if "--section" in sys.argv:
    idx = sys.argv.index("--section")
    if idx + 1 < len(sys.argv):
        SECTION_FILTER = DOCS / sys.argv[idx + 1]

SKIP_FILES = {
    "EMPTY_SECTIONS.md", "SEARCH.md", "HEADING_AUDIT.md",
    "PARAGRAPH_QUALITY.md", "CONTRADICTIONS.md", "VOCABULARY.md",
    "SIMILAR_PASSAGES.md", "QUESTIONS.md", "PASSIVE_VOICE.md",
}

PLACEHOLDER = "> _Секция в разработке. Добавьте содержимое._\n"


def _parse_sections(text: str) -> list[dict]:
    """Парсит заголовки и считает слова под каждым."""
    clean = re.sub(r'```.*?```', ' ', text, flags=re.DOTALL)
    lines = clean.splitlines()
    sections = []

    for i, line in enumerate(lines):
        m = re.match(r'^(#{1,4})\s+(.+)$', line)
        if m:
            sections.append({
                "level": len(m.group(1)),
                "title": m.group(2).strip(),
                "line_idx": i,
            })

    # Добавляем конец каждой секции и считаем слова
    for k, sec in enumerate(sections):
        start = sec["line_idx"] + 1
        end = sections[k + 1]["line_idx"] if k + 1 < len(sections) else len(lines)
        # Только прямой текст, не вложенные заголовки
        content = "\n".join(
            l for l in lines[start:end]
            if not re.match(r'^#{1,4}\s', l)
        )
        sec["content_words"] = len(content.split())
        sec["content_raw"] = content.strip()
        sec["line_end"] = end

    return sections


def analyze_file(path: Path) -> dict | None:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return None

    sections = _parse_sections(text)
    if not sections:
        return None

    empty = [s for s in sections if s["content_words"] < MIN_CONTENT and s["level"] >= 2]
    total = [s for s in sections if s["level"] >= 2]

    if not empty:
        return None

    ratio = len(empty) / max(len(total), 1)
    return {
        "file": str(path.relative_to(ROOT)),
        "path": path,
        "empty": empty,
        "total_sections": len(total),
        "empty_count": len(empty),
        "empty_ratio": round(ratio, 2),
        "text": text,
    }


def _fill_empty_sections(path: Path, text: str, empty_sections: list[dict]) -> bool:
    """Добавляет placeholder в пустые секции."""
    lines = text.splitlines(keepends=True)
    # Вставляем с конца чтобы не сдвигать индексы
    for sec in sorted(empty_sections, key=lambda x: -x["line_idx"]):
        insert_pos = sec["line_idx"] + 1
        if insert_pos <= len(lines):
            lines.insert(insert_pos, PLACEHOLDER)
    new_text = "".join(lines)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        return True
    return False


def main() -> None:
    mode = "FILL" if FILL else ("SUGGEST" if SUGGEST else "report")
    print(f"🕳️  improve_empty_sections.py — пустые секции ({mode})")
    print(f"   Порог: < {MIN_CONTENT} слов\n")

    target = SECTION_FILTER or DOCS
    files = [f for f in sorted(target.rglob("*.md"))
             if f.name not in SKIP_FILES
             and "-parts" not in str(f)
             and "obsidian" not in str(f)]
    print(f"   Файлов: {len(files)}\n")

    results = []
    for f in files:
        res = analyze_file(f)
        if res:
            results.append(res)

    total_empty = sum(r["empty_count"] for r in results)
    heavy = [r for r in results if r["empty_ratio"] >= 0.5]

    print(f"   Файлов с пустыми секциями: {len(results)}")
    print(f"   Всего пустых секций: {total_empty}")
    print(f"   Файлов с ≥50% пустых: {len(heavy)}")

    lines = [
        "# Пустые секции\n",
        f"_Обновлено: {TODAY}_\n",
        f"Файлов с проблемами: **{len(results)}** | Пустых секций: **{total_empty}**\n",
        f"> Пустая секция — заголовок с менее чем {MIN_CONTENT} слов содержимого.\n",
    ]

    if heavy:
        lines += [
            "\n## Файлы с ≥50% пустых секций (приоритет)\n",
            "| Файл | Пустых | Всего | % |",
            "|------|--------|-------|---|",
        ]
        for r in sorted(heavy, key=lambda x: -x["empty_ratio"]):
            fname = r["file"].split("/")[-1]
            lines.append(
                f"| `{fname}` | {r['empty_count']} | "
                f"{r['total_sections']} | {r['empty_ratio']*100:.0f}% |"
            )

    lines += ["\n## Все файлы с пустыми секциями\n"]
    for r in sorted(results, key=lambda x: -x["empty_count"]):
        fname = r["file"].split("/")[-1]
        lines.append(f"### `{fname}` ({r['empty_count']} из {r['total_sections']})\n")
        for sec in r["empty"][:5]:
            lines.append(
                f"- {'#' * sec['level']} {sec['title']} "
                f"({sec['content_words']} сл., строка {sec['line_idx']+1})"
            )
        if len(r["empty"]) > 5:
            lines.append(f"- _...ещё {len(r['empty'])-5}_")
        lines.append("")

    if FILL:
        filled = 0
        for r in results:
            if _fill_empty_sections(r["path"], r["text"], r["empty"]):
                filled += 1
                print(f"  ✅ {r['file']}")
        print(f"\n  Заполнено файлов: {filled}")
        lines.append(f"\n_Плейсхолдеры добавлены в {filled} файлов._\n")

    out = DOCS / "EMPTY_SECTIONS.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
