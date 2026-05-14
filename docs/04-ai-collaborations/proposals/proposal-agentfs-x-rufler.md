---
title: "Proposal: Agentfs × Rufler"
date: 2026-05-13
card_id: 9ff3ebab40d4
card_type: proposal
state: raw
tags: [proposal, agentfs, rufler, knowledge, orchestration, integration]
projects: [agentfs, rufler]
similarity: 0.272
score: 0.472
source: proposal-gen
---

# Proposal: Agentfs × Rufler

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> Интеграция knowledge-слоя (Agentfs) и orchestration-слоя (Rufler): Agentfs предоставляет файловую систему знаний с рёбрами, Rufler управляет агентными пайплайнами. Интеграция: Rufler нави

<!-- tags: proposal, agentfs, rufler, knowledge, orchestration, integration -->

## Гипотеза интеграции

Agentfs предоставляет файловую систему знаний с рёбрами, Rufler управляет агентными пайплайнами. Интеграция: Rufler навигирует по Agentfs как по рабочему пространству — граф как рабочая память оркестратора.

## Проекты

| Параметр | Agentfs | Rufler |
|----------|———————|——————|
| Слой | knowledge | orchestration |
| Автор | kksudo | zodigancode |
| Файл | `docs/05-habr-projects/knowledge/agentfs.md` | `docs/05-habr-projects/knowledge/rufler.md` |

## Метрики совместимости

| Метрика | Значение |
|---------|---------|
| Тематическое сходство (TF-IDF cosine) | 0.272 |
| Комплементарность слоёв | ✅ высокая |
| Итоговый рейтинг | 0.472 |

## Архитектурный контракт

Точка интеграции: **Card Envelope** (`card_type="agentfs"`, edges к `rufler`).

```json
{
  "card_type": "integration_proposal",
  "state": "raw",
  "projects": ["agentfs", "rufler"],
  "contract": "Card Envelope §3.1",
  "layer_a": "knowledge",
  "layer_b": "orchestration"
}
```

## Следующие шаги

- [ ] Изучить API Agentfs и Rufler
- [ ] Определить точку интеграции (Card Envelope / MCP)
- [ ] Связаться с kksudo и zodigancode
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
- [proposal-agentfs-x-mclaude](proposal-agentfs-x-mclaude.md)
- [proposal-knowledge-space-x-rufler](proposal-knowledge-space-x-rufler.md)
- [proposal-knowledge-space-x-mclaude](proposal-knowledge-space-x-mclaude.md)
- [proposal-mclaude-x-rufler](proposal-mclaude-x-rufler.md)


<!-- backlinks -->

---

**Кто ссылается на этот документ (6):**
- [README](README.md)
- [proposal-agentfs-x-mclaude](proposal-agentfs-x-mclaude.md)
- [proposal-knowledge-space-x-mclaude](proposal-knowledge-space-x-mclaude.md)
- [proposal-knowledge-space-x-rufler](proposal-knowledge-space-x-rufler.md)
- [READING_ORDER](../../READING_ORDER.md)
- [READING_TIME](../../READING_TIME.md)

