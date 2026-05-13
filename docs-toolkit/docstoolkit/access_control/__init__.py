"""Access control module for docs-toolkit.

Public API
----------
- ``Permission``       — enum of available permissions (READ, WRITE, DELETE, ADMIN, SEARCH, EXPORT)
- ``Role``             — named permission set
- ``Subject``          — entity requesting access
- ``Resource``         — resource being accessed
- ``AccessDecision``   — ALLOW / DENY / NOT_APPLICABLE
- ``AccessPolicy``     — abstract base for policies
- ``OwnerPolicy``      — owner always gets ALLOW
- ``RolePolicy``       — RBAC via role-permission mapping
- ``DenyAllPolicy``    — unconditional DENY sentinel
- ``AccessEnforcer``   — ordered policy chain with first-match semantics
- ``AccessDeniedError`` — raised by ``AccessEnforcer.require`` on denial
"""

from docstoolkit.access_control.permission import Permission, Role
from docstoolkit.access_control.policy import (
    Subject,
    Resource,
    AccessDecision,
    AccessPolicy,
    OwnerPolicy,
    RolePolicy,
    DenyAllPolicy,
)
from docstoolkit.access_control.enforcer import AccessEnforcer, AccessDeniedError

__all__ = [
    "Permission",
    "Role",
    "Subject",
    "Resource",
    "AccessDecision",
    "AccessPolicy",
    "OwnerPolicy",
    "RolePolicy",
    "DenyAllPolicy",
    "AccessEnforcer",
    "AccessDeniedError",
]
