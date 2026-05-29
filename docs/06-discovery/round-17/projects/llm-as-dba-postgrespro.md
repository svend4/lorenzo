---
date: 2026-05-29
tags: [rag, orchestration, ingestion, architecture, collaboration]
state: normalized
---

# LLM as DBA — LLM-пайплайн для работы со сложными БД

<!-- toc-auto -->
<!-- tags: llm-as-dba-postgrespro, docs -->


<!-- summary -->
> Паттерн Schema Extractor полезен при масштабировании: если Svyazi 2.0 вырастет до PostgreSQL с десятками таблиц —
если Svyazi 2.0 вырастет до PostgreSQL с десятками таблиц —  
Schema Extractor Agent становится необходимым.


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** команда PostgresPro (enterprise Postgres компания)  
**Хабр:** https://habr.com/ru/companies/postgrespro/articles/907614/  
**GitHub:** не найден (корпоративная статья с описанием паттернов)  
**Слой:** orchestration / analytics / knowledge  
**Дата:** май 2025  
**Уникальность:** PostgresPro — ведущий разработчик enterprise Postgres в РФ — описывает LLM-пайплайн для управления **сложностью схем БД**: вместо передачи всей схемы в LLM создаётся **schema extractor** — интеллектуальный фильтр, выбирающий только нужные таблицы/колонки. Плюс паттерн LLM As DBA: экосистема агентов для администрирования.

## Главная проблема: размер схемы

```
Корпоративная БД: 500+ таблиц, 5000+ колонок
        ↓
Наивный подход: весь DDL в контекст LLM
  = 50k+ токенов, дорого, slow, неточно
        ↓
PostgresPro решение: Schema Extractor Agent
  = анализирует вопрос → выбирает только нужные таблицы → 2-5k токенов
```

## Schema Extractor — интеллектуальный фильтр

```
Вопрос: "Покажи клиентов с просроченными платежами"
        ↓
Schema Extractor (LLM):
  - анализирует вопрос
  - ищет семантически близкие таблицы
  - исключает нерелевантные (50+ таблиц → 3-4 таблицы)
        ↓
Text-to-SQL Agent (сфокусированный контекст)
        ↓
SQL запрос (точный, без галлюцинаций)
```

## LLM As DBA — экосистема агентов

```
┌─────────────────────────────────────┐
│         LLM As DBA Ecosystem        │
├──────────────┬──────────────────────┤
│ Schema Agent │ понимает структуру БД│
│ Query Agent  │ генерирует SQL        │
│ Explain Agent│ анализирует EXPLAIN  │
│ Index Agent  │ рекомендует индексы  │
│ Vacuum Agent │ мониторит bloat      │
└──────────────┴──────────────────────┘
```

## Бенчмарки (PostgresPro)

- Обучение и оценка на **Spider / BIRD** датасетах (EX/EM метрики)
- Тесты с **Qwen-0.6B** + GRPO/SFT для специализированных Text-to-SQL задач
- Schema Extractor снижает токены на **85–90%** при сохранении точности

## Применение к Lorenzo

Lorenzo использует SQLite (`audit.db`) с простой схемой.  
Паттерн Schema Extractor полезен при **масштабировании**:  
если Svyazi 2.0 вырастет до PostgreSQL с десятками таблиц —  
Schema Extractor Agent становится необходимым.

Комбинация Text2SQL X5Tech (R15) + Schema Extractor (R17) = полный enterprise DBA pipeline:
- X5Tech даёт техники генерации точного SQL (CoT, Schema-aware prompting)
- PostgresPro даёт intelligent schema filtering (не передаём всю схему)

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **LLM DBA + Text2SQL (R15)** | Schema Extractor (R17) + CoT+RAG техники (R15) = полный SQL-агент |
| **LLM DBA + BI Pattern (R12)** | BI-агент с intelligent schema filtering = точнее + дешевле |
| **LLM DBA + Vector DB (R12)** | Schema Extractor использует Qdrant для семантического поиска по схеме |
| **LLM DBA + Observability (R13)** | Langfuse трейсит каждый Schema Extractor → видна эффективность фильтрации |

## Контакт

- Статья: https://habr.com/ru/companies/postgrespro/articles/907614/ (май 2025)
- PostgresPro: postgrespro.ru
- Смежная статья: https://habr.com/ru/companies/postgrespro/articles/979820/ (выбор LLM для агентов)
- Spider BIRD бенчмарк: bird-bench.github.io

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
