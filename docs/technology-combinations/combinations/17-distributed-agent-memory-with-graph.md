# Комбинация 17: Distributed Agent Memory with Graph

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
