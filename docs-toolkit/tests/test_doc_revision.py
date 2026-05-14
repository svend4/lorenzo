"""Tests for docstoolkit.doc_revision."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_revision import (
    BlameLine,
    DocRevision,
    Revision,
    RevisionDiff,
    RevisionStats,
)


class TestRevision:
    def test_create_basic(self):
        rev = Revision(revision_id=1, doc_id="d", content="x", created_at=1.0)
        assert rev.revision_id == 1
        assert rev.doc_id == "d"
        assert rev.content == "x"
        assert rev.created_at == 1.0
        assert rev.author is None
        assert rev.message is None
        assert rev.parent_revision_id is None

    def test_with_optional_fields(self):
        rev = Revision(
            revision_id=2,
            doc_id="d",
            content="y",
            created_at=2.0,
            author="alice",
            message="init",
            parent_revision_id=1,
        )
        assert rev.author == "alice"
        assert rev.message == "init"
        assert rev.parent_revision_id == 1


class TestBlameLine:
    def test_create(self):
        bl = BlameLine(line_num=1, line="hello", revision_id=3)
        assert bl.line_num == 1
        assert bl.line == "hello"
        assert bl.revision_id == 3
        assert bl.author is None
        assert bl.timestamp == 0.0

    def test_with_author_and_timestamp(self):
        bl = BlameLine(
            line_num=2, line="world", revision_id=4, author="bob", timestamp=100.0
        )
        assert bl.author == "bob"
        assert bl.timestamp == 100.0


class TestRevisionDiff:
    def test_create(self):
        d = RevisionDiff(
            from_revision=1,
            to_revision=2,
            unified_diff="diff",
            lines_added=2,
            lines_removed=1,
            lines_changed=0,
        )
        assert d.from_revision == 1
        assert d.to_revision == 2
        assert d.unified_diff == "diff"
        assert d.lines_added == 2
        assert d.lines_removed == 1
        assert d.lines_changed == 0


class TestRevisionStats:
    def test_create(self):
        s = RevisionStats(
            total_docs=2,
            total_revisions=5,
            revisions_per_doc={"a": 3, "b": 2},
            authors={"alice"},
        )
        assert s.total_docs == 2
        assert s.total_revisions == 5
        assert s.revisions_per_doc == {"a": 3, "b": 2}
        assert s.authors == {"alice"}


class TestCreateRevision:
    def test_first_revision(self):
        dr = DocRevision()
        rev = dr.create_revision("d1", "hello", author="alice", now=1.0)
        assert rev.revision_id == 1
        assert rev.doc_id == "d1"
        assert rev.content == "hello"
        assert rev.author == "alice"
        assert rev.created_at == 1.0
        assert rev.parent_revision_id is None

    def test_subsequent_revision_has_parent(self):
        dr = DocRevision()
        r1 = dr.create_revision("d1", "a")
        r2 = dr.create_revision("d1", "b")
        assert r2.parent_revision_id == r1.revision_id

    def test_revision_ids_auto_increment(self):
        dr = DocRevision()
        r1 = dr.create_revision("a", "x")
        r2 = dr.create_revision("b", "y")
        r3 = dr.create_revision("a", "x2")
        assert r1.revision_id == 1
        assert r2.revision_id == 2
        assert r3.revision_id == 3

    def test_different_docs_independent_chains(self):
        dr = DocRevision()
        r1 = dr.create_revision("a", "x")
        r2 = dr.create_revision("b", "y")
        assert r2.parent_revision_id is None
        assert r1.parent_revision_id is None

    def test_with_message(self):
        dr = DocRevision()
        rev = dr.create_revision("d", "x", message="initial commit")
        assert rev.message == "initial commit"


class TestGetRevision:
    def test_existing(self):
        dr = DocRevision()
        r = dr.create_revision("d", "x")
        got = dr.get_revision(r.revision_id)
        assert got is not None
        assert got.revision_id == r.revision_id

    def test_missing(self):
        dr = DocRevision()
        assert dr.get_revision(999) is None


class TestRevisionsForDoc:
    def test_returns_newest_first(self):
        dr = DocRevision()
        r1 = dr.create_revision("d", "a")
        r2 = dr.create_revision("d", "b")
        r3 = dr.create_revision("d", "c")
        revs = dr.revisions_for_doc("d")
        assert [r.revision_id for r in revs] == [r3.revision_id, r2.revision_id, r1.revision_id]

    def test_empty_for_unknown_doc(self):
        dr = DocRevision()
        assert dr.revisions_for_doc("none") == []

    def test_limit(self):
        dr = DocRevision()
        for i in range(5):
            dr.create_revision("d", f"v{i}")
        revs = dr.revisions_for_doc("d", limit=2)
        assert len(revs) == 2


class TestLatestRevision:
    def test_returns_last_created(self):
        dr = DocRevision()
        dr.create_revision("d", "a")
        r2 = dr.create_revision("d", "b")
        latest = dr.latest_revision("d")
        assert latest is not None
        assert latest.revision_id == r2.revision_id

    def test_none_for_unknown(self):
        dr = DocRevision()
        assert dr.latest_revision("none") is None


class TestRevisionCount:
    def test_zero(self):
        dr = DocRevision()
        assert dr.revision_count("d") == 0

    def test_after_creates(self):
        dr = DocRevision()
        dr.create_revision("d", "a")
        dr.create_revision("d", "b")
        dr.create_revision("d", "c")
        assert dr.revision_count("d") == 3

    def test_independent_per_doc(self):
        dr = DocRevision()
        dr.create_revision("a", "x")
        dr.create_revision("a", "x2")
        dr.create_revision("b", "y")
        assert dr.revision_count("a") == 2
        assert dr.revision_count("b") == 1


class TestDiff:
    def test_basic_diff(self):
        dr = DocRevision()
        r1 = dr.create_revision("d", "line1\nline2")
        r2 = dr.create_revision("d", "line1\nline2\nline3")
        diff = dr.diff(r1.revision_id, r2.revision_id)
        assert diff is not None
        assert diff.from_revision == r1.revision_id
        assert diff.to_revision == r2.revision_id
        assert diff.lines_added == 1
        assert diff.lines_removed == 0

    def test_diff_removed_lines(self):
        dr = DocRevision()
        r1 = dr.create_revision("d", "a\nb\nc")
        r2 = dr.create_revision("d", "a")
        diff = dr.diff(r1.revision_id, r2.revision_id)
        assert diff is not None
        assert diff.lines_removed == 2

    def test_diff_changed_lines(self):
        dr = DocRevision()
        r1 = dr.create_revision("d", "a\nb")
        r2 = dr.create_revision("d", "a\nB")
        diff = dr.diff(r1.revision_id, r2.revision_id)
        assert diff is not None
        assert diff.lines_changed >= 1

    def test_diff_identical(self):
        dr = DocRevision()
        r1 = dr.create_revision("d", "x\ny")
        r2 = dr.create_revision("d", "x\ny")
        diff = dr.diff(r1.revision_id, r2.revision_id)
        assert diff is not None
        assert diff.lines_added == 0
        assert diff.lines_removed == 0
        assert diff.lines_changed == 0

    def test_diff_missing_revisions(self):
        dr = DocRevision()
        r1 = dr.create_revision("d", "x")
        assert dr.diff(r1.revision_id, 999) is None
        assert dr.diff(999, r1.revision_id) is None
        assert dr.diff(998, 999) is None

    def test_diff_unified_format(self):
        dr = DocRevision()
        r1 = dr.create_revision("d", "old")
        r2 = dr.create_revision("d", "new")
        diff = dr.diff(r1.revision_id, r2.revision_id)
        assert diff is not None
        assert "revision_" in diff.unified_diff


class TestDiffToLatest:
    def test_diff_to_latest(self):
        dr = DocRevision()
        r1 = dr.create_revision("d", "a")
        dr.create_revision("d", "a\nb")
        r3 = dr.create_revision("d", "a\nb\nc")
        diff = dr.diff_to_latest("d", r1.revision_id)
        assert diff is not None
        assert diff.from_revision == r1.revision_id
        assert diff.to_revision == r3.revision_id
        assert diff.lines_added == 2

    def test_unknown_doc(self):
        dr = DocRevision()
        assert dr.diff_to_latest("none", 1) is None

    def test_unknown_revision(self):
        dr = DocRevision()
        dr.create_revision("d", "x")
        assert dr.diff_to_latest("d", 999) is None

    def test_revision_belongs_to_other_doc(self):
        dr = DocRevision()
        r1 = dr.create_revision("a", "x")
        dr.create_revision("b", "y")
        assert dr.diff_to_latest("b", r1.revision_id) is None


class TestBlame:
    def test_blame_single_revision(self):
        dr = DocRevision()
        r = dr.create_revision("d", "line1\nline2", author="alice", now=1.0)
        blame = dr.blame("d")
        assert len(blame) == 2
        assert blame[0].line_num == 1
        assert blame[0].line == "line1"
        assert blame[0].revision_id == r.revision_id
        assert blame[0].author == "alice"
        assert blame[0].timestamp == 1.0
        assert blame[1].line_num == 2

    def test_blame_multi_revision(self):
        dr = DocRevision()
        r1 = dr.create_revision("d", "a\nb", author="alice", now=1.0)
        r2 = dr.create_revision("d", "a\nB\nc", author="bob", now=2.0)
        blame = dr.blame("d")
        assert len(blame) == 3
        # Line "a" was introduced in r1
        assert blame[0].line == "a"
        assert blame[0].revision_id == r1.revision_id
        assert blame[0].author == "alice"
        # Line "B" was introduced in r2 (different from "b")
        assert blame[1].line == "B"
        assert blame[1].revision_id == r2.revision_id
        assert blame[1].author == "bob"
        # Line "c" introduced in r2
        assert blame[2].line == "c"
        assert blame[2].revision_id == r2.revision_id

    def test_blame_specific_revision(self):
        dr = DocRevision()
        r1 = dr.create_revision("d", "a\nb", author="alice")
        dr.create_revision("d", "a\nb\nc", author="bob")
        blame = dr.blame("d", revision_id=r1.revision_id)
        assert len(blame) == 2
        assert all(b.revision_id == r1.revision_id for b in blame)

    def test_blame_empty_doc(self):
        dr = DocRevision()
        assert dr.blame("none") == []

    def test_blame_unknown_revision(self):
        dr = DocRevision()
        dr.create_revision("d", "x")
        assert dr.blame("d", revision_id=999) == []

    def test_blame_revision_wrong_doc(self):
        dr = DocRevision()
        r1 = dr.create_revision("a", "x")
        dr.create_revision("b", "y")
        assert dr.blame("b", revision_id=r1.revision_id) == []


class TestRollback:
    def test_rollback_creates_new_revision(self):
        dr = DocRevision()
        r1 = dr.create_revision("d", "v1")
        dr.create_revision("d", "v2")
        r3 = dr.rollback("d", r1.revision_id, author="charlie", now=10.0)
        assert r3 is not None
        assert r3.content == "v1"
        assert r3.author == "charlie"
        assert r3.created_at == 10.0
        assert dr.revision_count("d") == 3

    def test_rollback_message_references_target(self):
        dr = DocRevision()
        r1 = dr.create_revision("d", "v1")
        dr.create_revision("d", "v2")
        r3 = dr.rollback("d", r1.revision_id)
        assert r3 is not None
        assert str(r1.revision_id) in r3.message

    def test_rollback_unknown_revision(self):
        dr = DocRevision()
        dr.create_revision("d", "x")
        assert dr.rollback("d", 999) is None

    def test_rollback_wrong_doc(self):
        dr = DocRevision()
        r1 = dr.create_revision("a", "x")
        dr.create_revision("b", "y")
        assert dr.rollback("b", r1.revision_id) is None

    def test_rollback_latest_is_new_rev(self):
        dr = DocRevision()
        r1 = dr.create_revision("d", "v1")
        dr.create_revision("d", "v2")
        r3 = dr.rollback("d", r1.revision_id)
        latest = dr.latest_revision("d")
        assert latest is not None
        assert latest.revision_id == r3.revision_id


class TestRestoreTo:
    def test_restore_drops_later(self):
        dr = DocRevision()
        r1 = dr.create_revision("d", "a")
        dr.create_revision("d", "b")
        dr.create_revision("d", "c")
        assert dr.restore_to("d", r1.revision_id) is True
        assert dr.revision_count("d") == 1
        latest = dr.latest_revision("d")
        assert latest is not None
        assert latest.revision_id == r1.revision_id

    def test_restore_unknown(self):
        dr = DocRevision()
        dr.create_revision("d", "x")
        assert dr.restore_to("d", 999) is False

    def test_restore_wrong_doc(self):
        dr = DocRevision()
        r1 = dr.create_revision("a", "x")
        dr.create_revision("b", "y")
        assert dr.restore_to("b", r1.revision_id) is False

    def test_restore_to_latest_noop(self):
        dr = DocRevision()
        dr.create_revision("d", "a")
        r2 = dr.create_revision("d", "b")
        assert dr.restore_to("d", r2.revision_id) is True
        assert dr.revision_count("d") == 2


class TestDeleteRevision:
    def test_delete_existing(self):
        dr = DocRevision()
        r = dr.create_revision("d", "x")
        assert dr.delete_revision(r.revision_id) is True
        assert dr.get_revision(r.revision_id) is None
        assert dr.revision_count("d") == 0

    def test_delete_missing(self):
        dr = DocRevision()
        assert dr.delete_revision(999) is False

    def test_delete_one_of_many(self):
        dr = DocRevision()
        r1 = dr.create_revision("d", "a")
        r2 = dr.create_revision("d", "b")
        assert dr.delete_revision(r1.revision_id) is True
        assert dr.revision_count("d") == 1
        latest = dr.latest_revision("d")
        assert latest.revision_id == r2.revision_id


class TestDeleteDoc:
    def test_delete_doc(self):
        dr = DocRevision()
        dr.create_revision("d", "a")
        dr.create_revision("d", "b")
        dr.create_revision("d", "c")
        n = dr.delete_doc("d")
        assert n == 3
        assert dr.revision_count("d") == 0

    def test_delete_doc_unknown(self):
        dr = DocRevision()
        assert dr.delete_doc("none") == 0

    def test_delete_doc_keeps_others(self):
        dr = DocRevision()
        dr.create_revision("a", "x")
        dr.create_revision("b", "y")
        dr.delete_doc("a")
        assert dr.revision_count("b") == 1


class TestAuthorsForDoc:
    def test_authors(self):
        dr = DocRevision()
        dr.create_revision("d", "x", author="alice")
        dr.create_revision("d", "y", author="bob")
        dr.create_revision("d", "z", author="alice")
        assert dr.authors_for_doc("d") == {"alice", "bob"}

    def test_authors_empty(self):
        dr = DocRevision()
        assert dr.authors_for_doc("none") == set()

    def test_authors_skip_none(self):
        dr = DocRevision()
        dr.create_revision("d", "x")
        dr.create_revision("d", "y", author="alice")
        assert dr.authors_for_doc("d") == {"alice"}


class TestRevisionsByAuthor:
    def test_by_author(self):
        dr = DocRevision()
        r1 = dr.create_revision("a", "x", author="alice")
        dr.create_revision("a", "y", author="bob")
        r3 = dr.create_revision("b", "z", author="alice")
        revs = dr.revisions_by_author("alice")
        ids = {r.revision_id for r in revs}
        assert ids == {r1.revision_id, r3.revision_id}

    def test_unknown_author(self):
        dr = DocRevision()
        dr.create_revision("d", "x", author="alice")
        assert dr.revisions_by_author("nobody") == []


class TestStats:
    def test_stats_empty(self):
        dr = DocRevision()
        s = dr.stats()
        assert s.total_docs == 0
        assert s.total_revisions == 0
        assert s.revisions_per_doc == {}
        assert s.authors == set()

    def test_stats_populated(self):
        dr = DocRevision()
        dr.create_revision("a", "x", author="alice")
        dr.create_revision("a", "y", author="bob")
        dr.create_revision("b", "z", author="alice")
        s = dr.stats()
        assert s.total_docs == 2
        assert s.total_revisions == 3
        assert s.revisions_per_doc == {"a": 2, "b": 1}
        assert s.authors == {"alice", "bob"}


class TestTotalRevisions:
    def test_property_zero(self):
        dr = DocRevision()
        assert dr.total_revisions == 0

    def test_property_after_creates(self):
        dr = DocRevision()
        dr.create_revision("a", "x")
        dr.create_revision("b", "y")
        assert dr.total_revisions == 2


class TestClear:
    def test_clear_resets_state(self):
        dr = DocRevision()
        dr.create_revision("d", "x")
        dr.create_revision("d", "y")
        dr.clear()
        assert dr.total_revisions == 0
        assert dr.revision_count("d") == 0
        assert dr.latest_revision("d") is None

    def test_clear_resets_id_counter(self):
        dr = DocRevision()
        dr.create_revision("d", "x")
        dr.clear()
        new_r = dr.create_revision("d", "y")
        assert new_r.revision_id == 1


class TestEdgeCases:
    def test_empty_content(self):
        dr = DocRevision()
        r = dr.create_revision("d", "")
        assert r.content == ""
        blame = dr.blame("d")
        # splitlines on empty string returns []
        assert blame == []

    def test_single_line_no_newline(self):
        dr = DocRevision()
        dr.create_revision("d", "single")
        blame = dr.blame("d")
        assert len(blame) == 1
        assert blame[0].line == "single"

    def test_thread_safety_concurrent_creates(self):
        dr = DocRevision()
        n_threads = 8
        per_thread = 25

        def worker(i):
            for j in range(per_thread):
                dr.create_revision(f"doc_{i}", f"content_{j}", author=f"author_{i}")

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(n_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert dr.total_revisions == n_threads * per_thread
        # Ensure unique revision ids
        ids = set()
        for i in range(n_threads):
            revs = dr.revisions_for_doc(f"doc_{i}")
            assert len(revs) == per_thread
            for r in revs:
                ids.add(r.revision_id)
        assert len(ids) == n_threads * per_thread

    def test_rollback_no_revisions(self):
        dr = DocRevision()
        assert dr.rollback("d", 1) is None

    def test_diff_to_latest_single_revision(self):
        dr = DocRevision()
        r1 = dr.create_revision("d", "only")
        diff = dr.diff_to_latest("d", r1.revision_id)
        assert diff is not None
        assert diff.from_revision == r1.revision_id
        assert diff.to_revision == r1.revision_id
        assert diff.lines_added == 0
        assert diff.lines_removed == 0

    def test_blame_after_rollback(self):
        dr = DocRevision()
        dr.create_revision("d", "old", author="alice", now=1.0)
        dr.create_revision("d", "new", author="bob", now=2.0)
        r1_id = 1
        dr.rollback("d", r1_id, author="charlie", now=3.0)
        blame = dr.blame("d")
        # the line "old" first appeared at revision 1
        assert len(blame) == 1
        assert blame[0].line == "old"
        assert blame[0].revision_id == r1_id
        assert blame[0].author == "alice"

    def test_revisions_for_doc_limit_larger_than_count(self):
        dr = DocRevision()
        dr.create_revision("d", "a")
        revs = dr.revisions_for_doc("d", limit=100)
        assert len(revs) == 1

    def test_delete_then_recreate(self):
        dr = DocRevision()
        dr.create_revision("d", "x")
        dr.delete_doc("d")
        r = dr.create_revision("d", "y")
        # next id should continue increasing (not reset, since clear was not called)
        assert r.revision_id >= 2
