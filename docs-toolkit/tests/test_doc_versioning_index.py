"""Tests for E427 DocVersioningIndex."""
from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_versioning_index import (
    DocVersioningIndex,
    VersionRef,
    VersioningStats,
)


# ---------------------------------------------------------------------------
# Construction & basic add/get
# ---------------------------------------------------------------------------
def test_empty_index_has_no_docs():
    idx = DocVersioningIndex()
    assert idx.all_doc_ids() == []


def test_empty_index_has_no_tags():
    idx = DocVersioningIndex()
    assert idx.all_tags() == []


def test_empty_stats():
    idx = DocVersioningIndex()
    s = idx.stats()
    assert isinstance(s, VersioningStats)
    assert s.total_versions == 0
    assert s.unique_docs == 0
    assert s.unique_tags == 0


def test_add_version_returns_versionref():
    idx = DocVersioningIndex()
    ref = idx.add_version("doc1", "v1", tag="stable", now=10.0)
    assert isinstance(ref, VersionRef)
    assert ref.doc_id == "doc1"
    assert ref.version == "v1"
    assert ref.tag == "stable"
    assert ref.created_at == 10.0
    assert ref.parent_version is None


def test_add_version_default_tag_empty():
    idx = DocVersioningIndex()
    ref = idx.add_version("doc1", "v1", now=1.0)
    assert ref.tag == ""


def test_add_version_default_now_uses_time():
    idx = DocVersioningIndex()
    ref = idx.add_version("doc1", "v1")
    assert ref.created_at > 0


def test_add_version_with_parent():
    idx = DocVersioningIndex()
    ref = idx.add_version("doc1", "v2", parent_version="v1", now=2.0)
    assert ref.parent_version == "v1"


def test_get_version_existing():
    idx = DocVersioningIndex()
    idx.add_version("d", "v1", now=1.0)
    ref = idx.get_version("d", "v1")
    assert ref is not None
    assert ref.version == "v1"


def test_get_version_missing_doc():
    idx = DocVersioningIndex()
    assert idx.get_version("nope", "v1") is None


def test_get_version_missing_version():
    idx = DocVersioningIndex()
    idx.add_version("d", "v1", now=1.0)
    assert idx.get_version("d", "v2") is None


def test_add_overwrites_existing():
    idx = DocVersioningIndex()
    idx.add_version("d", "v1", tag="draft", now=1.0)
    idx.add_version("d", "v1", tag="stable", now=5.0)
    ref = idx.get_version("d", "v1")
    assert ref.tag == "stable"
    assert ref.created_at == 5.0


def test_add_overwrites_removes_old_tag_membership():
    idx = DocVersioningIndex()
    idx.add_version("d", "v1", tag="draft", now=1.0)
    idx.add_version("d", "v1", tag="stable", now=2.0)
    assert idx.versions_with_tag("draft") == []
    assert len(idx.versions_with_tag("stable")) == 1


# ---------------------------------------------------------------------------
# remove_version
# ---------------------------------------------------------------------------
def test_remove_version_existing_returns_true():
    idx = DocVersioningIndex()
    idx.add_version("d", "v1", now=1.0)
    assert idx.remove_version("d", "v1") is True


def test_remove_version_missing_returns_false():
    idx = DocVersioningIndex()
    assert idx.remove_version("d", "v1") is False


def test_remove_version_clears_lookup():
    idx = DocVersioningIndex()
    idx.add_version("d", "v1", now=1.0)
    idx.remove_version("d", "v1")
    assert idx.get_version("d", "v1") is None


def test_remove_version_clears_by_doc_when_empty():
    idx = DocVersioningIndex()
    idx.add_version("d", "v1", now=1.0)
    idx.remove_version("d", "v1")
    assert idx.all_doc_ids() == []


def test_remove_version_keeps_doc_with_other_versions():
    idx = DocVersioningIndex()
    idx.add_version("d", "v1", now=1.0)
    idx.add_version("d", "v2", now=2.0)
    idx.remove_version("d", "v1")
    assert idx.all_doc_ids() == ["d"]
    assert idx.get_version("d", "v2") is not None


