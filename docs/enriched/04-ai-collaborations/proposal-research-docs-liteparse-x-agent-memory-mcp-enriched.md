# Proposal: Research-Docs-Liteparse × Agent-Memory-Mcp

<!-- summary: Интеграция ingestion-слоя (Research-Docs-Liteparse) и memory-слоя (Agent-Memory-Mcp): Research-Docs- -->
<!-- tags: proposal, research-docs-liteparse, agent-memory-mcp, ingestion, memory, integration -->
<!-- enriched: 2026-05-29 by improve_llm_enrich.py -->
<!-- source: docs\04-ai-collaborations\proposals\proposal-research-docs-liteparse-x-agent-memory-mcp.md -->

## Что это

Proposal для интеграции ingestion-слоя (Research-Docs-Liteparse) и memory-слоя (Agent-Memory-Mcp). Research-Docs-Liteparse хранит знания с decay и consolidation, а Agent-Memory-Mcp извлекает структурированные данные из документов. Ключевая идея — автоматическое накопление верифицированных фактов через передачу extracted evidence в episodes.

## Ключевые особенности

- **Decay и consolidation:** Research-Docs-Liteparse реализует механизм затухания и уплотнения знаний для управления релевантностью накопленной информации

- **Структурированная экстракция:** Agent-Memory-Mcp извлекает evidence из документов в структурированном виде, готовом к обработке

- **Двусторонний поток:** Extracted evidence из Agent-Memory-Mcp автоматически преобразуется в episodes в Research-Docs-Liteparse для верификации и накопления

## Статус проекта

| Параметр | Значение |
|----------|---------|
| Язык/стек | — |
| Лицензия | — |
| Ссылка | — |

## Интеграция с Svyazi

Проект позиционируется как proposal слой в архитектуре Svyazi 2.0, объединяющий процессы ingestion и memory management. Интеграция обеспечивает замкнутый цикл: документы → экстракция фактов → накопление знаний с автоматической фильтрацией через decay-механизмы.
---
_Обогащено автоматически: 2026-05-29_
_Источник: [proposal-research-docs-liteparse-x-agent-memory-mcp](docs\04-ai-collaborations\proposals\proposal-research-docs-liteparse-x-agent-memory-mcp.md)_
