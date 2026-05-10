---
title: "14. ADR-001: Federation over Merging"
tags:
  - architecture
  - collaboration
  - anthropic-vacancies
date: 2026-05-10
---

# 14. ADR-001: Federation over Merging

<!-- toc-auto -->
## Contents

- [14. ADR-001: Federation over Merging](#14-adr-001-federation-over-merging)
- [Похожие документы](#похожие-документы)
- [Смотрите также](#смотрите-также)
- [Упоминается в](#упоминается-в)
- [Упоминается в](#упоминается-в-1)
- [Связанные документы](#связанные-документы)
- [Связанные документы](#связанные-документы-1)
- [Кто ссылается на этот документ (3)](#кто-ссылается-на-этот-документ-3)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

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

## Похожие документы
- [[94-19-adr-001-federation-over-merging]] (сходство 0.89)
- [[95-20-adr-002-q6-as-first-class-protocol-concept]] (сходство 0.10)


<!-- see-also -->

---

## Использование
```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "14 ADR 001 Federation over Merging"
```

## Смотрите также
- [[94-19-adr-001-federation-over-merging]]
- [[95-20-adr-002-q6-as-first-class-protocol-concept]]
- [[96-21-adr-003-five-onboarding-paths-as-equal-rank]]
- [[06-1-introduction]]

<!-- backlinks-auto -->
## Упоминается в

- [[06-1-introduction|1. Introduction]]
- [[94-19-adr-001-federation-over-merging|19. ADR-001: Federation over Merging]]
- [[95-20-adr-002-q6-as-first-class-protocol-concept|20. ADR-002: Q6 as First-Class Protocol Concept]]
- [[96-21-adr-003-five-onboarding-paths-as-equal-rank|21. ADR-003: Five Onboarding Paths as Equal-Rank]]
- [[83-8-q6-space-normative|8. Q6 Space (Normative)]]
- [[README|Вакансии Anthropic — Анализ по кластерам]]
## Упоминается в

- [[README|Вакансии Anthropic — Анализ по кластерам]]

<!-- related-auto -->
## Связанные документы

- [[94-19-adr-001-federation-over-merging|19. ADR-001: Federation over Merging]] _53%_
- [[95-20-adr-002-q6-as-first-class-protocol-concept|20. ADR-002: Q6 as First-Class Protocol Concept]] _42%_
- [[96-21-adr-003-five-onboarding-paths-as-equal-rank|21. ADR-003: Five Onboarding Paths as Equal-Rank]] _42%_
## Связанные документы

- [[94-19-adr-001-federation-over-merging|19. ADR-001: Federation over Merging]] _37%_
- [[95-20-adr-002-q6-as-first-class-protocol-concept|20. ADR-002: Q6 as First-Class Protocol Concept]] _33%_
- [[96-21-adr-003-five-onboarding-paths-as-equal-rank|21. ADR-003: Five Onboarding Paths as Equal-Rank]] _33%_
- [[06-1-introduction|1. Introduction]] _21%_
- [[68-about|🇬🇧 About]] _21%_
- [[83-8-q6-space-normative|8. Q6 Space (Normative)]] _21%_

<!-- backlinks -->

---

## Кто ссылается на этот документ (3)
- [[94-19-adr-001-federation-over-merging]]
- [[95-20-adr-002-q6-as-first-class-protocol-concept]]
- [[README]]

