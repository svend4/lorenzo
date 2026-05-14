"""E305 DocQuotaManager — per-user and per-group document quota management.

Thread-safe via threading.Lock. Pure stdlib, no third-party dependencies.
"""
from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class QuotaRule:
    """A quota definition binding a subject to a resource limit.

    Attributes
    ----------
    rule_id:
        Unique identifier for this rule.
    subject:
        User ID, group ID, or ``"*"`` for a global default that applies to
        any subject with no exact match.
    resource:
        What is being limited, e.g. ``"docs"``, ``"storage_mb"``,
        ``"api_calls"``.
    limit:
        Maximum allowed usage (inclusive).
    period:
        Informational only — ``"total"``, ``"daily"``, or ``"monthly"``.
        Enforcement tracks raw cumulative usage; callers are responsible for
        resetting usage at period boundaries when periodic limits are desired.
    """

    rule_id: str
    subject: str
    resource: str
    limit: int
    period: str = "total"


@dataclass
class QuotaUsage:
    """Current usage snapshot for a (subject, resource) pair.

    Attributes
    ----------
    subject:
        The subject whose usage is captured.
    resource:
        The resource being measured.
    used:
        Raw usage counter at snapshot time.
    limit:
        The limit from the best-matching rule, or 0 if no rule exists.
    remaining:
        ``max(0, limit - used)``.  Always non-negative.
    exceeded:
        ``True`` when ``used > limit`` *and* a rule exists (limit > 0).
    """

    subject: str
    resource: str
    used: int
    limit: int
    remaining: int
    exceeded: bool


@dataclass
class QuotaCheckResult:
    """Result of a quota check for a proposed increment.

    Attributes
    ----------
    allowed:
        ``True`` when the proposed usage would not exceed the limit.
    subject:
        The subject that was checked.
    resource:
        The resource that was checked.
    used:
        Current usage *before* the proposed increment.
    limit:
        The applicable limit (0 when no rule matched).
    reason:
        Human-readable explanation of the decision.
    """

    allowed: bool
    subject: str
    resource: str
    used: int
    limit: int
    reason: str


