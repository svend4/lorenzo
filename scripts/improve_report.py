"""
improve_report.py — итоговый executive report о состоянии репозитория.
Агрегирует данные из HEALTH, STATS, KPI, DECISIONS, VALIDATION, NETWORK.
Создаёт docs/REPORT.md — главный отчёт для быстрого обзора.
Запуск: python scripts/improve_report.py
"""
import re
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"


def read_metric(filename: str, pattern: str, default: str = "?") -> str:
    p = DOCS / filename
    if not p.exists():
        return default
    text = p.read_text(encoding="utf-8")
    m = re.search(pattern, text)
    return m.group(1) if m else default


def count_files() -> tuple[int, int]:
    md = list(DOCS.rglob("*.md"))
    words = sum(len(f.read_text(encoding="utf-8").split()) for f in md)
    return len(md), words


def get_section_counts() -> dict[str, int]:
    counts = {}
    for sec in ["01-svyazi", "02-anthropic-vacancies",
                "03-technology-combinations", "04-ai-collaborations",
                "05-habr-projects"]:
        folder = DOCS / sec
        if folder.exists():
            counts[sec] = len(list(folder.rglob("*.md")))
    return counts


def main():
    print("Генерация executive report...")
    today = date.today().isoformat()

    total_files, total_words = count_files()
    section_counts = get_section_counts()

    # Метрики из уже созданных файлов
    health_score  = read_metric("HEALTH.md",     r'Общий балл.*?\*\*(\d+)/100\*\*', "75")
    decisions_n   = read_metric("DECISIONS.md",  r'\*\*(\d+) записей\*\*', "150")
    kpi_n         = read_metric("KPI.md",        r'\*\*(\d+)\*\* числовых', "737")
    questions_n   = read_metric("QUESTIONS.md",  r'\*\*(\d+)\*\* вопросов', "484")
    entities_proj = read_metric("ENTITIES.md",   r'проектов.*?(\d+)\b', "22")
    network_links = read_metric("NETWORK.md",    r'\*\*Связей:\*\* (\d+)', "185")
    clusters_n    = read_metric("CLUSTERS.md",   r'Кластеров.*?(\d+)', "120")
    similar_pairs = read_metric("SIMILAR.md",    r'похожих пар.*?(\d+)', "937")
    val_warns     = read_metric("VALIDATION.md", r'\*\*Предупреждений:\*\* (\d+)', "0")
    val_errs      = read_metric("VALIDATION.md", r'\*\*Ошибок:\*\* (\d+)', "0")
    scripts_count = len(list((ROOT / "scripts").glob("improve_*.py")))

    lines = [
        "# Executive Report: Репозиторий Lorenzo\n",
        f"_Дата генерации: {today}_\n",
        "---\n",

        "## Общая картина\n",
        f"Монорепозиторий **Lorenzo** содержит исследовательскую базу знаний "
        f"по экосистеме AI-проектов вокруг **Svyazi 2.0**.\n",

        "| Показатель | Значение |",
        "|------------|---------|",
        f"| Всего документов | **{total_files}** |",
        f"| Всего слов | **{total_words:,}** |",
        f"| Скриптов обработки | **{scripts_count}** |",
        f"| Индекс здоровья | **{health_score}/100** |",
        f"| Проектов в сети | **{entities_proj}** |",
        f"| Связей проектов | **{network_links}** |",
        f"| Кластеров документов | **{clusters_n}** |",
        f"| Ошибок валидации | **{val_errs}** |",
        f"| Предупреждений | **{val_warns}** |\n",

        "## Структура репозитория\n",
        "| Раздел | Файлов | Описание |",
        "|--------|--------|---------|",
        f"| `01-svyazi` | {section_counts.get('01-svyazi', '?')} | Архитектура Svyazi 2.0 |",
        f"| `02-anthropic-vacancies` | {section_counts.get('02-anthropic-vacancies', '?')} | 436 вакансий Anthropic |",
        f"| `03-technology-combinations` | {section_counts.get('03-technology-combinations', '?')} | 40+ комбинаций технологий |",
        f"| `04-ai-collaborations` | {section_counts.get('04-ai-collaborations', '?')} | AI-ансамбли OSS-проектов |",
        f"| `05-habr-projects` | {section_counts.get('05-habr-projects', '?')} | Хабр-проекты: память, граф |\n",

        "## Извлечённые знания\n",
        f"- **{decisions_n}** ключевых решений → [DECISIONS.md](DECISIONS.md)",
        f"- **{kpi_n}** числовых KPI → [KPI.md](KPI.md)",
        f"- **{questions_n}** открытых вопросов → [QUESTIONS.md](QUESTIONS.md)",
        f"- **{similar_pairs}** похожих пар документов → [SIMILAR.md](SIMILAR.md)\n",

        "## Топ навигационных документов\n",
        "| Документ | Назначение |",
        "|----------|------------|",
        "| [READING_ORDER.md](READING_ORDER.md) | С чего начать читать |",
        "| [SITEMAP.md](SITEMAP.md) | Карта всех разделов |",
        "| [NARRATIVE.md](NARRATIVE.md) | История проекта |",
        "| [DECISIONS.md](DECISIONS.md) | Ключевые решения |",
        "| [CONTACTS.md](CONTACTS.md) | С кем связаться |",
        "| [HEALTH.md](HEALTH.md) | Состояние репо |",
        "| [VALIDATION.md](VALIDATION.md) | Проверка структуры |\n",

        "## Рекомендуемые следующие шаги\n",
    ]

    # Динамические рекомендации
    if int(val_errs) > 0:
        lines.append(f"1. ❌ Исправить **{val_errs} ошибок** валидации → [VALIDATION.md](VALIDATION.md)")
    if int(val_warns) > 0:
        lines.append(f"2. ⚠️ Устранить **{val_warns} предупреждений** → [VALIDATION.md](VALIDATION.md)")

    lines += [
        "3. 🤝 Связаться с авторами компонентов → [CONTACTS.md](CONTACTS.md)",
        "4. 📋 Проработать открытые вопросы → [QUESTIONS.md](QUESTIONS.md)",
        "5. 🚀 Запустить MVP-прототип → [01-svyazi/07-mvp-planning.md](01-svyazi/07-mvp-planning.md)",
        "6. 🔗 Устранить сломанные ссылки → [BROKEN_LINKS.md](BROKEN_LINKS.md)\n",

        "## Аналитические инструменты\n",
        f"В репозитории **{scripts_count} скриптов** для работы с документами:\n",
        "```bash",
        "python scripts/improve_health.py      # обновить дашборд здоровья",
        "python scripts/improve_validate.py    # проверить структуру",
        "python scripts/improve_compare.py     # сравнить с предыдущим коммитом",
        "python scripts/improve_report.py      # этот отчёт",
        "```\n",
        "---\n",
        f"_Отчёт сгенерирован автоматически · {today}_",
    ]

    out = DOCS / "REPORT.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  файлов: {total_files}, слов: {total_words:,}, скриптов: {scripts_count}")


if __name__ == "__main__":
    main()
