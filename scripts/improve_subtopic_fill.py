"""
improve_subtopic_fill.py — дополняет файлы-заглушки контентом из базы знаний.

Для каждого файла с малым количеством слов (<MIN_WORDS):
  1. Определяет тему по заголовку и имеющимся словам
  2. Находит релевантные фрагменты из других файлов базы (по ключевым словам)
  3. Вставляет раздел "## Связанные материалы" с найденными цитатами
  4. Добавляет перекрёстные ссылки

Режимы:
  --dry-run  (по умолчанию) — показать план без записи
  --apply    — реально дополнить файлы
  --min-words N  — порог для «заглушки» (по умолчанию: 150)
  --section  — обрабатывать конкретную секцию

Запуск:
    python scripts/improve_subtopic_fill.py --dry-run
    python scripts/improve_subtopic_fill.py --apply --section 05-habr-projects
    python scripts/improve_subtopic_fill.py --apply --min-words 200
"""
import re
import sys
from collections import Counter
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TODAY = date.today().isoformat()

APPLY    = "--apply"   in sys.argv
DRY_RUN  = not APPLY

MIN_WORDS = 150
if "--min-words" in sys.argv:
    idx = sys.argv.index("--min-words")
    if idx + 1 < len(sys.argv):
        MIN_WORDS = int(sys.argv[idx + 1])

SECTION_FILTER = None
if "--section" in sys.argv:
    idx = sys.argv.index("--section")
    if idx + 1 < len(sys.argv):
        SECTION_FILTER = DOCS / sys.argv[idx + 1]

SKIP_FILES = {
    "README.md", "SEARCH.md", "READABILITY.md", "SPELLCHECK.md",
    "CONTENT_GAPS.md", "LINK_PREVIEW.md", "BROKEN_LINKS.md",
    "COVERAGE.md", "STALENESS.md", "OUTLINE.md", "COMPARE.md",
    "TOPIC_MODEL.md", "CITATION_INDEX.md",
}

STOPWORDS = {
    "и", "в", "не", "на", "с", "по", "к", "из", "за", "для", "это",
    "как", "но", "или", "что", "был", "the", "a", "an", "is", "are",
    "of", "in", "on", "to", "for", "with", "by", "and", "not",
}

FILL_MARKER = "<!-- subtopic-fill -->"
MAX_EXCERPTS = 3      # максимум цитат из других файлов
EXCERPT_LEN  = 400    # символов на цитату


def _word_count(text: str) -> int:
    return len(re.findall(r'\S+', text))


def _clean(text: str) -> str:
    text = re.sub(r'```.*?```', ' ', text, flags=re.DOTALL)
    text = re.sub(r'`[^`]+`', ' ', text)
    text = re.sub(r'<!--.*?-->', ' ', text, flags=re.DOTALL)
    text = re.sub(r'https?://\S+', ' ', text)
    return text.lower()


def _top_words(text: str, n: int = 20) -> set[str]:
    tokens = [
        t for t in re.findall(r'[а-яёa-z]{4,}', _clean(text))
        if t not in STOPWORDS
    ]
    return {w for w, _ in Counter(tokens).most_common(n)}


def _relevance(stub_words: set[str], source_text: str) -> float:
    """Релевантность источника для заглушки (Jaccard с буфером)."""
    source_words = _top_words(source_text, 40)
    if not stub_words or not source_words:
        return 0.0
    return len(stub_words & source_words) / max(1, len(stub_words | source_words))


def _extract_best_paragraph(text: str, query_words: set[str]) -> str:
    """Находит лучший абзац в тексте по пересечению с query_words."""
    clean = re.sub(r'```.*?```', ' ', text, flags=re.DOTALL)
    clean = re.sub(r'<!--.*?-->', ' ', clean, flags=re.DOTALL)
    paragraphs = [p.strip() for p in re.split(r'\n\n+', clean) if len(p.strip()) > 80]

    best_para, best_score = "", 0
    for para in paragraphs:
        words = set(re.findall(r'[а-яёa-z]{4,}', para.lower()))
        score = len(words & query_words)
        if score > best_score:
            best_score = score
            best_para = para

    # Обрезаем и чистим
    best_para = re.sub(r'[#*|_~>\[\]]', '', best_para)
    best_para = re.sub(r'\s+', ' ', best_para).strip()
    return best_para[:EXCERPT_LEN]


