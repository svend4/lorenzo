"""Tests for E417 docstoolkit.doc_trash_bin."""
from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_trash_bin import DocTrashBin, TrashedDoc, TrashStats


# ---------------------------------------------------------------------------
# TrashedDoc dataclass
# ---------------------------------------------------------------------------


class TestTrashedDoc:
    def test_construct_minimal(self):
        d = TrashedDoc(doc_id="a", content="hello")
        assert d.doc_id == "a"
        assert d.content == "hello"
        assert d.trashed_at == 0.0
        assert d.trashed_by == ""
        assert d.reason == ""
        assert d.expires_at is None
        assert d.metadata == {}

    def test_construct_full(self):
        d = TrashedDoc(
            doc_id="x",
            content="body",
            trashed_at=10.0,
            trashed_by="alice",
            reason="duplicate",
            expires_at=20.0,
            metadata={"k": "v"},
        )
        assert d.trashed_by == "alice"
        assert d.reason == "duplicate"
        assert d.expires_at == 20.0
        assert d.metadata == {"k": "v"}

    def test_metadata_default_independent(self):
        a = TrashedDoc("a", "")
        b = TrashedDoc("b", "")
        a.metadata["k"] = 1
        assert b.metadata == {}

    def test_is_expired_when_no_expiry(self):
        d = TrashedDoc("a", "c")
        assert d.is_expired(now=10**9) is False

    def test_is_expired_when_past(self):
        d = TrashedDoc("a", "c", expires_at=5.0)
        assert d.is_expired(now=10.0) is True

    def test_is_expired_when_future(self):
        d = TrashedDoc("a", "c", expires_at=100.0)
        assert d.is_expired(now=10.0) is False

    def test_is_expired_at_boundary(self):
        d = TrashedDoc("a", "c", expires_at=10.0)
        # strict less-than: equality does NOT count as expired
        assert d.is_expired(now=10.0) is False


# ---------------------------------------------------------------------------
# TrashStats dataclass
# ---------------------------------------------------------------------------


class TestTrashStats:
    def test_construct(self):
        s = TrashStats(total_trashed=3, expired_count=1, total_size_chars=120)
        assert s.total_trashed == 3
        assert s.expired_count == 1
        assert s.total_size_chars == 120


# ---------------------------------------------------------------------------
# trash() / restore() / peek()
# ---------------------------------------------------------------------------


class TestTrashAndRestore:
    def test_trash_returns_doc(self):
        bin_ = DocTrashBin()
        d = bin_.trash("a", "hello", now=1.0)
        assert isinstance(d, TrashedDoc)
        assert d.doc_id == "a"
        assert d.content == "hello"
        assert d.trashed_at == 1.0

    def test_trash_sets_optional_fields(self):
        bin_ = DocTrashBin()
        d = bin_.trash(
            "a", "x", trashed_by="bob", reason="r", metadata={"k": 1}, now=5.0
        )
        assert d.trashed_by == "bob"
        assert d.reason == "r"
        assert d.metadata == {"k": 1}

    def test_trash_with_retention_seconds(self):
        bin_ = DocTrashBin()
        d = bin_.trash("a", "x", retention_seconds=60.0, now=100.0)
        assert d.expires_at == 160.0

    def test_trash_without_retention_has_no_expiry(self):
        bin_ = DocTrashBin()
        d = bin_.trash("a", "x", now=100.0)
        assert d.expires_at is None

    def test_trash_overwrites_existing(self):
        bin_ = DocTrashBin()
        bin_.trash("a", "first", now=1.0)
        bin_.trash("a", "second", now=2.0)
        doc = bin_.peek("a")
        assert doc is not None
        assert doc.content == "second"
        assert doc.trashed_at == 2.0

    def test_trash_uses_time_when_now_none(self):
        bin_ = DocTrashBin()
        d = bin_.trash("a", "x")
        # We don't pin to exact value, just that it's non-zero (real time stamp).
        assert d.trashed_at > 0.0

    def test_trash_copies_metadata(self):
        bin_ = DocTrashBin()
        meta = {"k": "v"}
        d = bin_.trash("a", "x", metadata=meta, now=1.0)
        meta["k"] = "MUTATED"
        assert d.metadata == {"k": "v"}

    def test_trash_default_metadata_is_dict(self):
        bin_ = DocTrashBin()
        d = bin_.trash("a", "x", now=1.0)
        assert d.metadata == {}
        assert isinstance(d.metadata, dict)

    def test_restore_returns_and_removes(self):
        bin_ = DocTrashBin()
        bin_.trash("a", "hello", now=1.0)
        doc = bin_.restore("a")
        assert doc is not None
        assert doc.content == "hello"
        assert bin_.peek("a") is None

    def test_restore_missing_returns_none(self):
        bin_ = DocTrashBin()
        assert bin_.restore("nope") is None

    def test_restore_twice_returns_none_second_time(self):
        bin_ = DocTrashBin()
        bin_.trash("a", "c", now=1.0)
        assert bin_.restore("a") is not None
        assert bin_.restore("a") is None

    def test_peek_does_not_remove(self):
        bin_ = DocTrashBin()
        bin_.trash("a", "c", now=1.0)
        for _ in range(3):
            assert bin_.peek("a") is not None
        assert bin_.is_trashed("a")

    def test_peek_missing(self):
        bin_ = DocTrashBin()
        assert bin_.peek("none") is None


