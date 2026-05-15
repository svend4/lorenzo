---
date: 2026-05-15
tags: [memory, rag, orchestration, knowledge, ingestion]
state: normalized
---

# Memory MCP Server v0.8.0 (Part 2)

<!-- toc-auto -->
<!-- tags: memory-mcp-v2, docs -->


<!-- summary -->
> Хабр: https://habr.com/ru/articles/1033388/ GitHub: https://github.com/ipiton/agent-memory-mcp
Хабр: https://habr.com/ru/articles/1033388/  
GitHub: https://github.com/ipiton/agent-memory-mcp  
Слой: memory / MCP / engineering-intelligence  
Дата: май 2026 (2 дня назад от R06)  
Уникальность: Эволюция проекта из Round 01 — из


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** @ipiton  
**Хабр:** https://habr.com/ru/articles/1033388/  
**GitHub:** https://github.com/ipiton/agent-memory-mcp  
**Слой:** memory / MCP / engineering-intelligence  
**Дата:** май 2026 (2 дня назад от R06)  
**Уникальность:** Эволюция проекта из Round 01 — из инструмента семантического поиска в полноценный **memory backbone для инженерных агентов**. Новое: классификация инженерных артефактов (runbooks, postmortems, README, ADR), дифференциальное ранжирование в зависимости от типа запроса.

## Что изменилось с Round 01

| Версия | Возможности |
|--------|-------------|
| v0.1 (R01) | Семантический поиск по памяти агента, SQLite хранилище |
| v0.8.0 (R06) | Классификация артефактов, дифференциальное ранжирование, engineering memory backbone |

## Новые возможности v0.8.0

- **Классификация типов** инженерных артефактов: runbook, postmortem, README, ADR, incident report
- **Дифференциальное ранжирование**: для запросов «как исправить» — выше runbooks, для «что пошло не так» — выше postmortems
- MCP-интерфейс без изменений — drop-in upgrade
- Используется как backbone в production multi-agent системах

## Почему важно для Svyazi

Lorenzo уже знает этот проект (R01), но v0.8.0 меняет игру:  
классификация артефактов применима к `improve_named_entity_index.py` и Lorenzo-карточкам.  
Дифференциальное ранжирование = ответ на то, как сделать `improve_passage_retrieval.py` умнее.

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Memory MCP v2 + improve_passage_retrieval** | Тип запроса определяет источник: карточки vs документы |
| **Memory MCP v2 + Lorenzo improve_*.py** | Каждый скрипт пишет свои артефакты в memory backbone |
| **Memory MCP v2 + News System (R05)** | Новости как постоянная memory с типами: новость/тренд/событие |
| **Memory MCP v2 + Self-Aware MCP (R04)** | Время + тип контекста → точнее ранжированная память |

## Контакт

- GitHub: https://github.com/ipiton/agent-memory-mcp
- Хабр: часть 2 — https://habr.com/ru/articles/1033388/
- Хабр: часть 1 (R01) — уже в контактах (@ipiton)


## Использование
```bash
# Запуск
python scripts/improve_memory_mcp_v2.py
```

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
