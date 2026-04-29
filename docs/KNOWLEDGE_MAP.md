# Карта базы знаний Lorenzo

_Обновлено: 2026-04-29_

---

## Корпус

| Параметр | Значение |
|----------|----------|
| Документов | **1161** |
| Слов | **870,981** |
| Секций | **17** |
| RAG-чанков | **2021** (по 7 секциям) |

## Метрики качества

| Метрика | Значение |
|---------|----------|
| Здоровье репо | 77/100 |
| Средний балл документов | 71.3/100 |
| Словарное богатство (STTR) | 0.674 |
| Пассивный залог | 1.6% |
| Пустых секций | 1445 |
| Противоречий | 5408 |

## По секциям

| Секция | Файлов | Слов | Ср. слов/файл |
|--------|--------|------|---------------|
| `02-anthropic-vacancies` | 357 | 279,017 | 781 |
| `nautilus` | 255 | 148,523 | 582 |
| `anthropic-vacancies` | 111 | 30,929 | 278 |
| `04-ai-collaborations` | 17 | 26,057 | 1532 |
| `lorenzo-agent` | 62 | 19,979 | 322 |
| `habr-unique-projects` | 56 | 13,161 | 235 |
| `technology-combinations` | 53 | 12,903 | 243 |
| `svyazi-2-0` | 59 | 12,455 | 211 |
| `01-svyazi` | 16 | 10,998 | 687 |
| `05-habr-projects` | 10 | 8,619 | 861 |
| `ai-collaborations` | 30 | 8,207 | 273 |
| `contacts` | 15 | 3,151 | 210 |
| `03-technology-combinations` | 7 | 2,796 | 399 |
| `glossary` | 4 | 2,282 | 570 |
| `templates` | 6 | 635 | 105 |
| `autofilled` | 13 | 533 | 41 |
| `badges` | 1 | 44 | 44 |

## Ключевые концепты

| Концепт | Файлов | Категория |
|---------|--------|-----------|
| `docs` | 980 | other |
| `anthropic` | 793 | other |
| `claude` | 501 | other |
| `summary` | 485 | other |
| `vacancies` | 476 | other |
| `источник` | 465 | other |
| `mhtml` | 411 | other |
| `снимок` | 400 | other |

## Топ сущностей

| Сущность | Тип | Файлов |
|----------|-----|--------|
| `anthropic` | 👤 people | 746 |
| `nautilus` | 📦 projects | 463 |
| `claude` | 👤 people | 399 |
| `svyazi` | 📦 projects | 295 |
| `mcp` | ⚙️ tech | 291 |
| `вк` | 🏢 orgs | 261 |
| `github` | 📦 projects | 234 |
| `meta` | 🏢 orgs | 200 |
| `svend4` | 👤 people | 196 |
| `llm` | ⚙️ tech | 188 |
| `api` | ⚙️ tech | 165 |
| `rag` | ⚙️ tech | 148 |

## Открытые вопросы

- - -  Как реализован forensic RAG с доказуемостью? [[Карта базы знаний Lorenzo](docs/KNOWLEDGE_MAP.md
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

