# Lorenzo — Монорепозиторий исследований
<!-- badges -->
![docs](docs/badges/docs.svg) ![words](docs/badges/words.svg) ![scripts](docs/badges/scripts.svg) ![health](docs/badges/health.svg) ![go/no-go](docs/badges/scoring.svg) ![license](docs/badges/license.svg) ![branch](docs/badges/branch.svg) 


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
