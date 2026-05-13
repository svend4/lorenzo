"""Policy abstractions and built-in policy implementations."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, unique

from docstoolkit.access_control.permission import Permission, Role


@dataclass
class Subject:
    """An entity (user, service, …) requesting access."""

    subject_id: str
    roles: list[str] = field(default_factory=list)
    attributes: dict = field(default_factory=dict)


@dataclass
class Resource:
    """A resource being accessed."""

    resource_id: str
    resource_type: str
    owner_id: str = ""
    attributes: dict = field(default_factory=dict)


@unique
class AccessDecision(Enum):
    """The outcome of a single policy evaluation."""

    ALLOW = "allow"
    DENY = "deny"
    NOT_APPLICABLE = "not_applicable"


class AccessPolicy(ABC):
    """Abstract base for all access policies."""

    @abstractmethod
    def evaluate(
        self,
        subject: Subject,
        resource: Resource,
        permission: Permission,
    ) -> AccessDecision:
        """Evaluate the policy and return an :class:`AccessDecision`."""


class OwnerPolicy(AccessPolicy):
    """ALLOW when *subject* owns the *resource*; NOT_APPLICABLE otherwise."""

    def evaluate(
        self,
        subject: Subject,
        resource: Resource,
        permission: Permission,
    ) -> AccessDecision:
        if resource.owner_id and subject.subject_id == resource.owner_id:
            return AccessDecision.ALLOW
        return AccessDecision.NOT_APPLICABLE


class RolePolicy(AccessPolicy):
    """ALLOW when any of the subject's roles carries the requested permission.

    Returns NOT_APPLICABLE when the subject has no matching roles.
    Never returns DENY.
    """

    def __init__(self, roles: dict[str, Role]) -> None:
        self._roles: dict[str, Role] = dict(roles)

    @property
    def roles(self) -> dict[str, Role]:
        """Return the role registry used by this policy."""
        return self._roles

    def evaluate(
        self,
        subject: Subject,
        resource: Resource,
        permission: Permission,
    ) -> AccessDecision:
        for role_name in subject.roles:
            role = self._roles.get(role_name)
            if role is not None and role.has_permission(permission):
                return AccessDecision.ALLOW
        return AccessDecision.NOT_APPLICABLE


class DenyAllPolicy(AccessPolicy):
    """Unconditionally deny every request — useful as a catch-all sentinel."""

    def evaluate(
        self,
        subject: Subject,
        resource: Resource,
        permission: Permission,
    ) -> AccessDecision:
        return AccessDecision.DENY
