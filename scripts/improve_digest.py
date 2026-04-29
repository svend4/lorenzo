"""
improve_digest.py — дайджест недавних изменений репозитория.
Собирает из git log: новые файлы, изменённые, ключевые коммиты.
Создаёт docs/DIGEST.md.
Запуск: python scripts/improve_digest.py
"""
import re
import subprocess
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"


def git_log(n: int = 10) -> list[dict]:
    """Последние N коммитов."""
    result = subprocess.run(
        ["git", "log", f"-{n}", "--pretty=format:%H|%ad|%s", "--date=short"],
        cwd=ROOT, capture_output=True, text=True
    )
    commits = []
    for line in result.stdout.splitlines():
        parts = line.split("|", 2)
        if len(parts) == 3:
            commits.append({"hash": parts[0][:8], "date": parts[1], "msg": parts[2]})
    return commits


def files_in_commit(sha: str) -> list[str]:
    result = subprocess.run(
        ["git", "diff-tree", "--no-commit-id", "-r", "--name-only", sha],
        cwd=ROOT, capture_output=True, text=True
    )
    return [l.strip() for l in result.stdout.splitlines() if l.endswith(".md")]


def git_stats_since(n_commits: int = 1) -> dict:
    """Статистика изменений за последние n коммитов."""
    try:
        diff = subprocess.run(
            ["git", "diff", f"HEAD~{n_commits}", "HEAD", "--stat"],
            cwd=ROOT, capture_output=True, text=True
        )
        text = diff.stdout
        m_files = re.search(r'(\d+) files? changed', text)
        m_ins   = re.search(r'(\d+) insertions?', text)
        m_del   = re.search(r'(\d+) deletions?', text)
        return {
            "files":      int(m_files.group(1)) if m_files else 0,
            "insertions": int(m_ins.group(1))   if m_ins   else 0,
            "deletions":  int(m_del.group(1))   if m_del   else 0,
        }
    except Exception:
        return {"files": 0, "insertions": 0, "deletions": 0}


def new_files_since(n_commits: int = 3) -> list[str]:
    """Файлы, добавленные за последние n коммитов."""
    result = subprocess.run(
        ["git", "diff", f"HEAD~{n_commits}", "HEAD", "--name-status"],
        cwd=ROOT, capture_output=True, text=True
    )
    new_files = []
    for line in result.stdout.splitlines():
        if line.startswith("A\t") and line.endswith(".md"):
            new_files.append(line[2:].strip())
    return new_files


def count_scripts() -> int:
    return len(list((ROOT / "scripts").glob("improve_*.py")))


def main():
    print("Генерация дайджеста изменений...")
    today = date.today().isoformat()

    commits = git_log(15)
    stats_1 = git_stats_since(1)
    stats_3 = git_stats_since(3)
    new_md  = new_files_since(3)

    # Группируем новые файлы по разделам
    by_sec: dict[str, list] = {}
    for f in new_md:
        parts = Path(f).parts
        sec = parts[1] if len(parts) > 2 else "root"
        by_sec.setdefault(sec, []).append(Path(f).name)

    lines = [
        "# Дайджест изменений\n",
        f"_Обновлено: {today}_\n",

        "## Последний коммит\n",
    ]

    if commits:
        c = commits[0]
        lines += [
            f"**{c['date']}** — `{c['hash']}`",
            f"> {c['msg']}\n",
            f"Изменено файлов: **{stats_1['files']}** "
            f"(+{stats_1['insertions']} / -{stats_1['deletions']} строк)\n",
        ]

    lines += [
        "## Последние 3 коммита — итого\n",
        f"- Изменено файлов: **{stats_3['files']}**",
        f"- Добавлено строк: **+{stats_3['insertions']}**",
        f"- Удалено строк: **-{stats_3['deletions']}**",
        f"- Новых md-файлов: **{len(new_md)}**\n",
    ]

    if new_md:
        lines.append("## Новые документы\n")
        for sec, files in sorted(by_sec.items()):
            lines.append(f"**{sec}:**")
            for f in files[:10]:
                lines.append(f"- `{f}`")
            lines.append("")

    lines += [
        "## История коммитов (последние 15)\n",
        "| Дата | Hash | Описание |",
        "|------|------|---------|",
    ]
    for c in commits:
        msg = c["msg"][:70]
        lines.append(f"| {c['date']} | `{c['hash']}` | {msg} |")

    # Мета-статистика
    total_md = len(list(DOCS.rglob("*.md")))
    scripts  = count_scripts()
    lines += [
        "\n## Текущее состояние репозитория\n",
        f"| Параметр | Значение |",
        f"|----------|---------|",
        f"| Документов `.md` | **{total_md}** |",
        f"| Скриптов обработки | **{scripts}** |",
        f"| Последнее обновление | **{today}** |",
    ]

    out = DOCS / "DIGEST.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  коммитов: {len(commits)}, новых файлов: {len(new_md)}")


if __name__ == "__main__":
    main()
