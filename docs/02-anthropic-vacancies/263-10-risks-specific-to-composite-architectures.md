# 10. Risks Specific to Composite Architectures

> [!TIP]
> Документ содержит практические рекомендации и лучшие практики.

<!-- alert-added -->

<!-- summary -->
> Composite Skills Agents inherit some risks from Professional

---

<!-- toc -->
## Содержание

- [10. Risks Specific to Composite Architectures](#10-risks-specific-to-composite-architectures)
  - [10.1. Risk: Configuration Paralysis](#101-risk-configuration-paralysis)
  - [10.2. Risk: Configuration Echo Chamber](#102-risk-configuration-echo-chamber)
  - [10.3. Risk: Sub-Agent Dependency](#103-risk-sub-agent-dependency)
  - [10.4. Risk: Coordinator Bias](#104-risk-coordinator-bias)
  - [10.5. Risk: Quality Variation Across Sub-Agents](#105-risk-quality-variation-across-sub-agents)
  - [10.6. Risk: Profession Fragmentation](#106-risk-profession-fragmentation)
  - [10.7. Risk: Hidden Dependencies Among Sub-Agents](#107-risk-hidden-dependencies-among-sub-agents)
  - [10.8. Risk: Configuration as Competitive Advantage Hoarding](#108-risk-configuration-as-competitive-advantage-hoarding)

---

<!-- tags: rag, self-improvement -->




## 10. Risks Specific to Composite Architectures

Composite Skills Agents inherit some risks from Professional 
Colleague Agents but also introduce new risks specific to 
ensemble configurations.

### 10.1. Risk: Configuration Paralysis

**Scenario**: Faced with hundreds of available sub-agents, the 
principal cannot decide which to include. Configuration becomes 
overwhelming task. Principal gives up and uses generic 
Professional Colleague Agent instead, missing the value of 
composite.

**Mitigations**:
- Strong starting templates for common professional patterns
- AI-assisted recommendation as default (with override)
- Limit on initial configuration size (start with 5-10, grow 
  over time)
- Mentor connection for complex configuration decisions

### 10.2. Risk: Configuration Echo Chamber

**Scenario**: Principal selects sub-agents that confirm their 
existing approach, missing specializations that would challenge 
or expand their practice. Composite becomes a sophisticated 
form of confirmation bias.

**Mitigations**:
- Recommendation system explicitly suggests "growth-edge" 
  sub-agents outside principal's current configuration
- Regular configuration reviews with prompts to consider 
  unfamiliar specializations
- Mentor input that intentionally surfaces alternative 
  perspectives
- Public visibility of how others in the same profession 
  configure differently

### 10.3. Risk: Sub-Agent Dependency

**Scenario**: Principal becomes dependent on a specific sub-agent 
that is later deprecated or significantly changed. Their practice 
disrupts when configuration needs to change.

**Mitigations**:
- Open standards make sub-agents portable and replaceable
- Multiple sub-agents covering same specialization (compete on 
  quality, not lock-in)
- Notification when sub-agent will be deprecated, with 
  migration paths
- Configuration export so principal can move between 
  coordinator providers

### 10.4. Risk: Coordinator Bias

**Scenario**: The coordinator (general infrastructure managing 
configurations) develops biases in routing or synthesis that 
systematically favor some sub-agents over others. Practice 
patterns shift in ways principals didn't choose.

**Mitigations**:
- Open coordinator architecture, with multiple coordinator 
  options
- Transparent routing logic (principal can see why sub-agent 
  was selected)
- Auditable behavior over time
- Coordinator evaluation as part of platform governance

### 10.5. Risk: Quality Variation Across Sub-Agents

**Scenario**: Sub-agent registry includes high-quality and 
low-quality sub-agents. Principals using lower-quality sub-agents 
in their configurations get poorer support without realizing it.

**Mitigations**:
- Visible quality indicators on sub-agents
- Curation standards for inclusion in main registry
- User feedback loops affecting visibility
- Federated curation allowing principals to choose which 
  curators they trust

### 10.6. Risk: Profession Fragmentation

**Scenario**: As composite configurations diversify, professional 
practice fragments. Practitioners working on similar problems 
develop incompatible approaches because they used different 
sub-agent configurations. Professional coherence weakens.

**Mitigations**:
- Sub-agents share common foundational knowledge (so 
  configurations diverge from a common base)
- Guild structure maintains profession-level community across 
  diverse configurations
- Cross-configuration patterns in shared pattern library
- Recognition that some fragmentation is healthy diversification 
  versus unhealthy disconnection

### 10.7. Risk: Hidden Dependencies Among Sub-Agents

**Scenario**: A configuration appears to work well, but its 
output depends on subtle interactions between specific sub-agents. 
When one sub-agent updates, the configuration's output changes 
in ways neither principal nor coordinator anticipated.

**Mitigations**:
- Version pinning (configurations specify exact sub-agent 
  versions, opt into updates)
- Compatibility testing when sub-agents update
- Notification of significant behavioral changes in 
  sub-agents
- Configuration testing against past examples to detect drift

### 10.8. Risk: Configuration as Competitive Advantage Hoarding

**Scenario**: Principals discover that specific configurations 
are particularly effective. They keep these configurations 
secret as competitive advantage. Configuration knowledge becomes 
hoarded rather than shared, limiting benefit to broader 
practice.

**Mitigations**:
- Default openness about configurations (shared by default, 
  opt-in to keep private)
- Anonymized configuration patterns published in pattern 
  library
- Recognition for sharing effective configurations
- Cooperative ownership models that align individual benefit 
  with collective improvement

---

<!-- similar-docs -->

---

**Похожие документы:**
- [262-9-integration-with-okwf-infrastructure](262-9-integration-with-okwf-infrastructure.md) (сходство 0.15)
- [256-3-what-makes-a-composite-skills-agent](256-3-what-makes-a-composite-skills-agent.md) (сходство 0.15)
- [264-11-open-questions](264-11-open-questions.md) (сходство 0.15)


<!-- see-also -->

---

**Смотрите также:**
- [262-9-integration-with-okwf-infrastructure](262-9-integration-with-okwf-infrastructure.md)
- [264-11-open-questions](264-11-open-questions.md)
- [257-4-the-sub-agent-registry](257-4-the-sub-agent-registry.md)
- [256-3-what-makes-a-composite-skills-agent](256-3-what-makes-a-composite-skills-agent.md)

<!-- backlinks-auto -->
## Упоминается в

- [Вакансии Anthropic — Анализ по кластерам](../README.md)

<!-- related-auto -->
## Связанные документы

- [8. Risks and Mitigations](177-8-risks-and-mitigations.md) _42%_
- [3. What Makes a Composite Skills Agent](256-3-what-makes-a-composite-skills-agent.md) _37%_
- [11. Open Questions](264-11-open-questions.md) _37%_
- [OPEN KNOWLEDGE WORK FOUNDATION.md](151-open-knowledge-work-foundation-md.md) _29%_
- [10. Open Questions](179-10-open-questions.md) _29%_
- [Abstract](252-abstract.md) _29%_
- [5. Configuration: How Principals Build Their Ensembles](258-5-configuration-how-principals-build-their-ensembl.md) _29%_
- [6. Coordination and Disagreement Resolution](259-6-coordination-and-disagreement-resolution.md) _29%_
