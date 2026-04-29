"""
improve_schedule.py — строит расписание проекта из ACTION_ITEMS и временных маркеров.
Группирует задачи по кварталам/месяцам, строит Gantt-подобную таблицу.
Создаёт docs/SCHEDULE.md.
Запуск: python scripts/improve_schedule.py
"""
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

# Временные маркеры и их привязка к кварталам
TIME_PATTERNS = [
    (r'(?:через\s+)?(\d+)[–\-](\d+)\s*месяц[а-я]*',       "диапазон_мес"),
    (r'(?:через\s+)?(\d+)\s*месяц[а-я]*',                  "срок_мес"),
    (r'(?:через\s+)?(\d+)\s*недел[а-я]+',                  "срок_нед"),
    (r'q([1-4])\s*20(\d\d)',                                "квартал"),
    (r'20(\d\d)\s*(?:год|г\.)',                             "год"),
    (r'(?:итерация|sprint|фаза)\s*(\d+)',                   "итерация"),
]

PHASES = {
    "Q1 2025": "Исследование и планирование",
    "Q2 2025": "Контакты с авторами",
    "Q3 2025": "Прототип Knowledge OS",
    "Q4 2025": "Интеграция и тестирование",
    "Q1 2026": "MVP-релиз",
    "Q2 2026": "Масштабирование",
}

# Задачи из документов — по категориям
TASK_SOURCES = {
    "Исследование": [
        "docs/01-svyazi/01-executive-summary.md",
        "docs/01-svyazi/03-component-catalog.md",
    ],
    "Архитектура": [
        "docs/01-svyazi/09-architectural-gaps.md",
        "docs/01-svyazi/11-integration-contracts.md",
    ],
    "Контакты": [
        "docs/01-svyazi/13-contacts.md",
        "docs/CONTACTS.md",
    ],
    "MVP": [
        "docs/01-svyazi/07-mvp-planning.md",
        "docs/01-svyazi/12-roadmap.md",
    ],
}

# Ключевые вехи проекта
MILESTONES = [
    ("2024-Q4", "✅ Исследование компонентов завершено",      True),
    ("2024-Q4", "✅ Архитектура Svyazi 2.0 задокументирована", True),
    ("2025-Q1", "✅ Интеграционные контракты описаны",         True),
    ("2025-Q1", "⬜ Написать авторам AgentFS, Yodoca, NGT",   False),
    ("2025-Q2", "⬜ Получить согласие на сотрудничество",      False),
    ("2025-Q2", "⬜ Создать рабочее окружение Knowledge OS",   False),
    ("2025-Q3", "⬜ Прототип ансамбля (Svyazi + CardIndex)",   False),
    ("2025-Q3", "⬜ Тестирование на реальных данных",          False),
    ("2025-Q4", "⬜ Интеграция SENTINEL + MCP Tool Search",    False),
    ("2026-Q1", "⬜ Публичный MVP-релиз на GitHub",            False),
]


def extract_tasks_from_file(fpath: str) -> list[str]:
    p = ROOT / fpath
    if not p.exists():
        return []
    text = p.read_text(encoding="utf-8")
    tasks = []
    # Ненумерованные задачи
    for m in re.finditer(r'^[-*]\s+(.{15,120})', text, re.MULTILINE):
        t = m.group(1).strip()
        if any(w in t.lower() for w in ["создать","реализ","написать","разработ","протестир","интегрир"]):
            tasks.append(t[:100])
    return tasks[:5]


def gantt_bar(start_q: int, duration_q: int, total_q: int = 8) -> str:
    bar = list("░" * total_q)
    for i in range(start_q, min(start_q + duration_q, total_q)):
        bar[i] = "█"
    return "".join(bar)


