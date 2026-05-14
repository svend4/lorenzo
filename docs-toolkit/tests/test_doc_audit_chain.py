"""Tests for E230 DocAuditChain."""
from __future__ import annotations

import hashlib
import json

import pytest

from docstoolkit.doc_audit_chain import (
    AuditEntry,
    DocAuditChain,
    Proof,
    VerificationResult,
)


# ---------------------------------------------------------------------------
# AuditEntry
# ---------------------------------------------------------------------------


class TestAuditEntry:
    def test_create(self):
        e = AuditEntry(
            entry_id=1,
            doc_id="d1",
            action="create",
            actor="alice",
            payload={"k": "v"},
            timestamp=1.0,
            prev_hash="p",
            entry_hash="h",
        )
        assert e.entry_id == 1
        assert e.doc_id == "d1"
        assert e.action == "create"
        assert e.actor == "alice"
        assert e.payload == {"k": "v"}
        assert e.timestamp == 1.0
        assert e.prev_hash == "p"
        assert e.entry_hash == "h"

    def test_to_dict(self):
        e = AuditEntry(1, "d", "a", "u", {}, 0.0, "p", "h")
        d = e.to_dict()
        assert d["entry_id"] == 1
        assert d["doc_id"] == "d"
        assert d["prev_hash"] == "p"
        assert d["entry_hash"] == "h"

    def test_equality(self):
        a = AuditEntry(1, "d", "a", "u", {}, 0.0, "p", "h")
        b = AuditEntry(1, "d", "a", "u", {}, 0.0, "p", "h")
        assert a == b


# ---------------------------------------------------------------------------
# VerificationResult
# ---------------------------------------------------------------------------


class TestVerificationResult:
    def test_valid(self):
        r = VerificationResult(
            valid=True, total_entries=3, verified_count=3, first_invalid_id=None
        )
        assert r.valid is True
        assert r.verified_count == 3
        assert r.error is None

    def test_invalid_with_error(self):
        r = VerificationResult(
            valid=False,
            total_entries=3,
            verified_count=1,
            first_invalid_id=2,
            error="prev_hash mismatch",
        )
        assert r.valid is False
        assert r.first_invalid_id == 2
        assert "mismatch" in r.error

    def test_to_dict(self):
        r = VerificationResult(True, 1, 1, None)
        d = r.to_dict()
        assert d["valid"] is True
        assert d["total_entries"] == 1


# ---------------------------------------------------------------------------
# Proof (data class)
# ---------------------------------------------------------------------------


class TestProofDataclass:
    def test_create(self):
        p = Proof(
            entry_id=2,
            entry_hash="abc",
            prev_hash="def",
            position=2,
            total_entries=5,
        )
        assert p.entry_id == 2
        assert p.position == 2
        assert p.total_entries == 5

    def test_to_dict(self):
        p = Proof(1, "h", "p", 1, 1)
        d = p.to_dict()
        assert d["entry_id"] == 1
        assert d["entry_hash"] == "h"


# ---------------------------------------------------------------------------
# Append
# ---------------------------------------------------------------------------


class TestAppend:
    def test_first_entry(self):
        c = DocAuditChain(genesis_seed="seed")
        e = c.append("d1", "create", "alice", {"x": 1}, now=10.0)
        assert e.entry_id == 1
        assert e.doc_id == "d1"
        assert e.action == "create"
        assert e.actor == "alice"
        assert e.payload == {"x": 1}
        assert e.timestamp == 10.0

    def test_first_prev_hash_is_genesis(self):
        c = DocAuditChain(genesis_seed="seed")
        e = c.append("d1", "create", "alice", {})
        expected = hashlib.sha256(b"seed").hexdigest()
        assert e.prev_hash == expected

    def test_chained_prev_hash(self):
        c = DocAuditChain()
        a = c.append("d1", "create", "alice", {})
        b = c.append("d1", "update", "alice", {})
        assert b.prev_hash == a.entry_hash

    def test_entry_id_monotonic(self):
        c = DocAuditChain()
        ids = [c.append("d", "a", "u").entry_id for _ in range(5)]
        assert ids == [1, 2, 3, 4, 5]

    def test_default_payload_empty(self):
        c = DocAuditChain()
        e = c.append("d", "a", "u")
        assert e.payload == {}

    def test_entry_hash_set(self):
        c = DocAuditChain()
        e = c.append("d", "a", "u")
        assert isinstance(e.entry_hash, str)
        assert len(e.entry_hash) == 64

    def test_payload_copied(self):
        c = DocAuditChain()
        payload = {"k": "v"}
        e = c.append("d", "a", "u", payload)
        payload["k"] = "changed"
        assert e.payload == {"k": "v"}


