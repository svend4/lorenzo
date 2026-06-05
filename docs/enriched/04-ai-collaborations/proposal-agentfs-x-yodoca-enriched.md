# Proposal: Agentfs × Yodoca

<!-- summary: Интеграция knowledge-слоя (Agentfs) и memory-слоя (Yodoca): Agentfs обеспечивает персистентную памят -->
<!-- tags: proposal, agentfs, yodoca, knowledge, memory, integration -->
<!-- enriched: 2026-05-29 by improve_llm_enrich.py -->
<!-- source: docs\04-ai-collaborations\proposals\proposal-agentfs-x-yodoca.md -->

# Proposal: Agentfs × Yodoca

## Что это

Предложение по интеграции двух компонентов архитектуры: knowledge-слоя Agentfs и memory-слоя Yodoca. Agentfs обеспечивает персистентную память эпизодов, Yodoca хранит структурированный граф знаний. Интеграция направлена на реализацию контекстно-зависимого retrieval с временной семантикой.

## Ключевые особенности

- **Episodes as graph nodes:** Эпизоды из Agentfs трансформируются в узлы структурированного графа в Yodoca
- **Persistent episode memory:** Agentfs обеспечивает долгосрочное хранение эпизодической памяти
- **Temporal-semantic retrieval:** Интеграция позволяет извлекать знания с учётом временного контекста и семантических связей

## Статус проекта

| Параметр | Значение |
|----------|----------|
| Язык/стек | — |
| Лицензия | — |
| Ссылка | — |

## Интеграция с Svyazi

Proposal служит аналитической основой для проектирования интеграции между слоями памяти и знаний в архитектуре. Документирует гипотезу взаимодействия Agentfs и Yodoca, определяя механизмы трансформации данных и семантического поиска на уровне proposal-слоя.
---
_Обогащено автоматически: 2026-05-29_
_Источник: [proposal-agentfs-x-yodoca](docs\04-ai-collaborations\proposals\proposal-agentfs-x-yodoca.md)_