# ---------------------------------------------------------------------------
# purge / purge_expired / purge_all
# ---------------------------------------------------------------------------


class TestPurge:
    def test_purge_present(self):
        bin_ = DocTrashBin()
        bin_.trash("a", "c", now=1.0)
        assert bin_.purge("a") is True
        assert bin_.is_trashed("a") is False

    def test_purge_missing(self):
        bin_ = DocTrashBin()
        assert bin_.purge("missing") is False

    def test_purge_twice(self):
        bin_ = DocTrashBin()
        bin_.trash("a", "c", now=1.0)
        assert bin_.purge("a") is True
        assert bin_.purge("a") is False

    def test_purge_expired_removes_only_expired(self):
        bin_ = DocTrashBin()
        bin_.trash("a", "c", retention_seconds=10.0, now=0.0)   # expires at 10
        bin_.trash("b", "c", retention_seconds=100.0, now=0.0)  # expires at 100
        bin_.trash("c", "c", now=0.0)                            # no expiry
        removed = bin_.purge_expired(now=50.0)
        assert removed == 1
        assert not bin_.is_trashed("a")
        assert bin_.is_trashed("b")
        assert bin_.is_trashed("c")

    def test_purge_expired_strict_inequality(self):
        bin_ = DocTrashBin()
        bin_.trash("a", "c", retention_seconds=10.0, now=0.0)  # expires_at == 10
        # at exactly now == expires_at, it is not yet "< now"
        assert bin_.purge_expired(now=10.0) == 0
        assert bin_.is_trashed("a")
        assert bin_.purge_expired(now=10.0001) == 1

    def test_purge_expired_with_no_expired(self):
        bin_ = DocTrashBin()
        bin_.trash("a", "c", retention_seconds=1000.0, now=0.0)
        assert bin_.purge_expired(now=10.0) == 0

    def test_purge_expired_empty_bin(self):
        bin_ = DocTrashBin()
        assert bin_.purge_expired(now=10.0) == 0

    def test_purge_expired_ignores_unbounded_entries(self):
        bin_ = DocTrashBin()
        bin_.trash("a", "c", now=0.0)
        bin_.trash("b", "c", now=0.0)
        assert bin_.purge_expired(now=10**9) == 0
        assert bin_.is_trashed("a")
        assert bin_.is_trashed("b")

    def test_purge_all_returns_count(self):
        bin_ = DocTrashBin()
        bin_.trash("a", "c", now=1.0)
        bin_.trash("b", "c", now=2.0)
        bin_.trash("c", "c", now=3.0)
        assert bin_.purge_all() == 3
        assert bin_.list_trashed() == []

    def test_purge_all_empty(self):
        bin_ = DocTrashBin()
        assert bin_.purge_all() == 0

    def test_purge_all_idempotent(self):
        bin_ = DocTrashBin()
        bin_.trash("a", "c", now=1.0)
        bin_.purge_all()
        assert bin_.purge_all() == 0


