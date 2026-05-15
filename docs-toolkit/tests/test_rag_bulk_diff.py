"""Tests for bulk diff helpers (Sprint 92 / S5)."""
from __future__ import annotations

from pathlib import Path

import pytest

from docstoolkit.rag.bulk_diff import (
    DiffSummary,
    diff_corpus_dirs,
    diff_since_days,
)


def test_diff_corpus_dirs_added(tmp_path):
    a = tmp_path / "a"
    b = tmp_path / "b"
    a.mkdir()
    b.mkdir()
    (a / "old.md").write_text("legacy", encoding="utf-8")
    (b / "old.md").write_text("legacy", encoding="utf-8")
    (b / "new.md").write_text("fresh content", encoding="utf-8")

    res = diff_corpus_dirs(a, b)
    assert "new.md" in res.added
    assert res.removed == []
    assert isinstance(res.markdown, str)


def test_diff_corpus_dirs_removed(tmp_path):
    a = tmp_path / "a"
    b = tmp_path / "b"
    a.mkdir()
    b.mkdir()
    (a / "gone.md").write_text("bye", encoding="utf-8")
    (a / "stay.md").write_text("here", encoding="utf-8")
    (b / "stay.md").write_text("here", encoding="utf-8")

    res = diff_corpus_dirs(a, b)
    assert "gone.md" in res.removed
    assert res.added == []


def test_diff_corpus_dirs_modified(tmp_path):
    a = tmp_path / "a"
    b = tmp_path / "b"
    a.mkdir()
    b.mkdir()
    (a / "file.md").write_text("v1", encoding="utf-8")
    (b / "file.md").write_text("v2 with much more content here", encoding="utf-8")

    res = diff_corpus_dirs(a, b)
    assert "file.md" in res.modified


def test_diff_corpus_dirs_total_changes(tmp_path):
    a = tmp_path / "a"
    b = tmp_path / "b"
    a.mkdir()
    b.mkdir()
    (a / "x.md").write_text("a", encoding="utf-8")
    (b / "y.md").write_text("b", encoding="utf-8")
    res = diff_corpus_dirs(a, b)
    assert res.total_changes == 2  # 1 added + 1 removed


def test_diff_corpus_dirs_no_changes(tmp_path):
    a = tmp_path / "a"
    b = tmp_path / "b"
    a.mkdir()
    b.mkdir()
    (a / "x.md").write_text("same", encoding="utf-8")
    (b / "x.md").write_text("same", encoding="utf-8")
    res = diff_corpus_dirs(a, b)
    assert res.total_changes == 0


def test_diff_summary_has_markdown(tmp_path):
    a = tmp_path / "a"
    b = tmp_path / "b"
    a.mkdir()
    b.mkdir()
    (b / "new.md").write_text("# Hi", encoding="utf-8")
    res = diff_corpus_dirs(a, b)
    assert "markdown" in res.__dict__ or hasattr(res, "markdown")
    assert isinstance(res.markdown, str)


def test_diff_summary_dataclass():
    s = DiffSummary(added=["a"], modified=["b"], markdown="x")
    assert s.total_changes == 2
    assert s.markdown == "x"


def test_diff_empty_dirs(tmp_path):
    a = tmp_path / "a"
    b = tmp_path / "b"
    a.mkdir()
    b.mkdir()
    res = diff_corpus_dirs(a, b)
    assert res.total_changes == 0


def test_diff_nonexistent_dir(tmp_path):
    # `a` doesn't exist
    b = tmp_path / "b"
    b.mkdir()
    (b / "x.md").write_text("y", encoding="utf-8")
    res = diff_corpus_dirs(tmp_path / "missing", b)
    # New dir → everything in b looks added
    assert "x.md" in res.added
