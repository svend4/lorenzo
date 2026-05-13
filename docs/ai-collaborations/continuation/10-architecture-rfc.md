---
state: normalized
---

# Следующий артефакт: Svyazi 2.0 Architecture RFC

<!-- toc-auto -->
## Contents

- [Использование](#использование)
- [Смотрите также](#смотрите-также)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> Документ создан на основе исследования. Ссылки ведут на связанные материалы. Кто ссылается на этот документ (11):
Кто ссылается на этот документ (11):
 OUTLINE
 READABILITY
 READING_TIME
 SEARCH
 TABLES
 02-agentops-trace-envelope
 03-a2a-vs-mcp-protocols
 05-roadmap-6-12-months
 _...ещё 3_
 --
Похожие документы:
 10-architecture-rfc (сходство 0.98)
 13-commu
**Проекты:** Svyazi

---
<!-- tags: memory, rag, security, ingestion, architecture, roadmap, collaboration -->

> [!IMPORTANT]
> Нормативный документ. Описывает контракты и архитектурные решения.





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

<!-- see-also -->

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Следующий артефакт Svyazi 2 0"
```

## Смотрите также
- [06-metrics-tree](06-metrics-tree.md)
- [05-roadmap-6-12-months](05-roadmap-6-12-months.md)
- [02-agentops-trace-envelope](02-agentops-trace-envelope.md)
- [09-do-not-glue](09-do-not-glue.md)

Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации через граф концептов. Используйте скрипты группы reports для получения актуальной статистики по разделу. Рекомендуется начинать с основных документов раздела и переходить к деталям через внутренние ссылки. Все связанные документы доступны через граф концептов и поисковый индекс репозитория Lorenzo. Документы раздела индексированы в поисковой базе и доступны для семантического поиска и BM25. Документ индексирован в базе знаний репозитория.

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
- [05-roadmap-6-12-months](05-roadmap-6-12-months.md)
- _...ещё 3_


<!-- similar-docs -->

---

**Похожие документы:**
- [10-architecture-rfc](../../obsidian/ai-collaborations/continuation/10-architecture-rfc.md) (сходство 0.98)
- [13-communications](../../anthropic-vacancies/clusters/13-communications.md) (сходство 0.36)
- [03-section-3-solution-architecture](../../anthropic-vacancies/beneficial-deployments-concept/03-section-3-solution-architecture.md) (сходство 0.36)

