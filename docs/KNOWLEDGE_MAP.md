# Карта базы знаний Lorenzo

_Обновлено: 2026-05-10_

---

## Корпус

| Параметр | Значение |
|----------|----------|
| Документов | **1208** |
| Слов | **987,182** |
| Секций | **20** |
| RAG-чанков | **2063** (по 8 секциям) |

## Метрики качества

| Метрика | Значение |
|---------|----------|
| Здоровье репо | 80/100 |
| Средний балл документов | 72.2/100 |
| Словарное богатство (STTR) | 0.563 |
| Пассивный залог | 1.7% |
| Пустых секций | 1589 |
| Противоречий | 3683 |

## По секциям

| Секция | Файлов | Слов | Ср. слов/файл |
|--------|--------|------|---------------|
| `obsidian` | 521 | 669,804 | 1285 |
| `02-anthropic-vacancies` | 357 | 319,981 | 896 |
| `nautilus` | 255 | 148,539 | 582 |
| `anthropic-vacancies` | 111 | 31,046 | 279 |
| `04-ai-collaborations` | 17 | 26,608 | 1565 |
| `lorenzo-agent` | 62 | 20,013 | 322 |
| `processing-guide` | 13 | 16,675 | 1282 |
| `habr-unique-projects` | 56 | 13,445 | 240 |
| `technology-combinations` | 53 | 13,381 | 252 |
| `svyazi-2-0` | 59 | 12,925 | 219 |
| `01-svyazi` | 16 | 11,571 | 723 |
| `05-habr-projects` | 10 | 9,358 | 935 |
| `ai-collaborations` | 30 | 8,257 | 275 |
| `templates` | 24 | 5,139 | 214 |
| `contacts` | 15 | 3,747 | 249 |
| `03-technology-combinations` | 7 | 3,182 | 454 |
| `meta-scripting` | 7 | 2,594 | 370 |
| `glossary` | 4 | 2,300 | 575 |
| `autofilled` | 13 | 2,058 | 158 |
| `badges` | 1 | 44 | 44 |

## Ключевые концепты

| Концепт | Файлов | Категория |
|---------|--------|-----------|
| `документы` | 318 | other |
| `anthropic` | 273 | other |
| `auto` | 264 | other |
| `упоминается` | 247 | other |
| `связанные` | 187 | other |
| `readme` | 184 | other |
| `summary` | 165 | other |
| `анализ` | 162 | other |

## Топ сущностей

| Сущность | Тип | Файлов |
|----------|-----|--------|
| `anthropic` | 👤 people | 744 |
| `nautilus` | 📦 projects | 471 |
| `svyazi` | 📦 projects | 299 |
| `вк` | 🏢 orgs | 270 |
| `github` | 📦 projects | 238 |
| `claude` | 👤 people | 181 |
| `mcp` | ⚙️ tech | 159 |
| `rag` | ⚙️ tech | 140 |
| `svend4` | 👤 people | 139 |
| `agentfs` | 📦 projects | 133 |
| `cardindex` | 📦 projects | 126 |
| `lorenzo` | 📦 projects | 124 |

## Открытые вопросы

- **Интерфейс** — есть ли понятный публичный API/контракт для интеграции?
- **Доказуемость** — можно ли проверить, что слой работает правильно?
- ше задавать вопрос о memory write policy и conservative consolidation: *что в вашей архитектуре оказ
- о memory write policy и conservative consolidation: *что в вашей архитектуре оказалось критичнее для
- Вопрос: как вы оцениваете эту многоуровневую агентную архитектуру, где каждый член команды получает 
- как вы оцениваете эту многоуровневую агентную архитектуру, где каждый член команды получает персонал
- Как двойственная архитектура избегает этого?
- Как бы выглядел Слой B идеально?

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
- [HEALTH](docs/HEALTH.md)
- [STATS](docs/STATS.md)
- [WORD_FREQ](docs/WORD_FREQ.md)
- [SENTIMENT](docs/SENTIMENT.md)