# ---------------------------------------------------------------------------
# Get
# ---------------------------------------------------------------------------


class TestGet:
    def test_get_existing(self):
        c = DocAuditChain()
        e = c.append("d", "a", "u")
        got = c.get(e.entry_id)
        assert got == e

    def test_get_missing_returns_none(self):
        c = DocAuditChain()
        assert c.get(1) is None

    def test_get_out_of_range(self):
        c = DocAuditChain()
        c.append("d", "a", "u")
        assert c.get(99) is None

    def test_get_zero_returns_none(self):
        c = DocAuditChain()
        c.append("d", "a", "u")
        assert c.get(0) is None


# ---------------------------------------------------------------------------
# Verify valid
# ---------------------------------------------------------------------------


class TestVerifyValid:
    def test_empty_chain_valid(self):
        c = DocAuditChain()
        r = c.verify()
        assert r.valid is True
        assert r.total_entries == 0
        assert r.verified_count == 0
        assert r.first_invalid_id is None

    def test_single_entry_valid(self):
        c = DocAuditChain(genesis_seed="abc")
        c.append("d", "a", "u")
        r = c.verify()
        assert r.valid is True
        assert r.total_entries == 1
        assert r.verified_count == 1

    def test_many_entries_valid(self):
        c = DocAuditChain()
        for i in range(50):
            c.append("d%d" % i, "act", "user%d" % (i % 3), {"i": i}, now=i)
        r = c.verify()
        assert r.valid is True
        assert r.verified_count == 50

    def test_verify_error_is_none_when_valid(self):
        c = DocAuditChain()
        c.append("d", "a", "u")
        r = c.verify()
        assert r.error is None


# ---------------------------------------------------------------------------
# Verify tampered
# ---------------------------------------------------------------------------


class TestVerifyTampered:
    def test_tamper_payload(self):
        c = DocAuditChain()
        c.append("d1", "a", "u", {"x": 1})
        c.append("d2", "a", "u", {"x": 2})
        # tamper: alter payload of entry 1 without recomputing hash
        c._entries[0].payload["x"] = 999
        r = c.verify()
        assert r.valid is False
        assert r.first_invalid_id == 1

    def test_tamper_actor(self):
        c = DocAuditChain()
        c.append("d", "a", "alice")
        c.append("d", "a", "bob")
        c._entries[1].actor = "eve"
        r = c.verify()
        assert r.valid is False
        assert r.first_invalid_id == 2

    def test_tamper_entry_hash(self):
        c = DocAuditChain()
        c.append("d", "a", "u")
        c._entries[0].entry_hash = "0" * 64
        r = c.verify()
        assert r.valid is False
        assert r.first_invalid_id == 1

    def test_tamper_prev_hash_breaks_link(self):
        c = DocAuditChain()
        c.append("d", "a", "u")
        c.append("d", "a", "u")
        c._entries[1].prev_hash = "0" * 64
        r = c.verify()
        assert r.valid is False
        assert r.first_invalid_id == 2
        assert "mismatch" in r.error

    def test_verified_count_stops_at_first_invalid(self):
        c = DocAuditChain()
        c.append("d", "a", "u")
        c.append("d", "a", "u")
        c.append("d", "a", "u")
        c._entries[1].entry_hash = "0" * 64
        r = c.verify()
        assert r.verified_count == 1
        assert r.first_invalid_id == 2


