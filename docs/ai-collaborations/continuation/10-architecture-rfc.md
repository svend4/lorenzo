# Следующий артефакт: Svyazi 2.0 Architecture RFC

> Источник: MHTML‑снимок `Поиск коллабораций AI проектов` (корень репозитория).

10. Следующий конкретный артефакт: Svyazi‑2.0 Architecture RFC

После всех этих продолжений самым полезным документом будет не ещё один обзор, а RFC на 8–12 страниц. Его структура:

Problem statement: почему обычные CRM, Notion‑базы и RAG‑чаты не решают discovery коллабораций.

Core entities: person, project, episode, document, hypothesis, match, review, trace.

Contracts: Card Envelope, Evidence Envelope, Memory Write Policy, Trace Envelope, Review Record.

Runtime: MCP для tools, A2A для agents, HITL для risky actions.

Memory: episode/proposal/fact/conflict/decayed states.

Safety: PII separation, external content quarantine, prompt‑worm firewall, tool class policies.

Metrics: precision@k, evidence coverage, false association rate, cost per card, trace completeness.

MVP boundary: что входит в v0.1, что запрещено до v0.2.

Pilot scenarios: community OS, legal/research OS, AgentOps memory kernel.
