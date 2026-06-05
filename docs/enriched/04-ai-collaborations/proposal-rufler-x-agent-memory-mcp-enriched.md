# Proposal: Rufler × Agent-Memory-Mcp

<!-- summary: Интеграция orchestration-слоя (Rufler) и memory-слоя (Agent-Memory-Mcp): Rufler типизирует memory-пр -->
<!-- tags: proposal, rufler, agent-memory-mcp, orchestration, memory, integration -->
<!-- enriched: 2026-05-29 by improve_llm_enrich.py -->
<!-- source: docs\04-ai-collaborations\proposals\proposal-rufler-x-agent-memory-mcp.md -->

# Proposal: Rufler × Agent-Memory-Mcp

## Что это

Proposal интеграции двух компонентов системы: orchestration-слоя Rufler и memory-слоя Agent-Memory-Mcp. Цель — создать stateful orchestration, где Rufler типизирует memory-примитивы (episode/fact/proposal), а Agent-Memory-Mcp оркестрирует агентов через декларативные пайплайны с доступом к релевантному контексту.

## Ключевые особенности

- **Типизация memory-примитивов:** Rufler определяет и структурирует три основных типа памяти — episode, fact и proposal
- **Декларативная оркестрация:** Agent-Memory-Mcp управляет агентами через декларативные пайплайны без императивного кода
- **Контекстный доступ:** Agent-Memory-Mcp читает релевантный контекст из Rufler перед каждым шагом пайплайна, обеспечивая state awareness

## Статус проекта

| Параметр | Значение |
|----------|----------|
| Язык/стек | — |
| Лицензия | — |
| Ссылка | — |

## Интеграция с Svyazi

Proposal встраивается в слой proposal как стратегия интеграции двух ключевых подсистем памяти и оркестрации, определяя архитектурный паттерн для stateful агентных систем в рамках Svyazi 2.0.
---
_Обогащено автоматически: 2026-05-29_
_Источник: [proposal-rufler-x-agent-memory-mcp](docs\04-ai-collaborations\proposals\proposal-rufler-x-agent-memory-mcp.md)_
