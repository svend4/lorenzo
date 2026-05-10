---
template: project-component
version: "1.0"
author: "VitaliySemenov"
author_handle: "@moshael"
projects: ["agent-memory-mcp", "Memory OS"]
layer: memory
license: unspecified
maturity: working-oss
priority: 2
tags: [memory, mcp, typed-memory, sqlite, agent, bi-temporal]
---
# agent-memory-mcp + Memory OS

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
- Bi-temporal факты решают проблему "когда это было известно" для доказательных цепочек EvidenceEnvelope
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

- Контактный файл: [docs/contacts/vitalysemenov.md](../contacts/vitalysemenov.md)
- Статус: not_started

## Смотрите также

- [Yodoca: консолидация и забывание](yodoca.md) — memory decay + hot/slow path
- [NGT Memory: ассоциативный граф](ngt-memory.md) — граф-подход к памяти
- [MemNet: исследовательская память](memnet.md) — нейроархитектура памяти
- [AgentFS](../knowledge/agentfs.md) — файловая система + persistent state для агентов

---
_Создано: 2026-05-10_
