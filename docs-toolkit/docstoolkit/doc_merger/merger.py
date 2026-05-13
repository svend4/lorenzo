"""Document merger implementation.

Provides multiple strategies for combining several documents:
- CONCAT       — join with a separator
- DEDUP_LINES  — concat lines, preserve order of first occurrence
- BY_SECTION   — group sections by heading across documents
- THREE_WAY    — git-style three-way merge with conflict detection
- INTERLEAVE   — round-robin lines from each doc

All algorithms use only the Python standard library (``difflib``).
"""
from __future__ import annotations

import difflib
import re
from dataclasses import dataclass, field
from enum import Enum


# ---------------------------------------------------------------------------
# Enums and data containers
# ---------------------------------------------------------------------------


class MergeStrategy(Enum):
    """Available document merge strategies."""

    CONCAT = "concat"
    DEDUP_LINES = "dedup_lines"
    BY_SECTION = "by_section"
    THREE_WAY = "three_way"
    INTERLEAVE = "interleave"


@dataclass
class MergeConflict:
    """A single conflict region between two document versions."""

    section: str
    version_a: str
    version_b: str
    line_num: int


@dataclass
class MergeResult:
    """Result of a merge operation."""

    output: str
    conflicts: list[MergeConflict] = field(default_factory=list)
    strategy: MergeStrategy = MergeStrategy.CONCAT
    source_count: int = 0

    @property
    def had_conflicts(self) -> bool:
        """True iff at least one conflict was recorded."""
        return bool(self.conflicts)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


def _parse_sections(doc: str) -> list[tuple[str, str]]:
    """Parse markdown sections.

    Returns list of (heading, body) pairs. The body excludes the heading line.
    Content before the first heading is returned under the heading ``"preamble"``
    (only if non-empty).
    """
    lines = doc.split("\n")
    sections: list[tuple[str, list[str]]] = []
    current_heading = "preamble"
    current_body: list[str] = []

    for line in lines:
        if _HEADING_RE.match(line):
            # close previous section
            if current_heading != "preamble" or current_body:
                sections.append((current_heading, current_body))
            current_heading = line
            current_body = []
        else:
            current_body.append(line)

    # tail
    if current_heading != "preamble" or current_body:
        sections.append((current_heading, current_body))

    return [(h, "\n".join(body)) for h, body in sections]


def _heading_key(heading: str) -> str:
    """Normalised heading key for case-insensitive matching."""
    if heading == "preamble":
        return "preamble"
    m = _HEADING_RE.match(heading)
    if not m:
        return heading.strip().lower()
    return m.group(2).strip().lower()


# ---------------------------------------------------------------------------
# Merger
# ---------------------------------------------------------------------------


