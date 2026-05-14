---
title: "Proposal: Agentfs × Yodoca"
date: 2026-05-13
card_id: 0bd2cbea1dcc
card_type: proposal
state: raw
tags: [proposal, agentfs, yodoca, knowledge, memory, integration]
projects: [agentfs, yodoca]
similarity: 0.116
score: 0.416
source: proposal-gen
---

# Proposal: Agentfs × Yodoca

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> Интеграция knowledge-слоя (Agentfs) и memory-слоя (Yodoca): Agentfs обеспечивает персистентную память эпизодов, Yodoca хранит структурированный граф знаний. Интеграция: episodes из

<!-- tags: proposal, agentfs, yodoca, knowledge, memory, integration -->

## Гипотеза интеграции

Agentfs обеспечивает персистентную память эпизодов, Yodoca хранит структурированный граф знаний. Интеграция: episodes из Agentfs как узлы графа в Yodoca — контекстно-зависимый retrieval с временно́й семантикой.

## Проекты

| Параметр | Agentfs | Yodoca |
|----------|———————|——————|
| Слой | knowledge | memory |
| Автор | kksudo | VitalyOborin |
| Файл | `docs/05-habr-projects/knowledge/agentfs.md` | `docs/05-habr-projects/memory/yodoca.md` |

## Метрики совместимости

| Метрика | Значение |
|---------|---------|
| Тематическое сходство (TF-IDF cosine) | 0.116 |
| Комплементарность слоёв | ✅ высокая |
| Итоговый рейтинг | 0.416 |

## Архитектурный контракт

Точка интеграции: **Card Envelope** (`card_type="agentfs"`, edges к `yodoca`).

```json
{
  "card_type": "integration_proposal",
  "state": "raw",
  "projects": ["agentfs", "yodoca"],
  "contract": "Card Envelope §3.1",
  "layer_a": "knowledge",
  "layer_b": "memory"
}
```

## Следующие шаги

- [ ] Изучить API Agentfs и Yodoca
- [ ] Определить точку интеграции (Card Envelope / MCP)
- [ ] Связаться с kksudo и VitalyOborin
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
- [proposal-knowledge-space-x-yodoca](proposal-knowledge-space-x-yodoca.md)
- [proposal-wikontic-x-agent-memory-mcp](proposal-wikontic-x-agent-memory-mcp.md)


<!-- backlinks -->

---

**Кто ссылается на этот документ (7):**
- [README](README.md)
- [proposal-agentfs-x-agent-memory-mcp](proposal-agentfs-x-agent-memory-mcp.md)
- [proposal-agentfs-x-memnet](proposal-agentfs-x-memnet.md)
- [proposal-knowledge-space-x-yodoca](proposal-knowledge-space-x-yodoca.md)
- [proposal-wikontic-x-yodoca](proposal-wikontic-x-yodoca.md)
- [READING_ORDER](../../READING_ORDER.md)
- [READING_TIME](../../READING_TIME.md)

