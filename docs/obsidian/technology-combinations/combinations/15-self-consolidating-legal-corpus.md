---
title: "Комбинация 15: Self-Consolidating Legal Corpus"
tags:
  - technology-combinations
date: 2026-04-29
---

# Комбинация 15: Self-Consolidating Legal Corpus

<!-- summary -->
> > Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).

---
<!-- tags: memory, knowledge, self-improvement -->




> Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).

Родители:

Crawl4AI (GitHub 60k+ stars, LLM-optimized web scraping, markdown generation)

Docling (IBM Research, structured DoclingDocument)

Ebbinghaus memory decay (agent-second-brain, agentmemory MCP)

Дети:

Auto-updating legal knowledge base with decay

Crawl4AI scrapes Sozialgericht decisions nightly (BM25 filtering, BFS deep crawl)

Docling structures PDF→DoclingDocument (preserves headings, citations, §§)

Ebbinghaus decay: unused precedents fade from active memory

Consolidation: frequently-cited precedents strengthen, auto-promote to "core knowledge"

Architecture:

Daily: Crawl4AI → Sozialgericht RSS/search
Parse: Docling → structured decisions
Memory: agentmemory MCP → Ebbinghaus scoring
Active tier: accessed <7d (instant recall)
Archive tier: >90d, resurfaces randomly for creative connections

Wikipedia-style legal wiki with auto-decay

Each Bescheid/Urteil = markdown page in Obsidian vault

Crawl4AI extracts clean markdown (fit markdown, removes noise)

agentmemory MCP tracks: last accessed, access frequency

Auto-wikilink between related precedents

Vault health scoring: broken links, orphaned files, tag divergence

ROI: Self-maintaining corpus, stale precedents auto-archive

Уникальность: Первая система, применяющая Ebbinghaus decay к legal knowledge. Корпус "забывает" нерелевантные прецеденты, focus на frequently-used.

<!-- see-also -->

---

**Смотрите также:**
- [[17-distributed-agent-memory-with-graph]]
- [[10-legal-document-intelligence-pipeline]]
- [[07-crawl4ai-docling-yodoca-consolidator]]
- [[18-llm-powered-legal-corpus-builder]]


<!-- similar-docs -->

---

**Похожие документы:**
- [[10-legal-document-intelligence-pipeline]] (сходство 0.26)
- [[07-crawl4ai-docling-yodoca-consolidator]] (сходство 0.24)
- [[17-distributed-agent-memory-with-graph]] (сходство 0.24)

