"""Cross-encoder реранкинг для docs-toolkit.

Использование:
    from docstoolkit.rerank import rerank, get_reranker, TFIDFReranker

    passages = retrieve_passages(query, top_k=20)
    reranked = rerank(query, passages, TFIDFReranker(), top_k=5)

    # Или через фабрику:
    reranker = get_reranker("bge")   # fallback на tfidf при отсутствии зависимостей
    reranked = rerank(query, passages, reranker, top_k=5)
"""
from docstoolkit.rerank.reranker import (
    Reranker,
    NoOpReranker,
    TFIDFReranker,
    LLMReranker,
    BGEReranker,
    rerank,
    get_reranker,
)

__all__ = [
    "Reranker",
    "NoOpReranker",
    "TFIDFReranker",
    "LLMReranker",
    "BGEReranker",
    "rerank",
    "get_reranker",
]
