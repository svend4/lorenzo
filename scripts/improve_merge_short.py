"""
improve_merge_short.py — сливает слишком короткие файлы с предыдущим соседом.
Запуск: python scripts/improve_merge_short.py
"""
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
MIN_CHARS = 100


def merge_short_files():
    merged = 0
    deleted = 0

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
                prev_text = prev.read_text(encoding="utf-8")
                # Добавляем контент к предыдущему файлу
                prev.write_text(prev_text.rstrip() + "\n\n" + text.strip() + "\n",
                                encoding="utf-8")
                f.unlink()
                print(f"  merged {f.name} → {prev.name}")
                # Обновляем список
                files = sorted(folder.glob("*.md"))
                merged += 1
            else:
                i += 1

    print(f"\nИтого: {merged} файлов слито, {deleted} удалено.")


if __name__ == "__main__":
    merge_short_files()
