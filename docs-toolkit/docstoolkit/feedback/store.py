"""Feedback stores: E19 SignalStore and legacy FeedbackStore.

Public names
------------
``SignalStore``
    New E19 store for :class:`~docstoolkit.feedback.signal.FeedbackSignal`
    objects.  Exported as ``FeedbackStore`` from the package ``__init__``.

``FeedbackStore``
    Alias to the *legacy* store (pre-E19) — kept for backward compatibility
    so that existing code doing::

        from docstoolkit.feedback.store import Feedback, FeedbackStore

    …continues to work unchanged.

``Feedback``
    Legacy feedback dataclass (re-exported from ``legacy_store``).
"""
import sqlite3
from pathlib import Path

from docstoolkit.feedback.signal import FeedbackSignal, FeedbackType

# --- backward-compat re-exports ----------------------------------------
# Keep ``from docstoolkit.feedback.store import Feedback, FeedbackStore``
# working for code that predates E19 (e.g. test_autotuner.py).
from docstoolkit.feedback.legacy_store import (  # noqa: F401
    Feedback,
    FeedbackStore,  # legacy class with .record() / .aggregate_per_skill()
)
# -----------------------------------------------------------------------


_SCHEMA = """
CREATE TABLE IF NOT EXISTS feedback_signals (
    signal_id   TEXT PRIMARY KEY,
    query       TEXT NOT NULL,
    doc_id      TEXT,
    feedback_type TEXT NOT NULL,
    value       REAL NOT NULL,
    note        TEXT NOT NULL DEFAULT '',
    ts          REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_fs_query  ON feedback_signals(query);
CREATE INDEX IF NOT EXISTS idx_fs_doc_id ON feedback_signals(doc_id);
"""


def _row_to_signal(row: sqlite3.Row) -> FeedbackSignal:
    """Reconstruct a :class:`FeedbackSignal` from a DB row (skip re-normalisation)."""
    sig = object.__new__(FeedbackSignal)
    sig.signal_id = row["signal_id"]
    sig.query = row["query"]
    sig.doc_id = row["doc_id"]
    sig.feedback_type = FeedbackType(row["feedback_type"])
    sig.value = row["value"]
    sig.note = row["note"] or ""
    sig.ts = row["ts"]
    return sig


class SignalStore:
    """Persistent (or in-memory) store for :class:`FeedbackSignal` objects.

    This is the E19 store.  It is exported as ``FeedbackStore`` from
    ``docstoolkit.feedback`` (the package ``__init__``).

    Parameters
    ----------
    db_path:
        Path to an SQLite file, or ``":memory:"`` (default) for an
        ephemeral in-process database.
    """

    def __init__(self, db_path: str | Path = ":memory:") -> None:
        self._path = str(db_path)
        self._conn = sqlite3.connect(self._path)
        self._conn.row_factory = sqlite3.Row
        self._conn.executescript(_SCHEMA)
        self._conn.commit()

    # ------------------------------------------------------------------
    # Mutations
    # ------------------------------------------------------------------

    def add(self, signal: FeedbackSignal) -> None:
        """Persist *signal* (upsert by signal_id)."""
        self._conn.execute(
            "INSERT OR REPLACE INTO feedback_signals "
            "(signal_id, query, doc_id, feedback_type, value, note, ts) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                signal.signal_id,
                signal.query,
                signal.doc_id,
                signal.feedback_type.value,
                signal.value,
                signal.note,
                signal.ts,
            ),
        )
        self._conn.commit()

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def get(self, signal_id: str) -> FeedbackSignal | None:
        """Return the signal with *signal_id*, or ``None`` if not found."""
        row = self._conn.execute(
            "SELECT * FROM feedback_signals WHERE signal_id = ?",
            (signal_id,),
        ).fetchone()
        return _row_to_signal(row) if row else None

    def for_query(self, query: str) -> list[FeedbackSignal]:
        """Return all signals whose *query* field equals *query*."""
        rows = self._conn.execute(
            "SELECT * FROM feedback_signals WHERE query = ? ORDER BY ts",
            (query,),
        ).fetchall()
        return [_row_to_signal(r) for r in rows]

    def for_doc(self, doc_id: str) -> list[FeedbackSignal]:
        """Return all signals whose *doc_id* field equals *doc_id*."""
        rows = self._conn.execute(
            "SELECT * FROM feedback_signals WHERE doc_id = ? ORDER BY ts",
            (doc_id,),
        ).fetchall()
        return [_row_to_signal(r) for r in rows]

    # ------------------------------------------------------------------
    # Aggregations
    # ------------------------------------------------------------------

    def stats(self) -> dict:
        """Return aggregate statistics across all signals.

        Returns
        -------
        dict with keys:
            total, positive, negative, neutral, avg_value
        """
        rows = self._conn.execute(
            "SELECT value FROM feedback_signals"
        ).fetchall()
        values = [r["value"] for r in rows]
        total = len(values)
        positive = sum(1 for v in values if v > 0.0)
        negative = sum(1 for v in values if v < 0.0)
        neutral = total - positive - negative
        avg_value = sum(values) / total if total else 0.0
        return {
            "total": total,
            "positive": positive,
            "negative": negative,
            "neutral": neutral,
            "avg_value": avg_value,
        }

    def top_docs(self, n: int = 10) -> list[tuple[str, float]]:
        """Return the *n* documents with the highest average signal value.

        Only documents that have at least one signal are considered.
        Returns a list of ``(doc_id, avg_value)`` sorted descending.
        """
        rows = self._conn.execute(
            "SELECT doc_id, AVG(value) AS avg_val "
            "FROM feedback_signals "
            "WHERE doc_id IS NOT NULL "
            "GROUP BY doc_id "
            "ORDER BY avg_val DESC "
            "LIMIT ?",
            (n,),
        ).fetchall()
        return [(r["doc_id"], r["avg_val"]) for r in rows]

    def worst_docs(self, n: int = 10) -> list[tuple[str, float]]:
        """Return the *n* documents with the lowest average signal value.

        Returns a list of ``(doc_id, avg_value)`` sorted ascending.
        """
        rows = self._conn.execute(
            "SELECT doc_id, AVG(value) AS avg_val "
            "FROM feedback_signals "
            "WHERE doc_id IS NOT NULL "
            "GROUP BY doc_id "
            "ORDER BY avg_val ASC "
            "LIMIT ?",
            (n,),
        ).fetchall()
        return [(r["doc_id"], r["avg_val"]) for r in rows]

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def close(self) -> None:
        self._conn.close()
