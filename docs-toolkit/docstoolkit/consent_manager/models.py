"""Data models for the consent manager."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class ConsentStatus(str, Enum):
    """Lifecycle status of a consent record."""

    GRANTED = "granted"
    WITHDRAWN = "withdrawn"
    PENDING = "pending"


@dataclass
class ConsentRecord:
    """Represents a single user consent decision for one processing purpose."""

    user_id: str
    purpose: str
    status: ConsentStatus
    version: int = 1
    granted_at: Optional[float] = None
    withdrawn_at: Optional[float] = None
    metadata: dict = field(default_factory=dict)
