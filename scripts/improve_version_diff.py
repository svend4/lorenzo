"""
improve_version_diff.py — показывает содержательные изменения docs/ между коммитами.

В отличие от git diff показывает:
  - какие темы добавлены/удалены (по заголовкам ##)
  - сколько слов добавлено/удалено
  - какие файлы сильнее всего изменились

Создаёт docs/VERSION_DIFF.md.
Запуск:
    python scripts/improve_version_diff.py
    python scripts/improve_version_diff.py --from HEAD~5 --to HEAD
    python scripts/improve_version_diff.py --from v1.0 --to v2.0
    python scripts/improve_version_diff.py --last 7   # за последние 7 коммитов
"""
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TODAY = date.today().isoformat()

REV_FROM = "HEAD~10"
REV_TO = "HEAD"

if "--from" in sys.argv:
    idx = sys.argv.index("--from")
    if idx + 1 < len(sys.argv):
        REV_FROM = sys.argv[idx + 1]

if "--to" in sys.argv:
    idx = sys.argv.index("--to")
    if idx + 1 < len(sys.argv):
        REV_TO = sys.argv[idx + 1]

if "--last" in sys.argv:
    idx = sys.argv.index("--last")
    if idx + 1 < len(sys.argv):
        REV_FROM = f"HEAD~{sys.argv[idx + 1]}"
        REV_TO = "HEAD"


def _git_show(rev: str, path: str) -> str:
    """Получает содержимое файла на определённом коммите."""
    result = subprocess.run(
        ["git", "show", f"{rev}:{path}"],
        cwd=ROOT, capture_output=True, text=True,
    )
    return result.stdout if result.returncode == 0 else ""


def _changed_docs_files(rev_from: str, rev_to: str) -> list[str]:
    """Список .md файлов в docs/, изменившихся между ревизиями."""
    result = subprocess.run(
        ["git", "diff", "--name-only", rev_from, rev_to, "--", "docs/"],
        cwd=ROOT, capture_output=True, text=True,
    )
    if result.returncode != 0:
        return []
    return [f for f in result.stdout.strip().split('\n')
            if f and f.endswith('.md')]


def _extract_headings(text: str) -> set[str]:
    return set(re.findall(r'^#{1,3}\s+(.+)$', text, re.MULTILINE))


def _word_count(text: str) -> int:
    clean = re.sub(r'```.*?```', ' ', text, flags=re.DOTALL)
    clean = re.sub(r'[^а-яёa-zA-Z\s]', ' ', clean)
    return len(clean.split())


def _resolve_rev(rev: str) -> str:
    """Разворачивает ревизию в хэш."""
    result = subprocess.run(
        ["git", "rev-parse", "--short", rev],
        cwd=ROOT, capture_output=True, text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else rev


def main() -> None:
    print("📊 improve_version_diff.py — diff базы знаний между версиями")
    print(f"   От: {REV_FROM}  До: {REV_TO}\n")

    hash_from = _resolve_rev(REV_FROM)
    hash_to = _resolve_rev(REV_TO)

    if not hash_from or not hash_to:
        print("  ❌ Не удалось разрешить ревизии")
        print("  Убедитесь, что git-репозиторий содержит указанные коммиты")
        # Создаём пустой отчёт
        out = DOCS / "VERSION_DIFF.md"
        out.write_text(
            f"# Diff базы знаний\n\n_Обновлено: {TODAY}_\n\n"
            f"⚠️ Нет данных (ревизии не найдены: {REV_FROM} → {REV_TO})\n",
            encoding="utf-8",
        )
        return

    changed_files = _changed_docs_files(REV_FROM, REV_TO)
    print(f"  Изменённых файлов: {len(changed_files)}")

    file_stats = []
    total_added = 0
    total_removed = 0

    for rel_path in changed_files:
        old_text = _git_show(REV_FROM, rel_path)
        new_text = _git_show(REV_TO, rel_path)

        old_words = _word_count(old_text)
        new_words = _word_count(new_text)
        delta = new_words - old_words

        old_headings = _extract_headings(old_text)
        new_headings = _extract_headings(new_text)
        added_headings = new_headings - old_headings
        removed_headings = old_headings - new_headings

        status = "M"  # modified
        if not old_text:
            status = "A"  # added
        elif not new_text:
            status = "D"  # deleted

        if delta > 0:
            total_added += delta
        else:
            total_removed += abs(delta)

        file_stats.append({
            "path": rel_path,
            "status": status,
            "old_words": old_words,
            "new_words": new_words,
            "delta": delta,
            "added_headings": sorted(added_headings),
            "removed_headings": sorted(removed_headings),
        })

    file_stats.sort(key=lambda x: -abs(x["delta"]))

    lines = [
        "# Diff базы знаний между версиями\n",
        f"_Обновлено: {TODAY}_\n",
        f"**{REV_FROM}** (`{hash_from}`) → **{REV_TO}** (`{hash_to}`)\n",
        f"Изменено файлов: **{len(changed_files)}** | "
        f"Добавлено слов: **+{total_added}** | "
        f"Удалено слов: **-{total_removed}**\n",
    ]

    added_files = [f for f in file_stats if f["status"] == "A"]
    deleted_files = [f for f in file_stats if f["status"] == "D"]
    modified_files = [f for f in file_stats if f["status"] == "M"]

    if added_files:
        lines += [f"\n## ✅ Новые файлы ({len(added_files)})\n"]
        for f in added_files:
            lines.append(f"- `{f['path']}` (+{f['new_words']} слов)")

    if deleted_files:
        lines += [f"\n## ❌ Удалённые файлы ({len(deleted_files)})\n"]
        for f in deleted_files:
            lines.append(f"- `{f['path']}` (-{f['old_words']} слов)")

    if modified_files:
        lines += [
            f"\n## 📝 Изменённые файлы ({len(modified_files)})\n",
            "| Файл | Δ слов | Добавленные темы | Удалённые темы |",
            "|------|--------|------------------|----------------|",
        ]
        for f in modified_files:
            delta_str = f"+{f['delta']}" if f['delta'] > 0 else str(f['delta'])
            added_h = ', '.join(f['added_headings'][:3])
            removed_h = ', '.join(f['removed_headings'][:3])
            if len(f['added_headings']) > 3:
                added_h += f" +{len(f['added_headings'])-3}"
            if len(f['removed_headings']) > 3:
                removed_h += f" +{len(f['removed_headings'])-3}"
            lines.append(
                f"| `{f['path']}` | {delta_str} | {added_h or '—'} | {removed_h or '—'} |"
            )

    out = DOCS / "VERSION_DIFF.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  +{total_added} / -{total_removed} слов")


if __name__ == "__main__":
    main()
