"""Role-based permission matrix for document access (E284).

Public API
----------
- ``Permission``      — single action + allowed flag
- ``RolePolicy``      — named role with its action→bool permission map
- ``AccessDecision``  — result of a ``DocAccessMatrix.check`` call
- ``MatrixStats``     — aggregate counts for the current matrix state
- ``DocAccessMatrix`` — thread-safe RBAC matrix with explicit doc-level overrides
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class Permission:
    """A single permission entry: an action name and whether it is allowed."""

    action: str
    allowed: bool


@dataclass
class RolePolicy:
    """A named role together with its action → allowed permission map."""

    role: str
    permissions: dict[str, bool] = field(default_factory=dict)


@dataclass
class AccessDecision:
    """The result of a permission check."""

    principal: str
    doc_id: str
    action: str
    allowed: bool
    reason: str  # "explicit", "role:<rolename>", or "default_deny"


@dataclass
class MatrixStats:
    """Aggregate statistics about the current matrix state."""

    total_roles: int
    total_principals: int
    total_explicit_grants: int


# ---------------------------------------------------------------------------
# DocAccessMatrix
# ---------------------------------------------------------------------------

class DocAccessMatrix:
    """Thread-safe role-based permission matrix with per-document overrides.

    Priority order for :meth:`check`:

    1. Explicit doc-level grant/deny  → ``reason="explicit"``
    2. Role-based: allowed if *any* assigned role permits the action
       → ``reason="role:<rolename>"``
    3. Default deny → ``reason="default_deny"``
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()

        # role name → RolePolicy
        self._roles: dict[str, RolePolicy] = {}

        # principal → set of role names
        self._principal_roles: dict[str, set[str]] = {}

        # (principal, doc_id, action) → bool
        self._explicit: dict[tuple[str, str, str], bool] = {}

    # ------------------------------------------------------------------
    # Role management
    # ------------------------------------------------------------------

    def define_role(self, role: str, permissions: dict[str, bool]) -> RolePolicy:
        """Define or replace a role with the given permission set.

        Returns the new :class:`RolePolicy`.
        """
        policy = RolePolicy(role=role, permissions=dict(permissions))
        with self._lock:
            self._roles[role] = policy
        return policy

    def delete_role(self, role: str) -> bool:
        """Delete a role definition and remove all principal assignments.

        Returns ``True`` if the role existed, ``False`` otherwise.
        """
        with self._lock:
            if role not in self._roles:
                return False
            del self._roles[role]
            for principal in self._principal_roles:
                self._principal_roles[principal].discard(role)
        return True

    # ------------------------------------------------------------------
    # Principal → role assignments
    # ------------------------------------------------------------------

    def assign_role(self, principal: str, role: str) -> bool:
        """Assign *role* to *principal*.

        Returns ``True`` on success, ``False`` if the role is not defined.
        """
        with self._lock:
            if role not in self._roles:
                return False
            if principal not in self._principal_roles:
                self._principal_roles[principal] = set()
            self._principal_roles[principal].add(role)
        return True

    def revoke_role(self, principal: str, role: str) -> bool:
        """Remove *role* from *principal*.

        Returns ``True`` if the assignment existed, ``False`` otherwise.
        """
        with self._lock:
            assigned = self._principal_roles.get(principal, set())
            if role not in assigned:
                return False
            assigned.discard(role)
        return True

    def roles_for(self, principal: str) -> list[str]:
        """Return a sorted list of roles assigned to *principal*."""
        with self._lock:
            return sorted(self._principal_roles.get(principal, set()))

    def principals_with_role(self, role: str) -> list[str]:
        """Return a sorted list of principals that have *role* assigned."""
        with self._lock:
            return sorted(
                p for p, roles in self._principal_roles.items() if role in roles
            )

    # ------------------------------------------------------------------
    # Explicit doc-level overrides
    # ------------------------------------------------------------------

    def grant(self, principal: str, doc_id: str, action: str) -> None:
        """Grant an explicit doc-level permission to *principal*."""
        with self._lock:
            self._explicit[(principal, doc_id, action)] = True

    def deny(self, principal: str, doc_id: str, action: str) -> None:
        """Deny an explicit doc-level permission to *principal* (overrides role)."""
        with self._lock:
            self._explicit[(principal, doc_id, action)] = False

    def revoke_explicit(self, principal: str, doc_id: str, action: str) -> bool:
        """Remove an explicit grant/deny entry.

        Returns ``True`` if an entry existed, ``False`` otherwise.
        """
        with self._lock:
            key = (principal, doc_id, action)
            if key not in self._explicit:
                return False
            del self._explicit[key]
        return True

    # ------------------------------------------------------------------
    # Permission check
    # ------------------------------------------------------------------

    def check(self, principal: str, doc_id: str, action: str) -> AccessDecision:
        """Check whether *principal* may perform *action* on *doc_id*.

        Priority:

        1. Explicit doc-level entry (grant or deny).
        2. Role-based: allowed if *any* assigned role has the action mapped to
           ``True``.  The first matching role name is used in the reason string.
        3. Default deny.
        """
        with self._lock:
            # 1. Explicit override
            key = (principal, doc_id, action)
            if key in self._explicit:
                allowed = self._explicit[key]
                return AccessDecision(
                    principal=principal,
                    doc_id=doc_id,
                    action=action,
                    allowed=allowed,
                    reason="explicit",
                )

            # 2. Role-based check
            assigned_roles = sorted(self._principal_roles.get(principal, set()))
            for role_name in assigned_roles:
                policy = self._roles.get(role_name)
                if policy is None:
                    continue
                if policy.permissions.get(action) is True:
                    return AccessDecision(
                        principal=principal,
                        doc_id=doc_id,
                        action=action,
                        allowed=True,
                        reason=f"role:{role_name}",
                    )

            # 3. Default deny
            return AccessDecision(
                principal=principal,
                doc_id=doc_id,
                action=action,
                allowed=False,
                reason="default_deny",
            )

    # ------------------------------------------------------------------
    # Bulk principal removal
    # ------------------------------------------------------------------

    def delete_principal(self, principal: str) -> None:
        """Remove all role assignments and explicit permissions for *principal*."""
        with self._lock:
            self._principal_roles.pop(principal, None)
            keys_to_remove = [k for k in self._explicit if k[0] == principal]
            for k in keys_to_remove:
                del self._explicit[k]

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    def stats(self) -> MatrixStats:
        """Return aggregate counts for the current matrix state."""
        with self._lock:
            total_explicit = sum(1 for v in self._explicit.values() if v is True)
            return MatrixStats(
                total_roles=len(self._roles),
                total_principals=len(self._principal_roles),
                total_explicit_grants=total_explicit,
            )
