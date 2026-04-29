# Комбинация 27: Hybrid RAG with AST-Chunked Code

> Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).

Родители:

ASTChunk (structural code chunking)

Graph-RAG (precedent linking)

Crawl4AI (corpus building)

ClickHouse (columnar analytics)

Дети:

Code + legal precedents unified knowledge base

Knowledge base components:
1. Legal decisions (Crawl4AI → ClickHouse)
2. Automation scripts (ASTChunk → vector DB)
3. Graph links (§§ citations + code references)

Query: "How to calculate Widerspruchsfrist for KSV Bescheid?"

Retrieval:
- Graph-RAG: finds precedents citing SGG § 84
- ASTChunk: finds code implementing deadline calc
- ClickHouse: aggregates historical processing times

Output: 
- Legal basis (precedents)
- Implementation (code)
- Statistics (average duration)

Self-documenting legal corpus

Every code chunk links to relevant precedents

Every precedent links to implementation code

Graph shows: Legal rule → Code → Test cases → Decisions

ROI: Developer understands legal context, lawyer sees implementation

Уникальность: First hybrid knowledge graph combining legal texts + code. ASTChunk makes code semantically searchable. Bridges gap between legal theory and practice.
