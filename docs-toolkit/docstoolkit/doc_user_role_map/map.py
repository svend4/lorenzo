"""Global user role mapping.

This module provides a thread-safe registry of role definitions and
user-to-role assignments. Roles carry a list of permissions; permissions
are aggregated across all roles assigned to a user.

The map is *global* — assignments are not scoped to a specific document.
For per-document access control see :mod:`docstoolkit.doc_role_acl`.
"""
from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set


@dataclass
class UserRole:
    """A single role assignment to a user."""

    user_id: str
    role: str
    assigned_at: float = 0.0
    assigned_by: str = ""


@dataclass
class RoleDefinition:
    """A defined role with its permission set."""

    role: str
    permissions: List[str] = field(default_factory=list)
    description: str = ""


@dataclass
class UserRoleStats:
    """Aggregate statistics over the role map."""

    total_roles: int = 0
    total_users: int = 0
    role_counts: Dict[str, int] = field(default_factory=dict)


class DocUserRoleMap:
    """Thread-safe global user role map."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._roles: Dict[str, RoleDefinition] = {}
        self._user_roles: Dict[str, Set[str]] = {}
        self._history: List[UserRole] = []

    # ----------------------------------------------------------- definitions
    def define_role(self, role: RoleDefinition) -> None:
        """Create or overwrite a role definition."""
        with self._lock:
            self._roles[role.role] = RoleDefinition(
                role=role.role,
                permissions=list(role.permissions),
                description=role.description,
            )

    def undefine_role(self, role: str) -> bool:
        """Remove a role globally; cascades to all user assignments."""
        with self._lock:
            if role not in self._roles:
                return False
            del self._roles[role]
            empty_users: List[str] = []
            for user_id, roles in self._user_roles.items():
                roles.discard(role)
                if not roles:
                    empty_users.append(user_id)
            for user_id in empty_users:
                del self._user_roles[user_id]
            return True

    def get_role(self, role: str) -> Optional[RoleDefinition]:
        """Return a role definition or ``None`` if not defined."""
        with self._lock:
            rd = self._roles.get(role)
            if rd is None:
                return None
            return RoleDefinition(
                role=rd.role,
                permissions=list(rd.permissions),
                description=rd.description,
            )

    def list_roles(self) -> List[RoleDefinition]:
        """Return all role definitions, sorted by role name."""
        with self._lock:
            return [
                RoleDefinition(
                    role=rd.role,
                    permissions=list(rd.permissions),
                    description=rd.description,
                )
                for rd in sorted(self._roles.values(), key=lambda r: r.role)
            ]

    # ------------------------------------------------------------ assignments
    def assign(
        self,
        user_id: str,
        role: str,
        assigned_by: str = "",
        now: Optional[float] = None,
    ) -> Optional[UserRole]:
        """Assign ``role`` to ``user_id``.

        Returns the recorded :class:`UserRole` or ``None`` if the role
        has not been defined.
        """
        with self._lock:
            if role not in self._roles:
                return None
            ts = now if now is not None else time.time()
            entry = UserRole(
                user_id=user_id,
                role=role,
                assigned_at=ts,
                assigned_by=assigned_by,
            )
            self._user_roles.setdefault(user_id, set()).add(role)
            self._history.append(entry)
            return UserRole(
                user_id=entry.user_id,
                role=entry.role,
                assigned_at=entry.assigned_at,
                assigned_by=entry.assigned_by,
            )

    def revoke(self, user_id: str, role: str) -> bool:
        """Remove ``role`` from ``user_id``. Returns ``True`` if removed."""
        with self._lock:
            roles = self._user_roles.get(user_id)
            if not roles or role not in roles:
                return False
            roles.discard(role)
            if not roles:
                del self._user_roles[user_id]
            return True

    def roles_of(self, user_id: str) -> List[str]:
        """Return the user's roles, sorted."""
        with self._lock:
            roles = self._user_roles.get(user_id)
            if not roles:
                return []
            return sorted(roles)

    def users_with_role(self, role: str) -> List[str]:
        """Return user ids holding ``role``, sorted."""
        with self._lock:
            return sorted(
                user_id
                for user_id, roles in self._user_roles.items()
                if role in roles
            )

    def has_role(self, user_id: str, role: str) -> bool:
        """Return whether ``user_id`` holds ``role``."""
        with self._lock:
            roles = self._user_roles.get(user_id)
            return bool(roles) and role in roles

    # ------------------------------------------------------------ permissions
    def has_permission(self, user_id: str, permission: str) -> bool:
        """Return whether any of the user's roles grants ``permission``."""
        with self._lock:
            roles = self._user_roles.get(user_id)
            if not roles:
                return False
            for role in roles:
                rd = self._roles.get(role)
                if rd is not None and permission in rd.permissions:
                    return True
            return False

    def permissions_for(self, user_id: str) -> List[str]:
        """Return the sorted union of permissions across the user's roles."""
        with self._lock:
            roles = self._user_roles.get(user_id)
            if not roles:
                return []
            perms: Set[str] = set()
            for role in roles:
                rd = self._roles.get(role)
                if rd is not None:
                    perms.update(rd.permissions)
            return sorted(perms)

    # --------------------------------------------------------------- cleanup
    def clear_user(self, user_id: str) -> int:
        """Remove all role assignments for ``user_id``.

        Returns the number of roles removed.
        """
        with self._lock:
            roles = self._user_roles.pop(user_id, None)
            return len(roles) if roles else 0

    # --------------------------------------------------------------- history
    def history(self, user_id: Optional[str] = None) -> List[UserRole]:
        """Return the assignment history in chronological order.

        If ``user_id`` is provided, only that user's entries are returned.
        """
        with self._lock:
            entries = self._history
            if user_id is not None:
                entries = [e for e in entries if e.user_id == user_id]
            return [
                UserRole(
                    user_id=e.user_id,
                    role=e.role,
                    assigned_at=e.assigned_at,
                    assigned_by=e.assigned_by,
                )
                for e in entries
            ]

    # ----------------------------------------------------------------- stats
    def stats(self) -> UserRoleStats:
        """Return aggregate statistics."""
        with self._lock:
            role_counts: Dict[str, int] = {role: 0 for role in self._roles}
            for roles in self._user_roles.values():
                for role in roles:
                    if role in role_counts:
                        role_counts[role] += 1
                    else:
                        role_counts[role] = role_counts.get(role, 0) + 1
            return UserRoleStats(
                total_roles=len(self._roles),
                total_users=len(self._user_roles),
                role_counts=role_counts,
            )
