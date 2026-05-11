# Карта базы знаний Lorenzo

<!-- toc -->
## Содержание

- [Корпус](#корпус)
- [Метрики качества](#метрики-качества)
- [По секциям](#по-секциям)
- [Ключевые концепты](#ключевые-концепты)
- [Топ сущностей](#топ-сущностей)
- [Открытые вопросы](#открытые-вопросы)
- [Быстрые команды](#быстрые-команды)

---


<!-- toc-auto -->

> [!NOTE]
> Раздел `KNOWLEDGE_MAP` формируется автоматически из данных репозитория.

<!-- alert-added -->
<!-- tags: knowledge-map, docs -->


<!-- summary -->
> `KNOWLEDGE_MAP` — раздел документации проекта Lorenzo.


_Обновлено: 2026-05-11_

---

## Корпус

| Параметр | Значение |
|----------|----------|
| Документов | **1235** |
| Слов | **1,429,571** |
| Секций | **21** |
| RAG-чанков | **6879** (по 21 секциям) |

## Метрики качества

| Метрика | Значение |
|---------|----------|
| Здоровье репо | 90 |
| Средний балл документов | 95.9/100 |
| Словарное богатство (STTR) | 0.621 |
| Пассивный залог | 1.4% |
| Пустых секций | 3559 |
| Противоречий | 7754 |

## По секциям

| Секция | Файлов | Слов | Ср. слов/файл |
|--------|--------|------|---------------|
| `obsidian` | 1230 | 1,389,841 | 1129 |
| `02-anthropic-vacancies` | 357 | 341,828 | 957 |
| `nautilus` | 255 | 176,913 | 693 |
| `anthropic-vacancies` | 111 | 47,082 | 424 |
| `lorenzo-agent` | 62 | 28,664 | 462 |
| `04-ai-collaborations` | 17 | 27,940 | 1643 |
| `svyazi-2-0` | 60 | 20,715 | 345 |
| `habr-unique-projects` | 56 | 19,966 | 356 |
| `technology-combinations` | 53 | 19,585 | 369 |
| `processing-guide` | 13 | 17,500 | 1346 |
| `05-habr-projects` | 16 | 14,869 | 929 |
| `01-svyazi` | 16 | 13,360 | 835 |
| `ai-collaborations` | 31 | 12,182 | 392 |
| `templates` | 24 | 7,791 | 324 |
| `contacts` | 17 | 5,044 | 296 |
| `03-technology-combinations` | 7 | 3,815 | 545 |
| `letters` | 10 | 3,618 | 361 |
| `meta-scripting` | 7 | 3,344 | 477 |
| `autofilled` | 13 | 2,904 | 223 |
| `glossary` | 4 | 2,692 | 673 |
| `badges` | 1 | 113 | 113 |

## Ключевые концепты

| Концепт | Файлов | Категория |
|---------|--------|-----------|
| `документ` | 937 | other |
| `сходство` | 746 | other |
| `смотрите` | 687 | other |
| `также` | 683 | other |
| `использование` | 637 | other |
| `anthropic` | 633 | other |
| `связанные` | 546 | other |
| `note` | 546 | other |

## Топ сущностей

| Сущность | Тип | Файлов |
|----------|-----|--------|
| `obsidian` | 📦 projects | 807 |
| `anthropic` | 👤 people | 739 |
| `nautilus` | 📦 projects | 542 |
| `lorenzo` | 📦 projects | 499 |
| `claude` | 👤 people | 455 |
| `svyazi` | 📦 projects | 392 |
| `mcp` | ⚙️ tech | 361 |
| `вк` | 🏢 orgs | 298 |
| `github` | 📦 projects | 263 |
| `bm25` | ⚙️ tech | 261 |
| `meta` | 🏢 orgs | 224 |
| `llm` | ⚙️ tech | 218 |

## Открытые вопросы

- -  Какие 5 архитектурных зазоров выделены в исследовании? [Содержан]
- -  Что входит в интеграционный контракт между слоями? [Содержание]
- -  Как реализован forensic RAG с доказуемостью? [Содержание]
- -  Что такое Evidence Envelope и зачем он нужен? [Содержание]
- -  Какие RAG-подходы сравниваются в документах? [Содержание]
- - Какие 5 архитектурных зазоров выделены в исследовании? [[Глобальный Q&A](QA.md)]
- - Что входит в интеграционный контракт между слоями? [[Глобальный Q&A](QA.md)]
- - Как реализован forensic RAG с доказуемостью? [[Глобальный Q&A](QA.md)]

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


<!-- backlinks -->

---

**Кто ссылается на этот документ (9):**
- [OUTLINE](OUTLINE.md)
- [QA](QA.md)
- [READABILITY](READABILITY.md)
- [READING_TIME](READING_TIME.md)
- [README](README.md)
- [SEARCH](SEARCH.md)
- [SEE_ALSO](SEE_ALSO.md)
- [TABLES](TABLES.md)
- _...ещё 1_


<!-- similar-docs -->

---

**Похожие документы:**
- [KNOWLEDGE_MAP](obsidian/KNOWLEDGE_MAP.md) (сходство 0.95)
- [QA](03-technology-combinations/QA.md) (сходство 0.35)
- [CROSS_SECTION](CROSS_SECTION.md) (сходство 0.34)

