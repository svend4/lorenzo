---
title: "Proposal: Agentfs × Agent-Memory-Mcp"
date: 2026-05-13
card_id: b3e56e82f28b
card_type: proposal
state: raw
tags: [proposal, agentfs, agent-memory-mcp, knowledge, memory, integration]
projects: [agentfs, agent-memory-mcp]
similarity: 0.282
score: 0.582
source: proposal-gen
---

# Proposal: Agentfs × Agent-Memory-Mcp

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> Интеграция knowledge-слоя (Agentfs) и memory-слоя (Agent-Memory-Mcp): Agentfs обеспечивает персистентную память эпизодов, Agent-Memory-Mcp хранит структурированный граф знаний. Интеграция: e

<!-- tags: proposal, agentfs, agent-memory-mcp, knowledge, memory, integration -->

## Гипотеза интеграции

Agentfs обеспечивает персистентную память эпизодов, Agent-Memory-Mcp хранит структурированный граф знаний. Интеграция: episodes из Agentfs как узлы графа в Agent-Memory-Mcp — контекстно-зависимый retrieval с временно́й семантикой.

## Проекты

| Параметр | Agentfs | Agent-Memory-Mcp |
|----------|———————|————————————————|
| Слой | knowledge | memory |
| Автор | kksudo | VitaliySemenov |
| Файл | `docs/05-habr-projects/knowledge/agentfs.md` | `docs/05-habr-projects/memory/agent-memory-mcp.md` |

## Метрики совместимости

| Метрика | Значение |
|---------|---------|
| Тематическое сходство (TF-IDF cosine) | 0.282 |
| Комплементарность слоёв | ✅ высокая |
| Итоговый рейтинг | 0.582 |

## Архитектурный контракт

Точка интеграции: **Card Envelope** (`card_type="agentfs"`, edges к `agent-memory-mcp`).

```json
{
  "card_type": "integration_proposal",
  "state": "raw",
  "projects": ["agentfs", "agent-memory-mcp"],
  "contract": "Card Envelope §3.1",
  "layer_a": "knowledge",
  "layer_b": "memory"
}
```

## Следующие шаги

- [ ] Изучить API Agentfs и Agent-Memory-Mcp
- [ ] Определить точку интеграции (Card Envelope / MCP)
- [ ] Связаться с kksudo и VitaliySemenov
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
- [proposal-wikontic-x-agent-memory-mcp](proposal-wikontic-x-agent-memory-mcp.md)
- [proposal-agentfs-x-yodoca](proposal-agentfs-x-yodoca.md)
- [proposal-knowledge-space-x-agent-memory-mcp](proposal-knowledge-space-x-agent-memory-mcp.md)
- [proposal-knowledge-space-x-ngt-memory](proposal-knowledge-space-x-ngt-memory.md)


<!-- backlinks -->

---

**Кто ссылается на этот документ (9):**
- [README](README.md)
- [proposal-agentfs-x-memnet](proposal-agentfs-x-memnet.md)
- [proposal-agentfs-x-yodoca](proposal-agentfs-x-yodoca.md)
- [proposal-knowledge-space-x-agent-memory-mcp](proposal-knowledge-space-x-agent-memory-mcp.md)
- [proposal-research-docs-liteparse-x-agent-memory-mcp](proposal-research-docs-liteparse-x-agent-memory-mcp.md)
- [proposal-research-docs-liteparse-x-agentfs](proposal-research-docs-liteparse-x-agentfs.md)
- [proposal-wikontic-x-agent-memory-mcp](proposal-wikontic-x-agent-memory-mcp.md)
- [READING_ORDER](../../READING_ORDER.md)
- _...ещё 1_

