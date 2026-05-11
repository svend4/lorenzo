# Карта базы знаний Lorenzo

<!-- toc-auto -->
## Contents

- [Корпус](#корпус)
- [Метрики качества](#метрики-качества)
- [По секциям](#по-секциям)
- [Ключевые концепты](#ключевые-концепты)
- [Топ сущностей](#топ-сущностей)
- [Открытые вопросы](#открытые-вопросы)
- [Быстрые команды](#быстрые-команды)


<!-- tags: knowledge-map, docs -->


<!-- summary -->
> `KNOWLEDGE_MAP` — раздел документации проекта Lorenzo.


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

_Обновлено: 2026-05-11_

---

## Корпус

| Параметр | Значение |
|----------|----------|
| Документов | **1221** |
| Слов | **1,370,286** |
| Секций | **20** |
| RAG-чанков | **2063** (по 8 секциям) |

## Метрики качества

| Метрика | Значение |
|---------|----------|
| Здоровье репо | 90 |
| Средний балл документов | 100.0/100 |
| Словарное богатство (STTR) | 0.628 |
| Пассивный залог | 1.5% |
| Пустых секций | 3489 |
| Противоречий | 7848 |

## По секциям

| Секция | Файлов | Слов | Ср. слов/файл |
|--------|--------|------|---------------|
| `obsidian` | 1213 | 1,220,285 | 1006 |
| `02-anthropic-vacancies` | 357 | 340,655 | 954 |
| `nautilus` | 255 | 170,500 | 668 |
| `anthropic-vacancies` | 111 | 44,358 | 399 |
| `04-ai-collaborations` | 17 | 27,823 | 1636 |
| `lorenzo-agent` | 62 | 27,144 | 437 |
| `svyazi-2-0` | 60 | 19,089 | 318 |
| `habr-unique-projects` | 56 | 18,520 | 330 |
| `technology-combinations` | 53 | 18,351 | 346 |
| `processing-guide` | 13 | 17,244 | 1326 |
| `05-habr-projects` | 16 | 14,666 | 916 |
| `01-svyazi` | 16 | 13,246 | 827 |
| `ai-collaborations` | 31 | 11,309 | 364 |
| `templates` | 24 | 7,467 | 311 |
| `contacts` | 17 | 4,968 | 292 |
| `03-technology-combinations` | 7 | 3,783 | 540 |
| `meta-scripting` | 7 | 3,168 | 452 |
| `autofilled` | 13 | 2,648 | 203 |
| `glossary` | 4 | 2,575 | 643 |
| `badges` | 1 | 122 | 122 |

## Ключевые концепты

| Концепт | Файлов | Категория |
|---------|--------|-----------|
| `документ` | 965 | other |
| `смотрите` | 683 | other |
| `также` | 683 | other |
| `anthropic` | 638 | other |
| `связанные` | 563 | other |
| `note` | 509 | other |
| `ссылки` | 480 | other |
| `claude` | 470 | other |

## Топ сущностей

| Сущность | Тип | Файлов |
|----------|-----|--------|
| `anthropic` | 👤 people | 654 |
| `claude` | 👤 people | 450 |
| `lorenzo` | 📦 projects | 435 |
| `nautilus` | 📦 projects | 402 |
| `mcp` | ⚙️ tech | 352 |
| `svyazi` | 📦 projects | 333 |
| `вк` | 🏢 orgs | 297 |
| `bm25` | ⚙️ tech | 255 |
| `github` | 📦 projects | 254 |
| `meta` | 🏢 orgs | 216 |
| `llm` | ⚙️ tech | 211 |
| `svend4` | 👤 people | 191 |

## Открытые вопросы

- -  Какие 5 архитектурных зазоров выделены в исследовании? [Содержание]
- -  Что входит в интеграционный контракт между слоями? [Содержание]
- -  Как реализован forensic RAG с доказуемостью? [Содержание]
- -  Что такое Evidence Envelope и зачем он нужен? [Содержание]
- -  Какие RAG-подходы сравниваются в документах? [Содержание]
- -   Вопрос: fallback-ratio как критический или осмысленный? [Содержание]
- -  Q&A: svyazi-2-0   - Основной раздел - Содержание - Как реализован forensic RAG с доказуемостью? [
- -  Принимаем эту architecture как Lorenzo vision (с моими caveats)? [Содержание]

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

_Карта сгенерирована автоматически: 2026-05-11_


<!-- see-also -->

---

**Смотрите также:**
- [HEALTH](HEALTH.md)
- [STATS](STATS.md)
- [SENTIMENT](SENTIMENT.md)
- [CONCEPT_GRAPH](CONCEPT_GRAPH.md)