def _build_fill_section(stub_path: Path, stub_words: set[str],
                         all_files: list[Path]) -> str | None:
    """Строит раздел с дополнительными материалами."""
    candidates = []
    for f in all_files:
        if f == stub_path:
            continue
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue
        if _word_count(text) < 100:
            continue
        rel = _relevance(stub_words, text)
        if rel > 0.05:
            candidates.append((rel, f, text))

    candidates.sort(key=lambda x: -x[0])
    top = candidates[:MAX_EXCERPTS]

    if not top:
        return None

    lines = [
        f"\n{FILL_MARKER}",
        f"## Связанные материалы\n",
        f"_Автодополнено из базы знаний — {TODAY}_\n",
    ]
    for rel_score, f, text in top:
        rel_path = f.relative_to(ROOT)
        excerpt = _extract_best_paragraph(text, stub_words)
        title_m = re.search(r'^#\s+(.+)$', text, re.MULTILINE)
        title = title_m.group(1).strip() if title_m else f.stem.replace('-', ' ').title()

        lines.append(f"### [{title}]({rel_path})\n")
        if excerpt:
            lines.append(f"> {excerpt}\n")
        lines.append(f"_Релевантность: {int(rel_score*100)}%_\n")

    lines += [
        "## Перекрёстные ссылки\n",
        "См. также:",
    ]
    for _, f, _ in top:
        rel_path = f.relative_to(ROOT)
        lines.append(f"- [{f.stem}]({rel_path})")

    return "\n".join(lines)


def main() -> None:
    print("✏️  improve_subtopic_fill.py — дополнение файлов-заглушек")
    print(f"   Порог слов: {MIN_WORDS}  |  Режим: {'APPLY' if APPLY else 'dry-run'}\n")

    target = SECTION_FILTER or DOCS
    all_files = [
        f for f in sorted(DOCS.rglob("*.md"))  # ищем источники во всей базе
        if f.name not in SKIP_FILES
        and "obsidian" not in str(f)
        and "confluence" not in str(f)
    ]

    # Стабы — только в target
    stubs = [
        f for f in all_files
        if str(f).startswith(str(target))
    ]

    stub_targets = []
    for f in stubs:
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue
        if _word_count(text) < MIN_WORDS and FILL_MARKER not in text:
            stub_targets.append(f)

    print(f"   Файлов в базе: {len(all_files)}")
    print(f"   Файлов-заглушек (<{MIN_WORDS} слов): {len(stub_targets)}\n")

    if not stub_targets:
        print("  Заглушек не найдено — все файлы достаточно полные.")
        return

    filled = 0
    skipped = 0
    for stub in stub_targets:
        try:
            text = stub.read_text(encoding="utf-8")
        except Exception:
            continue
        stub_words = _top_words(text, 15)
        if len(stub_words) < 3:
            skipped += 1
            continue

        fill_section = _build_fill_section(stub, stub_words, all_files)
        if not fill_section:
            skipped += 1
            continue

        rel = stub.relative_to(ROOT)
        print(f"  📝 {rel}")
        print(f"     слов: {_word_count(text)}  ключевые: {', '.join(list(stub_words)[:5])}")

        if not DRY_RUN:
            stub.write_text(text.rstrip() + "\n" + fill_section + "\n", encoding="utf-8")
            filled += 1
        else:
            filled += 1

    action = "Дополнено" if APPLY else "Будет дополнено"
    print(f"\n  {action}: {filled} файлов  |  Пропущено: {skipped}")
    if DRY_RUN:
        print("  Запустите с --apply для реальной записи.")


if __name__ == "__main__":
    main()
