"""Feature store module — SQLite-backed feature registry and value store."""

from docstoolkit.feature_store.feature import (
    FeatureType,
    FeatureDefinition,
    FeatureValue,
)
from docstoolkit.feature_store.store import FeatureStore

__all__ = [
    "FeatureType",
    "FeatureDefinition",
    "FeatureValue",
    "FeatureStore",
]
