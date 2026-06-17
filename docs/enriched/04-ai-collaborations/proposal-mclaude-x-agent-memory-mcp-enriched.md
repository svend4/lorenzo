---
date: 2026-06-05
tags: [memory, orchestration, knowledge, ingestion, architecture]
state: normalized
---

# Proposal: Mclaude × Agent-Memory-Mcp


<!-- summary -->
> Раздел proposal-mclaude-x-agent-memory-mcp-enriched формируется автоматически из данных репозитория.

> [!NOTE]
> Раздел `proposal-mclaude-x-agent-memory-mcp-enriched` формируется автоматически из данных репозитория.

<!-- alert-added -->

<!-- summary: Интеграция orchestration-слоя (Mclaude) и memory-слоя (Agent-Memory-Mcp): Mclaude типизирует memory- -->
<!-- tags: proposal, mclaude, agent-memory-mcp, orchestration, memory, integration -->
<!-- enriched: 2026-05-29 by improve_llm_enrich.py -->
<!-- source: docs\04-ai-collaborations\proposals\proposal-mclaude-x-agent-memory-mcp.md -->

## Что это

Proposal интеграции orchestration-слоя Mclaude и memory-слоя Agent-Memory-Mcp для создания stateful системы управления агентами. Mclaude типизирует memory-примитивы (episode/fact/proposal), а Agent-Memory-Mcp оркестрирует агентов через декларативные пайплайны с контекстной памятью.

## Ключевые особенности

- **Типизация memory-примитивов:** Mclaude определяет структурированные типы для episode, fact и proposal, обеспечивая единый язык описания знаний.
- **Декларативная оркестрация:** Agent-Memory-Mcp управляет агентами через декларативные пайплайны вместо императивного кода.
- **Stateful orchestration:** Agent-Memory-Mcp читает релевантный контекст из Mclaude перед каждым шагом пайплайна, обеспечивая контекстную осведомленность агентов.

## Статус проекта

| Параметр | Значение |
|----------|---------|
| Язык/стек | — |
| Лицензия | — |
| Ссылка | — |

## Интеграция с Svyazi

Proposal описывает архитектурное разделение ответственности между слоями: Mclaude отвечает за типизацию и структурирование памяти, Agent-Memory-Mcp — за оркестрацию и пайплайны. Интеграция обеспечивает синергию между абстракциями памяти и механизмами управления агентами в системе.
---
_Обогащено автоматически: 2026-05-29_
_Источник: [proposal-mclaude-x-agent-memory-mcp](docs\04-ai-collaborations\proposals\proposal-mclaude-x-agent-memory-mcp.md)_


## Использование
```bash
# Запуск
python scripts/improve_proposal_mclaude_x_agent_memory_mcp_enriched.py
```
