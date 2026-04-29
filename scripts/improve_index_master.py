"""
improve_index_master.py — главный навигационный хаб docs/.
Собирает все ключевые документы, статистику, ссылки в один docs/INDEX.md.
Служит точкой входа для навигации по всей документации.
Запуск: python scripts/improve_index_master.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

SECTIONS = [
    ("01-svyazi",               "🏗️  Архитектура Svyazi 2.0",
     "Ключевые компоненты, контракты, MVP, дорожная карта"),
    ("02-anthropic-vacancies",  "💼 Вакансии Anthropic",
     "436 вакансий по 12 кластерам, стратегический анализ"),
    ("03-technology-combinations", "⚗️  Комбинации технологий",
     "40+ синергетических комбинаций AI-технологий"),
    ("04-ai-collaborations",    "🤝 AI-коллаборации",
     "5 ансамблей OSS-проектов: Knowledge OS, Agent Teams, Security Runtime"),
    ("05-habr-projects",        "📦 Хабр-проекты",
     "Yodoca, NGT, AgentFS, knowledge-space — проекты с Хабра"),
]

META_DOCS = [
    ("SCORING.md",         "🎯 Go/No-Go скоринг",    "Статус готовности: 96%"),
    ("HEALTH.md",          "❤️  Здоровье репо",       "Метрики качества документации"),
    ("TECH_RADAR.md",      "📡 Tech Radar",           "ADOPT/TRIAL/ASSESS/HOLD"),
    ("RISK_REGISTER.md",   "⚠️  Реестр рисков",       "10 рисков, матрица вероятность×влияние"),
    ("ONBOARDING.md",      "👋 Онбординг",            "Первые шаги, структура, контакты"),
    ("FAQ.md",             "❓ FAQ",                   "54 вопроса и ответа"),
    ("CONTACTS.md",        "📧 Контакты",             "Авторы компонентов, шаблоны писем"),
    ("SCHEDULE.md",        "📅 Расписание",           "Gantt, вехи, текущий статус"),
    ("COST.md",            "💰 Стоимость MVP",        "$86,400 · 25 чел-недель"),
    ("NETWORK.md",         "🕸️  Граф связей",         "20 узлов, 185 рёбер"),
    ("CHANGELOG_AUTO.md",  "📋 Changelog",            "Авто из git-истории"),
    ("DEPENDENCY_MAP.md",  "🗺️  Карта зависимостей", "49 скриптов → входы/выходы"),
]

REPORT_DOCS = [
    ("STATS.md",           "Статистика"),
    ("METRICS.md",         "Качество (65.7/100)"),
    ("VALIDATION.md",      "Валидация"),
    ("SENTIMENT.md",       "Тональность"),
    ("CLUSTERS.md",        "Кластеры тем"),
    ("SIMILAR.md",         "Похожие документы"),
    ("HEATMAP.md",         "Тепловая карта тем"),
    ("QUESTIONS.md",       "Открытые вопросы (484)"),
    ("KPI.md",             "KPI (737 показателей)"),
    ("ACTION_ITEMS.md",    "Задачи"),
    ("DECISIONS.md",       "Архитектурные решения"),
    ("PRIORITIES.md",      "Приоритеты"),
    ("PROGRESS.md",        "Прогресс MVP"),
    ("DIGEST_WEEKLY.md",   "Дайджест недели"),
    ("SITEMAP.md",         "Карта сайта"),
    ("WORD_CLOUD.md",      "Облако слов"),
    ("BACKLINKS.md",       "Обратные ссылки"),
    ("NARRATIVE.md",       "Нарратив проекта"),
    ("ORPHANS.md",         "Несвязанные файлы"),
    ("ALERTS.md",          "Callout-блоки"),
    ("FOOTNOTES.md",       "Сноски терминов"),
    ("ABBREVIATIONS.md",   "Аббревиатуры"),
    ("GLOSSARY.md",        "Глоссарий"),
    ("CONCEPTS.md",        "Концепции"),
    ("ENTITIES.md",        "Сущности"),
    ("TAGS.md",            "Теги"),
]


def read_stat(fname: str, pattern: str, default: str = "—") -> str:
    p = DOCS / fname
    if not p.exists():
        return default
    m = re.search(pattern, p.read_text(encoding="utf-8"))
    return m.group(1) if m else default


def main():
    print("Генерация главного индекса...")

    total_md    = len(list(DOCS.rglob("*.md")))
    total_words = sum(len(f.read_text(encoding="utf-8").split()) for f in DOCS.rglob("*.md"))
    n_scripts   = len(list((ROOT / "scripts").glob("improve_*.py")))
    scoring     = read_stat("SCORING.md",  r'(\d+)%', "96%")
    health      = read_stat("HEALTH.md",   r'(\d+)/100', "—")

    lines = [
        "# Индекс документации — Lorenzo / Svyazi 2.0\n",
        "_Главный навигационный хаб. Все разделы и документы._\n",

        "## Метрики репозитория\n",
        "| Параметр | Значение |",
        "|----------|---------|",
        f"| Markdown документов | **{total_md}** |",
        f"| Слов | **{total_words:,}** |",
        f"| Скриптов автоматизации | **{n_scripts}** |",
        f"| Go/No-Go скоринг | **{scoring} 🟢** |",
        f"| Здоровье репо | **{health}/100** |\n",

        "## Разделы документации\n",
    ]

    for folder, title, desc in SECTIONS:
        sec_dir = DOCS / folder
        if sec_dir.exists():
            n = len(list(sec_dir.rglob("*.md")))
            w = sum(len(f.read_text(encoding="utf-8").split()) for f in sec_dir.rglob("*.md"))
            lines.append(
                f"### [{title}](docs/{folder}/README.md)\n\n"
                f"{desc}\n\n"
                f"_{n} файлов · {w:,} слов_\n"
            )
        else:
            lines.append(f"### {title}\n\n{desc}\n\n_раздел не создан_\n")

    lines += ["\n## Аналитика и отчёты\n"]
    lines.append("| Документ | Описание |")
    lines.append("|----------|---------|")
    for fname, desc in REPORT_DOCS:
        p = DOCS / fname
        if p.exists():
            lines.append(f"| [`{fname}`](docs/{fname}) | {desc} |")

    lines += ["\n## Ключевые документы\n"]
    lines.append("| Документ | Тема | Описание |")
    lines.append("|----------|------|---------|")
    for fname, title, desc in META_DOCS:
        p = DOCS / fname
        exists = p.exists()
        link = f"[`{fname}`](docs/{fname})" if exists else f"`{fname}` _(нет)_"
        lines.append(f"| {link} | {title} | {desc} |")

    lines += [
        "\n## LLM-обогащение (Ступень 3)\n",
        "_Требуют `ANTHROPIC_API_KEY`:_\n",
        "| Документ | Описание |",
        "|----------|---------|",
    ]
    llm_docs = [
        ("LLM_ENRICHED.md",  "Обогащённые stub-файлы"),
        ("LLM_QA.md",        "Ответы на открытые вопросы"),
        ("LLM_GAPS.md",      "Семантические пробелы"),
        ("LLM_SUMMARIES.md", "AI-саммари разделов"),
    ]
    for fname, desc in llm_docs:
        p = DOCS / fname
        link = f"[`{fname}`](docs/{fname})" if p.exists() else f"`{fname}` _(нет)_"
        lines.append(f"| {link} | {desc} |")

    lines += [
        "\n## Быстрый старт\n",
        "```bash",
        "# Читать документацию",
        "cat docs/01-svyazi/01-executive-summary.md",
        "cat docs/ONBOARDING.md",
        "",
        "# Обновить всю документацию",
        "python scripts/improve_run_all.py --fast",
        "",
        "# Конкретная группа",
        "python scripts/improve_run_all.py --group analysis",
        "```\n",
        "---\n",
        f"_Индекс сгенерирован автоматически · {total_md} документов · {n_scripts} скриптов_\n",
    ]

    out = DOCS / "INDEX.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  разделов: {len(SECTIONS)}, мета-docs: {len(META_DOCS)}, отчётов: {len(REPORT_DOCS)}")


if __name__ == "__main__":
    main()
