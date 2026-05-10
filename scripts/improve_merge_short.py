"""
improve_merge_short.py — сливает слишком короткие файлы с предыдущим соседом.

Файлы короче MIN_CHARS символов присоединяются к предыдущему файлу той же папки
и удаляются. Операция необратима — используйте --dry-run перед применением.

Запуск:
    python scripts/improve_merge_short.py --dry-run   # показать план, не изменять
    python scripts/improve_merge_short.py             # применить (⚠ необратимо)
"""
import argparse
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
MIN_CHARS = 100


def merge_short_files(dry_run: bool = False) -> None:
    merged = 0

    for folder in sorted(DOCS.rglob("*")):
        if not folder.is_dir():
            continue

        files = sorted(folder.glob("*.md"))
        if len(files) < 2:
            continue

        i = 1
        while i < len(files):
            f = files[i]
            text = f.read_text(encoding="utf-8")

            if len(text) < MIN_CHARS:
                prev = files[i - 1]
                if dry_run:
                    print(f"  [dry-run] {f.relative_to(DOCS)} ({len(text)} симв.) → слить в {prev.name}")
                else:
                    prev_text = prev.read_text(encoding="utf-8")
                    prev.write_text(prev_text.rstrip() + "\n\n" + text.strip() + "\n",
                                    encoding="utf-8")
                    f.unlink()
                    print(f"  merged {f.name} → {prev.name}")
                    # Обновляем список только при реальном слиянии
                    files = sorted(folder.glob("*.md"))
                merged += 1
            else:
                i += 1

    if dry_run:
        print(f"\n[dry-run] файлов к слиянию: {merged}. Уберите --dry-run чтобы применить.")
        if merged > 0:
            print("[dry-run] ⚠  Операция необратима — слитые файлы удаляются.")
    else:
        print(f"\nИтого: {merged} файлов слито.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Сливает слишком короткие файлы с предыдущим соседом (⚠ необратимо)"
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Показать план слияния, не изменять файлы")
    args = parser.parse_args()
    merge_short_files(dry_run=args.dry_run)
