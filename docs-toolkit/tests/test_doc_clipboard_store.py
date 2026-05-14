"""Tests for E369 DocClipboardStore."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_clipboard_store import (
    ClipboardEntry,
    ClipboardStats,
    DocClipboardStore,
)


class TestClipboardEntryDataclass:
    def test_required_fields(self):
        e = ClipboardEntry(entry_id=1, user_id="u", content="c")
        assert e.entry_id == 1
        assert e.user_id == "u"
        assert e.content == "c"

    def test_defaults(self):
        e = ClipboardEntry(entry_id=1, user_id="u", content="c")
        assert e.source_doc_id == ""
        assert e.copied_at == 0.0
        assert e.pinned is False

    def test_custom_values(self):
        e = ClipboardEntry(
            entry_id=2,
            user_id="bob",
            content="hello",
            source_doc_id="doc1",
            copied_at=12.5,
            pinned=True,
        )
        assert e.source_doc_id == "doc1"
        assert e.copied_at == 12.5
        assert e.pinned is True

    def test_mutable(self):
        e = ClipboardEntry(entry_id=1, user_id="u", content="c")
        e.pinned = True
        assert e.pinned is True


class TestClipboardStatsDataclass:
    def test_fields(self):
        s = ClipboardStats(total_entries=10, unique_users=3, pinned_count=2)
        assert s.total_entries == 10
        assert s.unique_users == 3
        assert s.pinned_count == 2

    def test_equality(self):
        a = ClipboardStats(1, 1, 1)
        b = ClipboardStats(1, 1, 1)
        assert a == b


class TestConstruction:
    def test_default_max(self):
        s = DocClipboardStore()
        assert s._max_per_user == 20

    def test_custom_max(self):
        s = DocClipboardStore(max_per_user=5)
        assert s._max_per_user == 5

    def test_zero_raises(self):
        with pytest.raises(ValueError):
            DocClipboardStore(max_per_user=0)

    def test_negative_raises(self):
        with pytest.raises(ValueError):
            DocClipboardStore(max_per_user=-3)

    def test_initial_state_empty(self):
        s = DocClipboardStore()
        assert s.users_with_clipboards() == []
        assert s.stats().total_entries == 0


class TestCopy:
    def test_returns_entry(self):
        s = DocClipboardStore()
        e = s.copy("u", "hello")
        assert isinstance(e, ClipboardEntry)
        assert e.user_id == "u"
        assert e.content == "hello"

    def test_id_starts_at_one(self):
        s = DocClipboardStore()
        e = s.copy("u", "hi")
        assert e.entry_id == 1

    def test_id_increments(self):
        s = DocClipboardStore()
        a = s.copy("u", "a")
        b = s.copy("u", "b")
        c = s.copy("v", "c")
        assert (a.entry_id, b.entry_id, c.entry_id) == (1, 2, 3)

    def test_source_doc_id(self):
        s = DocClipboardStore()
        e = s.copy("u", "x", source_doc_id="doc-7")
        assert e.source_doc_id == "doc-7"

    def test_explicit_now(self):
        s = DocClipboardStore()
        e = s.copy("u", "x", now=100.0)
        assert e.copied_at == 100.0

    def test_default_now_is_set(self):
        s = DocClipboardStore()
        e = s.copy("u", "x")
        assert e.copied_at > 0

    def test_trail_trim(self):
        s = DocClipboardStore(max_per_user=3)
        ids = [s.copy("u", f"c{i}").entry_id for i in range(5)]
        remaining = [e.entry_id for e in s.entries_for("u")]
        # newest 3 stay
        assert remaining == list(reversed(ids[-3:]))

    def test_trim_removes_from_entries(self):
        s = DocClipboardStore(max_per_user=2)
        e1 = s.copy("u", "a")
        s.copy("u", "b")
        s.copy("u", "c")
        assert s.get(e1.entry_id) is None


class TestCopyTrimPreservesPinned:
    def test_pinned_not_dropped(self):
        s = DocClipboardStore(max_per_user=2)
        e1 = s.copy("u", "first")
        s.pin(e1.entry_id)
        s.copy("u", "second")
        s.copy("u", "third")
        assert s.get(e1.entry_id) is not None

    def test_oldest_non_pinned_dropped_first(self):
        s = DocClipboardStore(max_per_user=2)
        e1 = s.copy("u", "first")
        e2 = s.copy("u", "second")
        s.pin(e1.entry_id)
        s.copy("u", "third")
        # e2 should be dropped, e1 (pinned) and "third" remain
        assert s.get(e2.entry_id) is None
        assert s.get(e1.entry_id) is not None

    def test_all_pinned_stay(self):
        s = DocClipboardStore(max_per_user=2)
        e1 = s.copy("u", "a")
        e2 = s.copy("u", "b")
        s.pin(e1.entry_id)
        s.pin(e2.entry_id)
        s.copy("u", "c")
        # All three remain because the two old ones are pinned
        ids = {e.entry_id for e in s.entries_for("u")}
        assert e1.entry_id in ids and e2.entry_id in ids


class TestPin:
    def test_returns_true_when_found(self):
        s = DocClipboardStore()
        e = s.copy("u", "x")
        assert s.pin(e.entry_id) is True

    def test_sets_pinned_flag(self):
        s = DocClipboardStore()
        e = s.copy("u", "x")
        s.pin(e.entry_id)
        assert s.get(e.entry_id).pinned is True

    def test_returns_false_when_missing(self):
        s = DocClipboardStore()
        assert s.pin(999) is False

    def test_idempotent(self):
        s = DocClipboardStore()
        e = s.copy("u", "x")
        assert s.pin(e.entry_id) is True
        assert s.pin(e.entry_id) is True


class TestUnpin:
    def test_returns_true_when_found(self):
        s = DocClipboardStore()
        e = s.copy("u", "x")
        s.pin(e.entry_id)
        assert s.unpin(e.entry_id) is True
        assert s.get(e.entry_id).pinned is False

    def test_returns_false_when_missing(self):
        s = DocClipboardStore()
        assert s.unpin(404) is False

    def test_unpin_unpinned_is_true(self):
        s = DocClipboardStore()
        e = s.copy("u", "x")
        assert s.unpin(e.entry_id) is True


class TestDelete:
    def test_returns_true_when_existed(self):
        s = DocClipboardStore()
        e = s.copy("u", "x")
        assert s.delete(e.entry_id) is True
        assert s.get(e.entry_id) is None

    def test_returns_false_when_missing(self):
        s = DocClipboardStore()
        assert s.delete(123) is False

    def test_removes_from_user_trail(self):
        s = DocClipboardStore()
        e = s.copy("u", "x")
        s.delete(e.entry_id)
        assert s.entries_for("u") == []


class TestClearUser:
    def test_returns_count(self):
        s = DocClipboardStore()
        s.copy("u", "a")
        s.copy("u", "b")
        s.copy("u", "c")
        assert s.clear_user("u") == 3

    def test_empty_user_returns_zero(self):
        s = DocClipboardStore()
        assert s.clear_user("nobody") == 0

    def test_keeps_pinned_by_default(self):
        s = DocClipboardStore()
        e1 = s.copy("u", "a")
        s.copy("u", "b")
        s.pin(e1.entry_id)
        removed = s.clear_user("u")
        assert removed == 1
        assert s.get(e1.entry_id) is not None

    def test_include_pinned_removes_all(self):
        s = DocClipboardStore()
        e1 = s.copy("u", "a")
        s.copy("u", "b")
        s.pin(e1.entry_id)
        removed = s.clear_user("u", include_pinned=True)
        assert removed == 2
        assert s.entries_for("u") == []

    def test_does_not_affect_other_users(self):
        s = DocClipboardStore()
        s.copy("u", "a")
        s.copy("v", "b")
        s.clear_user("u", include_pinned=True)
        assert len(s.entries_for("v")) == 1


class TestGet:
    def test_found(self):
        s = DocClipboardStore()
        e = s.copy("u", "x")
        got = s.get(e.entry_id)
        assert got is e

    def test_not_found(self):
        s = DocClipboardStore()
        assert s.get(42) is None


class TestEntriesFor:
    def test_most_recent_first(self):
        s = DocClipboardStore()
        s.copy("u", "a")
        s.copy("u", "b")
        s.copy("u", "c")
        contents = [e.content for e in s.entries_for("u")]
        assert contents == ["c", "b", "a"]

    def test_empty_user(self):
        s = DocClipboardStore()
        assert s.entries_for("nobody") == []

    def test_pinned_only(self):
        s = DocClipboardStore()
        e1 = s.copy("u", "a")
        s.copy("u", "b")
        e3 = s.copy("u", "c")
        s.pin(e1.entry_id)
        s.pin(e3.entry_id)
        out = s.entries_for("u", pinned_only=True)
        assert [e.entry_id for e in out] == [e3.entry_id, e1.entry_id]

    def test_limit(self):
        s = DocClipboardStore()
        for ch in "abcdef":
            s.copy("u", ch)
        out = s.entries_for("u", limit=2)
        assert len(out) == 2
        assert [e.content for e in out] == ["f", "e"]

    def test_limit_with_pinned_only(self):
        s = DocClipboardStore()
        ids = [s.copy("u", c).entry_id for c in "abcd"]
        for i in ids:
            s.pin(i)
        out = s.entries_for("u", pinned_only=True, limit=2)
        assert len(out) == 2


class TestLatest:
    def test_returns_most_recent(self):
        s = DocClipboardStore()
        s.copy("u", "a")
        s.copy("u", "b")
        e = s.latest("u")
        assert e is not None
        assert e.content == "b"

    def test_none_when_empty(self):
        s = DocClipboardStore()
        assert s.latest("nobody") is None

    def test_after_delete(self):
        s = DocClipboardStore()
        s.copy("u", "a")
        b = s.copy("u", "b")
        s.delete(b.entry_id)
        assert s.latest("u").content == "a"


class TestSearch:
    def test_case_insensitive(self):
        s = DocClipboardStore()
        s.copy("u", "Hello World")
        out = s.search("u", "hello")
        assert len(out) == 1

    def test_substring(self):
        s = DocClipboardStore()
        s.copy("u", "fragment of text")
        out = s.search("u", "men")
        assert len(out) == 1

    def test_no_match(self):
        s = DocClipboardStore()
        s.copy("u", "abc")
        assert s.search("u", "xyz") == []

    def test_most_recent_first(self):
        s = DocClipboardStore()
        s.copy("u", "match one")
        s.copy("u", "skip")
        s.copy("u", "match two")
        out = s.search("u", "match")
        assert [e.content for e in out] == ["match two", "match one"]

    def test_only_within_user(self):
        s = DocClipboardStore()
        s.copy("u", "secret")
        s.copy("v", "secret")
        out = s.search("u", "secret")
        assert all(e.user_id == "u" for e in out)
        assert len(out) == 1


class TestPinnedEntries:
    def test_sorted_desc_by_copied_at(self):
        s = DocClipboardStore()
        e1 = s.copy("u", "a", now=10.0)
        e2 = s.copy("u", "b", now=30.0)
        e3 = s.copy("u", "c", now=20.0)
        for eid in (e1.entry_id, e2.entry_id, e3.entry_id):
            s.pin(eid)
        out = s.pinned_entries("u")
        assert [e.copied_at for e in out] == [30.0, 20.0, 10.0]

    def test_excludes_unpinned(self):
        s = DocClipboardStore()
        e1 = s.copy("u", "a")
        s.copy("u", "b")
        s.pin(e1.entry_id)
        out = s.pinned_entries("u")
        assert len(out) == 1
        assert out[0].entry_id == e1.entry_id

    def test_empty_when_none(self):
        s = DocClipboardStore()
        s.copy("u", "x")
        assert s.pinned_entries("u") == []

    def test_empty_user(self):
        s = DocClipboardStore()
        assert s.pinned_entries("nobody") == []


class TestUsersWithClipboards:
    def test_sorted(self):
        s = DocClipboardStore()
        s.copy("charlie", "x")
        s.copy("alice", "y")
        s.copy("bob", "z")
        assert s.users_with_clipboards() == ["alice", "bob", "charlie"]

    def test_empty(self):
        s = DocClipboardStore()
        assert s.users_with_clipboards() == []

    def test_excludes_emptied(self):
        s = DocClipboardStore()
        s.copy("u", "x")
        s.copy("v", "y")
        s.clear_user("u", include_pinned=True)
        assert s.users_with_clipboards() == ["v"]


class TestStats:
    def test_empty(self):
        s = DocClipboardStore()
        st = s.stats()
        assert st == ClipboardStats(0, 0, 0)

    def test_totals(self):
        s = DocClipboardStore()
        s.copy("u", "a")
        s.copy("u", "b")
        e = s.copy("v", "c")
        s.pin(e.entry_id)
        st = s.stats()
        assert st.total_entries == 3
        assert st.unique_users == 2
        assert st.pinned_count == 1

    def test_after_delete(self):
        s = DocClipboardStore()
        e = s.copy("u", "x")
        s.delete(e.entry_id)
        st = s.stats()
        assert st.total_entries == 0
        assert st.unique_users == 0


class TestThreadSafety:
    def test_concurrent_copy(self):
        s = DocClipboardStore(max_per_user=1000)
        n_threads = 8
        per_thread = 50

        def worker(uid: str):
            for i in range(per_thread):
                s.copy(uid, f"{uid}-{i}")

        threads = [
            threading.Thread(target=worker, args=(f"u{idx}",))
            for idx in range(n_threads)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        st = s.stats()
        assert st.total_entries == n_threads * per_thread
        assert st.unique_users == n_threads
        # All ids should be unique
        all_ids = set()
        for idx in range(n_threads):
            for e in s.entries_for(f"u{idx}"):
                all_ids.add(e.entry_id)
        assert len(all_ids) == n_threads * per_thread

    def test_concurrent_mixed_ops(self):
        s = DocClipboardStore(max_per_user=500)
        ids: list[int] = []
        lock = threading.Lock()

        def writer():
            for i in range(30):
                e = s.copy("u", f"x{i}")
                with lock:
                    ids.append(e.entry_id)

        def pinner():
            for _ in range(30):
                with lock:
                    snap = list(ids)
                for eid in snap:
                    s.pin(eid)

        threads = [threading.Thread(target=writer) for _ in range(3)]
        threads += [threading.Thread(target=pinner) for _ in range(2)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # No exceptions and totals consistent
        st = s.stats()
        assert st.total_entries == 90
