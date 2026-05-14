---
title: "Proposal: Agentfs × Mclaude"
date: 2026-05-13
card_id: b6c05719426a
card_type: proposal
state: raw
tags: [proposal, agentfs, mclaude, knowledge, orchestration, integration]
projects: [agentfs, mclaude]
similarity: 0.404
score: 0.604
source: proposal-gen
---

# Proposal: Agentfs × Mclaude

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> Интеграция knowledge-слоя (Agentfs) и orchestration-слоя (Mclaude): Agentfs предоставляет файловую систему знаний с рёбрами, Mclaude управляет агентными пайплайнами. Интеграция: Mclaude на

<!-- tags: proposal, agentfs, mclaude, knowledge, orchestration, integration -->

## Гипотеза интеграции

Agentfs предоставляет файловую систему знаний с рёбрами, Mclaude управляет агентными пайплайнами. Интеграция: Mclaude навигирует по Agentfs как по рабочему пространству — граф как рабочая память оркестратора.

## Проекты

| Параметр | Agentfs | Mclaude |
|----------|———————|———————|
| Слой | knowledge | orchestration |
| Автор | kksudo | AnastasiyaW |
| Файл | `docs/05-habr-projects/knowledge/agentfs.md` | `docs/05-habr-projects/knowledge/mclaude.md` |

## Метрики совместимости

| Метрика | Значение |
|---------|---------|
| Тематическое сходство (TF-IDF cosine) | 0.404 |
| Комплементарность слоёв | ✅ высокая |
| Итоговый рейтинг | 0.604 |

## Архитектурный контракт

Точка интеграции: **Card Envelope** (`card_type="agentfs"`, edges к `mclaude`).

```json
{
  "card_type": "integration_proposal",
  "state": "raw",
  "projects": ["agentfs", "mclaude"],
  "contract": "Card Envelope §3.1",
  "layer_a": "knowledge",
  "layer_b": "orchestration"
}
```

## Следующие шаги

- [ ] Изучить API Agentfs и Mclaude
- [ ] Определить точку интеграции (Card Envelope / MCP)
- [ ] Связаться с kksudo и AnastasiyaW
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
- [proposal-knowledge-space-x-mclaude](proposal-knowledge-space-x-mclaude.md)
- [proposal-agentfs-x-rufler](proposal-agentfs-x-rufler.md)
- [proposal-knowledge-space-x-rufler](proposal-knowledge-space-x-rufler.md)
- [proposal-mclaude-x-rufler](proposal-mclaude-x-rufler.md)


<!-- backlinks -->

---

**Кто ссылается на этот документ (6):**
- [README](README.md)
- [proposal-agentfs-x-rufler](proposal-agentfs-x-rufler.md)
- [proposal-knowledge-space-x-mclaude](proposal-knowledge-space-x-mclaude.md)
- [proposal-knowledge-space-x-rufler](proposal-knowledge-space-x-rufler.md)
- [READING_ORDER](../../READING_ORDER.md)
- [READING_TIME](../../READING_TIME.md)