# ---------------------------------------------------------------------------
# Verify range
# ---------------------------------------------------------------------------


class TestVerifyRange:
    def test_range_full(self):
        c = DocAuditChain()
        for _ in range(5):
            c.append("d", "a", "u")
        r = c.verify_range(1, 5)
        assert r.valid is True
        assert r.verified_count == 5

    def test_range_partial(self):
        c = DocAuditChain()
        for _ in range(5):
            c.append("d", "a", "u")
        r = c.verify_range(2, 4)
        assert r.valid is True
        assert r.verified_count == 3

    def test_range_single_entry(self):
        c = DocAuditChain()
        c.append("d", "a", "u")
        r = c.verify_range(1, 1)
        assert r.valid is True

    def test_range_invalid_bounds(self):
        c = DocAuditChain()
        c.append("d", "a", "u")
        r = c.verify_range(5, 10)
        assert r.valid is False
        assert r.error == "invalid range"

    def test_range_inverted(self):
        c = DocAuditChain()
        c.append("d", "a", "u")
        c.append("d", "a", "u")
        r = c.verify_range(2, 1)
        assert r.valid is False

    def test_range_detects_tamper(self):
        c = DocAuditChain()
        for _ in range(5):
            c.append("d", "a", "u")
        c._entries[3].entry_hash = "0" * 64
        r = c.verify_range(3, 5)
        assert r.valid is False
        assert r.first_invalid_id == 4


# ---------------------------------------------------------------------------
# Entries for doc
# ---------------------------------------------------------------------------


class TestEntriesForDoc:
    def test_filter_by_doc(self):
        c = DocAuditChain()
        c.append("d1", "a", "u")
        c.append("d2", "a", "u")
        c.append("d1", "b", "u")
        got = c.entries_for_doc("d1")
        assert len(got) == 2
        assert all(e.doc_id == "d1" for e in got)

    def test_no_match(self):
        c = DocAuditChain()
        c.append("d1", "a", "u")
        assert c.entries_for_doc("xxx") == []

    def test_limit(self):
        c = DocAuditChain()
        for _ in range(5):
            c.append("d1", "a", "u")
        assert len(c.entries_for_doc("d1", limit=3)) == 3

    def test_order_preserved(self):
        c = DocAuditChain()
        for i in range(3):
            c.append("d1", "a%d" % i, "u")
        got = c.entries_for_doc("d1")
        assert [e.action for e in got] == ["a0", "a1", "a2"]


# ---------------------------------------------------------------------------
# Entries by actor
# ---------------------------------------------------------------------------


class TestEntriesByActor:
    def test_filter(self):
        c = DocAuditChain()
        c.append("d", "a", "alice")
        c.append("d", "a", "bob")
        c.append("d", "a", "alice")
        assert len(c.entries_by_actor("alice")) == 2

    def test_no_match(self):
        c = DocAuditChain()
        c.append("d", "a", "alice")
        assert c.entries_by_actor("xxx") == []

    def test_limit(self):
        c = DocAuditChain()
        for _ in range(5):
            c.append("d", "a", "alice")
        assert len(c.entries_by_actor("alice", limit=2)) == 2


# ---------------------------------------------------------------------------
# Entries by action
# ---------------------------------------------------------------------------


class TestEntriesByAction:
    def test_filter(self):
        c = DocAuditChain()
        c.append("d", "create", "u")
        c.append("d", "update", "u")
        c.append("d", "create", "u")
        assert len(c.entries_by_action("create")) == 2

    def test_no_match(self):
        c = DocAuditChain()
        c.append("d", "create", "u")
        assert c.entries_by_action("delete") == []

    def test_limit(self):
        c = DocAuditChain()
        for _ in range(4):
            c.append("d", "create", "u")
        assert len(c.entries_by_action("create", limit=2)) == 2


# ---------------------------------------------------------------------------
# Proof
# ---------------------------------------------------------------------------


