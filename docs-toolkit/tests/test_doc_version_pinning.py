"""Tests for E328 DocVersionPinning."""

from __future__ import annotations

import threading
import uuid

import pytest

from docstoolkit.doc_version_pinning import (
    DocVersionPinning,
    PinningStats,
    VersionPin,
)


# ----------------------------------------------------------- dataclasses


class TestVersionPinDataclass:
    def test_required_fields(self):
        p = VersionPin(pin_id="x", doc_id="d", version="v1")
        assert p.pin_id == "x"
        assert p.doc_id == "d"
        assert p.version == "v1"

    def test_default_scope_is_global(self):
        p = VersionPin(pin_id="x", doc_id="d", version="v1")
        assert p.scope == "global"

    def test_default_scope_id_empty(self):
        p = VersionPin(pin_id="x", doc_id="d", version="v1")
        assert p.scope_id == ""

    def test_default_pinned_at(self):
        p = VersionPin(pin_id="x", doc_id="d", version="v1")
        assert p.pinned_at == 0.0

    def test_default_pinned_by(self):
        p = VersionPin(pin_id="x", doc_id="d", version="v1")
        assert p.pinned_by == ""

    def test_default_reason(self):
        p = VersionPin(pin_id="x", doc_id="d", version="v1")
        assert p.reason == ""

    def test_all_fields_set(self):
        p = VersionPin(
            pin_id="x",
            doc_id="d",
            version="v1",
            scope="user",
            scope_id="u1",
            pinned_at=42.0,
            pinned_by="alice",
            reason="testing",
        )
        assert p.scope == "user"
        assert p.scope_id == "u1"
        assert p.pinned_at == 42.0
        assert p.pinned_by == "alice"
        assert p.reason == "testing"

    def test_equality(self):
        a = VersionPin(pin_id="x", doc_id="d", version="v1")
        b = VersionPin(pin_id="x", doc_id="d", version="v1")
        assert a == b


class TestPinningStatsDataclass:
    def test_defaults(self):
        s = PinningStats(
            total_pins=0,
            unique_docs=0,
            unique_users=0,
            global_pins=0,
            user_pins=0,
            context_pins=0,
        )
        assert s.total_pins == 0
        assert s.unique_docs == 0
        assert s.unique_users == 0
        assert s.global_pins == 0
        assert s.user_pins == 0
        assert s.context_pins == 0

    def test_all_set(self):
        s = PinningStats(
            total_pins=5,
            unique_docs=3,
            unique_users=2,
            global_pins=1,
            user_pins=2,
            context_pins=2,
        )
        assert s.total_pins == 5
        assert s.unique_docs == 3
        assert s.unique_users == 2
        assert s.global_pins == 1
        assert s.user_pins == 2
        assert s.context_pins == 2

    def test_equality(self):
        a = PinningStats(1, 1, 0, 1, 0, 0)
        b = PinningStats(1, 1, 0, 1, 0, 0)
        assert a == b


# ----------------------------------------------------------- construction


class TestConstruction:
    def test_create(self):
        p = DocVersionPinning()
        assert p is not None

    def test_initial_empty_all_pins(self):
        p = DocVersionPinning()
        assert p.all_pins() == []

    def test_initial_stats(self):
        p = DocVersionPinning()
        s = p.stats()
        assert s.total_pins == 0
        assert s.unique_docs == 0
        assert s.global_pins == 0

    def test_initial_resolve_none(self):
        p = DocVersionPinning()
        assert p.resolve("doc1") is None


# -------------------------------------------------------------------- pin


