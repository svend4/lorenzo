# Виктория Дочкина — Sequential‑протокол распределённых агентов

<!-- summary -->
> > Источник: MHTML‑снимок `Поиск уникальных проектов на Хабре для совместной разработки - Claude` (корень репозитория).
**Проекты:** Svyazi, CardIndex

---
<!-- tags: memory, orchestration, knowledge, ingestion, architecture, collaboration -->




> Источник: MHTML‑снимок `Поиск уникальных проектов на Хабре для совместной разработки - Claude` (корень репозитория).

Источник данных и инфраструктурные кусочки

tg-chat-analyser Артура Гавронюка (https://habr.com/ru/articles/943498/, github.com/artur-gavronchuk/tg-chat-analyser) — простой open-source на Python для анализа паттернов поведения участников Telegram-чатов: когда активны, длина сообщений, употребительные слова, динамика. Идеально как третий источник данных для Svyazi помимо самопредставлений: чат сообщества → паттерны → дополнительные сигналы для CardIndex.

OpenClaw + 5 систем памяти (https://habr.com/ru/articles/1020860/) — карта пяти разных архитектурных взглядов на память: Lossless Claw (многоуровневые сводки в SQLite), OpenViking (инфраструктурный поиск с областями), ByteRover (дерево контекста в .brv/context-tree/, knowledge раскладывается по доменам/темам/подтемам как markdown с метаданными — это ровно та организация, которая нужна Svyazi для масштабирования), MemPalace (хранить всё дословно, искать потом), LLM Wiki (живая wiki, которую агент сам ведёт). По сути это меню, из которого можно выбрать слой консолидации для Svyazi.

Слепое пятно LLM-разработки (https://habr.com/ru/articles/1010478/) — про долговременную память на уровне экосистемы из десятков проектов, с таксономией Scope (project/cross-project) и Lifecycle (скорость устаревания). Это нужная теоретическая рамка для того, что Чуян делает в своём unknown_values.yml — там тоже разные сущности живут в разном lifecycle, и сейчас всё в одном файле.

Что из этого всего слипается в более проработанную схему

В прошлом ответе я предложил «Svyazi 2.0 на хеббовском графе». Теперь схема проявляется конкретнее — каждый блок занят конкретным проектом:

<!-- see-also -->

---

**Смотрите также:**
- [05-supplementary-infrastructure](docs/habr-unique-projects/key-findings/05-supplementary-infrastructure.md)
- [5-tinyml-mcp-skills](docs/habr-unique-projects/hardware-pairs/5-tinyml-mcp-skills.md)
- [02-memnet](docs/habr-unique-projects/key-findings/02-memnet.md)
- [3-crdt-self-hosted](docs/habr-unique-projects/software-pairs/3-crdt-self-hosted.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [05-supplementary-infrastructure](docs/habr-unique-projects/key-findings/05-supplementary-infrastructure.md) (сходство 0.23)
- [5-tinyml-mcp-skills](docs/habr-unique-projects/hardware-pairs/5-tinyml-mcp-skills.md) (сходство 0.17)
- [02-memnet](docs/habr-unique-projects/key-findings/02-memnet.md) (сходство 0.16)

