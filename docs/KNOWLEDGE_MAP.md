# Карта базы знаний Lorenzo

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> - ## Как реализован forensic RAG с доказуемостью? [Раздел: 01-svyazi]
**Проекты:** Svyazi

---

<!-- toc -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

## Содержание

- [Корпус](#корпус)
- [Метрики качества](#метрики-качества)
- [По секциям](#по-секциям)
- [Ключевые концепты](#ключевые-концепты)
- [Топ сущностей](#топ-сущностей)
- [Открытые вопросы](#открытые-вопросы)
- [Быстрые команды](#быстрые-команды)

---

<!-- tags: rag, security, ingestion, architecture, anthropic, self-improve, collaboration -->




_Обновлено: 2026-05-10_

---

## Корпус

| Параметр | Значение |
|----------|----------|
| Документов | **1209** |
| Слов | **1,092,412** |
| Секций | **20** |
| RAG-чанков | **2063** (по 8 секциям) |

## Метрики качества

| Метрика | Значение |
|---------|----------|
| Здоровье репо | 80/100 |
| Средний балл документов | 72.1/100 |
| Словарное богатство (STTR) | 0.643 |
| Пассивный залог | 1.6% |
| Пустых секций | 2049 |
| Противоречий | 5915 |

## По секциям

| Секция | Файлов | Слов | Ср. слов/файл |
|--------|--------|------|---------------|
| `obsidian` | 521 | 669,791 | 1285 |
| `02-anthropic-vacancies` | 357 | 319,964 | 896 |
| `nautilus` | 255 | 148,539 | 582 |
| `anthropic-vacancies` | 111 | 31,028 | 279 |
| `04-ai-collaborations` | 17 | 26,574 | 1563 |
| `lorenzo-agent` | 62 | 19,979 | 322 |
| `processing-guide` | 13 | 16,899 | 1299 |
| `habr-unique-projects` | 56 | 13,445 | 240 |
| `technology-combinations` | 53 | 13,381 | 252 |
| `svyazi-2-0` | 59 | 12,925 | 219 |
| `01-svyazi` | 16 | 11,578 | 723 |
| `05-habr-projects` | 10 | 9,335 | 933 |
| `ai-collaborations` | 30 | 8,257 | 275 |
| `templates` | 24 | 4,890 | 203 |
| `contacts` | 15 | 3,747 | 249 |
| `03-technology-combinations` | 7 | 3,159 | 451 |
| `meta-scripting` | 7 | 2,666 | 380 |
| `glossary` | 4 | 2,300 | 575 |
| `autofilled` | 13 | 2,058 | 158 |
| `badges` | 1 | 44 | 44 |

## Ключевые концепты

| Концепт | Файлов | Категория |
|---------|--------|-----------|
| `docs` | 1044 | other |
| `anthropic` | 814 | other |
| `claude` | 521 | other |
| `vacancies` | 500 | other |
| `источник` | 466 | other |
| `summary` | 432 | other |
| `mhtml` | 413 | other |
| `снимок` | 400 | other |

## Топ сущностей

| Сущность | Тип | Файлов |
|----------|-----|--------|
| `anthropic` | 👤 people | 770 |
| `nautilus` | 📦 projects | 496 |
| `claude` | 👤 people | 444 |
| `mcp` | ⚙️ tech | 337 |
| `svyazi` | 📦 projects | 310 |
| `вк` | 🏢 orgs | 288 |
| `github` | 📦 projects | 247 |
| `meta` | 🏢 orgs | 224 |
| `llm` | ⚙️ tech | 208 |
| `svend4` | 👤 people | 206 |
| `api` | ⚙️ tech | 179 |
| `rag` | ⚙️ tech | 161 |

## Открытые вопросы

- ## Как реализован forensic RAG с доказуемостью? [Раздел: 01-svyazi]
- ## Что такое Evidence Envelope и зачем он нужен? [Как реализован forensic RAG с доказуемостью?]
- ## Какие RAG-подходы сравниваются в документах? [Что такое Evidence Envelope и зачем он нужен?]
- ## Какие инструменты обеспечивают безопасность агентов? [Какие RAG-подходы сравниваются в документах
- ## Какова политика доступа по умолчанию (tool classes)? [Какие инструменты обеспечивают безопасность
- - Как реализован forensic RAG с доказуемостью? [[Глобальный Q&A](QA.md)]
- - Что такое Evidence Envelope и зачем он нужен? [[Глобальный Q&A](QA.md)]
- - Какие RAG-подходы сравниваются в документах? [[Глобальный Q&A](QA.md)]

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

_Карта сгенерирована автоматически: 2026-05-10_


<!-- see-also -->

---

**Смотрите также:**
- [CONCEPT_GRAPH](CONCEPT_GRAPH.md)
- [HEALTH](HEALTH.md)
- [STATS](STATS.md)
- [COVERAGE](COVERAGE.md)

