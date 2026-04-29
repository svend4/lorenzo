# 1. Why Single-Triangle Models Are Incomplete

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — paper «The Double-Triangle Architecture for Human-AI Collaboration».

---
<!-- tags: architecture, anthropic -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — paper «The Double-Triangle Architecture for Human-AI Collaboration».

## 1. Why Single-Triangle Models Are Incomplete

### 1.1. The Current Landscape

The AI-assisted knowledge work field currently divides into two 
non-overlapping camps, each implementing only one triangle of the 
full architecture.

**Lower-triangle-only systems.** Personal AI assistants 
(GitHub Copilot, Cursor, Claude Code, ChatGPT, Anthropic's Claude 
Desktop) operate as extensions of individual knowledge workers. 
The human conducts, assistants execute. This paradigm has rapidly 
matured over 2023–2026 and is now mainstream. It answers: **how 
does one person amplify their capacity with AI?**

**Upper-triangle-only systems.** Multi-agent frameworks (CrewAI, 
AutoGen, LangGraph, MetaGPT, ChatDev) orchestrate multiple AI 
agents to complete complex tasks. Humans either serve as external 
observers or are absent from the execution loop. This paradigm 
answers: **how do we automate entire workflows with AI?**

Enterprise AI platforms (Microsoft Copilot Enterprise, Google 
Workspace AI) attempt to bridge these but do so through **layer 
isolation** — personal assistants and team-level orchestration 
exist as separate products without formal protocols between them.

### 1.2. What Both Paradigms Miss

Both single-triangle approaches share a structural blind spot: 
they assume humans exist in one role at a time. In reality, 
**every knowledge worker simultaneously occupies both positions**:

- A software engineer uses Copilot to write code (lower triangle: 
human conducts assistant)
- At the same time, their team lead coordinates the engineer 
alongside five others toward a sprint goal (upper triangle: 
meta-agent coordinates human)

The engineer's decisions about **what** Copilot generates depend 
on the sprint context (coming from upper triangle). The team 
lead's decisions about **how** to coordinate the engineer depend 
on what Copilot is producing (coming from lower triangle). These 
two flows of information must be connected, yet in existing 
systems they are not.

This creates what we call the **coordination gap**: personal AI 
assistants don't know about team context, and team-level 
coordination tools don't know about assistant-generated artifacts. 
Information has to be manually translated by humans across this 
gap, constantly.

### 1.3. The Rising Urgency

As AI assistants become more capable, the coordination gap widens. 
When Copilot produced autocomplete in 2022, misalignment with team 
context was minor. When Claude Code produces entire modules in 
2026, misalignment can destabilize architectural decisions across 
a team.

The gap needs to be closed not through yet another centralized 
platform, but through a **protocol** — a way for the two triangles 
to negotiate through well-defined interfaces. This paper proposes 
such a protocol.

---

<!-- see-also -->

---

**Смотрите также:**
- [138-1-why-single-triangle-models-are-incomplete](docs/02-anthropic-vacancies/138-1-why-single-triangle-models-are-incomplete.md)
- [03-three-inter-layer-protocols](docs/nautilus/double-triangle-architecture/03-three-inter-layer-protocols.md)
- [136-abstract](docs/02-anthropic-vacancies/136-abstract.md)
- [02-double-triangle-architecture](docs/nautilus/double-triangle-architecture/02-double-triangle-architecture.md)

