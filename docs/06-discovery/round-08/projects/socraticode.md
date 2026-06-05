# SocratiCode (MCP-сервер понимания кодовой базы)

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** @giancarloerra  
**Хабр:** https://habr.com/ru/articles/1031878/  
**GitHub:** https://github.com/giancarloerra/SocratiCode  
**Слой:** developer-tools / MCP / codebase-intelligence  
**Зрелость:** production, опубликован на npm, в Cursor Directory  
**Уникальность:** MCP-сервер для глубокого понимания кодовой базы: гибридный семантический поиск (Qdrant), AST-чанкинг, граф зависимостей, анализ влияния на уровне символов. **61% меньше токенов, 84% меньше вызовов, 37× быстрее**. Zero setup. Работает с Claude Code, Cursor, Windsurf. Масштабируется до 40M+ строк кода.

## Что умеет

| Возможность | Описание |
|-------------|---------|
| Гибридный семантический поиск | Qdrant + BM25, понимает смысл, не только ключевые слова |
| AST-чанкинг | Режет код по смысловым единицам (функции, классы), не по строкам |
| Граф зависимостей | polyglot — Python, JS, Go, Rust и другие |
| Анализ влияния | symbol-level impact analysis: что сломается при изменении |
| Call-flow | граф вызовов функций |
| Contextual artifacts | схемы БД, API-спецификации, инфра-конфиги |
| Cross-project поиск | ищет по нескольким репозиториям + ветки |

## Ключевые метрики (из статьи на Хабре)

> 61% меньше токенов · 84% меньше MCP-вызовов · 37× быстрее

Сравнение: с SocratiCode агент тратит в 37 раз меньше времени на понимание кода.  
Это та же логика, что AI Web Tester (R05): убрать неэффективный слой — получить 50×+ экономию.

## Почему важно для Lorenzo/Svyazi

Lorenzo — 159 скриптов в `scripts/improve_*.py`, 12 MCP-серверов, 2483 карточки.  
SocratiCode подключается как MCP → Claude Code получает полную карту кодовой базы:  
«какие скрипты касаются NER», «что сломается если изменить `utils_chunker.py`».

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **SocratiCode + Lorenzo scripts** | Claude Code понимает всю кодовую базу Lorenzo (159 скриптов) |
| **SocratiCode + AI Review (R03)** | Ревью кода с полным контекстом зависимостей |
| **SocratiCode + DevClaw (R06)** | GitHub Issue → агент с полным пониманием базы → точный PR |
| **SocratiCode + TRAIL spec (R04)** | Один MCP-сервер для кода + связь с остальными серверами |

## Контакт

- GitHub: https://github.com/giancarloerra/SocratiCode
- npm: https://www.npmjs.com/package/socraticode
- Хабр: https://habr.com/ru/articles/1031878/
