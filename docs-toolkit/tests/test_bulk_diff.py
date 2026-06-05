"""Tests for docstoolkit.diff bulk diff module."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.diff import BulkDiffer, BulkDiffResult, DocDiff
from docstoolkit.diff.bulk import (
    diff_docs,
    extract_headings,
    semantic_similarity,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

DOC_A = """# Introduction

Some text about the introduction.

## Background

More context about the background.

## Methodology

Details of the methodology used here.
"""

DOC_B = """# Introduction

Some text about the introduction (updated).

## Background

More context about the background section.

## Results

New section about the results found.
"""

SPORTS_TEXT = "football soccer players team match goal penalty kick stadium"
COOKING_TEXT = "recipe ingredients flour butter sugar bake oven cake dessert"


# ---------------------------------------------------------------------------
# S5-1  Imports
# ---------------------------------------------------------------------------

def test_imports():
    assert BulkDiffer is not None
    assert BulkDiffResult is not None
    assert DocDiff is not None


# ---------------------------------------------------------------------------
# S5-2  extract_headings
# ---------------------------------------------------------------------------

def test_extract_headings_basic():
    text = "# Title\n## Section\n### Subsection\nsome text"
    headings = extract_headings(text)
    assert headings == ["Title", "Section", "Subsection"]


def test_extract_headings_no_headings():
    text = "just plain text\nno headings at all"
    assert extract_headings(text) == []


def test_extract_headings_strips_whitespace():
    text = "#  Padded Title  \n##  Another  "
    headings = extract_headings(text)
    assert headings[0] == "Padded Title"
    assert headings[1] == "Another"


def test_extract_headings_all_levels():
    text = "\n".join(f"{'#' * i} Level {i}" for i in range(1, 7))
    headings = extract_headings(text)
    assert len(headings) == 6
    assert "Level 1" in headings
    assert "Level 6" in headings


def test_extract_headings_ignores_inline_hash():
    text = "normal text with # not heading\n# Real Heading\n"
    headings = extract_headings(text)
    assert headings == ["Real Heading"]


# ---------------------------------------------------------------------------
# S5-3  semantic_similarity
# ---------------------------------------------------------------------------

def test_semantic_similarity_identical():
    text = "python programming code function class module library"
    sim = semantic_similarity(text, text)
    assert sim == pytest.approx(1.0, abs=0.01)


def test_semantic_similarity_different():
    sim = semantic_similarity(SPORTS_TEXT, COOKING_TEXT)
    assert sim < 0.3


def test_semantic_similarity_empty():
    assert semantic_similarity("", "some text") == 0.0
    assert semantic_similarity("some text", "") == 0.0
    assert semantic_similarity("", "") == 0.0


def test_semantic_similarity_range():
    sim = semantic_similarity(DOC_A, DOC_B)
    assert 0.0 <= sim <= 1.0


def test_semantic_similarity_related_texts():
    text1 = "python code function class module programming"
    text2 = "python programming module function library class"
    sim = semantic_similarity(text1, text2)
    assert sim > 0.5


# ---------------------------------------------------------------------------
# S5-4  DocDiff dataclass
# ---------------------------------------------------------------------------

def test_docdiff_fields():
    d = DocDiff(
        path="docs/foo.md",
        change="modified",
        headings_added=["New Section"],
        headings_removed=["Old Section"],
        semantic_similarity=0.85,
        line_changes=(10, 5),
    )
    assert d.path == "docs/foo.md"
    assert d.change == "modified"
    assert d.headings_added == ["New Section"]
    assert d.headings_removed == ["Old Section"]
    assert d.semantic_similarity == 0.85
    assert d.line_changes == (10, 5)


def test_docdiff_defaults():
    d = DocDiff(path="x.md", change="added")
    assert d.headings_added == []
    assert d.headings_removed == []
    assert d.semantic_similarity == 0.0
    assert d.line_changes == (0, 0)


# ---------------------------------------------------------------------------
# S5-5  diff_docs
# ---------------------------------------------------------------------------

def test_diff_docs_modified_same_path():
    d = diff_docs("docs/a.md", DOC_A, "docs/a.md", DOC_B)
    assert d.change == "modified"
    assert d.path == "docs/a.md"


def test_diff_docs_renamed_different_path():
    d = diff_docs("docs/old.md", DOC_A, "docs/new.md", DOC_B)
    assert d.change == "renamed"
    assert d.path == "docs/new.md"


def test_diff_docs_headings_added():
    d = diff_docs("docs/a.md", DOC_A, "docs/a.md", DOC_B)
    # DOC_B has "Results" which DOC_A does not
    assert "Results" in d.headings_added


def test_diff_docs_headings_removed():
    d = diff_docs("docs/a.md", DOC_A, "docs/a.md", DOC_B)
    # DOC_A has "Methodology" which DOC_B does not
    assert "Methodology" in d.headings_removed


def test_diff_docs_similarity_close_docs():
    d = diff_docs("a.md", DOC_A, "a.md", DOC_B)
    assert d.semantic_similarity > 0.3


def test_diff_docs_line_changes():
    d = diff_docs("a.md", DOC_A, "a.md", DOC_B)
    added, removed = d.line_changes
    assert isinstance(added, int) and added >= 0
    assert isinstance(removed, int) and removed >= 0


# ---------------------------------------------------------------------------
# S5-6  BulkDiffResult dataclass
# ---------------------------------------------------------------------------

def test_bulk_diff_result_fields():
    r = BulkDiffResult(
        added=[DocDiff(path="new.md", change="added")],
        removed=[],
        modified=[],
        summary="1 added",
        total_added=1,
        total_removed=0,
        total_modified=0,
    )
    assert r.total_added == 1
    assert r.total_removed == 0
    assert r.summary == "1 added"


# ---------------------------------------------------------------------------
# S5-7  BulkDiffer instantiation
# ---------------------------------------------------------------------------

def test_bulk_differ_instantiation(tmp_path):
    differ = BulkDiffer(tmp_path)
    assert differ.docs_dir == tmp_path


# ---------------------------------------------------------------------------
# S5-8  diff_snapshots
# ---------------------------------------------------------------------------

def test_diff_snapshots_added():
    differ = BulkDiffer(Path("."))
    snap_a = {}
    snap_b = {"docs/new.md": "# New Doc\nSome content"}
    result = differ.diff_snapshots(snap_a, snap_b)
    assert result.total_added == 1
    assert result.total_removed == 0
    assert result.total_modified == 0
    assert result.added[0].path == "docs/new.md"
    assert result.added[0].change == "added"


def test_diff_snapshots_removed():
    differ = BulkDiffer(Path("."))
    snap_a = {"docs/old.md": "# Old Doc\nSome text"}
    snap_b = {}
    result = differ.diff_snapshots(snap_a, snap_b)
    assert result.total_removed == 1
    assert result.removed[0].change == "removed"


def test_diff_snapshots_modified():
    differ = BulkDiffer(Path("."))
    snap_a = {"docs/a.md": DOC_A}
    snap_b = {"docs/a.md": DOC_B}
    result = differ.diff_snapshots(snap_a, snap_b)
    assert result.total_modified == 1
    assert result.total_added == 0
    assert result.total_removed == 0
    assert result.modified[0].change == "modified"


def test_diff_snapshots_unchanged_not_in_modified():
    differ = BulkDiffer(Path("."))
    snap = {"docs/same.md": DOC_A}
    result = differ.diff_snapshots(snap, snap)
    assert result.total_modified == 0


def test_diff_snapshots_mixed():
    differ = BulkDiffer(Path("."))
    snap_a = {
        "docs/kept.md": "Same content",
        "docs/old.md": "Old content only",
        "docs/changed.md": DOC_A,
    }
    snap_b = {
        "docs/kept.md": "Same content",
        "docs/new.md": "New content here",
        "docs/changed.md": DOC_B,
    }
    result = differ.diff_snapshots(snap_a, snap_b)
    assert result.total_added == 1
    assert result.total_removed == 1
    assert result.total_modified == 1


def test_diff_snapshots_added_headings_captured():
    differ = BulkDiffer(Path("."))
    snap_a = {}
    snap_b = {"docs/new.md": "# Title\n## Section One\n## Section Two\ntext"}
    result = differ.diff_snapshots(snap_a, snap_b)
    d = result.added[0]
    assert "Title" in d.headings_added
    assert "Section One" in d.headings_added


# ---------------------------------------------------------------------------
# S5-9  to_markdown
# ---------------------------------------------------------------------------

def test_to_markdown_contains_summary(tmp_path):
    differ = BulkDiffer(tmp_path)
    snap_a = {"docs/a.md": DOC_A}
    snap_b = {"docs/b.md": DOC_B}
    result = differ.diff_snapshots(snap_a, snap_b)
    md = differ.to_markdown(result)
    assert "Added" in md or "added" in md
    assert "Removed" in md or "removed" in md


def test_to_markdown_returns_string(tmp_path):
    differ = BulkDiffer(tmp_path)
    result = BulkDiffResult(summary="empty", total_added=0, total_removed=0, total_modified=0)
    md = differ.to_markdown(result)
    assert isinstance(md, str)
    assert len(md) > 0


def test_to_markdown_contains_stats(tmp_path):
    differ = BulkDiffer(tmp_path)
    snap_a = {}
    snap_b = {"docs/new.md": "# New\nContent"}
    result = differ.diff_snapshots(snap_a, snap_b)
    md = differ.to_markdown(result)
    # Should mention counts
    assert "1" in md
