---
date: 2026-05-29
tags: [memory, rag, knowledge, ingestion, architecture]
state: normalized
---

# Proposal: Knowledge-Space × Yodoca


<!-- summary -->
> Раздел proposal-knowledge-space-x-yodoca-enriched формируется автоматически из данных репозитория.

> [!NOTE]
> Раздел `proposal-knowledge-space-x-yodoca-enriched` формируется автоматически из данных репозитория.

<!-- alert-added -->

<!-- summary: Интеграция knowledge-слоя (Knowledge-Space) и memory-слоя (Yodoca): Knowledge-Space обеспечивает пер -->
<!-- tags: proposal, knowledge-space, yodoca, knowledge, memory, integration -->
<!-- enriched: 2026-05-29 by improve_llm_enrich.py -->
<!-- source: docs\04-ai-collaborations\proposals\proposal-knowledge-space-x-yodoca.md -->

# Proposal: Knowledge-Space × Yodoca

## Что это

Proposal описывает интеграцию двух слоёв системы: Knowledge-Space (персистентная память эпизодов) и Yodoca (структурированный граф знаний). Цель интеграции — обеспечить контекстно-зависимый retrieval с временной семантикой, где эпизоды из Knowledge-Space становятся узлами графа в Yodoca.

## Ключевые особенности

- **Двухслойная архитектура:** Knowledge-Space отвечает за персистентную память эпизодов, Yodoca — за структурированное хранение графа знаний
- **Эпизоды как узлы графа:** episodes из Knowledge-Space преобразуются в узлы графа в Yodoca для интеграции
- **Временная семантика:** Retrieval организован с учётом контекста и временных параметров эпизодов

## Статус проекта

| Параметр | Значение |
|----------|----------|
| Язык/стек | — |
| Лицензия | — |
| Ссылка | — |

## Интеграция с Svyazi

Proposal входит в слой knowledge-memory интеграции, определяя архитектурный подход к объединению механизмов хранения и извлечения знаний в базе знаний Svyazi 2.0.
---
_Обогащено автоматически: 2026-05-29_
_Источник: [proposal-knowledge-space-x-yodoca](docs\04-ai-collaborations\proposals\proposal-knowledge-space-x-yodoca.md)_


## Использование
```bash
# Запуск
python scripts/improve_proposal_knowledge_space_x_yodoca_enriched.py
```
