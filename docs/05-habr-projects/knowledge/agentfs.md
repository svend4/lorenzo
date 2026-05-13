---
state: normalized
template: project-component
version: "1.0"
author: "kksudo"
author_handle: "@kksudo"
component: AgentFS
projects: [AgentFS]
layer: knowledge
license: MIT
maturity: alpha
priority: 1
tags: [agentfs, obsidian, filesystem, agent, knowledge, persistent-state, security]
---
<!-- autofill-status -->
## Статус

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | 1384 |
| Слой | knowledge/filesystem |
| Контакт | [@kksudo](../../contacts/kksudo.md) |
| Статус связи | не писали |

_Обновлено: 2026-05-10_

# AgentFS

> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

<!-- summary -->
> Параметр | Значение | Упоминаний в репо | 1384 | Слой | knowledge/filesystem | Статус связи | не писали |
 Параметр | Значение |
 ----------|---------|
 Теги | — |
 Упоминаний в репо | 1384 |
 Слой | knowledge/filesystem |
 Контакт | @kksudo |
 Статус связи | не писали |
_Обновлено: 2026-05-10_
AgentFS
> [!WARNING]
> Документ содержит описание рис
**Проекты:** Svyazi[^svyazi], AgentFS, knowledge-space[^knowledge-space], mclaude, agent-memory-mcp, Wikontic

---

<!-- toc -->
## Содержание

- [Статус](#статус)
- [Профиль проекта](#профиль-проекта)
- [Описание](#описание)
- [Ключевые компоненты](#ключевые-компоненты)
- [Синергия со Svyazi 2.0](#синергия-со-svyazi-20)
- [Уровень релевантности](#уровень-релевантности)
- [Сравнение с аналогами](#сравнение-с-аналогами)
- [Контакт](#контакт)
- [Смотрите также](#смотрите-также)

---




<!-- summary: Превращает Obsidian-vault в операционную систему для AI-агентов с единым .agentos/-ядром -->
<!-- tags: agentfs, agent, filesystem, obsidian, knowledge, persistent-state, security, compile -->

## Профиль проекта

| Параметр | Значение |
|----------|---------|
| Автор | kksudo |
| GitHub | @kksudo |
| Источник | Хабр + GitHub |
| Лицензия | **MIT** |
| Версия | 0.1.5 |
| Maturity | Рабочий прототип; «рабочая, но не финальная» |
| Слой в Svyazi | knowledge / filesystem |

## Что это

AgentFS превращает Obsidian-vault в операционную систему для AI-агентов с единым `.agentos/`-ядром. Агент получает постоянный персистентный state, скомпилированные конфиги, политики безопасности и CLI-инструменты (`doctor`, `triage`, `compile`) для самодиагностики.

Это лучший кандидат на файловое ядро Svyazi 2.0: он уже знает, как организовать знания в структуру, понятную агентам, при этом оставаясь совместимым с Obsidian (человекочитаемый vault).

## Ключевые особенности

- **`.agentos/` ядро** — единая точка входа для всех агентских операций над vault
- **Compile-to-native configs** — преобразование YAML-конфигов в нативные форматы окружения
- **Persistent state** — агент сохраняет состояние между сессиями в структурированном виде
- **Security policies** — политики доступа к файлам и директориям
- **Memory consolidation** — консолидация памяти между сессиями агента
- **Doctor / Triage / Compile CLI** — самодиагностика и управление агентской файловой системой
- **Obsidian-совместимость** — vault остаётся читаемым для людей

## Синергия со Svyazi 2.0

- **Прямая интеграция**: AgentFS как файловое ядро + CardStore поверх него — агент работает с vault как с базой знаний
- **Security policies** переиспользуются как SkillPolicy из PROTOTYPE_SPEC: `{tool_class, approval_mode, rate_limit}`
- **Memory consolidation** дополняет MemoryWrite: episodic записи AgentFS → факты CardEnvelope
- **Persistent state** решает проблему потери контекста между сессиями агента
- **Compile CLI** — аналог `improve_card_index.py --build`: пересборка индекса по требованию
- **MIT лицензия** — прямая интеграция без юридических рисков

## Уровень релевантности

**Очень высокая** — AgentFS закрывает слой "filesystem/knowledge" в архитектуре Svyazi 2.0. Без него агенты теряют state между сессиями и не имеют единой точки доступа к vault.

## Сравнение с аналогами

| Проект | Подход | Нишa |
|--------|--------|------|
| **AgentFS** | **Obsidian-vault как agent OS** | **Файловое ядро** |
| knowledge-space | Reference cards, 785+ записей | База знаний по доменам |
| Wikontic | Семантический граф | Концептуальные связи |
| mclaude | Координация агентов | Multi-session orchestration |

## Контакт

- Контактный файл: [docs/contacts/kksudo.md](../../contacts/kksudo.md)
- Упомянут в документах: 13 раз (наибольшее число упоминаний среди всех авторов)

## Использование
```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "AgentFS"
```

## Смотрите также

- [knowledge-space](knowledge-space.md) — 785+ agent-first карточек как knowledge layer поверх AgentFS
- [mclaude](mclaude.md) — координация нескольких AgentFS-сессий через locks/handoffs
- [agent-memory-mcp](../memory/agent-memory-mcp.md) — typed MCP[^mcp] память совместимая с AgentFS persistent state
- [Wikontic: семантический граф](wikontic.md) — семантический граф как knowledge layer

---
_Создано: 2026-05-10_

<!-- backlinks -->

---

**Кто ссылается на этот документ (10):**
- [README](README.md)
- [knowledge-space](knowledge-space.md)
- [mclaude](mclaude.md)
- [research-docs-liteparse](research-docs-liteparse.md)
- [rufler](rufler.md)
- [agent-memory-mcp](../memory/agent-memory-mcp.md)
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- _...ещё 2_



<!-- footnotes-added -->

---

[^mcp]: Model Context Protocol — протокол для AI-инструментов

[^agentfs]: OSS-проект: файловая система для AI-агентов (MIT)

[^svyazi]: Главный проект: экосистема AI-компонентов

[^knowledge-space]: OSS-проект: база знаний 785+ карточек (MIT)

<!-- similar-docs -->

---

**Похожие документы:**
- [agentfs](../../svyazi-2-0/components/agentfs.md) (сходство 0.95)
- [mclaude](mclaude.md) (сходство 0.33)
- [mclaude](../../svyazi-2-0/components/mclaude.md) (сходство 0.30)

