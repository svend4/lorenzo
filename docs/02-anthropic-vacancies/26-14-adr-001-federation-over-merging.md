# 14. ADR-001: Federation over Merging

<!-- summary -->
> **Context:** При построении системы knowledge management встаёт

---
<!-- tags: architecture, collaboration -->




## 14. ADR-001: Federation over Merging

**Status:** Accepted

**Context:** При построении системы knowledge management встаёт 
выбор: заставить все данные мигрировать в единую схему (merge), 
либо сохранить разные native-форматы и переводить по необходимости 
(federation).

**Decision:** Выбрана federation.

**Consequences:**

**Positive:**
- Low barrier to entry: существующие Repos подключаются без 
  рефакторинга
- Authorship preserved: каждый автор работает в своей модели
- Multi-angle views: один концепт может существовать в трёх Repos 
  с тремя разными углами одновременно

**Negative:**
- Cross-repo queries дороже: требуется вызов всех адаптеров
- Consensus нетривиален: string matching — аппроксимация, не 
  formal mapping
- Bridges — текстовые описания, не machine-executable

**Alternatives rejected:**
- Unified RDF/OWL ontology: слишком высокий barrier to entry
- Centralized database: нарушает принцип local autonomy
- Schema-less dump: теряется семантика angles

---

<!-- similar-docs -->

---

**Похожие документы:**
- [94-19-adr-001-federation-over-merging](docs/02-anthropic-vacancies/94-19-adr-001-federation-over-merging.md) (сходство 0.89)
- [95-20-adr-002-q6-as-first-class-protocol-concept](docs/02-anthropic-vacancies/95-20-adr-002-q6-as-first-class-protocol-concept.md) (сходство 0.10)


<!-- see-also -->

---

**Смотрите также:**
- [94-19-adr-001-federation-over-merging](docs/02-anthropic-vacancies/94-19-adr-001-federation-over-merging.md)
- [95-20-adr-002-q6-as-first-class-protocol-concept](docs/02-anthropic-vacancies/95-20-adr-002-q6-as-first-class-protocol-concept.md)
- [96-21-adr-003-five-onboarding-paths-as-equal-rank](docs/02-anthropic-vacancies/96-21-adr-003-five-onboarding-paths-as-equal-rank.md)
- [06-1-introduction](docs/02-anthropic-vacancies/06-1-introduction.md)

<!-- backlinks-auto -->
## Упоминается в

- [Вакансии Anthropic — Анализ по кластерам](docs/02-anthropic-vacancies/README.md)

<!-- related-auto -->
## Связанные документы

- [19. ADR-001: Federation over Merging](docs/02-anthropic-vacancies/94-19-adr-001-federation-over-merging.md) _37%_
- [20. ADR-002: Q6 as First-Class Protocol Concept](docs/02-anthropic-vacancies/95-20-adr-002-q6-as-first-class-protocol-concept.md) _33%_
- [21. ADR-003: Five Onboarding Paths as Equal-Rank](docs/02-anthropic-vacancies/96-21-adr-003-five-onboarding-paths-as-equal-rank.md) _33%_
- [1. Introduction](docs/02-anthropic-vacancies/06-1-introduction.md) _21%_
- [🇬🇧 About](docs/02-anthropic-vacancies/68-about.md) _21%_
- [8. Q6 Space (Normative)](docs/02-anthropic-vacancies/83-8-q6-space-normative.md) _21%_