class DocQuotaManager:
    """Main interface for quota rule CRUD and usage enforcement.

    All public methods are thread-safe — a single :class:`threading.Lock`
    protects both the rule registry and the usage counters.

    Parameters
    ----------
    None — state is fully in-memory and starts empty.
    """

    def __init__(self) -> None:
        self._lock: threading.Lock = threading.Lock()
        self._rules: dict[str, QuotaRule] = {}
        # (subject, resource) -> current usage count
        self._usage: dict[tuple[str, str], int] = {}

    # ------------------------------------------------------------------
    # Rule management
    # ------------------------------------------------------------------

    def set_rule(self, rule: QuotaRule) -> None:
        """Register or replace a quota rule.

        Parameters
        ----------
        rule:
            The :class:`QuotaRule` to store.  An existing rule with the same
            ``rule_id`` is silently overwritten.
        """
        with self._lock:
            self._rules[rule.rule_id] = rule

    def remove_rule(self, rule_id: str) -> bool:
        """Remove a rule by its ID.

        Parameters
        ----------
        rule_id:
            ID of the rule to remove.

        Returns
        -------
        bool
            ``True`` if the rule existed and was removed, ``False`` otherwise.
        """
        with self._lock:
            if rule_id in self._rules:
                del self._rules[rule_id]
                return True
            return False

    def get_rule(self, rule_id: str) -> Optional[QuotaRule]:
        """Return a rule by its ID, or ``None`` if not found.

        Parameters
        ----------
        rule_id:
            ID of the rule to look up.
        """
        with self._lock:
            return self._rules.get(rule_id)

    def rules_for_subject(self, subject: str) -> list[QuotaRule]:
        """Return all rules whose *subject* matches *subject*, sorted by rule_id.

        Parameters
        ----------
        subject:
            The subject to filter by (exact string match).
        """
        with self._lock:
            matched = [r for r in self._rules.values() if r.subject == subject]
        return sorted(matched, key=lambda r: r.rule_id)

    # ------------------------------------------------------------------
    # Usage counters
    # ------------------------------------------------------------------

    def increment(self, subject: str, resource: str, amount: int = 1) -> int:
        """Add *amount* to the usage counter for (subject, resource).

        Parameters
        ----------
        subject:
            The subject whose counter is incremented.
        resource:
            The resource whose counter is incremented.
        amount:
            How much to add (default 1).

        Returns
        -------
        int
            The new total usage after incrementing.
        """
        key = (subject, resource)
        with self._lock:
            current = self._usage.get(key, 0)
            new_value = current + amount
            self._usage[key] = new_value
            return new_value

    def decrement(self, subject: str, resource: str, amount: int = 1) -> int:
        """Subtract *amount* from the usage counter, floored at 0.

        Parameters
        ----------
        subject:
            The subject whose counter is decremented.
        resource:
            The resource whose counter is decremented.
        amount:
            How much to subtract (default 1).

        Returns
        -------
        int
            The new total usage after decrementing (never negative).
        """
        key = (subject, resource)
        with self._lock:
            current = self._usage.get(key, 0)
            new_value = max(0, current - amount)
            self._usage[key] = new_value
            return new_value

    def reset_usage(self, subject: str, resource: str) -> None:
        """Set the usage counter for (subject, resource) to 0.

        Parameters
        ----------
        subject:
            The subject to reset.
        resource:
            The resource to reset.
        """
        key = (subject, resource)
        with self._lock:
            self._usage[key] = 0

    def get_usage(self, subject: str, resource: str) -> int:
        """Return the current raw usage for (subject, resource).

        Returns 0 if the counter has never been set or incremented.

        Parameters
        ----------
        subject:
            The subject to query.
        resource:
            The resource to query.
        """
        key = (subject, resource)
        with self._lock:
            return self._usage.get(key, 0)

    # ------------------------------------------------------------------
    # Quota enforcement
    # ------------------------------------------------------------------

    def _best_rule(self, subject: str, resource: str) -> Optional[QuotaRule]:
        """Return the best matching rule for (subject, resource).

        Exact *subject* match takes priority over the ``"*"`` wildcard.
        Among multiple rules for the same subject+resource pair the one
        with the lexicographically smallest ``rule_id`` is returned (stable
        tie-breaking).

        Must be called with ``self._lock`` already held.
        """
        exact: list[QuotaRule] = []
        wildcard: list[QuotaRule] = []
        for rule in self._rules.values():
            if rule.resource != resource:
                continue
            if rule.subject == subject:
                exact.append(rule)
            elif rule.subject == "*":
                wildcard.append(rule)

        candidates = exact if exact else wildcard
        if not candidates:
            return None
        return min(candidates, key=lambda r: r.rule_id)

    def check(
        self, subject: str, resource: str, amount: int = 1
    ) -> QuotaCheckResult:
        """Check whether a proposed *amount* of *resource* usage is allowed.

        Matching priority: exact ``subject`` match first, then ``"*"``
        wildcard.  If no rule is found the request is allowed (open by
        default).

        Parameters
        ----------
        subject:
            The subject requesting the usage.
        resource:
            The resource being requested.
        amount:
            The proposed increment (default 1).

        Returns
        -------
        QuotaCheckResult
            Describes whether the request is allowed and why.
        """
        with self._lock:
            used = self._usage.get((subject, resource), 0)
            rule = self._best_rule(subject, resource)

        if rule is None:
            return QuotaCheckResult(
                allowed=True,
                subject=subject,
                resource=resource,
                used=used,
                limit=0,
                reason="no rule defined; request allowed by default",
            )

        limit = rule.limit
        if used + amount > limit:
            return QuotaCheckResult(
                allowed=False,
                subject=subject,
                resource=resource,
                used=used,
                limit=limit,
                reason=(
                    f"quota exceeded: used={used}, requested={amount}, "
                    f"limit={limit}"
                ),
            )

        return QuotaCheckResult(
            allowed=True,
            subject=subject,
            resource=resource,
            used=used,
            limit=limit,
            reason=f"within quota: used={used}, requested={amount}, limit={limit}",
        )

    def usage_snapshot(self, subject: str, resource: str) -> QuotaUsage:
        """Return a :class:`QuotaUsage` snapshot for (subject, resource).

        Parameters
        ----------
        subject:
            The subject to snapshot.
        resource:
            The resource to snapshot.
        """
        with self._lock:
            used = self._usage.get((subject, resource), 0)
            rule = self._best_rule(subject, resource)

        if rule is None:
            limit = 0
            remaining = 0
            exceeded = False
        else:
            limit = rule.limit
            remaining = max(0, limit - used)
            exceeded = used > limit

        return QuotaUsage(
            subject=subject,
            resource=resource,
            used=used,
            limit=limit,
            remaining=remaining,
            exceeded=exceeded,
        )

    # ------------------------------------------------------------------
    # Aggregate queries
    # ------------------------------------------------------------------

    def all_subjects(self) -> list[str]:
        """Return a sorted list of subjects that have at least one usage entry.

        Returns
        -------
        list[str]
            Unique subjects, sorted lexicographically.
        """
        with self._lock:
            subjects = {key[0] for key in self._usage}
        return sorted(subjects)

    def exceeded_subjects(self) -> list[str]:
        """Return a sorted list of subjects where any resource is exceeded.

        A resource is *exceeded* when ``used > limit`` **and** a matching rule
        exists.  Subjects with no rules or where all resources are within
        limits are excluded.

        Returns
        -------
        list[str]
            Unique subjects with at least one exceeded resource, sorted
            lexicographically.
        """
        with self._lock:
            keys = list(self._usage.keys())

        result: set[str] = set()
        for subject, resource in keys:
            snapshot = self.usage_snapshot(subject, resource)
            if snapshot.exceeded:
                result.add(subject)
        return sorted(result)