# ---------------------------------------------------------------------------
# is_trashed / list_trashed
# ---------------------------------------------------------------------------


class TestQueries:
    def test_is_trashed_true(self):
        bin_ = DocTrashBin()
        bin_.trash("a", "c", now=1.0)
        assert bin_.is_trashed("a") is True

    def test_is_trashed_false(self):
        bin_ = DocTrashBin()
        assert bin_.is_trashed("a") is False

    def test_is_trashed_after_restore(self):
        bin_ = DocTrashBin()
        bin_.trash("a", "c", now=1.0)
        bin_.restore("a")
        assert bin_.is_trashed("a") is False

    def test_list_trashed_empty(self):
        bin_ = DocTrashBin()
        assert bin_.list_trashed() == []

    def test_list_trashed_sorted_desc(self):
        bin_ = DocTrashBin()
        bin_.trash("a", "1", now=1.0)
        bin_.trash("b", "2", now=3.0)
        bin_.trash("c", "3", now=2.0)
        out = bin_.list_trashed()
        assert [d.doc_id for d in out] == ["b", "c", "a"]

    def test_list_trashed_returns_all(self):
        bin_ = DocTrashBin()
        for i in range(5):
            bin_.trash(f"id{i}", "c", now=float(i))
        assert len(bin_.list_trashed()) == 5


# ---------------------------------------------------------------------------
# expiring_soon / expired
# ---------------------------------------------------------------------------


class TestExpiringSoon:
    def test_expiring_soon_basic(self):
        bin_ = DocTrashBin()
        bin_.trash("a", "c", retention_seconds=50.0, now=0.0)   # exp 50
        bin_.trash("b", "c", retention_seconds=200.0, now=0.0)  # exp 200
        bin_.trash("c", "c", retention_seconds=1.0, now=0.0)    # exp 1, already expired at now=10
        # at now=10, "soon" is 100s -> only "a" qualifies (exp 50 in [10, 110]).
        out = bin_.expiring_soon(within_seconds=100.0, now=10.0)
        assert [d.doc_id for d in out] == ["a"]

    def test_expiring_soon_excludes_already_expired(self):
        bin_ = DocTrashBin()
        bin_.trash("old", "c", retention_seconds=1.0, now=0.0)  # expired
        out = bin_.expiring_soon(within_seconds=10**9, now=10.0)
        assert out == []

    def test_expiring_soon_sorted_asc(self):
        bin_ = DocTrashBin()
        bin_.trash("a", "c", retention_seconds=30.0, now=0.0)
        bin_.trash("b", "c", retention_seconds=10.0, now=0.0)
        bin_.trash("c", "c", retention_seconds=20.0, now=0.0)
        out = bin_.expiring_soon(within_seconds=1000.0, now=0.0)
        assert [d.doc_id for d in out] == ["b", "c", "a"]

    def test_expiring_soon_excludes_unbounded(self):
        bin_ = DocTrashBin()
        bin_.trash("a", "c", now=0.0)
        bin_.trash("b", "c", retention_seconds=5.0, now=0.0)
        out = bin_.expiring_soon(within_seconds=10.0, now=0.0)
        assert [d.doc_id for d in out] == ["b"]

    def test_expiring_soon_empty(self):
        bin_ = DocTrashBin()
        assert bin_.expiring_soon(within_seconds=10.0, now=0.0) == []

    def test_expiring_soon_includes_boundary_now(self):
        bin_ = DocTrashBin()
        # expires_at == now is "not yet expired" so should be included
        bin_.trash("a", "c", retention_seconds=10.0, now=0.0)
        out = bin_.expiring_soon(within_seconds=0.0, now=10.0)
        assert [d.doc_id for d in out] == ["a"]


