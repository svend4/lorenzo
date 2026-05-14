"""Tests for docstoolkit.doc_conflict_resolver (E301)."""
from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_conflict_resolver import (
    Conflict,
    DocConflictResolver,
    Resolution,
    ResolverStats,
)


# ---------- helpers ----------

def _resolver() -> DocConflictResolver:
    return DocConflictResolver()


def _detect(
    r: DocConflictResolver,
    doc_id: str = "doc-1",
    version_a: str = "v1",
    version_b: str = "v2",
    field: str = "title",
    value_a: str = "Hello",
    value_b: str = "World",
    now: float = 0.0,
) -> Conflict:
    c = r.detect_conflict(
        doc_id=doc_id,
        version_a=version_a,
        version_b=version_b,
        field=field,
        value_a=value_a,
        value_b=value_b,
        now=now,
    )
    assert c is not None
    return c


# ---------- TestConflictDataclass ----------

class TestConflictDataclass:
    def test_required_fields(self):
        c = Conflict(
            conflict_id="cid",
            doc_id="doc-1",
            version_a="v1",
            version_b="v2",
            field="title",
            value_a="A",
            value_b="B",
        )
        assert c.conflict_id == "cid"
        assert c.doc_id == "doc-1"
        assert c.version_a == "v1"
        assert c.version_b == "v2"
        assert c.field == "title"
        assert c.value_a == "A"
        assert c.value_b == "B"

    def test_default_detected_at(self):
        c = Conflict("x", "d", "v1", "v2", "f", "a", "b")
        assert c.detected_at == 0.0

    def test_default_status(self):
        c = Conflict("x", "d", "v1", "v2", "f", "a", "b")
        assert c.status == "open"

    def test_custom_detected_at(self):
        c = Conflict("x", "d", "v1", "v2", "f", "a", "b", detected_at=99.9)
        assert c.detected_at == 99.9

    def test_custom_status(self):
        c = Conflict("x", "d", "v1", "v2", "f", "a", "b", status="resolved")
        assert c.status == "resolved"

    def test_is_dataclass(self):
        import dataclasses
        assert dataclasses.is_dataclass(Conflict)


# ---------- TestResolutionDataclass ----------

class TestResolutionDataclass:
    def test_required_fields(self):
        r = Resolution(
            conflict_id="cid",
            doc_id="doc-1",
            chosen_version="a",
            resolved_value="Hello",
        )
        assert r.conflict_id == "cid"
        assert r.doc_id == "doc-1"
        assert r.chosen_version == "a"
        assert r.resolved_value == "Hello"

    def test_default_resolved_at(self):
        r = Resolution("cid", "doc-1", "a", "val")
        assert r.resolved_at == 0.0

    def test_default_resolver(self):
        r = Resolution("cid", "doc-1", "a", "val")
        assert r.resolver == "manual"

    def test_custom_resolver(self):
        r = Resolution("cid", "doc-1", "b", "val", resolver="auto_latest")
        assert r.resolver == "auto_latest"

    def test_custom_resolved_at(self):
        r = Resolution("cid", "doc-1", "merged", "val", resolved_at=42.0)
        assert r.resolved_at == 42.0

    def test_is_dataclass(self):
        import dataclasses
        assert dataclasses.is_dataclass(Resolution)


# ---------- TestResolverStatsDataclass ----------

class TestResolverStatsDataclass:
    def test_fields(self):
        s = ResolverStats(
            total_conflicts=10,
            open_conflicts=4,
            resolved_conflicts=5,
            ignored_conflicts=1,
        )
        assert s.total_conflicts == 10
        assert s.open_conflicts == 4
        assert s.resolved_conflicts == 5
        assert s.ignored_conflicts == 1

    def test_is_dataclass(self):
        import dataclasses
        assert dataclasses.is_dataclass(ResolverStats)

    def test_zero_values(self):
        s = ResolverStats(0, 0, 0, 0)
        assert s.total_conflicts == 0


# ---------- TestConstruction ----------

