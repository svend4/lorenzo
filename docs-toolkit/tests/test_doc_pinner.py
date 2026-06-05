"""Tests for the doc_pinner module."""

from __future__ import annotations

import pytest

from docstoolkit.doc_pinner import (
    DocPinner,
    Pin,
    PinScope,
    PinState,
    ResolutionResult,
)


class TestPinScope:
    def test_scope_values(self):
        assert PinScope.USER.value == "user"
        assert PinScope.GROUP.value == "group"
        assert PinScope.GLOBAL.value == "global"

    def test_scope_members(self):
        assert {s.name for s in PinScope} == {"USER", "GROUP", "GLOBAL"}

    def test_scope_equality(self):
        assert PinScope.USER is PinScope.USER
        assert PinScope.USER is not PinScope.GROUP


class TestPinState:
    def test_state_values(self):
        assert PinState.ACTIVE.value == "active"
        assert PinState.EXPIRED.value == "expired"
        assert PinState.OVERRIDDEN.value == "overridden"

    def test_state_members(self):
        assert {s.name for s in PinState} == {"ACTIVE", "EXPIRED", "OVERRIDDEN"}


class TestPin:
    def test_construct_minimal(self):
        p = Pin(pin_id="p1", doc_id="doc", version="v1", scope=PinScope.GLOBAL)
        assert p.pin_id == "p1"
        assert p.doc_id == "doc"
        assert p.version == "v1"
        assert p.scope is PinScope.GLOBAL
        assert p.target is None
        assert p.created_at == 0.0
        assert p.expires_at is None
        assert p.reason is None

    def test_construct_full(self):
        p = Pin(
            pin_id="p1",
            doc_id="doc",
            version="v1",
            scope=PinScope.USER,
            target="alice",
            created_at=100.0,
            expires_at=200.0,
            reason="rollout",
        )
        assert p.target == "alice"
        assert p.reason == "rollout"

    def test_is_expired_no_expiry(self):
        p = Pin(pin_id="p1", doc_id="d", version="v", scope=PinScope.GLOBAL)
        assert p.is_expired(now=1e9) is False

    def test_is_expired_before(self):
        p = Pin(
            pin_id="p", doc_id="d", version="v",
            scope=PinScope.GLOBAL, expires_at=100.0,
        )
        assert p.is_expired(now=50.0) is False

    def test_is_expired_at(self):
        p = Pin(
            pin_id="p", doc_id="d", version="v",
            scope=PinScope.GLOBAL, expires_at=100.0,
        )
        assert p.is_expired(now=100.0) is True

    def test_is_expired_after(self):
        p = Pin(
            pin_id="p", doc_id="d", version="v",
            scope=PinScope.GLOBAL, expires_at=100.0,
        )
        assert p.is_expired(now=150.0) is True


class TestResolutionResult:
    def test_construct(self):
        r = ResolutionResult(doc_id="d", resolved_version="v1")
        assert r.doc_id == "d"
        assert r.resolved_version == "v1"
        assert r.pin_used is None
        assert r.state is PinState.ACTIVE

    def test_construct_with_pin(self):
        p = Pin(pin_id="p", doc_id="d", version="v", scope=PinScope.GLOBAL)
        r = ResolutionResult(
            doc_id="d", resolved_version="v", pin_used=p, state=PinState.ACTIVE,
        )
        assert r.pin_used is p
        assert r.state is PinState.ACTIVE


class TestPinGlobal:
    def test_pin_global_basic(self):
        dp = DocPinner()
        p = dp.pin("doc1", "v1")
        assert p.scope is PinScope.GLOBAL
        assert p.doc_id == "doc1"
        assert p.version == "v1"
        assert p.target is None
        assert dp.total_pins == 1

    def test_pin_global_with_target_dropped(self):
        dp = DocPinner()
        p = dp.pin("doc1", "v1", scope=PinScope.GLOBAL, target="anyone")
        assert p.target is None

    def test_pin_global_returns_pin(self):
        dp = DocPinner()
        p = dp.pin("doc1", "v1", reason="freeze", now=10.0)
        assert isinstance(p, Pin)
        assert p.reason == "freeze"
        assert p.created_at == 10.0

    def test_pin_ids_unique(self):
        dp = DocPinner()
        a = dp.pin("doc1", "v1")
        b = dp.pin("doc1", "v2")
        assert a.pin_id != b.pin_id


class TestPinUser:
    def test_pin_user_requires_target(self):
        dp = DocPinner()
        with pytest.raises(ValueError):
            dp.pin("doc", "v", scope=PinScope.USER)

    def test_pin_user_ok(self):
        dp = DocPinner()
        p = dp.pin("doc", "v", scope=PinScope.USER, target="alice")
        assert p.scope is PinScope.USER
        assert p.target == "alice"

    def test_pin_user_count(self):
        dp = DocPinner()
        dp.pin("doc", "v", scope=PinScope.USER, target="alice")
        dp.pin("doc", "v2", scope=PinScope.USER, target="bob")
        assert dp.total_pins == 2


