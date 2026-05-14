"""Tests for E359 DocChangesetStore."""

from __future__ import annotations

import threading
import uuid

import pytest

from docstoolkit.doc_changeset_store import (
    Changeset,
    ChangesetEdit,
    ChangesetStats,
    DocChangesetStore,
)


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


class TestChangesetDataclass:
    def test_create_with_required_fields(self):
        cs = Changeset(changeset_id="abc", title="T", author="alice")
        assert cs.changeset_id == "abc"
        assert cs.title == "T"
        assert cs.author == "alice"

    def test_default_created_at_zero(self):
        cs = Changeset(changeset_id="x", title="T", author="a")
        assert cs.created_at == 0.0

    def test_default_status_draft(self):
        cs = Changeset(changeset_id="x", title="T", author="a")
        assert cs.status == "draft"

    def test_default_description_empty(self):
        cs = Changeset(changeset_id="x", title="T", author="a")
        assert cs.description == ""

    def test_default_submitted_at_none(self):
        cs = Changeset(changeset_id="x", title="T", author="a")
        assert cs.submitted_at is None

    def test_default_merged_at_none(self):
        cs = Changeset(changeset_id="x", title="T", author="a")
        assert cs.merged_at is None

    def test_custom_values(self):
        cs = Changeset(
            changeset_id="id1",
            title="T",
            author="a",
            created_at=123.0,
            status="submitted",
            description="desc",
            submitted_at=124.0,
            merged_at=125.0,
        )
        assert cs.created_at == 123.0
        assert cs.status == "submitted"
        assert cs.description == "desc"
        assert cs.submitted_at == 124.0
        assert cs.merged_at == 125.0


class TestChangesetEditDataclass:
    def test_create_with_required_fields(self):
        e = ChangesetEdit(edit_id=1, changeset_id="cs", doc_id="d", operation="add")
        assert e.edit_id == 1
        assert e.changeset_id == "cs"
        assert e.doc_id == "d"
        assert e.operation == "add"

    def test_default_content_empty(self):
        e = ChangesetEdit(edit_id=1, changeset_id="cs", doc_id="d", operation="add")
        assert e.content == ""

    def test_custom_content(self):
        e = ChangesetEdit(
            edit_id=2, changeset_id="cs", doc_id="d", operation="modify", content="body"
        )
        assert e.content == "body"


class TestChangesetStatsDataclass:
    def test_create(self):
        s = ChangesetStats(
            total_changesets=5,
            draft_count=2,
            submitted_count=1,
            merged_count=1,
            discarded_count=1,
            total_edits=10,
        )
        assert s.total_changesets == 5
        assert s.draft_count == 2
        assert s.submitted_count == 1
        assert s.merged_count == 1
        assert s.discarded_count == 1
        assert s.total_edits == 10


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------


class TestConstruction:
    def test_default_construction(self):
        store = DocChangesetStore()
        assert isinstance(store, DocChangesetStore)

    def test_empty_stats(self):
        store = DocChangesetStore()
        s = store.stats()
        assert s.total_changesets == 0
        assert s.total_edits == 0

    def test_independent_stores(self):
        a = DocChangesetStore()
        b = DocChangesetStore()
        a.create_changeset("T", "alice")
        assert a.stats().total_changesets == 1
        assert b.stats().total_changesets == 0


# ---------------------------------------------------------------------------
# create_changeset
# ---------------------------------------------------------------------------


class TestCreateChangeset:
    def test_returns_changeset(self):
        store = DocChangesetStore()
        cs = store.create_changeset("T", "alice")
        assert isinstance(cs, Changeset)

    def test_id_is_uuid(self):
        store = DocChangesetStore()
        cs = store.create_changeset("T", "alice")
        # Will raise ValueError if not a valid UUID
        uuid.UUID(cs.changeset_id)

    def test_unique_ids(self):
        store = DocChangesetStore()
        ids = {store.create_changeset("T", "a").changeset_id for _ in range(20)}
        assert len(ids) == 20

    def test_initial_status_draft(self):
        store = DocChangesetStore()
        cs = store.create_changeset("T", "alice")
        assert cs.status == "draft"

    def test_records_title_author(self):
        store = DocChangesetStore()
        cs = store.create_changeset("My Title", "bob", "desc")
        assert cs.title == "My Title"
        assert cs.author == "bob"
        assert cs.description == "desc"

    def test_now_used_for_created_at(self):
        store = DocChangesetStore()
        cs = store.create_changeset("T", "a", now=42.0)
        assert cs.created_at == 42.0

    def test_default_now_is_realtime(self):
        store = DocChangesetStore()
        cs = store.create_changeset("T", "a")
        assert cs.created_at > 0

    def test_stored_for_lookup(self):
        store = DocChangesetStore()
        cs = store.create_changeset("T", "a")
        assert store.get_changeset(cs.changeset_id) is cs


