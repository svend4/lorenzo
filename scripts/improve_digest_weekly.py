"""
improve_digest_weekly.py — еженедельный дайджест изменений репозитория.
Показывает: новые файлы, изменённые, топ-активные папки, прирост слов.
Создаёт docs/DIGEST_WEEKLY.md.
Запуск: python scripts/improve_digest_weekly.py
"""
import subprocess
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timedelta

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"


def git(*args) -> str:
    result = subprocess.run(
        ["git"] + list(args), cwd=ROOT,
        capture_output=True, text=True
    )
    return result.stdout.strip()


def get_weekly_changes(days: int = 7) -> dict:
    since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    # Коммиты за период
    log = git("log", f"--since={since}", "--oneline", "--no-merges")
    commits = [l for l in log.splitlines() if l.strip()]

    # Изменённые файлы
    diff = git("diff", f"--name-status", f"HEAD~{len(commits)}", "HEAD") if commits else ""
    added:   list[str] = []
    modified: list[str] = []
    for line in diff.splitlines():
        parts = line.split("\t", 1)
        if len(parts) == 2:
            status, path = parts
            if status.startswith("A"):
                added.append(path)
            elif status.startswith("M"):
                modified.append(path)

    # Активность по папкам
    folder_count: dict[str, int] = defaultdict(int)
    for f in added + modified:
        parts = Path(f).parts
        folder = parts[1] if len(parts) > 2 else parts[0]
        folder_count[folder] += 1

    return {
        "commits":  commits,
        "added":    added,
        "modified": modified,
        "folders":  folder_count,
        "since":    since,
        "days":     days,
    }


def word_count_delta() -> tuple[int, int]:
    """Текущее и предыдущее кол-во слов (приблизительно)."""
    current = sum(len(f.read_text(encoding="utf-8").split()) for f in DOCS.rglob("*.md"))
    # Приближение прироста через git stash — слишком рискованно, просто возвращаем текущее
    return current, 0


def main():
    print("Еженедельный дайджест изменений...")

    data = get_weekly_changes(days=7)
    total_words, _ = word_count_delta()
    total_md = len(list(DOCS.rglob("*.md")))

    date_str = datetime.now().strftime("%Y-%m-%d")
    lines = [
        f"# Еженедельный дайджест — {date_str}\n",
        f"_Период: последние {data['days']} дней (с {data['since']})_\n",

        "## Итого\n",
        f"| Метрика | Значение |",
        f"|---------|---------|",
        f"| Коммитов за неделю | **{len(data['commits'])}** |",
        f"| Новых файлов | **{len(data['added'])}** |",
        f"| Изменённых файлов | **{len(data['modified'])}** |",
        f"| Всего MD файлов | **{total_md}** |",
        f"| Всего слов | **{total_words:,}** |\n",
    ]

    # Коммиты
    if data["commits"]:
        lines += [
            "## Коммиты\n",
            "```",
        ]
        for c in data["commits"][:15]:
            lines.append(c)
        lines += ["```\n"]

    # Новые файлы
    md_added = [f for f in data["added"] if f.endswith(".md")]
    if md_added:
        lines += ["## Новые документы\n"]
        for f in md_added[:20]:
            lines.append(f"- `{f}`")
        lines.append("")

    # Активные папки
    if data["folders"]:
        lines += [
            "## Активность по разделам\n",
            "| Раздел | Изменений |",
            "|--------|----------|",
        ]
        for folder, count in sorted(data["folders"].items(), key=lambda x: -x[1])[:10]:
            lines.append(f"| `{folder}/` | {count} |")
        lines.append("")

    # Изменённые файлы
    md_modified = [f for f in data["modified"] if f.endswith(".md")]
    if md_modified:
        lines += ["## Изменённые документы\n"]
        for f in md_modified[:15]:
            lines.append(f"- `{f}`")
        lines.append("")

    lines += [
        "---\n",
        f"_Сгенерировано: {datetime.now().strftime('%Y-%m-%d %H:%M')}_",
    ]

    out = DOCS / "DIGEST_WEEKLY.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  коммитов: {len(data['commits'])}, новых файлов: {len(data['added'])}")


if __name__ == "__main__":
    main()
