"""AccessEnforcer: evaluates an ordered chain of policies."""

from __future__ import annotations

from docstoolkit.access_control.permission import Permission, Role
from docstoolkit.access_control.policy import (
    AccessDecision,
    AccessPolicy,
    RolePolicy,
    Subject,
    Resource,
)


class AccessDeniedError(Exception):
    """Raised by :meth:`AccessEnforcer.require` when access is denied."""

    def __init__(self, subject_id: str, resource_id: str, permission: Permission) -> None:
        self.subject_id = subject_id
        self.resource_id = resource_id
        self.permission = permission
        super().__init__(
            f"Access denied: subject '{subject_id}' lacks '{permission.value}' "
            f"on resource '{resource_id}'"
        )


class AccessEnforcer:
    """Evaluates an ordered list of policies using first-match semantics.

    - Policies are evaluated in insertion order.
    - The first ALLOW or DENY decision terminates evaluation.
    - If every policy returns NOT_APPLICABLE, the decision is DENY.
    """

    def __init__(self, policies: list[AccessPolicy] | None = None) -> None:
        self._policies: list[AccessPolicy] = list(policies) if policies else []

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------

    def add_policy(self, policy: AccessPolicy) -> None:
        """Append *policy* to the evaluation chain."""
        self._policies.append(policy)

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    @property
    def roles(self) -> dict[str, Role]:
        """Return the combined role registry from all :class:`RolePolicy` instances."""
        combined: dict[str, Role] = {}
        for policy in self._policies:
            if isinstance(policy, RolePolicy):
                combined.update(policy.roles)
        return combined

    # ------------------------------------------------------------------
    # Evaluation
    # ------------------------------------------------------------------

    def _decide(
        self,
        subject: Subject,
        resource: Resource,
        permission: Permission,
    ) -> AccessDecision:
        for policy in self._policies:
            decision = policy.evaluate(subject, resource, permission)
            if decision is not AccessDecision.NOT_APPLICABLE:
                return decision
        # All policies returned NOT_APPLICABLE → default-deny
        return AccessDecision.DENY

    def check(
        self,
        subject: Subject,
        resource: Resource,
        permission: Permission,
    ) -> bool:
        """Return True if the subject is allowed, False otherwise."""
        return self._decide(subject, resource, permission) is AccessDecision.ALLOW

    def require(
        self,
        subject: Subject,
        resource: Resource,
        permission: Permission,
    ) -> None:
        """Raise :class:`AccessDeniedError` unless access is allowed."""
        if not self.check(subject, resource, permission):
            raise AccessDeniedError(subject.subject_id, resource.resource_id, permission)
