# Memory Firewall против prompt worms (ансамбль I)

<!-- toc-auto -->
## Contents

- [Использование](#использование)
- [Смотрите также](#смотрите-также)


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

<!-- summary -->
> Habr
Аудит OpenClaw показал практический слой этой проблемы: zero‑sanitization pipeline, timeout‑as‑approval, arbitrary exec через plugin system, plaintext credential storage, memory exfiltration/injection, default‑open command gating и другие критич
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

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Memory Firewall против prompt worms"
```

## Смотрите также
- [5-agent-firewall](../ensembles/5-agent-firewall.md)
- 03-a2a-vs-[mcp-protocols](03-a2a-vs-mcp-protocols.md)
- [02-agentops-trace-envelope](02-agentops-trace-envelope.md)
- [1-agentic-knowledge-os](../ensembles/1-agentic-knowledge-os.md)

_Документ индексирован в базе знаний репозитория Lorenzo._ _Для поиска доступен._

<!-- backlinks -->

---

**Кто ссылается на этот документ (11):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [TABLES](../../TABLES.md)
- [02-agentops-trace-envelope](02-agentops-trace-envelope.md)
- [03-a2a-vs-mcp-protocols](03-a2a-vs-mcp-protocols.md)
- [README](README.md)
- _...ещё 3_


<!-- similar-docs -->

---

**Похожие документы:**
- [04-memory-firewall-vs-prompt-worms](../../obsidian/ai-collaborations/continuation/04-memory-firewall-vs-prompt-worms.md) (сходство 0.98)
- [5-agent-firewall](../ensembles/5-agent-firewall.md) (сходство 0.21)
- [5-agent-firewall](../../obsidian/ai-collaborations/ensembles/5-agent-firewall.md) (сходство 0.21)

