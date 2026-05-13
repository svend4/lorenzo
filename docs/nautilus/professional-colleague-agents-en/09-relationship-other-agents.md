---
state: approved
---

# 9. Relationship to Other Agent Types

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — paper «Professional Colleague Agents (EN)», написанный совместно с Claude.

---

<!-- toc -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

## Содержание

- [9. Relationship to Other Agent Types](#9-relationship-to-other-agent-types)
  - [9.1. With Personal AI Assistants (Type 0)](#91-with-personal-ai-assistants-type-0)
  - [9.2. With Institutional Agents (Type 2)](#92-with-institutional-agents-type-2)
  - [9.3. With Employee Agents (Type 3)](#93-with-employee-agents-type-3)
  - [9.4. With Representative Agents (Type 4)](#94-with-representative-agents-type-4)
  - [9.5. Stack-Level View](#95-stack-level-view)

---

<!-- tags: orchestration, architecture, roadmap, anthropic, self-improvement -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — paper «Professional Colleague Agents (EN)», написанный совместно с Claude.

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

<!-- see-also -->

---

## Использование
```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "9 Relationship to Other Agent Types"
```

## Смотрите также
- [220-9-relationship-to-other-agent-types](../../02-anthropic-vacancies/220-9-relationship-to-other-agent-types.md)
- [01-five-type-typology](01-five-type-typology.md)
- [02-what-makes-pca](02-what-makes-pca.md)
- [212-1-the-five-type-typology-of-principal-side-agents](../../02-anthropic-vacancies/212-1-the-five-type-typology-of-principal-side-agents.md)


<!-- backlinks -->

---

**Кто ссылается на этот документ (9):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [00-abstract](00-abstract.md)
- [01-five-type-typology](01-five-type-typology.md)
- [02-what-makes-pca](02-what-makes-pca.md)
- [03-empirical-case-obuchay](03-empirical-case-obuchay.md)
- _...ещё 1_


<!-- similar-docs -->

---

**Похожие документы:**
- [09-relationship-other-agents](../../obsidian/nautilus/professional-colleague-agents-en/09-relationship-other-agents.md) (сходство 0.98)
- [220-9-relationship-to-other-agent-types](../../02-anthropic-vacancies/220-9-relationship-to-other-agent-types.md) (сходство 0.83)
- [220-9-relationship-to-other-agent-types](../../obsidian/02-anthropic-vacancies/220-9-relationship-to-other-agent-types.md) (сходство 0.82)