# ---------------------------------------------------------------------------
# add_edit
# ---------------------------------------------------------------------------


class TestAddEdit:
    def test_add_to_draft(self):
        store = DocChangesetStore()
        cs = store.create_changeset("T", "a")
        e = store.add_edit(cs.changeset_id, "doc1", "add", "hi")
        assert e is not None
        assert e.doc_id == "doc1"
        assert e.operation == "add"
        assert e.content == "hi"

    def test_returns_none_for_unknown_changeset(self):
        store = DocChangesetStore()
        assert store.add_edit("no-such", "doc", "add") is None

    def test_returns_none_for_submitted(self):
        store = DocChangesetStore()
        cs = store.create_changeset("T", "a")
        store.submit(cs.changeset_id)
        assert store.add_edit(cs.changeset_id, "doc", "add") is None

    def test_returns_none_for_merged(self):
        store = DocChangesetStore()
        cs = store.create_changeset("T", "a")
        store.submit(cs.changeset_id)
        store.merge(cs.changeset_id)
        assert store.add_edit(cs.changeset_id, "doc", "add") is None

    def test_returns_none_for_discarded(self):
        store = DocChangesetStore()
        cs = store.create_changeset("T", "a")
        store.discard(cs.changeset_id)
        assert store.add_edit(cs.changeset_id, "doc", "add") is None

    def test_returns_none_for_invalid_operation(self):
        store = DocChangesetStore()
        cs = store.create_changeset("T", "a")
        assert store.add_edit(cs.changeset_id, "doc", "bogus") is None

    def test_edit_id_starts_at_one(self):
        store = DocChangesetStore()
        cs = store.create_changeset("T", "a")
        e = store.add_edit(cs.changeset_id, "doc", "add")
        assert e.edit_id == 1

    def test_edit_id_increments(self):
        store = DocChangesetStore()
        cs = store.create_changeset("T", "a")
        ids = [store.add_edit(cs.changeset_id, "doc", "add").edit_id for _ in range(5)]
        assert ids == [1, 2, 3, 4, 5]

    def test_edit_id_increments_across_changesets(self):
        store = DocChangesetStore()
        a = store.create_changeset("A", "x")
        b = store.create_changeset("B", "y")
        e1 = store.add_edit(a.changeset_id, "d", "add")
        e2 = store.add_edit(b.changeset_id, "d", "add")
        assert e1.edit_id == 1
        assert e2.edit_id == 2

    def test_supports_all_operations(self):
        store = DocChangesetStore()
        cs = store.create_changeset("T", "a")
        for op in ("add", "modify", "delete"):
            e = store.add_edit(cs.changeset_id, "doc", op)
            assert e is not None
            assert e.operation == op


# ---------------------------------------------------------------------------
# submit
# ---------------------------------------------------------------------------


class TestSubmit:
    def test_draft_to_submitted(self):
        store = DocChangesetStore()
        cs = store.create_changeset("T", "a")
        assert store.submit(cs.changeset_id) is True
        assert store.get_changeset(cs.changeset_id).status == "submitted"

    def test_records_submitted_at(self):
        store = DocChangesetStore()
        cs = store.create_changeset("T", "a")
        store.submit(cs.changeset_id, now=100.0)
        assert store.get_changeset(cs.changeset_id).submitted_at == 100.0

    def test_false_for_unknown(self):
        store = DocChangesetStore()
        assert store.submit("missing") is False

    def test_false_for_already_submitted(self):
        store = DocChangesetStore()
        cs = store.create_changeset("T", "a")
        store.submit(cs.changeset_id)
        assert store.submit(cs.changeset_id) is False

    def test_false_for_merged(self):
        store = DocChangesetStore()
        cs = store.create_changeset("T", "a")
        store.submit(cs.changeset_id)
        store.merge(cs.changeset_id)
        assert store.submit(cs.changeset_id) is False

    def test_false_for_discarded(self):
        store = DocChangesetStore()
        cs = store.create_changeset("T", "a")
        store.discard(cs.changeset_id)
        assert store.submit(cs.changeset_id) is False


