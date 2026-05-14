# Сломанные внутренние ссылки

<!-- summary -->
> Сломанных ссылок: **18**, пропущено: 0

<!-- tags: quality, links, validation, broken-links -->

<!-- toc-auto -->
## Содержание

- [Сломанные ссылки](#сломанные-внутренние-ссылки)
- [Общие показатели](#общие-показатели)
- [Внешние URL](#внешние-url)
- [Использование](#использование)
- [Смотрите также](#смотрите-также)

> [!WARNING]
> Найдено 18 сломанных ссылок — требуют исправления.

<!-- alert-added -->

**Найдено:** 18 проблем, 0 пропущено (длинный путь)


Скрипт `improve_broken_links.py` проверяет все внутренние ссылки в папке `docs/`, исключая автоматически генерируемые разделы: `obsidian/`, `confluence/`, `templates/` и `autofilled/`. Проверяются ссылки на файлы (существование пути) и якоря (существование заголовка). Ссылки с путём длиннее 240 символов пропускаются из-за ограничений операционной системы и сохраняются в `bad_links.json`.

Якоря проверяются по алгоритму GitHub-style: заголовки переводятся в нижний регистр, удаляются специальные символы, пробелы заменяются дефисами. Дублирующиеся заголовки получают суффиксы `-1`, `-2` аналогично GitHub.


Автоматическое исправление (`--fix`) ищет файл с таким же именем в `docs/` и заменяет ссылку правильным относительным путём. Режим `--dry-run` показывает запланированные исправления без записи в файлы. Флаг `--section РАЗДЕЛ` ограничивает проверку конкретной подпапкой. Результаты записываются в `docs/BROKEN_LINKS.md` и опционально в `docs/bad_links.json`.


## Общие показатели

- Проверено файлов: большинство `.md` в `docs/`
- Сломанных ссылок: **18**
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

## Внешние URL (37 уникальных)

_Внешние ссылки не проверяются автоматически — требуют ручной проверки._

- https://forum.[obsidian
- https://habr.com/ru/articles/1002138/
- https://habr.com/ru/articles/1005776/
- https://habr.com/ru/articles/1006602/
- https://habr.com/ru/articles/1006622/
- https://habr.com/ru/articles/1007122/
- https://habr.com/ru/articles/1009538/
- https://habr.com/ru/articles/1009608/
- https://habr.com/ru/articles/1009958/
- https://habr.com/ru/articles/1010198/
- https://habr.com/ru/articles/1010478/
- https://habr.com/ru/articles/1016096/
- https://habr.com/ru/articles/1017200/
- https://habr.com/ru/articles/1019588/
- https://habr.com/ru/articles/1020598/
- https://habr.com/ru/articles/1020860/
- https://habr.com/ru/articles/1023446/
- https://habr.com/ru/articles/1024634/
- https://habr.com/ru/articles/1024884/comments/
- https://habr.com/ru/articles/1027210/
- https://habr.com/ru/articles/1027382/
- https://habr.com/ru/articles/1027658/
- https://habr.com/ru/articles/1027878/
- https://habr.com/ru/articles/893356/
- https://habr.com/ru/articles/938626/
- https://habr.com/ru/articles/943498/
- https://habr.com/ru/articles/955798/
- https://habr.com/ru/articles/975414/
- https://habr.com/ru/articles/983684/
- https://habr.com/ru/articles/996144/

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

<!-- backlinks -->

---

**Кто ссылается на этот документ (13):**
- [03-component-catalog](01-svyazi/03-component-catalog.md)
- [CITATION_INDEX](CITATION_INDEX.md)
- [HEALTH](HEALTH.md)
- [KNOWLEDGE_MAP](KNOWLEDGE_MAP.md)
- [METRICS](METRICS.md)
- [READABILITY](READABILITY.md)
- [READING_LIST](READING_LIST.md)
- [READING_TIME](READING_TIME.md)
- _...ещё 5_


<!-- see-also -->

---

**Смотрите также:**
- [KNOWLEDGE_MAP](KNOWLEDGE_MAP.md)
- [HEALTH](HEALTH.md)
- [METRICS](METRICS.md)
- [CITATION_INDEX](CITATION_INDEX.md)

