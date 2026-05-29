---
date: 2026-05-29
tags: [memory, rag, knowledge, ingestion, architecture]
state: normalized
---

# Proposal: Knowledge-Space × Ngt-Memory


<!-- summary -->
> Раздел proposal-knowledge-space-x-ngt-memory-enriched формируется автоматически из данных репозитория.

> [!NOTE]
> Раздел `proposal-knowledge-space-x-ngt-memory-enriched` формируется автоматически из данных репозитория.

<!-- alert-added -->

<!-- summary: Интеграция knowledge-слоя (Knowledge-Space) и memory-слоя (Ngt-Memory): Knowledge-Space обеспечивает -->
<!-- tags: proposal, knowledge-space, ngt-memory, knowledge, memory, integration -->
<!-- enriched: 2026-05-29 by improve_llm_enrich.py -->
<!-- source: docs\04-ai-collaborations\proposals\proposal-knowledge-space-x-ngt-memory.md -->

# Proposal: Knowledge-Space × Ngt-Memory

## Что это

Проект предлагает интеграцию двух слоёв системы: Knowledge-Space (персистентная память эпизодов) и Ngt-Memory (структурированный граф знаний). Целью интеграции является создание контекстно-зависимого retrieval с временной семантикой, где эпизоды из Knowledge-Space становятся узлами графа в Ngt-Memory.

## Ключевые особенности

- **Персистентная память эпизодов:** Knowledge-Space обеспечивает сохранение и управление эпизодической информацией как основного источника данных
- **Структурированный граф знаний:** Ngt-Memory реализует граф-базированное хранилище для организации знаний в виде связанных узлов
- **Временная семантика:** Интеграция обеспечивает retrieval с учётом временного контекста, связывая эпизоды с их позицией в последовательности событий

## Статус проекта

| Параметр | Значение |
|----------|----------|
| Язык/стек | — |
| Лицензия | — |
| Ссылка | — |

## Интеграция с Svyazi

Proposal позиционируется как исследовательское предложение, направленное на совершенствование архитектуры знаний и памяти в системе. Её реализация создаст основу для более эффективного управления контекстом и семантической релевантностью в рамках слоя интеграции Svyazi 2.0.
---
_Обогащено автоматически: 2026-05-29_
_Источник: [proposal-knowledge-space-x-ngt-memory](docs\04-ai-collaborations\proposals\proposal-knowledge-space-x-ngt-memory.md)_


## Использование
```bash
# Запуск
python scripts/improve_proposal_knowledge_space_x_ngt_memory_enriched.py
```
