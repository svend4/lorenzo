"""
improve_narrative.py — строит нарративную линию проекта.
Извлекает: ключевые решения, этапы, цитаты-выводы и строит связный рассказ.
Создаёт docs/NARRATIVE.md.
Запуск: python scripts/improve_narrative.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

SKIP = {"NARRATIVE.md", "DECISIONS.md", "TIMELINE.md", "CHANGELOG.md"}

# Паттерны для извлечения нарративных точек
NARRATIVE_PATTERNS = [
    # Этапы/фазы
    (r'(?:первый|первая|первое|начальный)\s+(?:этап|фаза|шаг|итерация)[:\s]+([^.\n]{20,200})',
     "🚀 Старт"),
    (r'(?:второй|второй|следующий)\s+(?:этап|фаза|шаг)[:\s]+([^.\n]{20,200})',
     "📈 Развитие"),
    (r'(?:финальный|последний|итоговый)\s+(?:этап|фаза|шаг)[:\s]+([^.\n]{20,200})',
     "🏁 Финал"),
    # Ключевые открытия
    (r'(?:ключевое|главное|важнейшее)\s+(?:открытие|вывод|решение|принцип)[:\s]+([^.\n]{20,200})',
     "💡 Вывод"),
    # MVP
    (r'mvp[:\s]+([^.\n]{20,200})',
     "🛠️ MVP"),
    # Риски
    (r'главный\s+риск[:\s]+([^.\n]{20,200})',
     "⚠️ Риск"),
    # Контакты/партнёрства
    (r'(?:написать|связаться|предложить)\s+([^.\n]{15,150})',
     "🤝 Контакт"),
    # Цели
    (r'(?:цель|задача|миссия)[:\s]+([^.\n]{20,200})',
     "🎯 Цель"),
]

# Ключевые документы для нарративной линии (в порядке истории)
NARRATIVE_DOCS = [
    "docs/01-svyazi/01-executive-summary.md",
    "docs/01-svyazi/03-component-catalog.md",
    "docs/01-svyazi/04-ensembles-overview.md",
    "docs/01-svyazi/07-mvp-planning.md",
    "docs/01-svyazi/09-architectural-gaps.md",
    "docs/01-svyazi/11-integration-contracts.md",
    "docs/01-svyazi/12-roadmap.md",
    "docs/01-svyazi/13-contacts.md",
    "docs/04-ai-collaborations/00-intro.md",
    "docs/05-habr-projects/memory/yodoca.md",
    "docs/05-habr-projects/memory/ngt-memory.md",
]

CHAPTER_TITLES = {
    "docs/01-svyazi/01-executive-summary.md":   "Глава 1: Исходная точка — Svyazi 2.0",
    "docs/01-svyazi/03-component-catalog.md":   "Глава 2: Экосистема проектов",
    "docs/01-svyazi/04-ensembles-overview.md":  "Глава 3: Ансамбли — синергия компонентов",
    "docs/01-svyazi/07-mvp-planning.md":        "Глава 4: MVP — что строим первым",
    "docs/01-svyazi/09-architectural-gaps.md":  "Глава 5: Архитектурные пробелы",
    "docs/01-svyazi/11-integration-contracts.md":"Глава 6: Контракты интеграции",
    "docs/01-svyazi/12-roadmap.md":             "Глава 7: Дорожная карта",
    "docs/01-svyazi/13-contacts.md":            "Глава 8: Команда и контакты",
    "docs/04-ai-collaborations/00-intro.md":    "Глава 9: AI-коллаборации",
    "docs/05-habr-projects/memory/yodoca.md":   "Глава 10: Yodoca — память",
    "docs/05-habr-projects/memory/ngt-memory.md":"Глава 11: NGT — граф памяти",
}


def extract_narrative_points(text: str) -> list[tuple[str, str]]:
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    points = []
    for pattern, label in NARRATIVE_PATTERNS:
        for m in re.finditer(pattern, text, re.IGNORECASE):
            val = re.sub(r'\s+', ' ', m.group(1)).strip()
            if len(val) >= 20:
                points.append((label, val[:200]))
    return points[:5]  # не более 5 точек на документ


def get_summary(text: str, max_words: int = 60) -> str:
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    text = re.sub(r'^#{1,6}\s+.*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'\s+', ' ', text).strip()
    words = text.split()
    return " ".join(words[:max_words]) + ("…" if len(words) > max_words else "")


def main():
    print("Строю нарративную линию...")

    lines = [
        "# Нарратив проекта Lorenzo\n",
        "_Связный рассказ о том, как складывается проект — "
        "от первых идей до конкретных планов._\n",
        "---\n",
    ]

    for doc_rel in NARRATIVE_DOCS:
        doc_path = ROOT / doc_rel
        if not doc_path.exists():
            continue

        text = doc_path.read_text(encoding="utf-8")
        chapter = CHAPTER_TITLES.get(doc_rel, doc_rel.split("/")[-1])
        summary = get_summary(text)
        points  = extract_narrative_points(text)

        lines.append(f"\n## {chapter}\n")
        lines.append(f"> {summary}\n")

        if points:
            for label, point in points:
                lines.append(f"- **{label}:** {point}")
            lines.append("")

        lines.append(f"_[→ Читать полностью]({doc_rel})_\n")
        lines.append("---\n")

    # Итоговый вывод
    lines += [
        "\n## Общая картина\n",
        "Lorenzo — это не один проект, а **экосистема взаимосвязанных компонентов**:\n",
        "1. **Svyazi 2.0** — ядро, объединяющее 20+ OSS-проектов",
        "2. **Ансамбли** — синергетические сборки для конкретных задач",
        "3. **MVP** — минимально жизнеспособный прототип за 12-18 месяцев",
        "4. **Команда** — распределённые авторы на Хабре и GitHub",
        "5. **Следующий шаг** — контакт с авторами ключевых компонентов\n",
        "_Полная дорожная карта: [docs/01-svyazi/12-roadmap.md](docs/01-svyazi/12-roadmap.md)_\n",
    ]

    out = DOCS / "NARRATIVE.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  глав в нарративе: {len(NARRATIVE_DOCS)}")


if __name__ == "__main__":
    main()
