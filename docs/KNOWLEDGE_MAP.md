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
> Раздел `KNOWLEDGE_MAP` автоматически формируется из данных репозитория.

<!-- alert-added -->
<!-- tags: knowledge-map, docs -->


<!-- summary -->
> `KNOWLEDGE_MAP` — раздел документации проекта Lorenzo.


_Обновлено: 2026-05-11_

---

## Корпус

| Параметр | Значение |
|----------|----------|
| Документов | **1221** |
| Слов | **1,352,893** |
| Секций | **20** |
| RAG-чанков | **2063** (по 8 секциям) |

## Метрики качества

| Метрика | Значение |
|---------|----------|
| Здоровье репо | 90 |
| Средний балл документов | 95.0/100 |
| Словарное богатство (STTR) | 0.631 |
| Пассивный залог | 1.3% |
| Пустых секций | 3565 |
| Противоречий | 7815 |

## По секциям

| Секция | Файлов | Слов | Ср. слов/файл |
|--------|--------|------|---------------|
| `obsidian` | 1213 | 1,218,913 | 1004 |
| `02-anthropic-vacancies` | 357 | 340,572 | 953 |
| `nautilus` | 255 | 170,474 | 668 |
| `anthropic-vacancies` | 111 | 44,300 | 399 |
| `04-ai-collaborations` | 17 | 27,749 | 1632 |
| `lorenzo-agent` | 62 | 27,075 | 436 |
| `svyazi-2-0` | 60 | 19,075 | 317 |
| `habr-unique-projects` | 56 | 18,518 | 330 |
| `technology-combinations` | 53 | 18,347 | 346 |
| `processing-guide` | 13 | 17,155 | 1319 |
| `05-habr-projects` | 16 | 14,590 | 911 |
| `01-svyazi` | 16 | 13,212 | 825 |
| `ai-collaborations` | 31 | 11,307 | 364 |
| `templates` | 24 | 6,930 | 288 |
| `contacts` | 17 | 4,886 | 287 |
| `03-technology-combinations` | 7 | 3,709 | 529 |
| `meta-scripting` | 7 | 3,086 | 440 |
| `autofilled` | 13 | 2,648 | 203 |
| `glossary` | 4 | 2,573 | 643 |
| `badges` | 1 | 44 | 44 |

## Ключевые концепты

| Концепт | Файлов | Категория |
|---------|--------|-----------|
| `документ` | 990 | other |
| `смотрите` | 685 | other |
| `также` | 685 | other |
| `anthropic` | 636 | other |
| `связанные` | 564 | other |
| `note` | 498 | other |
| `ссылки` | 483 | other |
| `claude` | 469 | other |

## Топ сущностей

| Сущность | Тип | Файлов |
|----------|-----|--------|
| `anthropic` | 👤 people | 651 |
| `claude` | 👤 people | 449 |
| `nautilus` | 📦 projects | 403 |
| `lorenzo` | 📦 projects | 396 |
| `mcp` | ⚙️ tech | 353 |
| `svyazi` | 📦 projects | 323 |
| `вк` | 🏢 orgs | 298 |
| `bm25` | ⚙️ tech | 257 |
| `github` | 📦 projects | 253 |
| `meta` | 🏢 orgs | 216 |
| `llm` | ⚙️ tech | 210 |
| `svend4` | 👤 people | 191 |

## Открытые вопросы

- - Какие 5 архитектурных зазоров выделены в исследовании? [[Svyazi 2.0 — Спецификация прототипа](PROT
- - Что входит в интеграционный контракт между слоями? [[Глобальный Q&A](QA.md)]
- - Как реализован forensic RAG с доказуемостью? [[Глобальный Q&A](QA.md)]
- - Что такое Evidence Envelope и зачем он нужен? [[Глобальный Q&A](QA.md)]
- - Какие RAG-подходы сравниваются в документах? [[Глобальный Q&A](QA.md)]
- ## Какие 5 архитектурных зазоров выделены в исследовании? [Глобальный Q&A]
- ## Что входит в интеграционный контракт между слоями? [Какие 5 архитектурных зазоров выделены в иссл
- ## Как реализован forensic RAG с доказуемостью? [Что входит в интеграционный контракт между слоями?]

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

**Кто ссылается на этот документ (8):**
- [OUTLINE](OUTLINE.md)
- [READABILITY](READABILITY.md)
- [READING_TIME](READING_TIME.md)
- [README](README.md)
- [SEARCH](SEARCH.md)
- [SEE_ALSO](SEE_ALSO.md)
- [TABLES](TABLES.md)
- [QA](svyazi-2-0/QA.md)

