"""Role-based ACL for documents.

Logic
-----
- Owner has ALL permissions on their document.
- Effective permissions for a user on a document are the union of:
  - user_grants[user_id]
  - role_grants[role] for every role the user has
  - public_perms
- A user holding :data:`Permission.ADMIN` (via any source) implicitly holds
  every other permission for that document.
"""
from __future__ import annotations

import threading
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set


class Permission(Enum):
    """Available document permissions."""

    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    SHARE = "share"
    ADMIN = "admin"


ALL_PERMISSIONS: Set[Permission] = {
    Permission.READ,
    Permission.WRITE,
    Permission.DELETE,
    Permission.SHARE,
    Permission.ADMIN,
}


@dataclass
class Role:
    """Named set of permissions."""

    name: str
    permissions: Set[Permission] = field(default_factory=set)
    description: str = ""


@dataclass
class User:
    """User with a set of assigned role names."""

    user_id: str
    roles: Set[str] = field(default_factory=set)


@dataclass
class Acl:
    """Per-document access control list."""

    doc_id: str
    owner: str
    role_grants: Dict[str, Set[Permission]] = field(default_factory=dict)
    user_grants: Dict[str, Set[Permission]] = field(default_factory=dict)
    public_perms: Set[Permission] = field(default_factory=set)


@dataclass
class AccessResult:
    """Result of an access check."""

    allowed: bool
    reason: str
    via: Optional[str] = None


def _expand_admin(perms: Set[Permission]) -> Set[Permission]:
    """If ADMIN is present, expand to all permissions."""
    if Permission.ADMIN in perms:
        return set(ALL_PERMISSIONS)
    return set(perms)


