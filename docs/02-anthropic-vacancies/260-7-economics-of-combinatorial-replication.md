# 7. Economics of Combinatorial Replication

<!-- summary -->
> The economics of Composite Skills Agents differ from both

---

<!-- toc -->
## Содержание

- [7. Economics of Combinatorial Replication](#7-economics-of-combinatorial-replication)
  - [7.1. Cost Structure](#71-cost-structure)
  - [7.2. Combinatorial Value](#72-combinatorial-value)
  - [7.3. Investment Strategy](#73-investment-strategy)
  - [7.4. Funding Models for Sub-Agent Development](#74-funding-models-for-sub-agent-development)
  - [7.5. Sustainable Economics for the SGB Pilot](#75-sustainable-economics-for-the-sgb-pilot)

---

<!-- tags: rag, orchestration, roadmap, anthropic -->




## 7. Economics of Combinatorial Replication

The economics of Composite Skills Agents differ from both 
Type 1 and Type 4 in interesting ways.

### 7.1. Cost Structure

**Sub-agent development**: substantial fixed cost per sub-agent. 
A high-quality narrow-specialist sub-agent might cost €50,000-
€500,000 to build, depending on knowledge base depth.

**Sub-agent maintenance**: moderate ongoing cost. Perhaps 
10-20% of build cost annually for keeping the knowledge base 
current.

**Coordinator development**: substantial one-time cost for 
the coordinator infrastructure. Once built, serves all 
configurations.

**Coordinator operation**: low marginal cost per principal. 
LLM API costs scale with use, but the coordinator itself 
doesn't require per-principal customization beyond 
configuration.

**Configuration management**: low per-principal cost. Adding 
sub-agents to a configuration is essentially free; the 
sub-agents already exist.

This produces interesting unit economics. If an ecosystem has 
500 sub-agents and 10,000 principals, the ratio of sub-agent 
fixed cost to total user value is highly favorable.

### 7.2. Combinatorial Value

The number of possible configurations grows combinatorially:
- 100 sub-agents, choose 15: ~250 billion possible 
  configurations
- 500 sub-agents, choose 20: astronomical

In practice, configurations cluster around common patterns. 
But even within any profession, there's room for substantial 
diversity. Each principal's configuration genuinely reflects 
their distinctive practice.

The combinatorial value is the central economic insight: a 
relatively small fixed investment in sub-agent development 
unlocks an essentially unlimited space of unique principal 
configurations.

### 7.3. Investment Strategy

For an ecosystem (like OKWF) building this infrastructure, 
the investment strategy follows from the economics:

**Phase 1**: Build a small set of broadly applicable sub-agents 
(perhaps 20-50 covering core specializations of one profession). 
This requires substantial upfront investment but enables 
initial configurations.

**Phase 2**: Expand to more specialized sub-agents based on 
observed configuration gaps. As principals use the system, 
their requests for specializations not yet available drive 
priority for new sub-agent development.

**Phase 3**: Federation with external sub-agent providers. 
Once the registry framework is established, sub-agents from 
other organizations can be integrated, accelerating coverage.

**Phase 4**: Cross-profession expansion. Sub-agents developed 
for one profession may apply to adjacent professions. Methodology 
sub-agents particularly cross professional boundaries.

This phasing parallels how academic libraries develop: starting 
with core texts, expanding to specialized works, federating 
with other libraries, and enabling cross-disciplinary access.

### 7.4. Funding Models for Sub-Agent Development

Several funding models are viable:

**Foundation-funded, public registry.** Most aligned with OKWF 
mission. Sub-agents developed through grants, available freely.

**Practitioner-funded, cooperative ownership.** Practitioners 
in a profession collectively fund sub-agent development; they 
own the registry collectively.

**Sponsorship-based.** Foundations or institutions sponsor 
specific sub-agents (e.g., disability rights organizations 
sponsor sub-agents for disability-related specializations).

**Commercial provider, open standards.** Companies build 
sub-agents commercially but follow open standards allowing 
integration. Mixed quality control, market-driven prioritization.

**Hybrid.** Most realistic for early-stage ecosystem. Foundation 
funds core infrastructure, sponsors fund priority sub-agents, 
practitioners contribute to specific narrow sub-agents through 
volunteer expert work.

For OKWF specifically, the hybrid approach plus eventual 
cooperative ownership seems most aligned with mission.

### 7.5. Sustainable Economics for the SGB Pilot

Applied to the SGB Advocate Colleague pilot from Professional 
Colleague Agents v1.0:

Instead of building one large profession-wide agent for German 
social law, build:
- 20-30 narrow sub-agents covering core SGB specializations
- A coordinator that practitioners configure individually
- Templates for common practice patterns (general advocacy, 
  disability rights, elderly care, mental health, child 
  welfare)

Estimated investment:
- 20 sub-agents at €50K average: €1,000,000
- Coordinator development: €300,000
- First-year operations: €200,000
- **Total Year 1: €1.5 million**

This is higher than the original estimate (€430K) but produces 
substantially more capability. Practitioners get composite 
configurations matching their specific practice, not a generic 
SGB agent.

For 1,000 practitioners over three years, this comes to 
approximately €500/practitioner/year — feasible for foundation 
funding or modest practitioner contribution.

---
