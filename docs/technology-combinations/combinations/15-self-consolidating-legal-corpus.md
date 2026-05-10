# Комбинация 15: Self-Consolidating Legal Corpus

<!-- toc-auto -->
## Contents

- [Смотрите также](#смотрите-также)
- [Кто ссылается на этот документ (3)](#кто-ссылается-на-этот-документ-3)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).

---
<!-- tags: memory, knowledge, self-improvement -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





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

## Смотрите также
- [17-distributed-agent-memory-with-graph](17-distributed-agent-memory-with-graph.md)
- [10-legal-document-intelligence-pipeline](10-legal-document-intelligence-pipeline.md)
- 07-crawl4ai-docling-[yodoca-consolidator](07-crawl4ai-docling-yodoca-consolidator.md)
- 18-[llm-powered-legal-corpus-builder](18-llm-powered-legal-corpus-builder.md)


<!-- backlinks -->

---

## Кто ссылается на этот документ (3)
- [components-by-name](../../glossary/components-by-name.md)
- [README](README.md)
- [15-19-extended](../synthesis-tables/15-19-extended.md)

