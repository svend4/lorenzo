"""Retention rule management for documents (E299)."""

from __future__ import annotations

import fnmatch
import threading
import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class RetentionRule:
    """A single retention rule for a document or pattern.

    Parameters
    ----------
    rule_id:
        Unique identifier for this rule.
    pattern:
        Document ID pattern.  Supports exact match, ``"*"`` wildcard (all
        docs), or any ``fnmatch``-compatible pattern such as ``"prefix:*"``.
    ttl_seconds:
        Maximum document age in seconds.  ``None`` means no TTL constraint.
    keep_versions:
        Maximum number of versions to retain.  ``None`` means unlimited.
    priority:
        Higher priority wins when multiple rules match the same doc_id.
    """

    rule_id: str
    pattern: str
    ttl_seconds: Optional[float] = None
    keep_versions: Optional[int] = None
    priority: int = 0


@dataclass
class RetentionResult:
    """Result of evaluating a retention policy against a single document.

    Parameters
    ----------
    doc_id:
        The document that was evaluated.
    rule_id:
        The rule that applied, or ``None`` if no rule matched.
    expired:
        ``True`` when the document exceeds the matched rule's TTL.
    versions_to_delete:
        Number of excess versions that should be removed (0 when
        ``keep_versions`` is not set or the version count is within limits).
    reason:
        Human-readable explanation of the evaluation outcome.
    """

    doc_id: str
    rule_id: Optional[str]
    expired: bool
    versions_to_delete: int
    reason: str


@dataclass
class PolicyStats:
    """Aggregate statistics for the :class:`DocRetentionPolicy` store.

    Parameters
    ----------
    total_rules:
        Number of rules currently registered.
    docs_tracked:
        Number of doc_ids that have been registered for evaluation.
    expired_count:
        Number of registered documents currently marked as expired.
    """

    total_rules: int
    docs_tracked: int
    expired_count: int


