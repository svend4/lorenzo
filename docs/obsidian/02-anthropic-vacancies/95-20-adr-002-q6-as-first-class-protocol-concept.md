---
title: "20. ADR-002: Q6 as First-Class Protocol Concept"
tags:
  - anthropic
  - collaboration
  - anthropic-vacancies
date: 2026-04-29
---

# 20. ADR-002: Q6 as First-Class Protocol Concept

<!-- summary -->
> **Status**: Accepted (new in v1.1)

---
<!-- tags: anthropic, collaboration -->




## 20. ADR-002: Q6 as First-Class Protocol Concept

**Status**: Accepted (new in v1.1)

**Context**: В v1.0 Q6-пространство существовало как implementation 
detail reference portal (pro2 → hexagrams). При росте экосистемы 
стало ясно, что Q6 работает как универсальная система координат 
для всех Repos, не только [[01-интегральный-анализ-профиля-svend4|pro2]].

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
- [[83-8-q6-space-normative]] (сходство 0.11)
- [[26-14-adr-001-federation-over-merging]] (сходство 0.10)


<!-- see-also -->

---

**Смотрите также:**
- [[26-14-adr-001-federation-over-merging]]
- [[83-8-q6-space-normative]]
- [[96-21-adr-003-five-onboarding-paths-as-equal-rank]]
- [[94-19-adr-001-federation-over-merging]]

<!-- backlinks-auto -->
## Упоминается в

- [[06-1-introduction|1. Introduction]]
- [[26-14-adr-001-federation-over-merging|14. ADR-001: Federation over Merging]]
- [[94-19-adr-001-federation-over-merging|19. ADR-001: Federation over Merging]]
- [[96-21-adr-003-five-onboarding-paths-as-equal-rank|21. ADR-003: Five Onboarding Paths as Equal-Rank]]
- [[83-8-q6-space-normative|8. Q6 Space (Normative)]]
- [[README|Вакансии Anthropic — Анализ по кластерам]]
- [[SIMILAR|Похожие документы]]
## Упоминается в

- [[README|Вакансии Anthropic — Анализ по кластерам]]

<!-- related-auto -->
## Связанные документы

- [[96-21-adr-003-five-onboarding-paths-as-equal-rank|21. ADR-003: Five Onboarding Paths as Equal-Rank]] _60%_
- [[94-19-adr-001-federation-over-merging|19. ADR-001: Federation over Merging]] _53%_
- [[26-14-adr-001-federation-over-merging|14. ADR-001: Federation over Merging]] _42%_
- [[83-8-q6-space-normative|8. Q6 Space (Normative)]] _25%_
## Связанные документы

- [[96-21-adr-003-five-onboarding-paths-as-equal-rank|21. ADR-003: Five Onboarding Paths as Equal-Rank]] _42%_
- [[83-8-q6-space-normative|8. Q6 Space (Normative)]] _37%_
- [[26-14-adr-001-federation-over-merging|14. ADR-001: Federation over Merging]] _33%_
- [[94-19-adr-001-federation-over-merging|19. ADR-001: Federation over Merging]] _33%_
- [[06-1-introduction|1. Introduction]] _17%_
- [[104-appendix-c-references|Appendix C: References]] _17%_
- [[40-bridges|Bridges]] _17%_
- [[60-bridges|Bridges]] _17%_