class TestConstruction:
    def test_empty_conflicts(self):
        r = _resolver()
        assert r.all_conflicts() == []

    def test_empty_open_conflicts(self):
        r = _resolver()
        assert r.open_conflicts() == []

    def test_empty_stats(self):
        r = _resolver()
        s = r.stats()
        assert s.total_conflicts == 0
        assert s.open_conflicts == 0
        assert s.resolved_conflicts == 0
        assert s.ignored_conflicts == 0

    def test_get_conflict_missing(self):
        r = _resolver()
        assert r.get_conflict("nope") is None

    def test_get_resolution_missing(self):
        r = _resolver()
        assert r.get_resolution("nope") is None


# ---------- TestDetectConflict ----------

class TestDetectConflict:
    def test_no_conflict_when_equal(self):
        r = _resolver()
        result = r.detect_conflict("doc-1", "v1", "v2", "title", "Same", "Same")
        assert result is None

    def test_creates_conflict_when_different(self):
        r = _resolver()
        c = r.detect_conflict("doc-1", "v1", "v2", "title", "A", "B")
        assert c is not None

    def test_conflict_fields_set(self):
        r = _resolver()
        c = r.detect_conflict("doc-1", "v1", "v2", "content", "old", "new", now=5.0)
        assert c.doc_id == "doc-1"
        assert c.version_a == "v1"
        assert c.version_b == "v2"
        assert c.field == "content"
        assert c.value_a == "old"
        assert c.value_b == "new"
        assert c.detected_at == 5.0

    def test_uuid_generated(self):
        r = _resolver()
        c = r.detect_conflict("doc-1", "v1", "v2", "title", "A", "B")
        assert c.conflict_id
        assert len(c.conflict_id) > 0

    def test_unique_ids(self):
        r = _resolver()
        c1 = r.detect_conflict("doc-1", "v1", "v2", "title", "A", "B")
        c2 = r.detect_conflict("doc-1", "v1", "v2", "title", "C", "D")
        assert c1.conflict_id != c2.conflict_id

    def test_status_open(self):
        r = _resolver()
        c = r.detect_conflict("doc-1", "v1", "v2", "title", "A", "B")
        assert c.status == "open"

    def test_stored_in_registry(self):
        r = _resolver()
        c = r.detect_conflict("doc-1", "v1", "v2", "title", "A", "B")
        assert r.get_conflict(c.conflict_id) is c

    def test_no_storage_when_no_conflict(self):
        r = _resolver()
        r.detect_conflict("doc-1", "v1", "v2", "title", "Same", "Same")
        assert r.all_conflicts() == []

    def test_now_none_defaults_to_zero(self):
        r = _resolver()
        c = r.detect_conflict("doc-1", "v1", "v2", "title", "A", "B", now=None)
        assert c.detected_at == 0.0


# ---------- TestResolve ----------

class TestResolve:
    def test_resolve_creates_resolution(self):
        r = _resolver()
        c = _detect(r)
        res = r.resolve(c.conflict_id, "a", "Hello")
        assert res is not None
        assert res.conflict_id == c.conflict_id
        assert res.doc_id == c.doc_id
        assert res.chosen_version == "a"
        assert res.resolved_value == "Hello"

    def test_resolve_marks_conflict_resolved(self):
        r = _resolver()
        c = _detect(r)
        r.resolve(c.conflict_id, "b", "World")
        assert r.get_conflict(c.conflict_id).status == "resolved"

    def test_resolve_stores_resolution(self):
        r = _resolver()
        c = _detect(r)
        res = r.resolve(c.conflict_id, "a", "Hello")
        assert r.get_resolution(c.conflict_id) is res

    def test_resolve_not_found_returns_none(self):
        r = _resolver()
        assert r.resolve("nonexistent", "a", "val") is None

    def test_resolve_default_resolver(self):
        r = _resolver()
        c = _detect(r)
        res = r.resolve(c.conflict_id, "a", "Hello")
        assert res.resolver == "manual"

    def test_resolve_custom_resolver(self):
        r = _resolver()
        c = _detect(r)
        res = r.resolve(c.conflict_id, "b", "World", resolver="auto_latest")
        assert res.resolver == "auto_latest"

    def test_resolve_now_recorded(self):
        r = _resolver()
        c = _detect(r)
        res = r.resolve(c.conflict_id, "a", "Hello", now=77.0)
        assert res.resolved_at == 77.0

    def test_resolve_now_none_defaults_to_zero(self):
        r = _resolver()
        c = _detect(r)
        res = r.resolve(c.conflict_id, "a", "Hello", now=None)
        assert res.resolved_at == 0.0


