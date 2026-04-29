"""
improve_progress.py — трекер прогресса MVP-проекта.
Извлекает чеклисты [ ] и [x] из docs/, группирует по теме,
считает % выполнения. Создаёт docs/PROGRESS.md.
Запуск: python scripts/improve_progress.py
"""
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

SKIP = {"PROGRESS.md", "ACTION_ITEMS.md", "MISSING.md", "VALIDATION.md"}

PHASE_KEYWORDS = {
    "Фаза 1: Исследование":  ["исследован", "анализ", "изучен", "оценк", "research"],
    "Фаза 2: Контакты":      ["написать", "связаться", "договорить", "contact", "outreach"],
    "Фаза 3: Прототип":      ["прототип", "mvp", "реализ", "implement", "build"],
    "Фаза 4: Интеграция":    ["интеграц", "контракт", "api", "соединить", "integrate"],
    "Фаза 5: Запуск":        ["запуск", "релиз", "deploy", "launch", "production"],
}

MVP_MILESTONES = [
    ("Определена архитектура Svyazi 2.0",         True),
    ("Составлен каталог 20+ компонентов",          True),
    ("Выявлены 5 ансамблей",                       True),
    ("Описаны интеграционные контракты",           True),
    ("Составлены контакты авторов",                True),
    ("Написаны авторам ключевых компонентов",      False),
    ("Получены ответы от авторов",                 False),
    ("Создан рабочий прототип Knowledge OS",       False),
    ("Пройдено тестирование ансамбля",             False),
    ("Опубликован MVP на GitHub",                  False),
]


def extract_checkitems(text: str) -> tuple[int, int, list[str]]:
    """Возвращает (done, total, todo_list)."""
    done_items = re.findall(r'- \[x\] (.+)', text, re.IGNORECASE)
    todo_items = re.findall(r'- \[ \] (.+)', text)
    return len(done_items), len(done_items) + len(todo_items), todo_items


def categorize(text: str) -> str:
    low = text.lower()
    for phase, kws in PHASE_KEYWORDS.items():
        if any(k in low for k in kws):
            return phase
    return "Общее"


def progress_bar(done: int, total: int, width: int = 20) -> str:
    if total == 0:
        return "░" * width + " —"
    filled = int(done / total * width)
    pct = int(done / total * 100)
    return "█" * filled + "░" * (width - filled) + f" {pct}%"


def main():
    print("Трекер прогресса MVP...")

    by_phase: dict[str, dict] = defaultdict(lambda: {"done": 0, "total": 0, "todos": []})
    all_done = all_total = 0

    for f in sorted(DOCS.rglob("*.md")):
        if f.name in SKIP:
            continue
        text = f.read_text(encoding="utf-8")
        done, total, todos = extract_checkitems(text)
        if total == 0:
            continue

        all_done  += done
        all_total += total

        for todo in todos[:5]:
            phase = categorize(todo)
            by_phase[phase]["done"]  += done
            by_phase[phase]["total"] += total
            by_phase[phase]["todos"].append((todo.strip()[:100], str(f.relative_to(ROOT))))

    # Milestone-прогресс
    ms_done  = sum(1 for _, done in MVP_MILESTONES if done)
    ms_total = len(MVP_MILESTONES)

    lines = [
        "# Прогресс MVP\n",
        f"_Обновлено автоматически из документов_\n",

        "## Ключевые этапы (Milestones)\n",
        f"`{progress_bar(ms_done, ms_total)}` {ms_done}/{ms_total}\n",
    ]

    for milestone, done in MVP_MILESTONES:
        mark = "✅" if done else "⬜"
        lines.append(f"{mark} {milestone}")

    # Чеклисты по фазам
    lines += [
        f"\n## Чеклисты по фазам\n",
        f"**Всего задач:** {all_total}  "
        f"**Выполнено:** {all_done}  "
        f"**Осталось:** {all_total - all_done}\n",
        f"`{progress_bar(all_done, all_total)}` — общий прогресс\n",
        "| Фаза | Прогресс | Выполнено | Всего |",
        "|------|----------|-----------|-------|",
    ]

    for phase in list(PHASE_KEYWORDS.keys()) + ["Общее"]:
        d = by_phase.get(phase)
        if not d or d["total"] == 0:
            continue
        bar = progress_bar(d["done"], d["total"], 15)
        lines.append(f"| **{phase}** | `{bar}` | {d['done']} | {d['total']} |")

    # Ближайшие задачи
    all_todos = []
    for phase, d in by_phase.items():
        for todo, fpath in d["todos"]:
            all_todos.append((phase, todo, fpath))

    if all_todos:
        lines += [
            "\n## Ближайшие задачи (открытые чеклисты)\n",
            "| Фаза | Задача | Источник |",
            "|------|--------|---------|",
        ]
        seen: set = set()
        for phase, todo, fpath in all_todos[:25]:
            key = todo[:40].lower()
            if key in seen:
                continue
            seen.add(key)
            short = fpath.split("/")[-1].replace(".md", "")[:25]
            lines.append(f"| {phase.split(':')[0]} | {todo[:60]} | `{short}` |")

    # Рекомендации
    lines += [
        "\n## Следующий шаг\n",
    ]
    next_ms = next((m for m, done in MVP_MILESTONES if not done), None)
    if next_ms:
        lines.append(f"➡️ **{next_ms}**\n")
        lines.append("Связанные документы:")
        lines.append("- [Контакты авторов](CONTACTS.md)")
        lines.append("- [MVP Planning](01-svyazi/07-mvp-planning.md)")
        lines.append("- [Roadmap](01-svyazi/12-roadmap.md)")

    out = DOCS / "PROGRESS.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  milestone: {ms_done}/{ms_total}, "
          f"чеклисты: {all_done}/{all_total}")


if __name__ == "__main__":
    main()
