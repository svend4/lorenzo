"""Embeddings provider для семантического поиска.

Архитектура:
  - Provider — общий интерфейс (encode, similarity)
  - TFIDFProvider — без зависимостей, baseline (всегда работает)
  - SentenceTransformersProvider — опциональный (требует sentence-transformers)
  - HybridSearcher — комбинирует keyword + semantic с весами

Конфиг (docstoolkit.toml):
  [embeddings]
  provider = "tfidf"        # или "sentence-transformers"
  model = "all-MiniLM-L6-v2"  # для st
  cache_dir = ".docstoolkit/cache/embeddings"
  hybrid_weights = {keyword = 0.4, semantic = 0.6}
"""
from docstoolkit.embeddings.base import EmbeddingProvider, SearchResult
from docstoolkit.embeddings.tfidf import TFIDFProvider
from docstoolkit.embeddings.dispatch import get_provider, list_providers
from docstoolkit.embeddings.hybrid import HybridSearcher

__all__ = [
    "EmbeddingProvider", "SearchResult",
    "TFIDFProvider", "HybridSearcher",
    "get_provider", "list_providers",
]
