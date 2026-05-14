"""E236 Document role-based access control v2 — inheritance + ABAC policies.

Public API
----------
:class:`Permission`     — enum of permissions
:class:`RoleDefinition` — role with permissions and parent roles
:class:`UserBinding`    — user-to-role binding with attributes
:class:`Policy`         — ABAC-style policy with condition callable
:class:`AccessRequest`  — request for an access decision
:class:`AccessDecision` — decision returned by :meth:`DocRoleV2.check_access`
:class:`DocRoleV2`      — main access-control manager
"""
from docstoolkit.doc_role_v2.role import (
    AccessDecision,
    AccessRequest,
    DocRoleV2,
    Permission,
    Policy,
    RoleDefinition,
    UserBinding,
)

__all__ = [
    "AccessDecision",
    "AccessRequest",
    "DocRoleV2",
    "Permission",
    "Policy",
    "RoleDefinition",
    "UserBinding",
]
