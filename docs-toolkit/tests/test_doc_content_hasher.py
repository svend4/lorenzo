"""Tests for docstoolkit.doc_content_hasher (E286).

Coverage (≥45 tests):
  - ContentHash: fields, values
  - ChangeRecord: fields, values
  - HasherStats: fields, defaults
  - DocContentHasher.__init__: default algorithm, bad algorithm raises
  - hash_content: basic hashing, returns ContentHash, content_len bytes, digest correct,
      algorithm stored, now param, default algorithm, explicit algorithm
  - hash_bytes: basic hashing, content_len = len(data), digest correct
  - get_hash: found, not found, explicit algorithm, default algorithm
  - verify: match, mismatch, no stored hash
  - has_changed: no prior hash → False, same content → False, changed → True
  - changes_for: no changes, one change, multiple changes, chronological order
  - find_duplicates: no dups, two docs same content, three docs, distinct content
  - delete: removes hash, returns True, second delete returns False,
            change history preserved after delete
  - stats: counts, algorithm_counts, changes reflected
  - total_docs property: increments, decrements on delete
  - Multi-algorithm: same doc hashed with sha256 and sha1 stored independently
  - Thread safety: concurrent hash_content calls do not corrupt state
"""

import hashlib
import threading
import time

import pytest

from docstoolkit.doc_content_hasher import (
    ChangeRecord,
    ContentHash,
    DocContentHasher,
    HasherStats,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _sha1(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


def _md5(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def _fresh(algo: str = "sha256") -> DocContentHasher:
    return DocContentHasher(default_algorithm=algo)


# ===========================================================================
# Dataclass shapes
# ===========================================================================

class TestContentHashDataclass:
    def test_fields_exist(self):
        ch = ContentHash(
            doc_id="d1",
            algorithm="sha256",
            digest="abc",
            content_len=3,
            computed_at=1.0,
        )
        assert ch.doc_id == "d1"
        assert ch.algorithm == "sha256"
        assert ch.digest == "abc"
        assert ch.content_len == 3
        assert ch.computed_at == 1.0

    def test_is_dataclass(self):
        import dataclasses
        assert dataclasses.is_dataclass(ContentHash)


class TestChangeRecordDataclass:
    def test_fields_exist(self):
        cr = ChangeRecord(
            doc_id="d1",
            old_digest="aaa",
            new_digest="bbb",
            changed_at=2.0,
            algorithm="sha256",
        )
        assert cr.doc_id == "d1"
        assert cr.old_digest == "aaa"
        assert cr.new_digest == "bbb"
        assert cr.changed_at == 2.0
        assert cr.algorithm == "sha256"

    def test_is_dataclass(self):
        import dataclasses
        assert dataclasses.is_dataclass(ChangeRecord)


class TestHasherStatsDataclass:
    def test_fields_exist(self):
        s = HasherStats(
            total_hashed=10,
            total_docs=5,
            total_changes=2,
            algorithm_counts={"sha256": 5},
        )
        assert s.total_hashed == 10
        assert s.total_docs == 5
        assert s.total_changes == 2
        assert s.algorithm_counts == {"sha256": 5}

    def test_is_dataclass(self):
        import dataclasses
        assert dataclasses.is_dataclass(HasherStats)


# ===========================================================================
# DocContentHasher.__init__
# ===========================================================================

class TestInit:
    def test_default_algorithm_sha256(self):
        h = DocContentHasher()
        ch = h.hash_content("d1", "hello")
        assert ch.algorithm == "sha256"

    def test_default_algorithm_sha1(self):
        h = DocContentHasher(default_algorithm="sha1")
        ch = h.hash_content("d1", "hello")
        assert ch.algorithm == "sha1"

    def test_default_algorithm_md5(self):
        h = DocContentHasher(default_algorithm="md5")
        ch = h.hash_content("d1", "hello")
        assert ch.algorithm == "md5"

    def test_bad_algorithm_raises(self):
        with pytest.raises(ValueError):
            DocContentHasher(default_algorithm="blake2b")

    def test_starts_empty(self):
        h = _fresh()
        assert h.total_docs == 0


# ===========================================================================
# hash_content
# ===========================================================================

class TestHashContent:
    def test_returns_content_hash(self):
        h = _fresh()
        ch = h.hash_content("doc1", "hello world")
        assert isinstance(ch, ContentHash)

    def test_doc_id_stored(self):
        h = _fresh()
        ch = h.hash_content("docX", "data")
        assert ch.doc_id == "docX"

    def test_correct_sha256_digest(self):
        h = _fresh()
        text = "the quick brown fox"
        ch = h.hash_content("d", text)
        assert ch.digest == _sha256(text)

    def test_correct_sha1_digest(self):
        h = _fresh()
        text = "hello sha1"
        ch = h.hash_content("d", text, algorithm="sha1")
        assert ch.digest == _sha1(text)

    def test_correct_md5_digest(self):
        h = _fresh()
        text = "hello md5"
        ch = h.hash_content("d", text, algorithm="md5")
        assert ch.digest == _md5(text)

    def test_content_len_is_utf8_bytes(self):
        h = _fresh()
        text = "привет"          # 6 chars but 12 UTF-8 bytes
        ch = h.hash_content("d", text)
        assert ch.content_len == len(text.encode("utf-8"))

    def test_content_len_ascii(self):
        h = _fresh()
        ch = h.hash_content("d", "abc")
        assert ch.content_len == 3

    def test_algorithm_in_result(self):
        h = _fresh()
        ch = h.hash_content("d", "x", algorithm="md5")
        assert ch.algorithm == "md5"

    def test_now_param_sets_computed_at(self):
        h = _fresh()
        ch = h.hash_content("d", "x", now=12345.0)
        assert ch.computed_at == 12345.0

    def test_computed_at_approx_now_when_not_given(self):
        h = _fresh()
        before = time.time()
        ch = h.hash_content("d", "y")
        after = time.time()
        assert before <= ch.computed_at <= after

    def test_bad_algorithm_param_raises(self):
        h = _fresh()
        with pytest.raises(ValueError):
            h.hash_content("d", "x", algorithm="crc32")

    def test_empty_string(self):
        h = _fresh()
        ch = h.hash_content("d", "")
        assert ch.content_len == 0
        assert ch.digest == _sha256("")


# ===========================================================================
# hash_bytes
# ===========================================================================

class TestHashBytes:
    def test_returns_content_hash(self):
        h = _fresh()
        ch = h.hash_bytes("d", b"data")
        assert isinstance(ch, ContentHash)

    def test_content_len_is_raw_byte_len(self):
        h = _fresh()
        data = b"\x00\x01\x02\x03"
        ch = h.hash_bytes("d", data)
        assert ch.content_len == 4

    def test_correct_sha256_for_bytes(self):
        h = _fresh()
        data = b"binary data"
        ch = h.hash_bytes("d", data)
        assert ch.digest == hashlib.sha256(data).hexdigest()

    def test_correct_md5_for_bytes(self):
        h = _fresh()
        data = b"binary"
        ch = h.hash_bytes("d", data, algorithm="md5")
        assert ch.digest == hashlib.md5(data).hexdigest()

    def test_now_param(self):
        h = _fresh()
        ch = h.hash_bytes("d", b"x", now=9999.0)
        assert ch.computed_at == 9999.0

    def test_empty_bytes(self):
        h = _fresh()
        ch = h.hash_bytes("d", b"")
        assert ch.content_len == 0


# ===========================================================================
# get_hash
# ===========================================================================

class TestGetHash:
    def test_returns_none_when_absent(self):
        h = _fresh()
        assert h.get_hash("missing") is None

    def test_returns_stored_hash(self):
        h = _fresh()
        h.hash_content("d", "hello")
        ch = h.get_hash("d")
        assert ch is not None
        assert ch.doc_id == "d"

    def test_explicit_algorithm(self):
        h = _fresh()
        h.hash_content("d", "hello", algorithm="md5")
        assert h.get_hash("d", algorithm="md5") is not None
        assert h.get_hash("d", algorithm="sha256") is None

    def test_default_algorithm_lookup(self):
        h = DocContentHasher(default_algorithm="sha1")
        h.hash_content("d", "x")
        ch = h.get_hash("d")      # should use sha1
        assert ch is not None
        assert ch.algorithm == "sha1"


# ===========================================================================
# verify
# ===========================================================================

class TestVerify:
    def test_verify_matching_content(self):
        h = _fresh()
        h.hash_content("d", "correct")
        assert h.verify("d", "correct") is True

    def test_verify_mismatched_content(self):
        h = _fresh()
        h.hash_content("d", "original")
        assert h.verify("d", "changed") is False

    def test_verify_no_stored_hash(self):
        h = _fresh()
        assert h.verify("d", "anything") is False

    def test_verify_explicit_algorithm(self):
        h = _fresh()
        h.hash_content("d", "text", algorithm="md5")
        assert h.verify("d", "text", algorithm="md5") is True
        assert h.verify("d", "text", algorithm="sha256") is False


# ===========================================================================
# has_changed
# ===========================================================================

class TestHasChanged:
    def test_no_prior_hash_returns_false(self):
        h = _fresh()
        assert h.has_changed("d", "any content") is False

    def test_same_content_returns_false(self):
        h = _fresh()
        h.hash_content("d", "stable")
        assert h.has_changed("d", "stable") is False

    def test_changed_content_returns_true(self):
        h = _fresh()
        h.hash_content("d", "version1")
        assert h.has_changed("d", "version2") is True

    def test_explicit_algorithm(self):
        h = _fresh()
        h.hash_content("d", "v1", algorithm="sha1")
        assert h.has_changed("d", "v2", algorithm="sha1") is True
        assert h.has_changed("d", "v2", algorithm="sha256") is False  # none stored


# ===========================================================================
# changes_for
# ===========================================================================

class TestChangesFor:
    def test_no_changes_initially(self):
        h = _fresh()
        h.hash_content("d", "first")
        assert h.changes_for("d") == []

    def test_one_change_recorded(self):
        h = _fresh()
        h.hash_content("d", "v1", now=1.0)
        h.hash_content("d", "v2", now=2.0)
        changes = h.changes_for("d")
        assert len(changes) == 1
        cr = changes[0]
        assert isinstance(cr, ChangeRecord)
        assert cr.doc_id == "d"
        assert cr.old_digest == _sha256("v1")
        assert cr.new_digest == _sha256("v2")
        assert cr.changed_at == 2.0

    def test_multiple_changes_in_order(self):
        h = _fresh()
        h.hash_content("d", "v1", now=1.0)
        h.hash_content("d", "v2", now=2.0)
        h.hash_content("d", "v3", now=3.0)
        changes = h.changes_for("d")
        assert len(changes) == 2
        assert changes[0].new_digest == _sha256("v2")
        assert changes[1].new_digest == _sha256("v3")

    def test_no_change_when_same_content(self):
        h = _fresh()
        h.hash_content("d", "same")
        h.hash_content("d", "same")
        assert h.changes_for("d") == []

    def test_returns_copy_not_reference(self):
        h = _fresh()
        h.hash_content("d", "v1", now=1.0)
        h.hash_content("d", "v2", now=2.0)
        lst = h.changes_for("d")
        lst.clear()
        assert len(h.changes_for("d")) == 1

    def test_unknown_doc_returns_empty(self):
        h = _fresh()
        assert h.changes_for("ghost") == []


# ===========================================================================
# find_duplicates
# ===========================================================================

class TestFindDuplicates:
    def test_no_docs_empty(self):
        h = _fresh()
        assert h.find_duplicates() == {}

    def test_no_duplicates(self):
        h = _fresh()
        h.hash_content("d1", "unique1")
        h.hash_content("d2", "unique2")
        assert h.find_duplicates() == {}

    def test_two_docs_same_content(self):
        h = _fresh()
        h.hash_content("d1", "same")
        h.hash_content("d2", "same")
        dups = h.find_duplicates()
        digest = _sha256("same")
        assert digest in dups
        assert sorted(dups[digest]) == ["d1", "d2"]

    def test_three_docs_same_content(self):
        h = _fresh()
        for i in range(3):
            h.hash_content(f"d{i}", "triple")
        dups = h.find_duplicates()
        digest = _sha256("triple")
        assert sorted(dups[digest]) == ["d0", "d1", "d2"]

    def test_only_dups_in_result(self):
        h = _fresh()
        h.hash_content("d1", "same")
        h.hash_content("d2", "same")
        h.hash_content("d3", "different")
        dups = h.find_duplicates()
        assert len(dups) == 1
        assert _sha256("different") not in dups


# ===========================================================================
# delete
# ===========================================================================

class TestDelete:
    def test_delete_existing_returns_true(self):
        h = _fresh()
        h.hash_content("d", "text")
        assert h.delete("d") is True

    def test_delete_missing_returns_false(self):
        h = _fresh()
        assert h.delete("ghost") is False

    def test_get_hash_after_delete_is_none(self):
        h = _fresh()
        h.hash_content("d", "text")
        h.delete("d")
        assert h.get_hash("d") is None

    def test_total_docs_decrements(self):
        h = _fresh()
        h.hash_content("d", "text")
        assert h.total_docs == 1
        h.delete("d")
        assert h.total_docs == 0

    def test_second_delete_returns_false(self):
        h = _fresh()
        h.hash_content("d", "x")
        h.delete("d")
        assert h.delete("d") is False

    def test_change_history_preserved_after_delete(self):
        h = _fresh()
        h.hash_content("d", "v1", now=1.0)
        h.hash_content("d", "v2", now=2.0)
        h.delete("d")
        # History kept even after deletion
        assert len(h.changes_for("d")) == 1

    def test_delete_removes_all_algorithms(self):
        h = _fresh()
        h.hash_content("d", "text", algorithm="sha256")
        h.hash_content("d", "text", algorithm="sha1")
        h.delete("d")
        assert h.get_hash("d", algorithm="sha256") is None
        assert h.get_hash("d", algorithm="sha1") is None


# ===========================================================================
# stats
# ===========================================================================

class TestStats:
    def test_empty_stats(self):
        h = _fresh()
        s = h.stats()
        assert s.total_hashed == 0
        assert s.total_docs == 0
        assert s.total_changes == 0
        assert s.algorithm_counts == {}

    def test_total_hashed_counts_calls(self):
        h = _fresh()
        h.hash_content("d1", "a")
        h.hash_content("d1", "b")  # update same doc
        h.hash_content("d2", "c")
        s = h.stats()
        assert s.total_hashed == 3

    def test_total_docs_unique_only(self):
        h = _fresh()
        h.hash_content("d1", "a")
        h.hash_content("d1", "b")
        h.hash_content("d2", "c")
        s = h.stats()
        assert s.total_docs == 2

    def test_total_changes(self):
        h = _fresh()
        h.hash_content("d", "v1")
        h.hash_content("d", "v2")
        h.hash_content("d", "v3")
        s = h.stats()
        assert s.total_changes == 2

    def test_algorithm_counts(self):
        h = _fresh()
        h.hash_content("d1", "x", algorithm="sha256")
        h.hash_content("d2", "y", algorithm="sha256")
        h.hash_content("d3", "z", algorithm="md5")
        s = h.stats()
        assert s.algorithm_counts["sha256"] == 2
        assert s.algorithm_counts["md5"] == 1

    def test_returns_hasher_stats_instance(self):
        h = _fresh()
        assert isinstance(h.stats(), HasherStats)


# ===========================================================================
# total_docs property
# ===========================================================================

class TestTotalDocs:
    def test_starts_at_zero(self):
        h = _fresh()
        assert h.total_docs == 0

    def test_increments_with_new_docs(self):
        h = _fresh()
        h.hash_content("d1", "a")
        assert h.total_docs == 1
        h.hash_content("d2", "b")
        assert h.total_docs == 2

    def test_same_doc_twice_no_increment(self):
        h = _fresh()
        h.hash_content("d1", "v1")
        h.hash_content("d1", "v2")
        assert h.total_docs == 1

    def test_decrements_after_delete(self):
        h = _fresh()
        h.hash_content("d1", "a")
        h.hash_content("d2", "b")
        h.delete("d1")
        assert h.total_docs == 1


# ===========================================================================
# Multi-algorithm support
# ===========================================================================

class TestMultiAlgorithm:
    def test_same_doc_multiple_algorithms_stored_independently(self):
        h = _fresh()
        h.hash_content("d", "content", algorithm="sha256")
        h.hash_content("d", "content", algorithm="sha1")
        ch256 = h.get_hash("d", algorithm="sha256")
        ch1 = h.get_hash("d", algorithm="sha1")
        assert ch256 is not None
        assert ch1 is not None
        assert ch256.digest == _sha256("content")
        assert ch1.digest == _sha1("content")

    def test_change_tracked_per_algorithm(self):
        h = _fresh()
        h.hash_content("d", "v1", algorithm="sha256")
        h.hash_content("d", "v1", algorithm="sha1")
        h.hash_content("d", "v2", algorithm="sha256")
        # Only sha256 changed, sha1 didn't
        changes = h.changes_for("d")
        assert len(changes) == 1
        assert changes[0].algorithm == "sha256"

    def test_total_docs_counts_doc_once_even_with_multiple_algos(self):
        h = _fresh()
        h.hash_content("d", "x", algorithm="sha256")
        h.hash_content("d", "x", algorithm="md5")
        assert h.total_docs == 1


# ===========================================================================
# Thread safety
# ===========================================================================

class TestThreadSafety:
    def test_concurrent_hash_content(self):
        """Multiple threads hashing different docs should not corrupt state."""
        h = _fresh()
        errors = []

        def worker(doc_id: str, content: str):
            try:
                for _ in range(20):
                    h.hash_content(doc_id, content)
            except Exception as exc:
                errors.append(exc)

        threads = [
            threading.Thread(target=worker, args=(f"doc{i}", f"content{i}"))
            for i in range(10)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
        assert h.total_docs == 10

    def test_concurrent_reads_and_writes(self):
        h = _fresh()
        h.hash_content("shared", "initial")
        errors = []

        def reader():
            try:
                for _ in range(50):
                    h.get_hash("shared")
                    h.verify("shared", "initial")
            except Exception as exc:
                errors.append(exc)

        def writer():
            try:
                for i in range(10):
                    h.hash_content("other", f"val{i}")
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=reader) for _ in range(4)]
        threads += [threading.Thread(target=writer) for _ in range(2)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