# ---------- TestIgnoreConflict ----------

class TestIgnoreConflict:
    def test_sets_status_ignored(self):
        r = _resolver()
        c = _detect(r)
        r.ignore_conflict(c.conflict_id)
        assert r.get_conflict(c.conflict_id).status == "ignored"

    def test_returns_true_when_found(self):
        r = _resolver()
        c = _detect(r)
        assert r.ignore_conflict(c.conflict_id) is True

    def test_returns_false_when_not_found(self):
        r = _resolver()
        assert r.ignore_conflict("nope") is False

    def test_ignored_not_in_open_conflicts(self):
        r = _resolver()
        c = _detect(r)
        r.ignore_conflict(c.conflict_id)
        assert r.open_conflicts() == []


# ---------- TestGetConflict ----------

class TestGetConflict:
    def test_found(self):
        r = _resolver()
        c = _detect(r)
        assert r.get_conflict(c.conflict_id) is c

    def test_not_found(self):
        r = _resolver()
        assert r.get_conflict("missing") is None

    def test_returns_correct_conflict(self):
        r = _resolver()
        c1 = _detect(r, field="title", value_a="A", value_b="B")
        c2 = _detect(r, field="content", value_a="X", value_b="Y")
        assert r.get_conflict(c1.conflict_id).field == "title"
        assert r.get_conflict(c2.conflict_id).field == "content"


# ---------- TestGetResolution ----------

class TestGetResolution:
    def test_found(self):
        r = _resolver()
        c = _detect(r)
        res = r.resolve(c.conflict_id, "a", "Hello")
        assert r.get_resolution(c.conflict_id) is res

    def test_not_found(self):
        r = _resolver()
        assert r.get_resolution("missing") is None

    def test_none_before_resolve(self):
        r = _resolver()
        c = _detect(r)
        assert r.get_resolution(c.conflict_id) is None


# ---------- TestConflictsForDoc ----------

class TestConflictsForDoc:
    def test_empty(self):
        r = _resolver()
        assert r.conflicts_for_doc("doc-1") == []

    def test_single(self):
        r = _resolver()
        c = _detect(r, doc_id="doc-1")
        result = r.conflicts_for_doc("doc-1")
        assert len(result) == 1
        assert result[0] is c

    def test_multiple_sorted_by_detected_at(self):
        r = _resolver()
        c1 = _detect(r, doc_id="doc-1", value_a="A", value_b="B", now=10.0)
        c2 = _detect(r, doc_id="doc-1", value_a="C", value_b="D", now=5.0)
        c3 = _detect(r, doc_id="doc-1", value_a="E", value_b="F", now=20.0)
        result = r.conflicts_for_doc("doc-1")
        assert result == [c2, c1, c3]

    def test_excludes_other_docs(self):
        r = _resolver()
        _detect(r, doc_id="doc-1")
        c2 = _detect(r, doc_id="doc-2", value_a="X", value_b="Y")
        result = r.conflicts_for_doc("doc-2")
        assert len(result) == 1
        assert result[0] is c2

    def test_doc_not_present(self):
        r = _resolver()
        _detect(r, doc_id="doc-1")
        assert r.conflicts_for_doc("doc-99") == []


# ---------- TestOpenConflicts ----------