class TestPinGroup:
    def test_pin_group_requires_target(self):
        dp = DocPinner()
        with pytest.raises(ValueError):
            dp.pin("doc", "v", scope=PinScope.GROUP)

    def test_pin_group_ok(self):
        dp = DocPinner()
        p = dp.pin("doc", "v", scope=PinScope.GROUP, target="admins")
        assert p.scope is PinScope.GROUP
        assert p.target == "admins"


class TestUnpin:
    def test_unpin_existing(self):
        dp = DocPinner()
        p = dp.pin("doc", "v")
        assert dp.unpin(p.pin_id) is True
        assert dp.total_pins == 0

    def test_unpin_missing(self):
        dp = DocPinner()
        assert dp.unpin("nope") is False

    def test_unpin_twice(self):
        dp = DocPinner()
        p = dp.pin("doc", "v")
        assert dp.unpin(p.pin_id) is True
        assert dp.unpin(p.pin_id) is False


class TestResolveDefault:
    def test_resolve_no_pins(self):
        dp = DocPinner()
        r = dp.resolve("doc1")
        assert r.doc_id == "doc1"
        assert r.resolved_version == "latest"
        assert r.pin_used is None
        assert r.state is PinState.ACTIVE

    def test_resolve_custom_default(self):
        dp = DocPinner()
        r = dp.resolve("doc1", default_version="v0")
        assert r.resolved_version == "v0"
        assert r.pin_used is None

    def test_resolve_other_doc_pinned(self):
        dp = DocPinner()
        dp.pin("other", "v9")
        r = dp.resolve("doc1", default_version="d")
        assert r.resolved_version == "d"
        assert r.pin_used is None


class TestResolveGlobalPin:
    def test_resolve_global(self):
        dp = DocPinner()
        p = dp.pin("doc", "v1")
        r = dp.resolve("doc")
        assert r.resolved_version == "v1"
        assert r.pin_used is p
        assert r.state is PinState.ACTIVE

    def test_resolve_global_latest_wins(self):
        dp = DocPinner()
        dp.pin("doc", "v1", now=1.0)
        p2 = dp.pin("doc", "v2", now=2.0)
        r = dp.resolve("doc")
        assert r.pin_used is p2
        assert r.resolved_version == "v2"

    def test_resolve_global_with_user_id_no_user_pin(self):
        dp = DocPinner()
        dp.pin("doc", "v1")
        r = dp.resolve("doc", user_id="alice")
        assert r.resolved_version == "v1"


class TestResolveGroupPin:
    def test_group_beats_global(self):
        dp = DocPinner()
        dp.pin("doc", "global-v", scope=PinScope.GLOBAL)
        gp = dp.pin("doc", "group-v", scope=PinScope.GROUP, target="admins")
        r = dp.resolve("doc", group_id="admins")
        assert r.pin_used is gp
        assert r.resolved_version == "group-v"

    def test_group_only_for_matching_group(self):
        dp = DocPinner()
        dp.pin("doc", "group-v", scope=PinScope.GROUP, target="admins")
        gp = dp.pin("doc", "global-v", scope=PinScope.GLOBAL)
        r = dp.resolve("doc", group_id="other")
        assert r.pin_used is gp
        assert r.resolved_version == "global-v"

    def test_group_without_global_falls_to_default(self):
        dp = DocPinner()
        dp.pin("doc", "g", scope=PinScope.GROUP, target="admins")
        r = dp.resolve("doc", group_id="other", default_version="def")
        assert r.resolved_version == "def"


class TestResolveUserPin:
    def test_user_beats_group_and_global(self):
        dp = DocPinner()
        dp.pin("doc", "g", scope=PinScope.GLOBAL)
        dp.pin("doc", "grp", scope=PinScope.GROUP, target="admins")
        up = dp.pin("doc", "user", scope=PinScope.USER, target="alice")
        r = dp.resolve("doc", user_id="alice", group_id="admins")
        assert r.pin_used is up
        assert r.resolved_version == "user"

    def test_user_only_for_matching_user(self):
        dp = DocPinner()
        up_alice = dp.pin("doc", "alice-v", scope=PinScope.USER, target="alice")
        global_p = dp.pin("doc", "g", scope=PinScope.GLOBAL)
        r_alice = dp.resolve("doc", user_id="alice")
        assert r_alice.pin_used is up_alice
        r_bob = dp.resolve("doc", user_id="bob")
        assert r_bob.pin_used is global_p

    def test_user_no_user_id(self):
        dp = DocPinner()
        dp.pin("doc", "alice-v", scope=PinScope.USER, target="alice")
        gp = dp.pin("doc", "g", scope=PinScope.GLOBAL)
        r = dp.resolve("doc")
        assert r.pin_used is gp


