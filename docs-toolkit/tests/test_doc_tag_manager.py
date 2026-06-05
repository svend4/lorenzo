"""Tests for E288 DocTagManager.

Run with:
    python -m pytest tests/test_doc_tag_manager.py -q
"""

from __future__ import annotations

import threading
import time

import pytest

from docstoolkit.doc_tag_manager import (
    DocTagManager,
    DocTags,
    TagInfo,
    TagManagerStats,
)


# ===========================================================================
# Fixtures
# ===========================================================================


@pytest.fixture
def mgr() -> DocTagManager:
    return DocTagManager()


# ===========================================================================
# add_tag
# ===========================================================================


class TestAddTag:
    def test_add_tag_returns_true_on_first_add(self, mgr):
        assert mgr.add_tag("doc1", "python") is True

    def test_add_tag_returns_false_on_duplicate(self, mgr):
        mgr.add_tag("doc1", "python")
        assert mgr.add_tag("doc1", "python") is False

    def test_add_tag_different_docs_both_true(self, mgr):
        assert mgr.add_tag("doc1", "python") is True
        assert mgr.add_tag("doc2", "python") is True

    def test_add_tag_multiple_tags_to_same_doc(self, mgr):
        mgr.add_tag("doc1", "python")
        mgr.add_tag("doc1", "testing")
        assert sorted(mgr.tags_for_doc("doc1")) == ["python", "testing"]

    def test_add_tag_resolves_alias(self, mgr):
        mgr.register_alias("js", "javascript")
        mgr.add_tag("doc1", "js")
        # canonical tag is stored
        assert mgr.has_tag("doc1", "javascript")
        # "js" alias is also resolved by has_tag (same result), but
        # the raw tag list must not contain the alias string "js"
        assert "js" not in mgr.tags_for_doc("doc1")

    def test_add_tag_alias_not_stored_as_own_tag(self, mgr):
        mgr.register_alias("py", "python")
        mgr.add_tag("doc1", "py")
        assert "py" not in mgr.tags_for_doc("doc1")


# ===========================================================================
# add_tags
# ===========================================================================


class TestAddTags:
    def test_add_tags_returns_count_of_new(self, mgr):
        assert mgr.add_tags("doc1", ["a", "b", "c"]) == 3

    def test_add_tags_returns_zero_when_all_present(self, mgr):
        mgr.add_tags("doc1", ["a", "b"])
        assert mgr.add_tags("doc1", ["a", "b"]) == 0

    def test_add_tags_partial_overlap(self, mgr):
        mgr.add_tags("doc1", ["a", "b"])
        count = mgr.add_tags("doc1", ["b", "c"])
        assert count == 1

    def test_add_tags_empty_list(self, mgr):
        assert mgr.add_tags("doc1", []) == 0

    def test_add_tags_resolves_aliases(self, mgr):
        mgr.register_alias("js", "javascript")
        mgr.register_alias("py", "python")
        count = mgr.add_tags("doc1", ["js", "py"])
        assert count == 2
        assert "javascript" in mgr.tags_for_doc("doc1")
        assert "python" in mgr.tags_for_doc("doc1")

    def test_add_tags_deduplication_within_call(self, mgr):
        # Both "js" and "javascript" resolve to "javascript"
        mgr.register_alias("js", "javascript")
        count = mgr.add_tags("doc1", ["js", "javascript"])
        assert count == 1


# ===========================================================================
# remove_tag
# ===========================================================================


class TestRemoveTag:
    def test_remove_tag_returns_true_when_present(self, mgr):
        mgr.add_tag("doc1", "python")
        assert mgr.remove_tag("doc1", "python") is True

    def test_remove_tag_returns_false_when_absent(self, mgr):
        assert mgr.remove_tag("doc1", "python") is False

    def test_remove_tag_actually_removes(self, mgr):
        mgr.add_tag("doc1", "python")
        mgr.remove_tag("doc1", "python")
        assert not mgr.has_tag("doc1", "python")

    def test_remove_tag_via_alias(self, mgr):
        mgr.register_alias("py", "python")
        mgr.add_tag("doc1", "python")
        assert mgr.remove_tag("doc1", "py") is True
        assert not mgr.has_tag("doc1", "python")

    def test_remove_tag_does_not_affect_other_docs(self, mgr):
        mgr.add_tag("doc1", "python")
        mgr.add_tag("doc2", "python")
        mgr.remove_tag("doc1", "python")
        assert mgr.has_tag("doc2", "python")


