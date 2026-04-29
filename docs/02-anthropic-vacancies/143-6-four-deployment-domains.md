# 6. Four Deployment Domains

<!-- summary -->
> The Double-Triangle Architecture is domain-agnostic but benefits

---

<!-- toc -->
## Содержание

- [6. Four Deployment Domains](#6-four-deployment-domains)
  - [6.1. Humanities Domain (Legal, Medical, Social)](#61-humanities-domain-legal-medical-social)
  - [6.2. Project Management Domain](#62-project-management-domain)
  - [6.3. Open-Source Development Domain](#63-open-source-development-domain)
  - [6.4. Generic Knowledge Work Domain](#64-generic-knowledge-work-domain)

---

<!-- tags: rag, roadmap, collaboration -->




## 6. Four Deployment Domains

The Double-Triangle Architecture is domain-agnostic but benefits 
from concrete deployment analysis. We describe four domains where 
the architecture applies naturally.

### 6.1. Humanities Domain (Legal, Medical, Social)

**Participants.** Legal professionals, social workers, medical 
practitioners, rights advocates.

**Lower triangle contents.** Assistants specialized for:
- Legal research (case law, statute lookup)
- Document drafting (Widerspruch, Klage, petitions)
- Compliance checking (GDPR, medical confidentiality)
- Timeline tracking (deadlines, Fristwahrung)

**Upper triangle contents.** Meta-agent coordinating multiple 
advocates on related cases, sharing anonymized patterns, 
escalating cross-jurisdictional issues.

**Pattern library examples.** SGB statutes, anonymized court 
decisions, Widerspruch templates, ICD-10 classifications, 
institutional procedure patterns.

**Concrete deployment.** An individual (the first author, 
svend4) currently engages with Sozialgericht Dresden on cases 
S 6 SO 58/26 ER and S 7 SO 99/25. Personal workflow already 
exhibits lower triangle structure (Claude Code for technical 
documents, Claude Sonnet for German legal drafting). Upper 
triangle would emerge when other advocates working on related 
cases coordinate through shared anonymized pattern library.

**Regulatory considerations.** GDPR Article 5 (data minimization), 
§ 203 StGB (professional confidentiality), UrhG § 5 (public 
domain status of statutes and court decisions). All compatible 
with Double-Triangle if anonymization pipeline operates correctly.

### 6.2. Project Management Domain

**Participants.** Software engineers, product managers, designers, 
DevOps engineers, QA engineers.

**Lower triangle contents.** Assistants specialized for:
- Code generation and review (Copilot, Cursor, Claude Code)
- Design ideation (Figma AI, sketch tools)
- Deployment automation (Terraform AI, kubectl-ai)
- Test generation (property-based test synthesis)

**Upper triangle contents.** Meta-agent performing sprint 
planning, dependency analysis, cross-team coordination, 
retrospective synthesis.

**Pattern library examples.** Agile methodologies, CI/CD 
patterns, deployment playbooks, incident postmortems (anonymized), 
architecture decision records.

**Existing partial implementations.** Jira AI, Linear AI, GitHub 
Projects automation — all provide fragments of this architecture 
but lack Protocol 3.

**Business opportunity.** Organizations currently spend 20–30% 
of engineering budget on middle management. A Double-Triangle 
implementation that replaces some coordination functions with AI 
meta-agents (while keeping humans in the engineer role) could 
significantly alter organizational economics.

### 6.3. Open-Source Development Domain

**Participants.** Maintainers, contributors, reviewers, users.

**Lower triangle contents.** Per-participant assistants for:
- Contribution drafting (PRs, issues, documentation)
- Code review (automated checks, suggestion generation)
- Community moderation (anti-spam, tone analysis)

**Upper triangle contents.** Meta-agent handling:
- Triage and routing of incoming contributions
- Release planning and coordination
- Security vulnerability coordination
- Community health monitoring

**Pattern library examples.** Governance templates (BDFL, 
foundation-based, consensus), contribution guidelines, release 
playbooks, security advisory formats, code of conduct templates.

**Novel opportunity.** Open-source projects traditionally lack 
scalable coordination. A Double-Triangle deployment could enable 
small maintainer teams to manage much larger contributor 
communities without proportional coordination overhead.

### 6.4. Generic Knowledge Work Domain

**Participants.** Researchers, writers, consultants, analysts, 
educators.

**Lower triangle contents.** Assistants for:
- Literature review and synthesis
- Draft generation and revision
- Data analysis and visualization
- Citation management

**Upper triangle contents.** Meta-agent coordinating:
- Research group collaboration
- Multi-author paper writing
- Conference/workshop organization
- Grant application coordination

**Pattern library examples.** Research methodologies, writing 
templates, citation styles, peer review conventions.

**Observation.** This domain is perhaps the broadest application 
of Double-Triangle architecture. Most modern knowledge workers 
could potentially benefit from this structure once mature tools 
exist.

---

<!-- similar-docs -->

---

**Похожие документы:**
- [158-4-proposed-infrastructure](158-4-proposed-infrastructure.md) (сходство 0.18)
- [145-8-call-to-action](145-8-call-to-action.md) (сходство 0.17)
- [164-10-appendices](164-10-appendices.md) (сходство 0.15)


<!-- see-also -->

---

**Смотрите также:**
- [158-4-proposed-infrastructure](158-4-proposed-infrastructure.md)
- [145-8-call-to-action](145-8-call-to-action.md)
- [164-10-appendices](164-10-appendices.md)
- [219-8-pilot-proposal-sgb-advocate-colleague](219-8-pilot-proposal-sgb-advocate-colleague.md)

<!-- backlinks-auto -->
## Упоминается в

- [Вакансии Anthropic — Анализ по кластерам](../README.md)

<!-- related-auto -->
## Связанные документы

- [Appendix A: Glossary](148-appendix-a-glossary.md) _37%_
- [8. Call to Action](145-8-call-to-action.md) _29%_
- [2. The Double-Triangle Architecture](139-2-the-double-triangle-architecture.md) _25%_
- [5. Pattern Library as Bridge Between Triangles](142-5-pattern-library-as-bridge-between-triangles.md) _25%_
- [7. Open Questions](144-7-open-questions.md) _21%_
- [9. Integration with OKWF Infrastructure](262-9-integration-with-okwf-infrastructure.md) _21%_
- [THE DOUBLE-TRIANGLE ARCHITECTURE.md](134-the-double-triangle-architecture-md.md) _18%_
- [Abstract](136-abstract.md) _17%_
