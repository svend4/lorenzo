"""Diff reporting — statistics and markdown output for semantic diffs.

Pure stdlib only.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from docstoolkit.semantic_diff.diff import DiffChunk, DiffType, SemanticDiffer


# ---------------------------------------------------------------------------
# DiffStats
# ---------------------------------------------------------------------------

@dataclass
class DiffStats:
    added: int = 0
    deleted: int = 0
    modified: int = 0
    unchanged: int = 0
    reordered: int = 0

    def total_changes(self) -> int:
        """Return sum of added, deleted, modified, and reordered counts."""
        return self.added + self.deleted + self.modified + self.reordered

    def change_rate(self) -> float:
        """Return fraction of chunks that represent changes.

        Formula: total_changes / (total_changes + unchanged + 1)
        The ``+1`` denominator guard prevents ZeroDivisionError on empty diffs.
        """
        return self.total_changes() / (self.total_changes() + self.unchanged + 1)


# ---------------------------------------------------------------------------
# DiffReport
# ---------------------------------------------------------------------------

@dataclass
class DiffReport:
    old_title: str
    new_title: str
    chunks: list[DiffChunk] = field(default_factory=list)
    stats: DiffStats = field(default_factory=DiffStats)

    def significant_chunks(self, threshold: float = 0.1) -> list[DiffChunk]:
        """Return only chunks deemed significant at *threshold*."""
        return [c for c in self.chunks if c.is_significant(threshold)]

    def to_markdown(self) -> str:
        """Render a markdown summary of significant changes."""
        sig = self.significant_chunks()
        lines: list[str] = [
            f"## Diff: `{self.old_title}` → `{self.new_title}`",
            "",
            f"**Changes:** {self.stats.total_changes()} "
            f"(+{self.stats.added} added, "
            f"-{self.stats.deleted} deleted, "
            f"~{self.stats.modified} modified, "
            f"{self.stats.reordered} reordered) | "
            f"Unchanged: {self.stats.unchanged}",
            "",
        ]
        if not sig:
            lines.append("_No significant changes._")
        else:
            lines.append("### Significant changes")
            lines.append("")
            for chunk in sig:
                lines.append(f"- {chunk.summary()}")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _stats_from_chunks(chunks: list[DiffChunk]) -> DiffStats:
    stats = DiffStats()
    for c in chunks:
        if c.diff_type == DiffType.ADDITION:
            stats.added += 1
        elif c.diff_type == DiffType.DELETION:
            stats.deleted += 1
        elif c.diff_type == DiffType.MODIFICATION:
            stats.modified += 1
        elif c.diff_type == DiffType.REORDER:
            stats.reordered += 1
        else:
            stats.unchanged += 1
    return stats


# ---------------------------------------------------------------------------
# DiffReporter
# ---------------------------------------------------------------------------

class DiffReporter:
    """High-level facade that drives SemanticDiffer and produces DiffReports."""

    def __init__(self) -> None:
        self._differ = SemanticDiffer()

    def report(
        self,
        old: str,
        new: str,
        old_title: str = "old",
        new_title: str = "new",
        level: str = "sentences",
    ) -> DiffReport:
        """Produce a DiffReport comparing *old* and *new* at *level* granularity.

        Parameters
        ----------
        old, new:
            The text strings to compare.
        old_title, new_title:
            Human-readable labels used in the report header.
        level:
            One of ``"sentences"``, ``"paragraphs"``, or ``"words"``.
        """
        if level == "paragraphs":
            chunks = self._differ.diff_paragraphs(old, new)
        elif level == "words":
            chunks = self._differ.diff_words(old, new)
        else:
            chunks = self._differ.diff_sentences(old, new)

        stats = _stats_from_chunks(chunks)
        return DiffReport(
            old_title=old_title,
            new_title=new_title,
            chunks=chunks,
            stats=stats,
        )

    def compare_sections(
        self,
        old_sections: dict[str, str],
        new_sections: dict[str, str],
    ) -> dict[str, DiffReport]:
        """Compare matching keys from two section dicts.

        Only keys that appear in **both** dicts are compared; sections present
        in only one dict are ignored (callers should detect additions/deletions
        themselves).
        """
        results: dict[str, DiffReport] = {}
        common_keys = old_sections.keys() & new_sections.keys()
        for key in sorted(common_keys):
            results[key] = self.report(
                old_sections[key],
                new_sections[key],
                old_title=f"{key} (old)",
                new_title=f"{key} (new)",
            )
        return results