def test_remove_version_clears_tag_index():
    idx = DocVersioningIndex()
    idx.add_version("d", "v1", tag="stable", now=1.0)
    idx.remove_version("d", "v1")
    assert idx.versions_with_tag("stable") == []
    assert idx.all_tags() == []


# ---------------------------------------------------------------------------
# set_tag
# ---------------------------------------------------------------------------
def test_set_tag_existing_returns_true():
    idx = DocVersioningIndex()
    idx.add_version("d", "v1", now=1.0)
    assert idx.set_tag("d", "v1", "stable") is True


def test_set_tag_missing_returns_false():
    idx = DocVersioningIndex()
    assert idx.set_tag("d", "v1", "stable") is False


def test_set_tag_updates_ref():
    idx = DocVersioningIndex()
    idx.add_version("d", "v1", now=1.0)
    idx.set_tag("d", "v1", "stable")
    assert idx.get_version("d", "v1").tag == "stable"


def test_set_tag_replaces_old_tag():
    idx = DocVersioningIndex()
    idx.add_version("d", "v1", tag="draft", now=1.0)
    idx.set_tag("d", "v1", "stable")
    assert idx.versions_with_tag("draft") == []
    assert len(idx.versions_with_tag("stable")) == 1


def test_set_tag_to_empty_string_clears_tag():
    idx = DocVersioningIndex()
    idx.add_version("d", "v1", tag="stable", now=1.0)
    idx.set_tag("d", "v1", "")
    assert idx.get_version("d", "v1").tag == ""
    assert idx.all_tags() == []


def test_set_tag_to_same_tag_idempotent():
    idx = DocVersioningIndex()
    idx.add_version("d", "v1", tag="stable", now=1.0)
    idx.set_tag("d", "v1", "stable")
    assert len(idx.versions_with_tag("stable")) == 1


# ---------------------------------------------------------------------------
# versions_for_doc
# ---------------------------------------------------------------------------
def test_versions_for_doc_empty():
    idx = DocVersioningIndex()
    assert idx.versions_for_doc("nope") == []


def test_versions_for_doc_sorted_by_created_at():
    idx = DocVersioningIndex()
    idx.add_version("d", "v3", now=3.0)
    idx.add_version("d", "v1", now=1.0)
    idx.add_version("d", "v2", now=2.0)
    refs = idx.versions_for_doc("d")
    assert [r.version for r in refs] == ["v1", "v2", "v3"]


def test_versions_for_doc_isolates_docs():
    idx = DocVersioningIndex()
    idx.add_version("a", "v1", now=1.0)
    idx.add_version("b", "v1", now=2.0)
    refs = idx.versions_for_doc("a")
    assert len(refs) == 1
    assert refs[0].doc_id == "a"


# ---------------------------------------------------------------------------
# latest_version
# ---------------------------------------------------------------------------
def test_latest_version_empty():
    idx = DocVersioningIndex()
    assert idx.latest_version("d") is None


def test_latest_version_single():
    idx = DocVersioningIndex()
    idx.add_version("d", "v1", now=1.0)
    ref = idx.latest_version("d")
    assert ref.version == "v1"


def test_latest_version_picks_highest_created_at():
    idx = DocVersioningIndex()
    idx.add_version("d", "v1", now=5.0)
    idx.add_version("d", "v2", now=2.0)
    idx.add_version("d", "v3", now=10.0)
    assert idx.latest_version("d").version == "v3"


# ---------------------------------------------------------------------------
# version_chain
# ---------------------------------------------------------------------------
def test_version_chain_missing_version():
    idx = DocVersioningIndex()
    assert idx.version_chain("d", "v1") == []


def test_version_chain_no_parent_returns_single():
    idx = DocVersioningIndex()
    idx.add_version("d", "v1", now=1.0)
    chain = idx.version_chain("d", "v1")
    assert [r.version for r in chain] == ["v1"]


def test_version_chain_linear():
    idx = DocVersioningIndex()
    idx.add_version("d", "v1", now=1.0)
    idx.add_version("d", "v2", parent_version="v1", now=2.0)
    idx.add_version("d", "v3", parent_version="v2", now=3.0)
    chain = idx.version_chain("d", "v3")
    assert [r.version for r in chain] == ["v3", "v2", "v1"]


