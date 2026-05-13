"""Tests for docstoolkit.audit_chain (E95)."""
import time
import pytest

from docstoolkit.audit_chain import AuditRecord, ChainStore, AuditChain


# ---------------------------------------------------------------------------
# AuditRecord
# ---------------------------------------------------------------------------

class TestAuditRecord:
    def test_defaults(self):
        r = AuditRecord()
        assert isinstance(r.record_id, str)
        assert len(r.record_id) == 12
        assert r.index == 0
        assert r.actor == ""
        assert r.action == ""
        assert r.resource == ""
        assert r.data == {}
        assert r.prev_hash == ""
        assert r.hash == ""

    def test_to_dict(self):
        r = AuditRecord(actor="alice", action="login", resource="app")
        d = r.to_dict()
        assert d["actor"] == "alice"
        assert d["action"] == "login"
        assert d["resource"] == "app"
        assert "record_id" in d
        assert "hash" in d

    def test_unique_ids(self):
        ids = {AuditRecord().record_id for _ in range(100)}
        assert len(ids) == 100

    def test_data_field(self):
        r = AuditRecord(data={"key": "value", "count": 42})
        assert r.data["key"] == "value"
        assert r.data["count"] == 42


# ---------------------------------------------------------------------------
# ChainStore
# ---------------------------------------------------------------------------

class TestChainStore:
    def test_empty_store(self):
        s = ChainStore()
        assert s.count() == 0
        assert s.latest() is None

    def test_append_and_get(self):
        s = ChainStore()
        r = AuditRecord(record_id="abc123", index=0, actor="alice",
                        action="create", resource="doc", hash="h1")
        s.append(r)
        got = s.get("abc123")
        assert got is not None
        assert got.record_id == "abc123"
        assert got.actor == "alice"
        assert got.action == "create"

    def test_get_missing(self):
        s = ChainStore()
        assert s.get("nonexistent") is None

    def test_get_by_index(self):
        s = ChainStore()
        r = AuditRecord(record_id="r0", index=0, actor="a", action="x", hash="h")
        s.append(r)
        got = s.get_by_index(0)
        assert got is not None
        assert got.record_id == "r0"

    def test_get_by_index_missing(self):
        s = ChainStore()
        assert s.get_by_index(99) is None

    def test_latest(self):
        s = ChainStore()
        r0 = AuditRecord(record_id="r0", index=0, actor="a", action="x", hash="h0")
        r1 = AuditRecord(record_id="r1", index=1, actor="b", action="y", hash="h1")
        s.append(r0)
        s.append(r1)
        latest = s.latest()
        assert latest is not None
        assert latest.record_id == "r1"

    def test_count(self):
        s = ChainStore()
        for i in range(5):
            s.append(AuditRecord(
                record_id=f"r{i}", index=i,
                actor="a", action="x", hash=f"h{i}"
            ))
        assert s.count() == 5

    def test_list_no_filter(self):
        s = ChainStore()
        for i in range(3):
            s.append(AuditRecord(
                record_id=f"r{i}", index=i,
                actor=f"actor{i}", action="read", hash=f"h{i}"
            ))
        records = s.list()
        assert len(records) == 3
        # Ordered by index
        assert records[0].index == 0
        assert records[2].index == 2

    def test_list_filter_actor(self):
        s = ChainStore()
        s.append(AuditRecord(record_id="r0", index=0, actor="alice", action="login", hash="h0"))
        s.append(AuditRecord(record_id="r1", index=1, actor="bob", action="login", hash="h1"))
        s.append(AuditRecord(record_id="r2", index=2, actor="alice", action="logout", hash="h2"))
        records = s.list(actor="alice")
        assert len(records) == 2
        assert all(r.actor == "alice" for r in records)

    def test_list_filter_action(self):
        s = ChainStore()
        s.append(AuditRecord(record_id="r0", index=0, actor="a", action="login", hash="h0"))
        s.append(AuditRecord(record_id="r1", index=1, actor="b", action="logout", hash="h1"))
        records = s.list(action="login")
        assert len(records) == 1
        assert records[0].action == "login"

    def test_list_filter_resource(self):
        s = ChainStore()
        s.append(AuditRecord(record_id="r0", index=0, actor="a",
                              action="read", resource="doc1", hash="h0"))
        s.append(AuditRecord(record_id="r1", index=1, actor="b",
                              action="write", resource="doc2", hash="h1"))
        records = s.list(resource="doc1")
        assert len(records) == 1
        assert records[0].resource == "doc1"

    def test_list_filter_combined(self):
        s = ChainStore()
        s.append(AuditRecord(record_id="r0", index=0, actor="alice",
                              action="login", resource="app", hash="h0"))
        s.append(AuditRecord(record_id="r1", index=1, actor="alice",
                              action="logout", resource="app", hash="h1"))
        records = s.list(actor="alice", action="login", resource="app")
        assert len(records) == 1

    def test_list_limit(self):
        s = ChainStore()
        for i in range(10):
            s.append(AuditRecord(record_id=f"r{i}", index=i,
                                 actor="a", action="x", hash=f"h{i}"))
        records = s.list(limit=3)
        assert len(records) == 3

    def test_data_serialized(self):
        s = ChainStore()
        data = {"k": "v", "n": 99, "nested": {"x": True}}
        s.append(AuditRecord(record_id="r0", index=0, actor="a",
                              action="x", data=data, hash="h0"))
        got = s.get("r0")
        assert got.data == data

    def test_close(self):
        s = ChainStore()
        s.close()  # Should not raise


# ---------------------------------------------------------------------------
# AuditChain
# ---------------------------------------------------------------------------

