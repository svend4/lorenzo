"""
improve_obsidian.py — готовит docs/ для импорта в Obsidian.

Преобразования:
  1. Добавляет YAML frontmatter (title, tags, date) если нет
  2. Заменяет [Text](../path/file.md) → [[file]] (wikilinks)
  3. Создаёт docs/obsidian/ с готовыми файлами (не перезаписывает оригиналы)

Запуск:
    python scripts/improve_obsidian.py
    python scripts/improve_obsidian.py --in-place   # правит оригиналы
    python scripts/improve_obsidian.py --dry-run
    python scripts/improve_obsidian.py --section 05-habr-projects
"""
import re
import sys
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
OUT_DIR = DOCS / "obsidian"
TODAY = date.today().isoformat()

IN_PLACE = "--in-place" in sys.argv
DRY_RUN  = "--dry-run"  in sys.argv

SECTION_FILTER = None
if "--section" in sys.argv:
    idx = sys.argv.index("--section")
    if idx + 1 < len(sys.argv):
        SECTION_FILTER = DOCS / sys.argv[idx + 1]

SKIP_FILES = {"READABILITY.md", "SPELLCHECK.md", "SEARCH.md", "CONTENT_GAPS.md",
              "LINK_PREVIEW.md", "BROKEN_LINKS.md"}

FRONTMATTER_RE = re.compile(r'^---\s*\n.*?\n---\s*\n', re.DOTALL)
MD_LINK_RE = re.compile(r'\[([^\]]+)\]\(([^)]+\.md[^)]*)\)')
TAG_RE = re.compile(r'<!--\s*tags:\s*([^-]+)\s*-->')


def _extract_title(text: str, path: Path) -> str:
    m = re.search(r'^#\s+(.+)$', text, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return path.stem.replace('-', ' ').replace('_', ' ').title()


def _extract_tags(text: str) -> list[str]:
    m = TAG_RE.search(text)
    if m:
        return [t.strip() for t in m.group(1).split(',') if t.strip()]
    # Угадываем тег по пути
    return []


def _section_tag(path: Path) -> str:
    parts = path.relative_to(DOCS).parts
    if len(parts) > 1:
        return parts[0].lstrip('0123456789-')
    return "general"


def _make_frontmatter(title: str, tags: list[str], path: Path) -> str:
    all_tags = list(dict.fromkeys(tags + [_section_tag(path)]))
    tags_str = "\n".join(f"  - {t}" for t in all_tags)
    return f"---\ntitle: \"{title}\"\ntags:\n{tags_str}\ndate: {TODAY}\n---\n\n"


def _convert_links(text: str, source_path: Path) -> str:
    """Заменяет markdown-ссылки на .md на [[wikilinks]]."""
    def _replace(m):
        label = m.group(1)
        href = m.group(2).split('#')[0]  # убираем якорь
        if not href.endswith('.md'):
            return m.group(0)
        target = (source_path.parent / href).resolve()
        # Берём имя файла без расширения как wiki-ссылку
        wiki = target.stem
        if wiki == label or label.lower() == wiki.lower():
            return f"[[{wiki}]]"
        return f"[[{wiki}|{label}]]"
    return MD_LINK_RE.sub(_replace, text)


def process_file(path: Path, out_base: Path | None) -> str | None:
    text = path.read_text(encoding="utf-8")

    # Убираем существующий frontmatter если есть
    has_fm = bool(FRONTMATTER_RE.match(text))
    body = FRONTMATTER_RE.sub('', text).lstrip() if has_fm else text

    title = _extract_title(body, path)
    tags = _extract_tags(body)
    fm = _make_frontmatter(title, tags, path)

    # Конвертируем ссылки
    body = _convert_links(body, path)

    result = fm + body

    if DRY_RUN:
        return result

    if IN_PLACE:
        out_path = path
    else:
        rel = path.relative_to(DOCS)
        out_path = out_base / rel
        out_path.parent.mkdir(parents=True, exist_ok=True)

    out_path.write_text(result, encoding="utf-8")
    return result


def main() -> None:
    print("🔮 improve_obsidian.py — подготовка для Obsidian")
    if IN_PLACE:
        print("   Режим: in-place (правим оригиналы)")
    elif DRY_RUN:
        print("   Режим: dry-run")
    else:
        print(f"   Вывод: {OUT_DIR.relative_to(ROOT)}/")

    target = SECTION_FILTER or DOCS
    files = [f for f in sorted(target.rglob("*.md"))
             if f.name not in SKIP_FILES and "obsidian" not in str(f)]
    print(f"   Файлов: {len(files)}\n")

    if not IN_PLACE and not DRY_RUN:
        OUT_DIR.mkdir(exist_ok=True)

    ok = 0
    for f in files:
        try:
            result = process_file(f, OUT_DIR if not IN_PLACE else None)
            if result:
                ok += 1
        except Exception as e:
            print(f"  ❌ {f.name}: {e}")

    print(f"  Обработано: {ok}/{len(files)} файлов")
    if not IN_PLACE and not DRY_RUN:
        print(f"  Obsidian vault: {OUT_DIR.relative_to(ROOT)}/")
        print("  Откройте папку docs/obsidian/ как vault в Obsidian.")


if __name__ == "__main__":
    main()
