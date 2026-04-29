"""
improve_onboarding.py — руководство для новых участников проекта.
Собирает: структуру repo, первые шаги, ключевые файлы, скрипты, контакты.
Создаёт docs/ONBOARDING.md.
Запуск: python scripts/improve_onboarding.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"


def count_section(folder: str) -> tuple[int, int]:
    p = DOCS / folder
    if not p.exists():
        return 0, 0
    files = list(p.rglob("*.md"))
    words = sum(len(f.read_text(encoding="utf-8").split()) for f in files)
    return len(files), words


def get_scoring() -> str:
    p = DOCS / "SCORING.md"
    if not p.exists():
        return "96%"
    m = re.search(r'(\d+)%', p.read_text(encoding="utf-8"))
    return f"{m.group(1)}%" if m else "96%"


def get_script_count() -> int:
    return len(list((ROOT / "scripts").glob("improve_*.py")))


def main():
    print("Генерация руководства для новых участников...")

    sections = [
        ("01-svyazi",               "Архитектура Svyazi 2.0"),
        ("02-anthropic-vacancies",  "Вакансии Anthropic"),
        ("03-technology-combinations", "Комбинации технологий"),
        ("04-ai-collaborations",    "AI-коллаборации"),
        ("05-habr-projects",        "Хабр-проекты"),
    ]

    scoring  = get_scoring()
    n_scripts = get_script_count()

    section_rows = []
    total_files = total_words = 0
    for folder, name in sections:
        f, w = count_section(folder)
        total_files += f
        total_words += w
        section_rows.append(f"| [`docs/{folder}/`](docs/{folder}/README.md) | {name} | {f} | {w:,} |")

    lines = [
        "# Онбординг — Svyazi 2.0 / Lorenzo\n",
        "_Руководство для новых участников проекта._\n",

        "## Что это такое?\n",
        "**Svyazi 2.0** — экосистема из 20+ взаимосвязанных OSS-проектов для построения "
        "AI-систем с долгосрочной памятью, оркестрацией агентов и безопасной обработкой данных.\n",
        f"Статус готовности: **{scoring} 🟢 GO** (документация и архитектура).\n",

        "## Первые 30 минут\n",
        "```bash",
        "# 1. Клонировать репозиторий",
        "git clone <repo-url> && cd lorenzo",
        "",
        "# 2. Прочитать Executive Summary",
        "cat docs/01-svyazi/01-executive-summary.md",
        "",
        "# 3. Посмотреть статус проекта",
        "cat docs/SCORING.md",
        "",
        "# 4. Прочитать FAQ",
        "cat docs/FAQ.md",
        "",
        "# 5. Запустить скрипты (генерация/обновление docs)",
        "pip install beautifulsoup4 lxml",
        "python scripts/improve_run_all.py --fast",
        "```\n",

        "## Структура документации\n",
        f"_Всего: {total_files} файлов, {total_words:,} слов_\n",
        "| Раздел | Тема | Файлов | Слов |",
        "|--------|------|--------|------|",
    ]
    lines += section_rows
    lines += [
        "\n## Ключевые документы\n",
        "| Документ | Зачем читать |",
        "|----------|-------------|",
        "| `docs/01-svyazi/01-executive-summary.md` | Общий обзор проекта — начни здесь |",
        "| `docs/01-svyazi/07-mvp-planning.md` | MVP план, риски, оценки времени |",
        "| `docs/01-svyazi/12-roadmap.md` | Дорожная карта по кварталам |",
        "| `docs/01-svyazi/11-integration-contracts.md` | API-контракты между компонентами |",
        "| `docs/CONTACTS.md` | Авторы компонентов и шаблоны писем |",
        "| `docs/FAQ.md` | 54 вопроса и ответа |",
        "| `docs/TECH_RADAR.md` | Что использовать, что избегать |",
        "| `CLAUDE.md` | Гид по репо для Claude Code |\n",

        "## Скрипты автоматизации\n",
        f"В репо {n_scripts} скриптов `improve_*.py` для автоматического обновления документации.\n",
        "```bash",
        "# Все скрипты быстро",
        "python scripts/improve_run_all.py --fast",
        "",
        "# Конкретная группа",
        "python scripts/improve_run_all.py --group analysis",
        "# Группы: structure, index, analysis, extract, quality, graph, reports, export",
        "",
        "# LLM-обогащение (нужен API ключ)",
        "export ANTHROPIC_API_KEY=sk-ant-...",
        "python scripts/improve_run_all.py --group enrich",
        "",
        "# Автономный вотчер (следит за изменениями)",
        "python scripts/improve_watcher.py",
        "```\n",

        "## Архитектура компонентов\n",
        "| Компонент | Роль | Лицензия | Автор |",
        "|-----------|------|---------|-------|",
        "| **CardIndex** | Индекс знаний (785+ карточек) | MIT | kksudo |",
        "| **AgentFS** | Файловая система для AI | MIT | kksudo |",
        "| **Yodoca** | Память с консолидацией | Apache 2.0 | spbmolot |",
        "| **NGT-memory** | Ассоциативный граф памяти | BSL 1.1 | — |",
        "| **SENTINEL** | Безопасность, allowlist MCP | MIT | — |",
        "| **Rufler** | Оркестратор агентов | — | — |",
        "| **Firecrawl** | Веб-краулер для AI | MIT | — |\n",

        "## Как внести вклад\n",
        "1. **Документация:** редактируй файлы в `docs/`, запусти `improve_run_all.py`",
        "2. **Скрипты:** добавь `scripts/improve_*.py`, добавь в группу в `improve_run_all.py`",
        "3. **Контакты:** авторы компонентов в `docs/CONTACTS.md`, шаблон в `docs/templates/contact-outreach.md`",
        "4. **Архитектура:** новые ADR в `docs/01-svyazi/` по шаблону `docs/templates/adr-template.md`\n",

        "## Контакты\n",
        "- Контакты авторов компонентов: `docs/CONTACTS.md`",
        "- Шаблон письма для коллаборации: `docs/templates/contact-outreach.md`",
        "- Автор репозитория: `svend4` (GitHub)\n",

        "---\n",
        "_Этот документ генерируется скриптом `improve_onboarding.py`._",
        "_Для AI-ассистента: читай `CLAUDE.md` для понимания структуры репо._\n",
    ]

    out = DOCS / "ONBOARDING.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  разделов: {len(sections)}, файлов: {total_files}, слов: {total_words:,}")


if __name__ == "__main__":
    main()
