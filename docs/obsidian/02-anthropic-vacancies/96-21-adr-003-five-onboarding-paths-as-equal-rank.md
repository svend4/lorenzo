---
title: "21. ADR-003: Five Onboarding Paths as Equal-Rank"
tags:
  - anthropic
  - anthropic-vacancies
date: 2026-04-29
---

# 21. ADR-003: Five Onboarding Paths as Equal-Rank

<!-- summary -->
> **Status**: Accepted (new in v1.1)

---
<!-- tags: anthropic -->




## 21. ADR-003: Five Onboarding Paths as Equal-Rank

**Status**: Accepted (new in v1.1)

**Context**: В v1.0 была одна "основная" стратегия подключения 
(manual adapter). В процессе развития reference implementation 
появились 4 дополнительных пути (B–E). Возникал вопрос: какой 
канонический?

**Decision**: Все 5 путей — равнорангованные. Выбор делается по 
контексту (раздел 12.6), не по иерархии.

**Consequences**:

**Positive**:
- Flexibility для разных use cases
- Self-declaring repos (Path C) enables federation без центральной 
  координации
- Automated paths (D, E) scale для fleet-federation

**Negative**:
- Больше документации
- Users могут путаться, какой путь выбрать (mitigated via раздел 
  12.6 guidance)

---

<!-- similar-docs -->

---

**Похожие документы:**
- [[94-19-adr-001-federation-over-merging]] (сходство 0.11)


<!-- see-also -->

---

**Смотрите также:**
- [[94-19-adr-001-federation-over-merging]]
- [[95-20-adr-002-q6-as-first-class-protocol-concept]]
- [[26-14-adr-001-federation-over-merging]]
- [[321-appendix-a-decision-tree-for-ingit-adopters]]

<!-- backlinks-auto -->
## Упоминается в

- [[README|Вакансии Anthropic — Анализ по кластерам]]

<!-- related-auto -->
## Связанные документы

- [[94-19-adr-001-federation-over-merging|19. ADR-001: Federation over Merging]] _60%_
- [[95-20-adr-002-q6-as-first-class-protocol-concept|20. ADR-002: Q6 as First-Class Protocol Concept]] _42%_
- [[26-14-adr-001-federation-over-merging|14. ADR-001: Federation over Merging]] _33%_
- [[83-8-q6-space-normative|8. Q6 Space (Normative)]] _21%_
- [[06-1-introduction|1. Introduction]] _17%_
- [[104-appendix-c-references|Appendix C: References]] _17%_
