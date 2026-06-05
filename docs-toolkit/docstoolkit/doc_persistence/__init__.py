"""Persistent document store with versioning (E272)."""

from .persistence import DocPersistence, PersistedDoc, PersistenceStats

__all__ = ["DocPersistence", "PersistedDoc", "PersistenceStats"]
