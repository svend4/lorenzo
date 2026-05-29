---
date: 2026-05-29
tags: [memory, rag, orchestration, knowledge, ingestion]
state: normalized
---

# RAG-агент для инцидент-менеджмента — автоматизация SRE через AI

<!-- toc-auto -->
<!-- tags: rag-incident-management, docs -->


<!-- summary -->
> Паттерн incident management = knowledge maintenance agent: "Инцидент" = битая ссылка / устаревший документ / противоречие
 "Инцидент" = битая ссылка / устаревший документ / противоречие
 RAG ищет: как аналогичная проблема решалась раньше
 Агент предлагает: конкретный скрипт ( ,  )
Связь с ADD Chronicles (R13): A


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** команда OTUS (образовательная платформа, практический кейс)  
**Хабр:** https://habr.com/ru/companies/otus/articles/912228/  
**GitHub:** не найден (статья с архитектурными паттернами и примерами)  
**Слой:** orchestration / knowledge / analytics  
**Дата:** 2025  
**Уникальность:** Первый детальный русскоязычный кейс применения RAG-агентов в DevOps/SRE — не теория, а конкретная архитектура: runbook-агент, который при поступлении алерта автоматически ищет похожие инциденты в базе знаний, предлагает диагностику и шаги исправления. Сочетание retrieval (исторические инциденты) + generation (plan действий) + tool use (kubectl, curl, pg_dump).

## Архитектура

```
Алерт (PagerDuty / Grafana / Prometheus)
        ↓
Incident Agent
  Stage 1: Enrichment
    → retrieve(alert.service + alert.error_type)
    → похожие исторические инциденты из базы
    → runbook для данного сервиса
        ↓
  Stage 2: Diagnosis
    → tool_call: kubectl describe pod <name>
    → tool_call: get_metrics(service, time_range)
    → tool_call: check_dependencies(service)
        ↓
  Stage 3: Action Plan
    → LLM: "На основе инцидента X (похожего) и текущих метрик → план"
    → priority: P1/P2/P3
    → next_steps: [конкретные команды]
        ↓
  Stage 4: Post-Mortem
    → записать инцидент + решение → обновить базу знаний
    → [новый пример для будущего retrieval]
```

## База знаний инцидентов

```
Структура документа-инцидента:
  - service: payment-service
  - error: OutOfMemoryError в контейнере
  - root_cause: memory leak в connection pool
  - resolution: restart pod + уменьшить max_connections
  - duration: 45 минут
  - severity: P1
  - tags: [memory, java, kubernetes, connection-pool]
```

**Retrieval**: BM25 + семантический поиск по `error + service + tags`.

## RAG-паттерны для SRE

### Runbook RAG
```
Алерт: "CPU > 90% на сервисе auth"
  → retrieve runbook: auth-service-cpu-runbook.md
  → LLM: адаптировать шаги под текущий контекст
  → generate: персонализированный план (не generic)
```

### Historical RAG
```
Алерт: "DB connection timeout"
  → retrieve: 5 похожих инцидентов за последние 6 месяцев
  → LLM: "В 4 из 5 случаев причина — connection pool exhaustion"
  → suggest: первым делом проверить pg_stat_activity
```

### Predictive RAG
```
Метрики за последний час (медленный рост)
  → retrieve: паттерны предшествовавшие прошлым инцидентам
  → LLM: "Похоже на pre-OOM паттерн, рекомендую скейлинг заранее"
```

## Стек

| Компонент | Технология | Назначение |
|-----------|-----------|-----------|
| Алерты | PagerDuty / Alertmanager | источник событий |
| База знаний | Markdown + векторная БД | исторические инциденты |
| Retrieval | BM25 + embeddings | поиск похожих случаев |
| LLM | GPT-4 / GigaChat / локальный | генерация плана |
| Tool use | kubectl, bash, curl | диагностика |
| Post-mortem | auto-write в базу | обучение агента |

## Self-improving loop

```
Инцидент решён
  ↓
Агент записывает: {alert, diagnosis, solution, duration}
  ↓
Следующий похожий инцидент
  ↓
Retrieval найдёт свежий пример → лучший план
```

Система улучшается с каждым инцидентом — без явного обучения.

## Применение к Lorenzo / Svyazi

Lorenzo — knowledge OS: база знаний проектов + агенты обработки.  
Паттерн incident management = **knowledge maintenance agent**:
- "Инцидент" = битая ссылка / устаревший документ / противоречие
- RAG ищет: как аналогичная проблема решалась раньше
- Агент предлагает: конкретный скрипт (`improve_broken_links.py`, `improve_contradiction_check.py`)

Связь с ADD Chronicles (R13): ADD feedback loop + RAG база решений = self-healing knowledge base.

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Incident RAG + ADD (R13)** | ADD feedback loop ← RAG исторических решений |
| **Incident RAG + Langfuse (R13)** | Каждый инцидент трейсится + Langfuse дашборд |
| **Incident RAG + Agentic RAG (R18)** | Retrieval-петля для поиска корневой причины |
| **Incident RAG + LLM DBA (R17)** | Schema Extractor диагностирует DB-инциденты |
| **Incident RAG + No-LangChain (R16)** | Агент без LangChain: function=diagnose, graph=workflow |

## Контакт

- Статья: https://habr.com/ru/companies/otus/articles/912228/ (2025)
- Смежная (SRE + AI): https://habr.com/ru/articles/896000/
- Incident.io blog: incident.io/blog/ai-incident-management
- OpenTelemetry + LLM: opentelemetry.io/docs/

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
