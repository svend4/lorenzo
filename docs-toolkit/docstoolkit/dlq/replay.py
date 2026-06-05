"""DLQ replay API — retry failed jobs with idempotency guarantees.

Supports:
* Filtering by job_id list, tags, failure reason, or date range.
* Per-job-type retry budget (max replays allowed before a job is
  considered a permanent failure / poison pill).
* Dry-run mode: simulate what would be replayed without executing.
* Idempotency: a separate SQLite table tracks which job_ids have been
  replayed so that network-partition scenarios cannot cause double-execution.

Usage::

    from docstoolkit.dlq import DeadLetterQueue
    from docstoolkit.dlq.replay import ReplayEngine, ReplayFilter

    dlq = DeadLetterQueue("jobs.db")
    engine = ReplayEngine(dlq, idempotency_db=":memory:")

    def handler(job_id: str, payload: str) -> None:
        ...  # re-process the job

    result = engine.replay(handler, mode="apply")
    print(result.replayed, result.skipped, result.errors)
"""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable, List, Optional

from docstoolkit.dlq.item import DeadLetterItem, FailureReason
from docstoolkit.dlq.queue import DeadLetterQueue


# ---------------------------------------------------------------------------
# Filter & result types
# ---------------------------------------------------------------------------

@dataclass
class ReplayFilter:
    """Criteria for selecting DLQ items to replay.

    All conditions are ANDed together.  An empty filter matches all pending
    items.
    """
    job_ids: Optional[List[str]] = None           # explicit allow-list
    tags: Optional[List[str]] = None              # item must carry *all* tags
    reason: Optional[FailureReason] = None        # match specific failure reason
    after_ts: Optional[str] = None               # ISO timestamp lower bound (inclusive)
    before_ts: Optional[str] = None              # ISO timestamp upper bound (inclusive)
    job_type: Optional[str] = None               # match job_id prefix (e.g. "email:")

    def matches(self, item: DeadLetterItem) -> bool:
        if self.job_ids is not None and item.job_id not in self.job_ids:
            return False
        if self.tags:
            for t in self.tags:
                if t not in item.tags:
                    return False
        if self.reason is not None and item.reason != self.reason:
            return False
        if self.after_ts and item.first_failure_ts < self.after_ts:
            return False
        if self.before_ts and item.first_failure_ts > self.before_ts:
            return False
        if self.job_type is not None and not item.job_id.startswith(self.job_type):
            return False
        return True


@dataclass
class ReplayResult:
    """Outcome of a :meth:`ReplayEngine.replay` call."""
    replayed: List[str] = field(default_factory=list)   # job_ids successfully replayed
    skipped: List[str] = field(default_factory=list)    # job_ids skipped (dry-run / budget)
    errors: List[str] = field(default_factory=list)     # job_ids that failed during replay

    @property
    def total(self) -> int:
        return len(self.replayed) + len(self.skipped) + len(self.errors)


# ---------------------------------------------------------------------------
# Idempotency store
# ---------------------------------------------------------------------------

_IDEMPOTENCY_DDL = """
CREATE TABLE IF NOT EXISTS replayed_jobs (
    job_id     TEXT    PRIMARY KEY,
    replayed_at TEXT   NOT NULL,
    attempt    INTEGER NOT NULL DEFAULT 1
);
CREATE TABLE IF NOT EXISTS job_type_budgets (
    job_type   TEXT    PRIMARY KEY,
    max_replays INTEGER NOT NULL
);
"""


class IdempotencyStore:
    """Tracks which jobs have already been replayed to prevent double-execution."""

    def __init__(self, db_path: str = ":memory:") -> None:
        self._db_path = db_path
        self._conn = sqlite3.connect(db_path)
        self._conn.row_factory = sqlite3.Row
        self._conn.executescript(_IDEMPOTENCY_DDL)
        self._conn.commit()

    def has_been_replayed(self, job_id: str) -> bool:
        row = self._conn.execute(
            "SELECT job_id FROM replayed_jobs WHERE job_id = ?", (job_id,)
        ).fetchone()
        return row is not None

    def mark_replayed(self, job_id: str) -> None:
        now = datetime.now().isoformat(timespec="seconds")
        self._conn.execute(
            "INSERT OR REPLACE INTO replayed_jobs (job_id, replayed_at, attempt) "
            "VALUES (?, ?, COALESCE((SELECT attempt + 1 FROM replayed_jobs WHERE job_id = ?), 1))",
            (job_id, now, job_id),
        )
        self._conn.commit()

    def replay_count(self, job_id: str) -> int:
        row = self._conn.execute(
            "SELECT attempt FROM replayed_jobs WHERE job_id = ?", (job_id,)
        ).fetchone()
        return row["attempt"] if row else 0

    def set_budget(self, job_type: str, max_replays: int) -> None:
        """Set a per-job-type replay budget."""
        self._conn.execute(
            "INSERT OR REPLACE INTO job_type_budgets (job_type, max_replays) VALUES (?, ?)",
            (job_type, max_replays),
        )
        self._conn.commit()

    def budget_for(self, job_type: str) -> Optional[int]:
        """Return the max-replay budget for *job_type*, or None if unlimited."""
        row = self._conn.execute(
            "SELECT max_replays FROM job_type_budgets WHERE job_type = ?", (job_type,)
        ).fetchone()
        return row["max_replays"] if row else None

    def close(self) -> None:
        self._conn.close()


