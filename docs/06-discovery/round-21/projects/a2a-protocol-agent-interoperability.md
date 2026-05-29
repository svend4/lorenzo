---
date: 2026-05-29
tags: [memory, rag, orchestration, knowledge, ingestion]
state: normalized
---

# A2A Протокол v1.0 — стандарт межагентного взаимодействия (Google + Cloud.ru)

<!-- toc-auto -->
<!-- tags: a2a-protocol-agent-interoperability, docs -->


<!-- summary -->
> Task — долгоживущая операция A2A vs MCP: дополняют, не конкурируют Протокол | Для чего | Направление |
 
A2A vs MCP: дополняют, не конкурируют
 Протокол | Для чего | Направление |
 ---------|----------|-------------|
 MCP | Агент ↔ Инструменты/Ресурсы | клиент-сервер (LLM→Tool) |
 A2A | Агент ↔ Агент | peer-to-peer (Agent→


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** команда Cloud.ru (российский облачный провайдер)  
**Хабр:** https://habr.com/ru/companies/cloud_ru/articles/1011868/  
**GitHub:** https://github.com/google/a2a-protocol (Apache 2.0, Google)  
**Слой:** orchestration / memory / knowledge  
**Дата:** апрель 2026 (v1.0 production-ready)  
**Уникальность:** A2A — первый production-ready открытый стандарт для межагентного взаимодействия: агенты от разных команд, фреймворков и провайдеров могут координироваться без единой кодовой базы. Cloud.ru первыми в РФ описали A2A v1.0 с Russian enterprise-контекстом и запустили Evolution AI Agents — маркетплейс A2A-совместимых агентов.

## Проблема без A2A

```
Без стандарта:
  Agent-A (LangGraph) ←→ Agent-B (CrewAI)?
    → разные API, разные форматы, разные транспорты
    → integration hell: N агентов = N*(N-1) точек интеграции

C A2A:
  Agent-A ←→ [A2A протокол] ←→ Agent-B
    → единый формат: Agent Cards, Tasks, Push-уведомления
    → N агентов = N адаптеров A2A (не N²)
```

## Архитектура A2A v1.0

```
Компоненты:
  ┌─────────────────────────────────────┐
  │           A2A Ecosystem             │
  ├──────────────┬──────────────────────┤
  │ Agent Card   │ JSON-манифест агента  │
  │              │ capabilities, schema  │
  ├──────────────┼──────────────────────┤
  │ Task         │ долгоживущая операция │
  │              │ id, status, artifacts │
  ├──────────────┼──────────────────────┤
  │ Push Notif   │ async callback        │
  │              │ когда задача готова   │
  ├──────────────┼──────────────────────┤
  │ Multi-tenant │ изоляция данных       │
  │              │ разные клиенты = разн │
  └──────────────┴──────────────────────┘
```

## Agent Card — визитная карточка агента

```json
{
  "name": "LorenzoEnrichmentAgent",
  "description": "Обогащает проектные файлы через LLM",
  "version": "1.2.0",
  "capabilities": {
    "enrich_project_file": {
      "input": {"file_path": "string", "section": "string"},
      "output": {"enriched_content": "string", "tags": ["string"]},
      "cost_estimate": {"tokens": 2000, "latency_ms": 5000}
    }
  },
  "transport": {
    "protocol": "https",
    "endpoint": "https://lorenzo.local/a2a/enrich"
  },
  "auth": {"type": "bearer"}
}
```

Любой A2A-совместимый оркестратор видит эту карточку и может вызвать агента.

## Task — долгоживущая операция

```python
# Создать задачу:
task = a2a_client.create_task(
    agent="LorenzoEnrichmentAgent",
    capability="enrich_project_file",
    input={"file_path": "docs/05-habr-projects/memory/yodoca.md"}
)

# Асинхронный результат через push:
@app.post("/a2a/webhook")
async def receive_result(notification: A2ANotification):
    if notification.task_id == task.id:
        result = notification.artifact  # enriched_content, tags

# Или polling:
result = a2a_client.wait_task(task.id, timeout=30)
```

## A2A vs MCP: дополняют, не конкурируют

| Протокол | Для чего | Направление |
|---------|----------|-------------|
| **MCP** | Агент ↔ Инструменты/Ресурсы | клиент-сервер (LLM→Tool) |
| **A2A** | Агент ↔ Агент | peer-to-peer (Agent→Agent) |

```
Пример связки MCP + A2A:
  Оркестратор-агент (A2A)
    → вызывает Lorenzo-агент через A2A
    → Lorenzo-агент использует MCP-инструменты (search, graph, ops)
    → результат через A2A push → оркестратор
```

## Cloud.ru Evolution AI Agents

```
Маркетплейс A2A-агентов:
  - выбрать готового агента из каталога
  - или загрузить свой через Docker image
  - автоматически генерирует Agent Card
  - интегрирует с корпоративными системами

Особенность: multi-tenancy нативно
  → разные бизнес-юниты = разные tenant'ы
  → агенты изолированы, но могут кооперировать через A2A
```

## Практика v1.0 (март 2026)

```
A2A v1.0 Production-Ready features:
  ✅ Multi-tenancy с изоляцией данных
  ✅ Task lifecycle: PENDING → WORKING → DONE/FAILED
  ✅ Push notifications (webhook/SSE)
  ✅ Agent Card discovery (well-known endpoint)
  ✅ Streaming artifacts (частичные результаты)
  ✅ Human in Loop signals (агент запрашивает одобрение)
```

## Применение к Lorenzo

Lorenzo имеет 12 MCP-серверов и 159+ скриптов.  
A2A = следующий уровень: Lorenzo как участник мультиагентной экосистемы:

```json
// Lorenzo Agent Card:
{
  "name": "LorenzoKnowledgeAgent",
  "capabilities": {
    "search_docs": {"input": {"query": "string"}, ...},
    "enrich_project": {"input": {"project_url": "string"}, ...},
    "find_collaborators": {"input": {"query": "string"}, ...}
  }
}
```

Svyazi 2.0 = оркестратор → Lorenzo = специализированный A2A-агент знаний.

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **A2A + 3-агент кейс (R21)** | A2A координирует Discovery/Enricher/Monitor агентов Lorenzo |
| **A2A + MCP (Lorenzo)** | Гибрид: MCP для инструментов + A2A для координации агентов |
| **A2A + No-LangChain (R16)** | A2A = стандарт координации без LangGraph/CrewAI |
| **A2A + TRAIL spec (R04)** | TRAIL задаёт поведение агента, A2A — как агенты общаются |
| **A2A + Incident RAG (R18)** | SRE: агенты диагностики координируются через A2A |

## Контакт

- Статья Cloud.ru: https://habr.com/ru/companies/cloud_ru/articles/1011868/ (апрель 2026)
- A2A GitHub: https://github.com/google/a2a-protocol (Apache 2.0)
- A2A спецификация: a2aprotocol.io
- Смежная (A2A vs MCP): https://habr.com/ru/articles/900498/
- Смежная (ACP протокол): https://habr.com/ru/companies/otus/articles/915156/

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
