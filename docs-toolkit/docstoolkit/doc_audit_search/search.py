"""Searchable audit log index for documents (E343).

Pure-stdlib, thread-safe, dataclass-based implementation.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass
class AuditEntry:
    """A single auditable action record."""

    entry_id: int
    doc_id: str
    actor: str
    action: str
    timestamp: float = 0.0
    details: dict = field(default_factory=dict)


@dataclass
class AuditSearchQuery:
    """A search query against the audit log."""

    doc_id: Optional[str] = None
    actor: Optional[str] = None
    action: Optional[str] = None
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    limit: Optional[int] = None


@dataclass
class AuditStats:
    """Aggregate statistics over the audit log."""

    total_entries: int
    unique_docs: int
    unique_actors: int
    unique_actions: int


class DocAuditSearch:
    """Main interface for audit search.

    Maintains a global ordered list of :class:`AuditEntry` plus secondary
    indexes (by doc_id, actor, action) for fast filtered lookup.
    Thread-safe via an internal :class:`threading.Lock`.
    """

    def __init__(self) -> None:
        self._entries: List[AuditEntry] = []
        self._by_doc: Dict[str, List[int]] = {}
        self._by_actor: Dict[str, List[int]] = {}
        self._by_action: Dict[str, List[int]] = {}
        self._next_id: int = 1
        self._lock = threading.Lock()

    # ------------------------------------------------------------------ record

    def record(
        self,
        doc_id: str,
        actor: str,
        action: str,
        details: Optional[dict] = None,
        now: Optional[float] = None,
    ) -> AuditEntry:
        """Record an audit entry and return it."""
        with self._lock:
            ts = now if now is not None else time.time()
            entry = AuditEntry(
                entry_id=self._next_id,
                doc_id=doc_id,
                actor=actor,
                action=action,
                timestamp=ts,
                details=dict(details) if details else {},
            )
            self._next_id += 1
            idx = len(self._entries)
            self._entries.append(entry)
            self._by_doc.setdefault(doc_id, []).append(idx)
            self._by_actor.setdefault(actor, []).append(idx)
            self._by_action.setdefault(action, []).append(idx)
            return entry

    # ------------------------------------------------------------------ search

    def search(self, query: AuditSearchQuery) -> List[AuditEntry]:
        """Apply filters and return entries sorted by timestamp desc."""
        with self._lock:
            # Pick narrowest available index for candidates
            candidates: Optional[List[int]] = None
            options: List[List[int]] = []
            if query.doc_id is not None:
                options.append(self._by_doc.get(query.doc_id, []))
            if query.actor is not None:
                options.append(self._by_actor.get(query.actor, []))
            if query.action is not None:
                options.append(self._by_action.get(query.action, []))

            if options:
                candidates = min(options, key=len)
                iter_indices: List[int] = list(candidates)
            else:
                iter_indices = list(range(len(self._entries)))

            results: List[AuditEntry] = []
            for idx in iter_indices:
                e = self._entries[idx]
                if query.doc_id is not None and e.doc_id != query.doc_id:
                    continue
                if query.actor is not None and e.actor != query.actor:
                    continue
                if query.action is not None and e.action != query.action:
                    continue
                if query.start_time is not None and e.timestamp < query.start_time:
                    continue
                if query.end_time is not None and e.timestamp > query.end_time:
                    continue
                results.append(e)

            results.sort(key=lambda x: x.timestamp, reverse=True)
            if query.limit is not None:
                results = results[: query.limit]
            return results

    # -------------------------------------------------------------- get_entry

    def get_entry(self, entry_id: int) -> Optional[AuditEntry]:
        """Return entry by id, or None."""
        with self._lock:
            for e in self._entries:
                if e.entry_id == entry_id:
                    return e
            return None

    # ----------------------------------------------------------- entries_for_*

    def entries_for_doc(
        self, doc_id: str, limit: Optional[int] = None
    ) -> List[AuditEntry]:
        """Entries for a doc, sorted by timestamp desc."""
        with self._lock:
            indices = self._by_doc.get(doc_id, [])
            entries = [self._entries[i] for i in indices]
            entries.sort(key=lambda x: x.timestamp, reverse=True)
            if limit is not None:
                entries = entries[:limit]
            return entries

    def entries_for_actor(
        self, actor: str, limit: Optional[int] = None
    ) -> List[AuditEntry]:
        """Entries for an actor, sorted by timestamp desc."""
        with self._lock:
            indices = self._by_actor.get(actor, [])
            entries = [self._entries[i] for i in indices]
            entries.sort(key=lambda x: x.timestamp, reverse=True)
            if limit is not None:
                entries = entries[:limit]
            return entries

    def entries_by_action(
        self, action: str, limit: Optional[int] = None
    ) -> List[AuditEntry]:
        """Entries for an action, sorted by timestamp desc."""
        with self._lock:
            indices = self._by_action.get(action, [])
            entries = [self._entries[i] for i in indices]
            entries.sort(key=lambda x: x.timestamp, reverse=True)
            if limit is not None:
                entries = entries[:limit]
            return entries

    def entries_in_range(
        self,
        start_time: float,
        end_time: float,
        doc_id: Optional[str] = None,
    ) -> List[AuditEntry]:
        """Entries within inclusive [start_time, end_time] window, sorted asc."""
        with self._lock:
            if doc_id is not None:
                indices = self._by_doc.get(doc_id, [])
                candidates = [self._entries[i] for i in indices]
            else:
                candidates = list(self._entries)
            results = [
                e
                for e in candidates
                if start_time <= e.timestamp <= end_time
            ]
            results.sort(key=lambda x: x.timestamp)
            return results

    # ----------------------------------------------------------------- top_*

    def top_actors(self, limit: int = 10) -> List[Tuple[str, int]]:
        """Top actors by entry count."""
        with self._lock:
            counts = [(actor, len(idxs)) for actor, idxs in self._by_actor.items()]
            counts.sort(key=lambda x: (-x[1], x[0]))
            return counts[:limit]

    def top_actions(self, limit: int = 10) -> List[Tuple[str, int]]:
        """Top actions by entry count."""
        with self._lock:
            counts = [
                (action, len(idxs)) for action, idxs in self._by_action.items()
            ]
            counts.sort(key=lambda x: (-x[1], x[0]))
            return counts[:limit]

    # ----------------------------------------------------------------- delete

    def delete_entries_for_doc(self, doc_id: str) -> int:
        """Remove a doc's entries from the indexes; return count removed."""
        with self._lock:
            indices = self._by_doc.pop(doc_id, [])
            if not indices:
                return 0
            removed = set(indices)
            # Filter from actor/action indexes
            for actor, idxs in list(self._by_actor.items()):
                new_idxs = [i for i in idxs if i not in removed]
                if new_idxs:
                    self._by_actor[actor] = new_idxs
                else:
                    del self._by_actor[actor]
            for action, idxs in list(self._by_action.items()):
                new_idxs = [i for i in idxs if i not in removed]
                if new_idxs:
                    self._by_action[action] = new_idxs
                else:
                    del self._by_action[action]
            return len(indices)

    def clear(self) -> int:
        """Clear all entries; return count cleared."""
        with self._lock:
            n = len(self._entries)
            self._entries.clear()
            self._by_doc.clear()
            self._by_actor.clear()
            self._by_action.clear()
            self._next_id = 1
            return n

    # ------------------------------------------------------------------ stats

    def stats(self) -> AuditStats:
        """Return aggregate statistics."""
        with self._lock:
            return AuditStats(
                total_entries=sum(len(v) for v in self._by_doc.values()),
                unique_docs=len(self._by_doc),
                unique_actors=len(self._by_actor),
                unique_actions=len(self._by_action),
            )
