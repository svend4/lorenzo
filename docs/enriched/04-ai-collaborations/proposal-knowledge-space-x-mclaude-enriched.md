---
date: 2026-05-29
tags: [memory, orchestration, knowledge, ingestion, architecture]
state: normalized
---

# Proposal: Knowledge-Space × Mclaude


<!-- summary -->
> Раздел proposal-knowledge-space-x-mclaude-enriched формируется автоматически из данных репозитория.

> [!NOTE]
> Раздел `proposal-knowledge-space-x-mclaude-enriched` формируется автоматически из данных репозитория.

<!-- alert-added -->

<!-- summary: Интеграция knowledge-слоя (Knowledge-Space) и orchestration-слоя (Mclaude): Knowledge-Space предоста -->
<!-- tags: proposal, knowledge-space, mclaude, knowledge, orchestration, integration -->
<!-- enriched: 2026-05-29 by improve_llm_enrich.py -->
<!-- source: docs\04-ai-collaborations\proposals\proposal-knowledge-space-x-mclaude.md -->

## Что это

Proposal описывает интеграцию Knowledge-Space (knowledge-слой) и Mclaude (orchestration-слой). Knowledge-Space предоставляет файловую систему знаний с рёбрами, Mclaude управляет агентными пайплайнами. Интеграция позволяет оркестратору навигировать по графу знаний как по рабочему пространству.

## Ключевые особенности

- **Граф как рабочая память:** Knowledge-Space функционирует как рабочая память оркестратора Mclaude, обеспечивая навигацию по структурированному пространству знаний с рёбрами
- **Двухслойная архитектура:** Разделение знания (Knowledge-Space) и управления пайплайнами (Mclaude) с возможностью их синергии через интеграцию
- **Файловая система знаний:** Knowledge-Space предоставляет файловую систему, организованную как граф с явно представленными связями между элементами

## Статус проекта

| Параметр | Значение |
|----------|---------|
| Язык/стек | — |
| Лицензия | — |
| Ссылка | — |

## Интеграция с Svyazi

Proposal представляет фундаментальное расширение архитектуры Svyazi через объединение knowledge и orchestration слоёв. Документ находится в статусе raw и служит основой для проектирования интеграции между Knowledge-Space и Mclaude в рамках экосистемы платформы.
---
_Обогащено автоматически: 2026-05-29_
_Источник: [proposal-knowledge-space-x-mclaude](docs\04-ai-collaborations\proposals\proposal-knowledge-space-x-mclaude.md)_


## Использование
```bash
# Запуск
python scripts/improve_proposal_knowledge_space_x_mclaude_enriched.py
```
