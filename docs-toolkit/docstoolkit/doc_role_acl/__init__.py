"""E190 Document role-based ACL — roles, permissions, ACL checks.

Public API
----------
:class:`Permission`    — enum of permissions (READ, WRITE, DELETE, SHARE, ADMIN)
:class:`Role`          — named set of permissions
:class:`User`          — user with assigned roles
:class:`Acl`           — per-document access control list
:class:`AccessResult`  — result of an access check
:class:`DocRoleAcl`    — main ACL manager
"""
from docstoolkit.doc_role_acl.acl import (
    AccessResult,
    Acl,
    DocRoleAcl,
    Permission,
    Role,
    User,
)

__all__ = [
    "AccessResult",
    "Acl",
    "DocRoleAcl",
    "Permission",
    "Role",
    "User",
]
