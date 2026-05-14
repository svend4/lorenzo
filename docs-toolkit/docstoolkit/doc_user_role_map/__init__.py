"""E389 DocUserRoleMap — global user role mapping (independent of docs).

Public API
----------
:class:`UserRole`         — a user's global role
:class:`RoleDefinition`   — a defined role
:class:`UserRoleStats`    — aggregate statistics
:class:`DocUserRoleMap`   — main interface for user role management
"""

from .map import UserRole, RoleDefinition, UserRoleStats, DocUserRoleMap

__all__ = ["UserRole", "RoleDefinition", "UserRoleStats", "DocUserRoleMap"]