def test_version_chain_stops_on_missing_parent():
    idx = DocVersioningIndex()
    idx.add_version("d", "v2", parent_version="ghost", now=2.0)
    chain = idx.version_chain("d", "v2")
    assert [r.version for r in chain] == ["v2"]


def test_version_chain_handles_cycle():
    idx = DocVersioningIndex()
    idx.add_version("d", "v1", parent_version="v2", now=1.0)
    idx.add_version("d", "v2", parent_version="v1", now=2.0)
    chain = idx.version_chain("d", "v1")
    versions = [r.version for r in chain]
    assert versions == ["v1", "v2"]


def test_version_chain_self_cycle():
    idx = DocVersioningIndex()
    idx.add_version("d", "v1", parent_version="v1", now=1.0)
    chain = idx.version_chain("d", "v1")
    assert [r.version for r in chain] == ["v1"]


# ---------------------------------------------------------------------------
# versions_with_tag / tags_of_doc / child_versions
# ---------------------------------------------------------------------------
def test_versions_with_tag_empty():
    idx = DocVersioningIndex()
    assert idx.versions_with_tag("none") == []


def test_versions_with_tag_returns_all():
    idx = DocVersioningIndex()
    idx.add_version("a", "v1", tag="stable", now=1.0)
    idx.add_version("b", "v2", tag="stable", now=2.0)
    idx.add_version("a", "v2", tag="draft", now=3.0)
    refs = idx.versions_with_tag("stable")
    assert {(r.doc_id, r.version) for r in refs} == {("a", "v1"), ("b", "v2")}


def test_versions_with_tag_sorted():
    idx = DocVersioningIndex()
    idx.add_version("b", "v2", tag="t", now=1.0)
    idx.add_version("a", "v3", tag="t", now=2.0)
    idx.add_version("a", "v1", tag="t", now=3.0)
    refs = idx.versions_with_tag("t")
    assert [(r.doc_id, r.version) for r in refs] == [
        ("a", "v1"),
        ("a", "v3"),
        ("b", "v2"),
    ]


def test_tags_of_doc_empty():
    idx = DocVersioningIndex()
    assert idx.tags_of_doc("d") == []


def test_tags_of_doc_omits_empty_tag():
    idx = DocVersioningIndex()
    idx.add_version("d", "v1", now=1.0)
    idx.add_version("d", "v2", tag="stable", now=2.0)
    assert idx.tags_of_doc("d") == ["stable"]


def test_tags_of_doc_unique_sorted():
    idx = DocVersioningIndex()
    idx.add_version("d", "v1", tag="zeta", now=1.0)
    idx.add_version("d", "v2", tag="alpha", now=2.0)
    idx.add_version("d", "v3", tag="alpha", now=3.0)
    assert idx.tags_of_doc("d") == ["alpha", "zeta"]


def test_child_versions_no_children():
    idx = DocVersioningIndex()
    idx.add_version("d", "v1", now=1.0)
    assert idx.child_versions("d", "v1") == []


def test_child_versions_missing_doc():
    idx = DocVersioningIndex()
    assert idx.child_versions("nope", "v1") == []


def test_child_versions_returns_only_direct_children():
    idx = DocVersioningIndex()
    idx.add_version("d", "v1", now=1.0)
    idx.add_version("d", "v2", parent_version="v1", now=2.0)
    idx.add_version("d", "v3", parent_version="v1", now=3.0)
    idx.add_version("d", "v4", parent_version="v2", now=4.0)
    refs = idx.child_versions("d", "v1")
    assert [r.version for r in refs] == ["v2", "v3"]


def test_child_versions_sorted_by_created_at():
    idx = DocVersioningIndex()
    idx.add_version("d", "v1", now=1.0)
    idx.add_version("d", "v3", parent_version="v1", now=5.0)
    idx.add_version("d", "v2", parent_version="v1", now=2.0)
    refs = idx.child_versions("d", "v1")
    assert [r.version for r in refs] == ["v2", "v3"]


