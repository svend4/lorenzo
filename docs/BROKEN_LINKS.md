# Сломанные внутренние ссылки

<!-- summary -->
> Сломанных ссылок: **3329**, пропущено: 0

<!-- tags: quality, links, validation, broken-links -->

<!-- toc-auto -->
## Содержание

- [Сломанные ссылки](#сломанные-внутренние-ссылки)
- [Общие показатели](#общие-показатели)
- [Внешние URL](#внешние-url)
- [Использование](#использование)
- [Смотрите также](#смотрите-также)

> [!WARNING]
> Найдено 3329 сломанных ссылок — требуют исправления.

<!-- alert-added -->

**Найдено:** 3329 проблем, 0 пропущено (длинный путь)


Скрипт `improve_broken_links.py` проверяет все внутренние ссылки в папке `docs/`, исключая автоматически генерируемые разделы: `obsidian/`, `confluence/`, `templates/` и `autofilled/`. Проверяются ссылки на файлы (существование пути) и якоря (существование заголовка). Ссылки с путём длиннее 240 символов пропускаются из-за ограничений операционной системы и сохраняются в `bad_links.json`.

Якоря проверяются по алгоритму GitHub-style: заголовки переводятся в нижний регистр, удаляются специальные символы, пробелы заменяются дефисами. Дублирующиеся заголовки получают суффиксы `-1`, `-2` аналогично GitHub.


Автоматическое исправление (`--fix`) ищет файл с таким же именем в `docs/` и заменяет ссылку правильным относительным путём. Режим `--dry-run` показывает запланированные исправления без записи в файлы. Флаг `--section РАЗДЕЛ` ограничивает проверку конкретной подпапкой. Результаты записываются в `docs/BROKEN_LINKS.md` и опционально в `docs/bad_links.json`.


## Общие показатели

- Проверено файлов: большинство `.md` в `docs/`
- Сломанных ссылок: **3329**
- Пропущено (длинный путь): **0**
- Внешние URL не проверяются (список формируется без запросов)

| Файл | Текст ссылки | Цель | Проблема |
|------|--------------|------|----------|
| `docs/01-svyazi/00-intro-part2.md` | SEARCH_RESULTS | `../obsidian/SEARCH_RESULTS.md` | файл не существует |
| `docs/01-svyazi/README.md` | ensembles/ | `ensembles/` | файл не существует |
| `docs/02-anthropic-vacancies/113-6-почему-это-валидный-паттерн-для-ai-assisted-work.md` | 07-why-valid-for-ai | `../obsidian/nautilus/review-methodology/` | файл не существует |
| `docs/02-anthropic-vacancies/118-appendix-a-шаблон-для-header-warning.md` | 12-appendix-a-header-warning | `../obsidian/nautilus/review-methodology/` | файл не существует |
| `docs/02-anthropic-vacancies/120-главные-технические-риски.md` | 14-main-technical-risks | `../obsidian/nautilus/review-methodology/` | файл не существует |
| `docs/02-anthropic-vacancies/191-1-синдром-золушки-почему-качество-остаётся-невидим.md` | 01-sindrom-zolushki | `../obsidian/nautilus/representative-agen` | файл не существует |
| `docs/02-anthropic-vacancies/192-2-исторические-прецеденты-агенты-как-цивилизационн.md` | 02-istoricheskie-pretsedenty | `../obsidian/nautilus/representative-agen` | файл не существует |
| `docs/02-anthropic-vacancies/197-7-управление-и-надзор.md` | 07-upravlenie-nadzor | `../obsidian/nautilus/representative-agen` | файл не существует |
| `docs/02-anthropic-vacancies/250-bridging-the-gap-between-profession-wide-and-indiv.md` | 13-communications | `../obsidian/anthropic-vacancies/clusters` | файл не существует |
| `docs/02-anthropic-vacancies/347-твоя-миссия.md` | 03-tvoya-missiya | `../obsidian/lorenzo-agent/03-tvoya-missi` | файл не существует |
| `docs/02-anthropic-vacancies/349-твоя-личность.md` | 05-tvoya-lichnost | `../obsidian/lorenzo-agent/05-tvoya-lichn` | файл не существует |
| `docs/02-anthropic-vacancies/357-твоя-коммуникация-в-outreach.md` | 13-outreach-communication | `../obsidian/lorenzo-agent/13-outreach-co` | файл не существует |
| `docs/02-anthropic-vacancies/359-твои-anti-patterns.md` | 15-anti-patterns | `../obsidian/lorenzo-agent/15-anti-patter` | файл не существует |
| `docs/02-anthropic-vacancies/362-когда-сомневаешься-escalate-к-max.md` | 18-escalate-to-max | `../obsidian/lorenzo-agent/18-escalate-to` | файл не существует |
| `docs/02-anthropic-vacancies/README.md` | clusters/ | `clusters/` | файл не существует |
| `docs/03-technology-combinations/README.md` | SEARCH_RESULTS | `../obsidian/SEARCH_RESULTS.md` | файл не существует |
| `docs/04-ai-collaborations/README.md` | ensembles/ | `ensembles/` | файл не существует |
| `docs/05-habr-projects/knowledge/agentfs.md` | Описание | `#описание` | якорь не найден |
| `docs/05-habr-projects/knowledge/agentfs.md` | Ключевые компоненты | `#ключевые-компоненты` | якорь не найден |
| `docs/05-habr-projects/knowledge/agentfs.md` | agentfs | `../../obsidian/05-habr-projects/knowledg` | файл не существует |
| `docs/05-habr-projects/knowledge/agentfs.md` | mclaude | `../../obsidian/05-habr-projects/knowledg` | файл не существует |
| `docs/05-habr-projects/knowledge/knowledge-space.md` | Описание | `#описание` | якорь не найден |
| `docs/05-habr-projects/knowledge/knowledge-space.md` | Ключевые компоненты | `#ключевые-компоненты` | якорь не найден |
| `docs/05-habr-projects/knowledge/knowledge-space.md` | Описание | `#описание` | якорь не найден |
| `docs/05-habr-projects/knowledge/knowledge-space.md` | Ключевые компоненты | `#ключевые-компоненты` | якорь не найден |
| `docs/05-habr-projects/knowledge/knowledge-space.md` | knowledge-space | `../../obsidian/05-habr-projects/knowledg` | файл не существует |
| `docs/05-habr-projects/knowledge/mclaude.md` | Описание | `#описание` | якорь не найден |
| `docs/05-habr-projects/knowledge/mclaude.md` | Ключевые компоненты | `#ключевые-компоненты` | якорь не найден |
| `docs/05-habr-projects/knowledge/mclaude.md` | Описание | `#описание` | якорь не найден |
| `docs/05-habr-projects/knowledge/mclaude.md` | Ключевые компоненты | `#ключевые-компоненты` | якорь не найден |
| `docs/05-habr-projects/knowledge/mclaude.md` | mclaude | `../../obsidian/05-habr-projects/knowledg` | файл не существует |
| `docs/05-habr-projects/knowledge/mclaude.md` | rufler | `../../obsidian/05-habr-projects/knowledg` | файл не существует |
| `docs/05-habr-projects/knowledge/research-docs-liteparse.md` | Описание | `#описание` | якорь не найден |
| `docs/05-habr-projects/knowledge/research-docs-liteparse.md` | Ключевые компоненты | `#ключевые-компоненты` | якорь не найден |
| `docs/05-habr-projects/knowledge/research-docs-liteparse.md` | research-docs-liteparse | `../../obsidian/05-habr-projects/knowledg` | файл не существует |
| `docs/05-habr-projects/knowledge/rufler.md` | Описание | `#описание` | якорь не найден |
| `docs/05-habr-projects/knowledge/rufler.md` | Ключевые компоненты | `#ключевые-компоненты` | якорь не найден |
| `docs/05-habr-projects/knowledge/rufler.md` | Описание | `#описание` | якорь не найден |
| `docs/05-habr-projects/knowledge/rufler.md` | Ключевые компоненты | `#ключевые-компоненты` | якорь не найден |
| `docs/05-habr-projects/knowledge/rufler.md` | rufler | `../../obsidian/05-habr-projects/knowledg` | файл не существует |
| `docs/05-habr-projects/knowledge/rufler.md` | mclaude | `../../obsidian/05-habr-projects/knowledg` | файл не существует |
| `docs/05-habr-projects/memory/agent-memory-mcp.md` | Описание | `#описание` | якорь не найден |
| `docs/05-habr-projects/memory/agent-memory-mcp.md` | Ключевые компоненты | `#ключевые-компоненты` | якорь не найден |
| `docs/05-habr-projects/memory/agent-memory-mcp.md` | agent-memory-mcp | `../../obsidian/05-habr-projects/memory/a` | файл не существует |
| `docs/COLLAB_SUGGESTIONS.md` | COLLAB_SUGGESTIONS | `obsidian/COLLAB_SUGGESTIONS.md` | файл не существует |
| `docs/CONCEPTS.md` | gaps | `obsidian/svyazi-2-0/architecture/gaps.md` | файл не существует |
| `docs/CONCEPTS.md` | components-by-name | `obsidian/glossary/components-by-name.md` | файл не существует |
| `docs/CONCEPTS.md` | components-by-name | `obsidian/glossary/components-by-name.md` | файл не существует |
| `docs/CONCEPTS.md` | components-by-name | `obsidian/glossary/components-by-name.md` | файл не существует |
| `docs/CONCEPTS.md` | 03-dsl-ast | `obsidian/technology-combinations/mega-st` | файл не существует |

_...и ещё 3279 проблем_

## Внешние URL (629 уникальных)

_Внешние ссылки не проверяются автоматически — требуют ручной проверки._

- http://local
- http://localhos
- http://localhos`
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
- http://localhost:8000``````````
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
- http://localhost:8080``````````
- http://localhost:8083/api/ask
- http://localhost:8083/api/ask`
- http://localhost:8083/api/ask``
- http://localhost:8083/api/ask```

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
