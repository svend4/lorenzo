"""Tests for E421 DocAnchorIndex."""

from __future__ import annotations

import threading
import time

import pytest

from docstoolkit.doc_anchor_index import AnchorRef, AnchorStats, DocAnchorIndex


# ---------------------------------------------------------------- construction


def test_construct_empty() -> None:
    idx = DocAnchorIndex()
    assert idx.stats() == AnchorStats(
        total_anchors=0, unique_docs=0, unique_keywords=0
    )


def test_empty_all_doc_ids() -> None:
    idx = DocAnchorIndex()
    assert idx.all_doc_ids() == []


def test_empty_all_keywords() -> None:
    idx = DocAnchorIndex()
    assert idx.all_keywords() == []


def test_empty_find_by_keyword() -> None:
    idx = DocAnchorIndex()
    assert idx.find_by_keyword("missing") == []


def test_empty_anchors_for_doc() -> None:
    idx = DocAnchorIndex()
    assert idx.anchors_for_doc("doc1") == []


# -------------------------------------------------------------------- add_anchor


def test_add_anchor_returns_ref() -> None:
    idx = DocAnchorIndex()
    ref = idx.add_anchor("doc1", "section-1", ["alpha", "beta"], now=100.0)
    assert isinstance(ref, AnchorRef)
    assert ref.doc_id == "doc1"
    assert ref.anchor == "section-1"
    assert ref.keywords == ["alpha", "beta"]
    assert ref.added_at == 100.0


def test_add_anchor_increments_stats() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("doc1", "a", ["k1"], now=1.0)
    s = idx.stats()
    assert s.total_anchors == 1
    assert s.unique_docs == 1
    assert s.unique_keywords == 1


def test_add_anchor_no_keywords() -> None:
    idx = DocAnchorIndex()
    ref = idx.add_anchor("doc1", "a", now=1.0)
    assert ref.keywords == []
    assert idx.stats().unique_keywords == 0


def test_add_anchor_keywords_none() -> None:
    idx = DocAnchorIndex()
    ref = idx.add_anchor("doc1", "a", keywords=None, now=1.0)
    assert ref.keywords == []


def test_add_anchor_default_now_uses_time() -> None:
    idx = DocAnchorIndex()
    before = time.time()
    ref = idx.add_anchor("doc1", "a")
    after = time.time()
    assert before <= ref.added_at <= after


def test_add_anchor_lowercases_keywords() -> None:
    idx = DocAnchorIndex()
    ref = idx.add_anchor("doc1", "a", ["Alpha", "BETA", "GaMma"], now=1.0)
    assert ref.keywords == ["alpha", "beta", "gamma"]


def test_add_anchor_strips_keywords() -> None:
    idx = DocAnchorIndex()
    ref = idx.add_anchor("doc1", "a", ["  spaced  ", "trim "], now=1.0)
    assert ref.keywords == ["spaced", "trim"]


def test_add_anchor_dedupes_keywords() -> None:
    idx = DocAnchorIndex()
    ref = idx.add_anchor("doc1", "a", ["x", "X", "x", "y"], now=1.0)
    assert ref.keywords == ["x", "y"]


def test_add_anchor_skips_empty_keywords() -> None:
    idx = DocAnchorIndex()
    ref = idx.add_anchor("doc1", "a", ["", "  ", "real"], now=1.0)
    assert ref.keywords == ["real"]


def test_add_anchor_replace_overwrites_keywords() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("doc1", "a", ["old1", "old2"], now=1.0)
    idx.add_anchor("doc1", "a", ["new1"], now=2.0)
    ref = idx.get_anchor("doc1", "a")
    assert ref is not None
    assert ref.keywords == ["new1"]
    assert ref.added_at == 2.0


def test_add_anchor_replace_keeps_unique_anchor_count() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("doc1", "a", ["k"], now=1.0)
    idx.add_anchor("doc1", "a", ["k2"], now=2.0)
    assert idx.stats().total_anchors == 1