# ---------------------------------------------------------------------------
# ReplayEngine
# ---------------------------------------------------------------------------

Handler = Callable[[str, str], None]   # (job_id, payload) -> None


class ReplayEngine:
    """Drives DLQ replay with filtering, idempotency, and retry budgets.

    Parameters
    ----------
    dlq:
        The :class:`~docstoolkit.dlq.queue.DeadLetterQueue` to read from.
    idempotency_db:
        Path for the idempotency SQLite store.  Use ``":memory:"`` for
        single-process use (no persistence across crashes).
    default_max_replays:
        Global default for how many times a single job_id may be replayed.
        ``None`` means unlimited.
    """

    def __init__(
        self,
        dlq: DeadLetterQueue,
        idempotency_db: str = ":memory:",
        default_max_replays: Optional[int] = None,
    ) -> None:
        self._dlq = dlq
        self._idem = IdempotencyStore(db_path=idempotency_db)
        self._default_max = default_max_replays

    def set_budget(self, job_type: str, max_replays: int) -> None:
        """Register a per-job-type retry budget (overrides global default)."""
        self._idem.set_budget(job_type, max_replays)

    def replay(
        self,
        handler: Handler,
        filter: Optional[ReplayFilter] = None,
        mode: str = "dry-run",
        limit: int = 100,
    ) -> ReplayResult:
        """Replay pending DLQ items matching *filter*.

        Parameters
        ----------
        handler:
            Callable ``(job_id, payload) -> None`` that re-processes a job.
            Must be idempotent.
        filter:
            :class:`ReplayFilter` to narrow which items to replay.
            ``None`` means replay all pending items.
        mode:
            ``"dry-run"`` — enumerate candidates but do not execute the handler
            or mutate the DLQ.
            ``"apply"`` — execute the handler and mark replayed items as
            resolved.
        limit:
            Maximum number of items to process in one call.

        Returns
        -------
        ReplayResult
        """
        if mode not in ("dry-run", "apply"):
            raise ValueError(f"mode must be 'dry-run' or 'apply', got {mode!r}")

        flt = filter or ReplayFilter()
        candidates = self._dlq.list_pending(limit=limit)
        result = ReplayResult()

        for item in candidates:
            if not flt.matches(item):
                continue

            job_type = _infer_job_type(item.job_id)
            budget = self._idem.budget_for(job_type) if job_type else None
            if budget is None:
                budget = self._default_max

            already = self._idem.replay_count(item.job_id)
            if budget is not None and already >= budget:
                result.skipped.append(item.job_id)
                continue

            if mode == "dry-run":
                result.skipped.append(item.job_id)
                continue

            # mode == "apply"
            if self._idem.has_been_replayed(item.job_id):
                # idempotency guard: already replayed in a previous call
                result.skipped.append(item.job_id)
                continue

            try:
                handler(item.job_id, item.payload)
                self._idem.mark_replayed(item.job_id)
                self._dlq.resolve(item.job_id)
                result.replayed.append(item.job_id)
            except Exception as exc:
                self._dlq.increment_attempt(item.job_id)
                result.errors.append(item.job_id)

        return result

    def close(self) -> None:
        self._idem.close()


# ---------------------------------------------------------------------------
# Convenience top-level function
# ---------------------------------------------------------------------------

def replay_dlq(
    dlq: DeadLetterQueue,
    handler: Handler,
    *,
    filter: Optional[ReplayFilter] = None,
    mode: str = "dry-run",
    limit: int = 100,
    idempotency_db: str = ":memory:",
    default_max_replays: Optional[int] = None,
) -> ReplayResult:
    """One-shot DLQ replay.

    Creates a temporary :class:`ReplayEngine`, runs the replay, and returns
    the result.  The idempotency store is discarded after the call (use
    :class:`ReplayEngine` directly if you need persistence across calls).

    Parameters mirror :meth:`ReplayEngine.replay`.
    """
    engine = ReplayEngine(
        dlq,
        idempotency_db=idempotency_db,
        default_max_replays=default_max_replays,
    )
    try:
        return engine.replay(handler, filter=filter, mode=mode, limit=limit)
    finally:
        engine.close()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _infer_job_type(job_id: str) -> Optional[str]:
    """Extract a job-type prefix from a job_id like ``"email:abc123"``."""
    if ":" in job_id:
        return job_id.split(":", 1)[0]
    return None
