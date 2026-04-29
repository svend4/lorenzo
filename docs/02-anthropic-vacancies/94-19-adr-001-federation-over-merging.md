# 19. ADR-001: Federation over Merging

<!-- summary -->
> **Status**: Accepted (since v1.0, reaffirmed in v1.1)

---
<!-- tags: architecture, collaboration -->




## 19. ADR-001: Federation over Merging

**Status**: Accepted (since v1.0, reaffirmed in v1.1)

**Context**: При построении системы knowledge management встаёт 
выбор: заставить все данные мигрировать в единую схему (merge), 
либо сохранить разные native-форматы и переводить по необходимости 
(federation).

**Decision**: Выбрана federation.

**Consequences**:

**Positive**:
- Low barrier to entry: существующие Repos подключаются без 
  рефакторинга
- Authorship preserved: каждый автор работает в своей модели
- Multi-angle views: один концепт может существовать в трёх Repos 
  с тремя разными углами одновременно
- Five onboarding paths: гибкость от manual до fully automated

**Negative**:
- Cross-repo queries дороже: требуется вызов всех адаптеров
- Consensus нетривиален: string matching — аппроксимация, не 
  formal mapping
- Bridges — текстовые описания, не machine-executable (открытый 
  вопрос для v2.0)

**Alternatives rejected**:
- Unified RDF/OWL ontology: слишком высокий barrier
- Centralized database: нарушает local autonomy
- Schema-less dump: теряется семантика angles

---

<!-- similar-docs -->

---

**Похожие документы:**
- [26-14-adr-001-federation-over-merging](docs/02-anthropic-vacancies/26-14-adr-001-federation-over-merging.md) (сходство 0.89)
- [96-21-adr-003-five-onboarding-paths-as-equal-rank](docs/02-anthropic-vacancies/96-21-adr-003-five-onboarding-paths-as-equal-rank.md) (сходство 0.11)


<!-- see-also -->

---

**Смотрите также:**
- [26-14-adr-001-federation-over-merging](docs/02-anthropic-vacancies/26-14-adr-001-federation-over-merging.md)
- [96-21-adr-003-five-onboarding-paths-as-equal-rank](docs/02-anthropic-vacancies/96-21-adr-003-five-onboarding-paths-as-equal-rank.md)
- [95-20-adr-002-q6-as-first-class-protocol-concept](docs/02-anthropic-vacancies/95-20-adr-002-q6-as-first-class-protocol-concept.md)
- [76-1-introduction](docs/02-anthropic-vacancies/76-1-introduction.md)

<!-- backlinks-auto -->
## Упоминается в

- [Вакансии Anthropic — Анализ по кластерам](docs/02-anthropic-vacancies/README.md)

<!-- related-auto -->
## Связанные документы

- [21. ADR-003: Five Onboarding Paths as Equal-Rank](docs/02-anthropic-vacancies/96-21-adr-003-five-onboarding-paths-as-equal-rank.md) _60%_
- [14. ADR-001: Federation over Merging](docs/02-anthropic-vacancies/26-14-adr-001-federation-over-merging.md) _37%_
- [20. ADR-002: Q6 as First-Class Protocol Concept](docs/02-anthropic-vacancies/95-20-adr-002-q6-as-first-class-protocol-concept.md) _33%_
- [1. Introduction](docs/02-anthropic-vacancies/06-1-introduction.md) _17%_
