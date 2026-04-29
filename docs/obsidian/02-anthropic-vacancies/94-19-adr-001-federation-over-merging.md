---
title: "19. ADR-001: Federation over Merging"
tags:
  - architecture
  - collaboration
  - anthropic-vacancies
date: 2026-04-29
---

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
- [[26-14-adr-001-federation-over-merging]] (сходство 0.89)
- [[96-21-adr-003-five-onboarding-paths-as-equal-rank]] (сходство 0.11)


<!-- see-also -->

---

**Смотрите также:**
- [[26-14-adr-001-federation-over-merging]]
- [[96-21-adr-003-five-onboarding-paths-as-equal-rank]]
- [[95-20-adr-002-q6-as-first-class-protocol-concept]]
- [[76-1-introduction]]

<!-- backlinks-auto -->
## Упоминается в

- [[06-1-introduction|1. Introduction]]
- [[26-14-adr-001-federation-over-merging|14. ADR-001: Federation over Merging]]
- [[95-20-adr-002-q6-as-first-class-protocol-concept|20. ADR-002: Q6 as First-Class Protocol Concept]]
- [[96-21-adr-003-five-onboarding-paths-as-equal-rank|21. ADR-003: Five Onboarding Paths as Equal-Rank]]
- [[README|Вакансии Anthropic — Анализ по кластерам]]
## Упоминается в

- [[README|Вакансии Anthropic — Анализ по кластерам]]

<!-- related-auto -->
## Связанные документы

- [[96-21-adr-003-five-onboarding-paths-as-equal-rank|21. ADR-003: Five Onboarding Paths as Equal-Rank]] _60%_
- [[26-14-adr-001-federation-over-merging|14. ADR-001: Federation over Merging]] _53%_
- [[95-20-adr-002-q6-as-first-class-protocol-concept|20. ADR-002: Q6 as First-Class Protocol Concept]] _53%_
## Связанные документы

- [[96-21-adr-003-five-onboarding-paths-as-equal-rank|21. ADR-003: Five Onboarding Paths as Equal-Rank]] _60%_
- [[26-14-adr-001-federation-over-merging|14. ADR-001: Federation over Merging]] _37%_
- [[95-20-adr-002-q6-as-first-class-protocol-concept|20. ADR-002: Q6 as First-Class Protocol Concept]] _33%_
- [[06-1-introduction|1. Introduction]] _17%_