class TestPin:
    def test_returns_version_pin(self):
        p = DocVersionPinning()
        out = p.pin("doc1", "v1")
        assert isinstance(out, VersionPin)

    def test_pin_id_is_uuid(self):
        p = DocVersionPinning()
        out = p.pin("doc1", "v1")
        # parsing must not raise
        parsed = uuid.UUID(out.pin_id)
        assert str(parsed) == out.pin_id

    def test_defaults_scope_global(self):
        p = DocVersionPinning()
        out = p.pin("doc1", "v1")
        assert out.scope == "global"
        assert out.scope_id == ""

    def test_now_set(self):
        p = DocVersionPinning()
        out = p.pin("doc1", "v1", now=123.0)
        assert out.pinned_at == 123.0

    def test_default_now_uses_time(self):
        p = DocVersionPinning()
        out = p.pin("doc1", "v1")
        assert out.pinned_at > 0.0

    def test_pinned_by_and_reason(self):
        p = DocVersionPinning()
        out = p.pin(
            "doc1", "v1", pinned_by="alice", reason="freeze"
        )
        assert out.pinned_by == "alice"
        assert out.reason == "freeze"

    def test_user_scope(self):
        p = DocVersionPinning()
        out = p.pin("doc1", "v1", scope="user", scope_id="u1")
        assert out.scope == "user"
        assert out.scope_id == "u1"

    def test_context_scope(self):
        p = DocVersionPinning()
        out = p.pin("doc1", "v1", scope="context", scope_id="c1")
        assert out.scope == "context"
        assert out.scope_id == "c1"

    def test_replace_on_same_tuple_global(self):
        p = DocVersionPinning()
        first = p.pin("doc1", "v1", now=1.0)
        second = p.pin("doc1", "v2", now=2.0)
        all_pins = p.all_pins()
        assert len(all_pins) == 1
        assert all_pins[0].pin_id == second.pin_id
        assert all_pins[0].version == "v2"
        # old gone
        assert p.get_pin(first.pin_id) is None

    def test_replace_on_same_tuple_user(self):
        p = DocVersionPinning()
        p.pin("doc1", "v1", scope="user", scope_id="u1")
        p.pin("doc1", "v2", scope="user", scope_id="u1")
        pins = p.pins_for_user("u1")
        assert len(pins) == 1
        assert pins[0].version == "v2"

    def test_different_tuple_does_not_replace(self):
        p = DocVersionPinning()
        p.pin("doc1", "v1", scope="global")
        p.pin("doc1", "v2", scope="user", scope_id="u1")
        assert len(p.all_pins()) == 2

    def test_unique_pin_ids(self):
        p = DocVersionPinning()
        a = p.pin("doc1", "v1")
        b = p.pin("doc2", "v1")
        assert a.pin_id != b.pin_id


# ------------------------------------------------------------------ unpin


class TestUnpin:
    def test_existing_returns_true(self):
        p = DocVersionPinning()
        out = p.pin("doc1", "v1")
        assert p.unpin(out.pin_id) is True

    def test_missing_returns_false(self):
        p = DocVersionPinning()
        assert p.unpin("does-not-exist") is False

    def test_gone_after_unpin(self):
        p = DocVersionPinning()
        out = p.pin("doc1", "v1")
        p.unpin(out.pin_id)
        assert p.get_pin(out.pin_id) is None

    def test_resolve_after_unpin(self):
        p = DocVersionPinning()
        out = p.pin("doc1", "v1")
        p.unpin(out.pin_id)
        assert p.resolve("doc1") is None

    def test_unpin_double(self):
        p = DocVersionPinning()
        out = p.pin("doc1", "v1")
        assert p.unpin(out.pin_id) is True
        assert p.unpin(out.pin_id) is False

    def test_lookup_cleaned(self):
        p = DocVersionPinning()
        out = p.pin("doc1", "v1", scope="user", scope_id="u1")
        p.unpin(out.pin_id)
        # re-pin to same key should not "replace" anything stale
        out2 = p.pin("doc1", "v2", scope="user", scope_id="u1")
        assert out2.version == "v2"
        assert len(p.all_pins()) == 1


# -------------------------------------------------------------- unpin_doc


