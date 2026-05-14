"""Tests for E389 DocUserRoleMap."""
from __future__ import annotations

import threading
import time

import pytest

from docstoolkit.doc_user_role_map import (
    DocUserRoleMap,
    RoleDefinition,
    UserRole,
    UserRoleStats,
)


# --------------------------------------------------------------------- helpers
def _admin() -> RoleDefinition:
    return RoleDefinition(
        role="admin",
        permissions=["read", "write", "delete"],
        description="Administrator",
    )


def _editor() -> RoleDefinition:
    return RoleDefinition(role="editor", permissions=["read", "write"])


def _viewer() -> RoleDefinition:
    return RoleDefinition(role="viewer", permissions=["read"])


# ===================================================================== dataclasses
class TestUserRoleDataclass:
    def test_defaults(self):
        ur = UserRole(user_id="u1", role="admin")
        assert ur.user_id == "u1"
        assert ur.role == "admin"
        assert ur.assigned_at == 0.0
        assert ur.assigned_by == ""

    def test_all_fields(self):
        ur = UserRole(user_id="u1", role="admin", assigned_at=1.5, assigned_by="root")
        assert ur.assigned_at == 1.5
        assert ur.assigned_by == "root"

    def test_equality(self):
        a = UserRole("u1", "r", 1.0, "x")
        b = UserRole("u1", "r", 1.0, "x")
        assert a == b


class TestRoleDefinitionDataclass:
    def test_defaults(self):
        rd = RoleDefinition(role="admin")
        assert rd.role == "admin"
        assert rd.permissions == []
        assert rd.description == ""

    def test_with_permissions(self):
        rd = RoleDefinition(role="admin", permissions=["a", "b"])
        assert rd.permissions == ["a", "b"]

    def test_permissions_independent_instances(self):
        a = RoleDefinition(role="r1")
        b = RoleDefinition(role="r2")
        a.permissions.append("x")
        assert b.permissions == []


class TestUserRoleStatsDataclass:
    def test_defaults(self):
        s = UserRoleStats()
        assert s.total_roles == 0
        assert s.total_users == 0
        assert s.role_counts == {}

    def test_with_values(self):
        s = UserRoleStats(total_roles=3, total_users=2, role_counts={"r": 1})
        assert s.total_roles == 3
        assert s.total_users == 2
        assert s.role_counts == {"r": 1}


# ===================================================================== construction
class TestConstruction:
    def test_default_construction(self):
        m = DocUserRoleMap()
        assert m.list_roles() == []
        assert m.stats().total_roles == 0
        assert m.stats().total_users == 0

    def test_independent_instances(self):
        a = DocUserRoleMap()
        b = DocUserRoleMap()
        a.define_role(_admin())
        assert b.list_roles() == []


# ===================================================================== define_role
class TestDefineRole:
    def test_define_single(self):
        m = DocUserRoleMap()
        m.define_role(_admin())
        rd = m.get_role("admin")
        assert rd is not None
        assert rd.role == "admin"

    def test_define_overwrites(self):
        m = DocUserRoleMap()
        m.define_role(RoleDefinition(role="admin", permissions=["read"]))
        m.define_role(RoleDefinition(role="admin", permissions=["read", "write"]))
        assert m.get_role("admin").permissions == ["read", "write"]

    def test_define_copies_permissions(self):
        m = DocUserRoleMap()
        perms = ["read", "write"]
        rd = RoleDefinition(role="r", permissions=perms)
        m.define_role(rd)
        perms.append("delete")
        stored = m.get_role("r")
        assert stored.permissions == ["read", "write"]

    def test_define_multiple(self):
        m = DocUserRoleMap()
        m.define_role(_admin())
        m.define_role(_editor())
        m.define_role(_viewer())
        assert len(m.list_roles()) == 3


# ===================================================================== undefine_role
class TestUndefineRole:
    def test_undefine_existing(self):
        m = DocUserRoleMap()
        m.define_role(_admin())
        assert m.undefine_role("admin") is True
        assert m.get_role("admin") is None

    def test_undefine_missing(self):
        m = DocUserRoleMap()
        assert m.undefine_role("nope") is False

    def test_undefine_cascades_to_users(self):
        m = DocUserRoleMap()
        m.define_role(_admin())
        m.define_role(_editor())
        m.assign("u1", "admin")
        m.assign("u1", "editor")
        m.assign("u2", "admin")
        m.undefine_role("admin")
        assert m.roles_of("u1") == ["editor"]
        assert m.roles_of("u2") == []
        assert "u2" not in [u for u in m.users_with_role("admin")]

    def test_undefine_removes_empty_user_entries(self):
        m = DocUserRoleMap()
        m.define_role(_admin())
        m.assign("u1", "admin")
        m.undefine_role("admin")
        # after cascade u1 has no roles, stats should not count them
        assert m.stats().total_users == 0