# ---------------------------------------------------------------------------
# clear_doc
# ---------------------------------------------------------------------------
def test_clear_doc_missing_returns_zero():
    idx = DocVersioningIndex()
    assert idx.clear_doc("nope") == 0


def test_clear_doc_returns_count():
    idx = DocVersioningIndex()
    idx.add_version("d", "v1", now=1.0)
    idx.add_version("d", "v2", now=2.0)
    idx.add_version("d", "v3", now=3.0)
    assert idx.clear_doc("d") == 3


def test_clear_doc_removes_all_versions():
    idx = DocVersioningIndex()
    idx.add_version("d", "v1", now=1.0)
    idx.add_version("d", "v2", now=2.0)
    idx.clear_doc("d")
    assert idx.versions_for_doc("d") == []
    assert idx.all_doc_ids() == []


def test_clear_doc_clears_tag_index():
    idx = DocVersioningIndex()
    idx.add_version("d", "v1", tag="stable", now=1.0)
    idx.add_version("d", "v2", tag="draft", now=2.0)
    idx.clear_doc("d")
    assert idx.all_tags() == []


def test_clear_doc_keeps_other_docs():
    idx = DocVersioningIndex()
    idx.add_version("a", "v1", tag="stable", now=1.0)
    idx.add_version("b", "v1", tag="stable", now=2.0)
    idx.clear_doc("a")
    assert idx.all_doc_ids() == ["b"]
    assert len(idx.versions_with_tag("stable")) == 1


# ---------------------------------------------------------------------------
# all_doc_ids / all_tags / stats
# ---------------------------------------------------------------------------
def test_all_doc_ids_sorted():
    idx = DocVersioningIndex()
    idx.add_version("zeta", "v1", now=1.0)
    idx.add_version("alpha", "v1", now=2.0)
    idx.add_version("mu", "v1", now=3.0)
    assert idx.all_doc_ids() == ["alpha", "mu", "zeta"]


def test_all_tags_sorted_unique():
    idx = DocVersioningIndex()
    idx.add_version("a", "v1", tag="zeta", now=1.0)
    idx.add_version("b", "v1", tag="alpha", now=2.0)
    idx.add_version("c", "v1", tag="alpha", now=3.0)
    assert idx.all_tags() == ["alpha", "zeta"]


def test_stats_counts():
    idx = DocVersioningIndex()
    idx.add_version("a", "v1", tag="stable", now=1.0)
    idx.add_version("a", "v2", tag="draft", now=2.0)
    idx.add_version("b", "v1", tag="stable", now=3.0)
    s = idx.stats()
    assert s.total_versions == 3
    assert s.unique_docs == 2
    assert s.unique_tags == 2


def test_stats_ignores_empty_tag():
    idx = DocVersioningIndex()
    idx.add_version("a", "v1", now=1.0)
    idx.add_version("b", "v1", now=2.0)
    s = idx.stats()
    assert s.unique_tags == 0


# ---------------------------------------------------------------------------
# Dataclass shape
# ---------------------------------------------------------------------------
def test_versionref_defaults():
    ref = VersionRef(doc_id="d", version="v")
    assert ref.tag == ""
    assert ref.created_at == 0.0
    assert ref.parent_version is None


