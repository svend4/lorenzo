"""
improve_crosslink_all.py — прописывает обратные ссылки (backlinks) во все файлы.

Алгоритм:
  1. Сканирует все .md файлы и строит граф: кто на кого ссылается
  2. Для каждого файла добавляет раздел "## Упоминается в" (обратные ссылки)
  3. Идемпотентно: обновляет существующий блок по маркеру

Дополнительно:
  - Добавляет прямые ссылки "## Связанные документы" на основе ключевых слов
  - Строит статистику связности (сколько входящих/исходящих ссылок)

Режимы:
  --dry-run  (по умолчанию)
  --apply    — реально записать
  --min-refs N — минимум обратных ссылок для добавления (по умолчанию: 1)
  --keywords — дополнительно добавлять ссылки по TF-IDF ключевым словам

Запуск:
    python scripts/improve_crosslink_all.py --dry-run
    python scripts/improve_crosslink_all.py --apply
    python scripts/improve_crosslink_all.py --apply --keywords
"""
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TODAY = date.today().isoformat()

APPLY    = "--apply"    in sys.argv
DRY_RUN  = not APPLY
KEYWORDS = "--keywords" in sys.argv

MIN_REFS = 1
if "--min-refs" in sys.argv:
    idx = sys.argv.index("--min-refs")
    if idx + 1 < len(sys.argv):
        MIN_REFS = int(sys.argv[idx + 1])

SECTION_FILTER = None
if "--section" in sys.argv:
    idx = sys.argv.index("--section")
    if idx + 1 < len(sys.argv):
        SECTION_FILTER = DOCS / sys.argv[idx + 1]

SKIP_FILES = {
    "SEARCH.md", "READABILITY.md", "SPELLCHECK.md", "CONTENT_GAPS.md",
    "LINK_PREVIEW.md", "BROKEN_LINKS.md", "COVERAGE.md", "STALENESS.md",
    "OUTLINE.md", "COMPARE.md", "TOPIC_MODEL.md", "CITATION_INDEX.md",
    "GITHUB_ISSUES.md", "DEPENDABOT.md",
}

BACKLINK_MARKER = "<!-- backlinks-auto -->"
RELATED_MARKER  = "<!-- related-auto -->"

STOPWORDS = {
    "и", "в", "не", "на", "с", "по", "к", "из", "за", "для", "это",
    "как", "но", "или", "что", "был", "the", "a", "an", "is", "are",
    "of", "in", "on", "to", "for", "with", "by", "and", "not",
}


def _extract_md_links(text: str, source_path: Path) -> set[Path]:
    """Извлекает все .md ссылки из текста, разрешает их в абсолютные пути."""
    found = set()
    for m in re.finditer(r'\[([^\]]*)\]\(([^)]+\.md[^)]*)\)', text):
        href = m.group(2).split('#')[0]
        try:
            target = (source_path.parent / href).resolve()
            if target.exists() and target.suffix == '.md':
                found.add(target)
        except Exception:
            pass
    return found


def _top_words(text: str, n: int = 15) -> set[str]:
    clean = re.sub(r'```.*?```', ' ', text, flags=re.DOTALL)
    clean = re.sub(r'https?://\S+', ' ', clean)
    tokens = [
        t for t in re.findall(r'[а-яёa-z]{4,}', clean.lower())
        if t not in STOPWORDS
    ]
    return {w for w, _ in Counter(tokens).most_common(n)}


def _title(path: Path, text: str) -> str:
    m = re.search(r'^#\s+(.+)$', text, re.MULTILINE)
    return m.group(1).strip() if m else path.stem.replace('-', ' ').title()


def _word_count(text: str) -> int:
    return len(re.findall(r'\S+', text))


def _build_backlink_block(backlinks: list[tuple[Path, str]]) -> str:
    """Строит блок обратных ссылок."""
    lines = [
        f"\n{BACKLINK_MARKER}",
        "## Упоминается в\n",
    ]
    for path, title in sorted(backlinks, key=lambda x: x[1]):
        rel = path.relative_to(ROOT)
        lines.append(f"- [{title}]({rel})")
    return "\n".join(lines) + "\n"


def _build_related_block(related: list[tuple[Path, str, float]]) -> str:
    """Строит блок связанных документов (по ключевым словам)."""
    lines = [
        f"\n{RELATED_MARKER}",
        "## Связанные документы\n",
    ]
    for path, title, sim in sorted(related, key=lambda x: -x[2])[:8]:
        rel = path.relative_to(ROOT)
        pct = int(sim * 100)
        lines.append(f"- [{title}]({rel}) _{pct}%_")
    return "\n".join(lines) + "\n"


