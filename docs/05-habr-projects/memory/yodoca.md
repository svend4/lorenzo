# Yodoca[^yodoca]: консолидация и забывание

<!-- abstract-auto -->
> **Абстракт** (авто)
>
> 🎯 **Проблема:** Yodoca^yodoca: консолидация и забывание !IMPORTANT Ключевой документ для понимания архитектуры.
> 🔧 **Подход:** Yodoca^yodoca: консолидация и забывание !IMPORTANT Ключевой документ для понимания архитектуры.
> 🏷️ **Ключевые слова:** `memory`, `projects`, `yodoca`, `svyazi`, `collaboration`, `wikontic`, `sqlite`, `readme`
>


> [!IMPORTANT]
> Ключевой документ для понимания архитектуры. Рекомендуется прочитать в первую очередь.

<!-- alert-added -->

<!-- autofill-status -->
## Статус

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | 229 |
| Слой | memory |
| Контакт | [@VitalyOborin](docs/contacts/vitalyoborin.md) |
| Статус связи | не писали |

_Обновлено: 2026-04-29_


<!-- summary -->
> Yodoca — «Научил ИИ-агента помнить важное и забывать лишнее в SQLite» https://habr.com/ru/articles/1006622/ Это не просто аналог, это архитектурное продолжение Svyazi[^svyazi] на уровне agentic memory. Что у н
**Проекты:** Svyazi, Yodoca

---
<!-- tags: memory, ingestion, architecture, collaboration -->




Yodoca — «Научил ИИ-агента помнить важное и забывать лишнее в SQLite» https://habr.com/ru/articles/1006622/ Это не просто аналог, это архитектурное продолжение Svyazi на уровне agentic memory. Что у него есть, чего у Чуяна пока нет:
— разделение на hot path (запись эпизодов в SQLite + FTS5 за <50 мс, без LLM[^llm]) и slow path (асинхронные эмбеддинги);
— отдельный приватный LLM-агент-«

<!-- similar-docs -->

---

**Похожие документы:**
- [README](docs/05-habr-projects/memory/README.md) (сходство 0.21)


<!-- see-also -->

---

**Смотрите также:**
- [01-synthesis](docs/05-habr-projects/01-synthesis.md)
- [wikontic](docs/05-habr-projects/knowledge/wikontic.md)
- [123-portal-mcp-py](docs/02-anthropic-vacancies/123-portal-mcp-py.md)
- [02-collaboration-partners](docs/05-habr-projects/02-collaboration-partners.md)



<!-- footnotes-added -->

---

[^llm]: Large Language Model — большая языковая модель

[^yodoca]: OSS-проект: система памяти с консолидацией (Apache 2.0)

[^svyazi]: Главный проект: экосистема AI-компонентов

<!-- backlinks-auto -->
## Упоминается в

- [Системы памяти](docs/05-habr-projects/memory/README.md)

<!-- related-auto -->
## Связанные документы

- [NGT[^ngt] Memory: ассоциативный граф](docs/05-habr-projects/memory/ngt-memory.md) _21%_
- [Синтез: как проекты собираются вместе](docs/05-habr-projects/01-synthesis.md) _17%_
- [Авторы и контакты](docs/05-habr-projects/02-collaboration-partners.md) _17%_
- [Wikontic: семантический граф](docs/05-habr-projects/knowledge/wikontic.md) _17%_
- [Diff базы знаний между версиями](docs/VERSION_DIFF.md) _17%_
