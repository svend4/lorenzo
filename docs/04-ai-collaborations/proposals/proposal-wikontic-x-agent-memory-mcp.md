---
title: "Proposal: Wikontic × Agent-Memory-Mcp"
date: 2026-05-13
card_id: f0abc228e126
card_type: proposal
state: raw
tags: [proposal, wikontic, agent-memory-mcp, knowledge, memory, integration]
projects: [wikontic, agent-memory-mcp]
similarity: 0.187
score: 0.487
source: proposal-gen
---

# Proposal: Wikontic × Agent-Memory-Mcp

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> Интеграция knowledge-слоя (Wikontic) и memory-слоя (Agent-Memory-Mcp): Wikontic обеспечивает персистентную память эпизодов, Agent-Memory-Mcp хранит структурированный граф знаний. Интеграция: 

<!-- tags: proposal, wikontic, agent-memory-mcp, knowledge, memory, integration -->

## Гипотеза интеграции

Wikontic обеспечивает персистентную память эпизодов, Agent-Memory-Mcp хранит структурированный граф знаний. Интеграция: episodes из Wikontic как узлы графа в Agent-Memory-Mcp — контекстно-зависимый retrieval с временно́й семантикой.

## Проекты

| Параметр | Wikontic | Agent-Memory-Mcp |
|----------|————————|————————————————|
| Слой | knowledge | memory |
| Автор | VitalyOborin | VitaliySemenov |
| Файл | `docs/05-habr-projects/knowledge/wikontic.md` | `docs/05-habr-projects/memory/agent-memory-mcp.md` |

## Метрики совместимости

| Метрика | Значение |
|---------|---------|
| Тематическое сходство (TF-IDF cosine) | 0.187 |
| Комплементарность слоёв | ✅ высокая |
| Итоговый рейтинг | 0.487 |

## Архитектурный контракт

Точка интеграции: **Card Envelope** (`card_type="wikontic"`, edges к `agent-memory-mcp`).

```json
{
  "card_type": "integration_proposal",
  "state": "raw",
  "projects": ["wikontic", "agent-memory-mcp"],
  "contract": "Card Envelope §3.1",
  "layer_a": "knowledge",
  "layer_b": "memory"
}
```

## Следующие шаги

- [ ] Изучить API Wikontic и Agent-Memory-Mcp
- [ ] Определить точку интеграции (Card Envelope / MCP)
- [ ] Связаться с VitalyOborin и VitaliySemenov
- [ ] Создать proof-of-concept (≤ 1 неделя)
- [ ] Написать RFC в docs/rfcs/

## Статус ревью

- [ ] Одобрено
- [ ] Отклонено
- [ ] Отложено


---
_Сгенерировано improve_proposal_gen.py: 2026-05-13_

<!-- see-also -->

---

**Смотрите также:**
- [proposal-wikontic-x-yodoca](proposal-wikontic-x-yodoca.md)
- [proposal-agentfs-x-agent-memory-mcp](proposal-agentfs-x-agent-memory-mcp.md)
- [proposal-wikontic-x-ngt-memory](proposal-wikontic-x-ngt-memory.md)
- [proposal-knowledge-space-x-agent-memory-mcp](proposal-knowledge-space-x-agent-memory-mcp.md)


<!-- backlinks -->

---

**Кто ссылается на этот документ (10):**
- [README](README.md)
- [proposal-01-synthesis-x-wikontic](proposal-01-synthesis-x-wikontic.md)
- [proposal-agentfs-x-agent-memory-mcp](proposal-agentfs-x-agent-memory-mcp.md)
- [proposal-agentfs-x-yodoca](proposal-agentfs-x-yodoca.md)
- [proposal-knowledge-space-x-agent-memory-mcp](proposal-knowledge-space-x-agent-memory-mcp.md)
- [proposal-wikontic-x-memnet](proposal-wikontic-x-memnet.md)
- [proposal-wikontic-x-ngt-memory](proposal-wikontic-x-ngt-memory.md)
- [proposal-wikontic-x-yodoca](proposal-wikontic-x-yodoca.md)
- _...ещё 2_

