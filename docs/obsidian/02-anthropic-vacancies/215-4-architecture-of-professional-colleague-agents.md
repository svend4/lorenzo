---
title: "4. Architecture of Professional Colleague Agents"
tags:
  - rag
  - architecture
  - anthropic-vacancies
date: 2026-04-29
---

# 4. Architecture of Professional Colleague Agents

<!-- abstract-auto -->
> **Абстракт** (авто)
>
> 🎯 **Проблема:** Your in-progress submission may need review." The practitioner decides whether to update their work.
> 🔧 **Подход:** Encoded knowledge of the profession: standards, regulations, methodologies, templates, vocabularies, common patterns.
> ✅ **Результат:** Different LLM providers can power the same Layer A.
> 🏷️ **Ключевые слова:** `professional`, `colleague`, `agent`, `knowledge`, `practitioner`, `architecture`, `layer`, `update`
>


<!-- summary -->
> A Professional Colleague Agent has three distinct internal

---

<!-- toc -->
## Содержание

- [4. Architecture of Professional Colleague Agents](#4-architecture-of-professional-colleague-agents)
  - [4.1. Three-Layer Internal Architecture](#41-three-layer-internal-architecture)
  - [4.2. Knowledge Curation Strategies](#42-knowledge-curation-strategies)
  - [4.3. Update and Versioning](#43-update-and-versioning)
  - [4.4. Quality Assurance Architecture](#44-quality-assurance-architecture)
  - [4.5. Integration Standards](#45-integration-standards)

---

<!-- tags: rag, architecture -->




## 4. Architecture of Professional Colleague Agents

### 4.1. Three-Layer Internal Architecture

A Professional Colleague Agent has three distinct internal
layers:

**Layer A — Professional Knowledge Base.** Encoded knowledge
of the profession: standards, regulations, methodologies,
templates, vocabularies, common patterns. Curated and
maintained by professional experts (with possible AI
assistance for updates).

This is the most expensive layer to build and the most
valuable competitive moat. A high-quality professional
knowledge base for German social law, for example,
represents thousands of hours of expert curation.

**Layer B — Generation and Reasoning Engine.** The active
component: an LLM (or ensemble of LLMs) configured to operate
within Layer A. Receives practitioner input, applies
professional knowledge, generates appropriate output.

This layer is largely interchangeable. Different LLM providers
can power the same Layer A.

**Layer C — Practitioner Interface and Personalization.**
The visible application: web/mobile/desktop interface,
authentication, personal preferences, work-in-progress
storage, integration with practitioner's other tools.

Personalization here does not reach into Layer A — the
professional context is shared across all users. Personal
preferences (UI, language, notification settings, current
projects) are layered on top.

### 4.2. Knowledge Curation Strategies

Layer A — the professional knowledge base — is the heart of
a Professional Colleague Agent. Several strategies for
building and maintaining it:

**Strategy 1 — Single Expert Curator.** A senior professional
or small team curates the knowledge base. Highest quality,
limited scale. Good for early stages.

**Strategy 2 — Federation of Practitioners.** Many practitioners
contribute knowledge fragments through pattern-library mechanism.
Quality varies, scale large. Requires curation oversight.
This connects directly to the Pattern Library architecture
in Nautilus.

**Strategy 3 — Authority Integration.** Direct integration
with authoritative sources (legal databases, medical
guidelines, educational standards). Auto-update as sources
update. Most rigorous, requires legal/institutional access.

**Strategy 4 — Hybrid.** Combination of authoritative sources
(for hard rules) and practitioner-contributed patterns (for
practical applications). Most practical for complex
professions.

For most domains, Strategy 4 is realistic. The "Обучай"
service appears to use this — official ФГОС for hard rules,
practitioner-driven refinements for practical application.

### 4.3. Update and Versioning

Professional knowledge changes. Tax codes update. Medical
guidelines revise. Educational standards modify. Legal
precedent shifts.

Professional Colleague Agents must handle this without
breaking practitioner workflows. Two principles:

**Principle of Snapshot Stability.** Practitioner work-in-progress
is anchored to a specific knowledge base version. Mid-project
updates to the knowledge base do not retroactively alter
practitioner's drafts. This prevents disorientation.

**Principle of Update Awareness.** Significant knowledge base
updates are surfaced to practitioner. "The relevant statute
was amended last week. Your in-progress submission may need
review." The practitioner decides whether to update their
work.

These principles parallel software development practices
(immutable releases, deprecation notices). Professional
Colleague Agents inherit these patterns.

### 4.4. Quality Assurance Architecture

Professional outputs have consequences. A flawed legal
document, medical record, or educational assessment produces
real harm. Quality assurance must be built into the architecture.

**QA Mechanism 1 — Confidence Indicators.** The agent reports
its confidence in each output element. High confidence:
"Standard format applied per current regulation." Low
confidence: "Approach uncertain; consult specialist guidance."

**QA Mechanism 2 — Cited Sources.** Each substantive claim
the agent makes is traceable to a source in the knowledge
base. The practitioner can verify by following citations.

**QA Mechanism 3 — Practitioner Review Required.** Outputs
are drafts requiring practitioner review and acceptance, not
final products. The agent's interface should make review
natural rather than burdensome.

**QA Mechanism 4 — Error Reporting.** Practitioners encountering
errors have low-friction way to report them. Aggregated reports
inform Layer A improvements.

These mechanisms together produce the equivalent of a
careful colleague: present, helpful, traceable, fallible
but explicit about it.

### 4.5. Integration Standards

Professional Colleague Agents should integrate with:

**Standard data formats** for the profession. Legal documents
should output in standard formats (typically structured XML
for some jurisdictions, formatted PDF/DOCX otherwise).
Medical records should output in clinical standards (HL7,
FHIR). Educational materials in standard exchange formats.

**Workflow tools** the profession uses. Lawyers use specific
case management systems. Teachers use specific gradebook
systems. Doctors use specific EHR systems. Integration here
removes friction.

**Authority systems** the profession is bound to. Legal
filings to court systems. Tax submissions to government.
Educational certifications. The agent should facilitate
authority interactions, not create new parallel ones.

This integration work is significant. It is also where many
"AI for X profession" projects fail — building a beautiful
agent that no practitioner can fit into their existing
workflow.

---

<!-- similar-docs -->

---

**Похожие документы:**
- [[257-4-the-sub-agent-registry]] (сходство 0.15)
- [[217-6-risks-specific-to-this-category]] (сходство 0.15)
- [[213-2-what-makes-a-professional-colleague-agent]] (сходство 0.14)


<!-- see-also -->

---

**Смотрите также:**
- [[257-4-the-sub-agent-registry]]
- [[217-6-risks-specific-to-this-category]]
- [[213-2-what-makes-a-professional-colleague-agent]]
- [[219-8-pilot-proposal-sgb-advocate-colleague]]

<!-- backlinks-auto -->
## Упоминается в

- [[138-1-why-single-triangle-models-are-incomplete|1. Why Single-Triangle Models Are Incomplete]]
- [[221-10-open-questions|10. Open Questions]]
- [[214-3-empirical-case-study-обучай|3. Empirical Case Study: «Обучай»]]
- [[257-4-the-sub-agent-registry|4. The Sub-Agent Registry]]
- [[216-5-the-economics-of-profession-wide-replication|5. The Economics of Profession-Wide Replication]]
- [[217-6-risks-specific-to-this-category|6. Risks Specific to this Category]]
- [[219-8-pilot-proposal-sgb-advocate-colleague|8. Pilot Proposal: SGB Advocate Colleague]]
- [[228-appendix-c-quick-start-architecture-for-sgb-advoca|Appendix C: Quick-Start Architecture for SGB Advocate Colleague]]
- [[README|Вакансии Anthropic — Анализ по кластерам]]
- [[365-развёрнутый-анализ-внуковой-комбинации|Развёрнутый анализ «внуковой» комбинации]]
## Упоминается в

- [[README|Вакансии Anthropic — Анализ по кластерам]]

<!-- related-auto -->
## Связанные документы

- [[217-6-risks-specific-to-this-category|6. Risks Specific to this Category]] _42%_
- [[216-5-the-economics-of-profession-wide-replication|5. The Economics of Profession-Wide Replication]] _29%_
- [[228-appendix-c-quick-start-architecture-for-sgb-advoca|Appendix C: Quick-Start Architecture for SGB Advocate Colleague]] _29%_
- [[221-10-open-questions|10. Open Questions]] _25%_
- [[213-2-what-makes-a-professional-colleague-agent|2. What Makes a Professional Colleague Agent]] _21%_
- [[214-3-empirical-case-study-обучай|3. Empirical Case Study: «Обучай»]] _21%_
- [[249-composite-skills-agent-md|COMPOSITE SKILLS AGENT.md]] _21%_
- [[254-1-why-the-binary-view-is-incomplete|1. Why the Binary View Is Incomplete]] _21%_
## Связанные документы

- [[228-appendix-c-quick-start-architecture-for-sgb-advoca|Appendix C: Quick-Start Architecture for SGB Advocate Colleague]] _37%_
- [[217-6-risks-specific-to-this-category|6. Risks Specific to this Category]] _33%_
- [[221-10-open-questions|10. Open Questions]] _33%_
- [[216-5-the-economics-of-profession-wide-replication|5. The Economics of Profession-Wide Replication]] _29%_
- [[151-open-knowledge-work-foundation-md|OPEN KNOWLEDGE WORK FOUNDATION.md]] _25%_
- [[208-professional-colleague-agents-md|PROFESSIONAL COLLEAGUE AGENTS.md]] _25%_
- [[213-2-what-makes-a-professional-colleague-agent|2. What Makes a Professional Colleague Agent]] _25%_
- [[214-3-empirical-case-study-обучай|3. Empirical Case Study: «Обучай»]] _25%_
