---
date: 2026-06-05
tags: [memory, orchestration, knowledge, ingestion, architecture]
state: normalized
---

# Proposal: Knowledge-Space × Rufler


<!-- summary -->
> Раздел proposal-knowledge-space-x-rufler-enriched формируется автоматически из данных репозитория.

> [!NOTE]
> Раздел `proposal-knowledge-space-x-rufler-enriched` формируется автоматически из данных репозитория.

<!-- alert-added -->

<!-- summary: Интеграция knowledge-слоя (Knowledge-Space) и orchestration-слоя (Rufler): Knowledge-Space предостав -->
<!-- tags: proposal, knowledge-space, rufler, knowledge, orchestration, integration -->
<!-- enriched: 2026-05-29 by improve_llm_enrich.py -->
<!-- source: docs\04-ai-collaborations\proposals\proposal-knowledge-space-x-rufler.md -->

## Что это

Proposal по интеграции Knowledge-Space (knowledge-слой с файловой системой знаний на основе графов с рёбрами) и Rufler (orchestration-слой для управления агентными пайплайнами). Ключевая идея: Rufler использует граф Knowledge-Space как рабочую память оркестратора для навигации по пространству знаний.

## Ключевые особенности

- **Knowledge-слой с рёбрами:** Knowledge-Space предоставляет файловую систему знаний, структурированную как граф с рёбрами между узлами
- **Orchestration через графы:** Rufler навигирует по Knowledge-Space как по рабочему пространству, используя граф в качестве рабочей памяти оркестратора
- **Агентные пайплайны:** Rufler управляет пайплайнами агентов, которые могут взаимодействовать с графом знаний

## Статус проекта

| Параметр | Значение |
|----------|----------|
| Язык/стек | — |
| Лицензия | — |
| Ссылка | — |

## Интеграция с Svyazi

Proposal является исследовательским заданием на уровне слоя proposal в архитектуре Svyazi 2.0. Интеграция Knowledge-Space × Rufler определяет архитектурный паттерн взаимодействия между knowledge-слоем и orchestration-слоем системы.
---
_Обогащено автоматически: 2026-05-29_
_Источник: [proposal-knowledge-space-x-rufler](docs\04-ai-collaborations\proposals\proposal-knowledge-space-x-rufler.md)_


## Использование
```bash
# Запуск
python scripts/improve_proposal_knowledge_space_x_rufler_enriched.py
```
