---
title: "Proposal: Knowledge-Space × Agent-Memory-Mcp"
date: 2026-05-13
card_id: 775a002b1753
card_type: proposal
state: normalized
tags: [proposal, knowledge-space, agent-memory-mcp, knowledge, memory, integration]
projects: [knowledge-space, agent-memory-mcp]
similarity: 0.214
score: 0.514
source: proposal-gen
---

# Proposal: Knowledge-Space × Agent-Memory-Mcp

<!-- summary -->
> Интеграция knowledge-слоя (Knowledge-Space) и memory-слоя (Agent-Memory-Mcp): Knowledge-Space обеспечивает персистентную память эпизодов, Agent-Memory-Mcp хранит структурированный граф знаний. Интег

<!-- tags: proposal, knowledge-space, agent-memory-mcp, knowledge, memory, integration -->

## Гипотеза интеграции

Knowledge-Space обеспечивает персистентную память эпизодов, Agent-Memory-Mcp хранит структурированный граф знаний. Интеграция: episodes из Knowledge-Space как узлы графа в Agent-Memory-Mcp — контекстно-зависимый retrieval с временно́й семантикой.

## Проекты

| Параметр | Knowledge-Space | Agent-Memory-Mcp |
|----------|———————————————|————————————————|
| Слой | knowledge | memory |
| Автор | AnastasiyaW | VitaliySemenov |
| Файл | `docs/05-habr-projects/knowledge/knowledge-space.md` | `docs/05-habr-projects/memory/agent-memory-mcp.md` |

## Метрики совместимости

| Метрика | Значение |
|---------|---------|
| Тематическое сходство (TF-IDF cosine) | 0.214 |
| Комплементарность слоёв | ✅ высокая |
| Итоговый рейтинг | 0.514 |

## Архитектурный контракт

Точка интеграции: **Card Envelope** (`card_type="knowledge-space"`, edges к `agent-memory-mcp`).

```json
{
  "card_type": "integration_proposal",
  "state": "raw",
  "projects": ["knowledge-space", "agent-memory-mcp"],
  "contract": "Card Envelope §3.1",
  "layer_a": "knowledge",
  "layer_b": "memory"
}
```

## Следующие шаги

- [ ] Изучить API Knowledge-Space и Agent-Memory-Mcp
- [ ] Определить точку интеграции (Card Envelope / MCP)
- [ ] Связаться с AnastasiyaW и VitaliySemenov
- [ ] Создать proof-of-concept (≤ 1 неделя)
- [ ] Написать RFC в docs/rfcs/

## Статус ревью

- [ ] Одобрено
- [ ] Отклонено
- [ ] Отложено


---
_Сгенерировано improve_proposal_gen.py: 2026-05-13_