# ---------------------------------------------------------------------------
# merge
# ---------------------------------------------------------------------------


class TestMerge:
    def test_submitted_to_merged(self):
        store = DocChangesetStore()
        cs = store.create_changeset("T", "a")
        store.submit(cs.changeset_id)
        assert store.merge(cs.changeset_id) is True
        assert store.get_changeset(cs.changeset_id).status == "merged"

    def test_records_merged_at(self):
        store = DocChangesetStore()
        cs = store.create_changeset("T", "a")
        store.submit(cs.changeset_id)
        store.merge(cs.changeset_id, now=200.0)
        assert store.get_changeset(cs.changeset_id).merged_at == 200.0

    def test_false_for_unknown(self):
        store = DocChangesetStore()
        assert store.merge("missing") is False

    def test_false_for_draft(self):
        store = DocChangesetStore()
        cs = store.create_changeset("T", "a")
        assert store.merge(cs.changeset_id) is False

    def test_false_for_already_merged(self):
        store = DocChangesetStore()
        cs = store.create_changeset("T", "a")
        store.submit(cs.changeset_id)
        store.merge(cs.changeset_id)
        assert store.merge(cs.changeset_id) is False

    def test_false_for_discarded(self):
        store = DocChangesetStore()
        cs = store.create_changeset("T", "a")
        store.discard(cs.changeset_id)
        assert store.merge(cs.changeset_id) is False


# ---------------------------------------------------------------------------
# discard
# ---------------------------------------------------------------------------


class TestDiscard:
    def test_from_draft(self):
        store = DocChangesetStore()
        cs = store.create_changeset("T", "a")
        assert store.discard(cs.changeset_id) is True
        assert store.get_changeset(cs.changeset_id).status == "discarded"

    def test_from_submitted(self):
        store = DocChangesetStore()
        cs = store.create_changeset("T", "a")
        store.submit(cs.changeset_id)
        assert store.discard(cs.changeset_id) is True
        assert store.get_changeset(cs.changeset_id).status == "discarded"

    def test_false_for_unknown(self):
        store = DocChangesetStore()
        assert store.discard("missing") is False

    def test_false_for_merged(self):
        store = DocChangesetStore()
        cs = store.create_changeset("T", "a")
        store.submit(cs.changeset_id)
        store.merge(cs.changeset_id)
        assert store.discard(cs.changeset_id) is False

    def test_false_for_already_discarded(self):
        store = DocChangesetStore()
        cs = store.create_changeset("T", "a")
        store.discard(cs.changeset_id)
        assert store.discard(cs.changeset_id) is False


# ---------------------------------------------------------------------------
# get_changeset / get_edit
# ---------------------------------------------------------------------------


class TestGetChangeset:
    def test_found(self):
        store = DocChangesetStore()
        cs = store.create_changeset("T", "a")
        assert store.get_changeset(cs.changeset_id) is cs

    def test_not_found(self):
        store = DocChangesetStore()
        assert store.get_changeset("missing") is None


class TestGetEdit:
    def test_found(self):
        store = DocChangesetStore()
        cs = store.create_changeset("T", "a")
        e = store.add_edit(cs.changeset_id, "doc", "add")
        assert store.get_edit(e.edit_id) is e

    def test_not_found(self):
        store = DocChangesetStore()
        assert store.get_edit(999) is None


# ---------------------------------------------------------------------------
# edits_for_changeset
# ---------------------------------------------------------------------------


class TestEditsForChangeset:
    def test_empty_for_no_edits(self):
        store = DocChangesetStore()
        cs = store.create_changeset("T", "a")
        assert store.edits_for_changeset(cs.changeset_id) == []

    def test_empty_for_unknown(self):
        store = DocChangesetStore()
        assert store.edits_for_changeset("missing") == []

    def test_returns_all_edits(self):
        store = DocChangesetStore()
        cs = store.create_changeset("T", "a")
        store.add_edit(cs.changeset_id, "d1", "add")
        store.add_edit(cs.changeset_id, "d2", "modify")
        assert len(store.edits_for_changeset(cs.changeset_id)) == 2

    def test_sorted_by_edit_id(self):
        store = DocChangesetStore()
        cs = store.create_changeset("T", "a")
        for i in range(5):
            store.add_edit(cs.changeset_id, f"d{i}", "add")
        edits = store.edits_for_changeset(cs.changeset_id)
        assert [e.edit_id for e in edits] == sorted(e.edit_id for e in edits)

    def test_isolated_per_changeset(self):
        store = DocChangesetStore()
        a = store.create_changeset("A", "x")
        b = store.create_changeset("B", "y")
        store.add_edit(a.changeset_id, "d", "add")
        store.add_edit(b.changeset_id, "d", "modify")
        assert len(store.edits_for_changeset(a.changeset_id)) == 1
        assert len(store.edits_for_changeset(b.changeset_id)) == 1


