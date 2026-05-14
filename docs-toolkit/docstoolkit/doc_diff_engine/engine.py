"""DocDiffEngine — compute and cache line-level document diffs (stdlib only)."""

from __future__ import annotations

import difflib
import threading
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class DiffLine:
    """A single line of a diff result."""

    op: str  # "equal", "insert", "delete"
    line: str
    line_number_a: Optional[int] = None  # 1-based, present for equal/delete
    line_number_b: Optional[int] = None  # 1-based, present for equal/insert


@dataclass
class DiffResult:
    """The full diff between two versions of a document."""

    doc_id: str
    version_a: str
    version_b: str
    lines: list[DiffLine] = field(default_factory=list)
    additions: int = 0
    deletions: int = 0
    computed_at: float = 0.0


@dataclass
class DiffStats:
    """Aggregate statistics for the engine's cache."""

    total_diffs: int = 0
    unique_docs: int = 0


class DocDiffEngine:
    """Compute and cache line-level diffs between document versions.

    Thread-safe via an internal :class:`threading.Lock`.
    Uses :func:`difflib.ndiff` for line diffing.
    """

    def __init__(self) -> None:
        self._cache: dict[tuple, DiffResult] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Computation
    # ------------------------------------------------------------------
    def compute(
        self,
        doc_id: str,
        version_a_label: str,
        content_a: str,
        version_b_label: str,
        content_b: str,
        cache: bool = True,
        now: Optional[float] = None,
    ) -> DiffResult:
        """Compute the diff between two pieces of content."""
        lines_a = content_a.split("\n")
        lines_b = content_b.split("\n")

        diff_lines: list[DiffLine] = []
        additions = 0
        deletions = 0
        counter_a = 0
        counter_b = 0

        for raw in difflib.ndiff(lines_a, lines_b):
            if not raw:
                continue
            tag = raw[:2]
            text = raw[2:] if len(raw) >= 2 else ""
            if tag == "  ":
                counter_a += 1
                counter_b += 1
                diff_lines.append(
                    DiffLine(
                        op="equal",
                        line=text,
                        line_number_a=counter_a,
                        line_number_b=counter_b,
                    )
                )
            elif tag == "+ ":
                counter_b += 1
                additions += 1
                diff_lines.append(
                    DiffLine(
                        op="insert",
                        line=text,
                        line_number_a=None,
                        line_number_b=counter_b,
                    )
                )
            elif tag == "- ":
                counter_a += 1
                deletions += 1
                diff_lines.append(
                    DiffLine(
                        op="delete",
                        line=text,
                        line_number_a=counter_a,
                        line_number_b=None,
                    )
                )
            elif tag == "? ":
                # hint line, skip
                continue
            else:
                # unexpected, skip
                continue

        timestamp = now if now is not None else time.time()
        result = DiffResult(
            doc_id=doc_id,
            version_a=version_a_label,
            version_b=version_b_label,
            lines=diff_lines,
            additions=additions,
            deletions=deletions,
            computed_at=timestamp,
        )

        if cache:
            key = (doc_id, version_a_label, version_b_label)
            with self._lock:
                self._cache[key] = result

        return result

    # ------------------------------------------------------------------
    # Cache access
    # ------------------------------------------------------------------
    def get_cached(
        self, doc_id: str, version_a: str, version_b: str
    ) -> Optional[DiffResult]:
        """Return the cached diff if present, else ``None``."""
        key = (doc_id, version_a, version_b)
        with self._lock:
            return self._cache.get(key)

    def invalidate(self, doc_id: str) -> int:
        """Remove all cached diffs for *doc_id*. Return the number removed."""
        with self._lock:
            keys = [k for k in self._cache if k[0] == doc_id]
            for k in keys:
                del self._cache[k]
            return len(keys)

    def invalidate_all(self) -> int:
        """Clear the entire cache; return the number of entries removed."""
        with self._lock:
            count = len(self._cache)
            self._cache.clear()
            return count

    # ------------------------------------------------------------------
    # Reporting
    # ------------------------------------------------------------------
    def summary(self, diff: DiffResult) -> dict:
        """Return ``{"additions": …, "deletions": …, "unchanged": …}``."""
        unchanged = sum(1 for ln in diff.lines if ln.op == "equal")
        return {
            "additions": diff.additions,
            "deletions": diff.deletions,
            "unchanged": unchanged,
        }

    def as_text(self, diff: DiffResult) -> str:
        """Format the diff as unified-like text joined by newlines."""
        prefixes = {"equal": "  ", "insert": "+ ", "delete": "- "}
        out: list[str] = []
        for ln in diff.lines:
            prefix = prefixes.get(ln.op, "  ")
            out.append(f"{prefix}{ln.line}")
        return "\n".join(out)

    def stats(self) -> DiffStats:
        """Return aggregate cache statistics."""
        with self._lock:
            total = len(self._cache)
            unique_docs = len({k[0] for k in self._cache})
        return DiffStats(total_diffs=total, unique_docs=unique_docs)