# ===========================================================================
# remove_all_tags
# ===========================================================================


class TestRemoveAllTags:
    def test_remove_all_returns_count(self, mgr):
        mgr.add_tags("doc1", ["a", "b", "c"])
        assert mgr.remove_all_tags("doc1") == 3

    def test_remove_all_empty_doc_returns_zero(self, mgr):
        assert mgr.remove_all_tags("nonexistent") == 0

    def test_remove_all_clears_tags(self, mgr):
        mgr.add_tags("doc1", ["x", "y"])
        mgr.remove_all_tags("doc1")
        assert mgr.tags_for_doc("doc1") == []

    def test_remove_all_does_not_affect_other_docs(self, mgr):
        mgr.add_tag("doc1", "shared")
        mgr.add_tag("doc2", "shared")
        mgr.remove_all_tags("doc1")
        assert mgr.has_tag("doc2", "shared")


# ===========================================================================
# has_tag / tags_for_doc / docs_with_tag
# ===========================================================================


class TestBasicQueries:
    def test_has_tag_true(self, mgr):
        mgr.add_tag("doc1", "python")
        assert mgr.has_tag("doc1", "python") is True

    def test_has_tag_false(self, mgr):
        assert mgr.has_tag("doc1", "python") is False

    def test_tags_for_doc_sorted(self, mgr):
        mgr.add_tags("doc1", ["zzz", "aaa", "mmm"])
        assert mgr.tags_for_doc("doc1") == ["aaa", "mmm", "zzz"]

    def test_tags_for_doc_empty(self, mgr):
        assert mgr.tags_for_doc("unknown") == []

    def test_docs_with_tag_sorted(self, mgr):
        mgr.add_tag("doc_c", "python")
        mgr.add_tag("doc_a", "python")
        mgr.add_tag("doc_b", "python")
        assert mgr.docs_with_tag("python") == ["doc_a", "doc_b", "doc_c"]

    def test_docs_with_tag_empty(self, mgr):
        assert mgr.docs_with_tag("nonexistent") == []

    def test_docs_with_tag_alias_resolved(self, mgr):
        mgr.register_alias("py", "python")
        mgr.add_tag("doc1", "python")
        assert mgr.docs_with_tag("py") == ["doc1"]


# ===========================================================================
# docs_with_all_tags / docs_with_any_tag
# ===========================================================================


class TestSetQueries:
    def test_docs_with_all_tags_basic(self, mgr):
        mgr.add_tags("doc1", ["a", "b", "c"])
        mgr.add_tags("doc2", ["a", "b"])
        mgr.add_tags("doc3", ["a"])
        assert mgr.docs_with_all_tags(["a", "b", "c"]) == ["doc1"]

    def test_docs_with_all_tags_empty_input(self, mgr):
        mgr.add_tag("doc1", "a")
        assert mgr.docs_with_all_tags([]) == []

    def test_docs_with_all_tags_no_match(self, mgr):
        mgr.add_tags("doc1", ["a", "b"])
        assert mgr.docs_with_all_tags(["a", "c"]) == []

    def test_docs_with_all_tags_single_tag(self, mgr):
        mgr.add_tag("doc1", "python")
        mgr.add_tag("doc2", "java")
        assert mgr.docs_with_all_tags(["python"]) == ["doc1"]

    def test_docs_with_any_tag_basic(self, mgr):
        mgr.add_tags("doc1", ["a"])
        mgr.add_tags("doc2", ["b"])
        mgr.add_tags("doc3", ["c"])
        result = mgr.docs_with_any_tag(["a", "b"])
        assert result == ["doc1", "doc2"]

    def test_docs_with_any_tag_deduplication(self, mgr):
        mgr.add_tags("doc1", ["a", "b"])
        result = mgr.docs_with_any_tag(["a", "b"])
        assert result == ["doc1"]

    def test_docs_with_any_tag_empty_input(self, mgr):
        mgr.add_tag("doc1", "a")
        assert mgr.docs_with_any_tag([]) == []

    def test_docs_with_any_tag_sorted(self, mgr):
        mgr.add_tag("doc_z", "x")
        mgr.add_tag("doc_a", "y")
        assert mgr.docs_with_any_tag(["x", "y"]) == ["doc_a", "doc_z"]


# ===========================================================================
# rename_tag
# ===========================================================================