class TestResolveExpired:
    def test_expired_global_skipped(self):
        dp = DocPinner()
        dp.pin("doc", "v1", expires_at=10.0, now=0.0)
        r = dp.resolve("doc", now=20.0, default_version="default")
        assert r.pin_used is None
        assert r.resolved_version == "default"

    def test_expired_user_falls_back_to_global(self):
        dp = DocPinner()
        dp.pin("doc", "user-v", scope=PinScope.USER, target="alice",
               expires_at=10.0, now=0.0)
        gp = dp.pin("doc", "global-v")
        r = dp.resolve("doc", user_id="alice", now=20.0)
        assert r.pin_used is gp
        assert r.resolved_version == "global-v"

    def test_not_yet_expired(self):
        dp = DocPinner()
        p = dp.pin("doc", "v", expires_at=100.0, now=0.0)
        r = dp.resolve("doc", now=50.0)
        assert r.pin_used is p

    def test_expired_at_boundary(self):
        dp = DocPinner()
        dp.pin("doc", "v", expires_at=100.0, now=0.0)
        r = dp.resolve("doc", now=100.0, default_version="def")
        assert r.pin_used is None
        assert r.resolved_version == "def"


class TestListPins:
    def test_list_all(self):
        dp = DocPinner()
        dp.pin("doc1", "v")
        dp.pin("doc2", "v")
        assert len(dp.list_pins()) == 2

    def test_list_by_doc(self):
        dp = DocPinner()
        dp.pin("doc1", "v")
        dp.pin("doc2", "v")
        out = dp.list_pins(doc_id="doc1")
        assert len(out) == 1
        assert out[0].doc_id == "doc1"

    def test_list_by_scope(self):
        dp = DocPinner()
        dp.pin("d", "v", scope=PinScope.GLOBAL)
        dp.pin("d", "v", scope=PinScope.USER, target="a")
        out = dp.list_pins(scope=PinScope.USER)
        assert len(out) == 1
        assert out[0].scope is PinScope.USER

    def test_list_excludes_expired(self):
        dp = DocPinner()
        dp.pin("d", "v", expires_at=10.0)
        dp.pin("d", "v2")
        out = dp.list_pins(now=20.0)
        assert len(out) == 1

    def test_list_empty(self):
        dp = DocPinner()
        assert dp.list_pins() == []


class TestPinsForUser:
    def test_pins_for_user_basic(self):
        dp = DocPinner()
        dp.pin("d1", "v", scope=PinScope.USER, target="alice")
        dp.pin("d2", "v", scope=PinScope.USER, target="alice")
        dp.pin("d3", "v", scope=PinScope.USER, target="bob")
        out = dp.pins_for_user("alice")
        assert len(out) == 2

    def test_pins_for_user_empty(self):
        dp = DocPinner()
        assert dp.pins_for_user("alice") == []

    def test_pins_for_user_excludes_expired(self):
        dp = DocPinner()
        dp.pin("d", "v", scope=PinScope.USER, target="a", expires_at=5.0)
        dp.pin("d2", "v", scope=PinScope.USER, target="a")
        out = dp.pins_for_user("a", now=10.0)
        assert len(out) == 1

    def test_pins_for_user_excludes_global(self):
        dp = DocPinner()
        dp.pin("d", "v", scope=PinScope.GLOBAL)
        assert dp.pins_for_user("alice") == []


class TestPinsForGroup:
    def test_pins_for_group_basic(self):
        dp = DocPinner()
        dp.pin("d", "v", scope=PinScope.GROUP, target="admins")
        dp.pin("d2", "v", scope=PinScope.GROUP, target="admins")
        dp.pin("d", "v", scope=PinScope.GROUP, target="users")
        assert len(dp.pins_for_group("admins")) == 2

    def test_pins_for_group_empty(self):
        dp = DocPinner()
        assert dp.pins_for_group("admins") == []

    def test_pins_for_group_excludes_expired(self):
        dp = DocPinner()
        dp.pin("d", "v", scope=PinScope.GROUP, target="g", expires_at=5.0)
        assert dp.pins_for_group("g", now=10.0) == []


class TestGlobalPins:
    def test_global_pins(self):
        dp = DocPinner()
        dp.pin("d", "v")
        dp.pin("d2", "v")
        dp.pin("d", "v", scope=PinScope.USER, target="a")
        out = dp.global_pins()
        assert len(out) == 2
        assert all(p.scope is PinScope.GLOBAL for p in out)

    def test_global_pins_empty(self):
        dp = DocPinner()
        assert dp.global_pins() == []

    def test_global_pins_excludes_expired(self):
        dp = DocPinner()
        dp.pin("d", "v", expires_at=5.0)
        assert dp.global_pins(now=10.0) == []