def test_add_anchor_replace_unindexes_old_keywords() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("doc1", "a", ["old"], now=1.0)
    idx.add_anchor("doc1", "a", ["new"], now=2.0)
    assert idx.find_by_keyword("old") == []
    assert len(idx.find_by_keyword("new")) == 1


def test_add_anchor_multiple_docs() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("doc1", "a", ["k"], now=1.0)
    idx.add_anchor("doc2", "a", ["k"], now=1.0)
    s = idx.stats()
    assert s.total_anchors == 2
    assert s.unique_docs == 2
    assert s.unique_keywords == 1


def test_add_anchor_multiple_anchors_one_doc() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("doc1", "a", ["k1"], now=1.0)
    idx.add_anchor("doc1", "b", ["k2"], now=1.0)
    s = idx.stats()
    assert s.total_anchors == 2
    assert s.unique_docs == 1
    assert s.unique_keywords == 2


# --------------------------------------------------------------------- get_anchor


def test_get_anchor_existing() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("doc1", "a", ["k1"], now=10.0)
    ref = idx.get_anchor("doc1", "a")
    assert ref is not None
    assert ref.keywords == ["k1"]
    assert ref.added_at == 10.0


def test_get_anchor_missing() -> None:
    idx = DocAnchorIndex()
    assert idx.get_anchor("doc1", "a") is None


def test_get_anchor_returns_copy() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("doc1", "a", ["k1"], now=1.0)
    ref1 = idx.get_anchor("doc1", "a")
    assert ref1 is not None
    ref1.keywords.append("mutated")
    ref2 = idx.get_anchor("doc1", "a")
    assert ref2 is not None
    assert ref2.keywords == ["k1"]


# ----------------------------------------------------------------- remove_anchor


def test_remove_anchor_existing() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("doc1", "a", ["k"], now=1.0)
    assert idx.remove_anchor("doc1", "a") is True
    assert idx.get_anchor("doc1", "a") is None


def test_remove_anchor_missing() -> None:
    idx = DocAnchorIndex()
    assert idx.remove_anchor("doc1", "a") is False


def test_remove_anchor_unindexes_keywords() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("doc1", "a", ["k1", "k2"], now=1.0)
    idx.remove_anchor("doc1", "a")
    assert idx.all_keywords() == []


def test_remove_anchor_updates_doc_set() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("doc1", "a", ["k"], now=1.0)
    idx.add_anchor("doc1", "b", ["k"], now=1.0)
    idx.remove_anchor("doc1", "a")
    assert [r.anchor for r in idx.anchors_for_doc("doc1")] == ["b"]


def test_remove_last_anchor_drops_doc() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("doc1", "a", ["k"], now=1.0)
    idx.remove_anchor("doc1", "a")
    assert idx.all_doc_ids() == []


def test_remove_anchor_shared_keyword_keeps_others() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("doc1", "a", ["shared"], now=1.0)
    idx.add_anchor("doc2", "b", ["shared"], now=1.0)
    idx.remove_anchor("doc1", "a")
    refs = idx.find_by_keyword("shared")
    assert len(refs) == 1
    assert refs[0].doc_id == "doc2"


# -------------------------------------------------------------- find_by_keyword


def test_find_by_keyword_basic() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("doc1", "a", ["python"], now=1.0)
    idx.add_anchor("doc2", "b", ["python"], now=1.0)
    refs = idx.find_by_keyword("python")
    assert [(r.doc_id, r.anchor) for r in refs] == [("doc1", "a"), ("doc2", "b")]


def test_find_by_keyword_case_insensitive() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("doc1", "a", ["Python"], now=1.0)
    assert len(idx.find_by_keyword("PYTHON")) == 1
    assert len(idx.find_by_keyword("python")) == 1
    assert len(idx.find_by_keyword("PyThOn")) == 1


def test_find_by_keyword_sorted_order() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("docZ", "z", ["k"], now=1.0)
    idx.add_anchor("docA", "a", ["k"], now=1.0)
    idx.add_anchor("docA", "z", ["k"], now=1.0)
    refs = idx.find_by_keyword("k")
    pairs = [(r.doc_id, r.anchor) for r in refs]
    assert pairs == [("docA", "a"), ("docA", "z"), ("docZ", "z")]


