# Memory Firewall против prompt worms (ансамбль I)

> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Поиск коллабораций AI проектов` (корень репозитория).
**Проекты:** Svyazi, SENTINEL

---
<!-- tags: memory, rag, security, ingestion, architecture, collaboration -->




> Источник: MHTML‑снимок `Поиск коллабораций AI проектов` (корень репозитория).

4. Четвёртый новый слой: защита от prompt worms и заражения памяти

Чем больше Svyazi‑2.0 становится агентной системой, тем больше она становится потенциальным переносчиком атак. На Хабре есть сильная линия материалов про Prompt Worms и аудит OpenClaw. Главная мысль: если агент читает недоверенный контент, имеет доступ к данным и может отправлять сообщения наружу, он превращается в вектор атаки. В статье про Prompt Worms отдельно выделен риск persistent memory: вредоносные инструкции могут быть записаны в долговременную память фрагментами и позже собраны в исполняемое поведение. Habr

Аудит OpenClaw показал практический слой этой проблемы: zero‑sanitization pipeline, timeout‑as‑approval, arbitrary exec через plugin system, plaintext credential storage, memory exfiltration/injection, default‑open command gating и другие критические/high‑risk проблемы. Habr

Ансамбль I — Memory Firewall

Родители: Svyazi privacy‑by‑design + SENTINEL/Prompt Worms lessons + LangGraph HITL + Card/Evidence/Memory contracts.

Что рождается: память, в которую нельзя просто “записать всё, что сказал агент”.

Mermaid

Практическое правило: внешний текст не должен иметь права становиться instruction memory. Он может стать episode, source, evidence, observation, но не system rule и не trusted fact без review. Это особенно важно для Svyazi‑2.0, потому что профили людей, чаты, PDF, сайты, GitHub‑issues и сообщения агентов будут смешиваться в одном graph‑пространстве.

<!-- see-also -->

---

**Смотрите также:**
- [5-agent-firewall](docs/ai-collaborations/ensembles/5-agent-firewall.md)
- [03-a2a-vs-mcp-protocols](docs/ai-collaborations/continuation/03-a2a-vs-mcp-protocols.md)
- [02-agentops-trace-envelope](docs/ai-collaborations/continuation/02-agentops-trace-envelope.md)
- [1-agentic-knowledge-os](docs/ai-collaborations/ensembles/1-agentic-knowledge-os.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [5-agent-firewall](docs/ai-collaborations/ensembles/5-agent-firewall.md) (сходство 0.20)
- [03-a2a-vs-mcp-protocols](docs/ai-collaborations/continuation/03-a2a-vs-mcp-protocols.md) (сходство 0.19)
- [01-shared-memory-between-agents](docs/ai-collaborations/continuation/01-shared-memory-between-agents.md) (сходство 0.17)

