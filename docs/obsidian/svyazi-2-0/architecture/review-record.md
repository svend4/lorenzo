---
title: "Review Record"
tags:
  - rag
  - orchestration
  - architecture
  - svyazi-2-0
date: 2026-04-29
---

# Review Record

<!-- summary -->
> > Источник: `deep-research-report (3).md`, раздел «Интеграционный контракт».
**Проекты:** mclaude, AI Factory

---
<!-- tags: rag, orchestration, architecture -->




> Источник: `deep-research-report (3).md`, раздел «Интеграционный контракт».

Не путать machine suggestion с accepted truth. Опирается на mclaude, AI Factory и Sequential‑протокол. citeturn20view2turn20view3turn20view11

## Минимальные поля

- `reviewer_role` — какая роль выносила решение (extractor / reviewer / publisher)
- `decision` — `approved` | `rejected` | `deferred`
- `reason` — текстовое обоснование
- `evidence_refs` — ссылки на Evidence Envelope
- `follow_up` — действие, которое нужно сделать после решения

<!-- see-also -->

---

**Смотрите также:**
- [[integration-spec]]
- [[card-envelope]]
- [[evidence-envelope]]
- [[memory-write-policy]]


<!-- similar-docs -->

---

**Похожие документы:**
- [[integration-spec]] (сходство 0.25)
- [[card-envelope]] (сходство 0.22)
- [[memory-write-policy]] (сходство 0.22)

