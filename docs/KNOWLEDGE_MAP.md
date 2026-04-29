# Карта базы знаний Lorenzo

_Обновлено: 2026-04-29_

---

## Корпус

| Параметр | Значение |
|----------|----------|
| Документов | **1162** |
| Слов | **1,039,600** |
| Секций | **18** |
| RAG-чанков | **5405** (по 17 секциям) |

## Метрики качества

| Метрика | Значение |
|---------|----------|
| Здоровье репо | 77/100 |
| Средний балл документов | 73.0/100 |
| Словарное богатство (STTR) | 0.636 |
| Пассивный залог | 1.6% |
| Пустых секций | 1632 |
| Противоречий | 9367 |

## По секциям

| Секция | Файлов | Слов | Ср. слов/файл |
|--------|--------|------|---------------|
| `obsidian` | 1158 | 1,016,778 | 878 |
| `02-anthropic-vacancies` | 357 | 312,388 | 875 |
| `nautilus` | 255 | 153,298 | 601 |
| `anthropic-vacancies` | 111 | 32,927 | 296 |
| `04-ai-collaborations` | 17 | 26,299 | 1547 |
| `lorenzo-agent` | 62 | 21,077 | 339 |
| `habr-unique-projects` | 56 | 14,157 | 252 |
| `technology-combinations` | 53 | 13,849 | 261 |
| `svyazi-2-0` | 59 | 13,565 | 229 |
| `01-svyazi` | 16 | 11,501 | 718 |
| `05-habr-projects` | 10 | 9,164 | 916 |
| `ai-collaborations` | 30 | 8,743 | 291 |
| `contacts` | 15 | 3,163 | 210 |
| `03-technology-combinations` | 7 | 3,093 | 441 |
| `glossary` | 4 | 2,354 | 588 |
| `autofilled` | 13 | 1,944 | 149 |
| `templates` | 6 | 633 | 105 |
| `badges` | 1 | 44 | 44 |

## Ключевые концепты

| Концепт | Файлов | Категория |
|---------|--------|-----------|
| `docs` | 954 | other |
| `сходство` | 775 | other |
| `anthropic` | 774 | other |
| `vacancies` | 497 | other |
| `claude` | 496 | other |
| `источник` | 449 | other |
| `nautilus` | 405 | other |
| `summary` | 395 | other |

## Топ сущностей

| Сущность | Тип | Файлов |
|----------|-----|--------|
| `anthropic` | 👤 people | 802 |
| `nautilus` | 📦 projects | 532 |
| `obsidian` | 📦 projects | 427 |
| `claude` | 👤 people | 416 |
| `svyazi` | 📦 projects | 315 |
| `mcp` | ⚙️ tech | 314 |
| `вк` | 🏢 orgs | 273 |
| `github` | 📦 projects | 239 |
| `svend4` | 👤 people | 206 |
| `meta` | 🏢 orgs | 201 |
| `llm` | ⚙️ tech | 191 |
| `lorenzo` | 📦 projects | 168 |

## Открытые вопросы

- - Как реализован forensic RAG с доказуемостью? [[Глобальный Q&A](docs/QA.md)]
- - Что такое Evidence Envelope и зачем он нужен? [[Глобальный Q&A](docs/QA.md)]
- - Какие RAG-подходы сравниваются в документах? [[Глобальный Q&A](docs/QA.md)]
- - Какие инструменты обеспечивают безопасность агентов? [[Глобальный Q&A](docs/QA.md)]
- - Какова политика доступа по умолчанию (tool classes)? [[Глобальный Q&A](docs/QA.md)]
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