def test_versioningstats_fields():
    s = VersioningStats(total_versions=1, unique_docs=2, unique_tags=3)
    assert s.total_versions == 1
    assert s.unique_docs == 2
    assert s.unique_tags == 3


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------
def test_thread_safe_add():
    idx = DocVersioningIndex()

    def writer(doc_id: str) -> None:
        for i in range(50):
            idx.add_version(doc_id, f"v{i}", now=float(i))

    threads = [threading.Thread(target=writer, args=(f"d{n}",)) for n in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    s = idx.stats()
    assert s.total_versions == 8 * 50
    assert s.unique_docs == 8


def test_thread_safe_mixed_ops():
    idx = DocVersioningIndex()
    for i in range(100):
        idx.add_version("d", f"v{i}", tag="stable" if i % 2 == 0 else "draft", now=float(i))

    errors: list = []

    def reader() -> None:
        try:
            for _ in range(100):
                idx.versions_for_doc("d")
                idx.versions_with_tag("stable")
                idx.latest_version("d")
                idx.stats()
        except Exception as e:  # pragma: no cover - defensive
            errors.append(e)

    def writer() -> None:
        try:
            for i in range(100, 200):
                idx.add_version("d", f"v{i}", now=float(i))
        except Exception as e:  # pragma: no cover - defensive
            errors.append(e)

    threads = [threading.Thread(target=reader) for _ in range(4)] + [
        threading.Thread(target=writer) for _ in range(2)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert errors == []
    s = idx.stats()
    # 100 initial + 100 new (writers may overwrite each other's same keys)
    assert s.total_versions >= 100


def test_thread_safe_remove():
    idx = DocVersioningIndex()
    for i in range(200):
        idx.add_version("d", f"v{i}", now=float(i))

    def remover(start: int) -> None:
        for i in range(start, start + 100):
            idx.remove_version("d", f"v{i}")

    t1 = threading.Thread(target=remover, args=(0,))
    t2 = threading.Thread(target=remover, args=(100,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    assert idx.versions_for_doc("d") == []


# ---------------------------------------------------------------------------
# Misc edge cases
# ---------------------------------------------------------------------------
def test_two_docs_independent_versions():
    idx = DocVersioningIndex()
    idx.add_version("a", "v1", now=1.0)
    idx.add_version("b", "v1", now=2.0)
    assert idx.get_version("a", "v1").doc_id == "a"
    assert idx.get_version("b", "v1").doc_id == "b"


def test_same_version_string_in_different_docs():
    idx = DocVersioningIndex()
    idx.add_version("a", "v1", tag="stable", now=1.0)
    idx.add_version("b", "v1", tag="stable", now=2.0)
    refs = idx.versions_with_tag("stable")
    assert len(refs) == 2


def test_child_versions_after_parent_removed():
    idx = DocVersioningIndex()
    idx.add_version("d", "v1", now=1.0)
    idx.add_version("d", "v2", parent_version="v1", now=2.0)
    idx.remove_version("d", "v1")
    refs = idx.child_versions("d", "v1")
    assert [r.version for r in refs] == ["v2"]


def test_version_chain_after_parent_removed():
    idx = DocVersioningIndex()
    idx.add_version("d", "v1", now=1.0)
    idx.add_version("d", "v2", parent_version="v1", now=2.0)
    idx.remove_version("d", "v1")
    chain = idx.version_chain("d", "v2")
    assert [r.version for r in chain] == ["v2"]


def test_readd_after_remove():
    idx = DocVersioningIndex()
    idx.add_version("d", "v1", tag="stable", now=1.0)
    idx.remove_version("d", "v1")
    idx.add_version("d", "v1", tag="draft", now=5.0)
    ref = idx.get_version("d", "v1")
    assert ref.tag == "draft"
    assert ref.created_at == 5.0


def test_versions_for_doc_stable_with_equal_created_at():
    idx = DocVersioningIndex()
    idx.add_version("d", "v2", now=1.0)
    idx.add_version("d", "v1", now=1.0)
    refs = idx.versions_for_doc("d")
    # tie-break by version
    assert [r.version for r in refs] == ["v1", "v2"]


def test_set_tag_does_not_affect_others():
    idx = DocVersioningIndex()
    idx.add_version("d", "v1", tag="stable", now=1.0)
    idx.add_version("d", "v2", tag="stable", now=2.0)
    idx.set_tag("d", "v1", "draft")
    stable = idx.versions_with_tag("stable")
    assert [r.version for r in stable] == ["v2"]


def test_add_with_explicit_now_zero():
    idx = DocVersioningIndex()
    ref = idx.add_version("d", "v1", now=0.0)
    assert ref.created_at == 0.0


def test_large_chain():
    idx = DocVersioningIndex()
    for i in range(50):
        parent = f"v{i - 1}" if i > 0 else None
        idx.add_version("d", f"v{i}", parent_version=parent, now=float(i))
    chain = idx.version_chain("d", "v49")
    assert len(chain) == 50
    assert chain[0].version == "v49"
    assert chain[-1].version == "v0"
