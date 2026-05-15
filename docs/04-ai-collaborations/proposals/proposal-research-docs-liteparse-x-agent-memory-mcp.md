---
title: "Proposal: Research-Docs-Liteparse × Agent-Memory-Mcp"
date: 2026-05-13
card_id: f369f80c605c
card_type: proposal
state: approved
tags: [proposal, research-docs-liteparse, agent-memory-mcp, ingestion, memory, integration]
projects: [research-docs-liteparse, agent-memory-mcp]
similarity: 0.163
score: 0.413
source: proposal-gen
---

# Proposal: Research-Docs-Liteparse × Agent-Memory-Mcp

<!-- toc-auto -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> Интеграция ingestion-слоя (Research-Docs-Liteparse) и memory-слоя (Agent-Memory-Mcp): Research-Docs-Liteparse хранит знания с decay и consolidation, Agent-Memory-Mcp извлекает структурированные данные из до

<!-- tags: proposal, research-docs-liteparse, agent-memory-mcp, ingestion, memory, integration -->

## Гипотеза интеграции

Research-Docs-Liteparse хранит знания с decay и consolidation, Agent-Memory-Mcp извлекает структурированные данные из документов. Интеграция: extracted evidence из Agent-Memory-Mcp → episodes в Research-Docs-Liteparse — автоматическое накопление верифицированных фактов.

## Проекты

| Параметр | Research-Docs-Liteparse | Agent-Memory-Mcp |
|----------|———————————————————————|————————————————|
| Слой | ingestion | memory |
| Автор | nlaik | VitaliySemenov |
| Файл | `docs/05-habr-projects/knowledge/research-docs-liteparse.md` | `docs/05-habr-projects/memory/agent-memory-mcp.md` |

## Метрики совместимости

| Метрика | Значение |
|---------|---------|
| Тематическое сходство (TF-IDF cosine) | 0.163 |
| Комплементарность слоёв | ✅ высокая |
| Итоговый рейтинг | 0.413 |

## Архитектурный контракт

Точка интеграции: **Card Envelope** (`card_type="research-docs-liteparse"`, edges к `agent-memory-mcp`).

```json
{
  "card_type": "integration_proposal",
  "state": "raw",
  "projects": ["research-docs-liteparse", "agent-memory-mcp"],
  "contract": "Card Envelope §3.1",
  "layer_a": "ingestion",
  "layer_b": "memory"
}
```

## Следующие шаги

- [ ] Изучить API Research-Docs-Liteparse и Agent-Memory-Mcp
- [ ] Определить точку интеграции (Card Envelope / MCP)
- [ ] Связаться с nlaik и VitaliySemenov
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
- [proposal-research-docs-liteparse-x-agentfs](proposal-research-docs-liteparse-x-agentfs.md)
- [proposal-research-docs-liteparse-x-knowledge-space](proposal-research-docs-liteparse-x-knowledge-space.md)
- [proposal-knowledge-space-x-agent-memory-mcp](proposal-knowledge-space-x-agent-memory-mcp.md)
- [proposal-agentfs-x-agent-memory-mcp](proposal-agentfs-x-agent-memory-mcp.md)


<!-- backlinks -->

---

**Кто ссылается на этот документ (5):**
- [README](README.md)
- [proposal-research-docs-liteparse-x-agentfs](proposal-research-docs-liteparse-x-agentfs.md)
- [proposal-research-docs-liteparse-x-knowledge-space](proposal-research-docs-liteparse-x-knowledge-space.md)
- [READING_ORDER](../../READING_ORDER.md)
- [READING_TIME](../../READING_TIME.md)

