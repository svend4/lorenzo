---
date: 2026-05-29
tags: [rag, orchestration, knowledge, ingestion, architecture]
state: normalized
---

# Proposal: Research-Docs-Liteparse × Agentfs


<!-- summary -->
> Раздел proposal-research-docs-liteparse-x-agentfs-enriched формируется автоматически из данных репозитория.

> [!NOTE]
> Раздел `proposal-research-docs-liteparse-x-agentfs-enriched` формируется автоматически из данных репозитория.

<!-- alert-added -->

<!-- summary: Интеграция ingestion-слоя (Research-Docs-Liteparse) и knowledge-слоя (Agentfs): Research-Docs-Litepa -->
<!-- tags: proposal, research-docs-liteparse, agentfs, ingestion, knowledge, integration -->
<!-- enriched: 2026-05-29 by improve_llm_enrich.py -->
<!-- source: docs\04-ai-collaborations\proposals\proposal-research-docs-liteparse-x-agentfs.md -->

## Что это

Proposal по интеграции ingestion-слоя (Research-Docs-Liteparse) и knowledge-слоя (Agentfs). Research-Docs-Liteparse хранит знания в виде графа документов, а Agentfs парсит и извлекает структуру из сырых источников. Интеграция обеспечивает автоматическое обогащение графа знаний из внешних источников.

## Ключевые особенности

- **Граф документов:** Research-Docs-Liteparse реализует хранилище знаний в виде связанного графа документов
- **Парсинг структуры:** Agentfs отвечает за парсинг и извлечение структуры из неструктурированных источников
- **Автоматическое обогащение:** Интеграция работает по схеме Agentfs → Card Envelope → Research-Docs-Liteparse, обеспечивая бесшовное добавление новых знаний в граф

## Статус проекта

| Параметр | Значение |
|----------|---------|
| Язык/стек | — |
| Лицензия | — |
| Ссылка | — |

## Интеграция с Svyazi

Проект позиционируется как proposal для слоя знаний базы Svyazi 2.0. Объединение ingestion и knowledge слоёв в единую систему обеспечивает автоматизированный workflow: от получения сырых источников через Agentfs к их структурированному хранению в Research-Docs-Liteparse.
---
_Обогащено автоматически: 2026-05-29_
_Источник: [proposal-research-docs-liteparse-x-agentfs](docs\04-ai-collaborations\proposals\proposal-research-docs-liteparse-x-agentfs.md)_


## Использование
```bash
# Запуск
python scripts/improve_proposal_research_docs_liteparse_x_agentfs_enriched.py
```
