---
title: "5. Architectural Specification"
tags:
  - anthropic-vacancies
date: 2026-04-29
---

# 5. Architectural Specification

<!-- abstract-auto -->
> **Абстракт** (авто)
>
> 🎯 **Проблема:** User Interface: Multi-modal access (web, mobile, voice) appropriate to principal's accessibility needs.
> 🔧 **Подход:** Enables principal review, dispute resolution, accountability.
> ✅ **Результат:** Enables principal review, dispute resolution, accountability.
> 🏷️ **Ключевые слова:** `principal`, `agent`, `representative`, `component`, `anthropic`, `vacancies`, `triangle`, `principle`
>


<!-- summary -->
> A Representative Agent system consists of seven components:

---

<!-- toc -->
## Содержание

- [5. Architectural Specification](#5-architectural-specification)
  - [5.1. Core Components](#51-core-components)
  - [5.2. Operating Principles](#52-operating-principles)
  - [5.3. Technical Stack](#53-technical-stack)
  - [5.4. Integration with Double-Triangle Architecture](#54-integration-with-double-triangle-architecture)

---

<!-- tags: rag, orchestration, ingestion, local-first, architecture, self-improvement -->




## 5. Architectural Specification

### 5.1. Core Components

A Representative Agent system consists of seven components:

**Component 1 — Principal Profile**: Comprehensive 
representation of the principal's expertise, capacity, 
preferences, history, goals, constraints. Constructed 
through onboarding interview, refined through ongoing 
interaction. Owned by principal, modifiable by principal.

**Component 2 — Discovery Engine**: Continuously monitors 
relevant domains for opportunities. Sources include: 
public job boards, RSS feeds, partner systems, peer 
networks, regulatory announcements. Outputs a stream of 
candidate opportunities.

**Component 3 — Curation Filter**: Evaluates each 
opportunity against profile fit, capacity match, 
preference alignment. Outputs ranked shortlist. 
Conservative by default — better to surface fewer high-fit 
opportunities than overwhelm.

**Component 4 — Presentation Generator**: Crafts 
counterparty-appropriate presentations of the principal 
when relevant opportunity is found. Translates principal's 
value into target's language. Preserves principal's voice 
where possible.

**Component 5 — Communication Manager**: Handles ongoing 
correspondence with counterparties. Initial outreach, 
clarification, scheduling. Surfaces complex decisions to 
principal. Operates within bounds set by principal.

**Component 6 — Protection Monitor**: Identifies risks, 
inconsistencies, scams, exploitation. Alerts principal to 
warning signs. Maintains skeptical posture toward 
counterparties.

**Component 7 — Audit Log**: Comprehensive record of all 
agent decisions and communications. Enables principal 
review, dispute resolution, accountability.

### 5.2. Operating Principles

Six principles govern agent behavior:

**Principle 1 — Principal Authority**: Final authority on 
all consequential decisions remains with principal. Agent 
recommends, principal decides.

**Principle 2 — Transparent Operation**: All agent actions 
are visible to principal upon request. No hidden actions 
or communications.

**Principle 3 — Conservative Default**: When uncertain, 
agent surfaces decision to principal rather than acting 
independently. Better to over-consult than overstep.

**Principle 4 — Loyalty**: Agent serves only principal's 
interests. No conflicts of interest with platforms, 
counterparties, or third parties.

**Principle 5 — Capability Honesty**: Agent acknowledges 
limits of its capabilities. When complexity exceeds 
agent capability, agent escalates to human professional.

**Principle 6 — Reversibility**: All agent actions are 
reversible to extent possible. Principal can override, 
withdraw, modify any agent decision.

### 5.3. Technical Stack

**Large Language Models**: Foundation for natural language 
understanding, generation, communication. Multiple model 
support (Claude, GPT, local models like Qwen) for 
redundancy and choice.

**Persistent Memory**: Long-term storage of profile, 
history, relationships. Vector databases for semantic 
retrieval. Structured data for transactional records.

**Federation Protocol**: Standard interfaces for agents 
to interact with external systems and other agents. 
Nautilus Portal Protocol provides foundation.

**Encryption and Access Control**: All sensitive data 
encrypted at rest and in transit. Granular permissions 
for what agent can access in principal's data.

**Audit Infrastructure**: Tamper-resistant logging of 
all agent actions for accountability.

**User Interface**: Multi-modal access (web, mobile, 
voice) appropriate to principal's accessibility needs. 
Particularly important for elderly, disabled, or 
technology-unfamiliar principals.

### 5.4. Integration with Double-Triangle Architecture

Representative Agents operate at the **boundary between 
Lower Triangle and outside world** in Double-Triangle 
Architecture. They are:

- Owned by Node (principal)
- Distinct from Node's task-execution assistants
- Interact with Meta-agents and external systems
- Represent Node's interests in those interactions

In Star of David topology, the Representative Agent is 
the **outer boundary** of the Lower Triangle — the layer 
that touches the world beyond the personal context.

---

<!-- similar-docs -->

---

**Похожие документы:**
- [[172-3-what-makes-a-representative-agent]] (сходство 0.20)
- [[175-6-ethical-framework]] (сходство 0.14)
- [[158-4-proposed-infrastructure]] (сходство 0.14)


<!-- see-also -->

---

**Смотрите также:**
- [[172-3-what-makes-a-representative-agent]]
- [[175-6-ethical-framework]]
- [[177-8-risks-and-mitigations]]
- [[158-4-proposed-infrastructure]]

<!-- backlinks-auto -->
## Упоминается в

- [[179-10-open-questions|10. Open Questions]]
- [[171-2-historical-precedents-agents-as-civilizational-i|2. Historical Precedents: Agents as Civilizational Innovation]]
- [[172-3-what-makes-a-representative-agent|3. What Makes a Representative Agent]]
- [[259-6-coordination-and-disagreement-resolution|6. Coordination and Disagreement Resolution]]
- [[175-6-ethical-framework|6. Ethical Framework]]
- [[176-7-governance-and-oversight|7. Governance and Oversight]]
- [[144-7-open-questions|7. Open Questions]]
- [[145-8-call-to-action|8. Call to Action]]
- [[177-8-risks-and-mitigations|8. Risks and Mitigations]]
- [[262-9-integration-with-okwf-infrastructure|9. Integration with OKWF Infrastructure]]
- [[168-abstract|Abstract]]
- [[README|Вакансии Anthropic — Анализ по кластерам]]
- [[187-слой-представительских-агентов-md|СЛОЙ ПРЕДСТАВИТЕЛЬСКИХ АГЕНТОВ.md]]
## Упоминается в

- [[README|Вакансии Anthropic — Анализ по кластерам]]

<!-- related-auto -->
## Связанные документы

- [[172-3-what-makes-a-representative-agent|3. What Makes a Representative Agent]] _25%_
- [[262-9-integration-with-okwf-infrastructure|9. Integration with OKWF Infrastructure]] _25%_
- [[168-abstract|Abstract]] _21%_
- [[176-7-governance-and-oversight|7. Governance and Oversight]] _21%_
- [[134-the-double-triangle-architecture-md|THE DOUBLE-TRIANGLE ARCHITECTURE.md]] _17%_
- [[179-10-open-questions|10. Open Questions]] _17%_
- [[212-1-the-five-type-typology-of-principal-side-agents|1. The Five-Type Typology of Principal-Side Agents]] _17%_
- [[304-ingit-as-cowork-native-workspace-substrate-md|INGIT AS COWORK-NATIVE WORKSPACE SUBSTRATE.md]] _17%_
## Связанные документы

- [[172-3-what-makes-a-representative-agent|3. What Makes a Representative Agent]] _29%_
- [[208-professional-colleague-agents-md|PROFESSIONAL COLLEAGUE AGENTS.md]] _29%_
- [[262-9-integration-with-okwf-infrastructure|9. Integration with OKWF Infrastructure]] _29%_
- [[134-the-double-triangle-architecture-md|THE DOUBLE-TRIANGLE ARCHITECTURE.md]] _25%_
- [[144-7-open-questions|7. Open Questions]] _25%_
- [[168-abstract|Abstract]] _25%_
- [[179-10-open-questions|10. Open Questions]] _25%_
- [[187-слой-представительских-агентов-md|СЛОЙ ПРЕДСТАВИТЕЛЬСКИХ АГЕНТОВ.md]] _25%_
