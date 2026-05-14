"""E336 DocRoleStore — role and permission assignment for users on documents.

Public API
----------
:class:`Role`             — a named role with permissions
:class:`RoleAssignment`   — a user's role on a document
:class:`RoleStats`        — aggregate statistics
:class:`DocRoleStore`     — main interface for role management
"""

from .store import Role, RoleAssignment, RoleStats, DocRoleStore

__all__ = ["Role", "RoleAssignment", "RoleStats", "DocRoleStore"]
