"""Регистр провайдеров embeddings."""
from typing import Type

from docstoolkit.embeddings.base import EmbeddingProvider
from docstoolkit.embeddings.tfidf import TFIDFProvider


_REGISTRY: dict[str, Type[EmbeddingProvider]] = {
    "tfidf": TFIDFProvider,
}


def list_providers() -> list[str]:
    return sorted(_REGISTRY)


def get_provider(name: str = "tfidf", **kwargs) -> EmbeddingProvider:
    """Возвращает инстанс провайдера. fallback на tfidf если запрошенный недоступен."""
    if name == "sentence-transformers":
        try:
            from docstoolkit.embeddings.sentence_transformers import SentenceTransformersProvider
            return SentenceTransformersProvider(**kwargs)
        except ImportError:
            pass  # fallback
    if name not in _REGISTRY:
        name = "tfidf"
    return _REGISTRY[name](**kwargs)


def register(name: str, cls: Type[EmbeddingProvider]):
    """Регистрация custom провайдера."""
    _REGISTRY[name] = cls