class TestUnpinDoc:
    def test_global_existing(self):
        p = DocVersionPinning()
        p.pin("doc1", "v1")
        assert p.unpin_doc("doc1") is True

    def test_global_missing(self):
        p = DocVersionPinning()
        assert p.unpin_doc("doc1") is False

    def test_user_existing(self):
        p = DocVersionPinning()
        p.pin("doc1", "v1", scope="user", scope_id="u1")
        assert p.unpin_doc("doc1", scope="user", scope_id="u1") is True

    def test_user_wrong_user(self):
        p = DocVersionPinning()
        p.pin("doc1", "v1", scope="user", scope_id="u1")
        assert p.unpin_doc("doc1", scope="user", scope_id="u2") is False

    def test_unpin_doc_does_not_affect_other_scopes(self):
        p = DocVersionPinning()
        p.pin("doc1", "v1", scope="global")
        p.pin("doc1", "v2", scope="user", scope_id="u1")
        assert p.unpin_doc("doc1", scope="global") is True
        # user pin still present
        pins = p.pins_for_doc("doc1")
        assert len(pins) == 1
        assert pins[0].scope == "user"


# ---------------------------------------------------------------- get_pin


class TestGetPin:
    def test_found(self):
        p = DocVersionPinning()
        out = p.pin("doc1", "v1")
        assert p.get_pin(out.pin_id) == out

    def test_not_found(self):
        p = DocVersionPinning()
        assert p.get_pin("nope") is None


# -------------------------------------------------------- resolve / global


class TestResolveGlobal:
    def test_global_pin_returned(self):
        p = DocVersionPinning()
        p.pin("doc1", "v1")
        assert p.resolve("doc1") == "v1"

    def test_global_pin_returned_with_user_no_pin(self):
        p = DocVersionPinning()
        p.pin("doc1", "v1")
        assert p.resolve("doc1", user_id="someone") == "v1"

    def test_global_pin_returned_with_context_no_pin(self):
        p = DocVersionPinning()
        p.pin("doc1", "v1")
        assert p.resolve("doc1", context_id="ctx") == "v1"

    def test_unrelated_doc_returns_none(self):
        p = DocVersionPinning()
        p.pin("doc1", "v1")
        assert p.resolve("doc2") is None


# ----------------------------------------------------------- resolve user


class TestResolveUser:
    def test_user_wins_over_global(self):
        p = DocVersionPinning()
        p.pin("doc1", "v_global")
        p.pin("doc1", "v_user", scope="user", scope_id="u1")
        assert p.resolve("doc1", user_id="u1") == "v_user"

    def test_other_user_falls_back_to_global(self):
        p = DocVersionPinning()
        p.pin("doc1", "v_global")
        p.pin("doc1", "v_user", scope="user", scope_id="u1")
        assert p.resolve("doc1", user_id="u2") == "v_global"

    def test_user_only_no_global(self):
        p = DocVersionPinning()
        p.pin("doc1", "v_user", scope="user", scope_id="u1")
        assert p.resolve("doc1", user_id="u1") == "v_user"

    def test_user_none_skips_user_level(self):
        p = DocVersionPinning()
        p.pin("doc1", "v_global")
        p.pin("doc1", "v_user", scope="user", scope_id="u1")
        # user_id=None means we don't look at user pins
        assert p.resolve("doc1") == "v_global"


# -------------------------------------------------------- resolve context


