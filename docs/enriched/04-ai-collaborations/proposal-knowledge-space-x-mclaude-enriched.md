# Proposal: Knowledge-Space × Mclaude

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