class DocMerger:
    """Merges multiple documents using configurable strategies."""

    # -- dispatcher ----------------------------------------------------------

    def merge(
        self,
        docs: list[str],
        strategy: MergeStrategy = MergeStrategy.CONCAT,
    ) -> MergeResult:
        """Merge ``docs`` using the given strategy.

        For ``THREE_WAY`` the input must be exactly three documents:
        ``[base, a, b]``.
        """
        if strategy == MergeStrategy.CONCAT:
            output = self.merge_concat(docs)
        elif strategy == MergeStrategy.DEDUP_LINES:
            output = self.merge_dedup_lines(docs)
        elif strategy == MergeStrategy.BY_SECTION:
            output = self.merge_by_section(docs)
        elif strategy == MergeStrategy.THREE_WAY:
            if len(docs) != 3:
                raise ValueError(
                    "THREE_WAY merge requires exactly 3 documents: [base, a, b]"
                )
            result = self.merge_three_way(docs[0], docs[1], docs[2])
            result.source_count = 3
            return result
        elif strategy == MergeStrategy.INTERLEAVE:
            output = self.merge_interleave(docs)
        else:  # pragma: no cover - defensive
            raise ValueError(f"Unknown strategy: {strategy}")

        return MergeResult(
            output=output,
            conflicts=[],
            strategy=strategy,
            source_count=len(docs),
        )

    # -- concat --------------------------------------------------------------

    def merge_concat(self, docs: list[str], separator: str = "\n\n") -> str:
        """Concatenate all documents with the given separator."""
        return separator.join(docs)

    # -- dedup lines ---------------------------------------------------------

    def merge_dedup_lines(self, docs: list[str]) -> str:
        """Concat all lines, removing duplicates while preserving first-seen order."""
        seen: set[str] = set()
        out: list[str] = []
        for doc in docs:
            for line in doc.split("\n"):
                if line not in seen:
                    seen.add(line)
                    out.append(line)
        return "\n".join(out)

    # -- by section ----------------------------------------------------------

    def merge_by_section(self, docs: list[str]) -> str:
        """Group sections by heading across docs, concatenate bodies.

        Headings are matched case-insensitively. The heading text from the first
        document that uses a given heading is preserved. Bodies are concatenated
        in the order the documents appear.
        """
        # ordered dict-style storage keyed by lowercase heading
        order: list[str] = []
        headings: dict[str, str] = {}   # key -> heading text to emit
        bodies: dict[str, list[str]] = {}  # key -> list of bodies (one per occurrence)

        for doc in docs:
            for heading, body in _parse_sections(doc):
                key = _heading_key(heading)
                if key not in headings:
                    headings[key] = heading
                    bodies[key] = []
                    order.append(key)
                bodies[key].append(body)

        out_parts: list[str] = []
        for key in order:
            heading = headings[key]
            combined_body = "\n".join(b for b in bodies[key] if b is not None)
            if heading == "preamble":
                if combined_body:
                    out_parts.append(combined_body)
            else:
                out_parts.append(heading + "\n" + combined_body)

        return "\n".join(out_parts).rstrip("\n")

    # -- three-way merge -----------------------------------------------------

    def merge_three_way(self, base: str, a: str, b: str) -> MergeResult:
        """Git-style three-way merge between ``base``, ``a`` and ``b``.

        Algorithm:
        - Compare ``base`` against ``a`` and ``base`` against ``b`` via
          ``difflib.SequenceMatcher``.
        - Walk the base line by line; for each base region, determine whether
          A modified it, B modified it, both modified it identically, or both
          modified it differently.
        - Identical modifications take the modified value; non-overlapping
          modifications are applied; conflicting modifications emit
          ``<<<<<<< A`` / ``=======`` / ``>>>>>>> B`` markers and record a
          ``MergeConflict``.
        """
        base_lines = base.split("\n")
        a_lines = a.split("\n")
        b_lines = b.split("\n")

        # If base is empty (no lines), and a == b, both identical — return a
        if base == a == b:
            return MergeResult(
                output=base,
                conflicts=[],
                strategy=MergeStrategy.THREE_WAY,
                source_count=3,
            )

        # Build mapping: for each base line index, what does A say / B say?
        # We use SequenceMatcher opcodes to derive per-base-segment replacements.
        sm_a = difflib.SequenceMatcher(a=base_lines, b=a_lines, autojunk=False)
        sm_b = difflib.SequenceMatcher(a=base_lines, b=b_lines, autojunk=False)

        # Build "edits": list of (base_start, base_end, a_replacement_lines)
        # for A, and same for B. Then merge them by walking base_lines.
        a_edits = self._opcodes_to_edits(sm_a.get_opcodes(), a_lines)
        b_edits = self._opcodes_to_edits(sm_b.get_opcodes(), b_lines)

        # Combine edits by walking base line by line; collect into atomic regions.
        # A region is a contiguous range of base lines (possibly empty for pure
        # insertions). We segment base by the union of edit boundaries.
        boundaries: set[int] = {0, len(base_lines)}
        for start, end, _ in a_edits:
            boundaries.add(start)
            boundaries.add(end)
        for start, end, _ in b_edits:
            boundaries.add(start)
            boundaries.add(end)
        bounds = sorted(boundaries)

        # Build per-segment view
        def segment_replacement(
            edits: list[tuple[int, int, list[str]]],
            seg_start: int,
            seg_end: int,
        ) -> list[str] | None:
            """Return replacement lines if any edit covers exactly this segment,
            else None meaning 'unchanged from base'."""
            # Look for an edit that exactly spans [seg_start, seg_end).
            for s, e, repl in edits:
                if s == seg_start and e == seg_end:
                    return repl
            # No matching edit; check if segment is fully outside any edit
            # range or fully inside an edit range. Since we segmented on every
            # edit boundary, exact match is the only case that applies.
            return None

        out_lines: list[str] = []
        conflicts: list[MergeConflict] = []
        current_section = "preamble"

        for i in range(len(bounds) - 1):
            seg_start, seg_end = bounds[i], bounds[i + 1]
            base_segment = base_lines[seg_start:seg_end]

            # update current section based on most recent heading in base
            for ln in base_segment:
                if _HEADING_RE.match(ln):
                    current_section = ln

            a_repl = segment_replacement(a_edits, seg_start, seg_end)
            b_repl = segment_replacement(b_edits, seg_start, seg_end)

            a_val = a_repl if a_repl is not None else base_segment
            b_val = b_repl if b_repl is not None else base_segment

            if a_repl is None and b_repl is None:
                out_lines.extend(base_segment)
            elif a_repl is None:
                out_lines.extend(b_val)
            elif b_repl is None:
                out_lines.extend(a_val)
            else:
                # both modified
                if a_val == b_val:
                    out_lines.extend(a_val)
                else:
                    # conflict
                    out_lines.append("<<<<<<< A")
                    out_lines.extend(a_val)
                    out_lines.append("=======")
                    out_lines.extend(b_val)
                    out_lines.append(">>>>>>> B")
                    conflicts.append(
                        MergeConflict(
                            section=current_section,
                            version_a="\n".join(a_val),
                            version_b="\n".join(b_val),
                            line_num=seg_start,
                        )
                    )

        return MergeResult(
            output="\n".join(out_lines),
            conflicts=conflicts,
            strategy=MergeStrategy.THREE_WAY,
            source_count=3,
        )

    @staticmethod
    def _opcodes_to_edits(
        opcodes: list[tuple[str, int, int, int, int]],
        other_lines: list[str],
    ) -> list[tuple[int, int, list[str]]]:
        """Convert SequenceMatcher opcodes (with ``a=base``) to a list of edits.

        Each edit is a tuple ``(base_start, base_end, replacement_lines)``
        representing 'the range base[base_start:base_end] should be replaced by
        replacement_lines'. ``equal`` regions are skipped.
        """
        edits: list[tuple[int, int, list[str]]] = []
        for tag, i1, i2, j1, j2 in opcodes:
            if tag == "equal":
                continue
            edits.append((i1, i2, other_lines[j1:j2]))
        return edits

    # -- interleave ----------------------------------------------------------

    def merge_interleave(self, docs: list[str]) -> str:
        """Round-robin lines from each document.

        Documents of unequal length: shorter ones simply stop contributing.
        """
        if not docs:
            return ""
        line_lists = [d.split("\n") for d in docs]
        max_len = max(len(ll) for ll in line_lists)
        out: list[str] = []
        for i in range(max_len):
            for ll in line_lists:
                if i < len(ll):
                    out.append(ll[i])
        return "\n".join(out)

    # -- section helpers -----------------------------------------------------

    def find_common_sections(self, docs: list[str]) -> list[str]:
        """Return list of section headings present in *every* document.

        Headings are compared case-insensitively. The heading text returned is
        the form used by the first document. ``preamble`` is never reported.
        Ordering: order of appearance in the first document.
        """
        if not docs:
            return []
        per_doc_keys: list[set[str]] = []
        first_doc_order: list[tuple[str, str]] = []  # (key, heading)
        for idx, doc in enumerate(docs):
            keys: set[str] = set()
            for heading, _ in _parse_sections(doc):
                if heading == "preamble":
                    continue
                k = _heading_key(heading)
                keys.add(k)
                if idx == 0:
                    if not any(prev_k == k for prev_k, _ in first_doc_order):
                        first_doc_order.append((k, heading))
            per_doc_keys.append(keys)

        common = set.intersection(*per_doc_keys) if per_doc_keys else set()
        return [heading for k, heading in first_doc_order if k in common]

    def find_unique_sections(self, docs: list[str]) -> dict[int, list[str]]:
        """Return mapping doc_index → headings unique to that document.

        A heading is "unique" if no other document contains it (case-insensitive
        match). ``preamble`` is excluded. Headings appear in the order they
        occur in each document.
        """
        per_doc_headings: list[list[tuple[str, str]]] = []  # (key, heading)
        for doc in docs:
            seen: list[tuple[str, str]] = []
            seen_keys: set[str] = set()
            for heading, _ in _parse_sections(doc):
                if heading == "preamble":
                    continue
                k = _heading_key(heading)
                if k in seen_keys:
                    continue
                seen_keys.add(k)
                seen.append((k, heading))
            per_doc_headings.append(seen)

        # union of keys across all *other* docs for each index
        result: dict[int, list[str]] = {}
        for i, headings in enumerate(per_doc_headings):
            other_keys: set[str] = set()
            for j, oth in enumerate(per_doc_headings):
                if i == j:
                    continue
                other_keys.update(k for k, _ in oth)
            unique = [h for k, h in headings if k not in other_keys]
            result[i] = unique
        return result
