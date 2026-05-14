"""Permission enum and Role dataclass for access control."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, unique


@unique
class Permission(Enum):
    """Available permissions in the docs-toolkit access control system."""

    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"
    SEARCH = "search"
    EXPORT = "export"


@dataclass
class Role:
    """A named collection of permissions assigned to subjects."""

    name: str
    permissions: set[Permission] = field(default_factory=set)
    description: str = ""

    def has_permission(self, perm: Permission) -> bool:
        """Return True if this role includes *perm*."""
        return perm in self.permissions

    def grant(self, perm: Permission) -> None:
        """Add *perm* to this role's permission set."""
        self.permissions.add(perm)

    def revoke(self, perm: Permission) -> None:
        """Remove *perm* from this role's permission set (no-op if absent)."""
        self.permissions.discard(perm)
