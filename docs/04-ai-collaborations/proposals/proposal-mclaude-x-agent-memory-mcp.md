---
title: "Proposal: Mclaude × Agent-Memory-Mcp"
date: 2026-05-13
card_id: 82437b5fd6b6
card_type: proposal
state: normalized
tags: [proposal, mclaude, agent-memory-mcp, orchestration, memory, integration]
projects: [mclaude, agent-memory-mcp]
similarity: 0.239
score: 0.439
source: proposal-gen
---

# Proposal: Mclaude × Agent-Memory-Mcp

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> Интеграция orchestration-слоя (Mclaude) и memory-слоя (Agent-Memory-Mcp): Mclaude типизирует memory-примитивы (episode/fact/proposal), Agent-Memory-Mcp оркестрирует агентов через декларативные п

<!-- tags: proposal, mclaude, agent-memory-mcp, orchestration, memory, integration -->

## Гипотеза интеграции

Mclaude типизирует memory-примитивы (episode/fact/proposal), Agent-Memory-Mcp оркестрирует агентов через декларативные пайплайны. Интеграция: Agent-Memory-Mcp читает релевантный контекст из Mclaude перед каждым шагом пайплайна — stateful orchestration.

## Проекты

| Параметр | Mclaude | Agent-Memory-Mcp |
|----------|———————|————————————————|
| Слой | orchestration | memory |
| Автор | AnastasiyaW | VitaliySemenov |
| Файл | `docs/05-habr-projects/knowledge/mclaude.md` | `docs/05-habr-projects/memory/agent-memory-mcp.md` |

## Метрики совместимости

| Метрика | Значение |
|---------|---------|
| Тематическое сходство (TF-IDF cosine) | 0.239 |
| Комплементарность слоёв | ✅ высокая |
| Итоговый рейтинг | 0.439 |

## Архитектурный контракт

Точка интеграции: **Card Envelope** (`card_type="mclaude"`, edges к `agent-memory-mcp`).

```json
{
  "card_type": "integration_proposal",
  "state": "raw",
  "projects": ["mclaude", "agent-memory-mcp"],
  "contract": "Card Envelope §3.1",
  "layer_a": "orchestration",
  "layer_b": "memory"
}
```

## Следующие шаги

- [ ] Изучить API Mclaude и Agent-Memory-Mcp
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

<!-- see-also -->

---

**Смотрите также:**
- [proposal-rufler-x-agent-memory-mcp](proposal-rufler-x-agent-memory-mcp.md)
- [proposal-mclaude-x-rufler](proposal-mclaude-x-rufler.md)
- [proposal-01-synthesis-x-yodoca](proposal-01-synthesis-x-yodoca.md)
- [proposal-01-synthesis-x-wikontic](proposal-01-synthesis-x-wikontic.md)


<!-- backlinks -->

---

**Кто ссылается на этот документ (4):**
- [README](README.md)
- [proposal-rufler-x-agent-memory-mcp](proposal-rufler-x-agent-memory-mcp.md)
- [READING_ORDER](../../READING_ORDER.md)
- [READING_TIME](../../READING_TIME.md)

