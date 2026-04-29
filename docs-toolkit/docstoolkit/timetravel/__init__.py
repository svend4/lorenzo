"""Time-travel queries: query состояние корпуса на любую точку git-истории.

Использование:
    from docstoolkit.timetravel import (
        snapshot_at, list_commits, diff_between, find_introduced,
    )

    # Состояние файла на конкретный commit
    text = snapshot_at("docs/HEALTH.md", "abc1234")

    # Список коммитов которые трогали файл
    commits = list_commits("docs/templates/rfc.md", limit=20)

    # Diff между двумя точками
    diff = diff_between("docs/01-svyazi/", "main~10", "main")

    # Когда был представлен какой-то токен (binary search через git history)
    intro = find_introduced("Yodoca", file_pattern="docs/")
"""
from docstoolkit.timetravel.git import (
    snapshot_at, list_commits, diff_between, find_introduced,
    list_dates, file_history,
)

__all__ = [
    "snapshot_at", "list_commits", "diff_between", "find_introduced",
    "list_dates", "file_history",
]
