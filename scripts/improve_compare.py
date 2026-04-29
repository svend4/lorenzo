"""
improve_compare.py — сравнивает текущее состояние docs/ с предыдущим коммитом.
Показывает: новые файлы, удалённые, изменившиеся, рост/падение слов.
Создаёт docs/COMPARE.md.
Запуск: python scripts/improve_compare.py
"""
import subprocess
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"


def git_log_files(n_commits: int = 1) -> dict[str, str]:
    """Получает содержимое md-файлов из HEAD~n."""
    result = {}
    try:
        # Список файлов в предыдущем коммите
        ls = subprocess.run(
            ["git", "ls-tree", "-r", "--name-only", f"HEAD~{n_commits}"],
            cwd=ROOT, capture_output=True, text=True
        )
        for line in ls.stdout.splitlines():
            if line.startswith("docs/") and line.endswith(".md"):
                show = subprocess.run(
                    ["git", "show", f"HEAD~{n_commits}:{line}"],
                    cwd=ROOT, capture_output=True, text=True
                )
                result[line] = show.stdout
    except Exception:
        pass
    return result


def word_count(text: str) -> int:
    return len(text.split())


def main():
    print("Сравниваю с предыдущим коммитом...")

    old_files = git_log_files(1)
    new_files = {}
    for f in sorted(DOCS.rglob("*.md")):
        rel = str(f.relative_to(ROOT))
        new_files[rel] = f.read_text(encoding="utf-8")

    added   = sorted(k for k in new_files if k not in old_files)
    removed = sorted(k for k in old_files if k not in new_files)
    changed = []
    for k in new_files:
        if k in old_files and new_files[k] != old_files[k]:
            old_w = word_count(old_files[k])
            new_w = word_count(new_files[k])
            diff  = new_w - old_w
            changed.append((k, old_w, new_w, diff))

    changed.sort(key=lambda x: abs(x[3]), reverse=True)

    total_old = sum(word_count(t) for t in old_files.values())
    total_new = sum(word_count(t) for t in new_files.values())

    lines = [
        "# Сравнение с предыдущим коммитом\n",
        f"**Файлов было:** {len(old_files)}  **стало:** {len(new_files)}  ",
        f"**Слов было:** {total_old:,}  **стало:** {total_new:,}  "
        f"**Δ:** {total_new - total_old:+,}\n",

        f"\n## Новые файлы ({len(added)})\n",
    ]
    for f in added[:40]:
        w = word_count(new_files[f])
        lines.append(f"- `{f}` ({w} слов)")
    if len(added) > 40:
        lines.append(f"_...и ещё {len(added)-40}_")

    lines += [f"\n## Удалённые файлы ({len(removed)})\n"]
    for f in removed[:20]:
        lines.append(f"- `{f}`")

    lines += [f"\n## Изменившиеся файлы ({len(changed)}) — топ по Δ слов\n",
              "| Файл | Было | Стало | Δ |",
              "|------|------|-------|---|"]
    for f, old_w, new_w, diff in changed[:30]:
        sign = "+" if diff >= 0 else ""
        short = f.split("/")[-1]
        lines.append(f"| `{short}` | {old_w} | {new_w} | {sign}{diff} |")

    out = DOCS / "COMPARE.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  новых: {len(added)}, удалённых: {len(removed)}, изменённых: {len(changed)}")


if __name__ == "__main__":
    main()