# ---------------------------------------------------------------------------
# changesets_by_status
# ---------------------------------------------------------------------------


class TestChangesetsByStatus:
    def test_filters_drafts(self):
        store = DocChangesetStore()
        c1 = store.create_changeset("A", "x", now=1.0)
        c2 = store.create_changeset("B", "x", now=2.0)
        store.submit(c2.changeset_id)
        result = store.changesets_by_status("draft")
        assert [c.changeset_id for c in result] == [c1.changeset_id]

    def test_filters_submitted(self):
        store = DocChangesetStore()
        c = store.create_changeset("A", "x")
        store.submit(c.changeset_id)
        assert len(store.changesets_by_status("submitted")) == 1

    def test_filters_merged(self):
        store = DocChangesetStore()
        c = store.create_changeset("A", "x")
        store.submit(c.changeset_id)
        store.merge(c.changeset_id)
        assert len(store.changesets_by_status("merged")) == 1

    def test_filters_discarded(self):
        store = DocChangesetStore()
        c = store.create_changeset("A", "x")
        store.discard(c.changeset_id)
        assert len(store.changesets_by_status("discarded")) == 1

    def test_empty_for_unmatched(self):
        store = DocChangesetStore()
        store.create_changeset("A", "x")
        assert store.changesets_by_status("merged") == []

    def test_sorted_by_created_at(self):
        store = DocChangesetStore()
        a = store.create_changeset("A", "x", now=3.0)
        b = store.create_changeset("B", "x", now=1.0)
        c = store.create_changeset("C", "x", now=2.0)
        result = store.changesets_by_status("draft")
        assert [r.changeset_id for r in result] == [b.changeset_id, c.changeset_id, a.changeset_id]


# ---------------------------------------------------------------------------
# changesets_by_author
# ---------------------------------------------------------------------------


class TestChangesetsByAuthor:
    def test_filters_by_author(self):
        store = DocChangesetStore()
        store.create_changeset("A", "alice")
        store.create_changeset("B", "bob")
        store.create_changeset("C", "alice")
        result = store.changesets_by_author("alice")
        assert len(result) == 2
        assert all(c.author == "alice" for c in result)

    def test_empty_for_unknown(self):
        store = DocChangesetStore()
        store.create_changeset("A", "alice")
        assert store.changesets_by_author("nobody") == []

    def test_sorted_by_created_at(self):
        store = DocChangesetStore()
        a = store.create_changeset("A", "alice", now=3.0)
        b = store.create_changeset("B", "alice", now=1.0)
        result = store.changesets_by_author("alice")
        assert [r.changeset_id for r in result] == [b.changeset_id, a.changeset_id]


# ---------------------------------------------------------------------------
# changesets_for_doc
# ---------------------------------------------------------------------------


class TestChangesetsForDoc:
    def test_empty_when_no_edits(self):
        store = DocChangesetStore()
        assert store.changesets_for_doc("doc1") == []

    def test_finds_changeset_with_edit(self):
        store = DocChangesetStore()
        cs = store.create_changeset("T", "a")
        store.add_edit(cs.changeset_id, "doc1", "add")
        result = store.changesets_for_doc("doc1")
        assert len(result) == 1
        assert result[0].changeset_id == cs.changeset_id

    def test_deduplicates_multiple_edits(self):
        store = DocChangesetStore()
        cs = store.create_changeset("T", "a")
        store.add_edit(cs.changeset_id, "doc1", "add")
        store.add_edit(cs.changeset_id, "doc1", "modify")
        store.add_edit(cs.changeset_id, "doc1", "delete")
        result = store.changesets_for_doc("doc1")
        assert len(result) == 1

    def test_excludes_other_docs(self):
        store = DocChangesetStore()
        cs = store.create_changeset("T", "a")
        store.add_edit(cs.changeset_id, "doc1", "add")
        assert store.changesets_for_doc("doc2") == []

    def test_sorted_by_created_at(self):
        store = DocChangesetStore()
        a = store.create_changeset("A", "x", now=3.0)
        b = store.create_changeset("B", "x", now=1.0)
        c = store.create_changeset("C", "x", now=2.0)
        store.add_edit(a.changeset_id, "doc", "add")
        store.add_edit(b.changeset_id, "doc", "add")
        store.add_edit(c.changeset_id, "doc", "add")
        result = store.changesets_for_doc("doc")
        assert [r.changeset_id for r in result] == [b.changeset_id, c.changeset_id, a.changeset_id]


