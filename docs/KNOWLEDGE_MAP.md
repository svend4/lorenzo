# Карта базы знаний Lorenzo

<!-- toc-auto -->
## Содержание

- Основной раздел


<!-- summary -->
> Карта базы знаний Lorenzo — документ базы знаний репозитория Lorenzo.

<!-- tags: docs, reference, lorenzo -->

> [!NOTE]
> Документ содержит структурированную информацию из базы знаний репозитория Lorenzo.

<!-- alert-added -->


_Обновлено: 2026-05-10_

---

## Корпус

| Параметр | Значение |
|----------|----------|
| Документов | **1221** |
| Слов | **1,317,558** |
| Секций | **20** |
| RAG-чанков | **2063** (по 8 секциям) |

## Метрики качества

| Метрика | Значение |
|---------|----------|
| Здоровье репо | 90 |
| Средний балл документов | 93.9/100 |
| Словарное богатство (STTR) | 0.632 |
| Пассивный залог | 1.3% |
| Пустых секций | 3565 |
| Противоречий | 6846 |

## По секциям

| Секция | Файлов | Слов | Ср. слов/файл |
|--------|--------|------|---------------|
| `obsidian` | 1213 | 1,208,590 | 996 |
| `02-anthropic-vacancies` | 357 | 340,387 | 953 |
| `nautilus` | 255 | 170,214 | 667 |
| `anthropic-vacancies` | 111 | 44,273 | 398 |
| `04-ai-collaborations` | 17 | 27,773 | 1633 |
| `lorenzo-agent` | 62 | 27,071 | 436 |
| `svyazi-2-0` | 60 | 18,790 | 313 |
| `habr-unique-projects` | 56 | 18,500 | 330 |
| `technology-combinations` | 53 | 18,341 | 346 |
| `processing-guide` | 13 | 17,155 | 1319 |
| `05-habr-projects` | 16 | 14,590 | 911 |
| `01-svyazi` | 16 | 13,212 | 825 |
| `ai-collaborations` | 31 | 11,048 | 356 |
| `templates` | 24 | 6,930 | 288 |
| `contacts` | 17 | 4,908 | 288 |
| `03-technology-combinations` | 7 | 3,735 | 533 |
| `meta-scripting` | 7 | 3,084 | 440 |
| `autofilled` | 13 | 2,648 | 203 |
| `glossary` | 4 | 2,571 | 642 |
| `badges` | 1 | 44 | 44 |

## Ключевые концепты

| Концепт | Файлов | Категория |
|---------|--------|-----------|
| `документ` | 959 | other |
| `смотрите` | 675 | other |
| `также` | 674 | other |
| `anthropic` | 639 | other |
| `связанные` | 572 | other |
| `ссылки` | 491 | other |
| `note` | 487 | other |
| `claude` | 471 | other |

## Топ сущностей

| Сущность | Тип | Файлов |
|----------|-----|--------|
| `anthropic` | 👤 people | 654 |
| `claude` | 👤 people | 449 |
| `nautilus` | 📦 projects | 403 |
| `lorenzo` | 📦 projects | 386 |
| `mcp` | ⚙️ tech | 352 |
| `svyazi` | 📦 projects | 319 |
| `вк` | 🏢 orgs | 296 |
| `bm25` | ⚙️ tech | 253 |
| `github` | 📦 projects | 253 |
| `meta` | 🏢 orgs | 214 |
| `llm` | ⚙️ tech | 211 |
| `svend4` | 👤 people | 192 |

## Открытые вопросы

- ## Какие 5 архитектурных зазоров выделены в исследовании? [Раздел: 01-svyazi]
- ## Что входит в интеграционный контракт между слоями? [Какие 5 архитектурных зазоров выделены в иссл
- ## Как реализован forensic RAG с доказуемостью? [Что входит в интеграционный контракт между слоями?]
- ## Что такое Evidence Envelope и зачем он нужен? [Как реализован forensic RAG с доказуемостью?]
- ## Какие RAG-подходы сравниваются в документах? [Что такое Evidence Envelope и зачем он нужен?]
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

_Карта сгенерирована автоматически: 2026-05-10_

