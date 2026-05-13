"""Consent manager module — GDPR-style user consent tracking backed by SQLite.

Public API
----------
- ``ConsentStatus``   — enum: GRANTED / WITHDRAWN / PENDING
- ``ConsentRecord``   — dataclass representing one consent decision
- ``ConsentManager``  — manages consent records with full CRUD + audit trail
"""
from docstoolkit.consent_manager.models import ConsentRecord, ConsentStatus
from docstoolkit.consent_manager.manager import ConsentManager

__all__ = [
    "ConsentStatus",
    "ConsentRecord",
    "ConsentManager",
]
