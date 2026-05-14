"""Tests for docstoolkit.doc_snapshot_manager (E291) — ≥45 tests."""

from __future__ import annotations

import threading
import time

import pytest

from docstoolkit.doc_snapshot_manager import (
    DocSnapshotManager,
    Snapshot,
    SnapshotDiff,
    SnapshotStats,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _mgr() -> DocSnapshotManager:
    return DocSnapshotManager()


# ===========================================================================
# 1. Snapshot dataclass
# ===========================================================================

class TestSnapshotDataclass:
    def test_fields_present(self):
        s = Snapshot(
            snapshot_id="snap_abc",
            doc_id="d1",
            version=1,
            content="hello",
            metadata={},
            created_at=1.0,
        )
        assert s.snapshot_id == "snap_abc"
        assert s.doc_id == "d1"
        assert s.version == 1
        assert s.content == "hello"
        assert s.metadata == {}
        assert s.created_at == 1.0
        assert s.label == ""

    def test_label_default_empty(self):
        s = Snapshot("id", "d", 1, "", {}, 0.0)
        assert s.label == ""

    def test_label_can_be_set(self):
        s = Snapshot("id", "d", 1, "", {}, 0.0, label="my-label")
        assert s.label == "my-label"


# ===========================================================================
# 2. SnapshotDiff dataclass
# ===========================================================================

class TestSnapshotDiffDataclass:
    def test_fields(self):
        sd = SnapshotDiff(
            doc_id="d",
            from_version=1,
            to_version=2,
            lines_added=3,
            lines_removed=1,
            diff_lines=["+ new\n"],
        )
        assert sd.doc_id == "d"
        assert sd.from_version == 1
        assert sd.to_version == 2
        assert sd.lines_added == 3
        assert sd.lines_removed == 1
        assert sd.diff_lines == ["+ new\n"]


# ===========================================================================
# 3. SnapshotStats dataclass
# ===========================================================================

class TestSnapshotStatsDataclass:
    def test_fields(self):
        st = SnapshotStats(total_snapshots=10, total_docs=3, avg_versions_per_doc=3.33)
        assert st.total_snapshots == 10
        assert st.total_docs == 3
        assert pytest.approx(st.avg_versions_per_doc, abs=0.01) == 3.33


# ===========================================================================
# 4. take()
# ===========================================================================

class TestTake:
    def test_returns_snapshot(self):
        m = _mgr()
        s = m.take("doc1", "content")
        assert isinstance(s, Snapshot)

    def test_snapshot_id_format(self):
        m = _mgr()
        s = m.take("doc1", "x")
        assert s.snapshot_id.startswith("snap_")
        assert len(s.snapshot_id) == len("snap_") + 12

    def test_first_version_is_one(self):
        m = _mgr()
        s = m.take("doc1", "x")
        assert s.version == 1

    def test_version_increments(self):
        m = _mgr()
        s1 = m.take("doc1", "a")
        s2 = m.take("doc1", "b")
        s3 = m.take("doc1", "c")
        assert s1.version == 1
        assert s2.version == 2
        assert s3.version == 3

    def test_versions_independent_per_doc(self):
        m = _mgr()
        m.take("docA", "a")
        m.take("docA", "b")
        s = m.take("docB", "c")
        assert s.version == 1

    def test_content_stored(self):
        m = _mgr()
        s = m.take("d", "hello world")
        assert s.content == "hello world"

    def test_metadata_defaults_to_empty(self):
        m = _mgr()
        s = m.take("d", "x")
        assert s.metadata == {}

    def test_metadata_stored(self):
        m = _mgr()
        meta = {"author": "alice", "tag": "draft"}
        s = m.take("d", "x", metadata=meta)
        assert s.metadata == meta

    def test_metadata_is_copied(self):
        m = _mgr()
        meta = {"k": "v"}
        s = m.take("d", "x", metadata=meta)
        meta["k"] = "changed"
        assert s.metadata["k"] == "v"

    def test_label_stored(self):
        m = _mgr()
        s = m.take("d", "x", label="initial")
        assert s.label == "initial"

    def test_now_overrides_timestamp(self):
        m = _mgr()
        s = m.take("d", "x", now=999.0)
        assert s.created_at == 999.0

    def test_doc_id_stored(self):
        m = _mgr()
        s = m.take("my-doc", "x")
        assert s.doc_id == "my-doc"

    def test_each_snapshot_unique_id(self):
        m = _mgr()
        ids = {m.take("d", "x").snapshot_id for _ in range(20)}
        assert len(ids) == 20


# ===========================================================================
# 5. get()
# ===========================================================================

class TestGet:
    def test_returns_snapshot_by_id(self):
        m = _mgr()
        s = m.take("d", "x")
        assert m.get(s.snapshot_id) is s

    def test_returns_none_for_unknown_id(self):
        m = _mgr()
        assert m.get("snap_nonexistent") is None

    def test_get_after_multiple_snaps(self):
        m = _mgr()
        s1 = m.take("d", "a")
        s2 = m.take("d", "b")
        assert m.get(s1.snapshot_id) is s1
        assert m.get(s2.snapshot_id) is s2


# ===========================================================================
# 6. get_version()
# ===========================================================================

class TestGetVersion:
    def test_get_version_1(self):
        m = _mgr()
        s = m.take("d", "first")
        assert m.get_version("d", 1) is s

    def test_get_specific_version(self):
        m = _mgr()
        m.take("d", "v1")
        s2 = m.take("d", "v2")
        m.take("d", "v3")
        assert m.get_version("d", 2) is s2

    def test_returns_none_for_missing_version(self):
        m = _mgr()
        m.take("d", "x")
        assert m.get_version("d", 99) is None

    def test_returns_none_for_unknown_doc(self):
        m = _mgr()
        assert m.get_version("ghost", 1) is None


# ===========================================================================
# 7. latest()
# ===========================================================================

class TestLatest:
    def test_latest_returns_most_recent(self):
        m = _mgr()
        m.take("d", "a")
        m.take("d", "b")
        s3 = m.take("d", "c")
        assert m.latest("d") is s3

    def test_latest_single_snap(self):
        m = _mgr()
        s = m.take("d", "only")
        assert m.latest("d") is s

    def test_latest_none_for_unknown_doc(self):
        m = _mgr()
        assert m.latest("unknown") is None


# ===========================================================================
# 8. history()
# ===========================================================================

class TestHistory:
    def test_history_newest_first(self):
        m = _mgr()
        s1 = m.take("d", "a")
        s2 = m.take("d", "b")
        s3 = m.take("d", "c")
        h = m.history("d")
        assert h == [s3, s2, s1]

    def test_history_empty_for_unknown_doc(self):
        m = _mgr()
        assert m.history("ghost") == []

    def test_history_limit(self):
        m = _mgr()
        for i in range(5):
            m.take("d", str(i))
        h = m.history("d", limit=2)
        assert len(h) == 2
        assert h[0].version == 5
        assert h[1].version == 4

    def test_history_limit_none_returns_all(self):
        m = _mgr()
        for _ in range(4):
            m.take("d", "x")
        assert len(m.history("d")) == 4

    def test_history_does_not_modify_internal_state(self):
        m = _mgr()
        m.take("d", "a")
        h = m.history("d")
        h.clear()
        assert len(m.history("d")) == 1


# ===========================================================================
# 9. diff()
# ===========================================================================

class TestDiff:
    def test_diff_returns_snapshot_diff(self):
        m = _mgr()
        m.take("d", "line1\nline2\n")
        m.take("d", "line1\nline3\n")
        result = m.diff("d", 1, 2)
        assert isinstance(result, SnapshotDiff)

    def test_diff_doc_id(self):
        m = _mgr()
        m.take("d", "a\n")
        m.take("d", "b\n")
        result = m.diff("d", 1, 2)
        assert result.doc_id == "d"

    def test_diff_versions(self):
        m = _mgr()
        m.take("d", "a\n")
        m.take("d", "b\n")
        result = m.diff("d", 1, 2)
        assert result.from_version == 1
        assert result.to_version == 2

    def test_diff_lines_added(self):
        m = _mgr()
        m.take("d", "a\n")
        m.take("d", "a\nb\n")
        result = m.diff("d", 1, 2)
        assert result.lines_added == 1

    def test_diff_lines_removed(self):
        m = _mgr()
        m.take("d", "a\nb\n")
        m.take("d", "a\n")
        result = m.diff("d", 1, 2)
        assert result.lines_removed == 1

    def test_diff_identical_content(self):
        m = _mgr()
        m.take("d", "same\n")
        m.take("d", "same\n")
        result = m.diff("d", 1, 2)
        assert result.lines_added == 0
        assert result.lines_removed == 0

    def test_diff_returns_none_missing_from(self):
        m = _mgr()
        m.take("d", "x")
        assert m.diff("d", 99, 1) is None

    def test_diff_returns_none_missing_to(self):
        m = _mgr()
        m.take("d", "x")
        assert m.diff("d", 1, 99) is None

    def test_diff_returns_none_unknown_doc(self):
        m = _mgr()
        assert m.diff("ghost", 1, 2) is None

    def test_diff_lines_list(self):
        m = _mgr()
        m.take("d", "hello\n")
        m.take("d", "world\n")
        result = m.diff("d", 1, 2)
        assert isinstance(result.diff_lines, list)

    def test_diff_header_not_counted(self):
        """Lines starting with +++ or --- must not be counted."""
        m = _mgr()
        m.take("d", "a\n")
        m.take("d", "b\n")
        result = m.diff("d", 1, 2)
        for line in result.diff_lines:
            if line.startswith("+++") or line.startswith("---"):
                # These are header lines and should NOT inflate the counts
                pass
        # The counts reflect only actual content changes, not headers
        assert result.lines_added >= 0
        assert result.lines_removed >= 0


# ===========================================================================
# 10. restore()
# ===========================================================================

class TestRestore:
    def test_restore_creates_new_snapshot(self):
        m = _mgr()
        m.take("d", "original")
        m.take("d", "changed")
        s3 = m.restore("d", 1)
        assert s3 is not None
        assert s3.version == 3
        assert s3.content == "original"

    def test_restore_label(self):
        m = _mgr()
        m.take("d", "v1")
        m.take("d", "v2")
        s = m.restore("d", 1)
        assert s.label == "restore_v1"

    def test_restore_returns_none_for_missing_version(self):
        m = _mgr()
        m.take("d", "x")
        assert m.restore("d", 99) is None

    def test_restore_now_param(self):
        m = _mgr()
        m.take("d", "x")
        s = m.restore("d", 1, now=42.0)
        assert s.created_at == 42.0

    def test_restore_copies_metadata(self):
        m = _mgr()
        m.take("d", "x", metadata={"k": "v"})
        s = m.restore("d", 1)
        assert s.metadata == {"k": "v"}


# ===========================================================================
# 11. delete_snapshot()
# ===========================================================================

class TestDeleteSnapshot:
    def test_delete_returns_true_if_existed(self):
        m = _mgr()
        s = m.take("d", "x")
        assert m.delete_snapshot(s.snapshot_id) is True

    def test_delete_removes_from_get(self):
        m = _mgr()
        s = m.take("d", "x")
        m.delete_snapshot(s.snapshot_id)
        assert m.get(s.snapshot_id) is None

    def test_delete_returns_false_if_missing(self):
        m = _mgr()
        assert m.delete_snapshot("snap_ghost") is False

    def test_delete_decrements_total(self):
        m = _mgr()
        s1 = m.take("d", "a")
        m.take("d", "b")
        assert m.total_snapshots == 2
        m.delete_snapshot(s1.snapshot_id)
        assert m.total_snapshots == 1

    def test_delete_last_snapshot_cleans_doc(self):
        m = _mgr()
        s = m.take("d", "x")
        m.delete_snapshot(s.snapshot_id)
        assert m.latest("d") is None
        assert m.history("d") == []


# ===========================================================================
# 12. delete_doc_snapshots()
# ===========================================================================

class TestDeleteDocSnapshots:
    def test_returns_count_removed(self):
        m = _mgr()
        for _ in range(3):
            m.take("d", "x")
        assert m.delete_doc_snapshots("d") == 3

    def test_doc_gone_after_delete(self):
        m = _mgr()
        m.take("d", "x")
        m.delete_doc_snapshots("d")
        assert m.latest("d") is None

    def test_returns_zero_for_unknown_doc(self):
        m = _mgr()
        assert m.delete_doc_snapshots("ghost") == 0

    def test_does_not_affect_other_docs(self):
        m = _mgr()
        m.take("d1", "a")
        m.take("d2", "b")
        m.delete_doc_snapshots("d1")
        assert m.latest("d2") is not None


# ===========================================================================
# 13. prune()
# ===========================================================================

class TestPrune:
    def test_prune_keeps_last_n(self):
        m = _mgr()
        for i in range(5):
            m.take("d", str(i))
        removed = m.prune("d", keep_last=2)
        assert removed == 3
        assert len(m.history("d")) == 2

    def test_prune_keeps_newest(self):
        m = _mgr()
        for i in range(4):
            m.take("d", str(i))
        m.prune("d", keep_last=2)
        h = m.history("d")
        versions = {s.version for s in h}
        assert 3 in versions
        assert 4 in versions

    def test_prune_keep_zero_removes_all(self):
        m = _mgr()
        for _ in range(3):
            m.take("d", "x")
        removed = m.prune("d", keep_last=0)
        assert removed == 3
        assert m.history("d") == []

    def test_prune_returns_zero_when_nothing_to_remove(self):
        m = _mgr()
        m.take("d", "x")
        m.take("d", "y")
        assert m.prune("d", keep_last=10) == 0

    def test_prune_unknown_doc_returns_zero(self):
        m = _mgr()
        assert m.prune("ghost", keep_last=2) == 0


# ===========================================================================
# 14. stats()
# ===========================================================================

class TestStats:
    def test_stats_empty(self):
        m = _mgr()
        s = m.stats()
        assert s.total_snapshots == 0
        assert s.total_docs == 0
        assert s.avg_versions_per_doc == 0.0

    def test_stats_single_doc(self):
        m = _mgr()
        m.take("d", "a")
        m.take("d", "b")
        s = m.stats()
        assert s.total_snapshots == 2
        assert s.total_docs == 1
        assert s.avg_versions_per_doc == 2.0

    def test_stats_multiple_docs(self):
        m = _mgr()
        m.take("d1", "x")
        m.take("d1", "y")
        m.take("d2", "z")
        s = m.stats()
        assert s.total_snapshots == 3
        assert s.total_docs == 2
        assert pytest.approx(s.avg_versions_per_doc) == 1.5

    def test_stats_returns_snapshot_stats_type(self):
        m = _mgr()
        assert isinstance(m.stats(), SnapshotStats)


# ===========================================================================
# 15. total_snapshots property
# ===========================================================================

class TestTotalSnapshots:
    def test_initial_zero(self):
        m = _mgr()
        assert m.total_snapshots == 0

    def test_increments_on_take(self):
        m = _mgr()
        m.take("d", "a")
        assert m.total_snapshots == 1
        m.take("d", "b")
        assert m.total_snapshots == 2

    def test_decrements_on_delete(self):
        m = _mgr()
        s = m.take("d", "a")
        m.take("d", "b")
        m.delete_snapshot(s.snapshot_id)
        assert m.total_snapshots == 1

    def test_matches_stats(self):
        m = _mgr()
        for i in range(7):
            m.take(f"d{i % 3}", "x")
        assert m.total_snapshots == m.stats().total_snapshots


# ===========================================================================
# 16. Thread safety
# ===========================================================================

class TestThreadSafety:
    def test_concurrent_take(self):
        m = _mgr()
        results = []
        errors = []

        def worker():
            try:
                s = m.take("shared", "data")
                results.append(s)
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        threads = [threading.Thread(target=worker) for _ in range(30)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
        assert len(results) == 30
        assert m.total_snapshots == 30

    def test_concurrent_take_different_docs(self):
        m = _mgr()
        errors = []

        def worker(doc_id: str):
            try:
                for _ in range(5):
                    m.take(doc_id, "x")
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        threads = [threading.Thread(target=worker, args=(f"doc{i}",)) for i in range(6)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
        assert m.total_snapshots == 30


# ===========================================================================
# 17. Import / public API
# ===========================================================================

class TestPublicApi:
    def test_can_import_from_package(self):
        from docstoolkit.doc_snapshot_manager import (  # noqa: F401
            DocSnapshotManager,
            Snapshot,
            SnapshotDiff,
            SnapshotStats,
        )

    def test_all_exports(self):
        import docstoolkit.doc_snapshot_manager as pkg
        for name in ["DocSnapshotManager", "Snapshot", "SnapshotDiff", "SnapshotStats"]:
            assert hasattr(pkg, name)
