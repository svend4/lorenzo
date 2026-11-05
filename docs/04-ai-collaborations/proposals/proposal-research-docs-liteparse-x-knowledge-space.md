---
title: "Proposal: Research-Docs-Liteparse × Knowledge-Space"
date: 2026-05-13
card_id: 6bcb9f660f5b
card_type: proposal
state: approved
tags: [proposal, research-docs-liteparse, knowledge-space, ingestion, knowledge, integration]
projects: [research-docs-liteparse, knowledge-space]
similarity: 0.242
score: 0.492
source: proposal-gen
---

# Proposal: Research-Docs-Liteparse × Knowledge-Space

<!-- toc-auto -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> Интеграция ingestion-слоя (Research-Docs-Liteparse) и knowledge-слоя (Knowledge-Space): Research-Docs-Liteparse хранит знания в виде графа документов, Knowledge-Space парсит и извлекает структуру из сырых ист

<!-- tags: proposal, research-docs-liteparse, knowledge-space, ingestion, knowledge, integration -->

## Гипотеза интеграции

Research-Docs-Liteparse хранит знания в виде графа документов, Knowledge-Space парсит и извлекает структуру из сырых источников. Интеграция: Knowledge-Space → Card Envelope → Research-Docs-Liteparse — автоматическое обогащение графа из внешних источников.

## Проекты

| Параметр | Research-Docs-Liteparse | Knowledge-Space |
|----------|———————————————————————|———————————————|
| Слой | ingestion | knowledge |
| Автор | nlaik | AnastasiyaW |
| Файл | `docs/05-habr-projects/knowledge/research-docs-liteparse.md` | `docs/05-habr-projects/knowledge/knowledge-space.md` |

## Метрики совместимости

| Метрика | Значение |
|---------|---------|
| Тематическое сходство (TF-IDF cosine) | 0.242 |
| Комплементарность слоёв | ✅ высокая |
| Итоговый рейтинг | 0.492 |

## Архитектурный контракт

Точка интеграции: **Card Envelope** (`card_type="research-docs-liteparse"`, edges к `knowledge-space`).

```json
{
  "card_type": "integration_proposal",
  "state": "raw",
  "projects": ["research-docs-liteparse", "knowledge-space"],
  "contract": "Card Envelope §3.1",
  "layer_a": "ingestion",
  "layer_b": "knowledge"
}
```

## Следующие шаги

- [ ] Изучить API Research-Docs-Liteparse и Knowledge-Space
- [ ] Определить точку интеграции (Card Envelope / MCP)
- [ ] Связаться с nlaik и AnastasiyaW
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
- [proposal-research-docs-liteparse-x-agent-memory-mcp](proposal-research-docs-liteparse-x-agent-memory-mcp.md)
- [proposal-knowledge-space-x-ngt-memory](proposal-knowledge-space-x-ngt-memory.md)
- [proposal-knowledge-space-x-agent-memory-mcp](proposal-knowledge-space-x-agent-memory-mcp.md)


<!-- backlinks -->

---

**Кто ссылается на этот документ (5):**
- [README](README.md)
- [proposal-research-docs-liteparse-x-agent-memory-mcp](proposal-research-docs-liteparse-x-agent-memory-mcp.md)
- [proposal-research-docs-liteparse-x-agentfs](proposal-research-docs-liteparse-x-agentfs.md)
- [READING_ORDER](../../READING_ORDER.md)
- [READING_TIME](../../READING_TIME.md)

