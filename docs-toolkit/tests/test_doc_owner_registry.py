"""Tests for E391 DocOwnerRegistry."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_owner_registry import (
    DocOwnerRegistry,
    Ownership,
    OwnershipStats,
)


class TestOwnershipDataclass:
    def test_minimal_construction(self):
        o = Ownership(doc_id="d1", owner="alice")
        assert o.doc_id == "d1"
        assert o.owner == "alice"
        assert o.co_owners == []
        assert o.assigned_at == 0.0
        assert o.transferred_from is None

    def test_full_construction(self):
        o = Ownership(
            doc_id="d1",
            owner="alice",
            co_owners=["bob", "carol"],
            assigned_at=123.4,
            transferred_from="zach",
        )
        assert o.co_owners == ["bob", "carol"]
        assert o.assigned_at == 123.4
        assert o.transferred_from == "zach"

    def test_co_owners_default_is_independent(self):
        a = Ownership(doc_id="d1", owner="alice")
        b = Ownership(doc_id="d2", owner="bob")
        a.co_owners.append("x")
        assert b.co_owners == []

    def test_equality(self):
        a = Ownership(doc_id="d", owner="u")
        b = Ownership(doc_id="d", owner="u")
        assert a == b


class TestOwnershipStatsDataclass:
    def test_construction(self):
        s = OwnershipStats(
            total_docs=3, unique_owners=2, total_co_owners=4, transferred_count=1
        )
        assert s.total_docs == 3
        assert s.unique_owners == 2
        assert s.total_co_owners == 4
        assert s.transferred_count == 1

    def test_equality(self):
        a = OwnershipStats(1, 1, 0, 0)
        b = OwnershipStats(1, 1, 0, 0)
        assert a == b


class TestConstruction:
    def test_empty_registry(self):
        r = DocOwnerRegistry()
        assert r.all_doc_ids() == []
        s = r.stats()
        assert s.total_docs == 0
        assert s.unique_owners == 0

    def test_multiple_instances_independent(self):
        r1 = DocOwnerRegistry()
        r2 = DocOwnerRegistry()
        r1.set_owner("d1", "alice")
        assert r2.owner_of("d1") is None


class TestSetOwner:
    def test_new_owner_returns_record(self):
        r = DocOwnerRegistry()
        rec = r.set_owner("d1", "alice", now=100.0)
        assert rec.doc_id == "d1"
        assert rec.owner == "alice"
        assert rec.assigned_at == 100.0
        assert rec.transferred_from is None
        assert rec.co_owners == []

    def test_set_owner_uses_default_now(self):
        r = DocOwnerRegistry()
        rec = r.set_owner("d1", "alice")
        assert rec.assigned_at > 0.0

    def test_replace_owner_sets_transferred_from(self):
        r = DocOwnerRegistry()
        r.set_owner("d1", "alice", now=10.0)
        rec = r.set_owner("d1", "bob", now=20.0)
        assert rec.owner == "bob"
        assert rec.transferred_from == "alice"
        assert rec.assigned_at == 20.0

    def test_replace_with_same_owner_no_transfer(self):
        r = DocOwnerRegistry()
        r.set_owner("d1", "alice", now=10.0)
        rec = r.set_owner("d1", "alice", now=20.0)
        assert rec.transferred_from is None

    def test_replace_preserves_co_owners(self):
        r = DocOwnerRegistry()
        r.set_owner("d1", "alice")
        r.add_co_owner("d1", "bob")
        r.add_co_owner("d1", "carol")
        rec = r.set_owner("d1", "dan")
        assert "bob" in rec.co_owners
        assert "carol" in rec.co_owners

    def test_replace_removes_from_old_owner_index(self):
        r = DocOwnerRegistry()
        r.set_owner("d1", "alice")
        r.set_owner("d1", "bob")
        assert r.docs_owned_by("alice") == []
        assert r.docs_owned_by("bob") == ["d1"]

    def test_promote_co_owner_to_primary(self):
        r = DocOwnerRegistry()
        r.set_owner("d1", "alice")
        r.add_co_owner("d1", "bob")
        rec = r.set_owner("d1", "bob")
        assert rec.owner == "bob"
        assert "bob" not in rec.co_owners
        assert r.docs_with_co_owner("bob") == []


class TestTransferOwner:
    def test_unknown_doc_returns_none(self):
        r = DocOwnerRegistry()
        assert r.transfer_owner("missing", "alice") is None

    def test_transfer_sets_transferred_from(self):
        r = DocOwnerRegistry()
        r.set_owner("d1", "alice")
        rec = r.transfer_owner("d1", "bob")
        assert rec is not None
        assert rec.owner == "bob"
        assert rec.transferred_from == "alice"

    def test_transfer_uses_now_value(self):
        r = DocOwnerRegistry()
        r.set_owner("d1", "alice", now=10.0)
        rec = r.transfer_owner("d1", "bob", now=50.0)
        assert rec is not None
        assert rec.assigned_at == 50.0


class TestAddCoOwner:
    def test_add_to_new_doc_returns_false(self):
        r = DocOwnerRegistry()
        assert r.add_co_owner("d1", "alice") is False

    def test_add_new_co_owner(self):
        r = DocOwnerRegistry()
        r.set_owner("d1", "alice")
        assert r.add_co_owner("d1", "bob") is True
        rec = r.get_ownership("d1")
        assert rec is not None and "bob" in rec.co_owners

    def test_add_duplicate_returns_false(self):
        r = DocOwnerRegistry()
        r.set_owner("d1", "alice")
        r.add_co_owner("d1", "bob")
        assert r.add_co_owner("d1", "bob") is False

    def test_add_primary_owner_blocked(self):
        r = DocOwnerRegistry()
        r.set_owner("d1", "alice")
        assert r.add_co_owner("d1", "alice") is False

    def test_co_owner_index_updated(self):
        r = DocOwnerRegistry()
        r.set_owner("d1", "alice")
        r.add_co_owner("d1", "bob")
        assert r.docs_with_co_owner("bob") == ["d1"]


class TestRemoveCoOwner:
    def test_remove_unknown_doc(self):
        r = DocOwnerRegistry()
        assert r.remove_co_owner("d1", "bob") is False

    def test_remove_non_co_owner(self):
        r = DocOwnerRegistry()
        r.set_owner("d1", "alice")
        assert r.remove_co_owner("d1", "bob") is False

    def test_remove_existing(self):
        r = DocOwnerRegistry()
        r.set_owner("d1", "alice")
        r.add_co_owner("d1", "bob")
        assert r.remove_co_owner("d1", "bob") is True
        rec = r.get_ownership("d1")
        assert rec is not None and "bob" not in rec.co_owners

    def test_remove_updates_index(self):
        r = DocOwnerRegistry()
        r.set_owner("d1", "alice")
        r.add_co_owner("d1", "bob")
        r.remove_co_owner("d1", "bob")
        assert r.docs_with_co_owner("bob") == []


class TestRemoveOwner:
    def test_remove_unknown(self):
        r = DocOwnerRegistry()
        assert r.remove_owner("d1") is False

    def test_remove_existing(self):
        r = DocOwnerRegistry()
        r.set_owner("d1", "alice")
        assert r.remove_owner("d1") is True
        assert r.owner_of("d1") is None

    def test_remove_cleans_indexes(self):
        r = DocOwnerRegistry()
        r.set_owner("d1", "alice")
        r.add_co_owner("d1", "bob")
        r.remove_owner("d1")
        assert r.docs_owned_by("alice") == []
        assert r.docs_with_co_owner("bob") == []


class TestGetOwnership:
    def test_unknown(self):
        r = DocOwnerRegistry()
        assert r.get_ownership("missing") is None

    def test_existing(self):
        r = DocOwnerRegistry()
        r.set_owner("d1", "alice")
        rec = r.get_ownership("d1")
        assert rec is not None and rec.owner == "alice"


class TestOwnerOf:
    def test_unknown(self):
        r = DocOwnerRegistry()
        assert r.owner_of("d1") is None

    def test_existing(self):
        r = DocOwnerRegistry()
        r.set_owner("d1", "alice")
        assert r.owner_of("d1") == "alice"

    def test_after_transfer(self):
        r = DocOwnerRegistry()
        r.set_owner("d1", "alice")
        r.transfer_owner("d1", "bob")
        assert r.owner_of("d1") == "bob"


class TestDocsOwnedBy:
    def test_empty(self):
        r = DocOwnerRegistry()
        assert r.docs_owned_by("alice") == []

    def test_sorted(self):
        r = DocOwnerRegistry()
        r.set_owner("doc_z", "alice")
        r.set_owner("doc_a", "alice")
        r.set_owner("doc_m", "alice")
        assert r.docs_owned_by("alice") == ["doc_a", "doc_m", "doc_z"]

    def test_primary_only_not_co_owner(self):
        r = DocOwnerRegistry()
        r.set_owner("d1", "alice")
        r.set_owner("d2", "bob")
        r.add_co_owner("d2", "alice")
        assert r.docs_owned_by("alice") == ["d1"]


class TestDocsWithCoOwner:
    def test_empty(self):
        r = DocOwnerRegistry()
        assert r.docs_with_co_owner("bob") == []

    def test_sorted(self):
        r = DocOwnerRegistry()
        r.set_owner("doc_z", "alice")
        r.set_owner("doc_a", "alice")
        r.set_owner("doc_m", "alice")
        r.add_co_owner("doc_z", "bob")
        r.add_co_owner("doc_a", "bob")
        r.add_co_owner("doc_m", "bob")
        assert r.docs_with_co_owner("bob") == ["doc_a", "doc_m", "doc_z"]

    def test_only_co_owner_role(self):
        r = DocOwnerRegistry()
        r.set_owner("d1", "alice")
        r.set_owner("d2", "bob")
        r.add_co_owner("d2", "alice")
        assert r.docs_with_co_owner("alice") == ["d2"]


class TestDocsAccessibleBy:
    def test_empty(self):
        r = DocOwnerRegistry()
        assert r.docs_accessible_by("alice") == []

    def test_union_primary_and_co_owner(self):
        r = DocOwnerRegistry()
        r.set_owner("d1", "alice")
        r.set_owner("d2", "bob")
        r.add_co_owner("d2", "alice")
        assert r.docs_accessible_by("alice") == ["d1", "d2"]

    def test_sorted(self):
        r = DocOwnerRegistry()
        r.set_owner("doc_z", "alice")
        r.set_owner("doc_m", "bob")
        r.add_co_owner("doc_m", "alice")
        r.set_owner("doc_a", "carol")
        r.add_co_owner("doc_a", "alice")
        assert r.docs_accessible_by("alice") == ["doc_a", "doc_m", "doc_z"]

    def test_dedup(self):
        # A user cannot be both primary and co-owner, so set is naturally unique
        r = DocOwnerRegistry()
        r.set_owner("d1", "alice")
        result = r.docs_accessible_by("alice")
        assert result.count("d1") == 1


class TestIsOwner:
    def test_unknown_doc(self):
        r = DocOwnerRegistry()
        assert r.is_owner("alice", "d1") is False

    def test_true(self):
        r = DocOwnerRegistry()
        r.set_owner("d1", "alice")
        assert r.is_owner("alice", "d1") is True

    def test_false_for_co_owner(self):
        r = DocOwnerRegistry()
        r.set_owner("d1", "alice")
        r.add_co_owner("d1", "bob")
        assert r.is_owner("bob", "d1") is False


class TestIsCoOwner:
    def test_unknown_doc(self):
        r = DocOwnerRegistry()
        assert r.is_co_owner("alice", "d1") is False

    def test_true(self):
        r = DocOwnerRegistry()
        r.set_owner("d1", "alice")
        r.add_co_owner("d1", "bob")
        assert r.is_co_owner("bob", "d1") is True

    def test_false_for_primary(self):
        r = DocOwnerRegistry()
        r.set_owner("d1", "alice")
        assert r.is_co_owner("alice", "d1") is False

    def test_false_for_stranger(self):
        r = DocOwnerRegistry()
        r.set_owner("d1", "alice")
        assert r.is_co_owner("carol", "d1") is False


class TestIsAuthorized:
    def test_unknown_doc(self):
        r = DocOwnerRegistry()
        assert r.is_authorized("alice", "d1") is False

    def test_primary_owner(self):
        r = DocOwnerRegistry()
        r.set_owner("d1", "alice")
        assert r.is_authorized("alice", "d1") is True

    def test_co_owner(self):
        r = DocOwnerRegistry()
        r.set_owner("d1", "alice")
        r.add_co_owner("d1", "bob")
        assert r.is_authorized("bob", "d1") is True

    def test_stranger(self):
        r = DocOwnerRegistry()
        r.set_owner("d1", "alice")
        assert r.is_authorized("carol", "d1") is False


class TestTransferHistoryCount:
    def test_empty(self):
        r = DocOwnerRegistry()
        assert r.transfer_history_count() == 0

    def test_no_transfers(self):
        r = DocOwnerRegistry()
        r.set_owner("d1", "alice")
        r.set_owner("d2", "bob")
        assert r.transfer_history_count() == 0

    def test_with_transfers(self):
        r = DocOwnerRegistry()
        r.set_owner("d1", "alice")
        r.set_owner("d2", "bob")
        r.transfer_owner("d1", "carol")
        r.transfer_owner("d2", "dan")
        assert r.transfer_history_count() == 2


class TestAllDocIds:
    def test_empty(self):
        r = DocOwnerRegistry()
        assert r.all_doc_ids() == []

    def test_sorted(self):
        r = DocOwnerRegistry()
        r.set_owner("doc_z", "alice")
        r.set_owner("doc_a", "alice")
        r.set_owner("doc_m", "bob")
        assert r.all_doc_ids() == ["doc_a", "doc_m", "doc_z"]


class TestStats:
    def test_empty(self):
        r = DocOwnerRegistry()
        s = r.stats()
        assert s == OwnershipStats(0, 0, 0, 0)

    def test_total_docs(self):
        r = DocOwnerRegistry()
        r.set_owner("d1", "alice")
        r.set_owner("d2", "bob")
        assert r.stats().total_docs == 2

    def test_unique_owners(self):
        r = DocOwnerRegistry()
        r.set_owner("d1", "alice")
        r.set_owner("d2", "alice")
        r.set_owner("d3", "bob")
        assert r.stats().unique_owners == 2

    def test_total_co_owners(self):
        r = DocOwnerRegistry()
        r.set_owner("d1", "alice")
        r.add_co_owner("d1", "bob")
        r.add_co_owner("d1", "carol")
        r.set_owner("d2", "alice")
        r.add_co_owner("d2", "bob")
        assert r.stats().total_co_owners == 3

    def test_transferred_count(self):
        r = DocOwnerRegistry()
        r.set_owner("d1", "alice")
        r.set_owner("d2", "bob")
        r.transfer_owner("d1", "carol")
        assert r.stats().transferred_count == 1


class TestThreadSafety:
    def test_concurrent_set_owner(self):
        r = DocOwnerRegistry()

        def worker(start: int, count: int):
            for i in range(start, start + count):
                r.set_owner(f"doc_{i}", f"user_{i % 10}")

        threads = [
            threading.Thread(target=worker, args=(i * 100, 100)) for i in range(8)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(r.all_doc_ids()) == 800

    def test_concurrent_co_owner_ops(self):
        r = DocOwnerRegistry()
        r.set_owner("d1", "alice")

        def add_workers(start: int, count: int):
            for i in range(start, start + count):
                r.add_co_owner("d1", f"user_{i}")

        threads = [
            threading.Thread(target=add_workers, args=(i * 50, 50)) for i in range(8)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        rec = r.get_ownership("d1")
        assert rec is not None
        assert len(rec.co_owners) == 400

    def test_concurrent_transfer(self):
        r = DocOwnerRegistry()
        for i in range(20):
            r.set_owner(f"doc_{i}", "alice")

        def transfer_workers(start: int, count: int):
            for i in range(start, start + count):
                doc = f"doc_{i % 20}"
                r.transfer_owner(doc, f"user_{i}")

        threads = [
            threading.Thread(target=transfer_workers, args=(i * 50, 50))
            for i in range(4)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Final state: all docs should exist and have an owner
        assert len(r.all_doc_ids()) == 20
        for i in range(20):
            assert r.owner_of(f"doc_{i}") is not None
