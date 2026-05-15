"""Bulk diff queries — Sprint 92 / S5.

One-liner helpers wrapping `docstoolkit.diff.BulkDiffer` for everyday use.

Usage:
    from docstoolkit.rag.bulk_diff import diff_corpus_dirs, diff_commits

    res = diff_corpus_dirs(Path("docs/"), Path("/tmp/old-docs/"))
    print(res.markdown)

    res = diff_commits(Path("."), "main~10", "main")
    print(res.added, res.removed, res.modified)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from docstoolkit.diff.bulk import BulkDiffer, BulkDiffResult, DocDiff


@dataclass
class DiffSummary:
    """Compact, dataclass-only view of a `BulkDiffResult` for callers."""

    added: list[str] = field(default_factory=list)
    removed: list[str] = field(default_factory=list)
    modified: list[str] = field(default_factory=list)
    markdown: str = ""

    @property
    def total_changes(self) -> int:
        return len(self.added) + len(self.removed) + len(self.modified)


def _summarise(differ: BulkDiffer, result: BulkDiffResult) -> DiffSummary:
    return DiffSummary(
        added=[d.path for d in result.added],
        removed=[d.path for d in result.removed],
        modified=[d.path for d in result.modified],
        markdown=differ.to_markdown(result),
    )


def _snapshot(dir_path: Path) -> dict[str, str]:
    dir_path = Path(dir_path)
    out: dict[str, str] = {}
    if not dir_path.exists():
        return out
    for f in sorted(dir_path.rglob("*.md")):
        rel = str(f.relative_to(dir_path)).replace("\\", "/")
        try:
            out[rel] = f.read_text(encoding="utf-8", errors="replace")
        except (OSError, PermissionError):
            continue
    return out


def diff_corpus_dirs(dir_a: Path, dir_b: Path) -> DiffSummary:
    """Compare two directories of `.md` files by content."""
    snap_a = _snapshot(dir_a)
    snap_b = _snapshot(dir_b)
    # BulkDiffer needs a base docs_dir; use dir_b for git context if present
    differ = BulkDiffer(docs_dir=Path(dir_b))
    res = differ.diff_snapshots(snap_a, snap_b)
    return _summarise(differ, res)


def diff_commits(
    docs_dir: Path,
    commit_a: str,
    commit_b: str,
) -> DiffSummary:
    """Compare two git commits via `git diff --name-status`."""
    differ = BulkDiffer(docs_dir=Path(docs_dir))
    res = differ.diff_git_commits(commit_a, commit_b)
    return _summarise(differ, res)


def diff_since_days(
    docs_dir: Path,
    days: int,
) -> DiffSummary:
    """Compare HEAD vs the commit closest to `days` ago."""
    differ = BulkDiffer(docs_dir=Path(docs_dir))
    res = differ.diff_since(days)
    return _summarise(differ, res)
