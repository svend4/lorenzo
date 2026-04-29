# Что брать из info repositories — concrete recommendations

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — анализ комбинирования пассивного Nautilus с активным CAMEL framework.

---
<!-- tags: architecture, roadmap, anthropic -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — анализ комбинирования пассивного Nautilus с активным CAMEL framework.

Что брать из info repositories — concrete recommendations

Берите concepts, не берите code из info1/info7/info40.

Concepts worth taking:

Trichotomous economy model (info40) → apply к OKWF deployment

Five orchestration strategies (info7) → use as decision framework для CAMEL Workforce setups

Layered architecture pattern (info7) → guide CAMEL deployment structure

Use case scenarios with metrics (info40) → write similar для SGB Advocate Colleague

Marketplace registry concept (info40) → potential future addition к Nautilus Portal Protocol

Corpus Callosum pattern (info7) → integrate CAMEL Memory с knowledge graph

5-level hierarchy concept (info7) → applicable для very complex domain coordination

Multi-tenancy + RBAC concerns (info7) → architectural considerations для shared deployment

Code worth taking: probably минимально. CAMEL provides better-tested infrastructure для most things. Write fresh code on CAMEL substrate, taking inspiration from info patterns.

Honest practical assessment

Этот synthesis technically feasible, но требует significant work:

Realistic timeline для SGB Advocate Colleague v0.1:

1 month: Setup CAMEL deployment, basic ChatAgent с general legal knowledge

2 months: Build first MCP servers (sgb-ix, sozialgericht-procedures)

3 months: Implement Workforce coordination для basic case handling

4-6 months: Refinement based на actual case work usage

Total to useful v0.1: ~6 months

Realistic timeline для federation through Nautilus: another 3-6 months after v0.1 working.

Realistic timeline для marketplace dimension: probably 12+ months после base system stable.

Это significant investment of time. Учитывая ваши active SGB cases, физические considerations, и other commitments, realistic question — насколько это feasible.

Альтернатива: minimum viable approach

Если full architecture seems too ambitious, minimum viable version:

Phase 0 — Just CAMEL:

Install CAMEL on your Termux setup

Create single ChatAgent с German legal system prompt

Add 5-10 simple tools (web search, document reading, basic calculations)

Use it для your own SGB cases

Phase 1 — Add specialization:

Build one MCP server (например, для SGB IX § 78)

Connect к CAMEL agent

Test if useful in real case work

Phase 2 — Add multi-agent:

Add second ChatAgent для different specialization

Use CAMEL's Role-Playing для collaboration

Test hybrid coordination

Phase 3 — Federate:

Expose simple Portal Protocol endpoint

See if другие practitioners adopt

Each phase testable per se. Don't commit к full vision before earlier phases prove value.

Один critical insight

Важная вещь: не пытайтесь implement all info repositories' concepts simultaneously. Они represent 3+ years of conceptual exploration. Pick one concept to implement first (например, Professional Agent specialization для SGB), validate it works, then add more.

info1 → info7 → info40 progression demonstrates accumulation of ideas. Implementation should similarly accumulate gradually. CAMEL provides infrastructure для each accumulation step.

Прямой ответ на ваш вопрос

Подходит ли CAMEL больше для этого? Да, существенно больше чем Hermes или Cowork. Reasons:

Multi-agent first design matches info7/info40 multi-agent vision

Workforce pattern directly implements info7's hierarchy concepts

Apache 2.0 license enables commercial deployment if marketplace pursued

Mature framework reduces infrastructure work

Python-based ecosystem easy для domain-specific extensions

Research orientation aligns с conceptual exploration character of info repos

Возможно ли частично взять что-то из info repositories и адаптировать на CAMEL? Да, но conceptually, не codewise. Take patterns, frameworks, decision strategies, economic models. Re-implement clean on CAMEL substrate.

Какой посредник? Combination:

MCP для tool/capability portability across platforms

Nautilus Portal Protocol для federation between deployments

Marketplace layer (longer term) для economy dimension

Это не one-thing-mediator. Эта layered mediation где каждый mediator handles different concern.

<!-- see-also -->

---

**Смотрите также:**
- [02-what-info-repos-contain](docs/anthropic-vacancies/nautilus-vs-camel/02-what-info-repos-contain.md)
- [03-sgb-advocate-colleague-example](docs/anthropic-vacancies/nautilus-vs-camel/03-sgb-advocate-colleague-example.md)
- [05-what-to-do-right-now](docs/anthropic-vacancies/nautilus-vs-camel/05-what-to-do-right-now.md)
- [08-implications-nautilus-okwf](docs/nautilus/ingit-cowork-en/08-implications-nautilus-okwf.md)