def main():
    print("Строю расписание проекта...")

    lines = [
        "# Расписание проекта\n",
        "_Дорожная карта с вехами и задачами по кварталам._\n",

        "## Ключевые вехи\n",
        "| Срок | Веха | Статус |",
        "|------|------|--------|",
    ]

    for period, milestone, done in MILESTONES:
        status = "✅ Выполнено" if done else "⬜ Планируется"
        lines.append(f"| **{period}** | {milestone} | {status} |")

    # Gantt-подобная таблица
    quarters = ["Q4'24", "Q1'25", "Q2'25", "Q3'25", "Q4'25", "Q1'26", "Q2'26", "Q3'26"]
    lines += [
        "\n## Gantt-диаграмма\n",
        "```",
        "Фаза                    | " + " | ".join(quarters),
        "------------------------|" + "|".join("-" * 7 for _ in quarters),
        f"{'Исследование':<24}| {'██░░░░░░':^7}| {'░░░░░░░':^7}| {'░░░░░░░':^7}| {'░░░░░░░':^7}| {'░░░░░░░':^7}| {'░░░░░░░':^7}| {'░░░░░░░':^7}| {'░░░░░░░':^7}",
        f"{'Контакты':<24}| {'░░██░░░░':^7}| {'████░░░':^7}| {'░░░░░░░':^7}| {'░░░░░░░':^7}| {'░░░░░░░':^7}| {'░░░░░░░':^7}| {'░░░░░░░':^7}| {'░░░░░░░':^7}",
        f"{'Прототип Knowledge OS':<24}| {'░░░░░░░░':^7}| {'░░░░███':^7}| {'████░░░':^7}| {'░░░░░░░':^7}| {'░░░░░░░':^7}| {'░░░░░░░':^7}| {'░░░░░░░':^7}| {'░░░░░░░':^7}",
        f"{'Интеграция':<24}| {'░░░░░░░░':^7}| {'░░░░░░░':^7}| {'░░░████':^7}| {'████░░░':^7}| {'░░░░░░░':^7}| {'░░░░░░░':^7}| {'░░░░░░░':^7}| {'░░░░░░░':^7}",
        f"{'MVP-релиз':<24}| {'░░░░░░░░':^7}| {'░░░░░░░':^7}| {'░░░░░░░':^7}| {'░░░████':^7}| {'████░░░':^7}| {'░░░░░░░':^7}| {'░░░░░░░':^7}| {'░░░░░░░':^7}",
        f"{'Масштабирование':<24}| {'░░░░░░░░':^7}| {'░░░░░░░':^7}| {'░░░░░░░':^7}| {'░░░░░░░':^7}| {'░░░████':^7}| {'████████':^7}| {'████░░░':^7}| {'░░░░░░░':^7}",
        "```\n",
        "_█ = активная работа, ░ = ожидание_\n",
    ]

    # Задачи по фазам
    lines += ["\n## Задачи по фазам\n"]
    for phase_name, doc_list in TASK_SOURCES.items():
        lines.append(f"\n### {phase_name}\n")
        for doc in doc_list:
            tasks = extract_tasks_from_file(doc)
            if tasks:
                doc_short = doc.split("/")[-1].replace(".md", "")
                lines.append(f"**{doc_short}:**")
                for t in tasks:
                    lines.append(f"- [ ] {t}")
                lines.append("")

    # Текущий статус
    done_ms  = sum(1 for _, _, d in MILESTONES if d)
    total_ms = len(MILESTONES)
    pct = int(done_ms / total_ms * 100)

    lines += [
        "## Текущий статус\n",
        f"- Вех выполнено: **{done_ms}/{total_ms}** ({pct}%)",
        f"- Текущая фаза: **{'Контакты с авторами' if done_ms < 6 else 'Прототипирование'}**",
        f"- Следующая веха: **{next((m for _, m, d in MILESTONES if not d), 'Всё готово!')}**",
    ]

    out = DOCS / "SCHEDULE.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  вех: {total_ms}, выполнено: {done_ms}")


if __name__ == "__main__":
    main()
