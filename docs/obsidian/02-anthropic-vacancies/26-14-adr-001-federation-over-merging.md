---
title: "14. ADR-001: Federation over Merging"
tags:
  - architecture
  - collaboration
  - anthropic-vacancies
date: 2026-04-29
---

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
- [[94-19-adr-001-federation-over-merging]] (сходство 0.89)
- [[95-20-adr-002-q6-as-first-class-protocol-concept]] (сходство 0.10)


<!-- see-also -->

---

**Смотрите также:**
- [[94-19-adr-001-federation-over-merging]]
- [[95-20-adr-002-q6-as-first-class-protocol-concept]]
- [[96-21-adr-003-five-onboarding-paths-as-equal-rank]]
- [[06-1-introduction]]

<!-- backlinks-auto -->
## Упоминается в

- [[README|Вакансии Anthropic — Анализ по кластерам]]

<!-- related-auto -->
## Связанные документы

- [[94-19-adr-001-federation-over-merging|19. ADR-001: Federation over Merging]] _37%_
- [[95-20-adr-002-q6-as-first-class-protocol-concept|20. ADR-002: Q6 as First-Class Protocol Concept]] _33%_
- [[96-21-adr-003-five-onboarding-paths-as-equal-rank|21. ADR-003: Five Onboarding Paths as Equal-Rank]] _33%_
- [[06-1-introduction|1. Introduction]] _21%_
- [[68-about|🇬🇧 About]] _21%_
- [[83-8-q6-space-normative|8. Q6 Space (Normative)]] _21%_
