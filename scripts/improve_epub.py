"""
improve_epub.py — собирает docs/ в EPUB через pandoc.

Объединяет все .md файлы секции в один EPUB с оглавлением.
Требует: pandoc (apt install pandoc / brew install pandoc)

Запуск:
    python scripts/improve_epub.py
    python scripts/improve_epub.py --section 01-svyazi --output docs/svyazi.epub
    python scripts/improve_epub.py --title "Svyazi 2.0 Knowledge Base"
    python scripts/improve_epub.py --check   # проверить, установлен ли pandoc
"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TODAY = date.today().isoformat()

SECTION_FILTER = None
if "--section" in sys.argv:
    idx = sys.argv.index("--section")
    if idx + 1 < len(sys.argv):
        SECTION_FILTER = DOCS / sys.argv[idx + 1]

OUTPUT = None
if "--output" in sys.argv:
    idx = sys.argv.index("--output")
    if idx + 1 < len(sys.argv):
        OUTPUT = ROOT / sys.argv[idx + 1]

TITLE = "Lorenzo Knowledge Base"
if "--title" in sys.argv:
    idx = sys.argv.index("--title")
    if idx + 1 < len(sys.argv):
        TITLE = sys.argv[idx + 1]

CHECK_ONLY = "--check" in sys.argv

SKIP_FILES = {"SEARCH.md", "READABILITY.md", "SPELLCHECK.md", "CONTENT_GAPS.md",
              "LINK_PREVIEW.md", "BROKEN_LINKS.md", "COVERAGE.md", "STALENESS.md"}


def _check_pandoc() -> bool:
    return shutil.which("pandoc") is not None


def _clean_for_epub(text: str) -> str:
    """Упрощает разметку для pandoc."""
    # Убираем HTML-комментарии
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    # Убираем badges/shields
    text = re.sub(r'!\[.*?\]\(https://img\.shields\.io[^)]+\)', '', text)
    return text


def build_epub(files: list[Path], output: Path, title: str) -> bool:
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)

        # Создаём merged.md
        merged_parts = [f"% {title}\n% Lorenzo / Svyazi 2.0\n% {TODAY}\n\n"]
        for f in files:
            try:
                text = f.read_text(encoding="utf-8")
                clean = _clean_for_epub(text)
                rel = f.relative_to(DOCS)
                merged_parts.append(f"\n\n---\n\n<!-- source: {rel} -->\n\n{clean}")
            except Exception:
                continue

        merged_file = tmp / "merged.md"
        merged_file.write_text("".join(merged_parts), encoding="utf-8")

        cmd = [
            "pandoc",
            str(merged_file),
            "-o", str(output),
            "--epub-chapter-level=2",
            f"--metadata=title:{title}",
            "--metadata=language:ru",
            "--toc",
            "--toc-depth=2",
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
        if result.returncode != 0:
            print(f"  ❌ pandoc error: {result.stderr[:200]}")
            return False
        return True


def main() -> None:
    print("📚 improve_epub.py — сборка EPUB")

    if CHECK_ONLY:
        if _check_pandoc():
            v = subprocess.run(["pandoc", "--version"], capture_output=True, text=True)
            ver = v.stdout.split('\n')[0] if v.stdout else "?"
            print(f"  ✅ pandoc доступен: {ver}")
        else:
            print("  ❌ pandoc не найден")
            print("  Установка: sudo apt install pandoc  или  brew install pandoc")
        return

    if not _check_pandoc():
        print("  ❌ pandoc не найден. Установите: sudo apt install pandoc")
        print("  Запустите с --check для проверки.")
        sys.exit(1)

    target = SECTION_FILTER or DOCS
    files = [f for f in sorted(target.rglob("*.md")) if f.name not in SKIP_FILES]
    print(f"   Файлов: {len(files)}")

    if not files:
        print("  Нет файлов для сборки")
        return

    section_name = SECTION_FILTER.name if SECTION_FILTER else "full"
    output = OUTPUT or (DOCS / f"export_{section_name}_{TODAY}.epub")

    print(f"   Вывод: {output.relative_to(ROOT)}")
    print(f"   Заголовок: {TITLE}\n")

    ok = build_epub(files, output, TITLE)
    if ok:
        size_kb = output.stat().st_size // 1024
        print(f"  ✅ EPUB создан: {output.relative_to(ROOT)} ({size_kb} KB)")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
