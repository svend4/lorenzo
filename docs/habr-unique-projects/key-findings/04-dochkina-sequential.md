---
state: approved
---

# Виктория Дочкина — Sequential‑протокол распределённых агентов

<!-- toc-auto -->
## Contents

- [Использование](#использование)
- [Смотрите также](#смотрите-также)
- [Кто ссылается на этот документ (4)](#кто-ссылается-на-этот-документ-4)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Поиск уникальных проектов на Хабре для совместной разработки - Claude` (корень репозитория). Документ создан на основе исследования.
**Проекты:** Svyazi, CardIndex

---
<!-- tags: memory, orchestration, knowledge, ingestion, architecture, collaboration -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





> Источник: MHTML‑снимок `Поиск уникальных проектов на Хабре для совместной разработки - Claude` (корень репозитория).

Источник данных и инфраструктурные кусочки

tg-chat-analyser Артура Гавронюка (https://habr.com/ru/articles/943498/, github.com/artur-gavronchuk/tg-chat-analyser) — простой open-source на Python для анализа паттернов поведения участников Telegram-чатов: когда активны, длина сообщений, употребительные слова, динамика. Идеально как третий источник данных для Svyazi помимо самопредставлений: чат сообщества → паттерны → дополнительные сигналы для CardIndex.

OpenClaw + 5 систем памяти (https://habr.com/ru/articles/1020860/) — карта пяти разных архитектурных взглядов на память: Lossless Claw (многоуровневые сводки в SQLite), OpenViking (инфраструктурный поиск с областями), ByteRover (дерево контекста в .brv/context-tree/, knowledge раскладывается по доменам/темам/подтемам как markdown с метаданными — это ровно та организация, которая нужна Svyazi для масштабирования), MemPalace (хранить всё дословно, искать потом), LLM Wiki (живая wiki, которую агент сам ведёт). По сути это меню, из которого можно выбрать слой консолидации для Svyazi.

Слепое пятно LLM-разработки (https://habr.com/ru/articles/1010478/) — про долговременную память на уровне экосистемы из десятков проектов, с таксономией Scope (project/cross-project) и Lifecycle (скорость устаревания). Это нужная теоретическая рамка для того, что Чуян делает в своём unknown_values.yml — там тоже разные сущности живут в разном lifecycle, и сейчас всё в одном файле.

Что из этого всего слипается в более проработанную схему

В прошлом ответе я предложил «Svyazi 2.0 на хеббовском графе». Теперь схема проявляется конкретнее — каждый блок занят конкретным проектом:

<!-- see-also -->

---

## Использование
```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Виктория Дочкина Sequential протокол"
```

## Смотрите также
- [05-supplementary-infrastructure](05-supplementary-infrastructure.md)
- 5-tinyml-[mcp-skills](../hardware-pairs/5-tinyml-mcp-skills.md)
- [02-memnet](02-memnet.md)
- [3-crdt-self-hosted](../software-pairs/3-crdt-self-hosted.md)


<!-- backlinks -->

---

## Кто ссылается на этот документ (4)
- [authors-by-name](../../glossary/authors-by-name.md)
- [components-by-name](../../glossary/components-by-name.md)
- [concepts](../../glossary/concepts.md)
- [README](README.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [04-dochkina-sequential](../../obsidian/habr-unique-projects/key-findings/04-dochkina-sequential.md) (сходство 0.96)
- [05-supplementary-infrastructure](05-supplementary-infrastructure.md) (сходство 0.27)
- [05-supplementary-infrastructure](../../obsidian/habr-unique-projects/key-findings/05-supplementary-infrastructure.md) (сходство 0.26)