class TestProof:
    def test_proof_for_existing_entry(self):
        c = DocAuditChain()
        e = c.append("d", "a", "u")
        p = c.proof(e.entry_id)
        assert p is not None
        assert p.entry_id == 1
        assert p.entry_hash == e.entry_hash
        assert p.prev_hash == e.prev_hash
        assert p.position == 1
        assert p.total_entries == 1

    def test_proof_for_missing_entry(self):
        c = DocAuditChain()
        assert c.proof(1) is None

    def test_proof_total_entries_grows(self):
        c = DocAuditChain()
        c.append("d", "a", "u")
        c.append("d", "a", "u")
        c.append("d", "a", "u")
        p = c.proof(2)
        assert p.total_entries == 3
        assert p.position == 2

    def test_proof_out_of_range(self):
        c = DocAuditChain()
        c.append("d", "a", "u")
        assert c.proof(99) is None

    def test_proof_zero(self):
        c = DocAuditChain()
        c.append("d", "a", "u")
        assert c.proof(0) is None


# ---------------------------------------------------------------------------
# verify_proof
# ---------------------------------------------------------------------------


class TestVerifyProof:
    def test_valid_proof(self):
        c = DocAuditChain()
        c.append("d", "a", "u")
        p = c.proof(1)
        assert c.verify_proof(p) is True

    def test_tampered_proof_hash(self):
        c = DocAuditChain()
        c.append("d", "a", "u")
        p = c.proof(1)
        bad = Proof(
            entry_id=p.entry_id,
            entry_hash="0" * 64,
            prev_hash=p.prev_hash,
            position=p.position,
            total_entries=p.total_entries,
        )
        assert c.verify_proof(bad) is False

    def test_tampered_proof_prev_hash(self):
        c = DocAuditChain()
        c.append("d", "a", "u")
        p = c.proof(1)
        bad = Proof(
            entry_id=p.entry_id,
            entry_hash=p.entry_hash,
            prev_hash="0" * 64,
            position=p.position,
            total_entries=p.total_entries,
        )
        assert c.verify_proof(bad) is False

    def test_proof_position_mismatch(self):
        c = DocAuditChain()
        c.append("d", "a", "u")
        c.append("d", "a", "u")
        p = c.proof(2)
        bad = Proof(
            entry_id=p.entry_id,
            entry_hash=p.entry_hash,
            prev_hash=p.prev_hash,
            position=99,
            total_entries=p.total_entries,
        )
        assert c.verify_proof(bad) is False

    def test_proof_unknown_id(self):
        c = DocAuditChain()
        c.append("d", "a", "u")
        bad = Proof(entry_id=99, entry_hash="x", prev_hash="x", position=99, total_entries=1)
        assert c.verify_proof(bad) is False

    def test_none_proof(self):
        c = DocAuditChain()
        assert c.verify_proof(None) is False

    def test_proof_detects_chain_tamper(self):
        c = DocAuditChain()
        c.append("d", "a", "u")
        p = c.proof(1)
        # mutate stored entry after proof generation
        c._entries[0].payload["leak"] = "yes"
        # entry_hash now doesn't match recomputed — proof.entry_hash still matches stored
        # so equality with stored holds; but recompute fails
        assert c.verify_proof(p) is False


# ---------------------------------------------------------------------------
# genesis_hash
# ---------------------------------------------------------------------------


class TestGenesisHash:
    def test_empty_seed(self):
        c = DocAuditChain()
        assert c.genesis_hash == hashlib.sha256(b"").hexdigest()

    def test_custom_seed(self):
        c = DocAuditChain(genesis_seed="hello")
        assert c.genesis_hash == hashlib.sha256(b"hello").hexdigest()

    def test_different_seeds_different_hash(self):
        a = DocAuditChain(genesis_seed="a")
        b = DocAuditChain(genesis_seed="b")
        assert a.genesis_hash != b.genesis_hash


# ---------------------------------------------------------------------------
# head_hash
# ---------------------------------------------------------------------------


