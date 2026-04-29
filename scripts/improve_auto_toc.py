"""
improve_auto_toc.py — автоматически добавляет таблицу содержания (TOC) в файлы.

Вставляет ## Contents после первого H1 заголовка.
Идемпотентно: обновляет существующий TOC по маркеру.
Пропускает файлы с менее чем 3 подзаголовками.

Режимы:
  --dry-run  (по умолчанию)
  --apply    — реально записать
  --section  — только одна секция
  --min-headings N — мин. заголовков для добавления TOC (по умолч.: 3)
  --depth N        — глубина TOC: 2=H2, 3=H2+H3 (по умолч.: 3)

Запуск:
    python scripts/improve_auto_toc.py --dry-run
    python scripts/improve_auto_toc.py --apply
    python scripts/improve_auto_toc.py --apply --section 02-anthropic-vacancies
"""
import re
import sys
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TODAY = date.today().isoformat()

APPLY   = "--apply"   in sys.argv
DRY_RUN = not APPLY

MIN_HEADINGS = 3
if "--min-headings" in sys.argv:
    idx = sys.argv.index("--min-headings")
    if idx + 1 < len(sys.argv):
        MIN_HEADINGS = int(sys.argv[idx + 1])

TOC_DEPTH = 3
if "--depth" in sys.argv:
    idx = sys.argv.index("--depth")
    if idx + 1 < len(sys.argv):
        TOC_DEPTH = int(sys.argv[idx + 1])

SECTION_FILTER = None
if "--section" in sys.argv:
    idx = sys.argv.index("--section")
    if idx + 1 < len(sys.argv):
        SECTION_FILTER = DOCS / sys.argv[idx + 1]

SKIP_FILES = {
    "README.md", "SEARCH.md", "OUTLINE.md", "COMPARE.md",
    "TOPIC_MODEL.md", "CITATION_INDEX.md", "READING_TIME.md",
    "READABILITY.md", "SPELLCHECK.md", "CONTENT_GAPS.md",
    "SOURCE_MAP.md", "DUPLICATE_ACROSS.md", "EXTERNAL_COMPARE.md",
}

TOC_MARKER = "<!-- toc-auto -->"


def _slug(heading: str) -> str:
    """GitHub-совместимый якорь из заголовка."""
    s = heading.lower().strip()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_]+', '-', s)
    return s.strip('-')


def _build_toc(headings: list[tuple[int, str]]) -> str:
    """Строит markdown TOC из списка (уровень, заголовок)."""
    lines = [TOC_MARKER, "## Contents\n"]
    seen_slugs: dict[str, int] = {}
    for level, title in headings:
        indent = "  " * (level - 2)
        slug = _slug(title)
        # Дедупликация якорей
        if slug in seen_slugs:
            seen_slugs[slug] += 1
            slug = f"{slug}-{seen_slugs[slug]}"
        else:
            seen_slugs[slug] = 0
        lines.append(f"{indent}- [{title}](#{slug})")
    return "\n".join(lines) + "\n"


def _extract_headings(text: str, max_level: int) -> list[tuple[int, str]]:
    """Извлекает заголовки H2..Hmax (H1 пропускаем — это заголовок документа)."""
    result = []
    in_code = False
    for line in text.split('\n'):
        if line.startswith('```'):
            in_code = not in_code
        if in_code:
            continue
        m = re.match(r'^(#{2,%d})\s+(.+)$' % max_level, line)
        if m:
            level = len(m.group(1))
            title = re.sub(r'[`*_]', '', m.group(2)).strip()
            result.append((level, title))
    return result


def _has_toc(text: str) -> bool:
    return TOC_MARKER in text or bool(re.search(
        r'^##\s+(Contents|Table of Contents|Содержание|Оглавление)',
        text, re.MULTILINE | re.IGNORECASE
    ))


def process_file(path: Path) -> bool:
    """Добавляет/обновляет TOC. Возвращает True если изменений."""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return False

    headings = _extract_headings(text, TOC_DEPTH)
    if len(headings) < MIN_HEADINGS:
        return False

    toc_block = _build_toc(headings)

    if _has_toc(text) and TOC_MARKER in text:
        # Обновляем существующий TOC
        new_text = re.sub(
            rf'{re.escape(TOC_MARKER)}.*?(?=\n##[^#]|\n#[^#]|\Z)',
            toc_block.strip(),
            text, flags=re.DOTALL,
        )
        if new_text == text:
            return False
    elif _has_toc(text):
        return False  # Есть ручной TOC — не трогаем
    else:
        # Вставляем после H1
        h1_m = re.search(r'^#\s+.+$', text, re.MULTILINE)
        if h1_m:
            insert_pos = h1_m.end()
            new_text = text[:insert_pos] + "\n\n" + toc_block + text[insert_pos:]
        else:
            new_text = toc_block + "\n" + text

    if APPLY:
        path.write_text(new_text, encoding="utf-8")
    return True


def main() -> None:
    print("📑 improve_auto_toc.py — автогенерация таблицы содержания")
    print(f"   Мин. заголовков: {MIN_HEADINGS}  |  Глубина: H2–H{TOC_DEPTH}")
    print(f"   Режим: {'APPLY' if APPLY else 'dry-run'}\n")

    target = SECTION_FILTER or DOCS
    files = [f for f in sorted(target.rglob("*.md")) if f.name not in SKIP_FILES]
    print(f"   Файлов: {len(files)}\n")

    updated = skipped_short = skipped_has = 0
    for f in files:
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue
        heads = _extract_headings(text, TOC_DEPTH)
        if len(heads) < MIN_HEADINGS:
            skipped_short += 1
            continue
        if _has_toc(text) and TOC_MARKER not in text:
            skipped_has += 1
            continue
        changed = process_file(f)
        if changed:
            rel = f.relative_to(ROOT)
            print(f"  ✅ {rel} ({len(heads)} заголовков)")
            updated += 1

    print(f"\n  {'Добавлено' if APPLY else 'Будет добавлено'}: {updated} TOC")
    print(f"  Пропущено (мало заголовков): {skipped_short}")
    print(f"  Пропущено (ручной TOC): {skipped_has}")
    if DRY_RUN:
        print("  Запустите с --apply для реальной записи.")


if __name__ == "__main__":
    main()
