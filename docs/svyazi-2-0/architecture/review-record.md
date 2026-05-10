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
- [integration-spec](integration-spec.md)
- [card-envelope](card-envelope.md)
- [evidence-envelope](evidence-envelope.md)
- [memory-write-policy](memory-write-policy.md)


<!-- backlinks -->

---

**Кто ссылается на этот документ (3):**
- [concepts](../../glossary/concepts.md)
- [README](README.md)
- [integration-spec](integration-spec.md)

