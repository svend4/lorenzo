---
title: "8. Pilot Proposal: SGB Advocate Colleague"
tags:
  - rag
  - architecture
  - roadmap
  - anthropic-vacancies
date: 2026-04-29
---

# 8. Pilot Proposal: SGB Advocate Colleague

<!-- summary -->
> We now apply the Professional Colleague Agent framework to a

---

<!-- toc -->
## Содержание

- [8. Pilot Proposal: SGB Advocate Colleague](#8-pilot-proposal-sgb-advocate-colleague)
  - [8.1. Context](#81-context)
  - [8.2. Target Practitioners](#82-target-practitioners)
  - [8.3. Burden Addressed](#83-burden-addressed)
  - [8.4. Knowledge Base Requirements](#84-knowledge-base-requirements)
  - [8.5. Pilot Cohort](#85-pilot-cohort)
  - [8.6. Resource Requirements](#86-resource-requirements)
  - [8.7. Expected Outcomes](#87-expected-outcomes)
  - [8.8. Why This Domain First](#88-why-this-domain-first)

---

<!-- tags: rag, architecture, roadmap -->




## 8. Pilot Proposal: SGB Advocate Colleague

We now apply the Professional Colleague Agent framework to a
specific opportunity: an agent for advocates in German social
law (SGB), particularly disability and welfare rights.

### 8.1. Context

The author of this paper engages directly with German social
law through ongoing Sozialgericht proceedings (cases S 6 SO
58/26 ER and S 7 SO 99/25 in Dresden). Direct experience
shows that legal advocacy in this domain is severely
under-resourced. Many qualified disabled people lose
entitlements through procedural failures because they cannot
access adequate representation.

This is the same domain identified in Representative Agent
Layer paper as Domain 4 (vulnerable citizens navigating
bureaucracy). Professional Colleague Agent for advocates
serving this population could amplify their capacity
substantially.

### 8.2. Target Practitioners

**Primary**: Lawyers specializing in social law (Sozialrecht)
in Germany. Estimated 5,000-10,000 active practitioners.

**Secondary**: Disability rights advocates in NGOs (Sozialverband
VdK, Behindertenverbände, Diakonie social work staff). Estimated
2,000-5,000 practitioners.

**Tertiary**: Self-representing affected individuals (with
supervisory professional review). Potentially hundreds of
thousands.

For pilot, focus on Primary and Secondary. Tertiary requires
careful design and supervision; appropriate for later phase.

### 8.3. Burden Addressed

**Routine drafting**:
- Widerspruch against rejected applications
- Klage (lawsuit) submission to Sozialgericht
- Stellungnahme on counterparty filings
- Antrag for procedural relief
- Eilantrag for emergency proceedings

**Knowledge lookup**:
- Relevant SGB statutes (IX, XII primarily)
- BSG decisions and precedent (e.g., B 8 SO 9/19 R)
- Local Sozialgericht procedural variations
- Federal-state law interaction

**Procedural management**:
- Deadline tracking (Fristwahrung)
- Document organization across multiple proceedings
- Evidence inventory and citation
- Hearing preparation

**Communication drafting**:
- Standard correspondence with KSV, Sozialamt, courts
- Routine procedural letters
- Client-facing summary documents

### 8.4. Knowledge Base Requirements

The Layer A for this agent requires:

**Statutory knowledge**:
- Full SGB IX (rehabilitation, disability)
- Full SGB XII (social assistance)
- Relevant SGG (procedural law)
- Selected SGB I, II, III, V, XI cross-references

**Case law**:
- BSG decisions (federal social court)
- Sächsisches Landessozialgericht decisions (state-specific)
- Selected Sozialgericht-level decisions

**Procedural standards**:
- Sozialgericht procedural conventions
- Local court practices (Dresden specifically for pilot)
- Standard formatting for filings

**Pattern library**:
- Successful Widerspruch templates by issue type
- Standard arguments for common rejection patterns
- Anonymized successful approaches

**Bureaucratic knowledge**:
- KSV Sachsen practices and known patterns
- Sozialamt Dresden practices
- Common procedural errors by authorities

This represents substantial curation work — perhaps 2,000-5,000
expert hours to bootstrap. Maintenance: 200-500 hours/year.

### 8.5. Pilot Cohort

**Phase 0 (Months 1-6)**: Bootstrap with 5-10 advocates,
including the author, plus 1-2 lawyers willing to test
intensively. Build initial Layer A. Refine through real use.

**Phase 1 (Months 6-18)**: Expand to 50-100 advocates. Iterate
on knowledge base. Establish quality assurance processes.

**Phase 2 (Months 18-36)**: Open to all interested practitioners
in domain. Target 500-1,000 active users.

**Phase 3 (Years 3+)**: Expand to adjacent domains (other German
states, other social law sub-specialties).

### 8.6. Resource Requirements

**Initial development (Year 1)**:
- 1 senior legal expert (curator) full-time: €100,000
- 2 software engineers: €200,000
- LLM API costs: €30,000
- Infrastructure: €20,000
- Legal compliance: €30,000
- Operations: €50,000
- **Total Year 1: €430,000**

**Steady state (Year 2+)**:
- Curation maintenance (0.5 FTE): €60,000
- Engineering maintenance (1 FTE): €100,000
- LLM API costs (scaled): €100,000-300,000
- Infrastructure: €30,000
- Operations: €50,000
- **Total annual: €340,000-540,000**

For 500-1,000 active practitioners, this is roughly
€500-1,000 per practitioner per year — viable for
foundation funding or modest practitioner subscriptions.

### 8.7. Expected Outcomes

**For practitioners**:
- 30-50% time reduction on routine drafting
- Improved consistency in formal compliance
- Faster ramp-up for new advocates

**For affected individuals (clients)**:
- More cases successfully advocated
- Faster procedural response
- Better access to entitlements

**For knowledge ecosystem**:
- Public pattern library of successful approaches
- Improved baseline for self-representation
- Anonymized case insights for academic study

**For broader project**:
- Reference implementation for OKWF Professional Colleague
  Agents
- Demonstration of foundation-funded model
- Connection to Representative Agent Layer (advocates use
  agents for clients who could later use Representative
  Agents directly)

### 8.8. Why This Domain First

Several factors make this an ideal first deployment for
OKWF Professional Colleague Agents:

**Personal expertise**: Author has direct experience and
domain knowledge.

**Underserved market**: Limited commercial competition in
this specific sub-specialty.

**Aligned values**: Serves vulnerable populations; mission-fit
with foundation funding.

**Manageable scope**: Single legal sub-domain in single
country. Tractable bootstrap.

**Clear demand**: Author personally needs this. Other advocates
do too.

**Network effects available**: Successful case anonymized
patterns benefit all users.

**Foundation-friendly economics**: Modest budget viable;
practitioners cannot afford expensive commercial alternatives;
public funding precedented in legal aid space.

This pilot provides the OKWF concept its first concrete
deployment. From here, expansion to adjacent domains becomes
incremental rather than novel.

---

<!-- similar-docs -->

---

**Похожие документы:**
- [[260-7-economics-of-combinatorial-replication]] (сходство 0.17)
- [[262-9-integration-with-okwf-infrastructure]] (сходство 0.16)
- [[164-10-appendices]] (сходство 0.15)


<!-- see-also -->

---

**Смотрите также:**
- [[260-7-economics-of-combinatorial-replication]]
- [[262-9-integration-with-okwf-infrastructure]]
- [[164-10-appendices]]
- [[216-5-the-economics-of-profession-wide-replication]]

<!-- backlinks-auto -->
## Упоминается в

- [[README|Вакансии Anthropic — Анализ по кластерам]]

<!-- related-auto -->
## Связанные документы

- [[216-5-the-economics-of-profession-wide-replication|5. The Economics of Profession-Wide Replication]] _29%_
- [[260-7-economics-of-combinatorial-replication|7. Economics of Combinatorial Replication]] _29%_
- [[151-open-knowledge-work-foundation-md|OPEN KNOWLEDGE WORK FOUNDATION.md]] _25%_
- [[215-4-architecture-of-professional-colleague-agents|4. Architecture of Professional Colleague Agents]] _25%_
- [[221-10-open-questions|10. Open Questions]] _25%_
- [[223-12-closing|12. Closing]] _25%_
- [[228-appendix-c-quick-start-architecture-for-sgb-advoca|Appendix C: Quick-Start Architecture for SGB Advocate Colleague]] _25%_
- [[273-infrastructure-for-ai-collaborative-intellectual-w|INFRASTRUCTURE FOR AI-COLLABORATIVE INTELLECTUAL WORK.md]] _25%_