class TestRenameTag:
    def test_rename_tag_returns_affected_count(self, mgr):
        mgr.add_tag("doc1", "python")
        mgr.add_tag("doc2", "python")
        assert mgr.rename_tag("python", "py3") == 2

    def test_rename_tag_old_tag_gone(self, mgr):
        mgr.add_tag("doc1", "old")
        mgr.rename_tag("old", "new")
        assert not mgr.has_tag("doc1", "old")
        assert mgr.has_tag("doc1", "new")

    def test_rename_tag_nonexistent_returns_zero(self, mgr):
        assert mgr.rename_tag("ghost", "new") == 0

    def test_rename_tag_doc_already_has_new_tag(self, mgr):
        mgr.add_tags("doc1", ["old", "new"])
        count = mgr.rename_tag("old", "new")
        # doc1 had 'old', it was removed; 'new' already present — still affected
        assert count == 1
        assert mgr.tags_for_doc("doc1") == ["new"]

    def test_rename_tag_updates_alias_canonical(self, mgr):
        mgr.register_alias("py", "python")
        mgr.add_tag("doc1", "python")
        mgr.rename_tag("python", "py3")
        # Alias should now point to new name
        mgr.add_tag("doc2", "py")
        assert mgr.has_tag("doc2", "py3")

    def test_rename_tag_updates_hierarchy_parent(self, mgr):
        mgr.set_parent("django", "python")
        mgr.rename_tag("python", "py3")
        assert mgr.ancestors_of("django") == ["py3"]


# ===========================================================================
# register_alias
# ===========================================================================


class TestRegisterAlias:
    def test_alias_resolves_on_add(self, mgr):
        mgr.register_alias("ts", "typescript")
        mgr.add_tag("doc1", "ts")
        assert mgr.has_tag("doc1", "typescript")

    def test_canonical_and_alias_same_doc(self, mgr):
        mgr.register_alias("py", "python")
        mgr.add_tag("doc1", "python")
        mgr.add_tag("doc1", "py")  # should not double-add
        assert mgr.tags_for_doc("doc1") == ["python"]

    def test_multiple_aliases_same_canonical(self, mgr):
        mgr.register_alias("py", "python")
        mgr.register_alias("python3", "python")
        mgr.add_tag("doc1", "py")
        mgr.add_tag("doc2", "python3")
        assert mgr.docs_with_tag("python") == ["doc1", "doc2"]

    def test_tag_info_lists_aliases(self, mgr):
        mgr.register_alias("py", "python")
        mgr.register_alias("python3", "python")
        mgr.add_tag("doc1", "python")
        info = mgr.tag_info("python")
        assert info is not None
        assert sorted(info.aliases) == ["py", "python3"]


# ===========================================================================
# set_parent / ancestors_of
# ===========================================================================


class TestHierarchy:
    def test_ancestors_single_level(self, mgr):
        mgr.set_parent("django", "python")
        assert mgr.ancestors_of("django") == ["python"]

    def test_ancestors_multi_level(self, mgr):
        mgr.set_parent("python", "language")
        mgr.set_parent("language", "programming")
        assert mgr.ancestors_of("python") == ["language", "programming"]

    def test_ancestors_three_levels(self, mgr):
        mgr.set_parent("django", "python")
        mgr.set_parent("python", "language")
        mgr.set_parent("language", "programming")
        assert mgr.ancestors_of("django") == ["python", "language", "programming"]

    def test_ancestors_no_parent(self, mgr):
        assert mgr.ancestors_of("python") == []

    def test_ancestors_cycle_does_not_hang(self, mgr):
        mgr.set_parent("a", "b")
        mgr.set_parent("b", "a")
        # Should return ["b"] or ["a"] — just one hop before cycle detected
        result = mgr.ancestors_of("a")
        assert "b" in result
        assert result.count("a") == 0  # "a" itself should not appear in ancestors

    def test_tag_info_has_parent(self, mgr):
        mgr.set_parent("django", "python")
        mgr.add_tag("doc1", "django")
        info = mgr.tag_info("django")
        assert info is not None
        assert info.parent == "python"


# ===========================================================================
# tag_info
# ===========================================================================


