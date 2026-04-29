# 6. Ethical Framework

<!-- toc -->
## Содержание

- [Contents](#contents)
- [6. Ethical Framework](#6-ethical-framework)
  - [6.1. Principal Sovereignty](#61-principal-sovereignty)
  - [6.2. Transparent Capability](#62-transparent-capability)
  - [6.3. No Adverse Action Without Notice](#63-no-adverse-action-without-notice)
  - [6.4. Fairness Across Principals](#64-fairness-across-principals)
  - [6.5. Vulnerability Protection](#65-vulnerability-protection)
  - [6.6. Consent and Capacity](#66-consent-and-capacity)
  - [6.7. Accessibility as First-Class Concern](#67-accessibility-as-first-class-concern)
- [Упоминается в](#упоминается-в)
- [Связанные документы](#связанные-документы)

---


<!-- toc-auto -->
## Contents

- [6. Ethical Framework](#6-ethical-framework)
  - [6.1. Principal Sovereignty](#61-principal-sovereignty)
  - [6.2. Transparent Capability](#62-transparent-capability)
  - [6.3. No Adverse Action Without Notice](#63-no-adverse-action-without-notice)
  - [6.4. Fairness Across Principals](#64-fairness-across-principals)
  - [6.5. Vulnerability Protection](#65-vulnerability-protection)
  - [6.6. Consent and Capacity](#66-consent-and-capacity)
  - [6.7. Accessibility as First-Class Concern](#67-accessibility-as-first-class-concern)


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


<!-- see-also -->

---

**Смотрите также:**
- [176-7-governance-and-oversight](docs/02-anthropic-vacancies/176-7-governance-and-oversight.md)
- [174-5-architectural-specification](docs/02-anthropic-vacancies/174-5-architectural-specification.md)
- [177-8-risks-and-mitigations](docs/02-anthropic-vacancies/177-8-risks-and-mitigations.md)
- [179-10-open-questions](docs/02-anthropic-vacancies/179-10-open-questions.md)

<!-- backlinks-auto -->
## Упоминается в

- [Вакансии Anthropic — Анализ по кластерам](docs/02-anthropic-vacancies/README.md)

<!-- related-auto -->
## Связанные документы

- [7. Governance and Oversight](docs/02-anthropic-vacancies/176-7-governance-and-oversight.md) _21%_
- [10. Open Questions](docs/02-anthropic-vacancies/179-10-open-questions.md) _21%_
- [12. Closing](docs/02-anthropic-vacancies/223-12-closing.md) _21%_
- [5. Configuration: How Principals Build Their Ensembles](docs/02-anthropic-vacancies/258-5-configuration-how-principals-build-their-ensembl.md) _21%_
- [7. Open Questions](docs/02-anthropic-vacancies/144-7-open-questions.md) _17%_
- [Acknowledgments](docs/02-anthropic-vacancies/146-acknowledgments.md) _17%_
- [2. Historical Precedents: Agents as Civilizational Innovation](docs/02-anthropic-vacancies/171-2-historical-precedents-agents-as-civilizational-i.md) _17%_
- [3. What Makes a Representative Agent](docs/02-anthropic-vacancies/172-3-what-makes-a-representative-agent.md) _17%_
