# Proposal: Knowledge-Space × Agent-Memory-Mcp

<!-- summary: Интеграция knowledge-слоя (Knowledge-Space) и memory-слоя (Agent-Memory-Mcp): Knowledge-Space обеспе -->
<!-- tags: proposal, knowledge-space, agent-memory-mcp, knowledge, memory, integration -->
<!-- enriched: 2026-05-29 by improve_llm_enrich.py -->
<!-- source: docs\04-ai-collaborations\proposals\proposal-knowledge-space-x-agent-memory-mcp.md -->

# Proposal: Knowledge-Space × Agent-Memory-Mcp

## Что это
Проект предлагает интеграцию двух компонентов системы памяти агента: Knowledge-Space (слой персистентной памяти эпизодов) и Agent-Memory-Mcp (слой структурированного графа знаний). Цель — обеспечить контекстно-зависимый поиск информации с учётом временной семантики через преобразование эпизодов в узлы графа.

## Ключевые особенности
- **Двухслойная архитектура памяти:** Knowledge-Space отвечает за эпизодическую память, Agent-Memory-Mcp — за структурированное представление знаний
- **Трансформация эпизодов в граф:** episodes из Knowledge-Space становятся узлами в графе Agent-Memory-Mcp для единого пространства знаний
- **Контекстно-зависимый retrieval:** интеграция обеспечивает поиск с учётом временной семантики и контекстных связей

## Статус проекта
| Параметр | Значение |
|----------|---------|
| Язык/стек | — |
| Лицензия | — |
| Ссылка | — |

## Интеграция с Svyazi
Проект позиционируется как proposal-уровневое решение для архитектуры памяти в системе Svyazi 2.0, определяя принципы интеграции персистентной эпизодической памяти со структурированным графом знаний агента.
---
_Обогащено автоматически: 2026-05-29_
_Источник: [proposal-knowledge-space-x-agent-memory-mcp](docs\04-ai-collaborations\proposals\proposal-knowledge-space-x-agent-memory-mcp.md)_
