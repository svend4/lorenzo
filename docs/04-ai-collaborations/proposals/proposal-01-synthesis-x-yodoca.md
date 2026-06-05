---
title: "Proposal: 01-Synthesis × Yodoca"
date: 2026-05-13
card_id: 94c4c85b2ef1
card_type: proposal
state: normalized
tags: [proposal, 01-synthesis, yodoca, unknown, memory, integration]
projects: [01-synthesis, yodoca]
similarity: 0.570
score: 0.670
source: proposal-gen
---

# Proposal: 01-Synthesis × Yodoca

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> Интеграция unknown-слоя (01-Synthesis) и memory-слоя (Yodoca): 01-Synthesis и Yodoca — взаимодополняющие компоненты Knowledge OS. Интеграция открывает синергию через общий Card Envelo

<!-- tags: proposal, 01-synthesis, yodoca, unknown, memory, integration -->

## Гипотеза интеграции

01-Synthesis и Yodoca — взаимодополняющие компоненты Knowledge OS. Интеграция открывает синергию через общий Card Envelope контракт.

## Проекты

| Параметр | 01-Synthesis | Yodoca |
|----------|————————————|——————|
| Слой | unknown | memory |
| Автор | ? | VitalyOborin |
| Файл | `docs/05-habr-projects/01-synthesis.md` | `docs/05-habr-projects/memory/yodoca.md` |

## Метрики совместимости

| Метрика | Значение |
|---------|---------|
| Тематическое сходство (TF-IDF cosine) | 0.570 |
| Комплементарность слоёв | ✅ высокая |
| Итоговый рейтинг | 0.670 |

## Архитектурный контракт

Точка интеграции: **Card Envelope** (`card_type="01-synthesis"`, edges к `yodoca`).

```json
{
  "card_type": "integration_proposal",
  "state": "raw",
  "projects": ["01-synthesis", "yodoca"],
  "contract": "Card Envelope §3.1",
  "layer_a": "unknown",
  "layer_b": "memory"
}
```

## Следующие шаги

- [ ] Изучить API 01-Synthesis и Yodoca
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

<!-- see-also -->

---

**Смотрите также:**
- [proposal-01-synthesis-x-wikontic](proposal-01-synthesis-x-wikontic.md)
- [proposal-mclaude-x-rufler](proposal-mclaude-x-rufler.md)
- [proposal-wikontic-x-yodoca](proposal-wikontic-x-yodoca.md)
- [proposal-knowledge-space-x-yodoca](proposal-knowledge-space-x-yodoca.md)


<!-- backlinks -->

---

**Кто ссылается на этот документ (7):**
- [README](README.md)
- [proposal-01-synthesis-x-wikontic](proposal-01-synthesis-x-wikontic.md)
- [proposal-mclaude-x-agent-memory-mcp](proposal-mclaude-x-agent-memory-mcp.md)
- [proposal-mclaude-x-rufler](proposal-mclaude-x-rufler.md)
- [proposal-rufler-x-agent-memory-mcp](proposal-rufler-x-agent-memory-mcp.md)
- [READING_ORDER](../../READING_ORDER.md)
- [READING_TIME](../../READING_TIME.md)

