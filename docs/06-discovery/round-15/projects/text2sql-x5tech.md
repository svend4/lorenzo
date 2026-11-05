---
date: 2026-06-05
tags: [rag, orchestration, security, architecture, roadmap]
state: normalized
---

# Text2SQL X5Tech — выжимаем максимум из open-source для SQL-агентов

<!-- toc-auto -->
<!-- tags: text2sql-x5tech, docs -->


<!-- summary -->
> Автор: команда X5 Tech (X5 Retail Group) Хабр: https://habr.com/ru/companies/X5Tech/articles/981494/
Хабр: https://habr.com/ru/companies/X5Tech/articles/981494/  
GitHub: не найден (корпоративная статья с открытыми техниками)  
Слой: orchestration / analytics / knowledge  
Дата: февраль 2026  
Уникальность:


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** команда X5 Tech (X5 Retail Group)  
**Хабр:** https://habr.com/ru/companies/X5Tech/articles/981494/  
**GitHub:** не найден (корпоративная статья с открытыми техниками)  
**Слой:** orchestration / analytics / knowledge  
**Дата:** февраль 2026  
**Уникальность:** Практический гайд от X5 (крупнейший ритейлер РФ): как добиться точного Text-to-SQL на open-source моделях с **русскоязычными данными**. Не просто синтаксически верный SQL — семантически точный, решающий задачу. Результаты на MERA и RuLLMArena бенчмарках. Применим к любому корпоративному BI-агенту.

## Ключевые техники (из статьи)

### Проблема: галлюцинации в SQL

```
Пользователь: "Покажи топ-10 магазинов по выручке за март"
Наивный LLM:  SELECT * FROM stores ORDER BY revenue LIMIT 10
Правильный:   SELECT store_id, SUM(revenue) as total
              FROM sales WHERE month = 3 AND year = 2026
              GROUP BY store_id ORDER BY total DESC LIMIT 10
```

### Техники повышения точности

| Техника | Что даёт |
|---------|---------|
| **Schema-aware prompting** | Детальные описания таблиц и колонок в промпте |
| **Chain-of-Thought (CoT)** | Агент сначала план, потом SQL |
| **RAG по схеме** | Поиск релевантных таблиц перед генерацией |
| **Self-correction loop** | SQL → выполнение → ошибка → LLM исправляет |
| **Few-shot примеры** | Примеры вопрос/SQL для данной схемы |
| **Декомпозиция** | Сложный вопрос → подзапросы → сборка |

### Результаты на русских данных

- Тестирование на **MERA** (русскоязычный ML-бенчмарк) и **RuLLMArena**
- Лучшие open-source модели для RU Text2SQL: Qwen 2.5 Coder, DeepSeek Coder V2
- CoT + schema-aware = значительный прирост точности vs baseline

## Multi-agent архитектура (advanced)

```
Вопрос пользователя
        ↓
Schema Retriever (RAG: найти релевантные таблицы)
        ↓
SQL Generator (CoT: план → SQL)
        ↓
SQL Validator (синтаксис + безопасность)
        ↓
SQL Executor + result checker
        ↓
Result Interpreter (объяснение на русском)
```

## Применение к Lorenzo

Lorenzo имеет `audit.db` (SQLite: все события MCP-серверов).  
BI Agent Pattern (R12) + X5Tech техники = **агент отвечает на вопросы об audit.db**:  
— «Какой MCP-сервер вызывался чаще всего на этой неделе?»  
— «Покажи медленные вызовы за последние 24 часа»

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Text2SQL + BI Pattern (R12)** | Техники X5Tech в BI-агенте: Schema-aware + CoT = точный SQL над Lorenzo KPI |
| **Text2SQL + Vector DB (R12)** | RAG по схеме через Qdrant: поиск релевантных таблиц перед генерацией |
| **Text2SQL + Observability (R13)** | Langfuse трейсит каждый SQL-запрос агента → видны ошибки и исправления |
| **Text2SQL + DSPy (R14)** | DSPy автооптимизирует Text2SQL промпты под конкретную схему БД |

## Контакт

- Статья: https://habr.com/ru/companies/X5Tech/articles/981494/ (февраль 2026)
- X5 Tech Хабр: https://habr.com/ru/companies/X5Tech/
- Смежная (multi-agent подход, GazPromBank): https://habr.com/ru/companies/gazprombank/articles/965292/

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
