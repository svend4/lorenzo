---
state: normalized
---

# Appendix C: Configuration Template Example

<!-- toc-auto -->
## Contents

- [Appendix C: Configuration Template Example](#appendix-c-configuration-template-example)
- [Похожие документы](#похожие-документы)
- [Смотрите также](#смотрите-также)
- [Кто ссылается на этот документ (8)](#кто-ссылается-на-этот-документ-8)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- abstract-auto -->
> **Абстракт** (авто)
>
> 🎯 **Проблема:** Some will remove sub-agents they don't need.
> ✅ **Результат:** Appendix C: Configuration Template Example For the SGB Advocate Colleague pilot, a starting configuration --- Appendix C: Configuration Template Example For the SGB Advocate Collea
> 🏷️ **Ключевые слова:** `appendix`, `configuration`, `anthropic`, `vacancies`, `their`, `template`, `agent`, `registry`
>


<!-- summary -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

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

## Похожие документы
- [270-appendix-b-sub-agent-registry-schema-sketch](270-appendix-b-sub-agent-registry-schema-sketch.md) (сходство 0.11)
- [258-5-configuration-how-principals-build-their-ensembl](258-5-configuration-how-principals-build-their-ensembl.md) (сходство 0.10)
- [265-12-call-for-collaboration](265-12-call-for-collaboration.md) (сходство 0.10)


<!-- see-also -->

---

## Смотрите также
- [270-appendix-b-sub-agent-registry-schema-sketch](270-appendix-b-sub-agent-registry-schema-sketch.md)
- [321-appendix-a-decision-tree-for-[ingit](306-with-anthropic-s-cowork-platform.md)-adopters](docs/02-anthropic-vacancies/321-appendix-a-decision-tree-for-ingit-adopters.md)
- [211-table-of-contents](211-table-of-contents.md)
- [253-table-of-contents](253-table-of-contents.md)


<!-- backlinks -->

---

## Кто ссылается на этот документ (8)
- [137-table-of-contents](137-table-of-contents.md)
- [211-table-of-contents](211-table-of-contents.md)
- [228-appendix-c-quick-start-architecture-for-sgb-advoca](228-appendix-c-quick-start-architecture-for-sgb-advoca.md)
- [253-table-of-contents](253-table-of-contents.md)
- [258-5-configuration-how-principals-build-their-ensembl](258-5-configuration-how-principals-build-their-ensembl.md)
- 321-appendix-a-decision-tree-for-[ingit-adopters](321-appendix-a-decision-tree-for-ingit-adopters.md)
- [326-содержание](326-содержание.md)
- [README](README.md)

