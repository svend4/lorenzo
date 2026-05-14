"""Implementation of DocSearchHistory and supporting types."""
from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import Optional


# --------------------------------------------------------------------- SearchQuery
@dataclass
class SearchQuery:
    """A single recorded search query."""

    query_id: int
    user_id: str
    query_text: str
    executed_at: float = 0.0
    result_count: int = 0
    clicked_doc_id: Optional[str] = None


# --------------------------------------------------------------------- QueryStats
@dataclass
class QueryStats:
    """Aggregate statistics for a query."""

    query_text: str
    total_executions: int
    unique_users: int
    avg_result_count: float
    click_through_count: int


# --------------------------------------------------------------------- HistoryStats
@dataclass
class HistoryStats:
    """Global aggregate statistics."""

    total_queries: int
    unique_users: int
    unique_query_texts: int


# --------------------------------------------------------------------- DocSearchHistory
class DocSearchHistory:
    """Per-user search query history with analytics."""

    def __init__(self) -> None:
        self._queries: list[SearchQuery] = []
        self._by_user: dict[str, list[int]] = {}
        self._by_text: dict[str, list[int]] = {}
        self._next_id: int = 1
        self._lock = threading.Lock()

    # ----------------------------------------------------------------- record
    def record(
        self,
        user_id: str,
        query_text: str,
        result_count: int = 0,
        clicked_doc_id: Optional[str] = None,
        now: Optional[float] = None,
    ) -> SearchQuery:
        """Record a new search query."""
        with self._lock:
            qid = self._next_id
            self._next_id += 1
            ts = now if now is not None else time.time()
            q = SearchQuery(
                query_id=qid,
                user_id=user_id,
                query_text=query_text,
                executed_at=ts,
                result_count=result_count,
                clicked_doc_id=clicked_doc_id,
            )
            self._queries.append(q)
            self._by_user.setdefault(user_id, []).append(qid)
            self._by_text.setdefault(query_text, []).append(qid)
            return q

    # ----------------------------------------------------------------- get_query
    def get_query(self, query_id: int) -> Optional[SearchQuery]:
        """Return the query with the given id, or ``None``."""
        with self._lock:
            # query_ids start at 1 and increment, so index = qid - 1 if not cleared.
            # But clear_user does NOT remove from _queries list, so this is safe.
            if 1 <= query_id < self._next_id:
                # Linear scan keeps correctness if list integrity ever shifts.
                idx = query_id - 1
                if 0 <= idx < len(self._queries) and self._queries[idx].query_id == query_id:
                    return self._queries[idx]
                for q in self._queries:
                    if q.query_id == query_id:
                        return q
            return None

    # ----------------------------------------------------------------- record_click
    def record_click(self, query_id: int, doc_id: str) -> bool:
        """Set ``clicked_doc_id`` on an existing query. Return True if found."""
        with self._lock:
            if 1 <= query_id < self._next_id:
                idx = query_id - 1
                if 0 <= idx < len(self._queries) and self._queries[idx].query_id == query_id:
                    self._queries[idx].clicked_doc_id = doc_id
                    return True
                for q in self._queries:
                    if q.query_id == query_id:
                        q.clicked_doc_id = doc_id
                        return True
            return False

    # ----------------------------------------------------------------- queries_for_user
    def queries_for_user(
        self, user_id: str, limit: Optional[int] = None
    ) -> list[SearchQuery]:
        """Return queries for a user, most recent first."""
        with self._lock:
            ids = self._by_user.get(user_id, [])
            items = [self._queries[i - 1] for i in ids if self._queries[i - 1].query_id == i]
            items.sort(key=lambda q: q.executed_at, reverse=True)
            if limit is not None:
                items = items[:limit]
            return items

    # ----------------------------------------------------------------- queries_for_text
    def queries_for_text(self, query_text: str) -> list[SearchQuery]:
        """Return queries with the given text sorted by ``executed_at``."""
        with self._lock:
            ids = self._by_text.get(query_text, [])
            items = [self._queries[i - 1] for i in ids if self._queries[i - 1].query_id == i]
            items.sort(key=lambda q: q.executed_at)
            return items

    # ----------------------------------------------------------------- recent_queries
    def recent_queries(self, limit: int = 10) -> list[SearchQuery]:
        """Return the most recent global queries, newest first."""
        with self._lock:
            tail = self._queries[-limit:] if limit > 0 else []
            return list(reversed(tail))

    # ----------------------------------------------------------------- top_queries
    def top_queries(self, limit: int = 10) -> list[tuple]:
        """Return ``(query_text, count)`` sorted by count desc, text asc."""
        with self._lock:
            counts: dict[str, int] = {}
            for text, ids in self._by_text.items():
                counts[text] = len(ids)
            items = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
            return items[:limit]

    # ----------------------------------------------------------------- query_stats
    def query_stats(self, query_text: str) -> Optional[QueryStats]:
        """Return :class:`QueryStats` for the query text, or ``None``."""
        with self._lock:
            ids = self._by_text.get(query_text)
            if not ids:
                return None
            execs: list[SearchQuery] = [
                self._queries[i - 1]
                for i in ids
                if self._queries[i - 1].query_id == i
            ]
            if not execs:
                return None
            users = {q.user_id for q in execs}
            avg = sum(q.result_count for q in execs) / len(execs)
            clicks = sum(1 for q in execs if q.clicked_doc_id is not None)
            return QueryStats(
                query_text=query_text,
                total_executions=len(execs),
                unique_users=len(users),
                avg_result_count=avg,
                click_through_count=clicks,
            )

    # ----------------------------------------------------------------- clear_user
    def clear_user(self, user_id: str) -> int:
        """Remove a user's query ids from indexes. Return removed count.

        The global ``_queries`` list is preserved; only the per-user and
        per-text indexes are updated.
        """
        with self._lock:
            ids = self._by_user.pop(user_id, [])
            if not ids:
                return 0
            id_set = set(ids)
            # Remove ids from _by_text
            empty_keys: list[str] = []
            for text, tids in self._by_text.items():
                kept = [i for i in tids if i not in id_set]
                if len(kept) != len(tids):
                    if kept:
                        self._by_text[text] = kept
                    else:
                        empty_keys.append(text)
            for k in empty_keys:
                del self._by_text[k]
            return len(ids)

    # ----------------------------------------------------------------- all_users
    def all_users(self) -> list[str]:
        """Return sorted list of all known users."""
        with self._lock:
            return sorted(self._by_user.keys())

    # ----------------------------------------------------------------- stats
    def stats(self) -> HistoryStats:
        """Return global :class:`HistoryStats`."""
        with self._lock:
            return HistoryStats(
                total_queries=sum(len(v) for v in self._by_user.values()),
                unique_users=len(self._by_user),
                unique_query_texts=len(self._by_text),
            )
