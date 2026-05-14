"""Feature definitions and values for the feature store."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum


class FeatureType(Enum):
    """Supported feature value types."""

    NUMERIC = "numeric"
    CATEGORICAL = "categorical"
    BINARY = "binary"
    TEXT = "text"
    VECTOR = "vector"


@dataclass
class FeatureDefinition:
    """Schema-level descriptor for a single feature."""

    name: str
    feature_type: FeatureType
    description: str = ""
    default_value: object = None
    tags: list[str] = field(default_factory=list)


@dataclass
class FeatureValue:
    """A recorded value for a (entity, feature) pair."""

    entity_id: str
    feature_name: str
    value: object
    ts: float = field(default_factory=time.time)
    version: int = 1