# ===================================================================== get_role
class TestGetRole:
    def test_get_existing(self):
        m = DocUserRoleMap()
        m.define_role(_admin())
        rd = m.get_role("admin")
        assert rd.description == "Administrator"

    def test_get_missing(self):
        m = DocUserRoleMap()
        assert m.get_role("missing") is None

    def test_get_returns_copy(self):
        m = DocUserRoleMap()
        m.define_role(_admin())
        rd = m.get_role("admin")
        rd.permissions.append("hacked")
        assert "hacked" not in m.get_role("admin").permissions


# ===================================================================== list_roles
class TestListRoles:
    def test_empty(self):
        m = DocUserRoleMap()
        assert m.list_roles() == []

    def test_sorted_by_role(self):
        m = DocUserRoleMap()
        m.define_role(RoleDefinition(role="zeta"))
        m.define_role(RoleDefinition(role="alpha"))
        m.define_role(RoleDefinition(role="mu"))
        names = [r.role for r in m.list_roles()]
        assert names == ["alpha", "mu", "zeta"]

    def test_returns_copies(self):
        m = DocUserRoleMap()
        m.define_role(_admin())
        roles = m.list_roles()
        roles[0].permissions.append("hacked")
        assert "hacked" not in m.get_role("admin").permissions


# ===================================================================== assign
class TestAssign:
    def test_assign_defined(self):
        m = DocUserRoleMap()
        m.define_role(_admin())
        result = m.assign("u1", "admin")
        assert result is not None
        assert result.user_id == "u1"
        assert result.role == "admin"

    def test_assign_undefined_returns_none(self):
        m = DocUserRoleMap()
        assert m.assign("u1", "ghost") is None

    def test_assign_records_timestamp(self):
        m = DocUserRoleMap()
        m.define_role(_admin())
        before = time.time()
        r = m.assign("u1", "admin")
        after = time.time()
        assert before <= r.assigned_at <= after

    def test_assign_explicit_now(self):
        m = DocUserRoleMap()
        m.define_role(_admin())
        r = m.assign("u1", "admin", now=42.0)
        assert r.assigned_at == 42.0

    def test_assign_assigned_by(self):
        m = DocUserRoleMap()
        m.define_role(_admin())
        r = m.assign("u1", "admin", assigned_by="root")
        assert r.assigned_by == "root"

    def test_assign_appends_history(self):
        m = DocUserRoleMap()
        m.define_role(_admin())
        m.assign("u1", "admin", now=1.0)
        m.assign("u2", "admin", now=2.0)
        h = m.history()
        assert len(h) == 2
        assert h[0].user_id == "u1"
        assert h[1].user_id == "u2"

    def test_assign_undefined_no_history(self):
        m = DocUserRoleMap()
        m.assign("u1", "ghost")
        assert m.history() == []

    def test_assign_duplicate_idempotent_on_set(self):
        m = DocUserRoleMap()
        m.define_role(_admin())
        m.assign("u1", "admin")
        m.assign("u1", "admin")
        assert m.roles_of("u1") == ["admin"]
        # but both still go into history
        assert len(m.history()) == 2


# ===================================================================== revoke
class TestRevoke:
    def test_revoke_existing(self):
        m = DocUserRoleMap()
        m.define_role(_admin())
        m.assign("u1", "admin")
        assert m.revoke("u1", "admin") is True
        assert m.roles_of("u1") == []

    def test_revoke_missing_user(self):
        m = DocUserRoleMap()
        assert m.revoke("ghost", "admin") is False

    def test_revoke_missing_role_for_user(self):
        m = DocUserRoleMap()
        m.define_role(_admin())
        m.define_role(_editor())
        m.assign("u1", "admin")
        assert m.revoke("u1", "editor") is False

    def test_revoke_keeps_other_roles(self):
        m = DocUserRoleMap()
        m.define_role(_admin())
        m.define_role(_editor())
        m.assign("u1", "admin")
        m.assign("u1", "editor")
        m.revoke("u1", "admin")
        assert m.roles_of("u1") == ["editor"]


