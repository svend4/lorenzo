# Комбинация 17: Distributed Agent Memory with Graph

<!-- summary -->
> > Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).
**Проекты:** NGT Memory, Yjs, Automerge

---
<!-- tags: memory, rag, local-first, self-improvement -->




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

**Смотрите также:**
- [20-hybrid-olap-oltp-with-real-time-sync](docs/technology-combinations/combinations/20-hybrid-olap-oltp-with-real-time-sync.md)
- [15-self-consolidating-legal-corpus](docs/technology-combinations/combinations/15-self-consolidating-legal-corpus.md)
- [11-hybrid-crdt-sql-database](docs/technology-combinations/combinations/11-hybrid-crdt-sql-database.md)
- [15-19-extended](docs/technology-combinations/synthesis-tables/15-19-extended.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [20-hybrid-olap-oltp-with-real-time-sync](docs/technology-combinations/combinations/20-hybrid-olap-oltp-with-real-time-sync.md) (сходство 0.29)
- [11-hybrid-crdt-sql-database](docs/technology-combinations/combinations/11-hybrid-crdt-sql-database.md) (сходство 0.28)
- [15-19-extended](docs/technology-combinations/synthesis-tables/15-19-extended.md) (сходство 0.25)

