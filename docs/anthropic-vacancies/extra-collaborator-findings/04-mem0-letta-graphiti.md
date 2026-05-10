# AI-ассистент с Mem0 / Letta / Graphiti integration

<!-- toc-auto -->
## Contents

- [Смотрите также](#смотрите-также)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Вариант D: продолжение поиска уникальных проектов и финальное ранжирование.
**Проекты:** NGT Memory, Wikontic

---
<!-- tags: memory, ingestion, architecture, anthropic, collaboration -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Вариант D: продолжение поиска уникальных проектов и финальное ранжирование.

4. AI ассистент с Mem0/Letta/Graphiti integration

Проект: «Память ИИ-агентов: как агенты запоминают, забывают и учатся»

URL: https://habr.com/ru/articles/1012894/

Что есть: Comprehensive guide по memory architectures для AI агентов. Three типа:

Эпизодическая память — события, факты о пользователе

Семантическая память — общая база знаний

Процедурная память — как делать, инструкции

Готовые решения упомянутые:

Mem0 — memory framework

Letta — agentic memory system

Graphiti — graph-based memory

Это off-the-shelf alternatives к building memory layer ourselves. Для SGB Advocate Colleague можно использовать одно из этих вместо building from scratch.

Расширенный landscape — actually impressive

Если суммировать все находки через нашу разговор:

Federation/coordination layer

HMP (kagvi13) — decentralized cognitive mesh

A2A (Google) — agent-to-agent protocol

ANP — Agent Network Protocol

Nautilus Portal Protocol (наш) — domain-specific federation

Memory layer

CoAlly — shared memory для team agents

Graph cognitive memory in SQLite (Виталий) — single-author working implementation

NGT Memory — Hebbian associative graph

Mem0 / Letta / Graphiti — production-ready frameworks

Knowledge representation

Happyin Knowledge Space (Анастасия) — knowledge for AI consumption

Knowledge Graph Kit (Galagher) — MCP wrapper over SQLite + ChromaDB

K2-18 (Романов) — quality metrics

Wikontic (Чепурова) — ontology alignment

Extraction/structuring

Свяжи (Чуян) — hybrid LLM + deterministic

Артём's legal knowledge graph с Louvain community detection

<!-- see-also -->

---

## Использование
```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "AI ассистент с Mem0 Letta Graphiti"
```

## Смотрите также
- [06-final-tier-ranking](06-final-tier-ranking.md)
- [10-collaborators-landscape](../../lorenzo-agent/10-collaborators-landscape.md)
- [354-существующий-landscape-collaborators-твоя-working-](../../02-anthropic-vacancies/354-существующий-landscape-collaborators-твоя-working-.md)
- [03-section-3-solution-architecture](../beneficial-deployments-concept/03-section-3-solution-architecture.md)

