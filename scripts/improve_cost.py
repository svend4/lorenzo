"""
improve_cost.py — оценка стоимости разработки MVP.
Извлекает временные оценки из документов, конвертирует в человеко-часы,
рассчитывает ориентировочный бюджет.
Создаёт docs/COST.md.
Запуск: python scripts/improve_cost.py
"""
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

SKIP = {"COST.md", "SCHEDULE.md", "KPI.md"}

# Часовые ставки (USD/час) по ролям
RATES = {
    "Senior Python Dev":   85,
    "AI/ML Engineer":     110,
    "DevOps":              75,
    "Tech Writer":         45,
    "Project Manager":     65,
}

# Компоненты MVP и оценки в человеко-неделях (ч/н)
MVP_COMPONENTS = [
    ("Knowledge OS ядро",          "Senior Python Dev",   3),
    ("CardIndex интеграция",       "Senior Python Dev",   2),
    ("AgentFS подключение",        "Senior Python Dev",   1),
    ("Yodoca memory layer",        "AI/ML Engineer",      3),
    ("NGT граф памяти",            "AI/ML Engineer",      2),
    ("SENTINEL безопасность",      "Senior Python Dev",   2),
    ("MCP Tool Search",            "Senior Python Dev",   1),
    ("Rufler оркестрация",         "AI/ML Engineer",      2),
    ("MCP протокол адаптер",       "Senior Python Dev",   2),
    ("Документация API",           "Tech Writer",         1),
    ("CI/CD и тесты",              "DevOps",              2),
    ("Project management",         "Project Manager",     4),
]

HOURS_PER_WEEK = 40


def extract_time_estimates(text: str) -> list[tuple[str, int]]:
    """Извлекает оценки времени из текста."""
    estimates = []
    # "X-Y месяцев" → берём среднее
    for m in re.finditer(r'(\d+)[–\-](\d+)\s*месяц[а-я]*', text):
        avg = (int(m.group(1)) + int(m.group(2))) // 2
        context = text[max(0, m.start()-60):m.end()+60].replace('\n', ' ').strip()
        estimates.append((context[:100], avg * 4))  # месяц ≈ 4 недели
    # "X месяцев"
    for m in re.finditer(r'(?<!\d)(\d+)\s*месяц[а-я]*(?!\s*\d)', text):
        n = int(m.group(1))
        if 1 <= n <= 24:
            context = text[max(0, m.start()-40):m.end()+40].replace('\n', ' ').strip()
            estimates.append((context[:100], n * 4))
    # "X недель"
    for m in re.finditer(r'(\d+)\s*недел[а-я]+', text):
        n = int(m.group(1))
        if 1 <= n <= 52:
            context = text[max(0, m.start()-40):m.end()+40].replace('\n', ' ').strip()
            estimates.append((context[:100], n))
    return estimates[:10]


def main():
    print("Оценка стоимости разработки MVP...")

    # Считаем из таблицы компонентов
    total_weeks  = sum(weeks for _, _, weeks in MVP_COMPONENTS)
    total_hours  = total_weeks * HOURS_PER_WEEK
    total_cost   = sum(RATES[role] * weeks * HOURS_PER_WEEK
                       for _, role, weeks in MVP_COMPONENTS)

    by_role: dict[str, dict] = defaultdict(lambda: {"weeks": 0, "cost": 0})
    for comp, role, weeks in MVP_COMPONENTS:
        by_role[role]["weeks"] += weeks
        by_role[role]["cost"]  += RATES[role] * weeks * HOURS_PER_WEEK

    # Извлекаем оценки из документов
    doc_estimates = []
    for f in sorted(DOCS.rglob("*.md")):
        if f.name in SKIP:
            continue
        text = f.read_text(encoding="utf-8")
        for ctx, weeks in extract_time_estimates(text):
            doc_estimates.append((str(f.relative_to(ROOT)), ctx, weeks))

    lines = [
        "# Оценка стоимости MVP\n",
        "_Ориентировочные цифры на основе документации проекта._\n",

        "## Итого\n",
        f"| Параметр | Значение |",
        f"|----------|---------|",
        f"| Человеко-недель | **{total_weeks}** |",
        f"| Человеко-часов | **{total_hours:,}** |",
        f"| Бюджет (USD) | **${total_cost:,}** |",
        f"| Календарный срок | **~{total_weeks // 4}-{total_weeks // 3} месяцев** |",
        f"| Команда | **{len(RATES)} ролей** |\n",

        "## По компонентам\n",
        "| Компонент | Роль | Недель | Стоимость USD |",
        "|-----------|------|--------|--------------|",
    ]
    for comp, role, weeks in sorted(MVP_COMPONENTS, key=lambda x: -x[2]):
        cost = RATES[role] * weeks * HOURS_PER_WEEK
        lines.append(f"| {comp} | {role} | {weeks} | ${cost:,} |")
    lines.append(f"| **ИТОГО** | | **{total_weeks}** | **${total_cost:,}** |")

    lines += [
        "\n## По ролям\n",
        "| Роль | Ставка USD/ч | Недель | Итого USD |",
        "|------|-------------|--------|----------|",
    ]
    for role, rate in RATES.items():
        d = by_role[role]
        if d["weeks"] == 0:
            continue
        lines.append(f"| {role} | ${rate} | {d['weeks']} | ${d['cost']:,} |")

    # Сценарии
    lines += [
        "\n## Сценарии\n",
        "| Сценарий | Команда | Срок | Бюджет |",
        "|----------|---------|------|--------|",
        f"| Минимальный (solo) | 1 разработчик | ~18 мес | ${total_cost // 3:,} |",
        f"| Оптимальный | 3 человека | ~8 мес | ${total_cost // 2:,} |",
        f"| Ускоренный | 5 человек | ~5 мес | ${total_cost:,} |",
        "\n_Минимальный сценарий: open source + личное время авторов компонентов._\n",
    ]

    # Временные оценки из документов
    if doc_estimates:
        lines += [
            "## Временные оценки из документов\n",
            "| Источник | Контекст | Недель |",
            "|----------|----------|--------|",
        ]
        seen: set = set()
        for src, ctx, weeks in sorted(doc_estimates, key=lambda x: -x[2])[:15]:
            key = ctx[:30].lower()
            if key in seen:
                continue
            seen.add(key)
            short = src.split("/")[-1].replace(".md", "")[:20]
            lines.append(f"| `{short}` | {ctx[:60]}… | {weeks} |")

    lines += [
        "\n## Допущения\n",
        "- Рабочая неделя: 40 часов",
        "- Ставки: рыночные для независимых разработчиков (Европа/США)",
        "- Open Source компоненты: бесплатны",
        "- Сервера и инфраструктура: не включены (~$200-500/мес)",
        "- Авторы OSS-компонентов могут участвовать добровольно → снижает бюджет",
    ]

    out = DOCS / "COST.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  итого: {total_weeks} чел-недель, ${total_cost:,}")


if __name__ == "__main__":
    main()
