# 3. Three Inter-Layer Protocols

<!-- summary -->
> The architecture requires three formalized protocols between layers.

---

<!-- toc -->
## Содержание

- [3. Three Inter-Layer Protocols](#3-three-inter-layer-protocols)
  - [3.1. Protocol 1 — Human Conducts Assistants](#31-protocol-1-human-conducts-assistants)
  - [3.2. Protocol 2 — Meta-Agent Coordinates Nodes](#32-protocol-2-meta-agent-coordinates-nodes)
  - [3.3. Protocol 3 — Assistant-to-Meta Negotiation](#33-protocol-3-assistant-to-meta-negotiation)
  - [3.4. Protocol Interactions](#34-protocol-interactions)

---

<!-- tags: rag, orchestration, architecture, anthropic, self-improvement -->




## 3. Three Inter-Layer Protocols

The architecture requires three formalized protocols between layers. 
Each has specific semantics, message formats, and failure modes.

### 3.1. Protocol 1 — Human Conducts Assistants

**Direction:** Node → Assistants (downward in lower triangle)

**Semantics.** The Node issues tasks to assistants, reviews 
outputs, integrates results. This is the current state of 
personal AI assistant workflows and is well-developed.

**Existing implementations:** Claude Code, Cursor, Copilot 
Workspace, Continue.dev, ChatGPT in IDE plugins.

**Message format.** Natural language prompts with structured 
context (file references, code selections, project files). 
Responses as text, code, or structured data.

**Failure modes:** Ambiguous prompts, context overflow, 
hallucinations. These are well-studied and mitigation strategies 
exist.

**Extensions needed for Double-Triangle:** Assistants must be 
aware of *team context markers* — annotations indicating which 
parts of their output affect team-visible deliverables versus 
purely personal work. This allows invariant 2 (Assistant Autonomy, 
Node Authority) to be enforced.

### 3.2. Protocol 2 — Meta-Agent Coordinates Nodes

**Direction:** Meta-agent M → Nodes (downward in upper triangle)

**Semantics.** M assigns tasks to Nodes, receives deliverables, 
integrates team-level outputs. M does not see internal Node 
processes, only public deliverables.

**Existing implementations:** Partial, fragmented. Jira with AI 
triage, Linear with AI suggestions, GitHub Projects with 
automation. None implement the full protocol, all require 
significant human management intervention.

**Message format.** Structured tasks with:
- Description
- Deliverable specification (what constitutes "done")
- Dependencies on other Nodes' deliverables
- Deadline
- Priority
- Assignee

**Failure modes:** Task assignment mismatches (wrong Node, wrong 
skill), deadline conflicts, scope creep, dependency deadlocks. 
These are classical project management challenges adapted to AI 
orchestration.

**Extensions needed for Double-Triangle:** M must respect 
invariant 3 (Meta-Agent Transparency, Not Omniscience) — decisions 
must cite only team-context reasoning, never reference Nodes' 
personal data. Requires careful design to prevent information leakage.

### 3.3. Protocol 3 — Assistant-to-Meta Negotiation

**Direction:** Assistant A of Node N → Meta-agent M (upward across triangles)

**Semantics.** This is the **novel protocol**. When an assistant 
in N's lower triangle requires information or coordination that 
involves other Nodes, it does not ping those Nodes directly. 
Instead, it issues a structured query that travels: A → N → M → 
N' → A' → response back through the chain.

**Existing implementations:** None in production systems. Closest 
analog: GitHub Copilot Workspace can see other team members' 
public code but cannot negotiate with their assistants. 
Anthropic's Managed Agents API moves toward this but does not 
implement full cross-triangle negotiation.

**Message format.** Three message types:

- **Query messages:** "Assistant requires information X; X is 
  outside current Node's scope; routing request via meta-agent"
- **Notification messages:** "Assistant detected conflict with 
  team context; escalating to meta-agent for resolution"  
- **Proposal messages:** "Assistant proposes decision D affecting 
  multiple Nodes; requesting meta-agent consensus routing"

**Routing semantics.** Messages are routed by the meta-agent 
based on:
- Ownership: which Node owns the relevant artifact
- Expertise: which Node has the required domain knowledge
- Availability: which Node is currently responsive

**Failure modes:** Routing loops, context fragmentation (details 
lost in translation), escalation spirals where every conflict 
reaches human review. These are genuinely unsolved and require 
empirical development.

**Why this protocol matters.** Without Protocol 3, humans become 
routing bottlenecks. Every cross-Node coordination requires 
humans to manually translate from their assistants' findings to 
team context, wait for replies, translate back. This adds hours 
or days to each interaction. Protocol 3 reduces this to minutes 
or seconds.

### 3.4. Protocol Interactions

The three protocols do not operate in isolation. Common interaction 
patterns include:

**Escalation chain.** Assistant detects issue (Protocol 3 → M) → 
M evaluates (internal) → M modifies task assignment (Protocol 2) 
→ Node receives updated task (Protocol 2) → Node redirects 
assistant (Protocol 1).

**Context propagation.** M updates team context (Protocol 2 to all 
Nodes) → Each Node propagates relevant updates to their assistants 
(Protocol 1) → Assistants adjust behavior accordingly.

**Cross-Node handoff.** Assistant of N_1 completes artifact 
(Protocol 1) → Node N_1 reviews and approves (Protocol 1) → N_1 
submits to M (Protocol 2) → M routes to N_2 (Protocol 2) → N_2's 
assistant picks up (Protocol 1).

These patterns are analogous to message-passing concurrency models 
in distributed systems, adapted for human-AI hybrid execution.

---

<!-- similar-docs -->

---

**Похожие документы:**
- [138-1-why-single-triangle-models-are-incomplete](docs/02-anthropic-vacancies/138-1-why-single-triangle-models-are-incomplete.md) (сходство 0.18)
- [139-2-the-double-triangle-architecture](docs/02-anthropic-vacancies/139-2-the-double-triangle-architecture.md) (сходство 0.17)
- [144-7-open-questions](docs/02-anthropic-vacancies/144-7-open-questions.md) (сходство 0.15)

