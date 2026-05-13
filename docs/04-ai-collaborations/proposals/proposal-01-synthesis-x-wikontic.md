---
title: "Proposal: 01-Synthesis × Wikontic"
date: 2026-05-13
card_id: 58344ee20467
card_type: proposal
state: raw
tags: [proposal, 01-synthesis, wikontic, unknown, knowledge, integration]
projects: [01-synthesis, wikontic]
similarity: 0.548
score: 0.648
source: proposal-gen
---

# Proposal: 01-Synthesis × Wikontic

<!-- summary -->
> Интеграция unknown-слоя (01-Synthesis) и knowledge-слоя (Wikontic): 01-Synthesis и Wikontic — взаимодополняющие компоненты Knowledge OS. Интеграция открывает синергию через общий Card Enve

<!-- tags: proposal, 01-synthesis, wikontic, unknown, knowledge, integration -->

## Гипотеза интеграции

01-Synthesis и Wikontic — взаимодополняющие компоненты Knowledge OS. Интеграция открывает синергию через общий Card Envelope контракт.

## Проекты

| Параметр | 01-Synthesis | Wikontic |
|----------|————————————|————————|
| Слой | unknown | knowledge |
| Автор | ? | VitalyOborin |
| Файл | `docs/05-habr-projects/01-synthesis.md` | `docs/05-habr-projects/knowledge/wikontic.md` |

## Метрики совместимости

| Метрика | Значение |
|---------|---------|
| Тематическое сходство (TF-IDF cosine) | 0.548 |
| Комплементарность слоёв | ✅ высокая |
| Итоговый рейтинг | 0.648 |

## Архитектурный контракт

Точка интеграции: **Card Envelope** (`card_type="01-synthesis"`, edges к `wikontic`).

```json
{
  "card_type": "integration_proposal",
  "state": "raw",
  "projects": ["01-synthesis", "wikontic"],
  "contract": "Card Envelope §3.1",
  "layer_a": "unknown",
  "layer_b": "knowledge"
}
```

## Следующие шаги

- [ ] Изучить API 01-Synthesis и Wikontic
- [ ] Определить точку интеграции (Card Envelope / MCP)
- [ ] Связаться с ? и VitalyOborin
- [ ] Создать proof-of-concept (≤ 1 неделя)
- [ ] Написать RFC в docs/rfcs/

## Статус ревью

- [ ] Одобрено
- [ ] Отклонено
- [ ] Отложено


---
_Сгенерировано improve_proposal_gen.py: 2026-05-13_
