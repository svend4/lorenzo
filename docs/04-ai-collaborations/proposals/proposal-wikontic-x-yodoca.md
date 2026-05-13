---
title: "Proposal: Wikontic × Yodoca"
date: 2026-05-13
card_id: 3642746e5aa3
card_type: proposal
state: raw
tags: [proposal, wikontic, yodoca, knowledge, memory, integration]
projects: [wikontic, yodoca]
similarity: 0.572
score: 0.872
source: proposal-gen
---

# Proposal: Wikontic × Yodoca

<!-- summary -->
> Интеграция knowledge-слоя (Wikontic) и memory-слоя (Yodoca): Wikontic обеспечивает персистентную память эпизодов, Yodoca хранит структурированный граф знаний. Интеграция: episodes и

<!-- tags: proposal, wikontic, yodoca, knowledge, memory, integration -->

## Гипотеза интеграции

Wikontic обеспечивает персистентную память эпизодов, Yodoca хранит структурированный граф знаний. Интеграция: episodes из Wikontic как узлы графа в Yodoca — контекстно-зависимый retrieval с временно́й семантикой.

## Проекты

| Параметр | Wikontic | Yodoca |
|----------|————————|——————|
| Слой | knowledge | memory |
| Автор | VitalyOborin | VitalyOborin |
| Файл | `docs/05-habr-projects/knowledge/wikontic.md` | `docs/05-habr-projects/memory/yodoca.md` |

## Метрики совместимости

| Метрика | Значение |
|---------|---------|
| Тематическое сходство (TF-IDF cosine) | 0.572 |
| Комплементарность слоёв | ✅ высокая |
| Итоговый рейтинг | 0.872 |

## Архитектурный контракт

Точка интеграции: **Card Envelope** (`card_type="wikontic"`, edges к `yodoca`).

```json
{
  "card_type": "integration_proposal",
  "state": "raw",
  "projects": ["wikontic", "yodoca"],
  "contract": "Card Envelope §3.1",
  "layer_a": "knowledge",
  "layer_b": "memory"
}
```

## Следующие шаги

- [ ] Изучить API Wikontic и Yodoca
- [ ] Определить точку интеграции (Card Envelope / MCP)
- [ ] Связаться с VitalyOborin и VitalyOborin
- [ ] Создать proof-of-concept (≤ 1 неделя)
- [ ] Написать RFC в docs/rfcs/

## Статус ревью

- [ ] Одобрено
- [ ] Отклонено
- [ ] Отложено


---
_Сгенерировано improve_proposal_gen.py: 2026-05-13_