class TestExpired:
    def test_expired_basic(self):
        bin_ = DocTrashBin()
        bin_.trash("a", "c", retention_seconds=1.0, now=0.0)  # exp 1
        bin_.trash("b", "c", retention_seconds=5.0, now=0.0)  # exp 5
        bin_.trash("c", "c", retention_seconds=100.0, now=0.0)  # exp 100
        out = bin_.expired(now=10.0)
        assert [d.doc_id for d in out] == ["a", "b"]

    def test_expired_sorted_asc(self):
        bin_ = DocTrashBin()
        bin_.trash("a", "c", retention_seconds=3.0, now=0.0)
        bin_.trash("b", "c", retention_seconds=1.0, now=0.0)
        bin_.trash("c", "c", retention_seconds=2.0, now=0.0)
        out = bin_.expired(now=100.0)
        assert [d.doc_id for d in out] == ["b", "c", "a"]

    def test_expired_excludes_unbounded(self):
        bin_ = DocTrashBin()
        bin_.trash("a", "c", now=0.0)
        out = bin_.expired(now=10**9)
        assert out == []

    def test_expired_empty(self):
        bin_ = DocTrashBin()
        assert bin_.expired(now=10.0) == []

    def test_expired_strict_inequality(self):
        bin_ = DocTrashBin()
        bin_.trash("a", "c", retention_seconds=10.0, now=0.0)  # exp 10
        assert bin_.expired(now=10.0) == []  # not yet < now
        out = bin_.expired(now=11.0)
        assert [d.doc_id for d in out] == ["a"]


# ---------------------------------------------------------------------------
# total_size / stats
# ---------------------------------------------------------------------------


class TestSizeAndStats:
    def test_total_size_empty(self):
        bin_ = DocTrashBin()
        assert bin_.total_size() == 0

    def test_total_size_sums(self):
        bin_ = DocTrashBin()
        bin_.trash("a", "abc", now=0.0)
        bin_.trash("b", "12345", now=0.0)
        assert bin_.total_size() == 8

    def test_total_size_after_restore(self):
        bin_ = DocTrashBin()
        bin_.trash("a", "abc", now=0.0)
        bin_.trash("b", "12", now=0.0)
        bin_.restore("a")
        assert bin_.total_size() == 2

    def test_stats_empty(self):
        bin_ = DocTrashBin()
        s = bin_.stats(now=0.0)
        assert s == TrashStats(total_trashed=0, expired_count=0, total_size_chars=0)

    def test_stats_with_entries(self):
        bin_ = DocTrashBin()
        bin_.trash("a", "abc", retention_seconds=1.0, now=0.0)  # exp 1
        bin_.trash("b", "xy", retention_seconds=100.0, now=0.0)  # exp 100
        bin_.trash("c", "z", now=0.0)
        s = bin_.stats(now=10.0)
        assert s.total_trashed == 3
        assert s.expired_count == 1  # "a" expired by now
        assert s.total_size_chars == 6  # 3+2+1

    def test_stats_no_expired(self):
        bin_ = DocTrashBin()
        bin_.trash("a", "xx", retention_seconds=1000.0, now=0.0)
        bin_.trash("b", "yy", now=0.0)
        s = bin_.stats(now=10.0)
        assert s.total_trashed == 2
        assert s.expired_count == 0
        assert s.total_size_chars == 4


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------


