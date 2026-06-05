---
date: 2026-06-05
tags: [memory, rag, orchestration, knowledge, ingestion]
state: normalized
---

# Proposal: Wikontic × Agent-Memory-Mcp


<!-- summary -->
> Раздел proposal-wikontic-x-agent-memory-mcp-enriched формируется автоматически из данных репозитория.

> [!NOTE]
> Раздел `proposal-wikontic-x-agent-memory-mcp-enriched` формируется автоматически из данных репозитория.

<!-- alert-added -->

<!-- summary: Интеграция knowledge-слоя (Wikontic) и memory-слоя (Agent-Memory-Mcp): Wikontic обеспечивает персист -->
<!-- tags: proposal, wikontic, agent-memory-mcp, knowledge, memory, integration -->
<!-- enriched: 2026-05-29 by improve_llm_enrich.py -->
<!-- source: docs\04-ai-collaborations\proposals\proposal-wikontic-x-agent-memory-mcp.md -->

# Proposal: Wikontic × Agent-Memory-Mcp

## Что это
Проект предлагает интеграцию knowledge-слоя (Wikontic) и memory-слоя (Agent-Memory-Mcp) для создания единой системы управления знаниями и памятью агентов. Wikontic обеспечивает персистентную память эпизодов, в то время как Agent-Memory-Mcp хранит структурированный граф знаний. Интеграция направлена на реализацию контекстно-зависимого retrieval с временной семантикой.

## Ключевые особенности
- **Персистентная память эпизодов:** Wikontic отвечает за сохранение и управление эпизодами агента во времени
- **Структурированный граф знаний:** Agent-Memory-Mcp реализует граф-структуру для организации знаний
- **Контекстно-зависимый retrieval:** Episodes из Wikontic преобразуются в узлы графа Agent-Memory-Mcp с поддержкой временной семантики

## Статус проекта
| Параметр | Значение |
|----------|---------|
| Язык/стек | — |
| Лицензия | — |
| Ссылка | — |

## Интеграция с Svyazi
Проект расширяет архитектуру Svyazi 2.0 за счет синергии между слоями памяти и знаний, обеспечивая агентам способность контекстно-зависимого поиска информации с учетом временных характеристик эпизодов.
---
_Обогащено автоматически: 2026-05-29_
_Источник: [proposal-wikontic-x-agent-memory-mcp](docs\04-ai-collaborations\proposals\proposal-wikontic-x-agent-memory-mcp.md)_


## Использование
```bash
# Запуск
python scripts/improve_proposal_wikontic_x_agent_memory_mcp_enriched.py
```
