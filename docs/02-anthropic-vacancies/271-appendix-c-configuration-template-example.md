# Appendix C: Configuration Template Example

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
- [270-appendix-b-sub-agent-registry-schema-sketch](docs/02-anthropic-vacancies/270-appendix-b-sub-agent-registry-schema-sketch.md) (сходство 0.11)
- [258-5-configuration-how-principals-build-their-ensembl](docs/02-anthropic-vacancies/258-5-configuration-how-principals-build-their-ensembl.md) (сходство 0.10)
- [265-12-call-for-collaboration](docs/02-anthropic-vacancies/265-12-call-for-collaboration.md) (сходство 0.10)

