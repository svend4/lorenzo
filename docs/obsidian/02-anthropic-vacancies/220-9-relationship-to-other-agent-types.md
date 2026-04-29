---
title: "9. Relationship to Other Agent Types"
tags:
  - anthropic-vacancies
date: 2026-04-29
---

# 9. Relationship to Other Agent Types

<!-- abstract-auto -->
> **Абстракт** (авто)
>
> 🎯 **Проблема:** Integration challenge: Layer C (interface layer) of Type 1 needs to talk to Type 2 systems.
> 🔧 **Подход:** This sequencing differs from what Representative Agent Layer paper proposed.
> ✅ **Результат:** Distinguishing them enables clear architecture.
> 🏷️ **Ключевые слова:** `agent`, `professional`, `agents`, `colleague`, `relationship`, `representative`, `practitioner`, `institutional`
>


<!-- summary -->
> Professional Colleague Agents do not stand alone. They

---

<!-- toc -->
## Содержание

- [9. Relationship to Other Agent Types](#9-relationship-to-other-agent-types)
  - [9.1. With Personal AI Assistants (Type 0)](#91-with-personal-ai-assistants-type-0)
  - [9.2. With Institutional Agents (Type 2)](#92-with-institutional-agents-type-2)
  - [9.3. With Employee Agents (Type 3)](#93-with-employee-agents-type-3)
  - [9.4. With Representative Agents (Type 4)](#94-with-representative-agents-type-4)
  - [9.5. Stack-Level View](#95-stack-level-view)

---

<!-- tags: orchestration, architecture, roadmap, self-improvement -->




## 9. Relationship to Other Agent Types

Professional Colleague Agents do not stand alone. They
integrate with the broader agent stack on the principal side.

### 9.1. With Personal AI Assistants (Type 0)

**Relationship**: Complementary. Personal AI Assistants handle
general tasks (writing emails, scheduling, brainstorming).
Professional Colleague Agents handle profession-specific tasks.

**Integration**: A practitioner uses both. ChatGPT for general
writing assistance. Professional Colleague Agent for
profession-specific work. Different tools for different
contexts.

**Risk**: Confusion about when to use which. Mitigated by
clear positioning: Professional Colleague Agent has the
professional context; Personal AI Assistant does not.

### 9.2. With Institutional Agents (Type 2)

**Relationship**: Professional Colleague Agent typically feeds
outputs into Institutional Agent. Teacher generates lesson
plan with Professional Colleague (Type 1), then exports to
school's grading system (Type 2).

**Integration challenge**: Layer C (interface layer) of Type
1 needs to talk to Type 2 systems. This is significant
engineering work and varies by institution.

**Architectural implication**: Open APIs and standard formats
critical. Otherwise each institutional integration becomes
custom work.

### 9.3. With Employee Agents (Type 3)

**Relationship**: Practitioner may delegate specific zones
of authority to Employee Agents while using Professional
Colleague for direct work. Teacher uses Professional Colleague
for lesson plan generation; Employee Agent handles routine
parent emails autonomously.

**Boundary issue**: When does helping (Type 1) become acting
(Type 3)? Lawyer using agent for drafting is Type 1. Lawyer
authorizing agent to file routine motions automatically would
be Type 3.

The line is consequential. Type 1 has minimal regulatory
concerns. Type 3 raises substantial questions about
professional licensure and authority.

**Practical recommendation**: Maintain clear distinction.
Type 1 first; Type 3 carefully and only after professional
and regulatory frameworks adapt.

### 9.4. With Representative Agents (Type 4)

**Relationship**: Different functions, complementary deployment.
Professional Colleague serves practitioner's daily work.
Representative Agent serves practitioner's career and market
position.

**Sequencing**: Professional Colleague Agents are higher-readiness
for deployment. They should precede Representative Agent
deployment in any practitioner's adoption journey. By the
time practitioners are comfortable with Type 1, they are
better prepared to evaluate Type 4.

**For OKWF specifically**: Deploy Professional Colleague
Agents in Phase 1. Add Representative Agent Layer in Phase
2-3, after practitioners and infrastructure are mature.

This sequencing differs from what Representative Agent Layer
paper proposed. Reflection on the «Обучай» case suggests
Type 1 is better starting point — both because it's more
deployable and because it builds the trust base necessary
for Type 4.

### 9.5. Stack-Level View

A mature deployment for a practitioner has all five types
simultaneously:

**Type 0** (Personal AI Assistant): General computing
assistance for non-professional tasks.

**Type 1** (Professional Colleague Agent): Embedded in daily
professional work.

**Type 2** (Institutional Agent): Bridges practitioner work
to institutional systems.

**Type 3** (Employee Agent): Handles delegated automated
tasks within professional zones.

**Type 4** (Representative Agent): Manages practitioner's
external position and opportunities.

Each is built differently. Each has different stakeholders.
Each requires different governance. Conflating them produces
confusion. Distinguishing them enables clear architecture.

---

<!-- similar-docs -->

---

**Похожие документы:**
- [[212-1-the-five-type-typology-of-principal-side-agents]] (сходство 0.18)
- [[210-abstract]] (сходство 0.17)
- [[223-12-closing]] (сходство 0.17)


<!-- see-also -->

---

**Смотрите также:**
- [[210-abstract]]
- [[212-1-the-five-type-typology-of-principal-side-agents]]
- [[223-12-closing]]
- [[213-2-what-makes-a-professional-colleague-agent]]

<!-- backlinks-auto -->
## Упоминается в

- [[212-1-the-five-type-typology-of-principal-side-agents|1. The Five-Type Typology of Principal-Side Agents]]
- [[223-12-closing|12. Closing]]
- [[213-2-what-makes-a-professional-colleague-agent|2. What Makes a Professional Colleague Agent]]
- [[214-3-empirical-case-study-обучай|3. Empirical Case Study: «Обучай»]]
- [[172-3-what-makes-a-representative-agent|3. What Makes a Representative Agent]]
- [[210-abstract|Abstract]]
- [[226-appendix-a-comparative-table-five-agent-types|Appendix A: Comparative Table — Five Agent Types]]
- [[269-appendix-a-the-six-type-taxonomy-updated|Appendix A: The Six-Type Taxonomy (Updated)]]
- [[227-appendix-b-decision-framework-when-to-build-type-1|Appendix B: Decision Framework — When to Build Type 1 First]]
- [[228-appendix-c-quick-start-architecture-for-sgb-advoca|Appendix C: Quick-Start Architecture for SGB Advocate Colleague]]
- [[211-table-of-contents|Table of Contents]]
- [[README|Вакансии Anthropic — Анализ по кластерам]]
- [[345-кто-ты|Кто ты]]
## Упоминается в

- [[README|Вакансии Anthropic — Анализ по кластерам]]

<!-- related-auto -->
## Связанные документы

- [[210-abstract|Abstract]] _53%_
- [[213-2-what-makes-a-professional-colleague-agent|2. What Makes a Professional Colleague Agent]] _53%_
- [[211-table-of-contents|Table of Contents]] _42%_
- [[212-1-the-five-type-typology-of-principal-side-agents|1. The Five-Type Typology of Principal-Side Agents]] _42%_
- [[223-12-closing|12. Closing]] _42%_
- [[227-appendix-b-decision-framework-when-to-build-type-1|Appendix B: Decision Framework — When to Build Type 1 First]] _37%_
- [[172-3-what-makes-a-representative-agent|3. What Makes a Representative Agent]] _29%_
- [[226-appendix-a-comparative-table-five-agent-types|Appendix A: Comparative Table — Five Agent Types]] _29%_
## Связанные документы

- [[212-1-the-five-type-typology-of-principal-side-agents|1. The Five-Type Typology of Principal-Side Agents]] _53%_
- [[213-2-what-makes-a-professional-colleague-agent|2. What Makes a Professional Colleague Agent]] _42%_
- [[210-abstract|Abstract]] _37%_
- [[211-table-of-contents|Table of Contents]] _37%_
- [[172-3-what-makes-a-representative-agent|3. What Makes a Representative Agent]] _33%_
- [[223-12-closing|12. Closing]] _33%_
- [[226-appendix-a-comparative-table-five-agent-types|Appendix A: Comparative Table — Five Agent Types]] _29%_
- [[227-appendix-b-decision-framework-when-to-build-type-1|Appendix B: Decision Framework — When to Build Type 1 First]] _29%_
