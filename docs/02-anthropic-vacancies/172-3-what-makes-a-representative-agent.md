# 3. What Makes a Representative Agent

<!-- abstract-auto -->
> **Абстракт** (авто)
>
> 🎯 **Проблема:** Adapting them to AI principals is a key research and design challenge addressed in Sections 6 and 7.
> 🔧 **Подход:** Adapting them to AI principals is a key research and design challenge addressed in Sections 6 and 7.
> 🏷️ **Ключевые слова:** `agent`, `principal`, `representative`, `assistants`, `makes`, `relationship`, `current`, `function`
>


<!-- summary -->
> A Representative Agent is distinct from existing AI categories.

---

<!-- toc -->
## Содержание

- [3. What Makes a Representative Agent](#3-what-makes-a-representative-agent)
  - [3.1. Three-Layer Distinction](#31-three-layer-distinction)
  - [3.2. Five Core Functions](#32-five-core-functions)
  - [3.3. What Distinguishes from Generic Personal AI Assistants](#33-what-distinguishes-from-generic-personal-ai-assistants)
  - [3.4. The Principal-Agent Relationship](#34-the-principal-agent-relationship)

---

<!-- tags: architecture -->




## 3. What Makes a Representative Agent

A Representative Agent is distinct from existing AI categories. 
We define it precisely.

### 3.1. Three-Layer Distinction

**Layer 1 — Personal AI Assistants** (current state of art):  
Examples: Cursor, Claude Code, Copilot, ChatGPT.  
Function: Help user execute tasks they've decided to do.  
Direction: User → AI ("do this for me").  
Locus of agency: User.  
Goal: Productivity multiplication on chosen tasks.

**Layer 2 — Multi-Agent Systems** (current research/prototype):  
Examples: MetaGPT, AutoGen, ChatDev, CrewAI.  
Function: AI agents collaborate among themselves to complete 
complex tasks.  
Direction: AI → AI.  
Locus of agency: System designer.  
Goal: Automation of multi-step processes.

**Layer 3 — Representative Agents** (proposed):  
Examples: None in production yet.  
Function: AI proactively represents user in markets and 
relationships.  
Direction: AI → World on behalf of user.  
Locus of agency: User delegates strategically.  
Goal: Access to opportunities user cannot reach alone.

### 3.2. Five Core Functions

A Representative Agent performs five interlocking functions:

**Function 1 — Discovery.** Continuously monitors relevant 
domains for opportunities matching the principal's profile. 
This includes: job postings, project announcements, 
collaboration requests, grant calls, regulatory deadlines, 
relationship opportunities. Acts as a **proactive scout**.

**Function 2 — Curation.** Filters discovered opportunities 
against principal's actual fit, capacity, and preferences. 
Prevents principal from being overwhelmed. Surfaces only 
high-relevance opportunities. Acts as a **filter and ranker**.

**Function 3 — Presentation.** Crafts presentations of the 
principal to relevant counterparties. This includes: 
applications, profiles, introductions, proposals. Translates 
the principal's value into language counterparties understand. 
Acts as a **translator and advocate**.

**Function 4 — Negotiation.** Engages in initial conversations 
with counterparties on behalf of the principal. Handles 
clarification, basic terms, scheduling. Surfaces complex 
decisions to the principal for human judgment. Acts as a 
**buffer and intermediary**.

**Function 5 — Protection.** Identifies risks, scams, 
exploitation, mismatched commitments. Prevents the principal 
from harm or overextension. Acts as a **gatekeeper and 
guardian**.

### 3.3. What Distinguishes from Generic Personal AI Assistants

A Representative Agent has properties that current personal 
AI assistants do not:

**Persistent operation**: Runs continuously, not session-based. 
Monitoring opportunities is 24/7 work.

**External interaction**: Communicates with parties beyond 
the principal. Most current assistants only communicate 
with the user.

**Strategic autonomy**: Makes decisions about what to surface 
to user vs. handle independently. Current assistants execute 
explicit user requests.

**Long-term relationship modeling**: Maintains models of 
principal's career arc, evolving preferences, life context. 
Current assistants have limited memory.

**Adversarial awareness**: Operates in environments where 
other parties may have conflicting interests. Current 
assistants generally assume cooperative environments.

**Mission alignment**: Operates within explicit ethical and 
strategic framework set by principal. Current assistants 
optimize for engagement or task completion.

### 3.4. The Principal-Agent Relationship

Representative Agents introduce a classic **principal-agent 
relationship** familiar from economics, law, and political 
science. The principal (the human) delegates to the agent 
(the AI). Key questions:

- What is delegated? What remains with principal?
- What constrains agent behavior?
- How does principal monitor agent?
- What recourse if agent misbehaves?

These questions have well-developed answers in human 
principal-agent contexts. Adapting them to AI principals is 
a key research and design challenge addressed in Sections 6 
and 7.

---

<!-- similar-docs -->

---

**Похожие документы:**
- [174-5-architectural-specification](docs/02-anthropic-vacancies/174-5-architectural-specification.md) (сходство 0.20)
- [212-1-the-five-type-typology-of-principal-side-agents](docs/02-anthropic-vacancies/212-1-the-five-type-typology-of-principal-side-agents.md) (сходство 0.15)
- [213-2-what-makes-a-professional-colleague-agent](docs/02-anthropic-vacancies/213-2-what-makes-a-professional-colleague-agent.md) (сходство 0.13)


<!-- see-also -->

---

**Смотрите также:**
- [174-5-architectural-specification](docs/02-anthropic-vacancies/174-5-architectural-specification.md)
- [212-1-the-five-type-typology-of-principal-side-agents](docs/02-anthropic-vacancies/212-1-the-five-type-typology-of-principal-side-agents.md)
- [213-2-what-makes-a-professional-colleague-agent](docs/02-anthropic-vacancies/213-2-what-makes-a-professional-colleague-agent.md)
- [220-9-relationship-to-other-agent-types](docs/02-anthropic-vacancies/220-9-relationship-to-other-agent-types.md)