class TestOpenConflicts:
    def test_only_open(self):
        r = _resolver()
        c1 = _detect(r, value_a="A", value_b="B")
        c2 = _detect(r, value_a="C", value_b="D")
        r.resolve(c2.conflict_id, "b", "D")
        open_ids = {c.conflict_id for c in r.open_conflicts()}
        assert c1.conflict_id in open_ids
        assert c2.conflict_id not in open_ids

    def test_sorted_by_detected_at(self):
        r = _resolver()
        c1 = _detect(r, value_a="A", value_b="B", now=10.0)
        c2 = _detect(r, value_a="C", value_b="D", now=3.0)
        c3 = _detect(r, value_a="E", value_b="F", now=7.0)
        result = r.open_conflicts()
        assert result == [c2, c3, c1]

    def test_changes_after_resolve(self):
        r = _resolver()
        c = _detect(r)
        assert len(r.open_conflicts()) == 1
        r.resolve(c.conflict_id, "a", "Hello")
        assert r.open_conflicts() == []

    def test_ignored_not_in_open(self):
        r = _resolver()
        c = _detect(r)
        r.ignore_conflict(c.conflict_id)
        assert r.open_conflicts() == []

    def test_empty_initially(self):
        r = _resolver()
        assert r.open_conflicts() == []


# ---------- TestAllConflicts ----------

class TestAllConflicts:
    def test_sorted_by_detected_at(self):
        r = _resolver()
        c1 = _detect(r, value_a="A", value_b="B", now=20.0)
        c2 = _detect(r, value_a="C", value_b="D", now=5.0)
        c3 = _detect(r, value_a="E", value_b="F", now=10.0)
        result = r.all_conflicts()
        assert result == [c2, c3, c1]

    def test_includes_all_statuses(self):
        r = _resolver()
        c1 = _detect(r, value_a="A", value_b="B")
        c2 = _detect(r, value_a="C", value_b="D")
        c3 = _detect(r, value_a="E", value_b="F")
        r.resolve(c2.conflict_id, "a", "C")
        r.ignore_conflict(c3.conflict_id)
        ids = {c.conflict_id for c in r.all_conflicts()}
        assert ids == {c1.conflict_id, c2.conflict_id, c3.conflict_id}

    def test_empty(self):
        r = _resolver()
        assert r.all_conflicts() == []


# ---------- TestAutoResolveLatest ----------

class TestAutoResolveLatest:
    def test_uses_value_b(self):
        r = _resolver()
        c = _detect(r, value_a="old", value_b="new")
        res = r.auto_resolve_latest(c.conflict_id)
        assert res is not None
        assert res.resolved_value == "new"

    def test_chosen_version_b(self):
        r = _resolver()
        c = _detect(r)
        res = r.auto_resolve_latest(c.conflict_id)
        assert res.chosen_version == "b"

    def test_resolver_auto_latest(self):
        r = _resolver()
        c = _detect(r)
        res = r.auto_resolve_latest(c.conflict_id)
        assert res.resolver == "auto_latest"

    def test_conflict_marked_resolved(self):
        r = _resolver()
        c = _detect(r)
        r.auto_resolve_latest(c.conflict_id)
        assert r.get_conflict(c.conflict_id).status == "resolved"

    def test_not_found_returns_none(self):
        r = _resolver()
        assert r.auto_resolve_latest("nope") is None

    def test_now_recorded(self):
        r = _resolver()
        c = _detect(r)
        res = r.auto_resolve_latest(c.conflict_id, now=55.0)
        assert res.resolved_at == 55.0


# ---------- TestAutoResolveMerge ----------