def test_find_by_keyword_missing() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("doc1", "a", ["x"], now=1.0)
    assert idx.find_by_keyword("y") == []


def test_find_by_keyword_empty_string() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("doc1", "a", ["x"], now=1.0)
    assert idx.find_by_keyword("") == []


def test_find_by_keyword_whitespace() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("doc1", "a", ["x"], now=1.0)
    assert idx.find_by_keyword("   ") == []


def test_find_by_keyword_returns_copies() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("doc1", "a", ["k"], now=1.0)
    refs = idx.find_by_keyword("k")
    refs[0].keywords.append("hack")
    fresh = idx.find_by_keyword("k")
    assert fresh[0].keywords == ["k"]


# ------------------------------------------------------------- find_by_keywords


def test_find_by_keywords_or() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("doc1", "a", ["x"], now=1.0)
    idx.add_anchor("doc2", "b", ["y"], now=1.0)
    refs = idx.find_by_keywords(["x", "y"])
    assert len(refs) == 2


def test_find_by_keywords_and() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("doc1", "a", ["x", "y"], now=1.0)
    idx.add_anchor("doc2", "b", ["x"], now=1.0)
    refs = idx.find_by_keywords(["x", "y"], all_match=True)
    assert len(refs) == 1
    assert refs[0].doc_id == "doc1"


def test_find_by_keywords_and_missing_kw_returns_empty() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("doc1", "a", ["x"], now=1.0)
    refs = idx.find_by_keywords(["x", "absent"], all_match=True)
    assert refs == []


def test_find_by_keywords_or_skips_missing() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("doc1", "a", ["x"], now=1.0)
    refs = idx.find_by_keywords(["x", "absent"], all_match=False)
    assert len(refs) == 1


def test_find_by_keywords_empty_list() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("doc1", "a", ["x"], now=1.0)
    assert idx.find_by_keywords([]) == []


def test_find_by_keywords_case_insensitive() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("doc1", "a", ["alpha", "beta"], now=1.0)
    refs = idx.find_by_keywords(["ALPHA", "BeTa"], all_match=True)
    assert len(refs) == 1


def test_find_by_keywords_sorted() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("docB", "b", ["k"], now=1.0)
    idx.add_anchor("docA", "a", ["k"], now=1.0)
    refs = idx.find_by_keywords(["k"])
    assert [r.doc_id for r in refs] == ["docA", "docB"]


# ------------------------------------------------------------- anchors_for_doc


def test_anchors_for_doc_sorted() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("doc1", "z", ["k"], now=1.0)
    idx.add_anchor("doc1", "a", ["k"], now=1.0)
    idx.add_anchor("doc1", "m", ["k"], now=1.0)
    anchors = [r.anchor for r in idx.anchors_for_doc("doc1")]
    assert anchors == ["a", "m", "z"]


def test_anchors_for_doc_missing() -> None:
    idx = DocAnchorIndex()
    assert idx.anchors_for_doc("nope") == []


def test_anchors_for_doc_returns_copies() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("doc1", "a", ["k"], now=1.0)
    refs = idx.anchors_for_doc("doc1")
    refs[0].keywords.append("mutated")
    fresh = idx.anchors_for_doc("doc1")
    assert fresh[0].keywords == ["k"]


# ------------------------------------------------------------------ keywords_of


def test_keywords_of_returns_sorted() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("doc1", "a", ["zeta", "alpha", "gamma"], now=1.0)
    assert idx.keywords_of("doc1", "a") == ["alpha", "gamma", "zeta"]


def test_keywords_of_missing() -> None:
    idx = DocAnchorIndex()
    assert idx.keywords_of("doc1", "a") == []


def test_keywords_of_empty() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("doc1", "a", [], now=1.0)
    assert idx.keywords_of("doc1", "a") == []


# -------------------------------------------------------------- update_keywords


def test_update_keywords_existing() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("doc1", "a", ["old"], now=1.0)
    assert idx.update_keywords("doc1", "a", ["new1", "new2"]) is True
    assert idx.keywords_of("doc1", "a") == ["new1", "new2"]


