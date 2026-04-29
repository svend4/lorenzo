---
title: "Appendix C: Configuration Template Example"
tags:
  - rag
  - anthropic-vacancies
date: 2026-04-29
---

# Appendix C: Configuration Template Example

<!-- abstract-auto -->
> **Абстракт** (авто)
>
> 🎯 **Проблема:** Some will remove sub-agents they don't need.
> ✅ **Результат:** Appendix C: Configuration Template Example For the SGB Advocate Colleague pilot, a starting configuration --- Appendix C: Configuration Template Example For the SGB Advocate Collea
> 🏷️ **Ключевые слова:** `appendix`, `configuration`, `anthropic`, `vacancies`, `their`, `template`, `agent`, `registry`
>


<!-- summary -->
> For the SGB Advocate Colleague pilot, a starting configuration

---
<!-- tags: rag -->




## Appendix C: Configuration Template Example

For the SGB Advocate Colleague pilot, a starting configuration 
template for "General Disability Rights Advocate" might include:

```yaml
configuration:
  name: "General Disability Rights Advocate (Saxony)"
  description: |
    Starting configuration for advocates working on disability 
    rights cases in Saxony, Germany. Suitable for practitioners 
    handling general SGB IX and SGB XII cases without specific 
    sub-specialization.
  base_profile:
    profession: "legal-advocate"
    sub_specialty: "disability-rights"
    jurisdiction: "germany-saxony"
    languages: ["de", "en"]
  sub_agents:
    foundational:
      - "sgb-ix-general-overview"
      - "sgb-xii-general-overview"
      - "german-procedural-law-basics"
      - "general-legal-drafting-german"
    specialized:
      - "sgb-ix-section-78-eingliederungshilfe"
      - "sgb-ix-personal-budget-procedures"
      - "bsg-precedent-disability-cases"
      - "saxony-court-procedural-conventions"
    supporting:
      - "medical-assessment-interpretation"
      - "fristwahrung-deadline-management"
      - "ksv-sachsen-interaction-patterns"
      - "sozialamt-dresden-interaction-patterns"
    optional_growth_edges:
      - "mental-health-disability-specifics"
      - "child-disability-specifics"
      - "elderly-disability-specifics"
      - "migrant-disability-specifics"
  total_sub_agents: 13 (with 4 optional)
  estimated_setup_time: "30-60 minutes"
  estimated_first_use: "Same day after configuration"
  recommended_review: "Quarterly for first year, then annually"
```

This template provides a starting point that practitioners 
modify based on their actual practice. Some will add sub-agents 
for additional specializations. Some will remove sub-agents 
they don't need. Each ends up with a configuration distinctive 
to their practice.

The "optional_growth_edges" section deliberately suggests 
specializations the practitioner might add as their practice 
develops, encouraging exploration beyond the initial 
configuration.

---

<!-- similar-docs -->

---

**Похожие документы:**
- [[270-appendix-b-sub-agent-registry-schema-sketch]] (сходство 0.11)
- [[258-5-configuration-how-principals-build-their-ensembl]] (сходство 0.10)
- [[265-12-call-for-collaboration]] (сходство 0.10)


<!-- see-also -->

---

**Смотрите также:**
- [[270-appendix-b-sub-agent-registry-schema-sketch]]
- [[306-with-anthropic-s-cowork-platform|321-appendix-a-decision-tree-for-[ingit]]-adopters](docs/02-anthropic-vacancies/321-appendix-a-decision-tree-for-ingit-adopters.md)
- [[211-table-of-contents]]
- [[253-table-of-contents]]

