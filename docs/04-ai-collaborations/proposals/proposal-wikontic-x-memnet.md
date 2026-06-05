---
title: "Proposal: Wikontic × Memnet"
date: 2026-05-13
card_id: d3d98a01c916
card_type: proposal
state: normalized
tags: [proposal, wikontic, memnet, knowledge, memory, integration]
projects: [wikontic, memnet]
similarity: 0.220
score: 0.520
source: proposal-gen
---

# Proposal: Wikontic × Memnet

> [!TIP]
> Документ содержит практические рекомендации и лучшие практики.

<!-- alert-added -->

<!-- summary -->
> Интеграция knowledge-слоя (Wikontic) и memory-слоя (Memnet): Wikontic обеспечивает персистентную память эпизодов, Memnet хранит структурированный граф знаний. Интеграция: episodes и

<!-- tags: proposal, wikontic, memnet, knowledge, memory, integration -->

## Гипотеза интеграции

Wikontic обеспечивает персистентную память эпизодов, Memnet хранит структурированный граф знаний. Интеграция: episodes из Wikontic как узлы графа в Memnet — контекстно-зависимый retrieval с временно́й семантикой.

## Проекты

| Параметр | Wikontic | Memnet |
|----------|————————|——————|
| Слой | knowledge | memory |
| Автор | VitalyOborin | Antipozitive |
| Файл | `docs/05-habr-projects/knowledge/wikontic.md` | `docs/05-habr-projects/memory/memnet.md` |

## Метрики совместимости

| Метрика | Значение |
|---------|---------|
| Тематическое сходство (TF-IDF cosine) | 0.220 |
| Комплементарность слоёв | ✅ высокая |
| Итоговый рейтинг | 0.520 |

## Архитектурный контракт

Точка интеграции: **Card Envelope** (`card_type="wikontic"`, edges к `memnet`).

```json
{
  "card_type": "integration_proposal",
  "state": "raw",
  "projects": ["wikontic", "memnet"],
  "contract": "Card Envelope §3.1",
  "layer_a": "knowledge",
  "layer_b": "memory"
}
```

## Следующие шаги

- [ ] Изучить API Wikontic и Memnet
- [ ] Определить точку интеграции (Card Envelope / MCP)
- [ ] Связаться с VitalyOborin и Antipozitive
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
- [proposal-agentfs-x-memnet](proposal-agentfs-x-memnet.md)
- [proposal-wikontic-x-yodoca](proposal-wikontic-x-yodoca.md)
- [proposal-wikontic-x-agent-memory-mcp](proposal-wikontic-x-agent-memory-mcp.md)
- [proposal-wikontic-x-ngt-memory](proposal-wikontic-x-ngt-memory.md)


<!-- backlinks -->

---

**Кто ссылается на этот документ (4):**
- [README](README.md)
- [proposal-agentfs-x-memnet](proposal-agentfs-x-memnet.md)
- [READING_ORDER](../../READING_ORDER.md)
- [READING_TIME](../../READING_TIME.md)

