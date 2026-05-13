---
state: approved
---

# 6. Ethical Framework

<!-- toc-auto -->
## Contents

- [Содержание](#содержание)
- [6. Ethical Framework](#6-ethical-framework)
  - [6.1. Principal Sovereignty](#61-principal-sovereignty)
  - [6.2. Transparent Capability](#62-transparent-capability)
  - [6.3. No Adverse Action Without Notice](#63-no-adverse-action-without-notice)
  - [6.4. Fairness Across Principals](#64-fairness-across-principals)
  - [6.5. Vulnerability Protection](#65-vulnerability-protection)
  - [6.6. Consent and Capacity](#66-consent-and-capacity)
  - [6.7. Accessibility as First-Class Concern](#67-accessibility-as-first-class-concern)
- [Использование](#использование)
- [Смотрите также](#смотрите-также)


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
- [Использование](#использование)
- [Смотрите также](#смотрите-также)

---


> [!IMPORTANT]
> Ключевой документ для понимания архитектуры. Рекомендуется прочитать в первую очередь.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — paper «Representative Agent Layer (EN)». Ключевой документ для понимания архитектуры.

---
<!-- tags: orchestration, local-first, architecture, anthropic -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — paper «Representative Agent Layer (EN)».

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

<!-- see-also -->

---

## Использование
```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "6 Ethical Framework"
```

## Смотрите также
- [175-6-ethical-framework](../../02-anthropic-vacancies/175-6-ethical-framework.md)
- [07-governance-oversight](07-governance-oversight.md)
- [05-architectural-specification](05-architectural-specification.md)
- [08-risks-mitigations](08-risks-mitigations.md)


<!-- backlinks -->

---

**Кто ссылается на этот документ (8):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [05-architectural-specification](05-architectural-specification.md)
- [07-governance-oversight](07-governance-oversight.md)
- [08-risks-mitigations](08-risks-mitigations.md)
- [README](README.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [06-ethical-framework](../../obsidian/nautilus/representative-agent-layer-en/06-ethical-framework.md) (сходство 0.98)
- [175-6-ethical-framework](../../02-anthropic-vacancies/175-6-ethical-framework.md) (сходство 0.85)
- [175-6-ethical-framework](../../obsidian/02-anthropic-vacancies/175-6-ethical-framework.md) (сходство 0.84)

