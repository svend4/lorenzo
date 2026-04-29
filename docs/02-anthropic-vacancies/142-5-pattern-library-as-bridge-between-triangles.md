# 5. Pattern Library as Bridge Between Triangles

> [!TIP]
> Документ содержит практические рекомендации и лучшие практики.

<!-- alert-added -->

<!-- summary -->
> Double-Triangle systems face a fundamental question: how do

---

<!-- toc -->
## Содержание

- [5. Pattern Library as Bridge Between Triangles](#5-pattern-library-as-bridge-between-triangles)
  - [5.1. The Problem of Shared Knowledge](#51-the-problem-of-shared-knowledge)
  - [5.2. Pattern Library Architecture](#52-pattern-library-architecture)
  - [5.3. Three Types of Bridges](#53-three-types-of-bridges)
  - [5.4. Anonymization as Contribution Mechanism](#54-anonymization-as-contribution-mechanism)
  - [5.5. Why This Architecture Is Critical for Double-Triangle](#55-why-this-architecture-is-critical-for-double-triangle)

---

<!-- tags: security, roadmap -->




## 5. Pattern Library as Bridge Between Triangles

### 5.1. The Problem of Shared Knowledge

Double-Triangle systems face a fundamental question: how do 
assistants in different Nodes' lower triangles share knowledge 
about best practices, conventions, and reusable patterns, without 
each Node privately replicating this knowledge?

Centralized shared knowledge (company wiki, organization 
playbook) has known problems: it stales, it duplicates with 
external sources, and it creates single points of failure.

Fully distributed knowledge (every assistant learns independently) 
has opposite problems: it doesn't compound, and it diverges.

### 5.2. Pattern Library Architecture

We propose a **pattern library architecture** operating in two 
tiers:

**Tier 1 — Public Patterns.** Repositories of abstract patterns: 
methodologies (Scrum, Kanban, DDD), legal norms (SGB statutes, 
EU directives), templates (pull request templates, meeting 
formats), best practices, antipatterns. These are shared across 
many teams and organizations.

**Tier 2 — Private Instances.** Concrete applications of patterns 
within specific contexts: a team's actual sprint, a lawyer's 
actual case, a developer's actual deployment. These are 
Node-specific and often confidential.

**Inheritance relationship.** Each private instance **inherits** 
from one or more public patterns. An instance can override 
specific parts of a pattern while retaining the overall structure.

```json
{
  "name": "my-case-2026",
  "format": "case_instance",
  "inherits_from": [
    "public:nautilus-legal:pattern/eingliederungshilfe_denial_reversal",
    "public:nautilus-legal:norm/sgb_xii_90",
    "public:nautilus-legal:template/widerspruch_generic"
  ],
  "overrides": {
    "eingliederungshilfe_denial_reversal": {
      "specific_to": "Sachsen jurisdiction",
      "timeline_adjusted": true
    }
  }
}
```

### 5.3. Three Types of Bridges

The pattern library introduces three distinct bridge types beyond 
NPP v1.1's single "bridges" concept:

**Inheritance bridge.** Private instance points to public pattern 
it uses as a template. Direction: instance → pattern.

**Citation bridge.** Private instance references specific norms, 
decisions, or authorities. Direction: instance → authority.

**Contribution bridge.** Private instance generates anonymized 
pattern to contribute back to public library. Direction: instance 
→ pattern (through anonymization pipeline).

These three bridge types correspond to three workflow phases:

- **Start** of work: instance inherits from patterns (use existing 
  knowledge)
- **During** work: instance cites authorities (ground work in 
  source material)
- **After** work: instance contributes back (compound shared 
  knowledge)

### 5.4. Anonymization as Contribution Mechanism

For pattern libraries to grow organically without privacy 
violations, we require a formal **anonymization pipeline**:

1. PII detection (names, dates, addresses, identifiers)
2. Replacement with type-consistent placeholders
3. Manual verification (automated anonymization is insufficient)
4. Structural metadata addition (pattern type, outcome, applicability)
5. Publication to public tier

This pipeline enables Tier 2 instances to generate Tier 1 
patterns while preserving privacy. Anonymization becomes the 
**compounding mechanism** for shared knowledge.

### 5.5. Why This Architecture Is Critical for Double-Triangle

Without pattern library architecture:
- Assistants in N_1's lower triangle and N_2's lower triangle 
  cannot share knowledge
- Cross-Node learning requires explicit human coordination
- Team knowledge does not compound with use

With pattern library architecture:
- Assistants can query public patterns before executing tasks 
  (Protocol 1)
- Meta-agent can route tasks based on pattern fit (Protocol 2)
- Nodes can contribute back after successful execution (closing 
  the loop)

The pattern library is the **glue** that binds the upper and 
lower triangles into a coherent system where knowledge flows 
efficiently between levels.

---

<!-- similar-docs -->

---

**Похожие документы:**
- [148-appendix-a-glossary](docs/02-anthropic-vacancies/148-appendix-a-glossary.md) (сходство 0.17)
- [139-2-the-double-triangle-architecture](docs/02-anthropic-vacancies/139-2-the-double-triangle-architecture.md) (сходство 0.15)
- [144-7-open-questions](docs/02-anthropic-vacancies/144-7-open-questions.md) (сходство 0.14)


<!-- see-also -->

---

**Смотрите также:**
- [148-appendix-a-glossary](docs/02-anthropic-vacancies/148-appendix-a-glossary.md)
- [139-2-the-double-triangle-architecture](docs/02-anthropic-vacancies/139-2-the-double-triangle-architecture.md)
- [144-7-open-questions](docs/02-anthropic-vacancies/144-7-open-questions.md)
- [158-4-proposed-infrastructure](docs/02-anthropic-vacancies/158-4-proposed-infrastructure.md)

<!-- backlinks-auto -->
## Упоминается в

- [Вакансии Anthropic — Анализ по кластерам](docs/02-anthropic-vacancies/README.md)

<!-- related-auto -->
## Связанные документы

- [Appendix A: Glossary](docs/02-anthropic-vacancies/148-appendix-a-glossary.md) _37%_
- [4. Nautilus Portal as Reference Substrate](docs/02-anthropic-vacancies/141-4-nautilus-portal-as-reference-substrate.md) _29%_
- [6. Four Deployment Domains](docs/02-anthropic-vacancies/143-6-four-deployment-domains.md) _25%_
- [Abstract](docs/02-anthropic-vacancies/136-abstract.md) _21%_
- [1. Why Single-Triangle Models Are Incomplete](docs/02-anthropic-vacancies/138-1-why-single-triangle-models-are-incomplete.md) _21%_
- [2. The Double-Triangle Architecture](docs/02-anthropic-vacancies/139-2-the-double-triangle-architecture.md) _21%_
- [3. Three Inter-Layer Protocols](docs/02-anthropic-vacancies/140-3-three-inter-layer-protocols.md) _21%_
- [7. Open Questions](docs/02-anthropic-vacancies/144-7-open-questions.md) _21%_
