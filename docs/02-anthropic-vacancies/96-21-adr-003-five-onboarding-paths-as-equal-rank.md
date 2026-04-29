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
- [94-19-adr-001-federation-over-merging](docs/02-anthropic-vacancies/94-19-adr-001-federation-over-merging.md) (сходство 0.11)


<!-- see-also -->

---

**Смотрите также:**
- [94-19-adr-001-federation-over-merging](docs/02-anthropic-vacancies/94-19-adr-001-federation-over-merging.md)
- [95-20-adr-002-q6-as-first-class-protocol-concept](docs/02-anthropic-vacancies/95-20-adr-002-q6-as-first-class-protocol-concept.md)
- [26-14-adr-001-federation-over-merging](docs/02-anthropic-vacancies/26-14-adr-001-federation-over-merging.md)
- [321-appendix-a-decision-tree-for-ingit-adopters](docs/02-anthropic-vacancies/321-appendix-a-decision-tree-for-ingit-adopters.md)

<!-- backlinks-auto -->
## Упоминается в

- [Вакансии Anthropic — Анализ по кластерам](docs/02-anthropic-vacancies/README.md)

<!-- related-auto -->
## Связанные документы

- [19. ADR-001: Federation over Merging](docs/02-anthropic-vacancies/94-19-adr-001-federation-over-merging.md) _60%_
- [20. ADR-002: Q6 as First-Class Protocol Concept](docs/02-anthropic-vacancies/95-20-adr-002-q6-as-first-class-protocol-concept.md) _42%_
- [14. ADR-001: Federation over Merging](docs/02-anthropic-vacancies/26-14-adr-001-federation-over-merging.md) _33%_
- [8. Q6 Space (Normative)](docs/02-anthropic-vacancies/83-8-q6-space-normative.md) _21%_
- [1. Introduction](docs/02-anthropic-vacancies/06-1-introduction.md) _17%_
- [Appendix C: References](docs/02-anthropic-vacancies/104-appendix-c-references.md) _17%_