class TestThreadSafety:
    def test_concurrent_trash(self):
        bin_ = DocTrashBin()

        def worker(start: int) -> None:
            for i in range(100):
                bin_.trash(f"doc-{start}-{i}", "x" * 10, now=float(start))

        threads = [threading.Thread(target=worker, args=(s,)) for s in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(bin_.list_trashed()) == 8 * 100
        assert bin_.total_size() == 8 * 100 * 10

    def test_concurrent_trash_and_purge(self):
        bin_ = DocTrashBin()

        def trasher() -> None:
            for i in range(200):
                bin_.trash(f"d{i}", "c", now=1.0)

        def purger() -> None:
            for i in range(200):
                bin_.purge(f"d{i}")

        threads = [
            threading.Thread(target=trasher),
            threading.Thread(target=trasher),
            threading.Thread(target=purger),
            threading.Thread(target=purger),
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        # Whatever is left should be consistent — no crash, count is sane.
        assert 0 <= len(bin_.list_trashed()) <= 200

    def test_concurrent_restore_only_one_wins(self):
        bin_ = DocTrashBin()
        bin_.trash("only", "content", now=1.0)

        results: list = []
        lock = threading.Lock()

        def restorer() -> None:
            r = bin_.restore("only")
            with lock:
                results.append(r)

        threads = [threading.Thread(target=restorer) for _ in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        successes = [r for r in results if r is not None]
        assert len(successes) == 1
        assert successes[0].content == "content"

    def test_concurrent_stats_and_trash(self):
        bin_ = DocTrashBin()
        stop = threading.Event()

        def writer() -> None:
            i = 0
            while not stop.is_set():
                bin_.trash(f"d{i}", "abc", now=1.0)
                i += 1

        def reader() -> None:
            for _ in range(200):
                bin_.stats(now=1.0)
                bin_.list_trashed()
                bin_.total_size()

        wt = threading.Thread(target=writer)
        rts = [threading.Thread(target=reader) for _ in range(4)]
        wt.start()
        for t in rts:
            t.start()
        for t in rts:
            t.join()
        stop.set()
        wt.join()
        # No crash, content is internally consistent.
        s = bin_.stats(now=1.0)
        assert s.total_trashed == len(bin_.list_trashed())


# ---------------------------------------------------------------------------
# Integration / end-to-end
# ---------------------------------------------------------------------------


class TestIntegration:
    def test_full_lifecycle(self):
        bin_ = DocTrashBin()
        bin_.trash("a", "alpha", trashed_by="u", reason="dup", now=1.0)
        bin_.trash("b", "beta", retention_seconds=10.0, now=1.0)
        assert bin_.is_trashed("a") and bin_.is_trashed("b")
        assert bin_.peek("a").reason == "dup"
        restored = bin_.restore("a")
        assert restored is not None and restored.content == "alpha"
        # After 100s, "b" should be expired.
        assert bin_.expired(now=200.0)[0].doc_id == "b"
        assert bin_.purge_expired(now=200.0) == 1
        assert bin_.list_trashed() == []

    def test_metadata_round_trip_via_peek(self):
        bin_ = DocTrashBin()
        bin_.trash("a", "c", metadata={"path": "/x.md", "size": 7}, now=1.0)
        d = bin_.peek("a")
        assert d is not None
        assert d.metadata == {"path": "/x.md", "size": 7}

    def test_metadata_round_trip_via_restore(self):
        bin_ = DocTrashBin()
        bin_.trash("a", "c", metadata={"tag": "x"}, now=1.0)
        d = bin_.restore("a")
        assert d is not None
        assert d.metadata == {"tag": "x"}

    def test_stats_consistent_with_list(self):
        bin_ = DocTrashBin()
        for i in range(5):
            bin_.trash(f"d{i}", "abc", now=float(i))
        s = bin_.stats(now=10.0)
        assert s.total_trashed == len(bin_.list_trashed())
        assert s.total_size_chars == bin_.total_size()

    def test_imports_at_package_level(self):
        # Sanity: ensure __init__ re-exports work.
        from docstoolkit.doc_trash_bin import DocTrashBin, TrashedDoc, TrashStats  # noqa: F401
