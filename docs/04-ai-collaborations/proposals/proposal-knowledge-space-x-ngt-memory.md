---
title: "Proposal: Knowledge-Space × Ngt-Memory"
date: 2026-05-13
card_id: d3e98e696a25
card_type: proposal
state: raw
tags: [proposal, knowledge-space, ngt-memory, knowledge, memory, integration]
projects: [knowledge-space, ngt-memory]
similarity: 0.135
score: 0.435
source: proposal-gen
---

# Proposal: Knowledge-Space × Ngt-Memory

<!-- summary -->
> Интеграция knowledge-слоя (Knowledge-Space) и memory-слоя (Ngt-Memory): Knowledge-Space обеспечивает персистентную память эпизодов, Ngt-Memory хранит структурированный граф знаний. Интеграция:

<!-- tags: proposal, knowledge-space, ngt-memory, knowledge, memory, integration -->

## Гипотеза интеграции

Knowledge-Space обеспечивает персистентную память эпизодов, Ngt-Memory хранит структурированный граф знаний. Интеграция: episodes из Knowledge-Space как узлы графа в Ngt-Memory — контекстно-зависимый retrieval с временно́й семантикой.

## Проекты

| Параметр | Knowledge-Space | Ngt-Memory |
|----------|———————————————|——————————|
| Слой | knowledge | memory |
| Автор | AnastasiyaW | spbmolot |
| Файл | `docs/05-habr-projects/knowledge/knowledge-space.md` | `docs/05-habr-projects/memory/ngt-memory.md` |

## Метрики совместимости

| Метрика | Значение |
|---------|---------|
| Тематическое сходство (TF-IDF cosine) | 0.135 |
| Комплементарность слоёв | ✅ высокая |
| Итоговый рейтинг | 0.435 |

## Архитектурный контракт

Точка интеграции: **Card Envelope** (`card_type="knowledge-space"`, edges к `ngt-memory`).

```json
{
  "card_type": "integration_proposal",
  "state": "raw",
  "projects": ["knowledge-space", "ngt-memory"],
  "contract": "Card Envelope §3.1",
  "layer_a": "knowledge",
  "layer_b": "memory"
}
```

## Следующие шаги

- [ ] Изучить API Knowledge-Space и Ngt-Memory
- [ ] Определить точку интеграции (Card Envelope / MCP)
- [ ] Связаться с AnastasiyaW и spbmolot
- [ ] Создать proof-of-concept (≤ 1 неделя)
- [ ] Написать RFC в docs/rfcs/

## Статус ревью

- [ ] Одобрено
- [ ] Отклонено
- [ ] Отложено


---
_Сгенерировано improve_proposal_gen.py: 2026-05-13_
