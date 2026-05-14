"""E336 DocRoleStore — role and permission assignment for users on documents.

Stdlib-only, thread-safe role-based permission store. Each (doc_id, user_id)
pair has at most one role assigned. Roles define the set of permissions
they grant.
"""
from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass
class Role:
    """A named role and the permissions it grants."""

    name: str
    permissions: List[str] = field(default_factory=list)
    description: str = ""


@dataclass
class RoleAssignment:
    """A user's role on a document."""

    doc_id: str
    user_id: str
    role_name: str
    assigned_at: float = 0.0
    assigned_by: str = ""


@dataclass
class RoleStats:
    """Aggregate counts across the store."""

    total_roles: int
    total_assignments: int
    unique_users: int
    unique_docs: int


class DocRoleStore:
    """In-memory store of role definitions and user assignments.

    Internal storage:
        * ``_roles``        – name → :class:`Role`
        * ``_assignments``  – (doc_id, user_id) → :class:`RoleAssignment`

    All mutations are protected by a single :class:`threading.Lock`.
    """

    def __init__(self) -> None:
        self._roles: Dict[str, Role] = {}
        self._assignments: Dict[Tuple[str, str], RoleAssignment] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------ Roles
    def define_role(self, role: Role) -> None:
        """Register or replace a role definition."""
        with self._lock:
            self._roles[role.name] = role

    def undefine_role(self, name: str) -> bool:
        """Remove a role and all of its assignments.

        Returns True if the role existed prior to the call.
        """
        with self._lock:
            if name not in self._roles:
                return False
            del self._roles[name]
            stale_keys = [
                key
                for key, assignment in self._assignments.items()
                if assignment.role_name == name
            ]
            for key in stale_keys:
                del self._assignments[key]
            return True

    def get_role(self, name: str) -> Optional[Role]:
        with self._lock:
            return self._roles.get(name)

    def list_roles(self) -> List[Role]:
        """Return all roles sorted by name."""
        with self._lock:
            return [self._roles[name] for name in sorted(self._roles)]

    # ------------------------------------------------------------ Assignments
    def assign(
        self,
        doc_id: str,
        user_id: str,
        role_name: str,
        assigned_by: str = "",
        now: Optional[float] = None,
    ) -> Optional[RoleAssignment]:
        """Create or replace an assignment.

        Returns the new :class:`RoleAssignment` or ``None`` if *role_name*
        has not been defined.
        """
        timestamp = now if now is not None else time.time()
        with self._lock:
            if role_name not in self._roles:
                return None
            assignment = RoleAssignment(
                doc_id=doc_id,
                user_id=user_id,
                role_name=role_name,
                assigned_at=timestamp,
                assigned_by=assigned_by,
            )
            self._assignments[(doc_id, user_id)] = assignment
            return assignment

    def unassign(self, doc_id: str, user_id: str) -> bool:
        """Remove a user's assignment on a doc. Returns True if it existed."""
        with self._lock:
            key = (doc_id, user_id)
            if key not in self._assignments:
                return False
            del self._assignments[key]
            return True

    def get_assignment(
        self, doc_id: str, user_id: str
    ) -> Optional[RoleAssignment]:
        with self._lock:
            return self._assignments.get((doc_id, user_id))

    # ------------------------------------------------------------------- Views
    def users_for_doc(self, doc_id: str) -> List[str]:
        """Return sorted user_ids that have any role on *doc_id*."""
        with self._lock:
            users = {
                assignment.user_id
                for (did, _uid), assignment in self._assignments.items()
                if did == doc_id
            }
        return sorted(users)

    def docs_for_user(self, user_id: str) -> List[str]:
        """Return sorted doc_ids where *user_id* holds a role."""
        with self._lock:
            docs = {
                assignment.doc_id
                for (_did, uid), assignment in self._assignments.items()
                if uid == user_id
            }
        return sorted(docs)

    def users_with_permission(
        self, doc_id: str, permission: str
    ) -> List[str]:
        """Return sorted user_ids on *doc_id* whose role grants *permission*."""
        with self._lock:
            users: List[str] = []
            for (did, uid), assignment in self._assignments.items():
                if did != doc_id:
                    continue
                role = self._roles.get(assignment.role_name)
                if role is None:
                    continue
                if permission in role.permissions:
                    users.append(uid)
        return sorted(users)

    def has_permission(
        self, user_id: str, doc_id: str, permission: str
    ) -> bool:
        """Return True iff *user_id* has a role on *doc_id* granting *permission*."""
        with self._lock:
            assignment = self._assignments.get((doc_id, user_id))
            if assignment is None:
                return False
            role = self._roles.get(assignment.role_name)
            if role is None:
                return False
            return permission in role.permissions

    def assignments_for_role(self, role_name: str) -> List[RoleAssignment]:
        """Return all assignments using *role_name* sorted by (doc_id, user_id)."""
        with self._lock:
            matches = [
                assignment
                for assignment in self._assignments.values()
                if assignment.role_name == role_name
            ]
        return sorted(matches, key=lambda a: (a.doc_id, a.user_id))

    # --------------------------------------------------------------- Maintenance
    def clear_doc(self, doc_id: str) -> int:
        """Remove every assignment for *doc_id*; return how many were removed."""
        with self._lock:
            keys = [key for key in self._assignments if key[0] == doc_id]
            for key in keys:
                del self._assignments[key]
            return len(keys)

    def clear_user(self, user_id: str) -> int:
        """Remove every assignment for *user_id*; return how many were removed."""
        with self._lock:
            keys = [key for key in self._assignments if key[1] == user_id]
            for key in keys:
                del self._assignments[key]
            return len(keys)

    def stats(self) -> RoleStats:
        """Aggregate statistics over the store."""
        with self._lock:
            users = {key[1] for key in self._assignments}
            docs = {key[0] for key in self._assignments}
            return RoleStats(
                total_roles=len(self._roles),
                total_assignments=len(self._assignments),
                unique_users=len(users),
                unique_docs=len(docs),
            )


__all__ = ["Role", "RoleAssignment", "RoleStats", "DocRoleStore"]