class TestAutoResolveMerge:
    def test_default_separator(self):
        r = _resolver()
        c = _detect(r, value_a="foo", value_b="bar")
        res = r.auto_resolve_merge(c.conflict_id)
        assert res is not None
        assert res.resolved_value == "foo | bar"

    def test_custom_separator(self):
        r = _resolver()
        c = _detect(r, value_a="foo", value_b="bar")
        res = r.auto_resolve_merge(c.conflict_id, separator=" <> ")
        assert res.resolved_value == "foo <> bar"

    def test_chosen_version_merged(self):
        r = _resolver()
        c = _detect(r)
        res = r.auto_resolve_merge(c.conflict_id)
        assert res.chosen_version == "merged"

    def test_resolver_auto_merge(self):
        r = _resolver()
        c = _detect(r)
        res = r.auto_resolve_merge(c.conflict_id)
        assert res.resolver == "auto_merge"

    def test_conflict_marked_resolved(self):
        r = _resolver()
        c = _detect(r)
        r.auto_resolve_merge(c.conflict_id)
        assert r.get_conflict(c.conflict_id).status == "resolved"

    def test_not_found_returns_none(self):
        r = _resolver()
        assert r.auto_resolve_merge("nope") is None

    def test_now_recorded(self):
        r = _resolver()
        c = _detect(r)
        res = r.auto_resolve_merge(c.conflict_id, now=12.0)
        assert res.resolved_at == 12.0

    def test_empty_separator(self):
        r = _resolver()
        c = _detect(r, value_a="abc", value_b="xyz")
        res = r.auto_resolve_merge(c.conflict_id, separator="")
        assert res.resolved_value == "abcxyz"


# ---------- TestStats ----------

class TestStats:
    def test_empty_stats(self):
        r = _resolver()
        s = r.stats()
        assert s.total_conflicts == 0
        assert s.open_conflicts == 0
        assert s.resolved_conflicts == 0
        assert s.ignored_conflicts == 0

    def test_counts_open(self):
        r = _resolver()
        _detect(r, value_a="A", value_b="B")
        _detect(r, value_a="C", value_b="D")
        s = r.stats()
        assert s.total_conflicts == 2
        assert s.open_conflicts == 2
        assert s.resolved_conflicts == 0
        assert s.ignored_conflicts == 0

    def test_counts_resolved(self):
        r = _resolver()
        c = _detect(r)
        r.resolve(c.conflict_id, "a", "val")
        s = r.stats()
        assert s.total_conflicts == 1
        assert s.open_conflicts == 0
        assert s.resolved_conflicts == 1
        assert s.ignored_conflicts == 0

    def test_counts_ignored(self):
        r = _resolver()
        c = _detect(r)
        r.ignore_conflict(c.conflict_id)
        s = r.stats()
        assert s.total_conflicts == 1
        assert s.open_conflicts == 0
        assert s.ignored_conflicts == 1

    def test_mixed_statuses(self):
        r = _resolver()
        c1 = _detect(r, value_a="A", value_b="B")
        c2 = _detect(r, value_a="C", value_b="D")
        c3 = _detect(r, value_a="E", value_b="F")
        c4 = _detect(r, value_a="G", value_b="H")
        r.resolve(c1.conflict_id, "a", "A")
        r.resolve(c2.conflict_id, "b", "D")
        r.ignore_conflict(c3.conflict_id)
        # c4 stays open
        s = r.stats()
        assert s.total_conflicts == 4
        assert s.open_conflicts == 1
        assert s.resolved_conflicts == 2
        assert s.ignored_conflicts == 1


# ---------- TestThreadSafety ----------

class TestThreadSafety:
    def test_concurrent_detect_conflict(self):
        r = _resolver()
        errors = []

        def worker(n: int) -> None:
            try:
                for i in range(n):
                    r.detect_conflict(
                        doc_id=f"doc-{i}",
                        version_a="v1",
                        version_b="v2",
                        field="title",
                        value_a=f"value-a-{i}",
                        value_b=f"value-b-{i}",
                    )
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=worker, args=(20,)) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
        assert len(r.all_conflicts()) == 100

    def test_concurrent_resolve(self):
        r = _resolver()
        conflicts = [_detect(r, value_a=f"a{i}", value_b=f"b{i}") for i in range(20)]
        errors = []

        def resolver_worker(conflict: Conflict) -> None:
            try:
                r.resolve(conflict.conflict_id, "b", conflict.value_b)
            except Exception as exc:
                errors.append(exc)

        threads = [
            threading.Thread(target=resolver_worker, args=(c,)) for c in conflicts
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
        assert r.stats().resolved_conflicts == 20
