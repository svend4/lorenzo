# Сломанные внутренние ссылки

<!-- summary -->
> Сломанных ссылок: **80**, пропущено: 0

<!-- tags: quality, links, validation, broken-links -->

<!-- toc-auto -->
## Содержание

- [Сломанные ссылки](#сломанные-внутренние-ссылки)
- [Общие показатели](#общие-показатели)
- [Внешние URL](#внешние-url)
- [Использование](#использование)
- [Смотрите также](#смотрите-также)

> [!WARNING]
> Найдено 80 сломанных ссылок — требуют исправления.

<!-- alert-added -->

**Найдено:** 80 проблем, 0 пропущено (длинный путь)


Скрипт `improve_broken_links.py` проверяет все внутренние ссылки в папке `docs/`, исключая автоматически генерируемые разделы: `obsidian/`, `confluence/`, `templates/` и `autofilled/`. Проверяются ссылки на файлы (существование пути) и якоря (существование заголовка). Ссылки с путём длиннее 240 символов пропускаются из-за ограничений операционной системы и сохраняются в `bad_links.json`.

Якоря проверяются по алгоритму GitHub-style: заголовки переводятся в нижний регистр, удаляются специальные символы, пробелы заменяются дефисами. Дублирующиеся заголовки получают суффиксы `-1`, `-2` аналогично GitHub.


Автоматическое исправление (`--fix`) ищет файл с таким же именем в `docs/` и заменяет ссылку правильным относительным путём. Режим `--dry-run` показывает запланированные исправления без записи в файлы. Флаг `--section РАЗДЕЛ` ограничивает проверку конкретной подпапкой. Результаты записываются в `docs/BROKEN_LINKS.md` и опционально в `docs/bad_links.json`.


## Общие показатели

- Проверено файлов: большинство `.md` в `docs/`
- Сломанных ссылок: **80**
- Пропущено (длинный путь): **0**
- Внешние URL не проверяются (список формируется без запросов)

| Файл | Текст ссылки | Цель | Проблема |
|------|--------------|------|----------|
| `docs/01-svyazi/README.md` | ensembles/ | `ensembles/` | файл не существует |
| `docs/02-anthropic-vacancies/README.md` | clusters/ | `clusters/` | файл не существует |
| `docs/04-ai-collaborations/README.md` | ensembles/ | `ensembles/` | файл не существует |
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
| `docs/READABILITY.md` | 10-essence | `obsidian/02-anthropic-vacancies/10-essen` | файл не существует |
| `docs/READABILITY.md` | 101-q6-отображение | `obsidian/02-anthropic-vacancies/101-q6-о` | файл не существует |
| `docs/READABILITY.md` | 11-native-format | `obsidian/02-anthropic-vacancies/11-nativ` | файл не существует |
| `docs/READABILITY.md` | 14-bridges | `obsidian/02-anthropic-vacancies/14-bridg` | файл не существует |
| `docs/READABILITY.md` | 15-author-contact | `obsidian/02-anthropic-vacancies/15-autho` | файл не существует |
| `docs/READABILITY.md` | 29-essence | `obsidian/02-anthropic-vacancies/29-essen` | файл не существует |
| `docs/READABILITY.md` | 30-native-format | `obsidian/02-anthropic-vacancies/30-nativ` | файл не существует |
| `docs/READABILITY.md` | 32-angle-perspective | `obsidian/02-anthropic-vacancies/32-angle` | файл не существует |
| `docs/READABILITY.md` | 33-author | `obsidian/02-anthropic-vacancies/33-autho` | файл не существует |
| `docs/READABILITY.md` | 99-описание | `obsidian/02-anthropic-vacancies/99-описа` | файл не существует |
| `docs/READABILITY.md` | minimal-test-card | `obsidian/04-ai-collaborations/minimal-te` | файл не существует |
| `docs/READABILITY.md` | 66-english-below | `obsidian/02-anthropic-vacancies/66-engli` | файл не существует |
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
| `docs/READING_LIST.md` | Claude hat geantwortet: Хорошо | `docs/nautilus/community-discussions/agen` | файл не существует |
| `docs/READING_LIST.md` | ⬡ | `docs/02-anthropic-vacancies/69-section.m` | файл не существует |
| `docs/READING_LIST.md` | Closing | `docs/02-anthropic-vacancies/165-closing.` | файл не существует |
| `docs/READING_LIST.md` | Приложение C: Образец Специфик | `docs/02-anthropic-vacancies/341-приложен` | файл не существует |
| `docs/READING_LIST.md` | Интегральный анализ профиля sv | `docs/02-anthropic-vacancies/01-интеграль` | файл не существует |

_...и ещё 30 проблем_

## Внешние URL (632 уникальных)

_Внешние ссылки не проверяются автоматически — требуют ручной проверки._

- http://localhos
- http://localhost:8
- http://localhost:8000
- http://localhost:8000`
- http://localhost:8000``
- http://localhost:8000```
- http://localhost:8000````
- http://localhost:8000`````
- http://localhost:8000``````
- http://localhost:8000```````
- http://localhost:8000````````
- http://localhost:8000`````````
- http://localhost:8080
- http://localhost:8080`
- http://localhost:8080``
- http://localhost:8080```
- http://localhost:8080````
- http://localhost:8080`````
- http://localhost:8080``````
- http://localhost:8080```````
- http://localhost:8080````````
- http://localhost:8080`````````
- http://localhost:8083/api/ask
- http://localhost:8083/api/ask`
- http://localhost:8083/api/ask``
- http://localhost:8083/api/ask```
- http://localhost:8083/api/ask````
- http://localhost:8083/api/benchmark
- http://localhost:8083/api/benchmark`
- http://localhost:8083/api/benchmark``

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
- [VERSION_DIFF](VERSION_DIFF.md)
- [KNOWLEDGE_MAP](KNOWLEDGE_MAP.md)
- [CITATION_INDEX](CITATION_INDEX.md)