class DocRetentionPolicy:
    """Main interface for retention rule CRUD and document evaluation.

    All public methods are thread-safe.

    Internal storage
    ----------------
    ``_rules``  : ``dict[str, RetentionRule]``   — rule_id → rule
    ``_docs``   : ``dict[str, tuple[float, int]]`` — doc_id → (created_at, version_count)
    """

    def __init__(self) -> None:
        self._rules: dict[str, RetentionRule] = {}
        self._docs: dict[str, tuple[float, int]] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------ #
    # Rule CRUD
    # ------------------------------------------------------------------ #

    def add_rule(self, rule: RetentionRule) -> None:
        """Register *rule*, replacing any existing rule with the same ID."""
        with self._lock:
            self._rules[rule.rule_id] = rule

    def remove_rule(self, rule_id: str) -> bool:
        """Remove rule by *rule_id*.  Returns ``True`` if the rule existed."""
        with self._lock:
            if rule_id in self._rules:
                del self._rules[rule_id]
                return True
            return False

    def get_rule(self, rule_id: str) -> Optional[RetentionRule]:
        """Return the rule with *rule_id*, or ``None`` if not found."""
        with self._lock:
            return self._rules.get(rule_id)

    def list_rules(self) -> list[RetentionRule]:
        """Return all rules sorted by descending priority, then rule_id."""
        with self._lock:
            return sorted(
                self._rules.values(),
                key=lambda r: (-r.priority, r.rule_id),
            )

    # ------------------------------------------------------------------ #
    # Document registration
    # ------------------------------------------------------------------ #

    def register_doc(
        self,
        doc_id: str,
        created_at: float,
        version_count: int = 1,
        now: Optional[float] = None,  # noqa: ARG002  (kept for API symmetry)
    ) -> None:
        """Register or update metadata for *doc_id*.

        Parameters
        ----------
        doc_id:
            Identifier of the document.
        created_at:
            Unix timestamp when the document was created.
        version_count:
            Number of versions currently stored for this document.
        now:
            Unused; accepted for API symmetry with :meth:`evaluate`.
        """
        with self._lock:
            self._docs[doc_id] = (float(created_at), int(version_count))

    # ------------------------------------------------------------------ #
    # Evaluation
    # ------------------------------------------------------------------ #

    def evaluate(
        self,
        doc_id: str,
        now: Optional[float] = None,
    ) -> RetentionResult:
        """Evaluate retention policy for *doc_id*.

        Finds the highest-priority rule whose pattern matches *doc_id* via
        :func:`fnmatch.fnmatch`, then determines expiry and excess versions.

        Parameters
        ----------
        doc_id:
            The document to evaluate.
        now:
            Reference timestamp (defaults to :func:`time.time`).

        Returns
        -------
        RetentionResult
            Evaluation outcome.  ``rule_id`` is ``None`` and ``expired`` is
            ``False`` when no rule matches.
        """
        effective_now = time.time() if now is None else now

        with self._lock:
            doc_meta = self._docs.get(doc_id)
            # Sort rules once: highest priority first, then by rule_id for
            # deterministic tie-breaking.
            sorted_rules = sorted(
                self._rules.values(),
                key=lambda r: (-r.priority, r.rule_id),
            )

        if doc_meta is None:
            # Doc not registered; we can still evaluate against a default
            # created_at of 0 if we have the metadata, but here it's unknown.
            created_at = 0.0
            version_count = 0
        else:
            created_at, version_count = doc_meta

        matching_rule: Optional[RetentionRule] = None
        for rule in sorted_rules:
            if fnmatch.fnmatch(doc_id, rule.pattern):
                matching_rule = rule
                break

        if matching_rule is None:
            return RetentionResult(
                doc_id=doc_id,
                rule_id=None,
                expired=False,
                versions_to_delete=0,
                reason="no matching rule",
            )

        # Evaluate TTL
        expired = (
            matching_rule.ttl_seconds is not None
            and (effective_now - created_at) > matching_rule.ttl_seconds
        )

        # Evaluate version count
        versions_to_delete = (
            max(0, version_count - matching_rule.keep_versions)
            if matching_rule.keep_versions is not None
            else 0
        )

        # Build reason string
        parts: list[str] = [f"rule '{matching_rule.rule_id}' matched"]
        if expired:
            age = effective_now - created_at
            parts.append(
                f"expired (age {age:.1f}s > ttl {matching_rule.ttl_seconds}s)"
            )
        if versions_to_delete > 0:
            parts.append(
                f"delete {versions_to_delete} excess version(s) "
                f"(have {version_count}, keep {matching_rule.keep_versions})"
            )

        return RetentionResult(
            doc_id=doc_id,
            rule_id=matching_rule.rule_id,
            expired=expired,
            versions_to_delete=versions_to_delete,
            reason="; ".join(parts),
        )

    def evaluate_all(
        self,
        now: Optional[float] = None,
    ) -> list[RetentionResult]:
        """Evaluate all registered documents and return results sorted by doc_id."""
        effective_now = time.time() if now is None else now

        with self._lock:
            doc_ids = list(self._docs.keys())

        return sorted(
            (self.evaluate(doc_id, now=effective_now) for doc_id in doc_ids),
            key=lambda r: r.doc_id,
        )

    # ------------------------------------------------------------------ #
    # Convenience helpers
    # ------------------------------------------------------------------ #

    def apply_ttl(
        self,
        doc_id: str,  # noqa: ARG002  (kept for API completeness)
        created_at: float,
        ttl_seconds: float,
        now: Optional[float] = None,
    ) -> bool:
        """Return ``True`` if ``(now - created_at) > ttl_seconds``.

        This is a pure computation helper — it does **not** mutate any state.

        Parameters
        ----------
        doc_id:
            Document identifier (unused; accepted for API symmetry).
        created_at:
            Unix timestamp when the document was created.
        ttl_seconds:
            TTL threshold in seconds.
        now:
            Reference timestamp (defaults to :func:`time.time`).
        """
        effective_now = time.time() if now is None else now
        return (effective_now - created_at) > ttl_seconds

    def stats(self) -> PolicyStats:
        """Return aggregate statistics for the policy store."""
        effective_now = time.time()

        with self._lock:
            total_rules = len(self._rules)
            docs_tracked = len(self._docs)
            doc_ids = list(self._docs.keys())

        expired_count = sum(
            1
            for doc_id in doc_ids
            if self.evaluate(doc_id, now=effective_now).expired
        )

        return PolicyStats(
            total_rules=total_rules,
            docs_tracked=docs_tracked,
            expired_count=expired_count,
        )
