# 1. The Five-Type Typology of Principal-Side Agents

<!-- abstract-auto -->
> **Абстракт** (авто)
>
> 🎯 **Проблема:** A single human professional could simultaneously have: Personal AI Assistants (Type 0) do not occupy a fixed layer — they function across all layers as utility, used as needed.
> 🔧 **Подход:** Embeds professional knowledge (norms, methodologies, regulations, templates) so that practitioners do not have to re-explain their context.
> 🏷️ **Ключевые слова:** `agent`, `agents`, `principal`, `professional`, `types`, `institutional`, `representative`, `anthropic`
>


<!-- summary -->
> The Representative Agent Layer paper introduced one type of AI

---

<!-- toc -->
## Содержание

- [1. The Five-Type Typology of Principal-Side Agents](#1-the-five-type-typology-of-principal-side-agents)
  - [1.1. Type 0 — Personal AI Assistants](#11-type-0-personal-ai-assistants)
  - [1.2. Type 1 — Professional Colleague Agents](#12-type-1-professional-colleague-agents)
  - [1.3. Type 2 — Institutional Agents](#13-type-2-institutional-agents)
  - [1.4. Type 3 — Employee Agents](#14-type-3-employee-agents)
  - [1.5. Type 4 — Representative Agents](#15-type-4-representative-agents)
  - [1.6. Layered Architecture on the Principal Side](#16-layered-architecture-on-the-principal-side)
  - [1.7. Why This Distinction Matters](#17-why-this-distinction-matters)

---

<!-- tags: ingestion, architecture, anthropic -->




## 1. The Five-Type Typology of Principal-Side Agents

The Representative Agent Layer paper introduced one type of AI
agent on the principal side. In doing so, it implicitly suggested
that "AI agent serving a human" is a single category. This
formulation, on reflection, obscures important distinctions.
We now identify five distinct types.

### 1.1. Type 0 — Personal AI Assistants

**Examples**: ChatGPT, Claude, Cursor, GitHub Copilot, Claude
Code.

**Function**: General-purpose helper with whatever task the
user explicitly brings.

**Direction**: Reactive. User initiates, AI responds.

**Specialization**: None. Universal across domains.

**Persistence**: Session-based. Memory limited.

**Replication**: One product serves all users.

**State of art**: Mature. Mass-deployed. Hundreds of millions
of users.

### 1.2. Type 1 — Professional Colleague Agents

**Examples**: «Обучай» (teachers), specialized medical AI
assistants, parajural AI tools, teacher-specific tutoring AI.

**Function**: Helper specialized for a specific profession.
Embeds professional knowledge (norms, methodologies, regulations,
templates) so that practitioners do not have to re-explain
their context.

**Direction**: Reactive within professional context.
Practitioner sets task; agent applies professional knowledge.

**Specialization**: Deep, single profession.

**Persistence**: Professional context persists across sessions.
User's specific work-in-progress may persist.

**Replication**: One product serves all practitioners of the
profession (millions of teachers, hundreds of thousands of
medical professionals, etc.).

**State of art**: Emerging. First successful examples like
«Обучай» exist. Mass deployment beginning.

### 1.3. Type 2 — Institutional Agents

**Examples**: AI integrated with school grading systems, court
filing systems, hospital electronic records, government benefit
processing.

**Function**: Embedded in institutional infrastructure. Serves
both the institution and the human practitioner. Bridges
between individual work and institutional records.

**Direction**: Bidirectional. Institutional rules constrain;
human work flows into institutional records.

**Specialization**: Both professional and institutional.

**Persistence**: Institutional. Records and decisions persist
in institutional memory.

**Replication**: One per institution-type, often customized
per institution.

**State of art**: Early. Some healthcare systems experimenting.
Major regulatory questions unresolved.

### 1.4. Type 3 — Employee Agents

**Examples**: AI handling routine email correspondence
autonomously. AI conducting initial student examinations. AI
processing standard insurance claims. AI making first-pass
hiring screening decisions.

**Function**: Operates within delegated scope of authority,
making decisions and taking actions independently. Reports
results to human supervisor.

**Direction**: Autonomous within delegation. Human sets scope;
AI executes within it.

**Specialization**: Specific task within a profession.

**Persistence**: Operational. Continuous activity within
scope.

**Replication**: Per-task replication.

**State of art**: Beginning. Significant ethical and regulatory
challenges. Examples exist but controversial.

### 1.5. Type 4 — Representative Agents

**Examples**: None in production. Proposed in Representative
Agent Layer paper.

**Function**: Represents principal externally — discovers
opportunities, manages presentation, conducts negotiations,
protects from harm.

**Direction**: Outward-facing. AI engages with world on
behalf of principal.

**Specialization**: Deep individual specialization. Each
principal has unique agent.

**Persistence**: Long-term. Models principal's life arc.

**Replication**: One per principal.

**State of art**: Conceptual. Architecture proposed, no
production deployment.

### 1.6. Layered Architecture on the Principal Side

These five types form a coherent **stack** on the principal
side. A single human professional could simultaneously have:

```
              [EXTERNAL WORLD]
                     ↑
             [Representative Agent]   (Type 4)
                     ↑
                [PRINCIPAL]
                     ↓
           [Professional Colleagues]  (Type 1)
                     ↓
            [Institutional Agents]    (Type 2)
                     ↓
              [Employee Agents]       (Type 3)
                     ↓
            [PROFESSIONAL WORK]
```

Personal AI Assistants (Type 0) do not occupy a fixed layer —
they function across all layers as utility, used as needed.

This typology is **not** a hierarchy of capability. Each type
serves a different function. Type 1 is not "less advanced
than" Type 4; it is "different from." A mature deployment of
AI infrastructure for professionals likely involves multiple
types operating together.

### 1.7. Why This Distinction Matters

Each type has fundamentally different characteristics:

| Property | Type 0 | Type 1 | Type 2 | Type 3 | Type 4 |
|----------|--------|--------|--------|--------|--------|
| Specialization | None | Profession | Institution+profession | Task | Individual |
| External communication | None | None | Some | Some | Extensive |
| Replicability | Universal | Per profession | Per institution | Per task | Per individual |
| Economics | Subscription | Profession-wide | Institutional | Variable | Individual |
| Ethical concerns | Low | Medium | Medium | High | Highest |
| Regulatory complexity | Low | Medium | High | Highest | Highest |
| Deployment readiness | Mature | Emerging | Early | Beginning | Conceptual |

Conflating these types in a single discussion produces
confused analysis. Each requires its own architectural,
ethical, and economic framework.

---

<!-- similar-docs -->

---

**Похожие документы:**
- [226-appendix-a-comparative-table-five-agent-types](docs/02-anthropic-vacancies/226-appendix-a-comparative-table-five-agent-types.md) (сходство 0.24)
- [220-9-relationship-to-other-agent-types](docs/02-anthropic-vacancies/220-9-relationship-to-other-agent-types.md) (сходство 0.18)
- [213-2-what-makes-a-professional-colleague-agent](docs/02-anthropic-vacancies/213-2-what-makes-a-professional-colleague-agent.md) (сходство 0.17)


<!-- see-also -->

---

**Смотрите также:**
- [226-appendix-a-comparative-table-five-agent-types](docs/02-anthropic-vacancies/226-appendix-a-comparative-table-five-agent-types.md)
- [220-9-relationship-to-other-agent-types](docs/02-anthropic-vacancies/220-9-relationship-to-other-agent-types.md)
- [213-2-what-makes-a-professional-colleague-agent](docs/02-anthropic-vacancies/213-2-what-makes-a-professional-colleague-agent.md)
- [172-3-what-makes-a-representative-agent](docs/02-anthropic-vacancies/172-3-what-makes-a-representative-agent.md)

