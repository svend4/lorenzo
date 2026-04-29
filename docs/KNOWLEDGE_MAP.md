# Карта базы знаний Lorenzo

_Обновлено: 2026-04-29_

---

## Корпус

| Параметр | Значение |
|----------|----------|
| Документов | **1185** |
| Слов | **908,390** |
| Секций | **17** |
| RAG-чанков | **2021** (по 7 секциям) |

## Метрики качества

| Метрика | Значение |
|---------|----------|
| Здоровье репо | 77/100 |
| Средний балл документов | 71.2/100 |
| Словарное богатство (STTR) | 0.675 |
| Пассивный залог | 1.7% |
| Пустых секций | 1671 |
| Противоречий | 6481 |

## По секциям

| Секция | Файлов | Слов | Ср. слов/файл |
|--------|--------|------|---------------|
| `02-anthropic-vacancies` | 357 | 278,999 | 781 |
| `nautilus` | 255 | 148,523 | 582 |
| `anthropic-vacancies` | 111 | 30,960 | 278 |
| `04-ai-collaborations` | 17 | 26,057 | 1532 |
| `lorenzo-agent` | 62 | 19,979 | 322 |
| `habr-unique-projects` | 56 | 13,161 | 235 |
| `technology-combinations` | 53 | 12,903 | 243 |
| `svyazi-2-0` | 59 | 12,455 | 211 |
| `01-svyazi` | 16 | 11,052 | 690 |
| `05-habr-projects` | 10 | 8,622 | 862 |
| `ai-collaborations` | 30 | 8,207 | 273 |
| `templates` | 24 | 4,858 | 202 |
| `contacts` | 15 | 3,492 | 232 |
| `03-technology-combinations` | 7 | 2,799 | 399 |
| `glossary` | 4 | 2,282 | 570 |
| `autofilled` | 13 | 533 | 41 |
| `badges` | 1 | 44 | 44 |

## Ключевые концепты

| Концепт | Файлов | Категория |
|---------|--------|-----------|
| `docs` | 995 | other |
| `anthropic` | 791 | other |
| `claude` | 502 | other |
| `summary` | 497 | other |
| `vacancies` | 474 | other |
| `источник` | 467 | other |
| `mhtml` | 411 | other |
| `снимок` | 400 | other |

## Топ сущностей

| Сущность | Тип | Файлов |
|----------|-----|--------|
| `anthropic` | 👤 people | 743 |
| `nautilus` | 📦 projects | 467 |
| `claude` | 👤 people | 400 |
| `mcp` | ⚙️ tech | 301 |
| `svyazi` | 📦 projects | 296 |
| `вк` | 🏢 orgs | 267 |
| `github` | 📦 projects | 237 |
| `meta` | 🏢 orgs | 199 |
| `svend4` | 👤 people | 196 |
| `llm` | ⚙️ tech | 193 |
| `api` | ⚙️ tech | 167 |
| `rag` | ⚙️ tech | 151 |

## Открытые вопросы

- - - - - - - - - -  Как реализован forensic RAG с доказуемостью? [[Карта базы знаний Lorenzo](docs/KN
- - Как реализован forensic RAG с доказуемостью? [[Глобальный Q&A](docs/QA.md)]
- - Что такое Evidence Envelope и зачем он нужен? [[Глобальный Q&A](docs/QA.md)]
- - Какие RAG-подходы сравниваются в документах? [[Глобальный Q&A](docs/QA.md)]
- - Какие инструменты обеспечивают безопасность агентов? [[Глобальный Q&A](docs/QA.md)]
- ## Как реализован forensic RAG с доказуемостью? [Раздел: 01-svyazi]
- ## Что такое Evidence Envelope и зачем он нужен? [Как реализован forensic RAG с доказуемостью?]
- ## Какие RAG-подходы сравниваются в документах? [Что такое Evidence Envelope и зачем он нужен?]

## Быстрые команды

```bash
# Поиск
python scripts/improve_passage_retrieval.py --query "ваш запрос"
python scripts/improve_faceted_search.py --query "ваш запрос"
python scripts/improve_keyword_index.py --query "ваш запрос"

# Улучшение контента
python scripts/improve_auto_toc.py --apply
python scripts/improve_abstract.py --apply
python scripts/improve_auto_linker.py --apply --types projects
python scripts/improve_empty_sections.py --fill

# Полный прогон
python scripts/improve_run_all.py --group deeptext
python scripts/improve_run_all.py --group nlpplus
```

_Карта сгенерирована автоматически: 2026-04-29_

