---
date: 2026-05-29
tags: [memory, rag, orchestration, knowledge, ingestion]
state: normalized
---

# Proposal: Agentfs × Agent-Memory-Mcp


<!-- summary -->
> Раздел proposal-agentfs-x-agent-memory-mcp-enriched формируется автоматически из данных репозитория.

> [!NOTE]
> Раздел `proposal-agentfs-x-agent-memory-mcp-enriched` формируется автоматически из данных репозитория.

<!-- alert-added -->

<!-- summary: Интеграция knowledge-слоя (Agentfs) и memory-слоя (Agent-Memory-Mcp): Agentfs обеспечивает персистен -->
<!-- tags: proposal, agentfs, agent-memory-mcp, knowledge, memory, integration -->
<!-- enriched: 2026-05-29 by improve_llm_enrich.py -->
<!-- source: docs\04-ai-collaborations\proposals\proposal-agentfs-x-agent-memory-mcp.md -->

# Proposal: Agentfs × Agent-Memory-Mcp

## Что это

Предложение об интеграции двух компонентов агентной памяти: knowledge-слоя (Agentfs) и memory-слоя (Agent-Memory-Mcp). Проект направлен на создание единой системы, где персистентная память эпизодов из Agentfs преобразуется в узлы структурированного графа знаний в Agent-Memory-Mcp, обеспечивая контекстно-зависимый retrieval с временно́й семантикой.

## Ключевые особенности

- **Персистентная память эпизодов:** Agentfs обеспечивает долгосрочное хранение эпизодических данных агента
- **Структурированный граф знаний:** Agent-Memory-Mcp организует информацию в виде связанного графа для логической обработки
- **Контекстно-зависимый retrieval:** Интеграция позволяет извлекать информацию с учётом временно́й семантики и контекста

## Статус проекта

| Параметр | Значение |
|----------|---------|
| Язык/стек | — |
| Лицензия | — |
| Ссылка | — |

## Интеграция с Svyazi

Proposal является частью слоя планирования и архитектуры для Svyazi 2.0, определяя способ синтеза эпизодической и семантической памяти в единую гибридную систему управления знаниями агента.
---
_Обогащено автоматически: 2026-05-29_
_Источник: [proposal-agentfs-x-agent-memory-mcp](docs\04-ai-collaborations\proposals\proposal-agentfs-x-agent-memory-mcp.md)_


## Использование
```bash
# Запуск
python scripts/improve_proposal_agentfs_x_agent_memory_mcp_enriched.py
```
