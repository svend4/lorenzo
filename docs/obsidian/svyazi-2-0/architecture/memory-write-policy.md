---
title: "Memory Write Policy"
tags:
  - memory
  - architecture
  - svyazi-2-0
date: 2026-04-29
---

# Memory Write Policy

<!-- summary -->
> > Источник: `deep-research-report (3).md`, раздел «Интеграционный контракт».
**Проекты:** Yodoca, NGT Memory, agent-memory-mcp

---
<!-- tags: memory, architecture -->




> Источник: `deep-research-report (3).md`, раздел «Интеграционный контракт».

Система должна различать хотя бы четыре режима записи:

- `episode` — для сырых наблюдений
- `fact` — для подтверждённого знания
- `proposal` — для гипотез
- `decay_event` — для понижения значимости

Yodoca уже мыслит память через consolidation + forgetting, NGT Memory — через ассоциативные связи и иерархическую консолидацию, agent-memory-mcp — через typed memory primitives, а Memory OS — через bi‑temporal и provenance‑heavy представление знаний. Из этих линий следует, что «записать что‑то в память» никогда не должно быть одной неразличимой операцией. citeturn21view0turn22view4turn20view16turn39view3

## Минимальные поля

- `write_type` — `episode` | `fact` | `proposal` | `decay_event`
- `promotion_rule` — правило перехода из proposal в fact
- `review_required` — нужен ли явный review перед промоцией
- `decay_policy` — параметры забывания (Ebbinghaus‑decay в стиле Yodoca)

<!-- see-also -->

---

**Смотрите также:**
- [[11-integration-contracts]]
- [[11-интеграционный-контракт-который-стоит-зафиксироват]]
- [[card-envelope]]
- [[review-record]]


<!-- similar-docs -->

---

**Похожие документы:**
- [[card-envelope]] (сходство 0.23)
- [[review-record]] (сходство 0.22)
- [[11-integration-contracts]] (сходство 0.21)

