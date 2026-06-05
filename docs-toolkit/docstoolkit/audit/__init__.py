"""Audit log: immutable event log with hash-chain tamper detection."""
from docstoolkit.audit.event import AuditEvent, EventCategory
from docstoolkit.audit.log import AuditLog
from docstoolkit.audit.verifier import AuditVerifier, VerificationReport

__all__ = [
    "AuditEvent", "EventCategory",
    "AuditLog",
    "AuditVerifier", "VerificationReport",
]
