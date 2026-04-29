"""
organize_docs.py — главный скрипт организации монорепозитория Lorenzo.

Запуск:
    cd /home/user/lorenzo
    python scripts/organize_docs.py

Что делает:
    1. docs/01-svyazi/      — из deep-research-report (1).md и (3).md
    2. docs/02-anthropic-vacancies/ — из MHTML "Вакансии в Anthropic..."
    3. docs/03-technology-combinations/ — из MHTML "Комбинирование технологий..."
    4. docs/04-ai-collaborations/ — из MHTML "Поиск коллабораций AI проектов"
    5. docs/05-habr-projects/ — из MHTML "Поиск уникальных проектов на Хабре..."

Исходные файлы НЕ удаляются и НЕ изменяются.
"""
import sys
from pathlib import Path

# Добавляем папку scripts в sys.path
sys.path.insert(0, str(Path(__file__).parent))

from part1_utils import ROOT, DOCS, write_doc
from part4_svyazi import run as run_svyazi
from part6_vacancies import run as run_vacancies
from part7_tech_combinations import run as run_tech
from part8_collaborations import run as run_collabs


README_CONTENT = """# Lorenzo — Монорепозиторий исследований

Организованные документы по темам. Исходные файлы сохранены в корне репозитория.

## Разделы

| Раздел | Описание |
|--------|----------|
| [01-svyazi](docs/01-svyazi/) | Svyazi 2.0: архитектура, компоненты, ансамбли, MVP |
| [02-anthropic-vacancies](docs/02-anthropic-vacancies/) | Анализ 436 вакансий Anthropic по 12 кластерам |
| [03-technology-combinations](docs/03-technology-combinations/) | 40+ синергетических комбинаций технологий |
| [04-ai-collaborations](docs/04-ai-collaborations/) | 5 ансамблей OSS-проектов для Svyazi |
| [05-habr-projects](docs/05-habr-projects/) | Проекты на Хабре: память, граф знаний, коллаборации |

## Исходные файлы

- `deep-research-report (1).md` — исходник для 01-svyazi (часть 1)
- `deep-research-report (2).md` — дубликат отчёта 1
- `deep-research-report (3).md` — исходник для 01-svyazi (часть 2)
- `deep-research-report (4).md` — дубликат отчёта 3
- `Вакансии в Anthropic по кластерам - Claude` — MHTML для 02-anthropic-vacancies
- `Комбинирование технологий для новых свойств - Claude` — MHTML для 03-technology-combinations
- `Поиск коллабораций AI проектов` — MHTML для 04-ai-collaborations
- `Поиск уникальных проектов на Хабре для совместной разработки - Claude` — MHTML для 05-habr-projects
- `Поиск уникальных проектов на Хабре для совместной разработки - Claude (1)` — дубликат

## Скрипты

- `scripts/organize_docs.py` — главный скрипт (этот файл)
- `scripts/extract_mhtml.py` — парсер MHTML → Markdown
- `scripts/part*.py` — модули по темам
"""

DOCS_README = """# Документация Lorenzo

Все документы организованы по тематическим разделам.
Каждый раздел содержит маленькие файлы по подтемам.

## Навигация

- [01-svyazi/](01-svyazi/) — Svyazi 2.0
- [02-anthropic-vacancies/](02-anthropic-vacancies/) — Вакансии Anthropic
- [03-technology-combinations/](03-technology-combinations/) — Комбинации технологий
- [04-ai-collaborations/](04-ai-collaborations/) — AI коллаборации
- [05-habr-projects/](05-habr-projects/) — Проекты с Хабра
"""


def write_readme_files():
    """Пишет корневой README и docs/README.md."""
    root_readme = ROOT / "README.md"
    # Обновляем README (добавляем навигацию, не удаляем)
    write_doc(root_readme, README_CONTENT)

    write_doc(DOCS / "README.md", DOCS_README)
    print("  README files written")


def main():
    print("=" * 50)
    print("Lorenzo Monorepo Doc Organizer")
    print("=" * 50)

    # Создаём все папки заранее
    for sub in [
        "01-svyazi/ensembles",
        "02-anthropic-vacancies/clusters",
        "03-technology-combinations",
        "04-ai-collaborations/ensembles",
        "05-habr-projects/memory",
        "05-habr-projects/knowledge",
    ]:
        (DOCS / sub).mkdir(parents=True, exist_ok=True)

    # Шаг 1: Markdown-отчёты → docs/01-svyazi/
    run_svyazi()

    # Шаг 2: Вакансии Anthropic
    run_vacancies()

    # Шаг 3: Комбинирование технологий
    run_tech()

    # Шаг 4: AI коллаборации + Хабр-проекты
    run_collabs()

    # Шаг 5: README файлы
    write_readme_files()

    # Итог
    all_md = list(DOCS.rglob("*.md"))
    print(f"\n{'=' * 50}")
    print(f"ГОТОВО: {len(all_md)} файлов создано в docs/")
    print("Исходные файлы не тронуты.")
    print("=" * 50)


if __name__ == '__main__':
    main()
