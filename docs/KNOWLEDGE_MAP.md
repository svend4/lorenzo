# Карта базы знаний Lorenzo

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
| Документов | **1221** |
| Слов | **1,371,771** |
| Секций | **20** |
| RAG-чанков | **2063** (по 8 секциям) |

## Метрики качества

| Метрика | Значение |
|---------|----------|
| Здоровье репо | 100/100 |
| Средний балл документов | 100.0/100 |
| Словарное богатство (STTR) | 0.627 |
| Пассивный залог | 2.0% |
| Пустых секций | 3626 |
| Противоречий | 7880 |

## По секциям

| Секция | Файлов | Слов | Ср. слов/файл |
|--------|--------|------|---------------|
| `obsidian` | 1213 | 1,220,254 | 1005 |
| `02-anthropic-vacancies` | 357 | 341,436 | 956 |
| `nautilus` | 255 | 172,062 | 674 |
| `anthropic-vacancies` | 111 | 45,124 | 406 |
| `04-ai-collaborations` | 17 | 27,978 | 1645 |
| `lorenzo-agent` | 62 | 27,676 | 446 |
| `svyazi-2-0` | 60 | 19,692 | 328 |
| `habr-unique-projects` | 56 | 18,966 | 338 |
| `technology-combinations` | 53 | 18,645 | 351 |
| `processing-guide` | 13 | 17,401 | 1338 |
| `05-habr-projects` | 16 | 14,769 | 923 |
| `01-svyazi` | 16 | 13,370 | 835 |
| `ai-collaborations` | 31 | 11,627 | 375 |
| `templates` | 24 | 7,312 | 304 |
| `contacts` | 17 | 5,004 | 294 |
| `03-technology-combinations` | 7 | 3,835 | 547 |
| `meta-scripting` | 7 | 3,246 | 463 |
| `autofilled` | 13 | 2,670 | 205 |
| `glossary` | 4 | 2,648 | 662 |
| `badges` | 1 | 102 | 102 |

## Ключевые концепты

| Концепт | Файлов | Категория |
|---------|--------|-----------|
| `документ` | 953 | other |
| `смотрите` | 705 | other |
| `также` | 701 | other |
| `использование` | 656 | other |
| `anthropic` | 630 | other |
| `связанные` | 563 | other |
| `note` | 545 | other |
| `репозитория` | 492 | project |

## Топ сущностей

| Сущность | Тип | Файлов |
|----------|-----|--------|
| `anthropic` | 👤 people | 656 |
| `lorenzo` | 📦 projects | 515 |
| `claude` | 👤 people | 451 |
| `nautilus` | 📦 projects | 405 |
| `svyazi` | 📦 projects | 381 |
| `mcp` | ⚙️ tech | 353 |
| `вк` | 🏢 orgs | 298 |
| `bm25` | ⚙️ tech | 254 |
| `github` | 📦 projects | 254 |
| `meta` | 🏢 orgs | 219 |
| `llm` | ⚙️ tech | 212 |
| `svend4` | 👤 people | 192 |

## Открытые вопросы

- -  Какие 5 архитектурных зазоров выделены в исследовании? [Contents]
- -  Что входит в интеграционный контракт между слоями? [Contents]
- -  Как реализован forensic RAG с доказуемостью? [Contents]
- -  Что такое Evidence Envelope и зачем он нужен? [Contents]
- -  Какие RAG-подходы сравниваются в документах? [Contents]
- - Какие 5 архитектурных зазоров выделены в исследовании? [[Svyazi 2.0 — Спецификация прототипа](PROT
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