class TestResolveContext:
    def test_context_wins_over_user(self):
        p = DocVersionPinning()
        p.pin("doc1", "v_global")
        p.pin("doc1", "v_user", scope="user", scope_id="u1")
        p.pin("doc1", "v_ctx", scope="context", scope_id="c1")
        assert (
            p.resolve("doc1", user_id="u1", context_id="c1") == "v_ctx"
        )

    def test_context_wins_over_global_no_user(self):
        p = DocVersionPinning()
        p.pin("doc1", "v_global")
        p.pin("doc1", "v_ctx", scope="context", scope_id="c1")
        assert p.resolve("doc1", context_id="c1") == "v_ctx"

    def test_other_context_falls_back_to_user(self):
        p = DocVersionPinning()
        p.pin("doc1", "v_user", scope="user", scope_id="u1")
        p.pin("doc1", "v_ctx", scope="context", scope_id="c1")
        assert (
            p.resolve("doc1", user_id="u1", context_id="c2") == "v_user"
        )

    def test_other_context_falls_back_to_global(self):
        p = DocVersionPinning()
        p.pin("doc1", "v_global")
        p.pin("doc1", "v_ctx", scope="context", scope_id="c1")
        assert p.resolve("doc1", context_id="c2") == "v_global"

    def test_context_none_skips_context_level(self):
        p = DocVersionPinning()
        p.pin("doc1", "v_global")
        p.pin("doc1", "v_ctx", scope="context", scope_id="c1")
        assert p.resolve("doc1") == "v_global"


# ----------------------------------------------------------- resolve none


class TestResolveNone:
    def test_empty_store(self):
        p = DocVersionPinning()
        assert p.resolve("doc1") is None

    def test_other_doc(self):
        p = DocVersionPinning()
        p.pin("doc2", "v1")
        assert p.resolve("doc1") is None

    def test_user_only_without_user_id(self):
        p = DocVersionPinning()
        p.pin("doc1", "v_user", scope="user", scope_id="u1")
        assert p.resolve("doc1") is None

    def test_context_only_without_context_id(self):
        p = DocVersionPinning()
        p.pin("doc1", "v_ctx", scope="context", scope_id="c1")
        assert p.resolve("doc1") is None


# --------------------------------------------------------- pins_for_doc


class TestPinsForDoc:
    def test_empty(self):
        p = DocVersionPinning()
        assert p.pins_for_doc("doc1") == []

    def test_returns_all_pins_for_doc(self):
        p = DocVersionPinning()
        p.pin("doc1", "v1", scope="global")
        p.pin("doc1", "v2", scope="user", scope_id="u1")
        p.pin("doc2", "vx")
        out = p.pins_for_doc("doc1")
        assert len(out) == 2
        assert all(x.doc_id == "doc1" for x in out)

    def test_sorted(self):
        p = DocVersionPinning()
        p.pin("doc1", "v_user", scope="user", scope_id="u1")
        p.pin("doc1", "v_ctx", scope="context", scope_id="c1")
        p.pin("doc1", "v_global", scope="global")
        out = p.pins_for_doc("doc1")
        keys = [(x.scope, x.scope_id) for x in out]
        assert keys == sorted(keys)


# --------------------------------------------------------- pins_for_user


class TestPinsForUser:
    def test_empty(self):
        p = DocVersionPinning()
        assert p.pins_for_user("u1") == []

    def test_only_user_scope(self):
        p = DocVersionPinning()
        p.pin("doc1", "v1", scope="user", scope_id="u1")
        p.pin("doc1", "v_global", scope="global")
        out = p.pins_for_user("u1")
        assert len(out) == 1
        assert out[0].scope == "user"

    def test_filters_user_id(self):
        p = DocVersionPinning()
        p.pin("doc1", "v1", scope="user", scope_id="u1")
        p.pin("doc1", "v2", scope="user", scope_id="u2")
        out = p.pins_for_user("u1")
        assert len(out) == 1
        assert out[0].scope_id == "u1"

    def test_sorted_by_doc_id(self):
        p = DocVersionPinning()
        p.pin("docB", "v1", scope="user", scope_id="u1")
        p.pin("docA", "v1", scope="user", scope_id="u1")
        p.pin("docC", "v1", scope="user", scope_id="u1")
        out = p.pins_for_user("u1")
        assert [x.doc_id for x in out] == ["docA", "docB", "docC"]


# ------------------------------------------------------------- all_pins


