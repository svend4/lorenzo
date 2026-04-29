"""
improve_changelog.py — генерирует CHANGELOG из git-истории репозитория.
Группирует коммиты по типам (feat/fix/chore/improve) и датам.
Создаёт docs/CHANGELOG.md и CHANGELOG.md в корне.
Запуск: python scripts/improve_changelog.py
"""
import re
import subprocess
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent

COMMIT_TYPES = {
    "feat":     ("✨", "Новые функции"),
    "fix":      ("🐛", "Исправления"),
    "improve":  ("⚡", "Улучшения"),
    "chore":    ("🔧", "Обслуживание"),
    "docs":     ("📝", "Документация"),
    "refactor": ("♻️",  "Рефакторинг"),
    "test":     ("🧪", "Тесты"),
    "ci":       ("🤖", "CI/CD"),
    "style":    ("💅", "Стиль"),
    "perf":     ("🚀", "Производительность"),
}


def get_git_log() -> list[dict]:
    """Получает историю коммитов через git log."""
    try:
        result = subprocess.run(
            ["git", "log", "--pretty=format:%H|%ai|%s|%b", "--no-merges"],
            capture_output=True, text=True, cwd=ROOT
        )
        commits = []
        for line in result.stdout.strip().split('\n'):
            if not line.strip():
                continue
            parts = line.split('|', 3)
            if len(parts) < 3:
                continue
            sha, date, subject = parts[0], parts[1], parts[2]
            body = parts[3] if len(parts) > 3 else ""
            commits.append({
                "sha": sha[:8],
                "date": date[:10],
                "subject": subject.strip(),
                "body": body.strip(),
            })
        return commits
    except Exception as e:
        print(f"  git log ошибка: {e}")
        return []


def parse_commit_type(subject: str) -> tuple[str, str]:
    """Разбирает тип коммита и описание из conventional commits."""
    m = re.match(r'^(feat|fix|improve|chore|docs|refactor|test|ci|style|perf)'
                 r'(?:\([^)]+\))?:\s*(.+)$', subject, re.IGNORECASE)
    if m:
        return m.group(1).lower(), m.group(2).strip()
    return "chore", subject


def group_by_date(commits: list[dict]) -> dict[str, list[dict]]:
    """Группирует коммиты по дате."""
    grouped: dict[str, list[dict]] = defaultdict(list)
    for c in commits:
        grouped[c["date"]].append(c)
    return grouped


def format_stats(commits: list[dict]) -> str:
    """Статистика по типам коммитов."""
    type_counts: dict[str, int] = defaultdict(int)
    for c in commits:
        t, _ = parse_commit_type(c["subject"])
        type_counts[t] += 1
    parts = [f"{COMMIT_TYPES.get(t, ('📌',''))[0]} {t}: {n}"
             for t, n in sorted(type_counts.items(), key=lambda x: -x[1])]
    return " | ".join(parts)


def main():
    print("Генерация CHANGELOG из git-истории...")
    commits = get_git_log()
    print(f"  коммитов найдено: {len(commits)}")

    if not commits:
        print("  нет коммитов, выходим")
        return

    by_date = group_by_date(commits)
    lines = [
        "# CHANGELOG\n",
        f"Всего коммитов: **{len(commits)}**  \n"
        f"Статистика: {format_stats(commits)}\n",
    ]

    for date in sorted(by_date.keys(), reverse=True):
        day_commits = by_date[date]
        lines.append(f"\n## {date} ({len(day_commits)} коммитов)\n")

        # Группируем по типу внутри дня
        by_type: dict[str, list[dict]] = defaultdict(list)
        for c in day_commits:
            t, desc = parse_commit_type(c["subject"])
            by_type[t].append({"desc": desc, "sha": c["sha"], "body": c["body"]})

        for commit_type, type_commits in sorted(by_type.items()):
            emoji, label = COMMIT_TYPES.get(commit_type, ("📌", commit_type))
            lines.append(f"### {emoji} {label}\n")
            for c in type_commits:
                lines.append(f"- {c['desc']} _{c['sha']}_")
                if c["body"] and len(c["body"]) > 10:
                    # Первая строка тела
                    body_line = c["body"].split('\n')[0][:100]
                    lines.append(f"  > {body_line}")

    # Записываем в docs/ и в корень
    content = "\n".join(lines) + "\n"
    (ROOT / "docs" / "CHANGELOG.md").write_text(content, encoding="utf-8")
    (ROOT / "CHANGELOG.md").write_text(content, encoding="utf-8")
    print(f"  wrote: docs/CHANGELOG.md")
    print(f"  wrote: CHANGELOG.md")


if __name__ == "__main__":
    main()
