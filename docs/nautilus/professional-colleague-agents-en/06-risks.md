# 6. Risks Specific to this Category

> [!TIP]
> Документ содержит практические рекомендации и лучшие практики.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — paper «Professional Colleague Agents (EN)», написанный совместно с Claude.

---

<!-- toc -->
## Содержание

- [6. Risks Specific to this Category](#6-risks-specific-to-this-category)
  - [6.1. Risk: Mediation Collapse](#61-risk-mediation-collapse)
  - [6.2. Risk: Skill Atrophy in New Practitioners](#62-risk-skill-atrophy-in-new-practitioners)
  - [6.3. Risk: Standardization Lock-In](#63-risk-standardization-lock-in)
  - [6.4. Risk: Liability Ambiguity](#64-risk-liability-ambiguity)
  - [6.5. Risk: Privacy Cascade](#65-risk-privacy-cascade)
  - [6.6. Risk: Subtle Bias in Knowledge Base](#66-risk-subtle-bias-in-knowledge-base)
  - [6.7. Risk: Profession Capture by Service Providers](#67-risk-profession-capture-by-service-providers)

---

<!-- tags: local-first, architecture, anthropic -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — paper «Professional Colleague Agents (EN)», написанный совместно с Claude.

## 6. Risks Specific to this Category

Professional Colleague Agents have risks distinct from
Representative Agents and other types. We identify seven
specific to this category.

### 6.1. Risk: Mediation Collapse

**Scenario**: When both parties to a professional interaction
use AI agents, the human content of the interaction approaches
zero.

**Concrete example**: Teacher generates assignments with AI.
Student completes assignments with AI. Teacher grades with AI.
Student receives grade. Where in this chain has actual learning
occurred?

This is the most-cited public concern about Type 1 agents.
Its resolution requires conscious design decisions:

**Mitigation 1 — Asymmetric design.** Teacher's agent
generates problems requiring active human reasoning, not
pattern-matching. Problems for which AI assistance produces
poor results. Design assignments AI-resistance into them.

**Mitigation 2 — Live elements.** Some assessments require
live human interaction (oral exams, project presentations,
collaborative work) where AI assistance is structurally
limited.

**Mitigation 3 — Process visibility.** Both parties see what
AI was used for. Norms develop about acceptable usage.

**Mitigation 4 — Reframing of education.** If AI changes
what students can do, education adapts. The era of
homework-as-assessment may end. New forms of assessment
emerge.

This is not solved within agent design alone. It requires
profession-wide adaptation.

### 6.2. Risk: Skill Atrophy in New Practitioners

**Scenario**: Junior practitioners using the agent from day
one never develop foundational skills the agent automates.
When agent fails (inevitably) or is unavailable, practitioner
cannot perform basic professional functions.

**Concrete example**: Junior lawyer uses parajural AI for
all routine drafting. Never develops drafting skills personally.
Cannot draft when AI is unavailable. Cannot critically review
AI output because they don't know what good drafting looks
like.

**Mitigation 1 — Educational pathway.** Professional training
includes period of doing work without AI assistance. Like
learning to compute by hand before using calculators.

**Mitigation 2 — Transparent operation.** Agent shows its work,
not just outputs. Practitioner can learn from observing agent's
process.

**Mitigation 3 — Mandatory review burden.** Practitioner must
genuinely review agent outputs, not approve mechanically. Spot
checks built into workflow.

**Mitigation 4 — Acceptable trade-offs.** Some skill atrophy
is acceptable. We do not lament the loss of mental arithmetic
skills due to calculators. The question is which skills are
essential to retain.

### 6.3. Risk: Standardization Lock-In

**Scenario**: Wide deployment of one agent in a profession
homogenizes professional practice. Innovations from outside
the agent's training data become harder to introduce.
Professional creativity declines.

**Concrete example**: All teachers use «Обучай»-style assignments.
All assignments converge to similar style. Pedagogical innovation
slows because non-conventional approaches are harder to access.

**Mitigation 1 — Open architecture.** Multiple Professional
Colleague Agents compete in each profession. No single
provider dominates.

**Mitigation 2 — Customization affordances.** Agents support
practitioner customization that goes beyond preferences into
methodology choices.

**Mitigation 3 — Innovation channels.** Profession maintains
non-AI channels for sharing innovative approaches. Journals,
conferences, peer mentorship persist alongside AI-assisted
work.

**Mitigation 4 — Active diversity.** Foundation-funded
agents could deliberately offer multiple methodological
approaches in their knowledge base, exposing practitioners
to variety.

### 6.4. Risk: Liability Ambiguity

**Scenario**: Practitioner uses agent-generated output that
turns out to contain professional errors. Who is liable?
Practitioner who used? Agent provider? Knowledge base curator?
LLM provider underlying generation?

**Concrete example**: Lawyer files brief with citation generated
by parajural AI. Citation turns out to be hallucination. Court
sanctions lawyer. Was the lawyer negligent? Was the AI provider?

**Current state**: Legal frameworks are immature. Courts are
beginning to address this case by case.

**Mitigation 1 — Explicit practitioner responsibility.**
Service terms make clear: practitioner is responsible for
outputs they use. Agent is tool, not professional.

**Mitigation 2 — Cited outputs only.** Agent outputs are
verifiable through citations. Practitioner who fails to
verify is negligent.

**Mitigation 3 — Professional liability evolution.** Insurance
products evolve to cover AI-assisted work. New regulatory
clarifications.

**Mitigation 4 — Transparent error rates.** Agent providers
publish error rates and known failure modes. Practitioners
factor these into use.

### 6.5. Risk: Privacy Cascade

**Scenario**: Practitioner uses agent on case involving
sensitive client data. Sensitive data flows through agent
infrastructure. Breach exposes client data.

**Concrete example**: Therapist uses Professional Colleague
Agent for note synthesis. Patient privacy is compromised
when agent provider has security incident.

**Mitigation 1 — Local-first deployment.** For high-sensitivity
domains, agent runs entirely on practitioner's device or
institutional infrastructure. No cloud dependencies.

**Mitigation 2 — Anonymization at input.** Practitioner uses
anonymized representations when working with agent. Real
identity stays in practitioner's separate records.

**Mitigation 3 — Compliance certification.** Agent providers
obtain HIPAA, GDPR, equivalent compliance.

**Mitigation 4 — Encrypted processing.** Modern cryptographic
techniques (homomorphic encryption, secure enclaves) enable
processing without exposure.

### 6.6. Risk: Subtle Bias in Knowledge Base

**Scenario**: Layer A knowledge base reflects biases of its
curators. Practitioners using agent inherit these biases.
Bias spreads systematically.

**Concrete example**: Legal Professional Colleague Agent's
knowledge base over-represents perspectives of one school of
legal thought. Practitioners using agent draft submissions
subtly aligned with that school. Legal pluralism declines.

**Mitigation 1 — Diverse curation panels.** Layer A built
by panels representing diverse views within the profession.

**Mitigation 2 — Methodological transparency.** Agent makes
explicit which methodological tradition informs its outputs.
Practitioner can choose alternatives.

**Mitigation 3 — External audit.** Independent reviewers
periodically audit knowledge base for bias.

**Mitigation 4 — User customization.** Practitioners can
configure which methodological frameworks the agent applies.

### 6.7. Risk: Profession Capture by Service Providers

**Scenario**: One Professional Colleague Agent dominates
profession. Provider acquires de facto power over professional
practice. Profession loses autonomy.

**Concrete example**: Single AI provider serves 90% of teachers.
Provider's design choices effectively determine pedagogy
nationally. Provider's pricing and terms determine teacher
working conditions.

**Mitigation 1 — Open standards.** Layer A knowledge bases
are standardized formats, portable between providers.

**Mitigation 2 — Foundation-owned alternatives.** Mission-driven
nonprofits maintain alternatives to commercial providers.

**Mitigation 3 — Cooperative ownership.** Practitioners
collectively own platforms serving them.

**Mitigation 4 — Regulatory frameworks.** Antitrust and
profession-specific regulation prevents excessive concentration.

This risk is real and serious. «Обучай» growing to 93,000
teachers in 7 months illustrates speed at which capture can
emerge.

---

<!-- see-also -->

---

**Смотрите также:**
- [217-6-risks-specific-to-this-category](docs/02-anthropic-vacancies/217-6-risks-specific-to-this-category.md)
- [04-sub-agent-registry](docs/nautilus/composite-skills-agents/04-sub-agent-registry.md)
- [10-risks](docs/nautilus/composite-skills-agents/10-risks.md)
- [04-architecture](docs/nautilus/professional-colleague-agents-en/04-architecture.md)

