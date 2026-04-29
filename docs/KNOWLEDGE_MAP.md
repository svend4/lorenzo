# Карта базы знаний Lorenzo

_Обновлено: 2026-04-29_

---

## Корпус

| Параметр | Значение |
|----------|----------|
| Документов | **492** |
| Слов | **433,953** |
| Секций | **8** |
| RAG-чанков | **2021** (по 7 секциям) |

## Метрики качества

| Метрика | Значение |
|---------|----------|
| Здоровье репо | 75/100 |
| Средний балл документов | 67.5/100 |
| Словарное богатство (STTR) | 0.675 |
| Пассивный залог | 2.2% |
| Пустых секций | 571 |
| Противоречий | 2966 |

## По секциям

| Секция | Файлов | Слов | Ср. слов/файл |
|--------|--------|------|---------------|
| `02-anthropic-vacancies` | 357 | 277,544 | 777 |
| `04-ai-collaborations` | 17 | 26,497 | 1558 |
| `01-svyazi` | 16 | 11,392 | 712 |
| `05-habr-projects` | 10 | 8,906 | 890 |
| `03-technology-combinations` | 7 | 2,862 | 408 |
| `contacts` | 14 | 2,376 | 169 |
| `templates` | 6 | 744 | 124 |
| `badges` | 1 | 44 | 44 |

## Ключевые концепты

| Концепт | Файлов | Категория |
|---------|--------|-----------|
| `docs` | 412 | other |
| `anthropic` | 347 | other |
| `vacancies` | 333 | other |
| `summary` | 241 | other |
| `сходство` | 225 | other |
| `tags` | 164 | other |
| `agent` | 118 | agent |
| `architecture` | 113 | other |

## Топ сущностей

| Сущность | Тип | Файлов |
|----------|-----|--------|
| `anthropic` | 👤 people | 374 |
| `nautilus` | 📦 projects | 147 |
| `claude` | 👤 people | 143 |
| `mcp` | ⚙️ tech | 126 |
| `github` | 📦 projects | 118 |
| `вк` | 🏢 orgs | 115 |
| `svyazi` | 📦 projects | 100 |
| `svend4` | 👤 people | 84 |
| `meta` | 🏢 orgs | 83 |
| `api` | ⚙️ tech | 72 |
| `2026-04` | 📅 dates | 66 |
| `llm` | ⚙️ tech | 64 |

## Открытые вопросы

- -  Как реализован forensic RAG с доказуемостью? [Содержание]
- -  Что такое Evidence Envelope и зачем он нужен? [Содержание]
- -  Какие RAG-подходы сравниваются в документах? [Содержание]
- -  Какие инструменты обеспечивают безопасность агентов? [Содержание]
- -  Какова политика доступа по умолчанию (tool classes)? [Содержание]
- -  А reflection — это вы делаете уже? [Содержание]
- What's the role of you (the proposer)? [Что было бы Concept Document]
- Specific Anthropic product для focus (Cowork? [Что mне нужно знать перед drafting]

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

