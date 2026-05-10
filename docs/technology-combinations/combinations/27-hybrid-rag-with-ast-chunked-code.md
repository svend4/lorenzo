# Комбинация 27: Hybrid RAG with AST-Chunked Code

<!-- toc-auto -->
## Contents

- [Смотрите также](#смотрите-также)
- [Кто ссылается на этот документ (3)](#кто-ссылается-на-этот-документ-3)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).
**Проекты:** Hybrid RAG

---
<!-- tags: rag, self-improvement -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





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

<!-- see-also -->

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Комбинация 27 Hybrid RAG with AST"
```

## Смотрите также
- [03-dsl-ast](../mega-stacks/03-dsl-ast.md)
- [26-ast-based-code-analysis-for-legal-automation](26-ast-based-code-analysis-for-legal-automation.md)
- [10-legal-document-intelligence-pipeline](10-legal-document-intelligence-pipeline.md)
- [25-30-extended](../synthesis-tables/25-30-extended.md)


<!-- backlinks -->

---

## Кто ссылается на этот документ (3)
- [components-by-name](../../glossary/components-by-name.md)
- [README](README.md)
- [25-30-extended](../synthesis-tables/25-30-extended.md)

_Материал индексирован и доступен для поиска, BM25 и навигации через граф концептов._ _Документ доступен для семантического поиска._ _Индексировано._