class TestAllPins:
    def test_empty(self):
        p = DocVersionPinning()
        assert p.all_pins() == []

    def test_returns_all(self):
        p = DocVersionPinning()
        p.pin("doc1", "v1")
        p.pin("doc2", "v1")
        p.pin("doc1", "v_user", scope="user", scope_id="u1")
        assert len(p.all_pins()) == 3

    def test_sorted(self):
        p = DocVersionPinning()
        p.pin("doc2", "v1", scope="user", scope_id="u1")
        p.pin("doc1", "v1", scope="global")
        p.pin("doc1", "v2", scope="user", scope_id="u1")
        p.pin("doc1", "v3", scope="context", scope_id="c1")
        out = p.all_pins()
        keys = [(x.doc_id, x.scope, x.scope_id) for x in out]
        assert keys == sorted(keys)


# ----------------------------------------------------------------- stats


class TestStats:
    def test_empty(self):
        p = DocVersionPinning()
        s = p.stats()
        assert s.total_pins == 0
        assert s.unique_docs == 0
        assert s.unique_users == 0
        assert s.global_pins == 0
        assert s.user_pins == 0
        assert s.context_pins == 0

    def test_counts_global(self):
        p = DocVersionPinning()
        p.pin("d1", "v1")
        p.pin("d2", "v1")
        s = p.stats()
        assert s.global_pins == 2
        assert s.user_pins == 0
        assert s.context_pins == 0

    def test_counts_user(self):
        p = DocVersionPinning()
        p.pin("d1", "v1", scope="user", scope_id="u1")
        p.pin("d2", "v1", scope="user", scope_id="u1")
        p.pin("d1", "v1", scope="user", scope_id="u2")
        s = p.stats()
        assert s.user_pins == 3
        assert s.unique_users == 2

    def test_counts_context(self):
        p = DocVersionPinning()
        p.pin("d1", "v1", scope="context", scope_id="c1")
        p.pin("d2", "v1", scope="context", scope_id="c1")
        s = p.stats()
        assert s.context_pins == 2

    def test_total_and_unique_docs(self):
        p = DocVersionPinning()
        p.pin("d1", "v1")
        p.pin("d2", "v1")
        p.pin("d1", "v_user", scope="user", scope_id="u1")
        s = p.stats()
        assert s.total_pins == 3
        assert s.unique_docs == 2

    def test_mixed(self):
        p = DocVersionPinning()
        p.pin("d1", "v1")
        p.pin("d1", "v_u", scope="user", scope_id="u1")
        p.pin("d1", "v_c", scope="context", scope_id="c1")
        p.pin("d2", "v1")
        s = p.stats()
        assert s.total_pins == 4
        assert s.unique_docs == 2
        assert s.global_pins == 2
        assert s.user_pins == 1
        assert s.context_pins == 1
        assert s.unique_users == 1


# ----------------------------------------------------------- thread safety


class TestThreadSafety:
    def test_concurrent_pin_different_docs(self):
        p = DocVersionPinning()

        def worker(i: int):
            for j in range(20):
                p.pin(f"doc-{i}-{j}", "v1")

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(p.all_pins()) == 8 * 20

    def test_concurrent_pin_same_tuple(self):
        p = DocVersionPinning()

        def worker(i: int):
            for _ in range(20):
                p.pin("doc1", f"v-{i}")

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(6)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Only one pin survives for (doc1, global, "")
        all_pins = p.all_pins()
        assert len(all_pins) == 1
        assert all_pins[0].doc_id == "doc1"

    def test_concurrent_pin_and_unpin(self):
        p = DocVersionPinning()

        def pinner():
            for i in range(50):
                p.pin(f"d{i}", "v1")

        def unpinner():
            for i in range(50):
                p.unpin_doc(f"d{i}")

        t1 = threading.Thread(target=pinner)
        t2 = threading.Thread(target=unpinner)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        # Should not raise and state should be consistent.
        s = p.stats()
        assert s.total_pins == len(p.all_pins())
