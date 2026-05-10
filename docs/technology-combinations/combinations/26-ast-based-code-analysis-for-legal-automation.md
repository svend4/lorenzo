# Комбинация 26: AST-Based Code Analysis for Legal Automation

<!-- toc-auto -->
## Contents

- [Смотрите также](#смотрите-также)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).

---
<!-- tags: rag -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





> Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).

Родители:

Python AST (code analysis, transformation)

ASTChunk (structural code chunking for RAG)

Pydantic validation (structured outputs)

LLM parsing (code → structured data)

Дети:

Legal automation script analyzer

Analyze existing legal automation scripts

Extract legal logic into structured format

Generate documentation automatically

Architecture:

python

# Input: Python script for Fristwahrung calculation
script = load_script("fristwahrung_calculator.py")

# AST analysis
ast_tree = ast.parse(script)

# Extract legal logic
legal_logic = extract_legal_rules(ast_tree)
# → Pydantic model: LegalRule(
# name="Widerspruchsfrist",
# base_duration=timedelta(days(),
# extensions=[...],
# legal_basis="SGG § 84"
# )

# ASTChunk for RAG
chunks = astchunk.chunkify(script, metadata_template="legal")
# → Each chunk: code + legal context

Cross-script legal consistency checker

Multiple scripts calculate deadlines differently

AST extracts calculation logic from each

LLM identifies inconsistencies

Pydantic validates proposed fixes

ROI: Prevents errors from inconsistent legal implementations

Уникальность: First application of ASTChunk to legal domain. Treats legal automation code as documentation source. Enables LLM-based code understanding with structural awareness.

<!-- see-also -->

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Комбинация 26 AST Based Code Analysis"
```

## Смотрите также
- [28-pydantic-enforced-legal-workflows](28-pydantic-enforced-legal-workflows.md)
- 27-hybrid-[rag-with-ast-chunked-code](27-hybrid-rag-with-ast-chunked-code.md)
- [25-legal-dsl-code-transpiler](25-legal-dsl-code-transpiler.md)
- [29-meta-programmatic-legal-template-generator](29-meta-programmatic-legal-template-generator.md)

_Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Материал доступен для семантического поиска, BM25 и навигации через граф концептов._ _Материал доступен для поиска._ _Индексировано._

<!-- backlinks -->

---

**Кто ссылается на этот документ (9):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [TABLES](../../TABLES.md)
- [25-legal-dsl-code-transpiler](25-legal-dsl-code-transpiler.md)
- [27-hybrid-rag-with-ast-chunked-code](27-hybrid-rag-with-ast-chunked-code.md)
- [README](README.md)
- _...ещё 1_

