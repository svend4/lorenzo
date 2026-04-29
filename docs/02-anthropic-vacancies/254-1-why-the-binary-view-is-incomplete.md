# 1. Why the Binary View Is Incomplete

<!-- summary -->
> Professional Colleague Agents (PCA) v1.0 introduced five types

---

<!-- toc -->
## Содержание

- [1. Why the Binary View Is Incomplete](#1-why-the-binary-view-is-incomplete)
  - [1.1. The Problem with the Existing Taxonomy](#11-the-problem-with-the-existing-taxonomy)
  - [1.2. How Mastery Actually Develops](#12-how-mastery-actually-develops)
  - [1.3. The Architecture That Should Match](#13-the-architecture-that-should-match)
  - [1.4. Why This Was Not Recognized Earlier](#14-why-this-was-not-recognized-earlier)

---

<!-- tags: ingestion, architecture, roadmap -->




## 1. Why the Binary View Is Incomplete

### 1.1. The Problem with the Existing Taxonomy

Professional Colleague Agents (PCA) v1.0 introduced five types 
of principal-side agents. Of these, Type 1 (Professional 
Colleague Agent) and Type 4 (Representative Agent) anchor the 
extremes of specialization:

**Type 1**: One agent design serves all practitioners of a 
profession. The teaching agent serves all teachers. The legal 
agent for social law serves all social law lawyers.

**Type 4**: One agent serves one principal, with deep individual 
specialization to that person's life and career.

The taxonomy treats these as endpoints of a spectrum but does 
not develop the spectrum itself. The implicit suggestion is 
that practitioners either need profession-wide standardization 
(Type 1) or individual-unique representation (Type 4).

This binary view fails to describe how mastery actually develops 
in skilled work.

### 1.2. How Mastery Actually Develops

Skilled practitioners in any sufficiently complex profession 
typically exhibit two characteristics simultaneously:

**They share a profession.** A musician is a musician. A lawyer 
is a lawyer. The profession provides a shared foundation, 
common vocabulary, baseline competencies, recognized credentials.

**They are differentiated within the profession.** No two 
musicians are identical. No two lawyers practice exactly the 
same way. Each combines particular specializations, particular 
influences, particular emphases that make their work distinctive.

This second characteristic is not exceptional but typical. It 
is **how professions actually contain their members**. The 
profession provides the genus; specialization provides the 
species; combination provides the individual instance.

Importantly, the differentiation usually comes not from 
inventing entirely novel skills but from **specific combinations 
of generally available skills**. A jazz pianist who also studied 
classical composition and has expertise in audio engineering 
is differentiated not because any of those skills is unique 
to her, but because the **combination** is rare.

### 1.3. The Architecture That Should Match

If mastery typically combines individually-general specializations 
into individually-uncommon configurations, then the AI 
infrastructure supporting mastery should match this structure.

A Type 1 agent (one shape fits all teachers) leaves out the 
specialization. A Type 4 agent (uniquely built for one teacher) 
duplicates work that could be shared.

Neither matches the actual structure of skilled practice.

What matches is an architecture where:
- Many narrow-specialist sub-agents exist, each built once
- Sub-agents are shared across all practitioners who need that 
  specialization
- Each principal configures their **own combination** of relevant 
  sub-agents
- A coordinating layer presents this combination as a coherent 
  composite agent

This is the **Composite Skills Agent** pattern.

### 1.4. Why This Was Not Recognized Earlier

The Composite Skills Agent pattern emerges naturally once the 
question is asked: "What about practitioners whose distinctive 
value comes from combining specializations?" But this question 
was not asked in earlier papers because the framing was 
profession-centric (Type 1) or individual-centric (Type 4) 
without explicit attention to the most common middle ground.

This mirrors a common pattern in technology architecture: the 
extremes get attention because they are conceptually clean; 
the middle gets neglected because it is messier. Yet the middle 
is where most actual practice happens.

Recognizing the Composite Skills Agent pattern is not a minor 
extension. It changes the practical strategy for deploying AI 
support to skilled professions.

---

<!-- similar-docs -->

---

**Похожие документы:**
- [252-abstract](252-abstract.md) (сходство 0.25)
- [266-13-closing](266-13-closing.md) (сходство 0.20)
- [255-2-the-twenty-one-teachers-pattern](255-2-the-twenty-one-teachers-pattern.md) (сходство 0.18)


<!-- see-also -->

---

**Смотрите также:**
- [252-abstract](252-abstract.md)
- [266-13-closing](266-13-closing.md)
- [255-2-the-twenty-one-teachers-pattern](255-2-the-twenty-one-teachers-pattern.md)
- [256-3-what-makes-a-composite-skills-agent](256-3-what-makes-a-composite-skills-agent.md)

<!-- backlinks-auto -->
## Упоминается в

- [10. Open Questions](221-10-open-questions.md)
- [13. Closing](266-13-closing.md)
- [2. Historical Precedents: Agents as Civilizational Innovation](171-2-historical-precedents-agents-as-civilizational-i.md)
- [2. The Twenty-One Teachers Pattern](255-2-the-twenty-one-teachers-pattern.md)
- [3. What Makes a Composite Skills Agent](256-3-what-makes-a-composite-skills-agent.md)
- [7. Economics of Combinatorial Replication](260-7-economics-of-combinatorial-replication.md)
- [8. Seven Domains of Application](261-8-seven-domains-of-application.md)
- [9. Integration with OKWF Infrastructure](262-9-integration-with-okwf-infrastructure.md)
- [Abstract](252-abstract.md)
- [Table of Contents](253-table-of-contents.md)
- [Вакансии Anthropic — Анализ по кластерам](README.md)
## Упоминается в

- [Вакансии Anthropic — Анализ по кластерам](../README.md)

<!-- related-auto -->
## Связанные документы

- [Abstract](252-abstract.md) _48%_
- [Table of Contents](253-table-of-contents.md) _33%_
- [2. The Twenty-One Teachers Pattern](255-2-the-twenty-one-teachers-pattern.md) _33%_
- [13. Closing](266-13-closing.md) _25%_
- [THE DOUBLE-TRIANGLE ARCHITECTURE.md](134-the-double-triangle-architecture-md.md) _21%_
- [Abstract](210-abstract.md) _21%_
- [1. The Five-Type Typology of Principal-Side Agents](212-1-the-five-type-typology-of-principal-side-agents.md) _21%_
- [3. Empirical Case Study: «Обучай»](214-3-empirical-case-study-обучай.md) _21%_
## Связанные документы

- [Abstract](252-abstract.md) _42%_
- [Table of Contents](253-table-of-contents.md) _33%_
- [9. Integration with OKWF Infrastructure](262-9-integration-with-okwf-infrastructure.md) _33%_
- [PROFESSIONAL COLLEAGUE AGENTS.md](208-professional-colleague-agents-md.md) _25%_
- [1. The Five-Type Typology of Principal-Side Agents](212-1-the-five-type-typology-of-principal-side-agents.md) _25%_
- [2. The Twenty-One Teachers Pattern](255-2-the-twenty-one-teachers-pattern.md) _25%_
- [3. What Makes a Composite Skills Agent](256-3-what-makes-a-composite-skills-agent.md) _25%_
- [6. Coordination and Disagreement Resolution](259-6-coordination-and-disagreement-resolution.md) _25%_
