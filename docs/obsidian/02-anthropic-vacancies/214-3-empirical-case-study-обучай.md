---
title: "3. Empirical Case Study: «Обучай»"
tags:
  - rag
  - roadmap
  - anthropic-vacancies
date: 2026-04-29
---

# 3. Empirical Case Study: «Обучай»

<!-- summary -->
> We document a successfully deployed Professional Colleague

---

<!-- toc -->
## Содержание

- [3. Empirical Case Study: «Обучай»](#3-empirical-case-study-обучай)
  - [3.1. Background](#31-background)
  - [3.2. Functional Description](#32-functional-description)
  - [3.3. Deployment Trajectory](#33-deployment-trajectory)
  - [3.4. Adoption Pattern](#34-adoption-pattern)
  - [3.5. Key Design Decisions Documented](#35-key-design-decisions-documented)
  - [3.6. Stated Philosophy](#36-stated-philosophy)
  - [3.7. Evidence of Type 1 Properties](#37-evidence-of-type-1-properties)
  - [3.8. Caveats](#38-caveats)

---

<!-- tags: rag, roadmap -->




## 3. Empirical Case Study: «Обучай»

We document a successfully deployed Professional Colleague
Agent that demonstrates this type's viability.

### 3.1. Background

«Обучай» (transliterated as "Obuchay", meaning "Teach") is a
Russian AI service for school teachers, launched in fall 2025
by Konstantin Chukavin (then 25 years old, teacher and
education enterpreneur in Petersburg) together with developer
Kirill Dyolog.

The genesis was Chukavin's own observation while teaching:
teachers spend approximately 20 unpaid hours per week on
routine tasks — preparing lesson materials, generating
assignments, grading, entering grades, managing schedule
substitutions. Much of this work is repetitive and could
plausibly be automated.

### 3.2. Functional Description

The service generates:
- Lesson plans for specific subjects, grade levels,
  difficulty levels
- Student assignments, calibrated to specific learning levels
- Images and presentations for lessons
- Tests and assessments

The agent applies:
- Federal Education Standards (ФГОС)
- Established methodological recommendations
- Knowledge of specific student levels (when teacher
  provides it)

Generated assignments are unique to the teacher's account —
they do not appear in publicly searchable form, so students
cannot find pre-existing answers.

### 3.3. Deployment Trajectory

| Date | Status |
|------|--------|
| Summer 2025 | Development begins |
| September 2025 | Public launch |
| April 2026 | 93,000 active teacher users |

Growth: zero to 93,000 users in seven months. This represents
substantial portion of Russia's teaching population (estimated
1.3 million teachers nationally; «Обучай» has reached
approximately 7% of the profession in less than one year).

### 3.4. Adoption Pattern

Chukavin reported that initial outreach to professional
networks ("Hey colleagues, try this for free") produced
**zero adoption**. First users found the service organically
through other channels.

This is consistent with general technology adoption patterns:
peer-recommended tools spread faster than self-promoted tools.
Once organic adopters created credibility, growth accelerated.

### 3.5. Key Design Decisions Documented

From publicly available information:

**Design choice 1**: Generate, do not publish. Materials live
in teacher's personal account, not in a public database.

This serves two purposes: (a) prevents student gaming
(searching for AI-generated answers online), (b) preserves
teacher authority over their materials.

**Design choice 2**: Apply standards, do not impose them.
Teacher specifies subject, grade, level. Agent applies
relevant ФГОС but does not force teacher into rigid template.

**Design choice 3**: One-click integration with existing
workflow. Roadmap goal: teacher's annual planning interface
with one-click generation of materials directly into the
school grading journal.

This treats the agent as part of the workflow, not a
separate tool to switch into.

### 3.6. Stated Philosophy

Chukavin's framing in interview is significant: "Teachers
who delegate routine tasks regain energy to actually feel
love for the profession, inspiration. To enter into
communication with students, to be for them not merely
someone who reads presentations, gives assignments and
grades."

The intended effect is **not** to reduce teacher labor in a
zero-sum sense. It is to **reallocate** teacher labor from
routine to relational. The agent automates the bureaucratic
work; the teacher invests freed time in actual pedagogy.

This reflects a sophisticated understanding of professional
work: the value-creating components are different from the
volume-occupying components. Automating the latter enables
the former.

### 3.7. Evidence of Type 1 Properties

«Обучай» exhibits all six defining Professional Colleague
Agent properties:

1. **Embedded professional context**: Yes (ФГОС, methodologies)
2. **Single-profession specialization**: Yes (teachers only)
3. **Augmentation not replacement**: Yes (teacher remains
   responsible for class)
4. **No external communications**: Yes (does not contact
   students or parents directly)
5. **Mass replication**: Yes (same product for all 93,000+
   teachers)
6. **Recognition of burden**: Yes (addresses 20 hours/week
   pain point teachers themselves identified)

This is a **clean instance** of the type. We can use it as
reference implementation for understanding the category.

### 3.8. Caveats

«Обучай» also illustrates the category's risks. Several
commenters publicly noted: "Students do homework with AI,
teachers generate assignments with AI. Schools can be
closed for lack of need."

This is a real risk we address in Section 6.

The service's broader societal impact is unproven. Whether
it actually improves education or merely accelerates a
bureaucratic process while leaving education quality
unchanged remains to be measured.

---

<!-- similar-docs -->

---

**Похожие документы:**
- [[213-2-what-makes-a-professional-colleague-agent]] (сходство 0.16)
- [[217-6-risks-specific-to-this-category]] (сходство 0.12)
- [[219-8-pilot-proposal-sgb-advocate-colleague]] (сходство 0.12)


<!-- see-also -->

---

**Смотрите также:**
- [[213-2-what-makes-a-professional-colleague-agent]]
- [[219-8-pilot-proposal-sgb-advocate-colleague]]
- [[217-6-risks-specific-to-this-category]]
- [[220-9-relationship-to-other-agent-types]]

<!-- backlinks-auto -->
## Упоминается в

- [[README|Вакансии Anthropic — Анализ по кластерам]]

<!-- related-auto -->
## Связанные документы

- [[211-table-of-contents|Table of Contents]] _29%_
- [[213-2-what-makes-a-professional-colleague-agent|2. What Makes a Professional Colleague Agent]] _25%_
- [[215-4-architecture-of-professional-colleague-agents|4. Architecture of Professional Colleague Agents]] _25%_
- [[252-abstract|Abstract]] _25%_
- [[210-abstract|Abstract]] _21%_
- [[212-1-the-five-type-typology-of-principal-side-agents|1. The Five-Type Typology of Principal-Side Agents]] _21%_
- [[217-6-risks-specific-to-this-category|6. Risks Specific to this Category]] _21%_
- [[219-8-pilot-proposal-sgb-advocate-colleague|8. Pilot Proposal: SGB Advocate Colleague]] _21%_
