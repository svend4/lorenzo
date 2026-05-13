"""Embedding store module — pure-stdlib in-memory vector store."""

from docstoolkit.embedding_store.vector import EmbeddingVector
from docstoolkit.embedding_store.store import StoreConfig, EmbeddingStore
from docstoolkit.embedding_store.persistence import EmbeddingPersistence

__all__ = [
    "EmbeddingVector",
    "StoreConfig",
    "EmbeddingStore",
    "EmbeddingPersistence",
]