def test_update_keywords_missing() -> None:
    idx = DocAnchorIndex()
    assert idx.update_keywords("doc1", "a", ["k"]) is False


def test_update_keywords_unindexes_old() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("doc1", "a", ["old"], now=1.0)
    idx.update_keywords("doc1", "a", ["new"])
    assert idx.find_by_keyword("old") == []
    assert len(idx.find_by_keyword("new")) == 1


def test_update_keywords_normalizes() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("doc1", "a", ["x"], now=1.0)
    idx.update_keywords("doc1", "a", ["NEW", "  Trim ", "new"])
    assert idx.keywords_of("doc1", "a") == ["new", "trim"]


def test_update_keywords_to_empty() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("doc1", "a", ["x", "y"], now=1.0)
    assert idx.update_keywords("doc1", "a", []) is True
    assert idx.keywords_of("doc1", "a") == []
    assert idx.all_keywords() == []


# ----------------------------------------------------------------- clear_doc


def test_clear_doc_returns_count() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("doc1", "a", ["k"], now=1.0)
    idx.add_anchor("doc1", "b", ["k"], now=1.0)
    idx.add_anchor("doc1", "c", ["k"], now=1.0)
    assert idx.clear_doc("doc1") == 3


def test_clear_doc_missing() -> None:
    idx = DocAnchorIndex()
    assert idx.clear_doc("nope") == 0


def test_clear_doc_drops_doc() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("doc1", "a", ["k"], now=1.0)
    idx.clear_doc("doc1")
    assert idx.all_doc_ids() == []


def test_clear_doc_keeps_other_docs() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("doc1", "a", ["shared"], now=1.0)
    idx.add_anchor("doc2", "a", ["shared"], now=1.0)
    idx.clear_doc("doc1")
    assert idx.all_doc_ids() == ["doc2"]
    assert idx.find_by_keyword("shared") != []


def test_clear_doc_unindexes_keywords() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("doc1", "a", ["only"], now=1.0)
    idx.clear_doc("doc1")
    assert idx.all_keywords() == []


# ---------------------------------------------------------------- clear_keyword


def test_clear_keyword_returns_count() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("doc1", "a", ["x", "shared"], now=1.0)
    idx.add_anchor("doc2", "b", ["shared"], now=1.0)
    assert idx.clear_keyword("shared") == 2


def test_clear_keyword_missing() -> None:
    idx = DocAnchorIndex()
    assert idx.clear_keyword("nope") == 0


def test_clear_keyword_removes_from_anchors() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("doc1", "a", ["x", "y"], now=1.0)
    idx.clear_keyword("x")
    assert idx.keywords_of("doc1", "a") == ["y"]


def test_clear_keyword_case_insensitive() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("doc1", "a", ["alpha"], now=1.0)
    idx.clear_keyword("ALPHA")
    assert idx.keywords_of("doc1", "a") == []


def test_clear_keyword_empty_returns_zero() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("doc1", "a", ["k"], now=1.0)
    assert idx.clear_keyword("") == 0
    assert idx.clear_keyword("   ") == 0


def test_clear_keyword_keeps_anchor_existent() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("doc1", "a", ["only"], now=1.0)
    idx.clear_keyword("only")
    assert idx.get_anchor("doc1", "a") is not None
    assert idx.keywords_of("doc1", "a") == []


# ------------------------------------------------------------------- all_doc_ids


def test_all_doc_ids_sorted() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("docB", "a", ["k"], now=1.0)
    idx.add_anchor("docA", "a", ["k"], now=1.0)
    idx.add_anchor("docC", "a", ["k"], now=1.0)
    assert idx.all_doc_ids() == ["docA", "docB", "docC"]


def test_all_keywords_sorted() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("doc1", "a", ["zebra", "apple", "mango"], now=1.0)
    assert idx.all_keywords() == ["apple", "mango", "zebra"]


# ----------------------------------------------------------------------- stats


