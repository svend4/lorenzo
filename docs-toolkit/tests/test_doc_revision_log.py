"""Tests for docstoolkit.doc_revision_log (E340)."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_revision_log import (
    Revision,
    RevisionLogStats,
    DocRevisionLog,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _log() -> DocRevisionLog:
    return DocRevisionLog()


def _commit(
    log: DocRevisionLog,
    doc_id: str = "d1",
    content: str = "hello",
    author: str = "alice",
    message: str = "",
    now: float | None = None,
) -> Revision:
    return log.commit(
        doc_id=doc_id,
        content=content,
        author=author,
        message=message,
        now=now,
    )


# ---------------------------------------------------------------------------
# Revision dataclass
# ---------------------------------------------------------------------------


class TestRevisionDataclass:
    def test_construct_with_required_only(self):
        r = Revision(
            revision_id=1,
            doc_id="d1",
            revision_number=1,
            content="hi",
        )
        assert r.revision_id == 1
        assert r.doc_id == "d1"
        assert r.revision_number == 1
        assert r.content == "hi"

    def test_default_author_empty(self):
        r = Revision(revision_id=1, doc_id="d", revision_number=1, content="")
        assert r.author == ""

    def test_default_created_at_zero(self):
        r = Revision(revision_id=1, doc_id="d", revision_number=1, content="")
        assert r.created_at == 0.0

    def test_default_message_empty(self):
        r = Revision(revision_id=1, doc_id="d", revision_number=1, content="")
        assert r.message == ""

    def test_default_parent_revision_none(self):
        r = Revision(revision_id=1, doc_id="d", revision_number=1, content="")
        assert r.parent_revision is None

    def test_all_fields_assignable(self):
        r = Revision(
            revision_id=5,
            doc_id="dX",
            revision_number=3,
            content="text",
            author="bob",
            created_at=42.5,
            message="initial",
            parent_revision=4,
        )
        assert r.revision_id == 5
        assert r.doc_id == "dX"
        assert r.revision_number == 3
        assert r.content == "text"
        assert r.author == "bob"
        assert r.created_at == 42.5
        assert r.message == "initial"
        assert r.parent_revision == 4

    def test_equality(self):
        a = Revision(revision_id=1, doc_id="d", revision_number=1, content="x")
        b = Revision(revision_id=1, doc_id="d", revision_number=1, content="x")
        assert a == b


# ---------------------------------------------------------------------------
# RevisionLogStats dataclass
# ---------------------------------------------------------------------------


class TestRevisionLogStatsDataclass:
    def test_fields_assignable(self):
        s = RevisionLogStats(total_revisions=10, unique_docs=4, unique_authors=2)
        assert s.total_revisions == 10
        assert s.unique_docs == 4
        assert s.unique_authors == 2

    def test_equality(self):
        a = RevisionLogStats(1, 1, 1)
        b = RevisionLogStats(1, 1, 1)
        assert a == b

    def test_zero_stats(self):
        s = RevisionLogStats(0, 0, 0)
        assert s.total_revisions == 0
        assert s.unique_docs == 0
        assert s.unique_authors == 0


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------


class TestConstruction:
    def test_empty_log(self):
        assert _log().stats().total_revisions == 0

    def test_no_docs_initially(self):
        assert _log().all_doc_ids() == []

    def test_get_missing_returns_none(self):
        assert _log().get_revision(1) is None

    def test_revisions_for_unknown_doc_empty(self):
        assert _log().revisions_for_doc("nope") == []

    def test_revision_count_unknown_zero(self):
        assert _log().revision_count("nope") == 0

    def test_latest_unknown_none(self):
        assert _log().latest("nope") is None


# ---------------------------------------------------------------------------
# commit
# ---------------------------------------------------------------------------


class TestCommit:
    def test_commit_returns_revision(self):
        log = _log()
        r = _commit(log)
        assert isinstance(r, Revision)

    def test_first_revision_id_is_one(self):
        log = _log()
        r = _commit(log)
        assert r.revision_id == 1

    def test_revision_ids_increment_globally(self):
        log = _log()
        r1 = _commit(log, doc_id="a")
        r2 = _commit(log, doc_id="b")
        r3 = _commit(log, doc_id="a")
        assert [r1.revision_id, r2.revision_id, r3.revision_id] == [1, 2, 3]

    def test_revision_number_per_doc_starts_at_one(self):
        log = _log()
        r = _commit(log, doc_id="a")
        assert r.revision_number == 1

    def test_revision_number_increments_per_doc(self):
        log = _log()
        a1 = _commit(log, doc_id="a")
        a2 = _commit(log, doc_id="a")
        a3 = _commit(log, doc_id="a")
        assert [a1.revision_number, a2.revision_number, a3.revision_number] == [
            1,
            2,
            3,
        ]

    def test_revision_number_independent_across_docs(self):
        log = _log()
        a1 = _commit(log, doc_id="a")
        b1 = _commit(log, doc_id="b")
        a2 = _commit(log, doc_id="a")
        b2 = _commit(log, doc_id="b")
        assert a1.revision_number == 1
        assert a2.revision_number == 2
        assert b1.revision_number == 1
        assert b2.revision_number == 2

    def test_parent_revision_none_for_first(self):
        log = _log()
        r = _commit(log, doc_id="a")
        assert r.parent_revision is None

    def test_parent_revision_set_for_subsequent(self):
        log = _log()
        r1 = _commit(log, doc_id="a")
        r2 = _commit(log, doc_id="a")
        assert r2.parent_revision == r1.revision_id

    def test_parent_revision_chains_correctly(self):
        log = _log()
        r1 = _commit(log, doc_id="a")
        _commit(log, doc_id="b")  # interleave another doc
        r2 = _commit(log, doc_id="a")
        # parent for r2 must be r1 — not the most recent global revision.
        assert r2.parent_revision == r1.revision_id

    def test_timestamp_set_when_now_none(self):
        log = _log()
        r = _commit(log, now=None)
        assert r.created_at > 0

    def test_timestamp_uses_now_when_given(self):
        log = _log()
        r = _commit(log, now=99.5)
        assert r.created_at == 99.5

    def test_all_fields_stored(self):
        log = _log()
        r = log.commit(
            doc_id="dZ",
            content="full text",
            author="carol",
            message="initial draft",
            now=12.0,
        )
        assert r.doc_id == "dZ"
        assert r.content == "full text"
        assert r.author == "carol"
        assert r.message == "initial draft"
        assert r.created_at == 12.0

    def test_default_author_empty(self):
        log = _log()
        r = log.commit("d", "content")
        assert r.author == ""

    def test_default_message_empty(self):
        log = _log()
        r = log.commit("d", "content")
        assert r.message == ""


# ---------------------------------------------------------------------------
# get_revision
# ---------------------------------------------------------------------------


class TestGetRevision:
    def test_found(self):
        log = _log()
        r = _commit(log)
        assert log.get_revision(r.revision_id) == r

    def test_not_found(self):
        log = _log()
        _commit(log)
        assert log.get_revision(999) is None

    def test_zero_id(self):
        log = _log()
        _commit(log)
        assert log.get_revision(0) is None

    def test_negative_id(self):
        assert _log().get_revision(-1) is None


# ---------------------------------------------------------------------------
# get_by_number
# ---------------------------------------------------------------------------


class TestGetByNumber:
    def test_found(self):
        log = _log()
        r1 = _commit(log, doc_id="a", content="v1")
        r2 = _commit(log, doc_id="a", content="v2")
        assert log.get_by_number("a", 1) == r1
        assert log.get_by_number("a", 2) == r2

    def test_not_found_missing_doc(self):
        assert _log().get_by_number("nope", 1) is None

    def test_not_found_missing_number(self):
        log = _log()
        _commit(log, doc_id="a")
        assert log.get_by_number("a", 999) is None

    def test_independent_per_doc(self):
        log = _log()
        a1 = _commit(log, doc_id="a", content="A1")
        b1 = _commit(log, doc_id="b", content="B1")
        assert log.get_by_number("a", 1) == a1
        assert log.get_by_number("b", 1) == b1


# ---------------------------------------------------------------------------
# latest
# ---------------------------------------------------------------------------


class TestLatest:
    def test_returns_most_recent(self):
        log = _log()
        _commit(log, doc_id="a", content="v1")
        _commit(log, doc_id="a", content="v2")
        r3 = _commit(log, doc_id="a", content="v3")
        assert log.latest("a") == r3

    def test_none_for_empty(self):
        assert _log().latest("a") is None

    def test_none_after_unrelated_doc(self):
        log = _log()
        _commit(log, doc_id="b")
        assert log.latest("a") is None

    def test_single_revision_is_latest(self):
        log = _log()
        r = _commit(log, doc_id="a")
        assert log.latest("a") == r


# ---------------------------------------------------------------------------
# revisions_for_doc
# ---------------------------------------------------------------------------


class TestRevisionsForDoc:
    def test_returns_only_doc_revisions(self):
        log = _log()
        _commit(log, doc_id="a")
        _commit(log, doc_id="b")
        _commit(log, doc_id="a")
        out = log.revisions_for_doc("a")
        assert len(out) == 2
        assert all(r.doc_id == "a" for r in out)

    def test_most_recent_first(self):
        log = _log()
        _commit(log, doc_id="a", content="v1")
        _commit(log, doc_id="a", content="v2")
        _commit(log, doc_id="a", content="v3")
        out = log.revisions_for_doc("a")
        assert [r.revision_number for r in out] == [3, 2, 1]

    def test_limit(self):
        log = _log()
        for _ in range(5):
            _commit(log, doc_id="a")
        assert len(log.revisions_for_doc("a", limit=3)) == 3

    def test_limit_zero(self):
        log = _log()
        _commit(log, doc_id="a")
        assert log.revisions_for_doc("a", limit=0) == []

    def test_limit_larger_than_available(self):
        log = _log()
        _commit(log, doc_id="a")
        assert len(log.revisions_for_doc("a", limit=100)) == 1

    def test_unknown_doc(self):
        assert _log().revisions_for_doc("missing") == []

    def test_limit_returns_most_recent(self):
        log = _log()
        _commit(log, doc_id="a", content="v1")
        _commit(log, doc_id="a", content="v2")
        _commit(log, doc_id="a", content="v3")
        out = log.revisions_for_doc("a", limit=2)
        assert [r.revision_number for r in out] == [3, 2]


# ---------------------------------------------------------------------------
# revisions_by_author
# ---------------------------------------------------------------------------


class TestRevisionsByAuthor:
    def test_returns_only_author_revisions(self):
        log = _log()
        _commit(log, author="alice")
        _commit(log, author="bob")
        _commit(log, author="alice")
        out = log.revisions_by_author("alice")
        assert len(out) == 2
        assert all(r.author == "alice" for r in out)

    def test_sorted_by_created_at_desc(self):
        log = _log()
        _commit(log, author="alice", now=1.0)
        _commit(log, author="alice", now=5.0)
        _commit(log, author="alice", now=3.0)
        out = log.revisions_by_author("alice")
        assert [r.created_at for r in out] == [5.0, 3.0, 1.0]

    def test_cross_doc(self):
        log = _log()
        _commit(log, doc_id="a", author="alice")
        _commit(log, doc_id="b", author="alice")
        out = log.revisions_by_author("alice")
        assert {r.doc_id for r in out} == {"a", "b"}

    def test_limit(self):
        log = _log()
        for i in range(4):
            _commit(log, author="alice", now=float(i))
        assert len(log.revisions_by_author("alice", limit=2)) == 2

    def test_limit_returns_most_recent(self):
        log = _log()
        _commit(log, author="alice", now=1.0)
        _commit(log, author="alice", now=5.0)
        _commit(log, author="alice", now=3.0)
        out = log.revisions_by_author("alice", limit=2)
        assert [r.created_at for r in out] == [5.0, 3.0]

    def test_unknown_author(self):
        assert _log().revisions_by_author("nobody") == []


# ---------------------------------------------------------------------------
# revision_count
# ---------------------------------------------------------------------------


class TestRevisionCount:
    def test_zero_for_unknown(self):
        assert _log().revision_count("missing") == 0

    def test_increments(self):
        log = _log()
        _commit(log, doc_id="a")
        assert log.revision_count("a") == 1
        _commit(log, doc_id="a")
        assert log.revision_count("a") == 2
        _commit(log, doc_id="a")
        assert log.revision_count("a") == 3

    def test_independent_per_doc(self):
        log = _log()
        _commit(log, doc_id="a")
        _commit(log, doc_id="a")
        _commit(log, doc_id="b")
        assert log.revision_count("a") == 2
        assert log.revision_count("b") == 1


# ---------------------------------------------------------------------------
# revert_to
# ---------------------------------------------------------------------------


class TestRevertTo:
    def test_creates_new_revision(self):
        log = _log()
        _commit(log, doc_id="a", content="v1")
        _commit(log, doc_id="a", content="v2")
        new = log.revert_to("a", 1)
        assert new is not None
        assert new.revision_number == 3
        assert new.content == "v1"

    def test_returned_revision_is_new(self):
        log = _log()
        r1 = _commit(log, doc_id="a", content="v1")
        _commit(log, doc_id="a", content="v2")
        new = log.revert_to("a", 1)
        assert new is not None
        assert new.revision_id != r1.revision_id

    def test_parent_is_previous_revision(self):
        log = _log()
        _commit(log, doc_id="a", content="v1")
        r2 = _commit(log, doc_id="a", content="v2")
        new = log.revert_to("a", 1)
        assert new is not None
        assert new.parent_revision == r2.revision_id

    def test_count_increases(self):
        log = _log()
        _commit(log, doc_id="a", content="v1")
        _commit(log, doc_id="a", content="v2")
        log.revert_to("a", 1)
        assert log.revision_count("a") == 3

    def test_target_missing_returns_none(self):
        log = _log()
        _commit(log, doc_id="a")
        assert log.revert_to("a", 999) is None

    def test_target_missing_doesnt_create(self):
        log = _log()
        _commit(log, doc_id="a")
        log.revert_to("a", 999)
        assert log.revision_count("a") == 1

    def test_revert_unknown_doc(self):
        assert _log().revert_to("missing", 1) is None

    def test_revert_carries_author_and_message(self):
        log = _log()
        _commit(log, doc_id="a", content="v1")
        _commit(log, doc_id="a", content="v2")
        new = log.revert_to("a", 1, author="bob", message="rollback")
        assert new is not None
        assert new.author == "bob"
        assert new.message == "rollback"

    def test_revert_uses_now(self):
        log = _log()
        _commit(log, doc_id="a", content="v1", now=1.0)
        _commit(log, doc_id="a", content="v2", now=2.0)
        new = log.revert_to("a", 1, now=99.0)
        assert new is not None
        assert new.created_at == 99.0


# ---------------------------------------------------------------------------
# delete_doc_revisions
# ---------------------------------------------------------------------------


class TestDeleteDocRevisions:
    def test_returns_count(self):
        log = _log()
        _commit(log, doc_id="a")
        _commit(log, doc_id="a")
        _commit(log, doc_id="b")
        assert log.delete_doc_revisions("a") == 2

    def test_all_gone(self):
        log = _log()
        _commit(log, doc_id="a")
        _commit(log, doc_id="a")
        log.delete_doc_revisions("a")
        assert log.revisions_for_doc("a") == []
        assert log.revision_count("a") == 0
        assert log.latest("a") is None

    def test_get_by_id_gone(self):
        log = _log()
        r = _commit(log, doc_id="a")
        log.delete_doc_revisions("a")
        assert log.get_revision(r.revision_id) is None

    def test_doc_id_removed_from_all_doc_ids(self):
        log = _log()
        _commit(log, doc_id="a")
        _commit(log, doc_id="b")
        log.delete_doc_revisions("a")
        assert "a" not in log.all_doc_ids()
        assert "b" in log.all_doc_ids()

    def test_other_docs_intact(self):
        log = _log()
        _commit(log, doc_id="a")
        _commit(log, doc_id="b")
        log.delete_doc_revisions("a")
        assert log.revision_count("b") == 1

    def test_delete_unknown_returns_zero(self):
        assert _log().delete_doc_revisions("missing") == 0

    def test_stats_reflects_deletion(self):
        log = _log()
        _commit(log, doc_id="a")
        _commit(log, doc_id="a")
        log.delete_doc_revisions("a")
        assert log.stats().total_revisions == 0
        assert log.stats().unique_docs == 0


# ---------------------------------------------------------------------------
# all_doc_ids
# ---------------------------------------------------------------------------


class TestAllDocIds:
    def test_sorted(self):
        log = _log()
        _commit(log, doc_id="zzz")
        _commit(log, doc_id="aaa")
        _commit(log, doc_id="mmm")
        assert log.all_doc_ids() == ["aaa", "mmm", "zzz"]

    def test_unique(self):
        log = _log()
        _commit(log, doc_id="x")
        _commit(log, doc_id="x")
        _commit(log, doc_id="x")
        assert log.all_doc_ids() == ["x"]

    def test_empty(self):
        assert _log().all_doc_ids() == []


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------


class TestStats:
    def test_totals(self):
        log = _log()
        _commit(log, doc_id="a", author="alice")
        _commit(log, doc_id="b", author="bob")
        _commit(log, doc_id="a", author="alice")
        s = log.stats()
        assert s.total_revisions == 3
        assert s.unique_docs == 2
        assert s.unique_authors == 2

    def test_empty_stats(self):
        assert _log().stats() == RevisionLogStats(0, 0, 0)

    def test_unique_authors_dedup(self):
        log = _log()
        _commit(log, author="alice")
        _commit(log, author="alice")
        _commit(log, author="bob")
        assert log.stats().unique_authors == 2

    def test_unique_authors_skips_empty(self):
        log = _log()
        log.commit("d", "c", author="")
        log.commit("d", "c", author="")
        assert log.stats().unique_authors == 0


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------


class TestThreadSafety:
    def test_concurrent_commit(self):
        log = _log()
        N = 16
        per_thread = 25

        def worker(uid: int):
            for i in range(per_thread):
                log.commit(
                    doc_id=f"d{uid % 4}",
                    content=f"v{i}",
                    author=f"u{uid}",
                )

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(N)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        s = log.stats()
        assert s.total_revisions == N * per_thread

    def test_concurrent_commit_unique_ids(self):
        log = _log()
        ids: list[int] = []
        ids_lock = threading.Lock()

        def worker():
            for _ in range(50):
                r = log.commit("d", "c", author="u")
                with ids_lock:
                    ids.append(r.revision_id)

        threads = [threading.Thread(target=worker) for _ in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(ids) == len(set(ids))
        assert min(ids) == 1
        assert max(ids) == len(ids)

    def test_concurrent_commit_per_doc_revision_numbers_contiguous(self):
        log = _log()
        per_thread = 40

        def worker():
            for _ in range(per_thread):
                log.commit("shared", "c", author="u")

        threads = [threading.Thread(target=worker) for _ in range(6)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        revs = log.revisions_for_doc("shared")
        numbers = sorted(r.revision_number for r in revs)
        assert numbers == list(range(1, 6 * per_thread + 1))


if __name__ == "__main__":  # pragma: no cover
    pytest.main([__file__, "-q"])
