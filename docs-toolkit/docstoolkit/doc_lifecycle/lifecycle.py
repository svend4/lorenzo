"""Document lifecycle management with automated policies."""

from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


SECONDS_PER_DAY = 86400.0


class LifecycleStage(str, Enum):
    """Stages a document goes through during its lifetime."""

    NEW = "new"
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"
    EXPIRED = "expired"
    DELETED = "deleted"


@dataclass
class LifecyclePolicy:
    """A policy describing how to transition documents through lifecycle stages."""

    policy_id: str
    name: str
    inactive_after_days: Optional[float] = None
    archive_after_days: Optional[float] = None
    delete_after_days: Optional[float] = None
    categories: list[str] = field(default_factory=list)
    enabled: bool = True


@dataclass
class DocLifecycle:
    """Lifecycle state of a single document."""

    doc_id: str
    stage: LifecycleStage
    created_at: float
    last_accessed: float = 0.0
    inactive_since: Optional[float] = None
    archived_at: Optional[float] = None
    expires_at: Optional[float] = None
    deleted_at: Optional[float] = None
    categories: list[str] = field(default_factory=list)
    policy_id: Optional[str] = None


@dataclass
class LifecycleStats:
    """Aggregate statistics about the managed corpus."""

    total: int
    by_stage: dict[str, int]
    policies_count: int
    eligible_for_archive: int
    eligible_for_deletion: int


