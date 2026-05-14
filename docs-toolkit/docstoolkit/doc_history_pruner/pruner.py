"""Pruner implementation for E379 DocHistoryPruner."""

from __future__ import annotations

import fnmatch
import threading
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class HistoryVersion:
    """A single retained version of a document."""

    version_id: str
    doc_id: str
    created_at: float
    size_bytes: int = 0
    kept: bool = True


@dataclass
class PruneRule:
    """A pruning rule (TTL or count-based)."""

    rule_id: str
    pattern: str
    max_versions: Optional[int] = None
    max_age_seconds: Optional[float] = None
    priority: int = 0


@dataclass
class PruneResult:
    """Outcome of a pruning operation for a single doc."""

    doc_id: str
    pruned_versions: list[str] = field(default_factory=list)
    kept_versions: list[str] = field(default_factory=list)
    applied_rule: Optional[str] = None
    pruned_count: int = 0


@dataclass
class PrunerStats:
    """Aggregate statistics for the pruner."""

    total_versions: int
    total_rules: int
    unique_docs: int
    total_pruned: int


class DocHistoryPruner:
    """Manage and prune document version histories."""

    def __init__(self) -> None:
        self._versions: dict[tuple, HistoryVersion] = {}
        self._by_doc: dict[str, list[str]] = {}
        self._rules: dict[str, PruneRule] = {}
        self._total_pruned: int = 0
        self._lock = threading.Lock()

    # ----- versions -----

    def add_version(
        self,
        doc_id: str,
        version_id: str,
        created_at: float,
        size_bytes: int = 0,
    ) -> HistoryVersion:
        """Add a version to the store."""
        with self._lock:
            version = HistoryVersion(
                version_id=version_id,
                doc_id=doc_id,
                created_at=created_at,
                size_bytes=size_bytes,
                kept=True,
            )
            key = (doc_id, version_id)
            if key not in self._versions:
                self._by_doc.setdefault(doc_id, []).append(version_id)
            self._versions[key] = version
            return version

    def remove_version(self, doc_id: str, version_id: str) -> bool:
        """Remove a specific version. Returns True if removed."""
        with self._lock:
            key = (doc_id, version_id)
            if key not in self._versions:
                return False
            del self._versions[key]
            if doc_id in self._by_doc:
                try:
                    self._by_doc[doc_id].remove(version_id)
                except ValueError:
                    pass
                if not self._by_doc[doc_id]:
                    del self._by_doc[doc_id]
            return True

    def versions_for(self, doc_id: str) -> list[HistoryVersion]:
        """Return all versions for a document, sorted by created_at desc."""
        with self._lock:
            ids = list(self._by_doc.get(doc_id, []))
            versions = [self._versions[(doc_id, vid)] for vid in ids if (doc_id, vid) in self._versions]
        return sorted(versions, key=lambda v: v.created_at, reverse=True)

    def kept_versions_for(self, doc_id: str) -> list[HistoryVersion]:
        """Return kept versions for a document, sorted by created_at desc."""
        return [v for v in self.versions_for(doc_id) if v.kept]

    def all_doc_ids(self) -> list[str]:
        """Return all doc IDs, sorted."""
        with self._lock:
            return sorted(self._by_doc.keys())

    # ----- rules -----

    def add_rule(self, rule: PruneRule) -> None:
        """Add or replace a rule."""
        with self._lock:
            self._rules[rule.rule_id] = rule

    def remove_rule(self, rule_id: str) -> bool:
        """Remove a rule. Returns True if removed."""
        with self._lock:
            if rule_id not in self._rules:
                return False
            del self._rules[rule_id]
            return True

    def list_rules(self) -> list[PruneRule]:
        """Return all rules, sorted by (-priority, rule_id)."""
        with self._lock:
            rules = list(self._rules.values())
        return sorted(rules, key=lambda r: (-r.priority, r.rule_id))

    # ----- prune -----

    def _find_rule(self, doc_id: str) -> Optional[PruneRule]:
        candidates = [r for r in self._rules.values() if fnmatch.fnmatchcase(doc_id, r.pattern)]
        if not candidates:
            return None
        candidates.sort(key=lambda r: (-r.priority, r.rule_id))
        return candidates[0]

    def prune(self, doc_id: str, now: Optional[float] = None) -> PruneResult:
        """Apply highest-priority matching rule to a document."""
        if now is None:
            now = time.time()
        with self._lock:
            rule = self._find_rule(doc_id)
            if rule is None:
                return PruneResult(doc_id=doc_id)

            # Collect kept versions for this doc, sorted newest first
            ids = list(self._by_doc.get(doc_id, []))
            versions = [self._versions[(doc_id, vid)] for vid in ids if (doc_id, vid) in self._versions]
            kept_versions = [v for v in versions if v.kept]
            kept_versions.sort(key=lambda v: v.created_at, reverse=True)

            to_prune: list[HistoryVersion] = []

            # Apply max_versions: keep newest N
            survivors = kept_versions
            if rule.max_versions is not None and len(survivors) > rule.max_versions:
                keep = survivors[: rule.max_versions]
                extra = survivors[rule.max_versions :]
                to_prune.extend(extra)
                survivors = keep

            # Apply max_age_seconds: drop those older than threshold
            if rule.max_age_seconds is not None:
                threshold = now - rule.max_age_seconds
                still_alive: list[HistoryVersion] = []
                for v in survivors:
                    if v.created_at < threshold:
                        to_prune.append(v)
                    else:
                        still_alive.append(v)
                survivors = still_alive

            # Mark as not kept
            pruned_ids: list[str] = []
            for v in to_prune:
                if v.kept:
                    v.kept = False
                    pruned_ids.append(v.version_id)

            self._total_pruned += len(pruned_ids)

            kept_ids = [v.version_id for v in survivors]

            return PruneResult(
                doc_id=doc_id,
                pruned_versions=pruned_ids,
                kept_versions=kept_ids,
                applied_rule=rule.rule_id,
                pruned_count=len(pruned_ids),
            )

    def prune_all(self, now: Optional[float] = None) -> list[PruneResult]:
        """Prune every document that matches any rule."""
        if now is None:
            now = time.time()
        with self._lock:
            doc_ids = list(self._by_doc.keys())
        results: list[PruneResult] = []
        for doc_id in sorted(doc_ids):
            result = self.prune(doc_id, now=now)
            if result.applied_rule is not None:
                results.append(result)
        return results

    def delete_pruned(self, doc_id: str) -> int:
        """Permanently remove versions where kept=False. Returns count."""
        with self._lock:
            ids = list(self._by_doc.get(doc_id, []))
            removed = 0
            survivors: list[str] = []
            for vid in ids:
                key = (doc_id, vid)
                v = self._versions.get(key)
                if v is not None and not v.kept:
                    del self._versions[key]
                    removed += 1
                else:
                    survivors.append(vid)
            if survivors:
                self._by_doc[doc_id] = survivors
            else:
                self._by_doc.pop(doc_id, None)
            return removed

    # ----- stats -----

    def stats(self) -> PrunerStats:
        """Return aggregate statistics."""
        with self._lock:
            return PrunerStats(
                total_versions=len(self._versions),
                total_rules=len(self._rules),
                unique_docs=len(self._by_doc),
                total_pruned=self._total_pruned,
            )
