# Appendix B: Sub-Agent Registry Schema (Sketch)

<!-- summary -->
> For implementation, sub-agent registry entries might follow

---
<!-- tags: rag, architecture, self-improvement -->




## Appendix B: Sub-Agent Registry Schema (Sketch)

For implementation, sub-agent registry entries might follow 
this schema:

```yaml
sub_agent:
  id: "sgb-ix-paragraph-78-24-7-assistance"
  name: "SGB IX § 78 Abs. 6 — 24/7 Psychiatric Assistance"
  domain: "german-social-law"
  specialization_path: 
    - "law"
    - "german"
    - "social-law"
    - "sgb-ix"
    - "section-78"
    - "subsection-6"
  scope:
    covers:
      - "Right to 24/7 psychiatric assistance"
      - "Documentation requirements"
      - "Procedural pathways"
      - "Appeal mechanisms"
    does_not_cover:
      - "Other forms of psychiatric care"
      - "Voluntary commitment procedures"
      - "Tax implications"
  knowledge_base:
    primary_sources:
      - "SGB IX § 78"
      - "BSG B 8 SO 9/19 R"
      - "Implementing regulations"
    methodology:
      - "Case-based reasoning"
      - "Statutory interpretation"
      - "Procedural guidance"
    last_updated: "2026-04-15"
    next_review: "2026-10-15"
  curators:
    primary: 
      name: "[Curator name]"
      credentials: "[Legal qualifications]"
    review_panel:
      - "[Reviewer 1]"
      - "[Reviewer 2]"
  compatibility:
    works_well_with:
      - "sgb-ix-general-procedural"
      - "psychiatric-assessment-interpretation"
      - "social-services-eligibility"
    requires_alongside:
      - "general-german-legal-drafting"
    conflicts_with: []
  quality_indicators:
    expert_review_score: 4.7
    practitioner_satisfaction: 4.5
    error_rate: "0.02"
    update_frequency: "quarterly"
  access:
    license: "CC BY-SA 4.0"
    cost: "Foundation-supported, free for OKWF guild members"
    api_endpoint: "https://nautilus-okwf.org/sub-agents/sgb-ix-paragraph-78-24-7"
```

This schema captures what coordinators need to route effectively, 
what principals need to evaluate fit, and what curators need to 
maintain quality.

The schema is illustrative; production deployment would require 
substantial refinement based on actual implementation experience.

---
