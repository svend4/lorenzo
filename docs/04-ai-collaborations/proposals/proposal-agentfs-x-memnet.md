---
title: "Proposal: Agentfs × Memnet"
date: 2026-05-13
card_id: 77f2ffc996e6
card_type: proposal
state: normalized
tags: [proposal, agentfs, memnet, knowledge, memory, integration]
projects: [agentfs, memnet]
similarity: 0.100
score: 0.400
source: proposal-gen
---

# Proposal: Agentfs × Memnet

> [!TIP]
> Документ содержит практические рекомендации и лучшие практики.

<!-- alert-added -->

<!-- summary -->
> Интеграция knowledge-слоя (Agentfs) и memory-слоя (Memnet): Agentfs обеспечивает персистентную память эпизодов, Memnet хранит структурированный граф знаний. Интеграция: episodes из

<!-- tags: proposal, agentfs, memnet, knowledge, memory, integration -->

## Гипотеза интеграции

Agentfs обеспечивает персистентную память эпизодов, Memnet хранит структурированный граф знаний. Интеграция: episodes из Agentfs как узлы графа в Memnet — контекстно-зависимый retrieval с временно́й семантикой.

## Проекты

| Параметр | Agentfs | Memnet |
|----------|———————|——————|
| Слой | knowledge | memory |
| Автор | kksudo | Antipozitive |
| Файл | `docs/05-habr-projects/knowledge/agentfs.md` | `docs/05-habr-projects/memory/memnet.md` |

## Метрики совместимости

| Метрика | Значение |
|---------|---------|
| Тематическое сходство (TF-IDF cosine) | 0.100 |
| Комплементарность слоёв | ✅ высокая |
| Итоговый рейтинг | 0.400 |

## Архитектурный контракт

Точка интеграции: **Card Envelope** (`card_type="agentfs"`, edges к `memnet`).

```json
{
  "card_type": "integration_proposal",
  "state": "raw",
  "projects": ["agentfs", "memnet"],
  "contract": "Card Envelope §3.1",
  "layer_a": "knowledge",
  "layer_b": "memory"
}
```

## Следующие шаги

- [ ] Изучить API Agentfs и Memnet
- [ ] Определить точку интеграции (Card Envelope / MCP)
- [ ] Связаться с kksudo и Antipozitive
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
- [proposal-wikontic-x-memnet](proposal-wikontic-x-memnet.md)
- [proposal-agentfs-x-agent-memory-mcp](proposal-agentfs-x-agent-memory-mcp.md)
- [proposal-agentfs-x-yodoca](proposal-agentfs-x-yodoca.md)
- [proposal-knowledge-space-x-ngt-memory](proposal-knowledge-space-x-ngt-memory.md)


<!-- backlinks -->

---

**Кто ссылается на этот документ (4):**
- [README](README.md)
- [proposal-wikontic-x-memnet](proposal-wikontic-x-memnet.md)
- [READING_ORDER](../../READING_ORDER.md)
- [READING_TIME](../../READING_TIME.md)

