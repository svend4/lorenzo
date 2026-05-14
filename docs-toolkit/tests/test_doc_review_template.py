"""Tests for docstoolkit.doc_review_template (E404)."""
from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_review_template import (
    ChecklistItem,
    DocReviewTemplate,
    ReviewTemplate,
    TemplateStats,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _mgr() -> DocReviewTemplate:
    return DocReviewTemplate()


def _items(n: int = 3, start_order: int = 0) -> list[ChecklistItem]:
    return [
        ChecklistItem(
            item_id=f"i{i}",
            text=f"check {i}",
            required=(i % 2 == 0),
            weight=float(i + 1),
            order=start_order + i,
        )
        for i in range(n)
    ]


# ---------------------------------------------------------------------------
# Dataclass tests
# ---------------------------------------------------------------------------

class TestChecklistItemDataclass:
    def test_required_fields(self):
        c = ChecklistItem(item_id="x", text="t")
        assert c.item_id == "x"
        assert c.text == "t"

    def test_defaults(self):
        c = ChecklistItem(item_id="x", text="t")
        assert c.required is True
        assert c.weight == 1.0
        assert c.order == 0

    def test_custom_values(self):
        c = ChecklistItem(item_id="x", text="t", required=False, weight=2.5, order=7)
        assert c.required is False
        assert c.weight == 2.5
        assert c.order == 7


class TestReviewTemplateDataclass:
    def test_required_fields(self):
        t = ReviewTemplate(template_id="t1", name="Name")
        assert t.template_id == "t1"
        assert t.name == "Name"

    def test_defaults(self):
        t = ReviewTemplate(template_id="t1", name="Name")
        assert t.description == ""
        assert t.items == []
        assert t.created_at == 0.0

    def test_items_factory_independent(self):
        a = ReviewTemplate(template_id="a", name="A")
        b = ReviewTemplate(template_id="b", name="B")
        a.items.append(ChecklistItem(item_id="x", text="t"))
        assert b.items == []


class TestTemplateStatsDataclass:
    def test_fields(self):
        s = TemplateStats(total_templates=2, total_items=5, avg_items_per_template=2.5)
        assert s.total_templates == 2
        assert s.total_items == 5
        assert s.avg_items_per_template == 2.5


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------

class TestConstruction:
    def test_empty(self):
        m = _mgr()
        assert m.list_templates() == []

    def test_stats_empty(self):
        m = _mgr()
        s = m.stats()
        assert s.total_templates == 0
        assert s.total_items == 0
        assert s.avg_items_per_template == 0.0

    def test_independent_instances(self):
        a = _mgr()
        b = _mgr()
        a.create_template("t1", "T1", _items(2))
        assert b.list_templates() == []


# ---------------------------------------------------------------------------
# create_template
# ---------------------------------------------------------------------------

class TestCreateTemplate:
    def test_returns_template(self):
        m = _mgr()
        t = m.create_template("t1", "Name", _items(2))
        assert isinstance(t, ReviewTemplate)
        assert t.template_id == "t1"
        assert t.name == "Name"

    def test_with_description(self):
        m = _mgr()
        t = m.create_template("t1", "Name", [], description="hi")
        assert t.description == "hi"

    def test_now_used(self):
        m = _mgr()
        t = m.create_template("t1", "N", [], now=42.0)
        assert t.created_at == 42.0

    def test_now_default(self):
        m = _mgr()
        t = m.create_template("t1", "N", [])
        assert t.created_at > 0

    def test_items_sorted_by_order(self):
        m = _mgr()
        items = [
            ChecklistItem(item_id="a", text="A", order=2),
            ChecklistItem(item_id="b", text="B", order=0),
            ChecklistItem(item_id="c", text="C", order=1),
        ]
        t = m.create_template("t1", "N", items)
        assert [i.item_id for i in t.items] == ["b", "c", "a"]

    def test_stored(self):
        m = _mgr()
        m.create_template("t1", "N", _items(2))
        assert m.get_template("t1") is not None

    def test_overwrite_same_id(self):
        m = _mgr()
        m.create_template("t1", "Old", _items(2))
        m.create_template("t1", "New", _items(3))
        t = m.get_template("t1")
        assert t.name == "New"
        assert len(t.items) == 3


# ---------------------------------------------------------------------------
# update_template
# ---------------------------------------------------------------------------

class TestUpdateTemplate:
    def test_missing_returns_none(self):
        m = _mgr()
        assert m.update_template("nope", name="X") is None

    def test_update_name(self):
        m = _mgr()
        m.create_template("t1", "Old", _items(1))
        t = m.update_template("t1", name="New")
        assert t.name == "New"

    def test_update_description(self):
        m = _mgr()
        m.create_template("t1", "N", _items(1), description="old")
        t = m.update_template("t1", description="new")
        assert t.description == "new"

    def test_update_items_resort(self):
        m = _mgr()
        m.create_template("t1", "N", _items(1))
        new_items = [
            ChecklistItem(item_id="x", text="X", order=5),
            ChecklistItem(item_id="y", text="Y", order=1),
        ]
        t = m.update_template("t1", items=new_items)
        assert [i.item_id for i in t.items] == ["y", "x"]

    def test_partial_keeps_other_fields(self):
        m = _mgr()
        m.create_template("t1", "Old", _items(2), description="desc")
        t = m.update_template("t1", name="New")
        assert t.name == "New"
        assert t.description == "desc"
        assert len(t.items) == 2

    def test_none_args_keep_existing(self):
        m = _mgr()
        m.create_template("t1", "Old", _items(2), description="d")
        t = m.update_template("t1")
        assert t.name == "Old"
        assert t.description == "d"
        assert len(t.items) == 2


# ---------------------------------------------------------------------------
# delete_template
# ---------------------------------------------------------------------------

class TestDeleteTemplate:
    def test_missing_returns_false(self):
        m = _mgr()
        assert m.delete_template("nope") is False

    def test_removes_template(self):
        m = _mgr()
        m.create_template("t1", "N", _items(1))
        assert m.delete_template("t1") is True
        assert m.get_template("t1") is None

    def test_removes_assignments(self):
        m = _mgr()
        m.create_template("t1", "N", _items(1))
        m.assign("doc-a", "t1")
        m.assign("doc-b", "t1")
        m.delete_template("t1")
        assert m.template_for_doc("doc-a") is None
        assert m.template_for_doc("doc-b") is None

    def test_doesnt_affect_other_assignments(self):
        m = _mgr()
        m.create_template("t1", "N1", _items(1))
        m.create_template("t2", "N2", _items(1))
        m.assign("doc-a", "t1")
        m.assign("doc-b", "t2")
        m.delete_template("t1")
        assert m.template_for_doc("doc-b") is not None


# ---------------------------------------------------------------------------
# get_template
# ---------------------------------------------------------------------------

class TestGetTemplate:
    def test_missing(self):
        m = _mgr()
        assert m.get_template("nope") is None

    def test_found(self):
        m = _mgr()
        m.create_template("t1", "N", _items(2))
        t = m.get_template("t1")
        assert t is not None
        assert t.template_id == "t1"


# ---------------------------------------------------------------------------
# list_templates
# ---------------------------------------------------------------------------

class TestListTemplates:
    def test_empty(self):
        m = _mgr()
        assert m.list_templates() == []

    def test_sorted_by_name(self):
        m = _mgr()
        m.create_template("a", "Zebra", [])
        m.create_template("b", "Apple", [])
        m.create_template("c", "Mango", [])
        names = [t.name for t in m.list_templates()]
        assert names == ["Apple", "Mango", "Zebra"]


# ---------------------------------------------------------------------------
# add_item
# ---------------------------------------------------------------------------

class TestAddItem:
    def test_missing_template(self):
        m = _mgr()
        assert m.add_item("nope", ChecklistItem(item_id="x", text="t")) is False

    def test_adds(self):
        m = _mgr()
        m.create_template("t1", "N", _items(2))
        assert m.add_item("t1", ChecklistItem(item_id="new", text="t", order=99)) is True
        assert m.get_template("t1").items[-1].item_id == "new"

    def test_sorted_after_add(self):
        m = _mgr()
        m.create_template("t1", "N", [
            ChecklistItem(item_id="a", text="a", order=0),
            ChecklistItem(item_id="c", text="c", order=2),
        ])
        m.add_item("t1", ChecklistItem(item_id="b", text="b", order=1))
        order_ids = [i.item_id for i in m.get_template("t1").items]
        assert order_ids == ["a", "b", "c"]


# ---------------------------------------------------------------------------
# remove_item
# ---------------------------------------------------------------------------

class TestRemoveItem:
    def test_missing_template(self):
        m = _mgr()
        assert m.remove_item("nope", "i0") is False

    def test_missing_item(self):
        m = _mgr()
        m.create_template("t1", "N", _items(2))
        assert m.remove_item("t1", "nope") is False

    def test_removes(self):
        m = _mgr()
        m.create_template("t1", "N", _items(3))
        assert m.remove_item("t1", "i1") is True
        ids = [i.item_id for i in m.get_template("t1").items]
        assert "i1" not in ids
        assert len(ids) == 2


# ---------------------------------------------------------------------------
# items_of
# ---------------------------------------------------------------------------

class TestItemsOf:
    def test_missing_template(self):
        m = _mgr()
        assert m.items_of("nope") == []

    def test_all(self):
        m = _mgr()
        m.create_template("t1", "N", _items(4))
        assert len(m.items_of("t1")) == 4

    def test_required_only(self):
        m = _mgr()
        # _items: required True when i%2==0 → i0, i2 are required
        m.create_template("t1", "N", _items(4))
        items = m.items_of("t1", required_only=True)
        assert all(i.required for i in items)
        assert len(items) == 2

    def test_sorted_by_order(self):
        m = _mgr()
        items = [
            ChecklistItem(item_id="a", text="A", order=3),
            ChecklistItem(item_id="b", text="B", order=1),
            ChecklistItem(item_id="c", text="C", order=2),
        ]
        m.create_template("t1", "N", items)
        ids = [i.item_id for i in m.items_of("t1")]
        assert ids == ["b", "c", "a"]


# ---------------------------------------------------------------------------
# total_weight
# ---------------------------------------------------------------------------

class TestTotalWeight:
    def test_missing(self):
        m = _mgr()
        assert m.total_weight("nope") == 0.0

    def test_empty(self):
        m = _mgr()
        m.create_template("t1", "N", [])
        assert m.total_weight("t1") == 0.0

    def test_sum(self):
        m = _mgr()
        # weights are 1.0, 2.0, 3.0
        m.create_template("t1", "N", _items(3))
        assert m.total_weight("t1") == 6.0


# ---------------------------------------------------------------------------
# assign
# ---------------------------------------------------------------------------

class TestAssign:
    def test_missing_template(self):
        m = _mgr()
        assert m.assign("doc-a", "nope") is False

    def test_success(self):
        m = _mgr()
        m.create_template("t1", "N", _items(1))
        assert m.assign("doc-a", "t1") is True

    def test_reassignment_overwrites(self):
        m = _mgr()
        m.create_template("t1", "N1", _items(1))
        m.create_template("t2", "N2", _items(1))
        m.assign("doc-a", "t1")
        m.assign("doc-a", "t2")
        t = m.template_for_doc("doc-a")
        assert t.template_id == "t2"


# ---------------------------------------------------------------------------
# template_for_doc
# ---------------------------------------------------------------------------

class TestTemplateForDoc:
    def test_unassigned(self):
        m = _mgr()
        assert m.template_for_doc("doc-a") is None

    def test_assigned(self):
        m = _mgr()
        m.create_template("t1", "N", _items(1))
        m.assign("doc-a", "t1")
        t = m.template_for_doc("doc-a")
        assert t is not None
        assert t.template_id == "t1"


# ---------------------------------------------------------------------------
# docs_using
# ---------------------------------------------------------------------------

class TestDocsUsing:
    def test_none(self):
        m = _mgr()
        m.create_template("t1", "N", _items(1))
        assert m.docs_using("t1") == []

    def test_sorted(self):
        m = _mgr()
        m.create_template("t1", "N", _items(1))
        m.assign("doc-c", "t1")
        m.assign("doc-a", "t1")
        m.assign("doc-b", "t1")
        assert m.docs_using("t1") == ["doc-a", "doc-b", "doc-c"]

    def test_only_matching(self):
        m = _mgr()
        m.create_template("t1", "N1", _items(1))
        m.create_template("t2", "N2", _items(1))
        m.assign("doc-a", "t1")
        m.assign("doc-b", "t2")
        assert m.docs_using("t1") == ["doc-a"]


# ---------------------------------------------------------------------------
# unassign
# ---------------------------------------------------------------------------

class TestUnassign:
    def test_missing(self):
        m = _mgr()
        assert m.unassign("doc-a") is False

    def test_success(self):
        m = _mgr()
        m.create_template("t1", "N", _items(1))
        m.assign("doc-a", "t1")
        assert m.unassign("doc-a") is True
        assert m.template_for_doc("doc-a") is None


# ---------------------------------------------------------------------------
# clear_assignments
# ---------------------------------------------------------------------------

class TestClearAssignments:
    def test_empty(self):
        m = _mgr()
        assert m.clear_assignments() == 0

    def test_count(self):
        m = _mgr()
        m.create_template("t1", "N", _items(1))
        m.assign("doc-a", "t1")
        m.assign("doc-b", "t1")
        m.assign("doc-c", "t1")
        assert m.clear_assignments() == 3
        assert m.template_for_doc("doc-a") is None
        assert m.template_for_doc("doc-b") is None
        assert m.template_for_doc("doc-c") is None

    def test_doesnt_remove_templates(self):
        m = _mgr()
        m.create_template("t1", "N", _items(1))
        m.assign("doc-a", "t1")
        m.clear_assignments()
        assert m.get_template("t1") is not None


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------

class TestStats:
    def test_empty(self):
        m = _mgr()
        s = m.stats()
        assert s.total_templates == 0
        assert s.total_items == 0
        assert s.avg_items_per_template == 0.0

    def test_totals(self):
        m = _mgr()
        m.create_template("t1", "A", _items(3))
        m.create_template("t2", "B", _items(5))
        s = m.stats()
        assert s.total_templates == 2
        assert s.total_items == 8
        assert s.avg_items_per_template == 4.0

    def test_avg_float(self):
        m = _mgr()
        m.create_template("t1", "A", _items(1))
        m.create_template("t2", "B", _items(2))
        m.create_template("t3", "C", _items(2))
        s = m.stats()
        assert s.total_templates == 3
        assert s.total_items == 5
        assert s.avg_items_per_template == pytest.approx(5 / 3)


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------

class TestThreadSafety:
    def test_concurrent_create_template(self):
        m = _mgr()
        N = 50

        def worker(i: int) -> None:
            m.create_template(f"t{i}", f"Name{i:03d}", _items(2))

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(N)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(m.list_templates()) == N
        s = m.stats()
        assert s.total_templates == N
        assert s.total_items == N * 2
