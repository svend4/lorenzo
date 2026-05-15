---
date: 2026-05-15
tags: [orchestration, architecture, self-improve, collaboration]
state: normalized
---

# LLM Observability Pattern — AI анализирует AI с Langfuse

<!-- toc-auto -->
<!-- tags: llm-observability-langfuse, docs -->


<!-- summary -->
> Автор: независимый разработчик (Хабр) Хабр: https://habr.com/ru/articles/987230/
Хабр: https://habr.com/ru/articles/987230/  
GitHub: https://github.com/langfuse/langfuse (Langfuse core, MIT)  
Слой: orchestration / observability / monitoring  
Дата: 2025–2026  
Уникальность: Паттерн «AI ан


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** независимый разработчик (Хабр)  
**Хабр:** https://habr.com/ru/articles/987230/  
**GitHub:** https://github.com/langfuse/langfuse (Langfuse core, MIT)  
**Слой:** orchestration / observability / monitoring  
**Дата:** 2025–2026  
**Уникальность:** Паттерн «AI анализирует AI»: Langfuse собирает трейсы LLM-агентов, Go-бэкенд передаёт trace ID в LLM, та возвращает структурированные рекомендации. Полностью open-source. Телеметрия агентов переходит от «nice to have» к «must have».

## Архитектура

```
LLM-агент (вызов) → Langfuse (трейсинг) → trace_id
                                              ↓
                           Go-бэкенд / Python-скрипт
                                              ↓
                           LLM-анализатор (читает трейс)
                                              ↓
                    Структурированный отчёт: аномалии / рекомендации
```

### Компоненты

| Компонент | Роль |
|-----------|------|
| **Langfuse** | Сбор трейсов, метрик, промптов, latency, cost |
| **Langfuse API** | Получить полный трейс по trace_id |
| **LLM-анализатор** | Интерпретация трейса: аномалии, паттерны, рекомендации |
| **Go / Python бэкенд** | Glue: подписка на трейсы → LLM-запрос → отчёт |

## Что видит Langfuse

- Полная цепочка вызовов агента (spans)
- Latency каждого шага
- Стоимость токенов (input / output)
- Версии промптов и модели
- Ошибки и fallback-пути

## Почему важно для Lorenzo

Lorenzo имеет 12 MCP-серверов и `audit.db` (SQLite лог событий).  
Сейчас: `improve_mcp_dashboard.py` — статичный Markdown.  
С паттерном: **LLM читает audit.db → находит аномалии → генерирует ALERT.md**.  
Это Ступень 7 автономии: агент наблюдает сам за собой.

### Применение к Lorenzo

```bash
# Текущий стек:
improve_audit_db.py → audit.db
improve_mcp_dashboard.py → MCP_DASHBOARD.md (статика)

# С паттерном observability:
audit.db → LLM-analyzer → аномалии → ALERTS.md
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Observability + improve_audit_db** | LLM читает audit.db → находит медленные вызовы, аномалии |
| **Observability + improve_watcher (R07)** | Watcher видит аномалии в реальном времени через Langfuse |
| **Observability + openLight (R07)** | openLight safety + трейсинг = полная видимость всех решений агента |
| **Observability + 9-агентов (R07)** | Мониторинг 9-агентного оркестратора: bottlenecks, cost per agent |

## Контакт

- Статья (паттерн): https://habr.com/ru/articles/987230/
- Большой гайд: https://habr.com/ru/articles/972480/
- Langfuse GitHub: https://github.com/langfuse/langfuse (MIT, 18k+ stars)
- Self-hosted: docker compose up (Postgres + Next.js + Python worker)

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