# ===================================================================== roles_of
class TestRolesOf:
    def test_empty(self):
        m = DocUserRoleMap()
        assert m.roles_of("nobody") == []

    def test_sorted(self):
        m = DocUserRoleMap()
        m.define_role(_admin())
        m.define_role(_editor())
        m.define_role(_viewer())
        m.assign("u1", "viewer")
        m.assign("u1", "admin")
        m.assign("u1", "editor")
        assert m.roles_of("u1") == ["admin", "editor", "viewer"]


# ===================================================================== users_with_role
class TestUsersWithRole:
    def test_empty(self):
        m = DocUserRoleMap()
        assert m.users_with_role("admin") == []

    def test_sorted(self):
        m = DocUserRoleMap()
        m.define_role(_admin())
        m.assign("zeta", "admin")
        m.assign("alpha", "admin")
        m.assign("mu", "admin")
        assert m.users_with_role("admin") == ["alpha", "mu", "zeta"]

    def test_isolation(self):
        m = DocUserRoleMap()
        m.define_role(_admin())
        m.define_role(_editor())
        m.assign("u1", "admin")
        m.assign("u2", "editor")
        assert m.users_with_role("admin") == ["u1"]


# ===================================================================== has_role
class TestHasRole:
    def test_true(self):
        m = DocUserRoleMap()
        m.define_role(_admin())
        m.assign("u1", "admin")
        assert m.has_role("u1", "admin") is True

    def test_false_other_role(self):
        m = DocUserRoleMap()
        m.define_role(_admin())
        m.define_role(_editor())
        m.assign("u1", "admin")
        assert m.has_role("u1", "editor") is False

    def test_false_unknown_user(self):
        m = DocUserRoleMap()
        m.define_role(_admin())
        assert m.has_role("ghost", "admin") is False


# ===================================================================== has_permission
class TestHasPermission:
    def test_grant_via_single_role(self):
        m = DocUserRoleMap()
        m.define_role(_admin())
        m.assign("u1", "admin")
        assert m.has_permission("u1", "delete") is True

    def test_grant_via_one_of_many(self):
        m = DocUserRoleMap()
        m.define_role(_viewer())
        m.define_role(_editor())
        m.assign("u1", "viewer")
        m.assign("u1", "editor")
        assert m.has_permission("u1", "write") is True

    def test_no_permission(self):
        m = DocUserRoleMap()
        m.define_role(_viewer())
        m.assign("u1", "viewer")
        assert m.has_permission("u1", "delete") is False

    def test_unknown_user(self):
        m = DocUserRoleMap()
        m.define_role(_admin())
        assert m.has_permission("ghost", "read") is False

    def test_role_undefined_after_assignment_skipped(self):
        # Role removed from definitions cascades; but if some inconsistency exists
        # it should not crash.
        m = DocUserRoleMap()
        m.define_role(_admin())
        m.assign("u1", "admin")
        m.undefine_role("admin")
        assert m.has_permission("u1", "read") is False


# ===================================================================== permissions_for
class TestPermissionsFor:
    def test_empty(self):
        m = DocUserRoleMap()
        assert m.permissions_for("ghost") == []

    def test_single_role_sorted(self):
        m = DocUserRoleMap()
        m.define_role(_admin())
        m.assign("u1", "admin")
        # admin has read, write, delete
        assert m.permissions_for("u1") == ["delete", "read", "write"]

    def test_union_across_roles(self):
        m = DocUserRoleMap()
        m.define_role(RoleDefinition(role="r1", permissions=["a", "b"]))
        m.define_role(RoleDefinition(role="r2", permissions=["b", "c"]))
        m.assign("u1", "r1")
        m.assign("u1", "r2")
        assert m.permissions_for("u1") == ["a", "b", "c"]

    def test_dedup(self):
        m = DocUserRoleMap()
        m.define_role(RoleDefinition(role="r1", permissions=["a", "a", "b"]))
        m.assign("u1", "r1")
        assert m.permissions_for("u1") == ["a", "b"]


# ===================================================================== clear_user
class TestClearUser:
    def test_clear_returns_count(self):
        m = DocUserRoleMap()
        m.define_role(_admin())
        m.define_role(_editor())
        m.assign("u1", "admin")
        m.assign("u1", "editor")
        assert m.clear_user("u1") == 2
        assert m.roles_of("u1") == []

    def test_clear_no_user_returns_zero(self):
        m = DocUserRoleMap()
        assert m.clear_user("ghost") == 0

    def test_clear_does_not_affect_others(self):
        m = DocUserRoleMap()
        m.define_role(_admin())
        m.assign("u1", "admin")
        m.assign("u2", "admin")
        m.clear_user("u1")
        assert m.roles_of("u2") == ["admin"]


