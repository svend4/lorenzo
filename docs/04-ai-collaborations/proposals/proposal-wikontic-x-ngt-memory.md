---
title: "Proposal: Wikontic × Ngt-Memory"
date: 2026-05-13
card_id: c2f631d59016
card_type: proposal
state: raw
tags: [proposal, wikontic, ngt-memory, knowledge, memory, integration]
projects: [wikontic, ngt-memory]
similarity: 0.216
score: 0.516
source: proposal-gen
---

# Proposal: Wikontic × Ngt-Memory

<!-- summary -->
> Интеграция knowledge-слоя (Wikontic) и memory-слоя (Ngt-Memory): Wikontic обеспечивает персистентную память эпизодов, Ngt-Memory хранит структурированный граф знаний. Интеграция: episod

<!-- tags: proposal, wikontic, ngt-memory, knowledge, memory, integration -->

## Гипотеза интеграции

Wikontic обеспечивает персистентную память эпизодов, Ngt-Memory хранит структурированный граф знаний. Интеграция: episodes из Wikontic как узлы графа в Ngt-Memory — контекстно-зависимый retrieval с временно́й семантикой.

## Проекты

| Параметр | Wikontic | Ngt-Memory |
|----------|————————|——————————|
| Слой | knowledge | memory |
| Автор | VitalyOborin | spbmolot |
| Файл | `docs/05-habr-projects/knowledge/wikontic.md` | `docs/05-habr-projects/memory/ngt-memory.md` |

## Метрики совместимости

| Метрика | Значение |
|---------|---------|
| Тематическое сходство (TF-IDF cosine) | 0.216 |
| Комплементарность слоёв | ✅ высокая |
| Итоговый рейтинг | 0.516 |

## Архитектурный контракт

Точка интеграции: **Card Envelope** (`card_type="wikontic"`, edges к `ngt-memory`).

```json
{
  "card_type": "integration_proposal",
  "state": "raw",
  "projects": ["wikontic", "ngt-memory"],
  "contract": "Card Envelope §3.1",
  "layer_a": "knowledge",
  "layer_b": "memory"
}
```

## Следующие шаги

- [ ] Изучить API Wikontic и Ngt-Memory
- [ ] Определить точку интеграции (Card Envelope / MCP)
- [ ] Связаться с VitalyOborin и spbmolot
- [ ] Создать proof-of-concept (≤ 1 неделя)
- [ ] Написать RFC в docs/rfcs/

## Статус ревью

- [ ] Одобрено
- [ ] Отклонено
- [ ] Отложено


---
_Сгенерировано improve_proposal_gen.py: 2026-05-13_
