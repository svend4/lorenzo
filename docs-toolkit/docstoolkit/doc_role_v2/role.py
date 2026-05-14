"""E236 Document role-based access control v2 — inheritance + ABAC policies."""
from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set


class Permission(Enum):
    """Permissions supported by DocRoleV2."""

    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"
    SHARE = "share"
    COMMENT = "comment"
    PUBLISH = "publish"


@dataclass
class RoleDefinition:
    """Definition of a role with optional parent role inheritance."""

    name: str
    permissions: Set[Permission]
    parent_roles: List[str] = field(default_factory=list)
    description: str = ""


@dataclass
class UserBinding:
    """Binding of a user to roles and attributes."""

    user_id: str
    roles: Set[str] = field(default_factory=set)
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Policy:
    """ABAC-style policy that grants a permission when condition is true."""

    policy_id: str
    name: str
    permission: Permission
    condition: Callable[[dict], bool]
    priority: int = 0


@dataclass
class AccessRequest:
    """Access request issued by a user for a particular resource."""

    user_id: str
    resource_id: str
    permission: Permission
    resource_attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AccessDecision:
    """Decision returned by :meth:`DocRoleV2.check_access`."""

    granted: bool
    reason: str
    matched_role: Optional[str] = None
    matched_policy: Optional[str] = None


