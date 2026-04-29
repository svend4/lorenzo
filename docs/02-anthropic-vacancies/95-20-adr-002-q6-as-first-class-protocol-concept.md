# 20. ADR-002: Q6 as First-Class Protocol Concept

<!-- summary -->
> **Status**: Accepted (new in v1.1)

---
<!-- tags: anthropic -->




## 20. ADR-002: Q6 as First-Class Protocol Concept

**Status**: Accepted (new in v1.1)

**Context**: В v1.0 Q6-пространство существовало как implementation 
detail reference portal (pro2 → hexagrams). При росте экосистемы 
стало ясно, что Q6 работает как универсальная система координат 
для всех Repos, не только pro2.

**Decision**: В v1.1 Q6 повышается до нормативного концепта 
протокола. Level 2+ адаптеры MUST обеспечивать Q6-координаты. 
Каждый format MUST документировать свой Q6 mapping rule.

**Consequences**:

**Positive**:
- Унифицированная система координат для всей экосистемы
- Возможность cross-format similarity queries через Hamming distance
- Визуализации (Q6 map, heatmaps) работают universally
- CA-class mapping даёт rich symbolic interpretation

**Negative**:
- Adapters Level 2+ вынуждены определять Q6 mapping
- 64 вершин может быть мало для некоторых форматов (но достаточно 
  для большинства)
- v2.0 может понадобиться Q8 или Q12 для больших экосистем

---

<!-- similar-docs -->

---

**Похожие документы:**
- [83-8-q6-space-normative](docs/02-anthropic-vacancies/83-8-q6-space-normative.md) (сходство 0.11)
- [26-14-adr-001-federation-over-merging](docs/02-anthropic-vacancies/26-14-adr-001-federation-over-merging.md) (сходство 0.10)


<!-- see-also -->

---

**Смотрите также:**
- [26-14-adr-001-federation-over-merging](docs/02-anthropic-vacancies/26-14-adr-001-federation-over-merging.md)
- [83-8-q6-space-normative](docs/02-anthropic-vacancies/83-8-q6-space-normative.md)
- [96-21-adr-003-five-onboarding-paths-as-equal-rank](docs/02-anthropic-vacancies/96-21-adr-003-five-onboarding-paths-as-equal-rank.md)
- [94-19-adr-001-federation-over-merging](docs/02-anthropic-vacancies/94-19-adr-001-federation-over-merging.md)

<!-- backlinks-auto -->
## Упоминается в

- [Вакансии Anthropic — Анализ по кластерам](docs/02-anthropic-vacancies/README.md)

<!-- related-auto -->
## Связанные документы

- [21. ADR-003: Five Onboarding Paths as Equal-Rank](docs/02-anthropic-vacancies/96-21-adr-003-five-onboarding-paths-as-equal-rank.md) _42%_
- [8. Q6 Space (Normative)](docs/02-anthropic-vacancies/83-8-q6-space-normative.md) _37%_
- [14. ADR-001: Federation over Merging](docs/02-anthropic-vacancies/26-14-adr-001-federation-over-merging.md) _33%_
- [19. ADR-001: Federation over Merging](docs/02-anthropic-vacancies/94-19-adr-001-federation-over-merging.md) _33%_
- [1. Introduction](docs/02-anthropic-vacancies/06-1-introduction.md) _17%_
- [Appendix C: References](docs/02-anthropic-vacancies/104-appendix-c-references.md) _17%_
- [Bridges](docs/02-anthropic-vacancies/40-bridges.md) _17%_
- [Bridges](docs/02-anthropic-vacancies/60-bridges.md) _17%_