class DocLifecycleManager:
    """Manages document lifecycle states and policy-driven transitions."""

    def __init__(self) -> None:
        self._policies: dict[str, LifecyclePolicy] = {}
        self._docs: dict[str, DocLifecycle] = {}
        self._lock = threading.Lock()

    # ----- Policies -------------------------------------------------------

    def add_policy(
        self,
        name: str,
        inactive_after_days: Optional[float] = None,
        archive_after_days: Optional[float] = None,
        delete_after_days: Optional[float] = None,
        categories: Optional[list[str]] = None,
    ) -> LifecyclePolicy:
        """Create and register a new lifecycle policy."""
        with self._lock:
            policy_id = uuid.uuid4().hex
            policy = LifecyclePolicy(
                policy_id=policy_id,
                name=name,
                inactive_after_days=inactive_after_days,
                archive_after_days=archive_after_days,
                delete_after_days=delete_after_days,
                categories=list(categories) if categories else [],
                enabled=True,
            )
            self._policies[policy_id] = policy
            return policy

    def remove_policy(self, policy_id: str) -> bool:
        """Remove a policy by id. Returns True if removed."""
        with self._lock:
            if policy_id in self._policies:
                del self._policies[policy_id]
                # Detach docs referencing this policy
                for doc in self._docs.values():
                    if doc.policy_id == policy_id:
                        doc.policy_id = None
                return True
            return False

    def list_policies(self, enabled_only: bool = False) -> list[LifecyclePolicy]:
        """List all policies, optionally filtering to enabled ones."""
        with self._lock:
            policies = list(self._policies.values())
            if enabled_only:
                policies = [p for p in policies if p.enabled]
            return policies

    def find_matching_policy(
        self, categories: Optional[list[str]]
    ) -> Optional[LifecyclePolicy]:
        """Find the first enabled policy that matches any of these categories."""
        cats = set(categories or [])
        with self._lock:
            for policy in self._policies.values():
                if not policy.enabled:
                    continue
                if not policy.categories:
                    # Empty policy categories matches everything
                    return policy
                if cats & set(policy.categories):
                    return policy
            return None

    # ----- Document registration ------------------------------------------

    def register(
        self,
        doc_id: str,
        categories: Optional[list[str]] = None,
        policy_id: Optional[str] = None,
        now: float = 0.0,
    ) -> DocLifecycle:
        """Register a new document and assign a policy (auto-match if not given)."""
        with self._lock:
            cats = list(categories) if categories else []
            chosen_policy_id: Optional[str] = None
            if policy_id is not None:
                if policy_id in self._policies:
                    chosen_policy_id = policy_id
            else:
                # Auto-match policy by category
                cats_set = set(cats)
                for pid, policy in self._policies.items():
                    if not policy.enabled:
                        continue
                    if not policy.categories:
                        chosen_policy_id = pid
                        break
                    if cats_set & set(policy.categories):
                        chosen_policy_id = pid
                        break

            doc = DocLifecycle(
                doc_id=doc_id,
                stage=LifecycleStage.NEW,
                created_at=now,
                last_accessed=now,
                categories=cats,
                policy_id=chosen_policy_id,
            )
            self._docs[doc_id] = doc
            return doc

    def record_access(self, doc_id: str, now: float = 0.0) -> bool:
        """Update last_accessed for a document; if INACTIVE, transition to ACTIVE."""
        with self._lock:
            doc = self._docs.get(doc_id)
            if doc is None:
                return False
            if doc.stage in (LifecycleStage.DELETED, LifecycleStage.EXPIRED):
                return False
            doc.last_accessed = now
            if doc.stage == LifecycleStage.NEW:
                doc.stage = LifecycleStage.ACTIVE
            elif doc.stage == LifecycleStage.INACTIVE:
                doc.stage = LifecycleStage.ACTIVE
                doc.inactive_since = None
            return True

    def get(self, doc_id: str) -> Optional[DocLifecycle]:
        """Retrieve a document's lifecycle record."""
        with self._lock:
            return self._docs.get(doc_id)

    # ----- Manual transitions ---------------------------------------------

    def archive_now(self, doc_id: str, now: float = 0.0) -> bool:
        """Manually archive a document."""
        with self._lock:
            doc = self._docs.get(doc_id)
            if doc is None:
                return False
            if doc.stage in (LifecycleStage.DELETED, LifecycleStage.ARCHIVED):
                return False
            doc.stage = LifecycleStage.ARCHIVED
            doc.archived_at = now
            return True

    def delete_now(self, doc_id: str, now: float = 0.0) -> bool:
        """Manually mark a document as deleted."""
        with self._lock:
            doc = self._docs.get(doc_id)
            if doc is None:
                return False
            if doc.stage == LifecycleStage.DELETED:
                return False
            doc.stage = LifecycleStage.DELETED
            doc.deleted_at = now
            return True

    def restore(self, doc_id: str, now: float = 0.0) -> bool:
        """Restore an ARCHIVED document back to ACTIVE."""
        with self._lock:
            doc = self._docs.get(doc_id)
            if doc is None:
                return False
            if doc.stage != LifecycleStage.ARCHIVED:
                return False
            doc.stage = LifecycleStage.ACTIVE
            doc.archived_at = None
            doc.inactive_since = None
            doc.last_accessed = now
            return True

    # ----- Policy evaluation ----------------------------------------------

    def evaluate_policies(self, now: float = 0.0) -> dict:
        """Apply policies to all docs, transitioning stages as needed."""
        inactivated = 0
        archived = 0
        deleted = 0
        with self._lock:
            for doc in self._docs.values():
                if doc.policy_id is None:
                    continue
                policy = self._policies.get(doc.policy_id)
                if policy is None or not policy.enabled:
                    continue

                # ACTIVE → INACTIVE
                if doc.stage == LifecycleStage.ACTIVE and policy.inactive_after_days is not None:
                    elapsed_days = (now - doc.last_accessed) / SECONDS_PER_DAY
                    if elapsed_days >= policy.inactive_after_days:
                        doc.stage = LifecycleStage.INACTIVE
                        doc.inactive_since = now
                        inactivated += 1

                # INACTIVE → ARCHIVED
                if doc.stage == LifecycleStage.INACTIVE and policy.archive_after_days is not None:
                    if doc.inactive_since is None:
                        # Defensive: set baseline if missing
                        doc.inactive_since = now
                    else:
                        elapsed_days = (now - doc.inactive_since) / SECONDS_PER_DAY
                        if elapsed_days >= policy.archive_after_days:
                            doc.stage = LifecycleStage.ARCHIVED
                            doc.archived_at = now
                            archived += 1

                # ARCHIVED → DELETED
                if doc.stage == LifecycleStage.ARCHIVED and policy.delete_after_days is not None:
                    if doc.archived_at is None:
                        doc.archived_at = now
                    else:
                        elapsed_days = (now - doc.archived_at) / SECONDS_PER_DAY
                        if elapsed_days >= policy.delete_after_days:
                            doc.stage = LifecycleStage.DELETED
                            doc.deleted_at = now
                            deleted += 1

        return {
            "inactivated": inactivated,
            "archived": archived,
            "deleted": deleted,
        }

    # ----- Queries --------------------------------------------------------

    def docs_in_stage(self, stage: LifecycleStage) -> list[DocLifecycle]:
        """Return all documents currently in a given stage."""
        with self._lock:
            return [d for d in self._docs.values() if d.stage == stage]

    def eligible_for_archive(self, now: float = 0.0) -> list[DocLifecycle]:
        """Return INACTIVE docs ready for archival under their policy."""
        result = []
        with self._lock:
            for doc in self._docs.values():
                if doc.stage != LifecycleStage.INACTIVE:
                    continue
                if doc.policy_id is None:
                    continue
                policy = self._policies.get(doc.policy_id)
                if policy is None or not policy.enabled:
                    continue
                if policy.archive_after_days is None:
                    continue
                if doc.inactive_since is None:
                    continue
                elapsed_days = (now - doc.inactive_since) / SECONDS_PER_DAY
                if elapsed_days >= policy.archive_after_days:
                    result.append(doc)
        return result

    def eligible_for_deletion(self, now: float = 0.0) -> list[DocLifecycle]:
        """Return ARCHIVED docs ready for deletion under their policy."""
        result = []
        with self._lock:
            for doc in self._docs.values():
                if doc.stage != LifecycleStage.ARCHIVED:
                    continue
                if doc.policy_id is None:
                    continue
                policy = self._policies.get(doc.policy_id)
                if policy is None or not policy.enabled:
                    continue
                if policy.delete_after_days is None:
                    continue
                if doc.archived_at is None:
                    continue
                elapsed_days = (now - doc.archived_at) / SECONDS_PER_DAY
                if elapsed_days >= policy.delete_after_days:
                    result.append(doc)
        return result

    def stats(self) -> LifecycleStats:
        """Snapshot of the corpus state."""
        by_stage: dict[str, int] = {s.value: 0 for s in LifecycleStage}
        with self._lock:
            for doc in self._docs.values():
                by_stage[doc.stage.value] = by_stage.get(doc.stage.value, 0) + 1
            total = len(self._docs)
            policies_count = len(self._policies)

        eligible_arc = len(self.eligible_for_archive(now=self._now_for_stats()))
        eligible_del = len(self.eligible_for_deletion(now=self._now_for_stats()))
        return LifecycleStats(
            total=total,
            by_stage=by_stage,
            policies_count=policies_count,
            eligible_for_archive=eligible_arc,
            eligible_for_deletion=eligible_del,
        )

    def _now_for_stats(self) -> float:
        """Default now used by stats() — current state, not time-extrapolated."""
        # Use max known timestamp to evaluate eligibility consistently.
        with self._lock:
            candidates: list[float] = []
            for doc in self._docs.values():
                if doc.inactive_since is not None:
                    candidates.append(doc.inactive_since)
                if doc.archived_at is not None:
                    candidates.append(doc.archived_at)
                if doc.last_accessed:
                    candidates.append(doc.last_accessed)
            return max(candidates) if candidates else 0.0

    # ----- Properties / utility -------------------------------------------

    @property
    def policy_count(self) -> int:
        """Number of registered policies."""
        with self._lock:
            return len(self._policies)

    @property
    def doc_count(self) -> int:
        """Number of registered documents."""
        with self._lock:
            return len(self._docs)

    def clear(self) -> None:
        """Remove all policies and documents."""
        with self._lock:
            self._policies.clear()
            self._docs.clear()