def test_stats_after_mixed_ops() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("doc1", "a", ["k1", "k2"], now=1.0)
    idx.add_anchor("doc1", "b", ["k2"], now=1.0)
    idx.add_anchor("doc2", "a", ["k3"], now=1.0)
    s = idx.stats()
    assert s.total_anchors == 3
    assert s.unique_docs == 2
    assert s.unique_keywords == 3


def test_stats_after_removal() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("doc1", "a", ["k1"], now=1.0)
    idx.add_anchor("doc2", "b", ["k2"], now=1.0)
    idx.remove_anchor("doc1", "a")
    s = idx.stats()
    assert s.total_anchors == 1
    assert s.unique_docs == 1
    assert s.unique_keywords == 1


# ------------------------------------------------------------------ thread safety


def test_concurrent_adds() -> None:
    idx = DocAnchorIndex()

    def worker(start: int) -> None:
        for i in range(start, start + 100):
            idx.add_anchor(f"doc{i}", "anchor", [f"kw{i}"], now=float(i))

    threads = [threading.Thread(target=worker, args=(i * 100,)) for i in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    s = idx.stats()
    assert s.total_anchors == 500
    assert s.unique_docs == 500
    assert s.unique_keywords == 500


def test_concurrent_add_remove() -> None:
    idx = DocAnchorIndex()
    for i in range(200):
        idx.add_anchor(f"doc{i}", "a", ["k"], now=1.0)

    def remover(start: int) -> None:
        for i in range(start, start + 50):
            idx.remove_anchor(f"doc{i}", "a")

    threads = [threading.Thread(target=remover, args=(i * 50,)) for i in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert idx.stats().total_anchors == 0


def test_concurrent_reads_and_writes() -> None:
    idx = DocAnchorIndex()

    def writer() -> None:
        for i in range(100):
            idx.add_anchor(f"d{i}", "a", ["shared"], now=1.0)

    def reader() -> None:
        for _ in range(100):
            idx.find_by_keyword("shared")
            idx.all_doc_ids()
            idx.stats()

    threads = [
        threading.Thread(target=writer),
        threading.Thread(target=reader),
        threading.Thread(target=reader),
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert idx.stats().total_anchors == 100


def test_concurrent_keyword_updates() -> None:
    idx = DocAnchorIndex()
    for i in range(50):
        idx.add_anchor(f"d{i}", "a", ["orig"], now=1.0)

    def updater(start: int) -> None:
        for i in range(start, start + 10):
            idx.update_keywords(f"d{i}", "a", [f"upd{i}"])

    threads = [threading.Thread(target=updater, args=(i * 10,)) for i in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert idx.find_by_keyword("orig") == []
    for i in range(50):
        assert idx.keywords_of(f"d{i}", "a") == [f"upd{i}"]


# ------------------------------------------------------------------ edge cases


def test_anchor_with_special_chars() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("doc/1", "sec#1.2", ["k"], now=1.0)
    assert idx.get_anchor("doc/1", "sec#1.2") is not None


def test_same_anchor_different_docs() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("doc1", "intro", ["k"], now=1.0)
    idx.add_anchor("doc2", "intro", ["k"], now=2.0)
    assert idx.stats().total_anchors == 2
    assert {r.doc_id for r in idx.find_by_keyword("k")} == {"doc1", "doc2"}


def test_keywords_field_default_factory_independent() -> None:
    ref1 = AnchorRef(doc_id="a", anchor="x")
    ref2 = AnchorRef(doc_id="b", anchor="y")
    ref1.keywords.append("k")
    assert ref2.keywords == []


def test_non_string_keywords_skipped() -> None:
    idx = DocAnchorIndex()
    # Mixed list with a non-string slipped in
    ref = idx.add_anchor("doc1", "a", ["ok", 123, None, "fine"], now=1.0)  # type: ignore[list-item]
    assert ref.keywords == ["ok", "fine"]


def test_unicode_keywords() -> None:
    idx = DocAnchorIndex()
    idx.add_anchor("doc1", "a", ["агент", "память"], now=1.0)
    assert idx.find_by_keyword("Агент")
    assert idx.keywords_of("doc1", "a") == ["агент", "память"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