class TestHeadHash:
    def test_empty_head_is_none(self):
        c = DocAuditChain()
        assert c.head_hash is None

    def test_head_matches_last_entry(self):
        c = DocAuditChain()
        c.append("d", "a", "u")
        e2 = c.append("d", "a", "u")
        assert c.head_hash == e2.entry_hash

    def test_head_advances(self):
        c = DocAuditChain()
        e1 = c.append("d", "a", "u")
        assert c.head_hash == e1.entry_hash
        e2 = c.append("d", "a", "u")
        assert c.head_hash == e2.entry_hash


# ---------------------------------------------------------------------------
# total_entries
# ---------------------------------------------------------------------------


class TestTotalEntries:
    def test_empty(self):
        c = DocAuditChain()
        assert c.total_entries == 0

    def test_grows(self):
        c = DocAuditChain()
        for i in range(7):
            c.append("d", "a", "u")
        assert c.total_entries == 7


# ---------------------------------------------------------------------------
# to_json
# ---------------------------------------------------------------------------


class TestToJson:
    def test_empty_chain(self):
        c = DocAuditChain(genesis_seed="seed")
        s = c.to_json()
        data = json.loads(s)
        assert data["genesis_seed"] == "seed"
        assert data["entries"] == []

    def test_with_entries(self):
        c = DocAuditChain(genesis_seed="seed")
        c.append("d", "a", "u", {"k": "v"})
        data = json.loads(c.to_json())
        assert len(data["entries"]) == 1
        assert data["entries"][0]["doc_id"] == "d"

    def test_deterministic(self):
        c = DocAuditChain(genesis_seed="seed")
        c.append("d", "a", "u", {"b": 2, "a": 1})
        s1 = c.to_json()
        s2 = c.to_json()
        assert s1 == s2


# ---------------------------------------------------------------------------
# from_json
# ---------------------------------------------------------------------------


class TestFromJson:
    def test_load_empty(self):
        src = DocAuditChain(genesis_seed="x")
        s = src.to_json()
        dst = DocAuditChain()
        assert dst.from_json(s) is True
        assert dst.total_entries == 0
        assert dst.genesis_hash == src.genesis_hash

    def test_load_with_entries(self):
        src = DocAuditChain(genesis_seed="s")
        src.append("d1", "create", "alice", {"x": 1})
        src.append("d2", "update", "bob", {"x": 2})
        dst = DocAuditChain()
        assert dst.from_json(src.to_json()) is True
        assert dst.total_entries == 2
        assert dst.verify().valid is True

    def test_load_rejects_invalid_json(self):
        dst = DocAuditChain()
        assert dst.from_json("not-json") is False

    def test_load_rejects_non_dict(self):
        dst = DocAuditChain()
        assert dst.from_json("[]") is False

    def test_load_rejects_tampered_payload(self):
        src = DocAuditChain()
        src.append("d", "a", "u", {"x": 1})
        data = json.loads(src.to_json())
        data["entries"][0]["payload"]["x"] = 999
        dst = DocAuditChain()
        assert dst.from_json(json.dumps(data)) is False

    def test_load_rejects_bad_entry_id_sequence(self):
        src = DocAuditChain()
        src.append("d", "a", "u")
        data = json.loads(src.to_json())
        data["entries"][0]["entry_id"] = 5
        # Recompute hash so verify passes, but entry_id sequence is off
        e = data["entries"][0]
        body = json.dumps(
            {
                "entry_id": 5,
                "doc_id": e["doc_id"],
                "action": e["action"],
                "actor": e["actor"],
                "payload": e["payload"],
                "timestamp": e["timestamp"],
                "prev_hash": e["prev_hash"],
            },
            sort_keys=True,
        )
        e["entry_hash"] = hashlib.sha256(body.encode()).hexdigest()
        dst = DocAuditChain()
        assert dst.from_json(json.dumps(data)) is False


# ---------------------------------------------------------------------------
# Round-trip
# ---------------------------------------------------------------------------


