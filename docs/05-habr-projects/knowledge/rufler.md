---
state: normalized
template: project-component
version: "1.0"
author: "zodigancode"
author_handle: "@zodigancode"
component: Rufler
projects: [Rufler]
layer: orchestration
license: MIT
maturity: beta
priority: 2
tags: [rufler, yaml, orchestration, agent-swarm, claude-code, declarative, mcp, token-accounting]
---
<!-- autofill-status -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

## Статус

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | 691 |
| Слой | orchestration |
| Контакт | [@zodigancode](../../contacts/zodigancode.md) |
| Статус связи | не писали |

_Обновлено: 2026-05-10_

# Rufler

<!-- toc-auto -->
## Contents

- [Статус](#статус)
- [Содержание](#содержание)
- [Профиль проекта](#профиль-проекта)
- [Описание](#описание)
- [Ключевые компоненты](#ключевые-компоненты)
- [Пример структуры задачи (Rufler DSL)](#пример-структуры-задачи-rufler-dsl)
- [Синергия со Svyazi 2.0](#синергия-со-svyazi-20)
- [Позиция в архитектуре](#позиция-в-архитектуре)
- [Контакт](#контакт)
- [Смотрите также](#смотрите-также)


<!-- toc -->
## Содержание

- [Статус](#статус)
- [Contents](#contents)
- [Профиль проекта](#профиль-проекта)
- [Описание](#описание)
- [Ключевые компоненты](#ключевые-компоненты)
- [Пример структуры задачи (Rufler DSL)](#пример-структуры-задачи-rufler-dsl)
- [Синергия со Svyazi[^svyazi] 2.0](#синергия-со-svyazi-20)
- [Позиция в архитектуре](#позиция-в-архитектуре)
- [Контакт](#контакт)
- [Смотрите также](#смотрите-также)

---


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> tags: [rufler, yaml, orchestration, agent-swarm, claude-code, declarative, mcp, token-accounting]
**Проекты:** Svyazi, AgentFS[^agentfs], knowledge-space[^knowledge-space], mclaude, Rufler, agent-memory-mcp

---



<!-- summary: Декларативный YAML-слой для запуска автономного роя Claude Code-агентов с depends_on, pause/resume и token accounting -->
<!-- tags: rufler, yaml, declarative, orchestration, agent-swarm, claude-code, mcp, depends_on, pause, resume -->

## Профиль проекта

| Параметр | Значение |
|----------|---------|
| Автор | zodigancode / lib4u |
| GitHub | @zodigancode |
| Источник | Хабр + repo/DEV |
| Лицензия | **MIT** |
| Maturity | Активный OSS |
| Слой в Svyazi | orchestration |

## Что это

Rufler — декларативный YAML-слой для запуска автономного роя Claude Code-агентов. Вместо написания кода оркестрации разработчик описывает задачи в YAML-файле: зависимости между задачами (`depends_on`), автоматическую генерацию целей для агентов (`auto-objective prompts`), управление жизненным циклом (`pause/resume`), учёт токенов (`token accounting`) и управление MCP[^mcp]-серверами.

Ключевое отличие от mclaude: Rufler работает как декларативный конфигурационный слой (описал → запустил), mclaude — как протокол координации уже запущенных агентов.

## Ключевые особенности

- **`depends_on`** — граф зависимостей задач: агент B запускается только после завершения агента A
- **Auto-objective prompts** — Rufler сам формирует цель задачи из YAML-описания, не нужно писать промпт вручную
- **Pause / Resume** — приостановка и возобновление роя без потери состояния
- **Token accounting** — учёт и ограничение потребления токенов на задачу и на весь рой
- **MCP server management** — Rufler управляет запуском/остановкой MCP-серверов для агентов
- **YAML DSL** — минималистичный язык описания агентных пайплайнов

## Пример структуры задачи (Rufler DSL)

```yaml
tasks:
  - id: extract_contacts
    objective: "Извлечь контакты авторов из docs/contacts/"
    depends_on: []
    token_limit: 5000

  - id: rank_by_priority
    objective: "Ранжировать контакты по приоритету коллаборации"
    depends_on: [extract_contacts]
    token_limit: 3000
```

## Синергия со Svyazi 2.0

- **depends_on** = порядок итераций PROTOTYPE_SPEC: retrieval → consolidation → collaboration
- **Token accounting** → SkillPolicy(rate_limit): контроль стоимости выполнения пайплайна
- **MCP server management** → управление `mcp_server.py` из Svyazi как отдельным агентным ресурсом
- **Auto-objective prompts** + knowledge-space: Rufler читает карточку задачи, сам формирует промпт
- **Pause/Resume** → MemoryWrite(type="episode"): сохранение прогресса роя между сессиями
- **MIT** — прямая интеграция без ограничений

## Позиция в архитектуре

Rufler — самый лёгкий путь к multi-agent pipeline: не нужно писать Python-оркестрацию, достаточно YAML. Это делает его идеальным для быстрого прототипирования агентных пайплайнов Svyazi 2.0 перед написанием полноценного кода.

## Контакт

- Контактный файл: [docs/contacts/zodigancode.md](../../contacts/zodigancode.md)

## Смотрите также

- [mclaude](mclaude.md) — протокол координации агентов (Rufler: запуск; mclaude: координация)
- [AgentFS](agentfs.md) — файловое ядро которым управляют Rufler-агенты
- [agent-memory-mcp](../memory/agent-memory-mcp.md) — memory слой для агентов в Rufler-рое
- [knowledge-space](knowledge-space.md) — база знаний для задач в Rufler YAML-конфиге

---
_Создано: 2026-05-10_

<!-- backlinks -->

---

**Кто ссылается на этот документ (6):**
- [README](README.md)
- [mclaude](mclaude.md)
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)



<!-- footnotes-added -->

---

[^mcp]: Model Context Protocol — протокол для AI-инструментов

[^agentfs]: OSS-проект: файловая система для AI-агентов (MIT)

[^rufler]: OSS-проект: оркестратор AI-агентов

[^svyazi]: Главный проект: экосистема AI-компонентов

[^knowledge-space]: OSS-проект: база знаний 785+ карточек (MIT)

<!-- similar-docs -->

---

**Похожие документы:**
- [rufler](../../svyazi-2-0/components/rufler.md) (сходство 0.94)
- [mclaude](mclaude.md) (сходство 0.37)
- [mclaude](../../svyazi-2-0/components/mclaude.md) (сходство 0.34)

