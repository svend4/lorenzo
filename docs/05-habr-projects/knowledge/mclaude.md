---
template: project-component
version: "1.0"
author: "AnastasiyaW"
author_handle: "@AnastasiyaW"
projects: ["mclaude"]
layer: orchestration
license: MIT
maturity: active-oss
priority: 2
tags: mclaude, multi-agent, orchestration, [claude-code, locks, handoffs, mailbox, parallel]
---
<!-- autofill-status -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

## Статус

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | 676 |
| Слой | knowledge/orchestration |
| Контакт | [@AnastasiyaW](../../contacts/anastasiyaw.md) |
| Статус связи | не писали |

_Обновлено: 2026-05-10_

# mclaude

<!-- toc-auto -->
## Contents

- [Статус](#статус)
- [Contents](#contents)
- [Contents](#contents-1)
- [Профиль проекта](#профиль-проекта)
- [Описание](#описание)
- [Ключевые компоненты](#ключевые-компоненты)
- [Синергия со Svyazi 2.0](#синергия-со-svyazi-20)
- [Позиция в экосистеме](#позиция-в-экосистеме)
- [Сравнение с аналогами](#сравнение-с-аналогами)
- [Контакт](#контакт)
- [Смотрите также](#смотрите-также)
## Contents

- [Статус](#статус)
- [Contents](#contents)
- [Профиль проекта](#профиль-проекта)
- [Описание](#описание)
- [Ключевые компоненты](#ключевые-компоненты)
- [Синергия со Svyazi 2.0](#синергия-со-svyazi-20)
- [Позиция в экосистеме](#позиция-в-экосистеме)
- [Сравнение с аналогами](#сравнение-с-аналогами)
- [Контакт](#контакт)
- [Смотрите также](#смотрите-также)
## Contents

- [Статус](#статус)
- [Профиль проекта](#профиль-проекта)
- [Описание](#описание)
- [Ключевые компоненты](#ключевые-компоненты)
- [Синергия со Svyazi 2.0](#синергия-со-svyazi-20)
- [Позиция в экосистеме](#позиция-в-экосистеме)
- [Сравнение с аналогами](#сравнение-с-аналогами)
- [Контакт](#контакт)
- [Смотрите также](#смотрите-также)


<!-- summary -->
> tags: [mclaude, multi-agent, orchestration, claude-code, locks, handoffs, mailbox, parallel]
**Проекты:** Svyazi, AgentFS, knowledge-space, mclaude, AI Factory, Rufler, Yodoca, agent-memory-mcp

---



<!-- summary: Координация нескольких параллельных сессий Claude Code над одним проектом через locks, handoffs и mailbox -->
<!-- tags: mclaude, multi-agent, orchestration, claude-code, parallel, locks, handoff, mailbox, shared-memory -->

## Профиль проекта

| Параметр | Значение |
|----------|---------|
| Автор | AnastasiyaW |
| GitHub | @AnastasiyaW |
| Источник | Хабр + GitHub |
| Лицензия | **MIT** |
| Maturity | Активный OSS |
| Слой в Svyazi | orchestration / coordination |

## Описание

mclaude — система координации нескольких параллельных сессий Claude Code и других coding-агентов над одним проектом. Решает задачу «многоголового агента»: несколько Claude-экземпляров могут одновременно работать над разными частями проекта без конфликтов и потерь контекста.

Ключевой механизм: `locks` (взаимные исключения для файлов/задач), `handoffs` (передача контекста между сессиями), `mailbox` (асинхронные сообщения между агентами), `shared project memory` (общее состояние проекта).

## Ключевые компоненты

- **Locks** — мьютексы для файлов и задач: предотвращают конфликты параллельных агентов
- **Handoffs** — структурированная передача контекста от агента к агенту
- **Mailbox** — асинхронный обмен сообщениями между сессиями
- **Multi-session turn-taking** — протокол очерёдности: кто работает сейчас, кто ждёт
- **Shared project memory** — общая память проекта (задачи, прогресс, решения)

## Синергия со Svyazi 2.0

- **Locks** → SkillPolicy(approval_mode="blocked"): блокировка конкурентных мутаций CardStore
- **Handoffs** → MemoryWrite(type="episode"): сохранение контекста сессии перед завершением
- **Mailbox** → ReviewRecord: асинхронная система рецензирования между агентами
- **Shared memory** → CardEnvelope(state="approved"): консолидированное общее знание
- **Turn-taking** решает проблему параллельной работы нескольких модераторов над одним графом
- **MIT** — прямая интеграция без ограничений

## Позиция в экосистеме

mclaude закрывает слой "multi-agent coordination" в Svyazi 2.0 — то, чего нет у AgentFS (файловое ядро), Yodoca (консолидация) или knowledge-space (база знаний). Без координационного слоя параллельная работа нескольких агентов над общим графом знаний невозможна.

## Сравнение с аналогами

| Проект | Подход | Ниша |
|--------|--------|------|
| **mclaude** | **Claude Code coordination** | **Multi-session parallelism** |
| Rufler | YAML-декларативный рой агентов | Запуск агентов из конфига |
| AgentFS | Persistent state для агента | Файловое ядро одного агента |
| AI Factory | Spec-driven multi-agent dev | Полный dev-цикл (plan→implement→review) |

## Контакт

- Контактный файл: [docs/contacts/anastasiyaw.md](../../contacts/anastasiyaw.md)
- Также автор: [knowledge-space](knowledge-space.md) (785+ карточек, MIT)

## Смотрите также

- [Rufler](rufler.md) — YAML-декларативный запуск роя агентов (альтернативный подход к оркестрации)
- [AgentFS](agentfs.md) — файловое ядро для одного агента, mclaude координирует несколько
- [knowledge-space](knowledge-space.md) — база знаний, которую mclaude агенты читают параллельно
- [agent-memory-mcp](../memory/agent-memory-mcp.md) — shared memory через MCP между сессиями

---
_Создано: 2026-05-10_
