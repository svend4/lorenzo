"""
improve_changelog_auto.py — автоматический changelog из git-истории.
Группирует коммиты по типу (feat/fix/docs/chore), строит версионированный лог.
Создаёт docs/CHANGELOG_AUTO.md.
Запуск: python scripts/improve_changelog_auto.py
"""
import re
import subprocess
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

COMMIT_TYPES = {
    "feat":     ("✨ Новые возможности",   0),
    "fix":      ("🐛 Исправления",         1),
    "docs":     ("📝 Документация",        2),
    "refactor": ("♻️  Рефакторинг",        3),
    "chore":    ("🔧 Технические задачи",  4),
    "test":     ("✅ Тесты",               5),
    "perf":     ("⚡ Производительность",  6),
    "style":    ("💅 Стиль",               7),
    "ci":       ("🤖 CI/CD",               8),
    "other":    ("📌 Прочее",              9),
}


def git(*args) -> str:
    r = subprocess.run(["git"] + list(args), cwd=ROOT, capture_output=True, text=True)
    return r.stdout.strip()


def parse_commits(log: str) -> list[dict]:
    commits = []
    for line in log.splitlines():
        line = line.strip()
        if not line:
            continue
        # Формат: hash|||date|||subject
        parts = line.split("|||")
        if len(parts) < 3:
            continue
        sha, date, subject = parts[0], parts[1], parts[2]

        # Conventional commits: type(scope): message
        m = re.match(r'^(\w+)(?:\(([^)]+)\))?!?:\s*(.+)$', subject)
        if m:
            ctype  = m.group(1).lower()
            scope  = m.group(2) or ""
            msg    = m.group(3)
        else:
            ctype  = "other"
            scope  = ""
            msg    = subject

        if ctype not in COMMIT_TYPES:
            ctype = "other"

        commits.append({
            "sha":   sha[:8],
            "date":  date[:10],
            "type":  ctype,
            "scope": scope,
            "msg":   msg[:120],
        })
    return commits


def group_by_month(commits: list[dict]) -> dict[str, list[dict]]:
    by_month: dict[str, list[dict]] = defaultdict(list)
    for c in commits:
        month = c["date"][:7]   # YYYY-MM
        by_month[month].append(c)
    return dict(sorted(by_month.items(), reverse=True))


def main():
    print("Генерация автоматического changelog...")

    log = git(
        "log", "--no-merges",
        "--pretty=format:%H|||%ci|||%s",
        "--max-count=200",
    )

    if not log:
        print("  нет коммитов в истории")
        commits = []
    else:
        commits = parse_commits(log)

    print(f"  коммитов: {len(commits)}")

    # Статистика по типам
    type_counts: dict[str, int] = defaultdict(int)
    for c in commits:
        type_counts[c["type"]] += 1

    by_month = group_by_month(commits)

    lines = [
        "# Changelog (авто)\n",
        f"_Сгенерировано из {len(commits)} коммитов git-истории._\n",
        "## Статистика коммитов\n",
        "| Тип | Название | Кол-во |",
        "|-----|---------|--------|",
    ]
    for ctype, (label, _) in sorted(COMMIT_TYPES.items(), key=lambda x: x[1][1]):
        count = type_counts.get(ctype, 0)
        if count > 0:
            lines.append(f"| `{ctype}` | {label} | {count} |")

    lines.append("\n## История изменений\n")

    for month, month_commits in by_month.items():
        lines.append(f"\n### {month}\n")
        by_type: dict[str, list[dict]] = defaultdict(list)
        for c in month_commits:
            by_type[c["type"]].append(c)

        for ctype, (label, order) in sorted(COMMIT_TYPES.items(), key=lambda x: x[1][1]):
            items = by_type.get(ctype, [])
            if not items:
                continue
            lines.append(f"**{label}**\n")
            for c in items:
                scope = f"({c['scope']}) " if c["scope"] else ""
                lines.append(f"- {scope}{c['msg']} `{c['sha']}`")
            lines.append("")

    lines += [
        "---\n",
        "_Changelog генерируется автоматически из conventional commits._\n",
        "_Ручной changelog: `docs/CHANGELOG.md` (если существует)._\n",
    ]

    out = DOCS / "CHANGELOG_AUTO.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    if by_month:
        print(f"  месяцев: {len(by_month)}, последний: {list(by_month.keys())[0]}")


if __name__ == "__main__":
    main()
