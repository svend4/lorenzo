"""Tests for docstoolkit.doc_label_manager (E302)."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_label_manager import (
    DocLabelManager,
    DocLabels,
    Label,
    LabelStats,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_manager() -> DocLabelManager:
    return DocLabelManager()


def make_label(
    name: str = "bug",
    color: str = "#ff0000",
    description: str = "A bug",
) -> Label:
    return Label(name=name, color=color, description=description)


# ---------------------------------------------------------------------------
# TestLabelDataclass
# ---------------------------------------------------------------------------

class TestLabelDataclass:
    def test_name_stored(self):
        lbl = Label(name="urgent")
        assert lbl.name == "urgent"

    def test_default_color(self):
        lbl = Label(name="x")
        assert lbl.color == "#cccccc"

    def test_custom_color(self):
        lbl = Label(name="x", color="#ff0000")
        assert lbl.color == "#ff0000"

    def test_default_description_empty(self):
        lbl = Label(name="x")
        assert lbl.description == ""

    def test_custom_description(self):
        lbl = Label(name="x", description="Some desc")
        assert lbl.description == "Some desc"

    def test_all_fields_set(self):
        lbl = Label(name="feat", color="#00ff00", description="Feature")
        assert lbl.name == "feat"
        assert lbl.color == "#00ff00"
        assert lbl.description == "Feature"


# ---------------------------------------------------------------------------
# TestDocLabelsDataclass
# ---------------------------------------------------------------------------

class TestDocLabelsDataclass:
    def test_doc_id_stored(self):
        dl = DocLabels(doc_id="d1")
        assert dl.doc_id == "d1"

    def test_default_labels_empty(self):
        dl = DocLabels(doc_id="d1")
        assert dl.labels == []

    def test_default_label_count_zero(self):
        dl = DocLabels(doc_id="d1")
        assert dl.label_count == 0

    def test_labels_and_count_stored(self):
        dl = DocLabels(doc_id="d1", labels=["a", "b"], label_count=2)
        assert dl.labels == ["a", "b"]
        assert dl.label_count == 2


# ---------------------------------------------------------------------------
# TestLabelStatsDataclass
# ---------------------------------------------------------------------------

class TestLabelStatsDataclass:
    def test_total_labels_stored(self):
        s = LabelStats(total_labels=5)
        assert s.total_labels == 5

    def test_total_docs_stored(self):
        s = LabelStats(total_docs=3)
        assert s.total_docs == 3

    def test_total_assignments_stored(self):
        s = LabelStats(total_assignments=10)
        assert s.total_assignments == 10

    def test_defaults_zero(self):
        s = LabelStats()
        assert s.total_labels == 0
        assert s.total_docs == 0
        assert s.total_assignments == 0


# ---------------------------------------------------------------------------
# TestConstruction
# ---------------------------------------------------------------------------

class TestConstruction:
    def test_empty_list_labels(self):
        m = make_manager()
        assert m.list_labels() == []

    def test_empty_stats(self):
        m = make_manager()
        s = m.stats()
        assert s.total_labels == 0
        assert s.total_docs == 0
        assert s.total_assignments == 0

    def test_get_label_unknown_returns_none(self):
        m = make_manager()
        assert m.get_label("nonexistent") is None

    def test_docs_with_label_empty(self):
        m = make_manager()
        assert m.docs_with_label("bug") == []


# ---------------------------------------------------------------------------
# TestDefineLabel
# ---------------------------------------------------------------------------

class TestDefineLabel:
    def test_define_new_label(self):
        m = make_manager()
        m.define_label(Label(name="bug"))
        assert m.get_label("bug") is not None

    def test_define_updates_existing(self):
        m = make_manager()
        m.define_label(Label(name="bug", color="#ff0000"))
        m.define_label(Label(name="bug", color="#0000ff"))
        assert m.get_label("bug").color == "#0000ff"

    def test_define_updates_description(self):
        m = make_manager()
        m.define_label(Label(name="bug", description="old"))
        m.define_label(Label(name="bug", description="new"))
        assert m.get_label("bug").description == "new"

    def test_define_multiple_labels(self):
        m = make_manager()
        m.define_label(Label(name="bug"))
        m.define_label(Label(name="feature"))
        assert len(m.list_labels()) == 2

    def test_define_stores_color(self):
        m = make_manager()
        m.define_label(Label(name="critical", color="#ff0000"))
        assert m.get_label("critical").color == "#ff0000"

    def test_define_stores_description(self):
        m = make_manager()
        m.define_label(Label(name="wontfix", description="Will not be fixed"))
        assert m.get_label("wontfix").description == "Will not be fixed"


# ---------------------------------------------------------------------------
# TestUndefineLabel
# ---------------------------------------------------------------------------

class TestUndefineLabel:
    def test_undefine_existing_returns_true(self):
        m = make_manager()
        m.define_label(Label(name="bug"))
        assert m.undefine_label("bug") is True

    def test_undefine_nonexistent_returns_false(self):
        m = make_manager()
        assert m.undefine_label("ghost") is False

    def test_undefine_removes_definition(self):
        m = make_manager()
        m.define_label(Label(name="bug"))
        m.undefine_label("bug")
        assert m.get_label("bug") is None

    def test_undefine_removes_assignments(self):
        m = make_manager()
        m.define_label(Label(name="bug"))
        m.assign_label("doc1", "bug")
        m.assign_label("doc2", "bug")
        m.undefine_label("bug")
        assert not m.has_label("doc1", "bug")
        assert not m.has_label("doc2", "bug")

    def test_undefine_removes_from_list(self):
        m = make_manager()
        m.define_label(Label(name="a"))
        m.define_label(Label(name="b"))
        m.undefine_label("a")
        names = [lbl.name for lbl in m.list_labels()]
        assert "a" not in names

    def test_undefine_twice_returns_false_second(self):
        m = make_manager()
        m.define_label(Label(name="x"))
        m.undefine_label("x")
        assert m.undefine_label("x") is False

    def test_undefine_cleans_doc_label_index(self):
        m = make_manager()
        m.define_label(Label(name="bug"))
        m.assign_label("doc1", "bug")
        m.undefine_label("bug")
        assert m.labels_for_doc("doc1").labels == []


# ---------------------------------------------------------------------------
# TestGetLabel
# ---------------------------------------------------------------------------

class TestGetLabel:
    def test_get_defined_label(self):
        m = make_manager()
        lbl = Label(name="urgent", color="#ff9900")
        m.define_label(lbl)
        result = m.get_label("urgent")
        assert result is not None
        assert result.name == "urgent"

    def test_get_undefined_label_returns_none(self):
        m = make_manager()
        assert m.get_label("missing") is None

    def test_get_returns_current_definition(self):
        m = make_manager()
        m.define_label(Label(name="x", color="#111111"))
        m.define_label(Label(name="x", color="#222222"))
        assert m.get_label("x").color == "#222222"


# ---------------------------------------------------------------------------
# TestListLabels
# ---------------------------------------------------------------------------

class TestListLabels:
    def test_list_empty(self):
        m = make_manager()
        assert m.list_labels() == []

    def test_list_sorted_by_name(self):
        m = make_manager()
        m.define_label(Label(name="zebra"))
        m.define_label(Label(name="alpha"))
        m.define_label(Label(name="middle"))
        names = [lbl.name for lbl in m.list_labels()]
        assert names == sorted(names)

    def test_list_returns_label_instances(self):
        m = make_manager()
        m.define_label(Label(name="bug"))
        result = m.list_labels()
        assert all(isinstance(lbl, Label) for lbl in result)

    def test_list_count(self):
        m = make_manager()
        for i in range(5):
            m.define_label(Label(name=f"lbl{i}"))
        assert len(m.list_labels()) == 5


# ---------------------------------------------------------------------------
# TestAssignLabel
# ---------------------------------------------------------------------------

class TestAssignLabel:
    def test_assign_new_returns_true(self):
        m = make_manager()
        assert m.assign_label("doc1", "bug") is True

    def test_assign_duplicate_returns_false(self):
        m = make_manager()
        m.assign_label("doc1", "bug")
        assert m.assign_label("doc1", "bug") is False

    def test_assign_implicit_no_predefine_needed(self):
        m = make_manager()
        result = m.assign_label("doc1", "unlisted_label")
        assert result is True
        assert m.has_label("doc1", "unlisted_label")

    def test_assign_multiple_labels_to_one_doc(self):
        m = make_manager()
        m.assign_label("doc1", "bug")
        m.assign_label("doc1", "urgent")
        dl = m.labels_for_doc("doc1")
        assert "bug" in dl.labels
        assert "urgent" in dl.labels

    def test_assign_same_label_to_multiple_docs(self):
        m = make_manager()
        m.assign_label("doc1", "bug")
        m.assign_label("doc2", "bug")
        assert "doc1" in m.docs_with_label("bug")
        assert "doc2" in m.docs_with_label("bug")

    def test_assign_different_label_names_same_doc(self):
        m = make_manager()
        m.assign_label("doc1", "a")
        m.assign_label("doc1", "b")
        assert m.has_label("doc1", "a")
        assert m.has_label("doc1", "b")


# ---------------------------------------------------------------------------
# TestUnassignLabel
# ---------------------------------------------------------------------------

class TestUnassignLabel:
    def test_unassign_present_returns_true(self):
        m = make_manager()
        m.assign_label("doc1", "bug")
        assert m.unassign_label("doc1", "bug") is True

    def test_unassign_absent_returns_false(self):
        m = make_manager()
        assert m.unassign_label("doc1", "bug") is False

    def test_unassign_removes_from_doc(self):
        m = make_manager()
        m.assign_label("doc1", "bug")
        m.unassign_label("doc1", "bug")
        assert not m.has_label("doc1", "bug")

    def test_unassign_removes_from_label_index(self):
        m = make_manager()
        m.assign_label("doc1", "bug")
        m.unassign_label("doc1", "bug")
        assert "doc1" not in m.docs_with_label("bug")

    def test_unassign_leaves_other_labels(self):
        m = make_manager()
        m.assign_label("doc1", "bug")
        m.assign_label("doc1", "urgent")
        m.unassign_label("doc1", "bug")
        assert m.has_label("doc1", "urgent")

    def test_unassign_from_wrong_doc_returns_false(self):
        m = make_manager()
        m.assign_label("doc1", "bug")
        assert m.unassign_label("doc2", "bug") is False


# ---------------------------------------------------------------------------
# TestUnassignAll
# ---------------------------------------------------------------------------

class TestUnassignAll:
    def test_unassign_all_returns_count(self):
        m = make_manager()
        m.assign_label("doc1", "a")
        m.assign_label("doc1", "b")
        m.assign_label("doc1", "c")
        assert m.unassign_all("doc1") == 3

    def test_unassign_all_empty_doc_returns_zero(self):
        m = make_manager()
        assert m.unassign_all("doc1") == 0

    def test_unassign_all_clears_doc(self):
        m = make_manager()
        m.assign_label("doc1", "a")
        m.assign_label("doc1", "b")
        m.unassign_all("doc1")
        assert m.labels_for_doc("doc1").labels == []

    def test_unassign_all_does_not_affect_other_docs(self):
        m = make_manager()
        m.assign_label("doc1", "bug")
        m.assign_label("doc2", "bug")
        m.unassign_all("doc1")
        assert m.has_label("doc2", "bug")

    def test_unassign_all_updates_label_index(self):
        m = make_manager()
        m.assign_label("doc1", "bug")
        m.unassign_all("doc1")
        assert "doc1" not in m.docs_with_label("bug")


# ---------------------------------------------------------------------------
# TestHasLabel
# ---------------------------------------------------------------------------

class TestHasLabel:
    def test_has_label_true(self):
        m = make_manager()
        m.assign_label("doc1", "bug")
        assert m.has_label("doc1", "bug") is True

    def test_has_label_false_not_assigned(self):
        m = make_manager()
        assert m.has_label("doc1", "bug") is False

    def test_has_label_false_after_unassign(self):
        m = make_manager()
        m.assign_label("doc1", "bug")
        m.unassign_label("doc1", "bug")
        assert m.has_label("doc1", "bug") is False

    def test_has_label_false_different_doc(self):
        m = make_manager()
        m.assign_label("doc1", "bug")
        assert m.has_label("doc2", "bug") is False


# ---------------------------------------------------------------------------
# TestLabelsForDoc
# ---------------------------------------------------------------------------

class TestLabelsForDoc:
    def test_labels_for_doc_sorted(self):
        m = make_manager()
        m.assign_label("doc1", "zebra")
        m.assign_label("doc1", "alpha")
        m.assign_label("doc1", "middle")
        dl = m.labels_for_doc("doc1")
        assert dl.labels == sorted(dl.labels)

    def test_labels_for_doc_count(self):
        m = make_manager()
        m.assign_label("doc1", "a")
        m.assign_label("doc1", "b")
        dl = m.labels_for_doc("doc1")
        assert dl.label_count == 2

    def test_labels_for_doc_returns_doc_labels_type(self):
        m = make_manager()
        result = m.labels_for_doc("doc1")
        assert isinstance(result, DocLabels)

    def test_labels_for_unknown_doc_returns_empty(self):
        m = make_manager()
        dl = m.labels_for_doc("nonexistent")
        assert dl.labels == []
        assert dl.label_count == 0
        assert dl.doc_id == "nonexistent"


# ---------------------------------------------------------------------------
# TestDocsWithLabel
# ---------------------------------------------------------------------------

class TestDocsWithLabel:
    def test_docs_with_label_sorted(self):
        m = make_manager()
        m.assign_label("doc_z", "bug")
        m.assign_label("doc_a", "bug")
        result = m.docs_with_label("bug")
        assert result == sorted(result)

    def test_docs_with_label_empty_when_none(self):
        m = make_manager()
        assert m.docs_with_label("bug") == []

    def test_docs_with_label_after_unassign(self):
        m = make_manager()
        m.assign_label("doc1", "bug")
        m.unassign_label("doc1", "bug")
        assert m.docs_with_label("bug") == []

    def test_docs_with_label_multiple_docs(self):
        m = make_manager()
        for i in range(3):
            m.assign_label(f"doc{i}", "bug")
        assert len(m.docs_with_label("bug")) == 3


# ---------------------------------------------------------------------------
# TestDocsWithAllLabels
# ---------------------------------------------------------------------------

class TestDocsWithAllLabels:
    def test_intersection_basic(self):
        m = make_manager()
        m.assign_label("doc1", "a")
        m.assign_label("doc1", "b")
        m.assign_label("doc2", "a")  # has 'a' but not 'b'
        result = m.docs_with_all_labels(["a", "b"])
        assert result == ["doc1"]

    def test_intersection_no_match(self):
        m = make_manager()
        m.assign_label("doc1", "a")
        m.assign_label("doc2", "b")
        assert m.docs_with_all_labels(["a", "b"]) == []

    def test_intersection_sorted(self):
        m = make_manager()
        for doc in ["doc_z", "doc_a", "doc_m"]:
            m.assign_label(doc, "x")
            m.assign_label(doc, "y")
        result = m.docs_with_all_labels(["x", "y"])
        assert result == sorted(result)

    def test_empty_label_names_returns_all_docs(self):
        m = make_manager()
        m.assign_label("doc1", "a")
        m.assign_label("doc2", "b")
        result = m.docs_with_all_labels([])
        assert set(result) == {"doc1", "doc2"}

    def test_single_label_intersection(self):
        m = make_manager()
        m.assign_label("doc1", "bug")
        m.assign_label("doc2", "bug")
        assert set(m.docs_with_all_labels(["bug"])) == {"doc1", "doc2"}


# ---------------------------------------------------------------------------
# TestDocsWithAnyLabel
# ---------------------------------------------------------------------------

class TestDocsWithAnyLabel:
    def test_union_basic(self):
        m = make_manager()
        m.assign_label("doc1", "a")
        m.assign_label("doc2", "b")
        result = m.docs_with_any_label(["a", "b"])
        assert set(result) == {"doc1", "doc2"}

    def test_union_deduplicated(self):
        m = make_manager()
        m.assign_label("doc1", "a")
        m.assign_label("doc1", "b")
        result = m.docs_with_any_label(["a", "b"])
        assert result.count("doc1") == 1

    def test_union_sorted(self):
        m = make_manager()
        m.assign_label("doc_z", "x")
        m.assign_label("doc_a", "y")
        result = m.docs_with_any_label(["x", "y"])
        assert result == sorted(result)

    def test_union_empty_labels_returns_empty(self):
        m = make_manager()
        m.assign_label("doc1", "a")
        assert m.docs_with_any_label([]) == []

    def test_union_label_no_docs_returns_empty(self):
        m = make_manager()
        assert m.docs_with_any_label(["nonexistent"]) == []


# ---------------------------------------------------------------------------
# TestRenameLabel
# ---------------------------------------------------------------------------

class TestRenameLabel:
    def test_rename_updates_assignments(self):
        m = make_manager()
        m.assign_label("doc1", "old")
        m.rename_label("old", "new")
        assert m.has_label("doc1", "new")
        assert not m.has_label("doc1", "old")

    def test_rename_updates_definition(self):
        m = make_manager()
        m.define_label(Label(name="old", color="#ff0000"))
        m.rename_label("old", "new")
        assert m.get_label("new") is not None
        assert m.get_label("old") is None

    def test_rename_returns_affected_count(self):
        m = make_manager()
        m.assign_label("doc1", "old")
        m.assign_label("doc2", "old")
        assert m.rename_label("old", "new") == 2

    def test_rename_no_assignments_returns_zero(self):
        m = make_manager()
        m.define_label(Label(name="old"))
        assert m.rename_label("old", "new") == 0

    def test_rename_preserves_color_in_definition(self):
        m = make_manager()
        m.define_label(Label(name="old", color="#abcdef"))
        m.rename_label("old", "new")
        lbl = m.get_label("new")
        assert lbl is not None
        assert lbl.color == "#abcdef"

    def test_rename_updates_docs_with_label(self):
        m = make_manager()
        m.assign_label("doc1", "old")
        m.rename_label("old", "new")
        assert "doc1" in m.docs_with_label("new")
        assert "doc1" not in m.docs_with_label("old")

    def test_rename_same_name_returns_zero(self):
        m = make_manager()
        m.assign_label("doc1", "tag")
        assert m.rename_label("tag", "tag") == 0

    def test_rename_nonexistent_label_returns_zero(self):
        m = make_manager()
        assert m.rename_label("ghost", "phantom") == 0


# ---------------------------------------------------------------------------
# TestStats
# ---------------------------------------------------------------------------

class TestStats:
    def test_stats_returns_label_stats(self):
        m = make_manager()
        assert isinstance(m.stats(), LabelStats)

    def test_stats_total_labels(self):
        m = make_manager()
        m.define_label(Label(name="a"))
        m.define_label(Label(name="b"))
        assert m.stats().total_labels == 2

    def test_stats_total_docs(self):
        m = make_manager()
        m.assign_label("doc1", "x")
        m.assign_label("doc2", "x")
        assert m.stats().total_docs == 2

    def test_stats_total_assignments(self):
        m = make_manager()
        m.assign_label("doc1", "a")
        m.assign_label("doc1", "b")
        m.assign_label("doc2", "a")
        assert m.stats().total_assignments == 3

    def test_stats_empty_manager(self):
        m = make_manager()
        s = m.stats()
        assert s.total_labels == 0
        assert s.total_docs == 0
        assert s.total_assignments == 0

    def test_stats_after_unassign_all(self):
        m = make_manager()
        m.assign_label("doc1", "a")
        m.unassign_all("doc1")
        s = m.stats()
        assert s.total_docs == 0
        assert s.total_assignments == 0

    def test_stats_docs_with_at_least_one_label(self):
        m = make_manager()
        m.assign_label("doc1", "a")
        m.assign_label("doc1", "b")
        # doc1 has 2 labels but is only one doc
        assert m.stats().total_docs == 1


# ---------------------------------------------------------------------------
# TestThreadSafety
# ---------------------------------------------------------------------------

class TestThreadSafety:
    def test_concurrent_assign_label(self):
        """Multiple threads assigning unique labels should not lose any."""
        m = make_manager()
        errors: list[Exception] = []

        def worker(doc_id: str, label_name: str) -> None:
            try:
                m.assign_label(doc_id, label_name)
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        threads = [
            threading.Thread(target=worker, args=(f"doc{i}", f"label{i}"))
            for i in range(50)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == [], f"Exceptions in threads: {errors}"
        # Each thread assigned one unique label to one unique doc
        for i in range(50):
            assert m.has_label(f"doc{i}", f"label{i}")

    def test_concurrent_assign_same_label(self):
        """Many threads assigning the same label to the same doc: exactly one wins."""
        m = make_manager()
        results: list[bool] = []
        lock = threading.Lock()

        def worker() -> None:
            result = m.assign_label("shared_doc", "shared_label")
            with lock:
                results.append(result)

        threads = [threading.Thread(target=worker) for _ in range(30)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Exactly one True (newly assigned), rest False (already present)
        assert results.count(True) == 1
        assert results.count(False) == 29