def _update_or_append(text: str, marker: str, new_block: str) -> str:
    """Обновляет существующий блок по маркеру или добавляет в конец."""
    if marker in text:
        # Заменяем от маркера до следующего ## или конца файла
        pattern = re.compile(
            rf'{re.escape(marker)}.*?(?=\n##|\Z)',
            re.DOTALL,
        )
        return pattern.sub(new_block.strip(), text)
    return text.rstrip() + "\n" + new_block


def main() -> None:
    print("🔗 improve_crosslink_all.py — добавление обратных ссылок")
    print(f"   Режим: {'APPLY' if APPLY else 'dry-run'}")
    if KEYWORDS:
        print("   + ключевые слова: включено\n")
    else:
        print("   Ключевые слова: выкл (добавьте --keywords)\n")

    target = SECTION_FILTER or DOCS
    all_files = [
        f for f in sorted(DOCS.rglob("*.md"))
        if f.name not in SKIP_FILES
        and "obsidian" not in str(f)
        and "confluence" not in str(f)
        and "merged" not in str(f)
    ]
    print(f"   Файлов: {len(all_files)}\n")

    # Загружаем тексты и строим граф ссылок
    texts: dict[str, str] = {}
    for f in all_files:
        try:
            texts[str(f)] = f.read_text(encoding="utf-8")
        except Exception:
            texts[str(f)] = ""

    # Граф: file → set of files it links to
    links_to: dict[str, set[str]] = {}
    for f in all_files:
        text = texts[str(f)]
        targets = _extract_md_links(text, f)
        links_to[str(f)] = {str(t) for t in targets if str(t) in texts}

    # Инвертируем: file → list of files that link to it (backlinks)
    backlinks_map: dict[str, list[str]] = defaultdict(list)
    for src, targets in links_to.items():
        for tgt in targets:
            backlinks_map[tgt].append(src)

    # Ключевые слова для related
    kw_cache: dict[str, set[str]] = {}
    if KEYWORDS:
        print("   Вычисляем ключевые слова...", end=" ", flush=True)
        for f in all_files:
            kw_cache[str(f)] = _top_words(texts[str(f)], 20)
        print("готово\n")

    # Фильтруем: только файлы в target
    target_files = [f for f in all_files if str(f).startswith(str(target))]

    updated = 0
    no_backlinks = 0

    for f in target_files:
        text = texts[str(f)]
        if _word_count(text) < 20:
            continue

        # Обратные ссылки
        bl_paths = [Path(p) for p in backlinks_map.get(str(f), [])
                    if Path(p).name not in SKIP_FILES]
        bl_list = [(p, _title(p, texts.get(str(p), ""))) for p in bl_paths]

        # Related по ключевым словам
        related_list: list[tuple[Path, str, float]] = []
        if KEYWORDS and str(f) in kw_cache:
            my_kw = kw_cache[str(f)]
            for other in all_files:
                if other == f or str(other) not in kw_cache:
                    continue
                sim = len(my_kw & kw_cache[str(other)]) / max(1, len(my_kw | kw_cache[str(other)]))
                if sim >= 0.15:
                    related_list.append((other, _title(other, texts.get(str(other), "")), sim))

        if len(bl_list) < MIN_REFS and not related_list:
            no_backlinks += 1
            continue

        rel = f.relative_to(ROOT)
        new_text = text

        if len(bl_list) >= MIN_REFS:
            bl_block = _build_backlink_block(bl_list)
            new_text = _update_or_append(new_text, BACKLINK_MARKER, bl_block)
            print(f"  ← {rel} ({len(bl_list)} backlinks)")

        if related_list:
            rel_block = _build_related_block(related_list)
            new_text = _update_or_append(new_text, RELATED_MARKER, rel_block)

        if new_text != text:
            updated += 1
            if APPLY:
                f.write_text(new_text, encoding="utf-8")

    print(f"\n  Обновлено: {updated} файлов")
    print(f"  Без входящих ссылок: {no_backlinks}")

    # Статистика связности
    top_linked = sorted(backlinks_map.items(), key=lambda x: -len(x[1]))[:5]
    if top_linked:
        print("\n  Топ-5 самых цитируемых файлов:")
        for path_str, refs in top_linked:
            f = Path(path_str)
            if f.exists():
                print(f"    {len(refs):3d}× {f.relative_to(ROOT)}")

    if DRY_RUN:
        print("\n  Запустите с --apply для реальной записи.")


if __name__ == "__main__":
    main()
