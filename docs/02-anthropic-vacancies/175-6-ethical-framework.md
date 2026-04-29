# 6. Ethical Framework

> [!IMPORTANT]
> Ключевой документ для понимания архитектуры. Рекомендуется прочитать в первую очередь.

<!-- alert-added -->

<!-- summary -->
> Representative Agents raise novel ethical questions. We

---
<!-- tags: orchestration, local-first -->




## 6. Ethical Framework

Representative Agents raise novel ethical questions. We 
propose a framework grounded in established principles 
adapted to AI context.

### 6.1. Principal Sovereignty

The principal is **sovereign** over their own representation. 
This means:

- Principal owns all data about themselves used by agent
- Principal can modify or terminate agent at any time
- Principal can override any agent decision
- Principal can audit all agent actions
- Principal cannot be exploited by agent provider

This is non-negotiable. Without principal sovereignty, 
the system becomes another mechanism for exploitation 
of the very populations it claims to serve.

### 6.2. Transparent Capability

Agents must be **honest about what they can and cannot 
do**. This includes:

- Acknowledging when domain expertise exceeds agent 
  capability
- Recommending human professional involvement when 
  appropriate
- Not overstating likelihood of success
- Disclosing failure rates and limitations

Particularly critical in legal, medical, and financial 
domains where overconfidence can cause harm.

### 6.3. No Adverse Action Without Notice

Agent cannot take consequential actions adverse to 
counterparties without principal awareness and approval. 
Examples of adverse actions: legal complaints, public 
allegations, withdrawal of cooperation. These require 
explicit principal decision.

### 6.4. Fairness Across Principals

If multiple principals use agents that interact, fairness 
considerations apply. Agent should not gain advantage 
through manipulation, deception, or exploitation of other 
agents' behavior. Adversarial robustness is required.

### 6.5. Vulnerability Protection

When principal is in vulnerable state (mental health 
crisis, severe illness, cognitive decline), agent's role 
shifts toward protection. May involve:

- Refusing high-stakes commitments
- Escalating to designated trusted human
- Maintaining stable status quo until vulnerability 
  resolves

### 6.6. Consent and Capacity

Some principals (severe cognitive disability, dementia, 
minors) cannot fully consent to agent operation. For 
these populations:

- Agent operates only with explicit guardian authorization
- Guardian retains all override capability
- Agent's scope is conservative, defaulting to status quo
- Periodic re-authorization required

### 6.7. Accessibility as First-Class Concern

Agent interfaces must be **accessible** to populations 
they serve. This means:

- Visual disabilities: full screen-reader compatibility
- Cognitive disabilities: clear, simple language options
- Motor disabilities: voice and alternative input
- Linguistic diversity: high-quality multi-language 
  support
- Technology unfamiliarity: human-mediated onboarding

A Representative Agent that's only accessible to 
tech-sophisticated principals fails its core mission.

---

<!-- similar-docs -->

---

**Похожие документы:**
- [176-7-governance-and-oversight](docs/02-anthropic-vacancies/176-7-governance-and-oversight.md) (сходство 0.15)
- [174-5-architectural-specification](docs/02-anthropic-vacancies/174-5-architectural-specification.md) (сходство 0.14)
- [177-8-risks-and-mitigations](docs/02-anthropic-vacancies/177-8-risks-and-mitigations.md) (сходство 0.13)

