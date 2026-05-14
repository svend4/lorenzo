"""Tests for E396 DocViewLayout."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_view_layout import DocViewLayout, ViewLayout, ViewLayoutStats


# --------------------------------------------------------------------- dataclasses
class TestViewLayoutDataclass:
    def test_required_fields(self):
        v = ViewLayout(user_id="u", doc_id="d")
        assert v.user_id == "u"
        assert v.doc_id == "d"

    def test_default_panels(self):
        v = ViewLayout(user_id="u", doc_id="d")
        assert v.panels == []

    def test_default_column_widths(self):
        v = ViewLayout(user_id="u", doc_id="d")
        assert v.column_widths == {}

    def test_default_theme(self):
        v = ViewLayout(user_id="u", doc_id="d")
        assert v.theme == "default"

    def test_default_updated_at(self):
        v = ViewLayout(user_id="u", doc_id="d")
        assert v.updated_at == 0.0

    def test_custom_fields(self):
        v = ViewLayout(
            user_id="u",
            doc_id="d",
            panels=["a", "b"],
            column_widths={"c1": 100},
            theme="dark",
            updated_at=5.0,
        )
        assert v.panels == ["a", "b"]
        assert v.column_widths == {"c1": 100}
        assert v.theme == "dark"
        assert v.updated_at == 5.0

    def test_independent_defaults(self):
        v1 = ViewLayout(user_id="u1", doc_id="d1")
        v2 = ViewLayout(user_id="u2", doc_id="d2")
        v1.panels.append("p")
        assert v2.panels == []


class TestViewLayoutStatsDataclass:
    def test_basic(self):
        s = ViewLayoutStats(total_layouts=10, unique_users=3, unique_docs=4)
        assert s.total_layouts == 10
        assert s.unique_users == 3
        assert s.unique_docs == 4

    def test_zero(self):
        s = ViewLayoutStats(total_layouts=0, unique_users=0, unique_docs=0)
        assert s.total_layouts == 0


# --------------------------------------------------------------------- construction
class TestConstruction:
    def test_empty_after_init(self):
        dvl = DocViewLayout()
        st = dvl.stats()
        assert st.total_layouts == 0
        assert st.unique_users == 0
        assert st.unique_docs == 0

    def test_has_lock(self):
        dvl = DocViewLayout()
        assert hasattr(dvl, "_lock")


# --------------------------------------------------------------------- save_layout
class TestSaveLayout:
    def test_save_returns_layout(self):
        dvl = DocViewLayout()
        out = dvl.save_layout("u1", "d1", ["p1"], now=1.0)
        assert isinstance(out, ViewLayout)
        assert out.user_id == "u1"
        assert out.doc_id == "d1"
        assert out.panels == ["p1"]
        assert out.updated_at == 1.0

    def test_save_default_theme(self):
        dvl = DocViewLayout()
        out = dvl.save_layout("u", "d", [], now=1.0)
        assert out.theme == "default"

    def test_save_with_column_widths(self):
        dvl = DocViewLayout()
        out = dvl.save_layout("u", "d", [], column_widths={"c": 50}, now=1.0)
        assert out.column_widths == {"c": 50}

    def test_replace_existing(self):
        dvl = DocViewLayout()
        dvl.save_layout("u", "d", ["a"], now=1.0)
        dvl.save_layout("u", "d", ["b", "c"], theme="dark", now=2.0)
        layout = dvl.get_layout("u", "d")
        assert layout.panels == ["b", "c"]
        assert layout.theme == "dark"
        assert layout.updated_at == 2.0

    def test_panels_copied(self):
        dvl = DocViewLayout()
        src = ["a", "b"]
        out = dvl.save_layout("u", "d", src, now=1.0)
        src.append("c")
        assert out.panels == ["a", "b"]

    def test_column_widths_copied(self):
        dvl = DocViewLayout()
        src = {"c": 10}
        out = dvl.save_layout("u", "d", [], column_widths=src, now=1.0)
        src["c"] = 99
        assert out.column_widths == {"c": 10}


# --------------------------------------------------------------------- get_layout
class TestGetLayout:
    def test_returns_layout(self):
        dvl = DocViewLayout()
        dvl.save_layout("u", "d", ["p"], now=1.0)
        out = dvl.get_layout("u", "d")
        assert out is not None
        assert out.panels == ["p"]

    def test_missing_returns_none(self):
        dvl = DocViewLayout()
        assert dvl.get_layout("u", "d") is None

    def test_other_user_returns_none(self):
        dvl = DocViewLayout()
        dvl.save_layout("u1", "d", ["p"], now=1.0)
        assert dvl.get_layout("u2", "d") is None


# --------------------------------------------------------------------- delete_layout
class TestDeleteLayout:
    def test_delete_existing(self):
        dvl = DocViewLayout()
        dvl.save_layout("u", "d", [], now=1.0)
        assert dvl.delete_layout("u", "d") is True
        assert dvl.get_layout("u", "d") is None

    def test_delete_missing(self):
        dvl = DocViewLayout()
        assert dvl.delete_layout("u", "d") is False

    def test_delete_updates_indexes(self):
        dvl = DocViewLayout()
        dvl.save_layout("u", "d", [], now=1.0)
        dvl.delete_layout("u", "d")
        assert dvl.layouts_for_user("u") == []
        assert dvl.layouts_for_doc("d") == []

    def test_delete_keeps_others(self):
        dvl = DocViewLayout()
        dvl.save_layout("u", "d1", [], now=1.0)
        dvl.save_layout("u", "d2", [], now=1.0)
        dvl.delete_layout("u", "d1")
        assert dvl.get_layout("u", "d2") is not None


# --------------------------------------------------------------------- set_default
class TestSetDefault:
    def test_set_default(self):
        dvl = DocViewLayout()
        layout = ViewLayout(user_id="*", doc_id="d", panels=["x"])
        dvl.set_default("d", layout)
        assert dvl.get_default("d") is layout

    def test_overwrite_default(self):
        dvl = DocViewLayout()
        l1 = ViewLayout(user_id="*", doc_id="d", panels=["a"])
        l2 = ViewLayout(user_id="*", doc_id="d", panels=["b"])
        dvl.set_default("d", l1)
        dvl.set_default("d", l2)
        assert dvl.get_default("d") is l2


# --------------------------------------------------------------------- get_default
class TestGetDefault:
    def test_missing(self):
        dvl = DocViewLayout()
        assert dvl.get_default("d") is None

    def test_returns_layout(self):
        dvl = DocViewLayout()
        layout = ViewLayout(user_id="*", doc_id="d")
        dvl.set_default("d", layout)
        assert dvl.get_default("d") is layout


# --------------------------------------------------------------------- resolve
class TestResolve:
    def test_user_wins(self):
        dvl = DocViewLayout()
        default = ViewLayout(user_id="*", doc_id="d", panels=["default"])
        dvl.set_default("d", default)
        dvl.save_layout("u", "d", ["mine"], now=1.0)
        out = dvl.resolve("u", "d")
        assert out.panels == ["mine"]

    def test_default_fallback(self):
        dvl = DocViewLayout()
        default = ViewLayout(user_id="*", doc_id="d", panels=["default"])
        dvl.set_default("d", default)
        out = dvl.resolve("u", "d")
        assert out is default

    def test_neither_returns_none(self):
        dvl = DocViewLayout()
        assert dvl.resolve("u", "d") is None

    def test_user_layout_only(self):
        dvl = DocViewLayout()
        dvl.save_layout("u", "d", ["mine"], now=1.0)
        out = dvl.resolve("u", "d")
        assert out.panels == ["mine"]


# --------------------------------------------------------------------- layouts_for_user
class TestLayoutsForUser:
    def test_empty(self):
        dvl = DocViewLayout()
        assert dvl.layouts_for_user("u") == []

    def test_sorted_by_doc_id(self):
        dvl = DocViewLayout()
        dvl.save_layout("u", "d3", [], now=1.0)
        dvl.save_layout("u", "d1", [], now=1.0)
        dvl.save_layout("u", "d2", [], now=1.0)
        out = dvl.layouts_for_user("u")
        assert [l.doc_id for l in out] == ["d1", "d2", "d3"]

    def test_only_this_user(self):
        dvl = DocViewLayout()
        dvl.save_layout("u1", "d", [], now=1.0)
        dvl.save_layout("u2", "d", [], now=1.0)
        out = dvl.layouts_for_user("u1")
        assert len(out) == 1
        assert out[0].user_id == "u1"


# --------------------------------------------------------------------- layouts_for_doc
class TestLayoutsForDoc:
    def test_empty(self):
        dvl = DocViewLayout()
        assert dvl.layouts_for_doc("d") == []

    def test_sorted_by_user_id(self):
        dvl = DocViewLayout()
        dvl.save_layout("u3", "d", [], now=1.0)
        dvl.save_layout("u1", "d", [], now=1.0)
        dvl.save_layout("u2", "d", [], now=1.0)
        out = dvl.layouts_for_doc("d")
        assert [l.user_id for l in out] == ["u1", "u2", "u3"]

    def test_only_this_doc(self):
        dvl = DocViewLayout()
        dvl.save_layout("u", "d1", [], now=1.0)
        dvl.save_layout("u", "d2", [], now=1.0)
        out = dvl.layouts_for_doc("d1")
        assert len(out) == 1
        assert out[0].doc_id == "d1"


# --------------------------------------------------------------------- update_theme
class TestUpdateTheme:
    def test_update_existing(self):
        dvl = DocViewLayout()
        dvl.save_layout("u", "d", [], now=1.0)
        assert dvl.update_theme("u", "d", "dark", now=2.0) is True
        layout = dvl.get_layout("u", "d")
        assert layout.theme == "dark"
        assert layout.updated_at == 2.0

    def test_update_missing(self):
        dvl = DocViewLayout()
        assert dvl.update_theme("u", "d", "dark", now=1.0) is False

    def test_idempotent(self):
        dvl = DocViewLayout()
        dvl.save_layout("u", "d", [], theme="x", now=1.0)
        assert dvl.update_theme("u", "d", "x", now=2.0) is True


# --------------------------------------------------------------------- add_panel
class TestAddPanel:
    def test_add_new(self):
        dvl = DocViewLayout()
        dvl.save_layout("u", "d", [], now=1.0)
        assert dvl.add_panel("u", "d", "p1", now=2.0) is True
        assert dvl.get_layout("u", "d").panels == ["p1"]

    def test_duplicate_returns_false(self):
        dvl = DocViewLayout()
        dvl.save_layout("u", "d", ["p1"], now=1.0)
        assert dvl.add_panel("u", "d", "p1", now=2.0) is False

    def test_missing_layout(self):
        dvl = DocViewLayout()
        assert dvl.add_panel("u", "d", "p1", now=1.0) is False

    def test_updates_timestamp(self):
        dvl = DocViewLayout()
        dvl.save_layout("u", "d", [], now=1.0)
        dvl.add_panel("u", "d", "p1", now=5.0)
        assert dvl.get_layout("u", "d").updated_at == 5.0

    def test_append_order(self):
        dvl = DocViewLayout()
        dvl.save_layout("u", "d", ["a"], now=1.0)
        dvl.add_panel("u", "d", "b", now=2.0)
        dvl.add_panel("u", "d", "c", now=3.0)
        assert dvl.get_layout("u", "d").panels == ["a", "b", "c"]


# --------------------------------------------------------------------- remove_panel
class TestRemovePanel:
    def test_remove_existing(self):
        dvl = DocViewLayout()
        dvl.save_layout("u", "d", ["a", "b"], now=1.0)
        assert dvl.remove_panel("u", "d", "a", now=2.0) is True
        assert dvl.get_layout("u", "d").panels == ["b"]

    def test_remove_missing_panel(self):
        dvl = DocViewLayout()
        dvl.save_layout("u", "d", ["a"], now=1.0)
        assert dvl.remove_panel("u", "d", "z", now=2.0) is False

    def test_remove_missing_layout(self):
        dvl = DocViewLayout()
        assert dvl.remove_panel("u", "d", "p", now=1.0) is False

    def test_updates_timestamp(self):
        dvl = DocViewLayout()
        dvl.save_layout("u", "d", ["a"], now=1.0)
        dvl.remove_panel("u", "d", "a", now=9.0)
        assert dvl.get_layout("u", "d").updated_at == 9.0


# --------------------------------------------------------------------- set_column_width
class TestSetColumnWidth:
    def test_set_new(self):
        dvl = DocViewLayout()
        dvl.save_layout("u", "d", [], now=1.0)
        assert dvl.set_column_width("u", "d", "c1", 100.0, now=2.0) is True
        assert dvl.get_layout("u", "d").column_widths == {"c1": 100.0}

    def test_overwrite(self):
        dvl = DocViewLayout()
        dvl.save_layout("u", "d", [], column_widths={"c1": 50}, now=1.0)
        dvl.set_column_width("u", "d", "c1", 200.0, now=2.0)
        assert dvl.get_layout("u", "d").column_widths["c1"] == 200.0

    def test_missing_layout(self):
        dvl = DocViewLayout()
        assert dvl.set_column_width("u", "d", "c", 1.0, now=1.0) is False

    def test_updates_timestamp(self):
        dvl = DocViewLayout()
        dvl.save_layout("u", "d", [], now=1.0)
        dvl.set_column_width("u", "d", "c", 1.0, now=7.0)
        assert dvl.get_layout("u", "d").updated_at == 7.0


# --------------------------------------------------------------------- clear_user
class TestClearUser:
    def test_clear_count(self):
        dvl = DocViewLayout()
        dvl.save_layout("u", "d1", [], now=1.0)
        dvl.save_layout("u", "d2", [], now=1.0)
        dvl.save_layout("u", "d3", [], now=1.0)
        assert dvl.clear_user("u") == 3

    def test_clear_empty(self):
        dvl = DocViewLayout()
        assert dvl.clear_user("u") == 0

    def test_clear_removes_layouts(self):
        dvl = DocViewLayout()
        dvl.save_layout("u", "d1", [], now=1.0)
        dvl.clear_user("u")
        assert dvl.get_layout("u", "d1") is None

    def test_clear_keeps_other_users(self):
        dvl = DocViewLayout()
        dvl.save_layout("u1", "d", [], now=1.0)
        dvl.save_layout("u2", "d", [], now=1.0)
        dvl.clear_user("u1")
        assert dvl.get_layout("u2", "d") is not None

    def test_clear_updates_by_doc_index(self):
        dvl = DocViewLayout()
        dvl.save_layout("u1", "d", [], now=1.0)
        dvl.save_layout("u2", "d", [], now=1.0)
        dvl.clear_user("u1")
        assert [l.user_id for l in dvl.layouts_for_doc("d")] == ["u2"]


# --------------------------------------------------------------------- clear_doc
class TestClearDoc:
    def test_clear_count(self):
        dvl = DocViewLayout()
        dvl.save_layout("u1", "d", [], now=1.0)
        dvl.save_layout("u2", "d", [], now=1.0)
        assert dvl.clear_doc("d") == 2

    def test_clear_default_removed(self):
        dvl = DocViewLayout()
        dvl.set_default("d", ViewLayout(user_id="*", doc_id="d"))
        dvl.clear_doc("d")
        assert dvl.get_default("d") is None

    def test_clear_removes_layouts(self):
        dvl = DocViewLayout()
        dvl.save_layout("u", "d", [], now=1.0)
        dvl.clear_doc("d")
        assert dvl.get_layout("u", "d") is None

    def test_clear_empty(self):
        dvl = DocViewLayout()
        assert dvl.clear_doc("d") == 0

    def test_clear_keeps_other_docs(self):
        dvl = DocViewLayout()
        dvl.save_layout("u", "d1", [], now=1.0)
        dvl.save_layout("u", "d2", [], now=1.0)
        dvl.clear_doc("d1")
        assert dvl.get_layout("u", "d2") is not None

    def test_clear_updates_by_user_index(self):
        dvl = DocViewLayout()
        dvl.save_layout("u", "d1", [], now=1.0)
        dvl.save_layout("u", "d2", [], now=1.0)
        dvl.clear_doc("d1")
        assert [l.doc_id for l in dvl.layouts_for_user("u")] == ["d2"]


# --------------------------------------------------------------------- stats
class TestStats:
    def test_empty(self):
        dvl = DocViewLayout()
        s = dvl.stats()
        assert s.total_layouts == 0
        assert s.unique_users == 0
        assert s.unique_docs == 0

    def test_totals(self):
        dvl = DocViewLayout()
        dvl.save_layout("u1", "d1", [], now=1.0)
        dvl.save_layout("u1", "d2", [], now=1.0)
        dvl.save_layout("u2", "d1", [], now=1.0)
        s = dvl.stats()
        assert s.total_layouts == 3
        assert s.unique_users == 2
        assert s.unique_docs == 2

    def test_after_delete(self):
        dvl = DocViewLayout()
        dvl.save_layout("u", "d", [], now=1.0)
        dvl.delete_layout("u", "d")
        s = dvl.stats()
        assert s.total_layouts == 0
        assert s.unique_users == 0
        assert s.unique_docs == 0

    def test_default_not_counted(self):
        dvl = DocViewLayout()
        dvl.set_default("d", ViewLayout(user_id="*", doc_id="d"))
        s = dvl.stats()
        assert s.total_layouts == 0


# --------------------------------------------------------------------- thread safety
class TestThreadSafety:
    def test_concurrent_save_layout(self):
        dvl = DocViewLayout()
        n_threads = 16
        per_thread = 25
        errors = []

        def worker(tid):
            try:
                for i in range(per_thread):
                    dvl.save_layout(f"u{tid}", f"d{i}", ["p"], now=float(i))
            except Exception as e:  # pragma: no cover
                errors.append(e)

        threads = [threading.Thread(target=worker, args=(t,)) for t in range(n_threads)]
        for th in threads:
            th.start()
        for th in threads:
            th.join()

        assert errors == []
        s = dvl.stats()
        assert s.total_layouts == n_threads * per_thread
        assert s.unique_users == n_threads
        assert s.unique_docs == per_thread

    def test_concurrent_mixed_ops(self):
        dvl = DocViewLayout()
        for t in range(8):
            for i in range(10):
                dvl.save_layout(f"u{t}", f"d{i}", [], now=1.0)

        errors = []

        def worker(tid):
            try:
                for i in range(10):
                    dvl.add_panel(f"u{tid}", f"d{i}", "p", now=2.0)
                    dvl.update_theme(f"u{tid}", f"d{i}", "dark", now=2.0)
                    dvl.set_column_width(f"u{tid}", f"d{i}", "c", 10.0, now=2.0)
            except Exception as e:  # pragma: no cover
                errors.append(e)

        threads = [threading.Thread(target=worker, args=(t,)) for t in range(8)]
        for th in threads:
            th.start()
        for th in threads:
            th.join()

        assert errors == []
        layout = dvl.get_layout("u0", "d0")
        assert layout.theme == "dark"
        assert layout.panels == ["p"]
        assert layout.column_widths == {"c": 10.0}
