---
date: 2026-06-05
tags: [rag, knowledge, ingestion, architecture, collaboration]
state: normalized
---

# Proposal: Research-Docs-Liteparse × Knowledge-Space


<!-- summary -->
> Proposal: Research-Docs-Liteparse × Knowledge-Space Проект предлагает интеграцию двух слоёв системы: ingestion-слоя (Research-Docs-Liteparse) и knowledge-слоя (Knowledge-Space).
Что это
Проект предлагает интеграцию двух слоёв системы: ingestion-слоя (Research-Docs-Liteparse) и knowledge-слоя (Knowledge-Space).

> [!NOTE]
> Раздел `proposal-research-docs-liteparse-x-knowledge-space-enriched` формируется автоматически из данных репозитория.

<!-- alert-added -->

<!-- summary: Интеграция ingestion-слоя (Research-Docs-Liteparse) и knowledge-слоя (Knowledge-Space): Research-Doc -->
<!-- tags: proposal, research-docs-liteparse, knowledge-space, ingestion, knowledge, integration -->
<!-- enriched: 2026-05-29 by improve_llm_enrich.py -->
<!-- source: docs\04-ai-collaborations\proposals\proposal-research-docs-liteparse-x-knowledge-space.md -->

# Proposal: Research-Docs-Liteparse × Knowledge-Space

## Что это

Проект предлагает интеграцию двух слоёв системы: ingestion-слоя (Research-Docs-Liteparse) и knowledge-слоя (Knowledge-Space). Research-Docs-Liteparse хранит знания в виде графа документов, а Knowledge-Space отвечает за парсинг и извлечение структуры из сырых источников. Целью интеграции является автоматическое обогащение графа документов из внешних источников.

## Ключевые особенности

- **Graph-based Knowledge Storage:** Research-Docs-Liteparse использует граф документов как основную структуру хранения знаний
- **Parsing and Structure Extraction:** Knowledge-Space парсит сырые источники и извлекает из них структурированную информацию
- **Automated Pipeline:** Интеграция реализуется через цепочку Knowledge-Space → Card Envelope → Research-Docs-Liteparse для автоматического пополнения графа

## Статус проекта

| Параметр | Значение |
|----------|---------|
| Язык/стек | — |
| Лицензия | — |
| Ссылка | — |

## Интеграция с Svyazi

Проект является proposal-уровневой инициативой, определяющей архитектурный паттерн взаимодействия между ingestion и knowledge слоями базы знаний. Интеграция критична для создания единого пайплайна обогащения документографии из внешних источников.
---
_Обогащено автоматически: 2026-05-29_
_Источник: [proposal-research-docs-liteparse-x-knowledge-space](docs\04-ai-collaborations\proposals\proposal-research-docs-liteparse-x-knowledge-space.md)_


## Использование
```bash
# Запуск
python scripts/improve_proposal_research_docs_liteparse_x_knowledge_space_enriched.py
```
