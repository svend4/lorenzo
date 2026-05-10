---
template: project-component
version: "1.0"
author: "VitaliySemenov"
author_handle: "@moshael"
projects: "agent-memory-[mcp", "Memory OS"]
layer: memory
license: unspecified
maturity: working-oss
priority: 2
tags: memory, mcp, typed-memory, [sqlite, agent, bi-temporal]
---
<!-- autofill-status -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

## Статус

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | 169 |
| Слой | memory/MCP[^mcp] |
| Контакт | [@VitaliySemenov](../../contacts/vitalysemenov.md) |
| Статус связи | не писали |

_Обновлено: 2026-05-10_

# agent-memory-mcp + Memory OS

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> projects: ["agent-memory-mcp", "Memory OS"]
**Проекты:** Svyazi[^svyazi], CardIndex[^cardindex], AgentFS[^agentfs], Yodoca[^yodoca], NGT[^ngt] Memory, MemNet, agent-memory-mcp

---

<!-- toc -->
## Содержание

- [Статус](#статус)
- [Профиль проекта](#профиль-проекта)
- [Описание](#описание)
- [Ключевые компоненты](#ключевые-компоненты)
- [Синергия со Svyazi 2.0](#синергия-со-svyazi-20)
- [Сравнение с другими memory-проектами](#сравнение-с-другими-memory-проектами)
- [Открытые вопросы](#открытые-вопросы)
- [Контакт](#контакт)
- [Смотрите также](#смотрите-также)

---




<!-- summary: Типизированный MCP-сервер памяти агента с bi-temporal фактами и gardener-loop -->
<!-- tags: memory, mcp, agent, typed-memory, sqlite, bi-temporal -->

## Профиль проекта

| Параметр | Значение |
|----------|---------|
| Автор | VitaliySemenov / moshael |
| GitHub | @moshael |
| Источник | Хабр + GitHub |
| Лицензия | не уточнена |
| Maturity | agent-memory-mcp — рабочий OSS; Memory OS — концепт |
| Слой в Svyazi | memory |

## Описание

`agent-memory-mcp` — типизированный MCP-сервер памяти для AI-агентов с поддержкой четырёх типов записей: `episodic`, `semantic`, `procedural`, `working`. Хранение на SQLite + WAL обеспечивает локальную, GDPR-safe, offline-capable работу. Включает поиск по репо и документам, а также path guard для управления доступом.

`Memory OS` — более амбициозная концепция поверх agent-memory-mcp: онтология знаний, gardener-loop (автоматическое поддержание качества памяти), bi-temporal факты (время события + время записи), planner/scout/synthesizer агентный стек.

## Ключевые компоненты

- **SQLite + WAL** — локальное хранение, offline-capable, GDPR-safe
- **Typed memories** — episodic, semantic, procedural, working
- **Repo / doc search** — поиск по репозиторию и документам
- **Path guard** — управление доступом к файловым путям
- **Ontology** — концептуальная онтология знаний (Memory OS)
- **Gardener-loop** — автоматическое поддержание и очистка памяти
- **Bi-temporal facts** — время события + время записи (Memory OS)
- **Planner / scout / synthesizer** — агентный стек (Memory OS)
- **Concept loop** — цикл обновления концептов

## Синергия со Svyazi 2.0

- Готовый memory-слой с MCP API для Claude Desktop — нулевые накладные расходы на интеграцию
- Typed memories дополняют CardEnvelope: episodic → fact цикл через MemoryWrite
- SQLite + WAL — тот же стек, что и у CardStore (локальный, без сетевых зависимостей)
- Gardener-loop реализует идею decay из PROTOTYPE_SPEC: автоматический переход `raw → decayed`
- Bi-temporal факты решают проблему "когда это было известно" для доказательных цепочек Evidence Envelope
- Path guard можно переиспользовать как SkillPolicy: какие инструменты могут читать/писать какие пути

## Сравнение с другими memory-проектами

| Проект | Подход | Отличие |
|--------|--------|---------|
| Yodoca | Консолидация + забывание | Фокус на decay и consolidator |
| NGT Memory | Ассоциативный граф | Нейроподобные связи, не типы |
| MemNet | Нейроархитектура | Исследовательский, не MCP |
| **agent-memory-mcp** | **Типизированный MCP** | **Готовый API для агентов** |

## Открытые вопросы

1. Есть ли публичная документация по Memory OS (bi-temporal facts, gardener-loop)?
2. Планируется ли поддержка внешних источников (CardIndex / doc-ingestion)?
3. Как memory write API взаимодействует с внешними источниками?
4. Планируется ли поддержка batch-ingestion из документов?

## Контакт

- Контактный файл: [docs/contacts/vitalysemenov.md](../../contacts/vitalysemenov.md)
- Статус: not_started

## Использование
```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "agent memory mcp Memory OS"
```

## Смотрите также

- [Yodoca: консолидация и забывание](yodoca.md) — memory decay + hot/slow path
- [NGT Memory: ассоциативный граф](ngt-memory.md) — граф-подход к памяти
- [MemNet: исследовательская память](memnet.md) — нейроархитектура памяти
- [AgentFS](../knowledge/agentfs.md) — файловая система + persistent state для агентов

---
_Создано: 2026-05-10_

<!-- backlinks -->

---

**Кто ссылается на этот документ (12):**
- [agentfs](../knowledge/agentfs.md)
- [mclaude](../knowledge/mclaude.md)
- [research-docs-liteparse](../knowledge/research-docs-liteparse.md)
- [rufler](../knowledge/rufler.md)
- [README](README.md)
- [memnet](memnet.md)
- [ngt-memory](ngt-memory.md)
- [COLLAB_SUGGESTIONS](../../COLLAB_SUGGESTIONS.md)
- _...ещё 4_



<!-- footnotes-added -->

---

[^mcp]: Model Context Protocol — протокол для AI-инструментов

[^cardindex]: OSS-проект: индекс знаний на карточках (MIT)

[^agentfs]: OSS-проект: файловая система для AI-агентов (MIT)

[^yodoca]: OSS-проект: система памяти с консолидацией (Apache 2.0)

[^ngt]: OSS-проект: ассоциативный граф памяти (BSL 1.1)

[^svyazi]: Главный проект: экосистема AI-компонентов
