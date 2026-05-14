"""In-memory full-text search engine (E108).

Provides BM25-scored search over multi-field documents using a pure
stdlib inverted index — no external dependencies required.

Quick-start
-----------
>>> from docstoolkit.search_engine import SearchEngine, Document
>>> engine = SearchEngine()
>>> engine.add(Document("d1", {"title": "Hello world", "body": "A test doc"}))
>>> results = engine.search("hello")
>>> results[0].doc_id
'd1'
"""
from docstoolkit.search_engine.engine import Document, SearchEngine, SearchResult

__all__ = ["Document", "SearchEngine", "SearchResult"]