# ===================================================================== history
class TestHistory:
    def test_empty(self):
        m = DocUserRoleMap()
        assert m.history() == []

    def test_chronological(self):
        m = DocUserRoleMap()
        m.define_role(_admin())
        m.assign("u1", "admin", now=1.0)
        m.assign("u2", "admin", now=2.0)
        m.assign("u3", "admin", now=3.0)
        ts = [e.assigned_at for e in m.history()]
        assert ts == [1.0, 2.0, 3.0]

    def test_filter_by_user(self):
        m = DocUserRoleMap()
        m.define_role(_admin())
        m.define_role(_editor())
        m.assign("u1", "admin", now=1.0)
        m.assign("u2", "admin", now=2.0)
        m.assign("u1", "editor", now=3.0)
        filtered = m.history(user_id="u1")
        assert len(filtered) == 2
        assert all(e.user_id == "u1" for e in filtered)

    def test_filter_unknown_user(self):
        m = DocUserRoleMap()
        m.define_role(_admin())
        m.assign("u1", "admin")
        assert m.history(user_id="ghost") == []

    def test_history_returns_copies(self):
        m = DocUserRoleMap()
        m.define_role(_admin())
        m.assign("u1", "admin")
        h = m.history()
        h[0].role = "tampered"
        assert m.history()[0].role == "admin"


# ===================================================================== stats
class TestStats:
    def test_empty(self):
        m = DocUserRoleMap()
        s = m.stats()
        assert s.total_roles == 0
        assert s.total_users == 0
        assert s.role_counts == {}

    def test_totals(self):
        m = DocUserRoleMap()
        m.define_role(_admin())
        m.define_role(_editor())
        m.assign("u1", "admin")
        m.assign("u2", "editor")
        m.assign("u3", "admin")
        s = m.stats()
        assert s.total_roles == 2
        assert s.total_users == 3

    def test_role_counts(self):
        m = DocUserRoleMap()
        m.define_role(_admin())
        m.define_role(_editor())
        m.assign("u1", "admin")
        m.assign("u2", "admin")
        m.assign("u3", "editor")
        s = m.stats()
        assert s.role_counts["admin"] == 2
        assert s.role_counts["editor"] == 1

    def test_role_with_zero_users(self):
        m = DocUserRoleMap()
        m.define_role(_admin())
        m.define_role(_editor())
        m.assign("u1", "admin")
        s = m.stats()
        assert s.role_counts["editor"] == 0


# ===================================================================== thread-safety
class TestThreadSafety:
    def test_concurrent_assign(self):
        m = DocUserRoleMap()
        m.define_role(_admin())
        n_threads = 20
        per_thread = 50

        def worker(tid: int) -> None:
            for i in range(per_thread):
                m.assign(f"u-{tid}-{i}", "admin")

        threads = [threading.Thread(target=worker, args=(t,)) for t in range(n_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        # Each user is unique → total users == n_threads * per_thread
        assert m.stats().total_users == n_threads * per_thread
        assert m.stats().role_counts["admin"] == n_threads * per_thread
        assert len(m.history()) == n_threads * per_thread

    def test_concurrent_assign_same_user(self):
        m = DocUserRoleMap()
        m.define_role(_admin())
        m.define_role(_editor())

        def assign_admin() -> None:
            for _ in range(100):
                m.assign("u1", "admin")

        def assign_editor() -> None:
            for _ in range(100):
                m.assign("u1", "editor")

        t1 = threading.Thread(target=assign_admin)
        t2 = threading.Thread(target=assign_editor)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        # Idempotent on the role set; both roles should be present.
        assert sorted(m.roles_of("u1")) == ["admin", "editor"]
        assert len(m.history()) == 200

    def test_concurrent_assign_revoke(self):
        m = DocUserRoleMap()
        m.define_role(_admin())

        def assigner() -> None:
            for i in range(200):
                m.assign(f"u{i}", "admin")

        def revoker() -> None:
            for i in range(200):
                m.revoke(f"u{i}", "admin")

        ts = [threading.Thread(target=assigner) for _ in range(2)]
        ts += [threading.Thread(target=revoker) for _ in range(2)]
        for t in ts:
            t.start()
        for t in ts:
            t.join()
        # No crash, history captures all 400 assignments.
        assert len(m.history()) == 400
