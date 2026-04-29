# 11. Open Questions

<!-- toc -->
## Содержание

- [Contents](#contents)
- [11. Open Questions](#11-open-questions)
  - [11.1. Granularity Questions](#111-granularity-questions)
  - [11.2. Configuration Stability](#112-configuration-stability)
  - [11.3. Cross-Professional Configurations](#113-cross-professional-configurations)
  - [11.4. Configuration Evolution at Scale](#114-configuration-evolution-at-scale)
  - [11.5. Sub-Agent Quality Across Cultures](#115-sub-agent-quality-across-cultures)
  - [11.6. Liability for Composite Outputs](#116-liability-for-composite-outputs)
  - [11.7. The "Emergence" Question](#117-the-emergence-question)
  - [11.8. Transition from Composite to Representative](#118-transition-from-composite-to-representative)
- [Упоминается в](#упоминается-в)
- [Связанные документы](#связанные-документы)

---


<!-- toc-auto -->
## Contents

- [11. Open Questions](#11-open-questions)
  - [11.1. Granularity Questions](#111-granularity-questions)
  - [11.2. Configuration Stability](#112-configuration-stability)
  - [11.3. Cross-Professional Configurations](#113-cross-professional-configurations)
  - [11.4. Configuration Evolution at Scale](#114-configuration-evolution-at-scale)
  - [11.5. Sub-Agent Quality Across Cultures](#115-sub-agent-quality-across-cultures)
  - [11.6. Liability for Composite Outputs](#116-liability-for-composite-outputs)
  - [11.7. The "Emergence" Question](#117-the-emergence-question)
  - [11.8. Transition from Composite to Representative](#118-transition-from-composite-to-representative)


> [!TIP]
> Документ содержит практические рекомендации и лучшие практики.

<!-- alert-added -->

<!-- summary -->
> Many questions about Composite Skills Agents remain open.

---
<!-- tags: rag, anthropic -->




## 11. Open Questions

Many questions about Composite Skills Agents remain open.

### 11.1. Granularity Questions

How narrow should sub-agents be? Too narrow and configurations 
become unmanageable; too broad and the composite pattern 
collapses back to Professional Colleague Agent.

What's the right granularity for different professions? Likely 
varies — music might support finer granularity than law. 
Empirical question requiring deployment.

### 11.2. Configuration Stability

How often should principals revise configurations? Too often 
and they spend more time configuring than working; too rarely 
and configurations drift from current practice.

What signals suggest configuration revision is needed? Likely 
some combination of: significant change in principal's work, 
new sub-agents available, observed gaps in current configuration, 
explicit annual review.

### 11.3. Cross-Professional Configurations

When practitioners genuinely span professions (lawyer who is 
also social worker, doctor who is also researcher), can their 
configuration span sub-agents from multiple professions? How 
does the coordinator handle this?

This case is increasingly common as work becomes more 
interdisciplinary.

### 11.4. Configuration Evolution at Scale

If 10,000 practitioners use composite agents, what happens 
across the population? Do configurations cluster around 
patterns? Does this clustering match natural sub-specialties 
or create artificial groupings?

Empirical study would inform whether the architecture supports 
or constrains professional evolution.

### 11.5. Sub-Agent Quality Across Cultures

Sub-agents developed primarily in one cultural or linguistic 
context may not serve well in others. How does the registry 
handle cultural variation? Multiple parallel sub-agents for 
different contexts? Configurable cultural overlays?

### 11.6. Liability for Composite Outputs

When a composite agent's output (drawing on multiple sub-agents) 
contains errors, who bears responsibility? The principal who 
used it? The coordinator? Each sub-agent that contributed? 
The platform?

Legal frameworks for traditional Professional Colleague Agents 
are nascent; composite versions add complexity.

### 11.7. The "Emergence" Question

When many sub-agents combine in a configuration, do useful 
properties emerge that weren't present in any individual 
sub-agent? Or do composite outputs simply average their 
contributions?

Theoretically interesting question with practical implications 
for whether composite is genuinely more than the sum of parts.

### 11.8. Transition from Composite to Representative

As principals develop sophisticated composite configurations, 
when (if ever) does it make sense to graduate to a Representative 
Agent (Type 4) with truly individual specialization? Or do 
composites serve indefinitely?

The pattern from human mastery suggests configurations evolve 
indefinitely; "graduation" may not be the right metaphor.

---

<!-- similar-docs -->

---

**Похожие документы:**
- [265-12-call-for-collaboration](docs/02-anthropic-vacancies/265-12-call-for-collaboration.md) (сходство 0.18)
- [221-10-open-questions](docs/02-anthropic-vacancies/221-10-open-questions.md) (сходство 0.18)
- [256-3-what-makes-a-composite-skills-agent](docs/02-anthropic-vacancies/256-3-what-makes-a-composite-skills-agent.md) (сходство 0.18)


<!-- see-also -->

---

**Смотрите также:**
- [265-12-call-for-collaboration](docs/02-anthropic-vacancies/265-12-call-for-collaboration.md)
- [256-3-what-makes-a-composite-skills-agent](docs/02-anthropic-vacancies/256-3-what-makes-a-composite-skills-agent.md)
- [262-9-integration-with-okwf-infrastructure](docs/02-anthropic-vacancies/262-9-integration-with-okwf-infrastructure.md)
- [221-10-open-questions](docs/02-anthropic-vacancies/221-10-open-questions.md)

<!-- backlinks-auto -->
## Упоминается в

- [Вакансии Anthropic — Анализ по кластерам](docs/02-anthropic-vacancies/README.md)

<!-- related-auto -->
## Связанные документы

- [10. Risks Specific to Composite Architectures](docs/02-anthropic-vacancies/263-10-risks-specific-to-composite-architectures.md) _37%_
- [12. Call for Collaboration](docs/02-anthropic-vacancies/265-12-call-for-collaboration.md) _33%_
- [OPEN KNOWLEDGE WORK FOUNDATION.md](docs/02-anthropic-vacancies/151-open-knowledge-work-foundation-md.md) _29%_
- [10. Open Questions](docs/02-anthropic-vacancies/179-10-open-questions.md) _29%_
- [10. Open Questions](docs/02-anthropic-vacancies/221-10-open-questions.md) _29%_
- [COMPOSITE SKILLS AGENT.md](docs/02-anthropic-vacancies/249-composite-skills-agent-md.md) _29%_
- [3. What Makes a Composite Skills Agent](docs/02-anthropic-vacancies/256-3-what-makes-a-composite-skills-agent.md) _29%_
- [5. Configuration: How Principals Build Their Ensembles](docs/02-anthropic-vacancies/258-5-configuration-how-principals-build-their-ensembl.md) _29%_
