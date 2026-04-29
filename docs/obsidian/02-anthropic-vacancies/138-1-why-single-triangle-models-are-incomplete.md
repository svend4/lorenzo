---
title: "1. Why Single-Triangle Models Are Incomplete"
tags:
  - architecture
  - anthropic
  - anthropic-vacancies
date: 2026-04-29
---

# 1. Why Single-Triangle Models Are Incomplete

<!-- toc -->
## Содержание

- [Contents](#contents)
- [1. Why Single-Triangle Models Are Incomplete](#1-why-single-triangle-models-are-incomplete)
  - [1.1. The Current Landscape](#11-the-current-landscape)
  - [1.2. What Both Paradigms Miss](#12-what-both-paradigms-miss)
  - [1.3. The Rising Urgency](#13-the-rising-urgency)

---


<!-- abstract-auto -->
> **Абстракт** (авто)
>
> 🎯 **Проблема:** The gap needs to be closed not through yet another centralized platform, but through a protocol — a way for the two triangles to negotiate through well-defined interfaces.
> 🔧 **Подход:** What Both Paradigms Miss Both single-triangle approaches share a structural blind spot: they assume humans exist in one role at a time.
> 🏷️ **Ключевые слова:** `triangle`, `anthropic`, `vacancies`, `architecture`, `copilot`, `single`, `assistants`, `layer`
>


<!-- toc-auto -->
## Contents

- [1. Why Single-Triangle Models Are Incomplete](#1-why-single-triangle-models-are-incomplete)
  - [1.1. The Current Landscape](#11-the-current-landscape)
  - [1.2. What Both Paradigms Miss](#12-what-both-paradigms-miss)
  - [1.3. The Rising Urgency](#13-the-rising-urgency)


<!-- summary -->
> The AI-assisted knowledge work field currently divides into two

---
<!-- tags: architecture, anthropic -->




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
[[01-интегральный-анализ-профиля-svend4|AutoGen]], LangGraph, MetaGPT, ChatDev) orchestrate multiple AI 
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

<!-- similar-docs -->

---

**Похожие документы:**
- [[136-abstract]] (сходство 0.19)
- [[140-3-three-inter-layer-protocols]] (сходство 0.18)
- [[139-2-the-double-triangle-architecture]] (сходство 0.14)


<!-- see-also -->

---

**Смотрите также:**
- [[136-abstract]]
- [[140-3-three-inter-layer-protocols]]
- [[139-2-the-double-triangle-architecture]]
- [[142-5-pattern-library-as-bridge-between-triangles]]

