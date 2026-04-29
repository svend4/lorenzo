# 4. The Sub-Agent Registry

> [!TIP]
> Документ содержит практические рекомендации и лучшие практики.

<!-- alert-added -->

<!-- summary -->
> The infrastructure underlying Composite Skills Agents requires

---

<!-- toc -->
## Содержание

- [4. The Sub-Agent Registry](#4-the-sub-agent-registry)
  - [4.1. What a Sub-Agent Is](#41-what-a-sub-agent-is)
  - [4.2. Registry Structure](#42-registry-structure)
  - [4.3. How Sub-Agents Get Built](#43-how-sub-agents-get-built)
  - [4.4. The Registry as Public Good](#44-the-registry-as-public-good)
  - [4.5. Curation and Trust](#45-curation-and-trust)

---

<!-- tags: ingestion, roadmap, self-improvement -->




## 4. The Sub-Agent Registry

The infrastructure underlying Composite Skills Agents requires 
a curated registry of narrow-specialist sub-agents. This is a 
substantial architectural component deserving its own discussion.

### 4.1. What a Sub-Agent Is

A sub-agent in this context is functionally equivalent to a 
narrow Professional Colleague Agent (Type 1) — but for a 
**very narrow** specialization.

Where a typical Professional Colleague Agent might serve "all 
teachers," a sub-agent might serve "all teachers working on 
constructivist pedagogy for mathematics in upper primary 
grades."

The narrowness is the point. Sub-agents are deeply specialized 
in their narrow areas. That depth is what makes the composite 
configuration valuable.

### 4.2. Registry Structure

The sub-agent registry must capture, for each sub-agent:

**Identity and scope.** What does this sub-agent specialize in? 
What questions does it answer? What questions does it not 
answer?

**Boundary conditions.** Where does this sub-agent's expertise 
end? What other specializations does it complement? What 
specializations does it not engage with?

**Quality indicators.** How was the sub-agent's knowledge base 
curated? By whom? When last updated? What is the known error 
profile?

**Compatibility hints.** Which other sub-agents commonly combine 
with this one? Which combinations work poorly?

**Usage patterns.** How is this sub-agent typically used? In 
what types of tasks? At what stages of professional work?

This registry information is what enables the composite agent 
coordinator to route effectively. Without rich registry data, 
routing degrades.

### 4.3. How Sub-Agents Get Built

Building a sub-agent is a substantial effort. Each requires:
- Curated knowledge base for the narrow specialization
- Quality assurance against expert practice
- Integration interface compatible with composite agents
- Documentation of scope, boundaries, and usage

Several models for building sub-agents:

**Model 1 — Expert-driven, paid.** A curator with deep expertise 
in the specialization is paid to develop the sub-agent. Highest 
quality, slowest scaling.

**Model 2 — Expert-driven, voluntary.** Practitioners contribute 
to sub-agent development as part of community participation. 
Lower direct cost, requires strong community.

**Model 3 — Federation contribution.** Existing knowledge 
artifacts (textbooks, methodological documents, case studies) 
are integrated into sub-agent knowledge bases through partial 
automation plus expert review. Hybrid efficiency.

**Model 4 — Pattern library extraction.** Patterns extracted 
from many practitioners' work (anonymized through Nautilus-style 
anonymization pipeline) become sub-agent training material. 
Highest scale, requires substantial active practice base.

For mature ecosystems, all four models operate simultaneously. 
For new ecosystems (like OKWF in early phases), Model 1 plus 
Model 3 are most feasible.

### 4.4. The Registry as Public Good

A critical architectural decision: should the sub-agent registry 
be proprietary or open?

**Arguments for proprietary**: easier monetization, more 
investment incentive, quality control through gatekeeping.

**Arguments for open**: prevents profession capture, allows 
multiple coordinators to compete, enables community contribution, 
matches mission of foundation-funded infrastructure.

For OKWF specifically, the open registry is strongly preferred. 
A proprietary registry concentrating control over which 
specializations exist would replicate exactly the kind of 
gatekeeping the foundation aims to dismantle.

The open registry model parallels how academic literature, 
open-source software libraries, and Creative Commons content 
work: many contributors, public access, multiple aggregators 
on top.

### 4.5. Curation and Trust

An open registry needs curation to maintain quality. Without 
curation, sub-agents of varying quality flood the registry, 
making coordination unreliable.

Curation can be:
- **Centralized**: foundation-employed curators evaluate 
  submissions
- **Distributed**: peer review by qualified practitioners
- **Reputation-based**: established sub-agents gain reputation 
  through use; new ones earn reputation over time
- **Federated**: multiple curating organizations operate, each 
  with their own standards; principals choose which curators 
  they trust

A combination is likely best. Foundation curators provide 
baseline; peer review distributes load; reputation accumulates 
over time; federation allows diverse views.

This is similar to how scholarly publishing works: journals 
provide gatekeeping, but the journal landscape includes diverse 
publishers with different standards, and reputation accumulates 
across both journals and individual researchers.

---

<!-- similar-docs -->

---

**Похожие документы:**
- [260-7-economics-of-combinatorial-replication](docs/02-anthropic-vacancies/260-7-economics-of-combinatorial-replication.md) (сходство 0.19)
- [262-9-integration-with-okwf-infrastructure](docs/02-anthropic-vacancies/262-9-integration-with-okwf-infrastructure.md) (сходство 0.18)
- [256-3-what-makes-a-composite-skills-agent](docs/02-anthropic-vacancies/256-3-what-makes-a-composite-skills-agent.md) (сходство 0.16)


<!-- see-also -->

---

**Смотрите также:**
- [262-9-integration-with-okwf-infrastructure](docs/02-anthropic-vacancies/262-9-integration-with-okwf-infrastructure.md)
- [260-7-economics-of-combinatorial-replication](docs/02-anthropic-vacancies/260-7-economics-of-combinatorial-replication.md)
- [158-4-proposed-infrastructure](docs/02-anthropic-vacancies/158-4-proposed-infrastructure.md)
- [263-10-risks-specific-to-composite-architectures](docs/02-anthropic-vacancies/263-10-risks-specific-to-composite-architectures.md)