class TestTagInfo:
    def test_tag_info_none_for_unknown(self, mgr):
        assert mgr.tag_info("ghost") is None

    def test_tag_info_doc_count(self, mgr):
        mgr.add_tag("doc1", "python")
        mgr.add_tag("doc2", "python")
        info = mgr.tag_info("python")
        assert info is not None
        assert info.doc_count == 2

    def test_tag_info_decreases_after_removal(self, mgr):
        mgr.add_tag("doc1", "python")
        mgr.add_tag("doc2", "python")
        mgr.remove_tag("doc1", "python")
        info = mgr.tag_info("python")
        assert info is not None
        assert info.doc_count == 1

    def test_tag_info_known_via_alias(self, mgr):
        mgr.register_alias("py", "python")
        # "python" is canonical of "py" alias → should be known
        info = mgr.tag_info("python")
        assert info is not None
        assert "py" in info.aliases

    def test_tag_info_known_via_parent(self, mgr):
        mgr.set_parent("django", "python")
        # "django" has a parent, so it should be known even with 0 docs
        info = mgr.tag_info("django")
        assert info is not None
        assert info.parent == "python"

    def test_tag_info_tag_field(self, mgr):
        mgr.add_tag("doc1", "rust")
        info = mgr.tag_info("rust")
        assert info is not None
        assert info.tag == "rust"


# ===========================================================================
# all_tags
# ===========================================================================


class TestAllTags:
    def test_all_tags_empty(self, mgr):
        assert mgr.all_tags() == []

    def test_all_tags_sorted(self, mgr):
        mgr.add_tag("doc1", "zzz")
        mgr.add_tag("doc2", "aaa")
        mgr.add_tag("doc3", "mmm")
        assert mgr.all_tags() == ["aaa", "mmm", "zzz"]

    def test_all_tags_excludes_removed(self, mgr):
        mgr.add_tag("doc1", "python")
        mgr.remove_tag("doc1", "python")
        assert "python" not in mgr.all_tags()

    def test_all_tags_excludes_alias_name(self, mgr):
        mgr.register_alias("py", "python")
        mgr.add_tag("doc1", "py")
        tags = mgr.all_tags()
        assert "python" in tags
        assert "py" not in tags


# ===========================================================================
# get_doc_tags
# ===========================================================================


class TestGetDocTags:
    def test_get_doc_tags_basic(self, mgr):
        mgr.add_tags("doc1", ["b", "a", "c"])
        dt = mgr.get_doc_tags("doc1")
        assert isinstance(dt, DocTags)
        assert dt.doc_id == "doc1"
        assert dt.tags == ["a", "b", "c"]
        assert dt.tag_count == 3

    def test_get_doc_tags_empty(self, mgr):
        dt = mgr.get_doc_tags("nobody")
        assert dt.doc_id == "nobody"
        assert dt.tags == []
        assert dt.tag_count == 0


# ===========================================================================
# stats
# ===========================================================================


class TestStats:
    def test_stats_empty(self, mgr):
        s = mgr.stats()
        assert isinstance(s, TagManagerStats)
        assert s.total_tags == 0
        assert s.total_docs == 0
        assert s.total_assignments == 0

    def test_stats_after_adds(self, mgr):
        mgr.add_tags("doc1", ["a", "b"])
        mgr.add_tags("doc2", ["b", "c"])
        s = mgr.stats()
        assert s.total_tags == 3   # a, b, c
        assert s.total_docs == 2
        assert s.total_assignments == 4

    def test_stats_decreases_after_remove_all(self, mgr):
        mgr.add_tags("doc1", ["x", "y"])
        mgr.remove_all_tags("doc1")
        s = mgr.stats()
        assert s.total_docs == 0
        assert s.total_assignments == 0


# ===========================================================================
# Thread safety
# ===========================================================================


class TestThreadSafety:
    def test_concurrent_add_tags(self, mgr):
        errors: list[Exception] = []

        def worker(doc_id: str, tags: list[str]) -> None:
            try:
                mgr.add_tags(doc_id, tags)
            except Exception as exc:
                errors.append(exc)

        threads = [
            threading.Thread(target=worker, args=(f"doc{i}", ["tag_a", "tag_b", f"t{i}"]))
            for i in range(20)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors
        s = mgr.stats()
        assert s.total_docs == 20

    def test_concurrent_read_write(self, mgr):
        mgr.add_tags("shared", ["x", "y", "z"])
        results: list[list[str]] = []

        def reader() -> None:
            for _ in range(50):
                results.append(mgr.tags_for_doc("shared"))

        def writer() -> None:
            for i in range(10):
                mgr.add_tag("shared", f"new_{i}")

        r = threading.Thread(target=reader)
        w = threading.Thread(target=writer)
        r.start()
        w.start()
        r.join()
        w.join()
        # No assertion on results order — just verify no exception was raised
        assert len(results) == 50
