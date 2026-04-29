---
title: "1. Why the Binary View Is Incomplete"
tags:
  - ingestion
  - architecture
  - roadmap
  - anthropic-vacancies
date: 2026-04-29
---

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
- [[252-abstract]] (сходство 0.25)
- [[266-13-closing]] (сходство 0.20)
- [[255-2-the-twenty-one-teachers-pattern]] (сходство 0.18)


<!-- see-also -->

---

**Смотрите также:**
- [[252-abstract]]
- [[266-13-closing]]
- [[255-2-the-twenty-one-teachers-pattern]]
- [[256-3-what-makes-a-composite-skills-agent]]

<!-- backlinks-auto -->
## Упоминается в

- [[README|Вакансии Anthropic — Анализ по кластерам]]

<!-- related-auto -->
## Связанные документы

- [[252-abstract|Abstract]] _42%_
- [[253-table-of-contents|Table of Contents]] _33%_
- [[262-9-integration-with-okwf-infrastructure|9. Integration with OKWF Infrastructure]] _33%_
- [[208-professional-colleague-agents-md|PROFESSIONAL COLLEAGUE AGENTS.md]] _25%_
- [[212-1-the-five-type-typology-of-principal-side-agents|1. The Five-Type Typology of Principal-Side Agents]] _25%_
- [[255-2-the-twenty-one-teachers-pattern|2. The Twenty-One Teachers Pattern]] _25%_
- [[256-3-what-makes-a-composite-skills-agent|3. What Makes a Composite Skills Agent]] _25%_
- [[259-6-coordination-and-disagreement-resolution|6. Coordination and Disagreement Resolution]] _25%_
