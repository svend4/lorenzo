"""Document Glossary module (E251).

CRUD-style glossary manager with auto-linking. Manages terms, definitions,
examples, synonyms, related terms, and category-based grouping.

Different from `glossary_builder` (E131) which builds a glossary from text.
This module provides a managed glossary with add/update/remove operations
and the ability to auto-link mentions of registered terms inside text.

Usage:
    from docstoolkit.doc_glossary import DocGlossary, Term, GlossaryStats

    g = DocGlossary()
    g.add_term("RAG", "Retrieval-Augmented Generation", category="ai",
               synonyms=["retrieval augmented generation"],
               examples=["LangChain", "LlamaIndex"])
    g.add_term("LLM", "Large Language Model", category="ai")

    linked = g.auto_link("RAG combines retrieval with an LLM.")
    md = g.to_markdown()
"""
from docstoolkit.doc_glossary.glossary import (
    DocGlossary,
    GlossaryStats,
    Term,
)

__all__ = [
    "DocGlossary",
    "GlossaryStats",
    "Term",
]
