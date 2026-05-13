# Карта базы знаний Lorenzo

<!-- toc-auto -->

> [!NOTE]
> Раздел `KNOWLEDGE_MAP` формируется автоматически из данных репозитория.

<!-- alert-added -->
<!-- tags: knowledge-map, docs -->


<!-- summary -->
> `KNOWLEDGE_MAP` — раздел документации проекта Lorenzo.


_Обновлено: 2026-05-13_

---

## Корпус

| Параметр | Значение |
|----------|----------|
| Документов | **1236** |
| Слов | **1,378,364** |
| Секций | **21** |
| RAG-чанков | **6864** (по 21 секциям) |

## Метрики качества

| Метрика | Значение |
|---------|----------|
| Здоровье репо | 90 |
| Средний балл документов | 97.9/100 |
| Словарное богатство (STTR) | 0.624 |
| Пассивный залог | 1.6% |
| Пустых секций | 3625 |
| Противоречий | 8934 |

## По секциям

| Секция | Файлов | Слов | Ср. слов/файл |
|--------|--------|------|---------------|
| `obsidian` | 1231 | 1,361,772 | 1106 |
| `02-anthropic-vacancies` | 357 | 341,899 | 957 |
| `nautilus` | 255 | 176,913 | 693 |
| `anthropic-vacancies` | 111 | 47,099 | 424 |
| `lorenzo-agent` | 62 | 28,615 | 461 |
| `04-ai-collaborations` | 17 | 27,853 | 1638 |
| `svyazi-2-0` | 60 | 20,715 | 345 |
| `habr-unique-projects` | 56 | 19,966 | 356 |
| `technology-combinations` | 53 | 19,585 | 369 |
| `processing-guide` | 13 | 17,453 | 1342 |
| `05-habr-projects` | 16 | 14,824 | 926 |
| `01-svyazi` | 16 | 13,329 | 833 |
| `ai-collaborations` | 31 | 12,182 | 392 |
| `templates` | 24 | 7,636 | 318 |
| `contacts` | 17 | 5,009 | 294 |
| `03-technology-combinations` | 7 | 3,781 | 540 |
| `letters` | 10 | 3,568 | 356 |
| `meta-scripting` | 7 | 3,331 | 475 |
| `autofilled` | 13 | 2,904 | 223 |
| `glossary` | 4 | 2,692 | 673 |
| `badges` | 1 | 102 | 102 |

## Ключевые концепты

| Концепт | Файлов | Категория |
|---------|--------|-----------|
| `документ` | 938 | other |
| `сходство` | 723 | other |
| `смотрите` | 688 | other |
| `также` | 683 | other |
| `использование` | 637 | other |
| `anthropic` | 631 | other |
| `note` | 550 | other |
| `связанные` | 549 | other |

## Топ сущностей

| Сущность | Тип | Файлов |
|----------|-----|--------|
| `obsidian` | 📦 projects | 775 |
| `anthropic` | 👤 people | 736 |
| `nautilus` | 📦 projects | 542 |
| `lorenzo` | 📦 projects | 511 |
| `claude` | 👤 people | 458 |
| `svyazi` | 📦 projects | 391 |
| `mcp` | ⚙️ tech | 360 |
| `вк` | 🏢 orgs | 297 |
| `bm25` | ⚙️ tech | 259 |
| `github` | 📦 projects | 259 |
| `meta` | 🏢 orgs | 224 |
| `llm` | ⚙️ tech | 217 |

## Открытые вопросы

- - Какие 5 архитектурных зазоров выделены в исследовании? [[Глобальный Q&A](QA.md)]
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

_Карта сгенерирована автоматически: 2026-05-13_


<!-- backlinks -->

---

**Кто ссылается на этот документ (11):**
- [BROKEN_LINKS](BROKEN_LINKS.md)
- [CROSS_SECTION](CROSS_SECTION.md)
- [OUTLINE](OUTLINE.md)
- [READABILITY](READABILITY.md)
- [READING_TIME](READING_TIME.md)
- [README](README.md)
- [SEARCH](SEARCH.md)
- [SEE_ALSO](SEE_ALSO.md)
- _...ещё 3_

