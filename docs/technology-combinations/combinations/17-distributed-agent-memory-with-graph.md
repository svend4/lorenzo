# Комбинация 17: Distributed Agent Memory with Graph

<!-- toc-auto -->
## Contents

- [Смотрите также](#смотрите-также)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).
**Проекты:** NGT Memory, Yjs, Automerge

---
<!-- tags: memory, rag, local-first, self-improvement -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





> Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).

Родители:

agentmemory MCP (51 tools, Ebbinghaus decay, memory consolidation)

CRDT offline-first (Yjs/Automerge)

Graph-RAG (Microsoft Research, graph-based retrieval)

NGT Memory (Hebbian associative graph)

Дети:

P2P agent knowledge graph with biological decay

Each agent instance has local graph (NGT Memory, Hebbian learning)

CRDT syncs graphs P2P (conflict-free merge of nodes/edges)

agentmemory MCP: Ebbinghaus decay on nodes

Frequently co-accessed nodes strengthen connections (Hebbian)

Consolidation: episodic memories → semantic facts

Example: "Aktenzeichen S 7 SO 99/25" + "BSG B 8 SO 9/19 R" accessed together → edge strengthens

Multi-agent legal research with shared memory

Agent A researches precedents, stores graph locally

Agent B (different device) researches legislation

CRDT merges graphs → both agents see combined knowledge

Ebbinghaus: unused precedents decay, frequently-cited survive

ROI: Distributed research without central server, knowledge compounds

Уникальность: Biological memory (Hebbian, Ebbinghaus) + distributed sync (CRDT) + graph structure (NGT, Graph-RAG). Первая децентрализованная система с когнитивной памятью.

<!-- see-also -->

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Комбинация 17 Distributed Agent Memory"
```

## Смотрите также
- [20-hybrid-olap-oltp-with-real-time-sync](20-hybrid-olap-oltp-with-real-time-sync.md)
- [15-self-consolidating-legal-corpus](15-self-consolidating-legal-corpus.md)
- 11-hybrid-crdt-[sql-database](11-hybrid-crdt-sql-database.md)
- [15-19-extended](../synthesis-tables/15-19-extended.md)

_Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ индексирован в поисковой базе репозитория и доступен для поиска._ _Доступен семантический поиск._ _Индексировано._
