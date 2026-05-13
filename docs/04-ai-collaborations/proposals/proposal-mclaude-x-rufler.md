---
title: "Proposal: Mclaude × Rufler"
date: 2026-05-13
card_id: 4c8b591921ba
card_type: proposal
state: raw
tags: [proposal, mclaude, rufler, orchestration, orchestration, integration]
projects: [mclaude, rufler]
similarity: 0.415
score: 0.415
source: proposal-gen
---

# Proposal: Mclaude × Rufler

<!-- summary -->
> Интеграция orchestration-слоя (Mclaude) и orchestration-слоя (Rufler): Mclaude и Rufler — взаимодополняющие компоненты Knowledge OS. Интеграция открывает синергию через общий Card Envelope ко

<!-- tags: proposal, mclaude, rufler, orchestration, orchestration, integration -->

## Гипотеза интеграции

Mclaude и Rufler — взаимодополняющие компоненты Knowledge OS. Интеграция открывает синергию через общий Card Envelope контракт.

## Проекты

| Параметр | Mclaude | Rufler |
|----------|———————|——————|
| Слой | orchestration | orchestration |
| Автор | AnastasiyaW | zodigancode |
| Файл | `docs/05-habr-projects/knowledge/mclaude.md` | `docs/05-habr-projects/knowledge/rufler.md` |

## Метрики совместимости

| Метрика | Значение |
|---------|---------|
| Тематическое сходство (TF-IDF cosine) | 0.415 |
| Комплементарность слоёв | ⚠ одинаковый слой |
| Итоговый рейтинг | 0.415 |

## Архитектурный контракт

Точка интеграции: **Card Envelope** (`card_type="mclaude"`, edges к `rufler`).

```json
{
  "card_type": "integration_proposal",
  "state": "raw",
  "projects": ["mclaude", "rufler"],
  "contract": "Card Envelope §3.1",
  "layer_a": "orchestration",
  "layer_b": "orchestration"
}
```

## Следующие шаги

- [ ] Изучить API Mclaude и Rufler
- [ ] Определить точку интеграции (Card Envelope / MCP)
- [ ] Связаться с AnastasiyaW и zodigancode
- [ ] Создать proof-of-concept (≤ 1 неделя)
- [ ] Написать RFC в docs/rfcs/

## Статус ревью

- [ ] Одобрено
- [ ] Отклонено
- [ ] Отложено


---
_Сгенерировано improve_proposal_gen.py: 2026-05-13_