class DocRoleV2:
    """Advanced role-based access control with inheritance and ABAC policies."""

    def __init__(self) -> None:
        self._roles: Dict[str, RoleDefinition] = {}
        self._users: Dict[str, UserBinding] = {}
        self._policies: Dict[str, Policy] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------ Roles
    def define_role(
        self,
        name: str,
        permissions: Set[Permission],
        parent_roles: Optional[List[str]] = None,
        description: str = "",
    ) -> RoleDefinition:
        if not isinstance(name, str) or not name:
            raise ValueError("Role name must be a non-empty string")
        parents = list(parent_roles) if parent_roles else []
        with self._lock:
            # Detect cycles for parents that already exist
            for parent in parents:
                if parent == name:
                    raise ValueError("Role cannot be its own parent")
                if parent in self._roles and self._creates_cycle(name, parent):
                    raise ValueError(
                        f"Adding parent {parent!r} creates a cycle for {name!r}"
                    )
            role = RoleDefinition(
                name=name,
                permissions=set(permissions),
                parent_roles=parents,
                description=description,
            )
            self._roles[name] = role
            return role

    def remove_role(self, name: str) -> bool:
        with self._lock:
            if name not in self._roles:
                return False
            del self._roles[name]
            # Detach from other roles' parent lists
            for role in self._roles.values():
                if name in role.parent_roles:
                    role.parent_roles = [p for p in role.parent_roles if p != name]
            # Revoke from users
            for user in self._users.values():
                user.roles.discard(name)
            return True

    def update_role_permissions(self, name: str, permissions: Set[Permission]) -> bool:
        with self._lock:
            if name not in self._roles:
                return False
            self._roles[name].permissions = set(permissions)
            return True

    def add_parent_role(self, role: str, parent: str) -> bool:
        with self._lock:
            if role not in self._roles or parent not in self._roles:
                return False
            if role == parent:
                return False
            if parent in self._roles[role].parent_roles:
                return True  # already a parent
            if self._creates_cycle(role, parent):
                return False
            self._roles[role].parent_roles.append(parent)
            return True

    def _creates_cycle(self, role: str, candidate_parent: str) -> bool:
        """Return True if adding *candidate_parent* to *role* introduces a cycle.

        That happens when *role* itself is reachable from *candidate_parent* via
        the existing parent links.
        """
        if role == candidate_parent:
            return True
        visited: Set[str] = set()
        stack: List[str] = [candidate_parent]
        while stack:
            current = stack.pop()
            if current == role:
                return True
            if current in visited:
                continue
            visited.add(current)
            node = self._roles.get(current)
            if node:
                stack.extend(node.parent_roles)
        return False

    def effective_permissions(self, role: str) -> Set[Permission]:
        with self._lock:
            if role not in self._roles:
                return set()
            return self._effective_permissions_unlocked(role)

    def _effective_permissions_unlocked(self, role: str) -> Set[Permission]:
        perms: Set[Permission] = set()
        visited: Set[str] = set()
        queue: List[str] = [role]
        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)
            node = self._roles.get(current)
            if not node:
                continue
            perms |= node.permissions
            for parent in node.parent_roles:
                if parent not in visited:
                    queue.append(parent)
        return perms

    def ancestors(self, role: str) -> List[str]:
        with self._lock:
            if role not in self._roles:
                return []
            result: List[str] = []
            visited: Set[str] = set()
            queue: List[str] = list(self._roles[role].parent_roles)
            while queue:
                current = queue.pop(0)
                if current in visited:
                    continue
                visited.add(current)
                if current in self._roles:
                    result.append(current)
                    queue.extend(self._roles[current].parent_roles)
            return result

    def child_roles(self, role: str) -> List[str]:
        with self._lock:
            return [
                name
                for name, definition in self._roles.items()
                if role in definition.parent_roles
            ]

    # ------------------------------------------------------------------ Users
    def bind_user(
        self,
        user_id: str,
        roles: Optional[Set[str]] = None,
        attributes: Optional[Dict[str, Any]] = None,
    ) -> UserBinding:
        if not isinstance(user_id, str) or not user_id:
            raise ValueError("user_id must be a non-empty string")
        with self._lock:
            binding = UserBinding(
                user_id=user_id,
                roles=set(roles) if roles else set(),
                attributes=dict(attributes) if attributes else {},
            )
            self._users[user_id] = binding
            return binding

    def assign_role(self, user_id: str, role: str) -> bool:
        with self._lock:
            if user_id not in self._users or role not in self._roles:
                return False
            self._users[user_id].roles.add(role)
            return True

    def revoke_role(self, user_id: str, role: str) -> bool:
        with self._lock:
            if user_id not in self._users:
                return False
            if role not in self._users[user_id].roles:
                return False
            self._users[user_id].roles.discard(role)
            return True

    def set_attribute(self, user_id: str, key: str, value: Any) -> bool:
        with self._lock:
            if user_id not in self._users:
                return False
            self._users[user_id].attributes[key] = value
            return True

    def user_roles(self, user_id: str) -> Set[str]:
        with self._lock:
            if user_id not in self._users:
                return set()
            return set(self._users[user_id].roles)

    def user_permissions(self, user_id: str) -> Set[Permission]:
        with self._lock:
            if user_id not in self._users:
                return set()
            perms: Set[Permission] = set()
            for role in self._users[user_id].roles:
                perms |= self._effective_permissions_unlocked(role)
            return perms

    def has_role(self, user_id: str, role: str) -> bool:
        with self._lock:
            if user_id not in self._users:
                return False
            direct = self._users[user_id].roles
            if role in direct:
                return True
            # Check if `role` is an ancestor of any of the user's direct roles
            for direct_role in direct:
                if role in self._ancestors_unlocked(direct_role):
                    return True
            return False

    def _ancestors_unlocked(self, role: str) -> List[str]:
        if role not in self._roles:
            return []
        result: List[str] = []
        visited: Set[str] = set()
        queue: List[str] = list(self._roles[role].parent_roles)
        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)
            if current in self._roles:
                result.append(current)
                queue.extend(self._roles[current].parent_roles)
        return result

    def users_with_role(self, role: str) -> List[str]:
        with self._lock:
            result: List[str] = []
            for user_id, binding in self._users.items():
                if role in binding.roles:
                    result.append(user_id)
                    continue
                for direct in binding.roles:
                    if role in self._ancestors_unlocked(direct):
                        result.append(user_id)
                        break
            return result

    # --------------------------------------------------------------- Policies
    def add_policy(
        self,
        name: str,
        permission: Permission,
        condition: Callable[[dict], bool],
        priority: int = 0,
    ) -> Policy:
        if not callable(condition):
            raise ValueError("condition must be callable")
        if not isinstance(permission, Permission):
            raise ValueError("permission must be a Permission enum value")
        with self._lock:
            policy_id = uuid.uuid4().hex
            policy = Policy(
                policy_id=policy_id,
                name=name,
                permission=permission,
                condition=condition,
                priority=priority,
            )
            self._policies[policy_id] = policy
            return policy

    def remove_policy(self, policy_id: str) -> bool:
        with self._lock:
            if policy_id not in self._policies:
                return False
            del self._policies[policy_id]
            return True

    # -------------------------------------------------------- Access checking
    def check_access(self, request: AccessRequest) -> AccessDecision:
        with self._lock:
            user = self._users.get(request.user_id)
            user_attrs: Dict[str, Any] = dict(user.attributes) if user else {}
            context: Dict[str, Any] = {
                "user_id": request.user_id,
                "resource_id": request.resource_id,
                "permission": request.permission,
                **user_attrs,
                **(request.resource_attributes or {}),
            }

            # Policies first, sorted by priority desc
            sorted_policies = sorted(
                self._policies.values(), key=lambda p: p.priority, reverse=True
            )
            for policy in sorted_policies:
                if policy.permission != request.permission:
                    continue
                try:
                    matched = bool(policy.condition(context))
                except Exception:
                    matched = False
                if matched:
                    return AccessDecision(
                        granted=True,
                        reason=f"policy:{policy.name}",
                        matched_policy=policy.policy_id,
                    )

            # Role-based check
            if user is None:
                return AccessDecision(granted=False, reason="user-not-bound")

            for role in user.roles:
                perms = self._effective_permissions_unlocked(role)
                if request.permission in perms:
                    return AccessDecision(
                        granted=True,
                        reason=f"role:{role}",
                        matched_role=role,
                    )

            return AccessDecision(granted=False, reason="no-matching-role-or-policy")

    # ------------------------------------------------------------- Properties
    @property
    def total_roles(self) -> int:
        with self._lock:
            return len(self._roles)

    @property
    def total_users(self) -> int:
        with self._lock:
            return len(self._users)

    @property
    def total_policies(self) -> int:
        with self._lock:
            return len(self._policies)

    def clear(self) -> None:
        with self._lock:
            self._roles.clear()
            self._users.clear()
            self._policies.clear()


__all__ = [
    "Permission",
    "RoleDefinition",
    "UserBinding",
    "Policy",
    "AccessRequest",
    "AccessDecision",
    "DocRoleV2",
]