class TestAuditChain:
    def test_empty_chain(self):
        chain = AuditChain()
        assert chain.count() == 0
        assert chain.latest() is None

    def test_append_returns_record(self):
        chain = AuditChain()
        r = chain.append("alice", "login")
        assert r.actor == "alice"
        assert r.action == "login"
        assert r.index == 0
        assert r.prev_hash == ""
        assert r.hash != ""

    def test_sequential_indices(self):
        chain = AuditChain()
        r0 = chain.append("a", "x")
        r1 = chain.append("b", "y")
        r2 = chain.append("c", "z")
        assert r0.index == 0
        assert r1.index == 1
        assert r2.index == 2

    def test_hash_chain_links(self):
        chain = AuditChain()
        r0 = chain.append("a", "x")
        r1 = chain.append("b", "y")
        r2 = chain.append("c", "z")
        assert r1.prev_hash == r0.hash
        assert r2.prev_hash == r1.hash

    def test_verify_valid_chain(self):
        chain = AuditChain()
        for i in range(5):
            chain.append(f"actor{i}", f"action{i}")
        ok, bad = chain.verify()
        assert ok
        assert bad == []

    def test_verify_empty_chain(self):
        chain = AuditChain()
        ok, bad = chain.verify()
        assert ok
        assert bad == []

    def test_verify_detects_tampered_hash(self):
        store = ChainStore()
        chain = AuditChain(store)
        for i in range(3):
            chain.append(f"actor{i}", f"action{i}")

        # Tamper with index 1's hash directly in the DB
        store._conn.execute(
            "UPDATE audit_chain SET hash = 'tampered' WHERE idx = 1"
        )
        store._conn.commit()

        ok, bad = chain.verify()
        assert not ok
        assert 1 in bad

    def test_verify_detects_prev_hash_tamper(self):
        store = ChainStore()
        chain = AuditChain(store)
        for i in range(3):
            chain.append(f"actor{i}", f"action{i}")

        # Tamper with index 2's prev_hash
        store._conn.execute(
            "UPDATE audit_chain SET prev_hash = 'wrong' WHERE idx = 2"
        )
        store._conn.commit()

        ok, bad = chain.verify()
        assert not ok
        assert 2 in bad

    def test_verify_range(self):
        chain = AuditChain()
        for i in range(5):
            chain.append(f"actor{i}", f"action{i}")
        ok, bad = chain.verify_range(1, 3)
        assert ok
        assert bad == []

    def test_verify_range_partial(self):
        store = ChainStore()
        chain = AuditChain(store)
        for i in range(5):
            chain.append(f"actor{i}", f"action{i}")

        # Tamper with index 4
        store._conn.execute(
            "UPDATE audit_chain SET hash = 'bad' WHERE idx = 4"
        )
        store._conn.commit()

        # Verifying range 0-3 should be ok
        ok, bad = chain.verify_range(0, 3)
        assert ok

        # Verifying range 3-4 should detect the tamper
        ok, bad = chain.verify_range(3, 4)
        assert not ok
        assert 4 in bad

    def test_append_with_data(self):
        chain = AuditChain()
        r = chain.append("alice", "update", resource="file.txt",
                         data={"size": 1024, "type": "text"})
        assert r.resource == "file.txt"
        assert r.data["size"] == 1024

    def test_get(self):
        chain = AuditChain()
        r = chain.append("alice", "login")
        got = chain.get(r.record_id)
        assert got is not None
        assert got.record_id == r.record_id

    def test_list(self):
        chain = AuditChain()
        chain.append("alice", "login", resource="app")
        chain.append("bob", "login", resource="app")
        chain.append("alice", "logout", resource="app")
        records = chain.list(actor="alice")
        assert len(records) == 2

    def test_export(self):
        chain = AuditChain()
        chain.append("a", "x")
        chain.append("b", "y")
        exported = chain.export()
        assert len(exported) == 2
        assert isinstance(exported[0], dict)
        assert "hash" in exported[0]
        assert "actor" in exported[0]

    def test_custom_store(self):
        store = ChainStore()
        chain = AuditChain(store)
        chain.append("alice", "action")
        assert chain.count() == 1
        assert store.count() == 1

    def test_count_increments(self):
        chain = AuditChain()
        for i in range(7):
            chain.append(f"actor{i}", "action")
        assert chain.count() == 7

    def test_hashes_are_deterministic(self):
        """Same content → same hash."""
        store = ChainStore()
        chain = AuditChain(store)
        r = chain.append("alice", "login")
        recomputed = chain._compute_hash(r)
        assert recomputed == r.hash

    def test_different_actors_different_hashes(self):
        chain1 = AuditChain()
        chain2 = AuditChain()
        r1 = chain1.append("alice", "login")
        r2 = chain2.append("bob", "login")
        assert r1.hash != r2.hash

    def test_data_affects_hash(self):
        chain1 = AuditChain()
        chain2 = AuditChain()
        r1 = chain1.append("alice", "update", data={"v": 1})
        r2 = chain2.append("alice", "update", data={"v": 2})
        assert r1.hash != r2.hash

    def test_persist_across_instances(self):
        import tempfile, os
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        try:
            store1 = ChainStore(db_path)
            chain1 = AuditChain(store1)
            chain1.append("alice", "login")
            chain1.append("bob", "action")
            store1.close()

            store2 = ChainStore(db_path)
            chain2 = AuditChain(store2)
            assert chain2.count() == 2
            ok, bad = chain2.verify()
            assert ok
            store2.close()
        finally:
            os.unlink(db_path)