# ---------------------------------------------------------------------------
# delete_changeset
# ---------------------------------------------------------------------------


class TestDeleteChangeset:
    def test_returns_true_when_deleted(self):
        store = DocChangesetStore()
        cs = store.create_changeset("T", "a")
        assert store.delete_changeset(cs.changeset_id) is True

    def test_returns_false_for_unknown(self):
        store = DocChangesetStore()
        assert store.delete_changeset("missing") is False

    def test_removes_from_lookup(self):
        store = DocChangesetStore()
        cs = store.create_changeset("T", "a")
        store.delete_changeset(cs.changeset_id)
        assert store.get_changeset(cs.changeset_id) is None

    def test_deletes_associated_edits(self):
        store = DocChangesetStore()
        cs = store.create_changeset("T", "a")
        e1 = store.add_edit(cs.changeset_id, "d", "add")
        e2 = store.add_edit(cs.changeset_id, "d", "modify")
        store.delete_changeset(cs.changeset_id)
        assert store.get_edit(e1.edit_id) is None
        assert store.get_edit(e2.edit_id) is None

    def test_does_not_affect_other_changesets(self):
        store = DocChangesetStore()
        a = store.create_changeset("A", "x")
        b = store.create_changeset("B", "y")
        eb = store.add_edit(b.changeset_id, "d", "add")
        store.delete_changeset(a.changeset_id)
        assert store.get_changeset(b.changeset_id) is b
        assert store.get_edit(eb.edit_id) is eb


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------


class TestStats:
    def test_empty(self):
        store = DocChangesetStore()
        s = store.stats()
        assert s.total_changesets == 0
        assert s.draft_count == 0
        assert s.submitted_count == 0
        assert s.merged_count == 0
        assert s.discarded_count == 0
        assert s.total_edits == 0

    def test_counts_by_status(self):
        store = DocChangesetStore()
        d = store.create_changeset("D", "a")
        s_cs = store.create_changeset("S", "a")
        store.submit(s_cs.changeset_id)
        m = store.create_changeset("M", "a")
        store.submit(m.changeset_id)
        store.merge(m.changeset_id)
        x = store.create_changeset("X", "a")
        store.discard(x.changeset_id)
        s = store.stats()
        assert s.total_changesets == 4
        assert s.draft_count == 1
        assert s.submitted_count == 1
        assert s.merged_count == 1
        assert s.discarded_count == 1
        # silence unused
        _ = d

    def test_total_edits(self):
        store = DocChangesetStore()
        cs = store.create_changeset("T", "a")
        for _ in range(3):
            store.add_edit(cs.changeset_id, "d", "add")
        assert store.stats().total_edits == 3

    def test_total_edits_decreases_on_delete(self):
        store = DocChangesetStore()
        cs = store.create_changeset("T", "a")
        store.add_edit(cs.changeset_id, "d", "add")
        store.add_edit(cs.changeset_id, "d", "modify")
        assert store.stats().total_edits == 2
        store.delete_changeset(cs.changeset_id)
        assert store.stats().total_edits == 0


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------


class TestThreadSafety:
    def test_concurrent_create_changeset(self):
        store = DocChangesetStore()
        N = 50
        ids: list[str] = []
        lock = threading.Lock()

        def worker(i: int):
            cs = store.create_changeset(f"T{i}", "a")
            with lock:
                ids.append(cs.changeset_id)

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(N)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(ids) == N
        assert len(set(ids)) == N
        assert store.stats().total_changesets == N

    def test_concurrent_add_edit_unique_ids(self):
        store = DocChangesetStore()
        cs = store.create_changeset("T", "a")
        N = 50
        edit_ids: list[int] = []
        lock = threading.Lock()

        def worker(i: int):
            e = store.add_edit(cs.changeset_id, f"d{i}", "add")
            with lock:
                edit_ids.append(e.edit_id)

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(N)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(edit_ids) == N
        assert len(set(edit_ids)) == N
