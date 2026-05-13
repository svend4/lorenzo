---
title: "Proposal: Rufler × Agent-Memory-Mcp"
date: 2026-05-13
card_id: 729eed52f163
card_type: proposal
state: raw
tags: [proposal, rufler, agent-memory-mcp, orchestration, memory, integration]
projects: [rufler, agent-memory-mcp]
similarity: 0.202
score: 0.402
source: proposal-gen
---

# Proposal: Rufler × Agent-Memory-Mcp

<!-- summary -->
> Интеграция orchestration-слоя (Rufler) и memory-слоя (Agent-Memory-Mcp): Rufler типизирует memory-примитивы (episode/fact/proposal), Agent-Memory-Mcp оркестрирует агентов через декларативные па

<!-- tags: proposal, rufler, agent-memory-mcp, orchestration, memory, integration -->

## Гипотеза интеграции

Rufler типизирует memory-примитивы (episode/fact/proposal), Agent-Memory-Mcp оркестрирует агентов через декларативные пайплайны. Интеграция: Agent-Memory-Mcp читает релевантный контекст из Rufler перед каждым шагом пайплайна — stateful orchestration.

## Проекты

| Параметр | Rufler | Agent-Memory-Mcp |
|----------|——————|————————————————|
| Слой | orchestration | memory |
| Автор | zodigancode | VitaliySemenov |
| Файл | `docs/05-habr-projects/knowledge/rufler.md` | `docs/05-habr-projects/memory/agent-memory-mcp.md` |

## Метрики совместимости

| Метрика | Значение |
|---------|---------|
| Тематическое сходство (TF-IDF cosine) | 0.202 |
| Комплементарность слоёв | ✅ высокая |
| Итоговый рейтинг | 0.402 |

## Архитектурный контракт

Точка интеграции: **Card Envelope** (`card_type="rufler"`, edges к `agent-memory-mcp`).

```json
{
  "card_type": "integration_proposal",
  "state": "raw",
  "projects": ["rufler", "agent-memory-mcp"],
  "contract": "Card Envelope §3.1",
  "layer_a": "orchestration",
  "layer_b": "memory"
}
```

## Следующие шаги

- [ ] Изучить API Rufler и Agent-Memory-Mcp
- [ ] Определить точку интеграции (Card Envelope / MCP)
- [ ] Связаться с zodigancode и VitaliySemenov
- [ ] Создать proof-of-concept (≤ 1 неделя)
- [ ] Написать RFC в docs/rfcs/

## Статус ревью

- [ ] Одобрено
- [ ] Отклонено
- [ ] Отложено


---
_Сгенерировано improve_proposal_gen.py: 2026-05-13_
