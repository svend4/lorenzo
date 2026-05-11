# Сломанные внутренние ссылки

<!-- summary -->
> Сломанных ссылок: **74**, пропущено: 0

<!-- tags: quality, links, validation, broken-links -->

<!-- toc-auto -->
## Содержание

- [Сломанные ссылки](#сломанные-внутренние-ссылки)
- [Общие показатели](#общие-показатели)
- [Внешние URL](#внешние-url)
- [Использование](#использование)
- [Смотрите также](#смотрите-также)

> [!WARNING]
> Найдено 74 сломанных ссылок — требуют исправления.

<!-- alert-added -->

**Найдено:** 74 проблем, 0 пропущено (длинный путь)


Скрипт `improve_broken_links.py` проверяет все внутренние ссылки в папке `docs/`, исключая автоматически генерируемые разделы: `obsidian/`, `confluence/`, `templates/` и `autofilled/`. Проверяются ссылки на файлы (существование пути) и якоря (существование заголовка). Ссылки с путём длиннее 240 символов пропускаются из-за ограничений операционной системы и сохраняются в `bad_links.json`.

Якоря проверяются по алгоритму GitHub-style: заголовки переводятся в нижний регистр, удаляются специальные символы, пробелы заменяются дефисами. Дублирующиеся заголовки получают суффиксы `-1`, `-2` аналогично GitHub.


Автоматическое исправление (`--fix`) ищет файл с таким же именем в `docs/` и заменяет ссылку правильным относительным путём. Режим `--dry-run` показывает запланированные исправления без записи в файлы. Флаг `--section РАЗДЕЛ` ограничивает проверку конкретной подпапкой. Результаты записываются в `docs/BROKEN_LINKS.md` и опционально в `docs/bad_links.json`.


## Общие показатели

- Проверено файлов: большинство `.md` в `docs/`
- Сломанных ссылок: **74**
- Пропущено (длинный путь): **0**
- Внешние URL не проверяются (список формируется без запросов)

| Файл | Текст ссылки | Цель | Проблема |
|------|--------------|------|----------|
| `docs/05-habr-projects/knowledge/agentfs.md` | Описание | `#описание` | якорь не найден |
| `docs/05-habr-projects/knowledge/agentfs.md` | Ключевые компоненты | `#ключевые-компоненты` | якорь не найден |
| `docs/05-habr-projects/knowledge/knowledge-space.md` | Описание | `#описание` | якорь не найден |
| `docs/05-habr-projects/knowledge/knowledge-space.md` | Ключевые компоненты | `#ключевые-компоненты` | якорь не найден |
| `docs/05-habr-projects/knowledge/knowledge-space.md` | Описание | `#описание` | якорь не найден |
| `docs/05-habr-projects/knowledge/knowledge-space.md` | Ключевые компоненты | `#ключевые-компоненты` | якорь не найден |
| `docs/05-habr-projects/knowledge/mclaude.md` | Описание | `#описание` | якорь не найден |
| `docs/05-habr-projects/knowledge/mclaude.md` | Ключевые компоненты | `#ключевые-компоненты` | якорь не найден |
| `docs/05-habr-projects/knowledge/mclaude.md` | Описание | `#описание` | якорь не найден |
| `docs/05-habr-projects/knowledge/mclaude.md` | Ключевые компоненты | `#ключевые-компоненты` | якорь не найден |
| `docs/05-habr-projects/knowledge/research-docs-liteparse.md` | Описание | `#описание` | якорь не найден |
| `docs/05-habr-projects/knowledge/research-docs-liteparse.md` | Ключевые компоненты | `#ключевые-компоненты` | якорь не найден |
| `docs/05-habr-projects/knowledge/rufler.md` | Описание | `#описание` | якорь не найден |
| `docs/05-habr-projects/knowledge/rufler.md` | Ключевые компоненты | `#ключевые-компоненты` | якорь не найден |
| `docs/05-habr-projects/knowledge/rufler.md` | Описание | `#описание` | якорь не найден |
| `docs/05-habr-projects/knowledge/rufler.md` | Ключевые компоненты | `#ключевые-компоненты` | якорь не найден |
| `docs/05-habr-projects/memory/agent-memory-mcp.md` | Описание | `#описание` | якорь не найден |
| `docs/05-habr-projects/memory/agent-memory-mcp.md` | Ключевые компоненты | `#ключевые-компоненты` | якорь не найден |
| `docs/READING_LIST.md` | Все таблицы репозитория | `docs/TABLES.md` | файл не существует |
| `docs/READING_LIST.md` | Outline базы знаний | `docs/OUTLINE.md` | файл не существует |
| `docs/READING_LIST.md` | Читаемость документов (Flesch- | `docs/READABILITY.md` | файл не существует |
| `docs/READING_LIST.md` | Время чтения документов | `docs/READING_TIME.md` | файл не существует |
| `docs/READING_LIST.md` | Приложение C: Образец Специфик | `docs/02-anthropic-vacancies/341-приложен` | файл не существует |
| `docs/READING_LIST.md` | Интегральный анализ профиля sv | `docs/02-anthropic-vacancies/01-интеграль` | файл не существует |
| `docs/READING_LIST.md` | Обратная связь | `docs/02-anthropic-vacancies/133-обратная` | файл не существует |
| `docs/READING_LIST.md` | Глоссарий понятий | `docs/CONCEPTS.md` | файл не существует |
| `docs/READING_LIST.md` | Карта происхождения текстов | `docs/SOURCE_MAP.md` | файл не существует |
| `docs/READING_LIST.md` | Введение | `docs/04-ai-collaborations/00-intro.md` | файл не существует |
| `docs/READING_LIST.md` | Что такое Вариант C — Concept  | `docs/02-anthropic-vacancies/342-что-тако` | файл не существует |
| `docs/READING_LIST.md` | Карта репозитория Lorenzo | `docs/SITEMAP.md` | файл не существует |
| `docs/READING_LIST.md` | Diff базы знаний между версиям | `docs/VERSION_DIFF.md` | файл не существует |
| `docs/READING_LIST.md` | Claude hat geantwortet: Хорошо | `docs/nautilus/community-discussions/agen` | файл не существует |
| `docs/READING_LIST.md` | ⬡ | `docs/02-anthropic-vacancies/69-section.m` | файл не существует |
| `docs/READING_LIST.md` | Приложение C: Образец Специфик | `docs/02-anthropic-vacancies/341-приложен` | файл не существует |
| `docs/READING_LIST.md` | Интегральный анализ профиля sv | `docs/02-anthropic-vacancies/01-интеграль` | файл не существует |
| `docs/READING_LIST.md` | Обратная связь | `docs/02-anthropic-vacancies/133-обратная` | файл не существует |
| `docs/READING_LIST.md` | Что такое Вариант C — Concept  | `docs/02-anthropic-vacancies/342-что-тако` | файл не существует |
| `docs/READING_LIST.md` | ⬡ | `docs/02-anthropic-vacancies/69-section.m` | файл не существует |
| `docs/READING_LIST.md` | Введение | `docs/04-ai-collaborations/00-intro.md` | файл не существует |
| `docs/READING_LIST.md` | Глоссарий понятий | `docs/CONCEPTS.md` | файл не существует |
| `docs/READING_LIST.md` | Outline базы знаний | `docs/OUTLINE.md` | файл не существует |
| `docs/READING_LIST.md` | Читаемость документов (Flesch- | `docs/READABILITY.md` | файл не существует |
| `docs/READING_LIST.md` | Время чтения документов | `docs/READING_TIME.md` | файл не существует |
| `docs/READING_LIST.md` | Карта репозитория Lorenzo | `docs/SITEMAP.md` | файл не существует |
| `docs/READING_LIST.md` | Карта происхождения текстов | `docs/SOURCE_MAP.md` | файл не существует |
| `docs/READING_LIST.md` | Все таблицы репозитория | `docs/TABLES.md` | файл не существует |
| `docs/READING_LIST.md` | Diff базы знаний между версиям | `docs/VERSION_DIFF.md` | файл не существует |
| `docs/READING_LIST.md` | Claude hat geantwortet: Хорошо | `docs/nautilus/community-discussions/agen` | файл не существует |
| `docs/SENTINEL.md` | HTTP без TLS | `#http-без-tls` | якорь не найден |
| `docs/TABLES.md` | @handle | `obsidian/templates/ссылка` | файл не существует |

_...и ещё 24 проблем_

## Внешние URL (452 уникальных)

_Внешние ссылки не проверяются автоматически — требуют ручной проверки._

- http://localhost:8000
- http://localhost:8000`
- http://localhost:8000``
- http://localhost:8000```
- http://localhost:8000````
- http://localhost:8000`````
- http://localhost:8000``````
- http://localhost:8080
- http://localhost:8080`
- http://localhost:8080``
- http://localhost:8080```
- http://localhost:8080````
- http://localhost:8080`````
- http://localhost:8080``````
- http://localhost:8083/api/ask
- http://localhost:8083/api/ask`
- http://localhost:8083/api/benchmark
- http://localhost:8083/api/benchmark`
- http://localhost:8083/api/cards
- http://localhost:8083/api/cards`
- http://localhost:8083/api/collabs
- http://localhost:8083/api/collabs`
- http://localhost:8083/api/health
- http://localhost:8083/api/health`
- http://localhost:8083/api/search
- http://localhost:8083/api/search`
- http://localhost:8083/docs
- http://localhost:8083/docs`
- http://localhost:8083/v1
- http://localhost:8083/v1/chat/completions

## Использование

```bash
python scripts/improve_broken_links.py
```

```bash
# Автоматическое исправление битых ссылок
python scripts/improve_broken_links.py --fix
```


## Смотрите также

- [HEALTH](HEALTH.md) — общее здоровье репозитория
- [METRICS](METRICS.md) — метрики качества документов
- [VALIDATION](VALIDATION.md) — валидация структуры

<!-- see-also -->

---

**Смотрите также:**
- [READING_LIST](READING_LIST.md)
- [KEYWORD_INDEX](KEYWORD_INDEX.md)
- [KNOWLEDGE_MAP](KNOWLEDGE_MAP.md)
- [DIGEST_WEEKLY](DIGEST_WEEKLY.md)