class TestCleanupExpired:
    def test_cleanup_removes_expired(self):
        dp = DocPinner()
        dp.pin("d", "v", expires_at=5.0)
        dp.pin("d2", "v")
        removed = dp.cleanup_expired(now=10.0)
        assert removed == 1
        assert dp.total_pins == 1

    def test_cleanup_nothing_to_remove(self):
        dp = DocPinner()
        dp.pin("d", "v")
        assert dp.cleanup_expired(now=100.0) == 0

    def test_cleanup_empty(self):
        dp = DocPinner()
        assert dp.cleanup_expired() == 0

    def test_cleanup_returns_count(self):
        dp = DocPinner()
        dp.pin("a", "v", expires_at=1.0)
        dp.pin("b", "v", expires_at=1.0)
        dp.pin("c", "v", expires_at=1.0)
        assert dp.cleanup_expired(now=5.0) == 3
        assert dp.total_pins == 0


class TestClear:
    def test_clear_all(self):
        dp = DocPinner()
        dp.pin("d", "v")
        dp.pin("d2", "v")
        dp.clear()
        assert dp.total_pins == 0

    def test_clear_empty(self):
        dp = DocPinner()
        dp.clear()
        assert dp.total_pins == 0

    def test_clear_resolution_falls_back(self):
        dp = DocPinner()
        dp.pin("d", "v")
        dp.clear()
        r = dp.resolve("d", default_version="def")
        assert r.resolved_version == "def"


class TestPinCount:
    def test_pin_count_active(self):
        dp = DocPinner()
        dp.pin("d", "v")
        dp.pin("d2", "v")
        assert dp.pin_count() == 2

    def test_pin_count_excludes_expired(self):
        dp = DocPinner()
        dp.pin("d", "v", expires_at=5.0)
        dp.pin("d2", "v")
        assert dp.pin_count(now=10.0) == 1

    def test_pin_count_empty(self):
        dp = DocPinner()
        assert dp.pin_count() == 0


class TestTotalPins:
    def test_total_includes_expired(self):
        dp = DocPinner()
        dp.pin("d", "v", expires_at=1.0)
        dp.pin("d2", "v")
        assert dp.total_pins == 2

    def test_total_after_unpin(self):
        dp = DocPinner()
        p = dp.pin("d", "v")
        dp.pin("d2", "v")
        dp.unpin(p.pin_id)
        assert dp.total_pins == 1

    def test_total_empty(self):
        dp = DocPinner()
        assert dp.total_pins == 0


class TestEdgeCases:
    def test_no_pins_resolve(self):
        dp = DocPinner()
        r = dp.resolve("anything", user_id="u", group_id="g")
        assert r.pin_used is None
        assert r.resolved_version == "latest"

    def test_multiple_user_pins_latest_wins(self):
        dp = DocPinner()
        dp.pin("d", "v1", scope=PinScope.USER, target="a", now=1.0)
        latest = dp.pin("d", "v2", scope=PinScope.USER, target="a", now=2.0)
        r = dp.resolve("d", user_id="a")
        assert r.pin_used is latest

    def test_multiple_group_pins_latest_wins(self):
        dp = DocPinner()
        dp.pin("d", "v1", scope=PinScope.GROUP, target="g", now=1.0)
        latest = dp.pin("d", "v2", scope=PinScope.GROUP, target="g", now=2.0)
        r = dp.resolve("d", group_id="g")
        assert r.pin_used is latest

    def test_resolve_returns_resolution_result(self):
        dp = DocPinner()
        r = dp.resolve("d")
        assert isinstance(r, ResolutionResult)

    def test_unpinned_id_resolution(self):
        dp = DocPinner()
        p = dp.pin("d", "v")
        dp.unpin(p.pin_id)
        r = dp.resolve("d", default_version="x")
        assert r.resolved_version == "x"
        assert r.pin_used is None

    def test_pin_user_without_target_raises_value_error(self):
        dp = DocPinner()
        with pytest.raises(ValueError):
            dp.pin("d", "v", scope=PinScope.USER, target=None)

    def test_pin_group_without_target_raises_value_error(self):
        dp = DocPinner()
        with pytest.raises(ValueError):
            dp.pin("d", "v", scope=PinScope.GROUP, target=None)

    def test_resolve_with_only_user_when_group_pin_present(self):
        dp = DocPinner()
        gp = dp.pin("d", "g", scope=PinScope.GROUP, target="grp")
        # user_id supplied but no user pin; group_id matches
        r = dp.resolve("d", user_id="alice", group_id="grp")
        assert r.pin_used is gp
