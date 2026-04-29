# 9. Integration with OKWF Infrastructure

> [!TIP]
> Документ содержит практические рекомендации и лучшие практики.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — paper «Composite Skills Agents».

---

<!-- toc -->
## Содержание

- [9. Integration with OKWF Infrastructure](#9-integration-with-okwf-infrastructure)
  - [9.1. Connection to Pattern Library](#91-connection-to-pattern-library)
  - [9.2. Connection to Guild Structure](#92-connection-to-guild-structure)
  - [9.3. Connection to Double-Triangle Architecture](#93-connection-to-double-triangle-architecture)
  - [9.4. Connection to Representative Agents](#94-connection-to-representative-agents)
  - [9.5. Refined OKWF Rollout Plan](#95-refined-okwf-rollout-plan)
  - [9.6. Practical Implication for Pilot Design](#96-practical-implication-for-pilot-design)

---

<!-- tags: rag, architecture, roadmap, anthropic -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — paper «Composite Skills Agents».

## 9. Integration with OKWF Infrastructure

Composite Skills Agents fit naturally into the OKWF infrastructure 
proposed in earlier papers, with some specific implications.

### 9.1. Connection to Pattern Library

The Nautilus pattern library architecture (public patterns, 
private instances, anonymization pipeline) provides foundational 
support for the sub-agent registry. Patterns become source 
material for sub-agents. Anonymized practitioner contributions 
flow into pattern library, which informs sub-agent updates.

The connection is not just analogical. The same infrastructure 
serves both:
- Pattern library: knowledge fragments accessible to humans 
for review
- Sub-agent registry: knowledge fragments operationalized 
into AI assistants

A given knowledge artifact can serve both functions.

### 9.2. Connection to Guild Structure

OKWF's guild structure (groups of practitioners by professional 
area) provides natural organization for sub-agent development. 
Each guild can:
- Identify priority sub-agents for their area
- Contribute expert curation
- Test sub-agents in actual practice
- Maintain quality standards
- Develop common configuration templates

Guilds become both consumers and producers of composite 
infrastructure.

### 9.3. Connection to Double-Triangle Architecture

In the Double-Triangle Architecture, each Node (human 
practitioner) has lower-triangle assistants supporting their 
work. Composite Skills Agents formalize what lower-triangle 
assistants typically contain: not one undifferentiated assistant 
but a coordinated configuration of narrow specialists.

The composite agent itself is the orchestrator of the lower 
triangle. The sub-agents in the configuration are the actual 
"lower triangle assistants" doing specialized work.

This refines the Double-Triangle model: the lower triangle is 
not a flat set of assistants but a coordinated ensemble.

### 9.4. Connection to Representative Agents

Composite Skills Agents and Representative Agents work together 
naturally:
- The composite agent supports the practitioner's work
- The representative agent supports the practitioner's external 
position

A mature practitioner has both: composite for daily work, 
representative for opportunity navigation. They share underlying 
profile information about the practitioner but operate in 
different layers.

### 9.5. Refined OKWF Rollout Plan

Earlier papers proposed sequencing of OKWF deployment. With 
Composite Skills Agents recognized, the sequence refines to:

**Phase 0** (Months 1-12): Foundation establishment, initial 
sub-agent set for one profession (perhaps SGB social law). Build 
20-30 narrow sub-agents plus coordinator. Pilot with 5-10 
practitioners.

**Phase 1** (Year 2): Expand sub-agent set, scale practitioners 
to 100-500. Establish pattern library connection, anonymization 
pipeline. Begin contribution flow back into sub-agent updates.

**Phase 2** (Years 2-3): Expand to second profession (perhaps 
educational support for disabled students, maintaining thematic 
connection). Cross-profession integration of methodology 
sub-agents.

**Phase 3** (Years 3-5): Multiple professions, federated 
sub-agent registry, mature configuration management. Begin 
adding Representative Agent layer for principals who want it.

**Phase 4** (Year 5+): Multi-language, multi-jurisdiction 
expansion. Open registry with multiple curating organizations.

This plan is more realistic than the earlier proposal because 
it matches how skilled practitioners actually develop and what 
they actually need.

### 9.6. Practical Implication for Pilot Design

For the SGB Advocate Colleague pilot specifically:

**Original plan**: Build one comprehensive Professional 
Colleague Agent for German social law.

**Refined plan**: Build a sub-agent registry covering 
20-30 narrow SGB specializations, plus a coordinator that 
practitioners configure individually.

Cost increases (€1.5M vs €430K for Year 1), but produces a 
genuinely useful infrastructure that scales to multiple 
adjacent legal domains and supports practitioners' actual 
diverse practices rather than forcing one-size-fits-all 
generalization.

This is a better proposal for foundation funders even at higher 
cost, because it demonstrates a more sophisticated understanding 
of how skilled practice works and produces infrastructure with 
broader applicability.

---

<!-- see-also -->

---

**Смотрите также:**
- [262-9-integration-with-okwf-infrastructure](docs/02-anthropic-vacancies/262-9-integration-with-okwf-infrastructure.md)
- [13-closing](docs/nautilus/composite-skills-agents/13-closing.md)
- [07-economics-combinatorial](docs/nautilus/composite-skills-agents/07-economics-combinatorial.md)
- [04-sub-agent-registry](docs/nautilus/composite-skills-agents/04-sub-agent-registry.md)

