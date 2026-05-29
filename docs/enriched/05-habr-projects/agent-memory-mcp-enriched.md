---
date: 2026-05-29
tags: [memory, orchestration, knowledge, ingestion, architecture]
state: normalized
---

# agent-memory-mcp + Memory OS


<!-- summary -->
> Раздел agent-memory-mcp-enriched формируется автоматически из данных репозитория.

> [!NOTE]
> Раздел `agent-memory-mcp-enriched` формируется автоматически из данных репозитория.

<!-- alert-added -->

<!-- summary: Документ создан на основе исследования. Ссылки ведут на связанные материалы. Параметр | Значение | У -->
<!-- tags: memory, mcp, agent, typed-memory, sqlite, bi-temporal -->
<!-- enriched: 2026-05-29 by improve_llm_enrich.py -->
<!-- source: docs\05-habr-projects\memory\agent-memory-mcp.md -->

# agent-memory-mcp + Memory OS

## Что это

Проект реализует слой памяти для агентов через MCP (Model Context Protocol), интегрируя типизированное хранилище памяти с би-темпоральной архитектурой. Решает задачу структурированного управления знаниями и состоянием агентов с использованием SQLite в качестве базы данных.

## Ключевые особенности

- **Типизированная память:** Использует typed-memory для структурированного хранения данных агентов
- **SQLite-хранилище:** Реализует персистентное хранилище на основе SQLite
- **Би-темпоральная архитектура:** Поддерживает отслеживание истории изменений состояния
- **MCP-интеграция:** Встроена в слой memory/MCP для взаимодействия с другими компонентами

## Статус проекта

| Параметр | Значение |
|----------|---------|
| Матurity | alpha |
| Лицензия | Unknown |
| Упоминаний в репо | 169 |
| Контакт | @VitaliySemenov |
| Статус связи | не писали |

## Интеграция с Svyazi

Компонент занимает критическое место в архитектуре memory-слоя проекта Svyazi 2.0, обеспечивая основу для работы других компонентов: CardIndex, AgentFS, Yodoca, NGT Memory и MemNet. Служит базисом для типизированного управления памятью в распределённой системе агентов.
---
_Обогащено автоматически: 2026-05-29_
_Источник: [agent-memory-mcp](docs\05-habr-projects\memory\agent-memory-mcp.md)_


## Использование
```bash
# Запуск
python scripts/improve_agent_memory_mcp_enriched.py
```
