---
title: "Proposal: Knowledge-Space × Mclaude"
date: 2026-05-13
card_id: c9c4af732973
card_type: proposal
state: raw
tags: [proposal, knowledge-space, mclaude, knowledge, orchestration, integration]
projects: [knowledge-space, mclaude]
similarity: 0.391
score: 0.591
source: proposal-gen
---

# Proposal: Knowledge-Space × Mclaude

<!-- summary -->
> Интеграция knowledge-слоя (Knowledge-Space) и orchestration-слоя (Mclaude): Knowledge-Space предоставляет файловую систему знаний с рёбрами, Mclaude управляет агентными пайплайнами. Интеграция: Mc

<!-- tags: proposal, knowledge-space, mclaude, knowledge, orchestration, integration -->

## Гипотеза интеграции

Knowledge-Space предоставляет файловую систему знаний с рёбрами, Mclaude управляет агентными пайплайнами. Интеграция: Mclaude навигирует по Knowledge-Space как по рабочему пространству — граф как рабочая память оркестратора.

## Проекты

| Параметр | Knowledge-Space | Mclaude |
|----------|———————————————|———————|
| Слой | knowledge | orchestration |
| Автор | AnastasiyaW | AnastasiyaW |
| Файл | `docs/05-habr-projects/knowledge/knowledge-space.md` | `docs/05-habr-projects/knowledge/mclaude.md` |

## Метрики совместимости

| Метрика | Значение |
|---------|---------|
| Тематическое сходство (TF-IDF cosine) | 0.391 |
| Комплементарность слоёв | ✅ высокая |
| Итоговый рейтинг | 0.591 |

## Архитектурный контракт

Точка интеграции: **Card Envelope** (`card_type="knowledge-space"`, edges к `mclaude`).

```json
{
  "card_type": "integration_proposal",
  "state": "raw",
  "projects": ["knowledge-space", "mclaude"],
  "contract": "Card Envelope §3.1",
  "layer_a": "knowledge",
  "layer_b": "orchestration"
}
```

## Следующие шаги

- [ ] Изучить API Knowledge-Space и Mclaude
- [ ] Определить точку интеграции (Card Envelope / MCP)
- [ ] Связаться с AnastasiyaW и AnastasiyaW
- [ ] Создать proof-of-concept (≤ 1 неделя)
- [ ] Написать RFC в docs/rfcs/

## Статус ревью

- [ ] Одобрено
- [ ] Отклонено
- [ ] Отложено


---
_Сгенерировано improve_proposal_gen.py: 2026-05-13_