class TestRoundTrip:
    def test_round_trip_preserves_chain(self):
        src = DocAuditChain(genesis_seed="seed-42")
        src.append("d1", "create", "alice", {"k": "v"}, now=1.0)
        src.append("d2", "delete", "bob", {"n": 7}, now=2.0)
        src.append("d1", "update", "alice", {"x": "y"}, now=3.0)

        dst = DocAuditChain()
        assert dst.from_json(src.to_json()) is True

        assert dst.total_entries == src.total_entries
        assert dst.head_hash == src.head_hash
        for i in range(1, src.total_entries + 1):
            assert dst.get(i) == src.get(i)

    def test_round_trip_verify_after_load(self):
        src = DocAuditChain()
        for i in range(10):
            src.append("d", "a", "u", {"i": i}, now=float(i))
        dst = DocAuditChain()
        dst.from_json(src.to_json())
        r = dst.verify()
        assert r.valid is True
        assert r.verified_count == 10

    def test_round_trip_proof_still_verifies(self):
        src = DocAuditChain()
        src.append("d", "a", "u")
        src.append("d", "a", "u")
        p = src.proof(2)
        dst = DocAuditChain()
        dst.from_json(src.to_json())
        assert dst.verify_proof(p) is True


# ---------------------------------------------------------------------------
# Clear
# ---------------------------------------------------------------------------


class TestClear:
    def test_clear_empties_chain(self):
        c = DocAuditChain()
        c.append("d", "a", "u")
        c.append("d", "a", "u")
        c.clear()
        assert c.total_entries == 0
        assert c.head_hash is None

    def test_clear_preserves_genesis(self):
        c = DocAuditChain(genesis_seed="seed")
        prior_genesis = c.genesis_hash
        c.append("d", "a", "u")
        c.clear()
        assert c.genesis_hash == prior_genesis

    def test_append_after_clear_restarts_ids(self):
        c = DocAuditChain()
        c.append("d", "a", "u")
        c.append("d", "a", "u")
        c.clear()
        e = c.append("d", "a", "u")
        assert e.entry_id == 1


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_empty_payload_default(self):
        c = DocAuditChain()
        e = c.append("d", "a", "u")
        assert e.payload == {}

    def test_large_payload(self):
        c = DocAuditChain()
        big = {"k%d" % i: "v" * 100 for i in range(50)}
        e = c.append("d", "a", "u", big)
        r = c.verify()
        assert r.valid is True
        assert e.payload == big

    def test_unicode_fields(self):
        c = DocAuditChain(genesis_seed="привет")
        c.append("документ-1", "создать", "пользователь", {"ключ": "значение"})
        assert c.verify().valid is True

    def test_many_entries_chain_valid(self):
        c = DocAuditChain()
        for i in range(200):
            c.append("d%d" % (i % 5), "act", "actor%d" % (i % 3), {"i": i})
        r = c.verify()
        assert r.valid is True
        assert r.verified_count == 200

    def test_same_input_yields_same_hash(self):
        h1 = DocAuditChain._compute_hash(1, "d", "a", "u", {"x": 1}, 1.0, "p")
        h2 = DocAuditChain._compute_hash(1, "d", "a", "u", {"x": 1}, 1.0, "p")
        assert h1 == h2

    def test_different_payload_different_hash(self):
        h1 = DocAuditChain._compute_hash(1, "d", "a", "u", {"x": 1}, 1.0, "p")
        h2 = DocAuditChain._compute_hash(1, "d", "a", "u", {"x": 2}, 1.0, "p")
        assert h1 != h2

    def test_thread_safety_append(self):
        import threading as _t

        c = DocAuditChain()

        def worker():
            for _ in range(20):
                c.append("d", "a", "u")

        threads = [_t.Thread(target=worker) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert c.total_entries == 100
        assert c.verify().valid is True

    def test_verify_range_clamps_to_total(self):
        c = DocAuditChain()
        for _ in range(3):
            c.append("d", "a", "u")
        # end_id beyond total — should clamp
        r = c.verify_range(1, 100)
        assert r.valid is True
        assert r.verified_count == 3

    def test_genesis_hash_immutable_for_chain_after_first_append(self):
        c = DocAuditChain(genesis_seed="seed")
        before = c.genesis_hash
        c.append("d", "a", "u")
        c.append("d", "a", "u")
        assert c.genesis_hash == before


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
