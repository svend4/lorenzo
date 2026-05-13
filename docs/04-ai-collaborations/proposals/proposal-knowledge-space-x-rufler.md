---
title: "Proposal: Knowledge-Space × Rufler"
date: 2026-05-13
card_id: 433b5d48c942
card_type: proposal
state: raw
tags: [proposal, knowledge-space, rufler, knowledge, orchestration, integration]
projects: [knowledge-space, rufler]
similarity: 0.264
score: 0.464
source: proposal-gen
---

# Proposal: Knowledge-Space × Rufler

<!-- summary -->
> Интеграция knowledge-слоя (Knowledge-Space) и orchestration-слоя (Rufler): Knowledge-Space предоставляет файловую систему знаний с рёбрами, Rufler управляет агентными пайплайнами. Интеграция: Ruf

<!-- tags: proposal, knowledge-space, rufler, knowledge, orchestration, integration -->

## Гипотеза интеграции

Knowledge-Space предоставляет файловую систему знаний с рёбрами, Rufler управляет агентными пайплайнами. Интеграция: Rufler навигирует по Knowledge-Space как по рабочему пространству — граф как рабочая память оркестратора.

## Проекты

| Параметр | Knowledge-Space | Rufler |
|----------|———————————————|——————|
| Слой | knowledge | orchestration |
| Автор | AnastasiyaW | zodigancode |
| Файл | `docs/05-habr-projects/knowledge/knowledge-space.md` | `docs/05-habr-projects/knowledge/rufler.md` |

## Метрики совместимости

| Метрика | Значение |
|---------|---------|
| Тематическое сходство (TF-IDF cosine) | 0.264 |
| Комплементарность слоёв | ✅ высокая |
| Итоговый рейтинг | 0.464 |

## Архитектурный контракт

Точка интеграции: **Card Envelope** (`card_type="knowledge-space"`, edges к `rufler`).

```json
{
  "card_type": "integration_proposal",
  "state": "raw",
  "projects": ["knowledge-space", "rufler"],
  "contract": "Card Envelope §3.1",
  "layer_a": "knowledge",
  "layer_b": "orchestration"
}
```

## Следующие шаги

- [ ] Изучить API Knowledge-Space и Rufler
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
