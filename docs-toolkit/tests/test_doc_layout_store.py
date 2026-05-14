"""Tests for E362 DocLayoutStore module.

Run with:
    cd /home/user/lorenzo/docs-toolkit
    python -m pytest tests/test_doc_layout_store.py -q
"""
from __future__ import annotations

import threading
import uuid

import pytest

from docstoolkit.doc_layout_store import (
    DocLayout,
    DocLayoutStore,
    LayoutBlock,
    LayoutStats,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _block(block_id: str, position: int, block_type: str = "section", **props) -> LayoutBlock:
    return LayoutBlock(
        block_id=block_id,
        block_type=block_type,
        position=position,
        properties=dict(props),
    )


# ---------------------------------------------------------------------------
# TestLayoutBlockDataclass
# ---------------------------------------------------------------------------

class TestLayoutBlockDataclass:
    def test_required_fields(self):
        b = LayoutBlock(block_id="b1", block_type="header", position=0)
        assert b.block_id == "b1"
        assert b.block_type == "header"
        assert b.position == 0

    def test_default_properties_is_empty_dict(self):
        b = LayoutBlock(block_id="b1", block_type="header", position=0)
        assert b.properties == {}

    def test_explicit_properties(self):
        b = LayoutBlock(block_id="b1", block_type="image", position=1, properties={"src": "x"})
        assert b.properties == {"src": "x"}

    def test_properties_default_independent(self):
        a = LayoutBlock(block_id="a", block_type="section", position=0)
        b = LayoutBlock(block_id="b", block_type="section", position=0)
        a.properties["x"] = 1
        assert "x" not in b.properties

    def test_equality(self):
        a = LayoutBlock(block_id="x", block_type="t", position=0)
        b = LayoutBlock(block_id="x", block_type="t", position=0)
        assert a == b


# ---------------------------------------------------------------------------
# TestDocLayoutDataclass
# ---------------------------------------------------------------------------

class TestDocLayoutDataclass:
    def test_required_fields(self):
        lay = DocLayout(doc_id="d", layout_id="L1")
        assert lay.doc_id == "d"
        assert lay.layout_id == "L1"

    def test_default_name_empty(self):
        lay = DocLayout(doc_id="d", layout_id="L1")
        assert lay.name == ""

    def test_default_blocks_empty(self):
        lay = DocLayout(doc_id="d", layout_id="L1")
        assert lay.blocks == []

    def test_default_timestamps_zero(self):
        lay = DocLayout(doc_id="d", layout_id="L1")
        assert lay.created_at == 0.0
        assert lay.updated_at == 0.0

    def test_default_blocks_independent(self):
        a = DocLayout(doc_id="d1", layout_id="L1")
        b = DocLayout(doc_id="d2", layout_id="L2")
        a.blocks.append(_block("x", 0))
        assert b.blocks == []

    def test_explicit_fields(self):
        blk = _block("b1", 0)
        lay = DocLayout(
            doc_id="d", layout_id="L1", name="main", blocks=[blk],
            created_at=10.0, updated_at=20.0,
        )
        assert lay.name == "main"
        assert lay.blocks == [blk]
        assert lay.created_at == 10.0
        assert lay.updated_at == 20.0


# ---------------------------------------------------------------------------
# TestLayoutStatsDataclass
# ---------------------------------------------------------------------------

class TestLayoutStatsDataclass:
    def test_fields(self):
        s = LayoutStats(total_layouts=2, total_blocks=5, unique_docs=1)
        assert s.total_layouts == 2
        assert s.total_blocks == 5
        assert s.unique_docs == 1

    def test_equality(self):
        a = LayoutStats(1, 2, 3)
        b = LayoutStats(1, 2, 3)
        assert a == b

    def test_inequality(self):
        a = LayoutStats(1, 2, 3)
        b = LayoutStats(0, 2, 3)
        assert a != b


# ---------------------------------------------------------------------------
# TestConstruction
# ---------------------------------------------------------------------------

class TestConstruction:
    def test_empty_store(self):
        s = DocLayoutStore()
        assert s.stats() == LayoutStats(0, 0, 0)

    def test_all_doc_ids_empty(self):
        assert DocLayoutStore().all_doc_ids() == []

    def test_get_layout_missing(self):
        assert DocLayoutStore().get_layout("nope") is None


# ---------------------------------------------------------------------------
# TestCreateLayout
# ---------------------------------------------------------------------------

class TestCreateLayout:
    def test_returns_doc_layout(self):
        s = DocLayoutStore()
        lay = s.create_layout("d1")
        assert isinstance(lay, DocLayout)

    def test_doc_id_set(self):
        lay = DocLayoutStore().create_layout("doc-A")
        assert lay.doc_id == "doc-A"

    def test_layout_id_is_uuid(self):
        lay = DocLayoutStore().create_layout("d")
        # Should parse as UUID
        uuid.UUID(lay.layout_id)

    def test_layout_ids_unique(self):
        s = DocLayoutStore()
        ids = {s.create_layout("d").layout_id for _ in range(50)}
        assert len(ids) == 50

    def test_default_name_empty(self):
        lay = DocLayoutStore().create_layout("d")
        assert lay.name == ""

    def test_explicit_name(self):
        lay = DocLayoutStore().create_layout("d", name="main")
        assert lay.name == "main"

    def test_default_blocks_empty(self):
        lay = DocLayoutStore().create_layout("d")
        assert lay.blocks == []

    def test_initial_blocks_sorted(self):
        blocks = [_block("a", 5), _block("b", 1), _block("c", 3)]
        lay = DocLayoutStore().create_layout("d", blocks=blocks)
        assert [b.block_id for b in lay.blocks] == ["b", "c", "a"]

    def test_initial_blocks_copied(self):
        original = [_block("a", 0)]
        lay = DocLayoutStore().create_layout("d", blocks=original)
        original.append(_block("b", 1))
        assert len(lay.blocks) == 1

    def test_uses_now_override(self):
        lay = DocLayoutStore().create_layout("d", now=1234.5)
        assert lay.created_at == 1234.5
        assert lay.updated_at == 1234.5

    def test_default_timestamps_set(self):
        lay = DocLayoutStore().create_layout("d")
        assert lay.created_at > 0
        assert lay.updated_at == lay.created_at

    def test_stored_in_index(self):
        s = DocLayoutStore()
        lay = s.create_layout("d1")
        assert s.get_layout(lay.layout_id) is lay

    def test_indexed_by_doc(self):
        s = DocLayoutStore()
        lay = s.create_layout("d1")
        assert s.layouts_for_doc("d1") == [lay]


# ---------------------------------------------------------------------------
# TestUpdateLayout
# ---------------------------------------------------------------------------

class TestUpdateLayout:
    def test_unknown_returns_none(self):
        assert DocLayoutStore().update_layout("nope", name="x") is None

    def test_update_name(self):
        s = DocLayoutStore()
        lay = s.create_layout("d", now=1.0)
        updated = s.update_layout(lay.layout_id, name="renamed", now=2.0)
        assert updated is not None
        assert updated.name == "renamed"

    def test_update_blocks(self):
        s = DocLayoutStore()
        lay = s.create_layout("d", now=1.0)
        s.update_layout(lay.layout_id, blocks=[_block("a", 0)], now=2.0)
        assert [b.block_id for b in s.get_layout(lay.layout_id).blocks] == ["a"]

    def test_partial_update_keeps_other_fields(self):
        s = DocLayoutStore()
        lay = s.create_layout("d", name="orig", blocks=[_block("a", 0)], now=1.0)
        s.update_layout(lay.layout_id, name="new", now=2.0)
        assert lay.blocks == [_block("a", 0)]

    def test_blocks_sorted_after_update(self):
        s = DocLayoutStore()
        lay = s.create_layout("d", now=1.0)
        s.update_layout(
            lay.layout_id,
            blocks=[_block("a", 5), _block("b", 1), _block("c", 3)],
            now=2.0,
        )
        ordered = [b.block_id for b in s.get_layout(lay.layout_id).blocks]
        assert ordered == ["b", "c", "a"]

    def test_blocks_copied(self):
        s = DocLayoutStore()
        lay = s.create_layout("d", now=1.0)
        external = [_block("a", 0)]
        s.update_layout(lay.layout_id, blocks=external, now=2.0)
        external.append(_block("z", 99))
        assert len(s.get_layout(lay.layout_id).blocks) == 1

    def test_updated_at_advances(self):
        s = DocLayoutStore()
        lay = s.create_layout("d", now=1.0)
        s.update_layout(lay.layout_id, name="new", now=5.0)
        assert lay.updated_at == 5.0

    def test_no_change_does_not_advance(self):
        s = DocLayoutStore()
        lay = s.create_layout("d", name="orig", now=1.0)
        s.update_layout(lay.layout_id, name="orig", now=5.0)
        assert lay.updated_at == 1.0

    def test_none_args_do_nothing(self):
        s = DocLayoutStore()
        lay = s.create_layout("d", name="orig", now=1.0)
        s.update_layout(lay.layout_id, now=5.0)
        assert lay.name == "orig"
        assert lay.updated_at == 1.0


# ---------------------------------------------------------------------------
# TestAddBlock
# ---------------------------------------------------------------------------

class TestAddBlock:
    def test_unknown_layout_returns_false(self):
        assert DocLayoutStore().add_block("nope", _block("a", 0)) is False

    def test_known_layout_returns_true(self):
        s = DocLayoutStore()
        lay = s.create_layout("d")
        assert s.add_block(lay.layout_id, _block("a", 0)) is True

    def test_block_appended(self):
        s = DocLayoutStore()
        lay = s.create_layout("d")
        s.add_block(lay.layout_id, _block("a", 0))
        assert len(lay.blocks) == 1

    def test_blocks_sorted_by_position(self):
        s = DocLayoutStore()
        lay = s.create_layout("d")
        s.add_block(lay.layout_id, _block("a", 5))
        s.add_block(lay.layout_id, _block("b", 1))
        s.add_block(lay.layout_id, _block("c", 3))
        assert [b.block_id for b in lay.blocks] == ["b", "c", "a"]

    def test_updated_at_set(self):
        s = DocLayoutStore()
        lay = s.create_layout("d", now=1.0)
        s.add_block(lay.layout_id, _block("a", 0), now=7.0)
        assert lay.updated_at == 7.0


# ---------------------------------------------------------------------------
# TestRemoveBlock
# ---------------------------------------------------------------------------

class TestRemoveBlock:
    def test_unknown_layout_returns_false(self):
        assert DocLayoutStore().remove_block("nope", "b") is False

    def test_unknown_block_returns_false(self):
        s = DocLayoutStore()
        lay = s.create_layout("d")
        assert s.remove_block(lay.layout_id, "nope") is False

    def test_existing_block_returns_true(self):
        s = DocLayoutStore()
        lay = s.create_layout("d", blocks=[_block("a", 0)])
        assert s.remove_block(lay.layout_id, "a") is True

    def test_block_removed(self):
        s = DocLayoutStore()
        lay = s.create_layout("d", blocks=[_block("a", 0), _block("b", 1)])
        s.remove_block(lay.layout_id, "a")
        assert [b.block_id for b in lay.blocks] == ["b"]

    def test_updated_at_set_on_success(self):
        s = DocLayoutStore()
        lay = s.create_layout("d", blocks=[_block("a", 0)], now=1.0)
        s.remove_block(lay.layout_id, "a", now=9.0)
        assert lay.updated_at == 9.0

    def test_updated_at_unchanged_on_miss(self):
        s = DocLayoutStore()
        lay = s.create_layout("d", now=1.0)
        s.remove_block(lay.layout_id, "nope", now=9.0)
        assert lay.updated_at == 1.0


# ---------------------------------------------------------------------------
# TestMoveBlock
# ---------------------------------------------------------------------------

class TestMoveBlock:
    def test_unknown_layout_returns_false(self):
        assert DocLayoutStore().move_block("nope", "b", 0) is False

    def test_unknown_block_returns_false(self):
        s = DocLayoutStore()
        lay = s.create_layout("d")
        assert s.move_block(lay.layout_id, "nope", 0) is False

    def test_existing_returns_true(self):
        s = DocLayoutStore()
        lay = s.create_layout("d", blocks=[_block("a", 0)])
        assert s.move_block(lay.layout_id, "a", 10) is True

    def test_position_updated(self):
        s = DocLayoutStore()
        lay = s.create_layout("d", blocks=[_block("a", 0)])
        s.move_block(lay.layout_id, "a", 10)
        assert lay.blocks[0].position == 10

    def test_re_sorts(self):
        s = DocLayoutStore()
        lay = s.create_layout(
            "d",
            blocks=[_block("a", 0), _block("b", 1), _block("c", 2)],
        )
        s.move_block(lay.layout_id, "a", 5)
        assert [b.block_id for b in lay.blocks] == ["b", "c", "a"]

    def test_updated_at_set(self):
        s = DocLayoutStore()
        lay = s.create_layout("d", blocks=[_block("a", 0)], now=1.0)
        s.move_block(lay.layout_id, "a", 5, now=8.0)
        assert lay.updated_at == 8.0


# ---------------------------------------------------------------------------
# TestDeleteLayout
# ---------------------------------------------------------------------------

class TestDeleteLayout:
    def test_unknown_returns_false(self):
        assert DocLayoutStore().delete_layout("nope") is False

    def test_existing_returns_true(self):
        s = DocLayoutStore()
        lay = s.create_layout("d")
        assert s.delete_layout(lay.layout_id) is True

    def test_layout_gone(self):
        s = DocLayoutStore()
        lay = s.create_layout("d")
        s.delete_layout(lay.layout_id)
        assert s.get_layout(lay.layout_id) is None

    def test_doc_index_updated(self):
        s = DocLayoutStore()
        lay = s.create_layout("d1")
        s.delete_layout(lay.layout_id)
        assert s.layouts_for_doc("d1") == []

    def test_doc_dropped_when_last_layout_deleted(self):
        s = DocLayoutStore()
        lay = s.create_layout("d1")
        s.delete_layout(lay.layout_id)
        assert "d1" not in s.all_doc_ids()

    def test_other_layouts_preserved(self):
        s = DocLayoutStore()
        a = s.create_layout("d")
        b = s.create_layout("d")
        s.delete_layout(a.layout_id)
        assert s.layouts_for_doc("d") == [b]


# ---------------------------------------------------------------------------
# TestGetLayout
# ---------------------------------------------------------------------------

class TestGetLayout:
    def test_found(self):
        s = DocLayoutStore()
        lay = s.create_layout("d")
        assert s.get_layout(lay.layout_id) is lay

    def test_not_found(self):
        assert DocLayoutStore().get_layout("nope") is None


# ---------------------------------------------------------------------------
# TestLayoutsForDoc
# ---------------------------------------------------------------------------

class TestLayoutsForDoc:
    def test_empty(self):
        assert DocLayoutStore().layouts_for_doc("d") == []

    def test_only_matching_doc(self):
        s = DocLayoutStore()
        a = s.create_layout("d1", now=1.0)
        s.create_layout("d2", now=2.0)
        result = s.layouts_for_doc("d1")
        assert result == [a]

    def test_sorted_by_created_at(self):
        s = DocLayoutStore()
        c = s.create_layout("d", now=3.0)
        a = s.create_layout("d", now=1.0)
        b = s.create_layout("d", now=2.0)
        ordered = s.layouts_for_doc("d")
        assert ordered == [a, b, c]


# ---------------------------------------------------------------------------
# TestBlocksOf
# ---------------------------------------------------------------------------

class TestBlocksOf:
    def test_unknown_layout(self):
        assert DocLayoutStore().blocks_of("nope") == []

    def test_returns_blocks_sorted(self):
        s = DocLayoutStore()
        lay = s.create_layout(
            "d",
            blocks=[_block("a", 3), _block("b", 1), _block("c", 2)],
        )
        ids = [b.block_id for b in s.blocks_of(lay.layout_id)]
        assert ids == ["b", "c", "a"]

    def test_type_filter(self):
        s = DocLayoutStore()
        lay = s.create_layout(
            "d",
            blocks=[
                _block("h", 0, block_type="header"),
                _block("s1", 1, block_type="section"),
                _block("s2", 2, block_type="section"),
                _block("f", 3, block_type="footer"),
            ],
        )
        ids = [b.block_id for b in s.blocks_of(lay.layout_id, block_type="section")]
        assert ids == ["s1", "s2"]

    def test_type_filter_no_match(self):
        s = DocLayoutStore()
        lay = s.create_layout("d", blocks=[_block("a", 0, block_type="header")])
        assert s.blocks_of(lay.layout_id, block_type="footer") == []

    def test_empty_layout(self):
        s = DocLayoutStore()
        lay = s.create_layout("d")
        assert s.blocks_of(lay.layout_id) == []


# ---------------------------------------------------------------------------
# TestBlockCount
# ---------------------------------------------------------------------------

class TestBlockCount:
    def test_unknown_zero(self):
        assert DocLayoutStore().block_count("nope") == 0

    def test_empty_zero(self):
        s = DocLayoutStore()
        lay = s.create_layout("d")
        assert s.block_count(lay.layout_id) == 0

    def test_counts(self):
        s = DocLayoutStore()
        lay = s.create_layout(
            "d", blocks=[_block("a", 0), _block("b", 1), _block("c", 2)],
        )
        assert s.block_count(lay.layout_id) == 3


# ---------------------------------------------------------------------------
# TestAllDocIds
# ---------------------------------------------------------------------------

class TestAllDocIds:
    def test_empty(self):
        assert DocLayoutStore().all_doc_ids() == []

    def test_sorted(self):
        s = DocLayoutStore()
        s.create_layout("c")
        s.create_layout("a")
        s.create_layout("b")
        assert s.all_doc_ids() == ["a", "b", "c"]

    def test_unique(self):
        s = DocLayoutStore()
        s.create_layout("a")
        s.create_layout("a")
        s.create_layout("b")
        assert s.all_doc_ids() == ["a", "b"]


# ---------------------------------------------------------------------------
# TestStats
# ---------------------------------------------------------------------------

class TestStats:
    def test_empty(self):
        assert DocLayoutStore().stats() == LayoutStats(0, 0, 0)

    def test_total_layouts(self):
        s = DocLayoutStore()
        s.create_layout("d1")
        s.create_layout("d1")
        s.create_layout("d2")
        assert s.stats().total_layouts == 3

    def test_total_blocks(self):
        s = DocLayoutStore()
        l1 = s.create_layout("d1", blocks=[_block("a", 0), _block("b", 1)])
        l2 = s.create_layout("d2", blocks=[_block("c", 0)])
        assert s.stats().total_blocks == 3

    def test_unique_docs(self):
        s = DocLayoutStore()
        s.create_layout("d1")
        s.create_layout("d1")
        s.create_layout("d2")
        assert s.stats().unique_docs == 2

    def test_after_delete(self):
        s = DocLayoutStore()
        l1 = s.create_layout("d1", blocks=[_block("a", 0)])
        l2 = s.create_layout("d2")
        s.delete_layout(l1.layout_id)
        st = s.stats()
        assert st == LayoutStats(total_layouts=1, total_blocks=0, unique_docs=1)


# ---------------------------------------------------------------------------
# TestThreadSafety
# ---------------------------------------------------------------------------

class TestThreadSafety:
    def test_concurrent_create_layout(self):
        s = DocLayoutStore()
        errors: list[Exception] = []

        def worker(idx: int) -> None:
            try:
                for j in range(20):
                    s.create_layout(f"doc-{idx}", name=f"n{j}")
            except Exception as e:  # pragma: no cover - safety net
                errors.append(e)

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
        st = s.stats()
        assert st.total_layouts == 8 * 20
        assert st.unique_docs == 8

    def test_concurrent_add_and_remove(self):
        s = DocLayoutStore()
        lay = s.create_layout("d")

        def adder() -> None:
            for i in range(50):
                s.add_block(lay.layout_id, _block(f"b{i}", i))

        def remover() -> None:
            for i in range(50):
                s.remove_block(lay.layout_id, f"b{i}")

        threads = [threading.Thread(target=adder), threading.Thread(target=remover)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        # Should not raise and store should remain consistent
        assert s.get_layout(lay.layout_id) is lay
