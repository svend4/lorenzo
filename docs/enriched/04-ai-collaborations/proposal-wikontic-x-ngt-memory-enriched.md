# Proposal: Wikontic × Ngt-Memory

<!-- summary: Интеграция knowledge-слоя (Wikontic) и memory-слоя (Ngt-Memory): Wikontic обеспечивает персистентную -->
<!-- tags: proposal, wikontic, ngt-memory, knowledge, memory, integration -->
<!-- enriched: 2026-05-29 by improve_llm_enrich.py -->
<!-- source: docs\04-ai-collaborations\proposals\proposal-wikontic-x-ngt-memory.md -->

# Proposal: Wikontic × Ngt-Memory

## Что это
Проект предлагает интеграцию knowledge-слоя (Wikontic) и memory-слоя (Ngt-Memory) для создания единой системы управления знаниями и памятью. Wikontic обеспечивает персистентную память эпизодов, а Ngt-Memory хранит структурированный граф знаний, позволяя реализовать контекстно-зависимый поиск с временной семантикой.

## Ключевые особенности
- **Двухслойная архитектура:** разделение персистентной памяти эпизодов (Wikontic) и структурированного графа знаний (Ngt-Memory)
- **Эпизоды как узлы графа:** преобразование эпизодов из Wikontic в узлы графа Ngt-Memory для унифицированного представления
- **Контекстно-временной retrieval:** поиск знаний с учётом временных зависимостей и контекстных связей между эпизодами

## Статус проекта
| Параметр | Значение |
|----------|----------|
| Язык/стек | — |
| Лицензия | — |
| Ссылка | — |

## Интеграция с Svyazi
Проект находится на этапе proposal и предназначен для слоя знаний и памяти архитектуры Svyazi 2.0. Интеграция Wikontic и Ngt-Memory позволит создать единую систему контекстно-осведомленного поиска и управления эпизодической информацией в рамках системы.
---
_Обогащено автоматически: 2026-05-29_
_Источник: [proposal-wikontic-x-ngt-memory](docs\04-ai-collaborations\proposals\proposal-wikontic-x-ngt-memory.md)_