class DocRoleAcl:
    """Role-based ACL manager for documents."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._roles: Dict[str, Role] = {}
        self._users: Dict[str, User] = {}
        self._acls: Dict[str, Acl] = {}

    # ------------------------------------------------------------------ roles
    def define_role(
        self,
        name: str,
        permissions: Set[Permission],
        description: str = "",
    ) -> Role:
        """Create or overwrite a role definition."""
        with self._lock:
            role = Role(name=name, permissions=set(permissions), description=description)
            self._roles[name] = role
            return role

    def remove_role(self, name: str) -> bool:
        """Remove a role globally; also revokes it from all users and ACLs."""
        with self._lock:
            if name not in self._roles:
                return False
            del self._roles[name]
            for user in self._users.values():
                user.roles.discard(name)
            for acl in self._acls.values():
                acl.role_grants.pop(name, None)
            return True

    def assign_role(self, user_id: str, role_name: str) -> bool:
        """Assign a previously defined role to a user."""
        with self._lock:
            if role_name not in self._roles:
                return False
            user = self._users.get(user_id)
            if user is None:
                user = User(user_id=user_id)
                self._users[user_id] = user
            user.roles.add(role_name)
            return True

    def unassign_role(self, user_id: str, role_name: str) -> bool:
        """Revoke a role assignment from a user (internal helper)."""
        with self._lock:
            user = self._users.get(user_id)
            if user is None or role_name not in user.roles:
                return False
            user.roles.discard(role_name)
            return True

    # ------------------------------------------------------------------ grants
    def grant_user(
        self, doc_id: str, user_id: str, perms: Set[Permission]
    ) -> None:
        """Grant explicit permissions to a user on a document."""
        with self._lock:
            acl = self._acls.get(doc_id)
            if acl is None:
                # Document with no owner yet — create with empty owner.
                acl = Acl(doc_id=doc_id, owner="")
                self._acls[doc_id] = acl
            current = acl.user_grants.get(user_id, set())
            acl.user_grants[user_id] = current | set(perms)

    def grant_role(
        self, doc_id: str, role_name: str, perms: Set[Permission]
    ) -> None:
        """Grant permissions to all holders of a role on a document."""
        with self._lock:
            acl = self._acls.get(doc_id)
            if acl is None:
                acl = Acl(doc_id=doc_id, owner="")
                self._acls[doc_id] = acl
            current = acl.role_grants.get(role_name, set())
            acl.role_grants[role_name] = current | set(perms)

    def grant_public(self, doc_id: str, perms: Set[Permission]) -> None:
        """Grant permissions to everyone (anonymous + authenticated)."""
        with self._lock:
            acl = self._acls.get(doc_id)
            if acl is None:
                acl = Acl(doc_id=doc_id, owner="")
                self._acls[doc_id] = acl
            acl.public_perms |= set(perms)

    # ----------------------------------------------------------------- revokes
    def revoke_user(
        self,
        doc_id: str,
        user_id: str,
        perms: Optional[Set[Permission]] = None,
    ) -> bool:
        """Revoke a user's explicit grants on a doc.

        If ``perms`` is ``None``, removes the user entirely; otherwise removes
        only the listed permissions.
        """
        with self._lock:
            acl = self._acls.get(doc_id)
            if acl is None or user_id not in acl.user_grants:
                return False
            if perms is None:
                del acl.user_grants[user_id]
                return True
            acl.user_grants[user_id] -= set(perms)
            if not acl.user_grants[user_id]:
                del acl.user_grants[user_id]
            return True

    def revoke_role(  # type: ignore[override]
        self,
        doc_or_user_id: str,
        role_name: str,
        perms: Optional[Set[Permission]] = None,
    ) -> bool:
        """Revoke a role.

        Polymorphic on the first argument:

        - If ``doc_or_user_id`` names a known user with ``role_name``
          assigned (and ``perms`` is ``None``), the role is unassigned
          from that user.
        - Otherwise, revokes the role's grants on the document
          ``doc_or_user_id`` (all permissions, or only ``perms``).
        """
        # Treat as user-unassignment when the first arg matches a known
        # user that holds this role and no per-permission filter was given.
        if perms is None:
            with self._lock:
                user = self._users.get(doc_or_user_id)
                if user is not None and role_name in user.roles:
                    user.roles.discard(role_name)
                    return True
        with self._lock:
            acl = self._acls.get(doc_or_user_id)
            if acl is None or role_name not in acl.role_grants:
                return False
            if perms is None:
                del acl.role_grants[role_name]
                return True
            acl.role_grants[role_name] -= set(perms)
            if not acl.role_grants[role_name]:
                del acl.role_grants[role_name]
            return True

    # ------------------------------------------------------------------ owner
    def set_owner(self, doc_id: str, owner_id: str) -> Acl:
        """Create or update the owner of a document, returning the ACL."""
        with self._lock:
            acl = self._acls.get(doc_id)
            if acl is None:
                acl = Acl(doc_id=doc_id, owner=owner_id)
                self._acls[doc_id] = acl
            else:
                acl.owner = owner_id
            return acl

    # ----------------------------------------------------------------- checks
    def _user_roles(self, user_id: str) -> Set[str]:
        user = self._users.get(user_id)
        return set(user.roles) if user else set()

    def check(self, user_id: str, doc_id: str, perm: Permission) -> AccessResult:
        """Check whether ``user_id`` may use ``perm`` on ``doc_id``."""
        with self._lock:
            acl = self._acls.get(doc_id)
            if acl is None:
                return AccessResult(
                    allowed=False,
                    reason=f"no acl for doc {doc_id!r}",
                    via=None,
                )

            # Owner gets everything.
            if acl.owner and user_id == acl.owner:
                return AccessResult(
                    allowed=True,
                    reason="user is owner",
                    via="owner",
                )

            # Explicit user grants.
            user_perms = _expand_admin(acl.user_grants.get(user_id, set()))
            if perm in user_perms:
                return AccessResult(
                    allowed=True,
                    reason=f"user grant on {doc_id!r}",
                    via="user_grant",
                )

            # Role grants for any role the user holds.
            for role_name in self._user_roles(user_id):
                role_perms = _expand_admin(acl.role_grants.get(role_name, set()))
                if perm in role_perms:
                    return AccessResult(
                        allowed=True,
                        reason=f"role {role_name!r} grants {perm.value}",
                        via=f"role_grant:{role_name}",
                    )

            # Public.
            public_perms = _expand_admin(acl.public_perms)
            if perm in public_perms:
                return AccessResult(
                    allowed=True,
                    reason="public permission",
                    via="public",
                )

            return AccessResult(
                allowed=False,
                reason=f"no grant for {perm.value} on {doc_id!r}",
                via=None,
            )

    def has_permission(
        self, user_id: str, doc_id: str, perm: Permission
    ) -> bool:
        """Convenience boolean wrapper around :meth:`check`."""
        return self.check(user_id, doc_id, perm).allowed

    def effective_permissions(
        self, user_id: str, doc_id: str
    ) -> Set[Permission]:
        """Return the full set of permissions ``user_id`` has on ``doc_id``."""
        with self._lock:
            acl = self._acls.get(doc_id)
            if acl is None:
                return set()
            if acl.owner and user_id == acl.owner:
                return set(ALL_PERMISSIONS)
            perms: Set[Permission] = set()
            perms |= acl.user_grants.get(user_id, set())
            for role_name in self._user_roles(user_id):
                perms |= acl.role_grants.get(role_name, set())
            perms |= acl.public_perms
            return _expand_admin(perms)

    def acl_for(self, doc_id: str) -> Optional[Acl]:
        """Return the ACL for ``doc_id`` or ``None`` if absent."""
        with self._lock:
            return self._acls.get(doc_id)

    def docs_accessible_to(
        self,
        user_id: str,
        perm: Permission = Permission.READ,
    ) -> List[str]:
        """List documents on which ``user_id`` holds ``perm``."""
        with self._lock:
            doc_ids = list(self._acls.keys())
        result: List[str] = []
        for doc_id in doc_ids:
            if self.has_permission(user_id, doc_id, perm):
                result.append(doc_id)
        return result

    def clear(self) -> None:
        """Reset all state."""
        with self._lock:
            self._roles.clear()
            self._users.clear()
            self._acls.clear()
