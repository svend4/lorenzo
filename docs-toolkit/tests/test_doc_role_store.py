"""Tests for E336 DocRoleStore."""
from __future__ import annotations

import threading
import time

import pytest

from docstoolkit.doc_role_store import (
    DocRoleStore,
    Role,
    RoleAssignment,
    RoleStats,
)


# ---------------------------------------------------------------- helpers
def _make_store_with_roles() -> DocRoleStore:
    store = DocRoleStore()
    store.define_role(Role(name="reader", permissions=["read"]))
    store.define_role(
        Role(name="writer", permissions=["read", "write"])
    )
    store.define_role(
        Role(name="admin", permissions=["read", "write", "delete"])
    )
    return store


# ---------------------------------------------------------------- dataclasses
class TestRoleDataclass:
    def test_minimal_role(self) -> None:
        role = Role(name="reader")
        assert role.name == "reader"
        assert role.permissions == []
        assert role.description == ""

    def test_role_with_permissions(self) -> None:
        role = Role(name="writer", permissions=["read", "write"])
        assert role.permissions == ["read", "write"]

    def test_role_with_description(self) -> None:
        role = Role(name="admin", description="full access")
        assert role.description == "full access"

    def test_role_default_permissions_independent(self) -> None:
        a = Role(name="a")
        b = Role(name="b")
        a.permissions.append("read")
        assert b.permissions == []

    def test_role_equality(self) -> None:
        assert Role(name="r", permissions=["read"]) == Role(
            name="r", permissions=["read"]
        )


class TestRoleAssignmentDataclass:
    def test_minimal_assignment(self) -> None:
        assignment = RoleAssignment(
            doc_id="doc1", user_id="u1", role_name="reader"
        )
        assert assignment.doc_id == "doc1"
        assert assignment.user_id == "u1"
        assert assignment.role_name == "reader"
        assert assignment.assigned_at == 0.0
        assert assignment.assigned_by == ""

    def test_full_assignment(self) -> None:
        assignment = RoleAssignment(
            doc_id="d",
            user_id="u",
            role_name="r",
            assigned_at=10.5,
            assigned_by="admin",
        )
        assert assignment.assigned_at == 10.5
        assert assignment.assigned_by == "admin"

    def test_assignment_equality(self) -> None:
        a = RoleAssignment(doc_id="d", user_id="u", role_name="r")
        b = RoleAssignment(doc_id="d", user_id="u", role_name="r")
        assert a == b


class TestRoleStatsDataclass:
    def test_construct(self) -> None:
        stats = RoleStats(
            total_roles=3,
            total_assignments=10,
            unique_users=4,
            unique_docs=5,
        )
        assert stats.total_roles == 3
        assert stats.total_assignments == 10
        assert stats.unique_users == 4
        assert stats.unique_docs == 5

    def test_equality(self) -> None:
        assert RoleStats(1, 2, 3, 4) == RoleStats(1, 2, 3, 4)


# ---------------------------------------------------------------- construction
class TestConstruction:
    def test_default_state(self) -> None:
        store = DocRoleStore()
        assert store.list_roles() == []
        assert store.stats().total_roles == 0
        assert store.stats().total_assignments == 0

    def test_independent_instances(self) -> None:
        s1 = DocRoleStore()
        s2 = DocRoleStore()
        s1.define_role(Role(name="reader"))
        assert s2.list_roles() == []


# ---------------------------------------------------------------- define_role
class TestDefineRole:
    def test_define_new_role(self) -> None:
        store = DocRoleStore()
        store.define_role(Role(name="reader", permissions=["read"]))
        assert store.get_role("reader") is not None
        assert store.get_role("reader").permissions == ["read"]

    def test_replace_existing_role(self) -> None:
        store = DocRoleStore()
        store.define_role(Role(name="reader", permissions=["read"]))
        store.define_role(
            Role(name="reader", permissions=["read", "comment"])
        )
        role = store.get_role("reader")
        assert role.permissions == ["read", "comment"]

    def test_define_role_with_description(self) -> None:
        store = DocRoleStore()
        store.define_role(Role(name="admin", description="full"))
        assert store.get_role("admin").description == "full"

    def test_define_role_does_not_affect_assignments(self) -> None:
        store = _make_store_with_roles()
        store.assign("d1", "u1", "writer")
        # Redefine writer with new permissions
        store.define_role(
            Role(name="writer", permissions=["read", "write", "publish"])
        )
        # Existing assignment still uses the role name; reads new perms
        assert store.has_permission("u1", "d1", "publish") is True


# ---------------------------------------------------------------- undefine
class TestUndefineRole:
    def test_undefine_existing_returns_true(self) -> None:
        store = _make_store_with_roles()
        assert store.undefine_role("reader") is True
        assert store.get_role("reader") is None

    def test_undefine_missing_returns_false(self) -> None:
        store = DocRoleStore()
        assert store.undefine_role("ghost") is False

    def test_undefine_removes_assignments(self) -> None:
        store = _make_store_with_roles()
        store.assign("d1", "u1", "writer")
        store.assign("d2", "u2", "writer")
        store.assign("d3", "u3", "reader")
        assert store.undefine_role("writer") is True
        assert store.get_assignment("d1", "u1") is None
        assert store.get_assignment("d2", "u2") is None
        # Other roles' assignments survive
        assert store.get_assignment("d3", "u3") is not None

    def test_undefine_updates_stats(self) -> None:
        store = _make_store_with_roles()
        store.assign("d1", "u1", "writer")
        store.assign("d2", "u2", "writer")
        store.undefine_role("writer")
        assert store.stats().total_assignments == 0


# ---------------------------------------------------------------- get_role
class TestGetRole:
    def test_get_found(self) -> None:
        store = _make_store_with_roles()
        role = store.get_role("admin")
        assert role is not None
        assert role.name == "admin"

    def test_get_missing(self) -> None:
        store = DocRoleStore()
        assert store.get_role("nope") is None


# ---------------------------------------------------------------- list_roles
class TestListRoles:
    def test_empty(self) -> None:
        assert DocRoleStore().list_roles() == []

    def test_sorted_by_name(self) -> None:
        store = DocRoleStore()
        store.define_role(Role(name="zeta"))
        store.define_role(Role(name="alpha"))
        store.define_role(Role(name="mu"))
        names = [r.name for r in store.list_roles()]
        assert names == ["alpha", "mu", "zeta"]


# ---------------------------------------------------------------- assign
class TestAssign:
    def test_assign_creates_new(self) -> None:
        store = _make_store_with_roles()
        a = store.assign("d1", "u1", "reader")
        assert isinstance(a, RoleAssignment)
        assert a.doc_id == "d1"
        assert a.user_id == "u1"
        assert a.role_name == "reader"

    def test_assign_returns_none_for_undefined_role(self) -> None:
        store = DocRoleStore()
        result = store.assign("d", "u", "ghost")
        assert result is None
        assert store.stats().total_assignments == 0

    def test_assign_replaces_existing(self) -> None:
        store = _make_store_with_roles()
        store.assign("d1", "u1", "reader")
        store.assign("d1", "u1", "writer")
        a = store.get_assignment("d1", "u1")
        assert a.role_name == "writer"
        assert store.stats().total_assignments == 1

    def test_assign_with_assigned_by(self) -> None:
        store = _make_store_with_roles()
        a = store.assign("d1", "u1", "reader", assigned_by="root")
        assert a.assigned_by == "root"

    def test_assign_with_explicit_now(self) -> None:
        store = _make_store_with_roles()
        a = store.assign("d1", "u1", "reader", now=123.45)
        assert a.assigned_at == 123.45

    def test_assign_default_now_uses_clock(self) -> None:
        store = _make_store_with_roles()
        before = time.time()
        a = store.assign("d1", "u1", "reader")
        after = time.time()
        assert before <= a.assigned_at <= after


# ---------------------------------------------------------------- unassign
class TestUnassign:
    def test_unassign_existing(self) -> None:
        store = _make_store_with_roles()
        store.assign("d1", "u1", "reader")
        assert store.unassign("d1", "u1") is True
        assert store.get_assignment("d1", "u1") is None

    def test_unassign_missing(self) -> None:
        store = _make_store_with_roles()
        assert store.unassign("d1", "u1") is False

    def test_unassign_only_targets_one(self) -> None:
        store = _make_store_with_roles()
        store.assign("d1", "u1", "reader")
        store.assign("d1", "u2", "reader")
        store.unassign("d1", "u1")
        assert store.get_assignment("d1", "u2") is not None


# ---------------------------------------------------------------- get_assignment
class TestGetAssignment:
    def test_found(self) -> None:
        store = _make_store_with_roles()
        store.assign("d1", "u1", "writer")
        a = store.get_assignment("d1", "u1")
        assert a is not None
        assert a.role_name == "writer"

    def test_missing(self) -> None:
        store = _make_store_with_roles()
        assert store.get_assignment("nodoc", "nouser") is None


# ---------------------------------------------------------------- users_for_doc
class TestUsersForDoc:
    def test_sorted(self) -> None:
        store = _make_store_with_roles()
        store.assign("d1", "zoe", "reader")
        store.assign("d1", "alice", "reader")
        store.assign("d1", "bob", "writer")
        assert store.users_for_doc("d1") == ["alice", "bob", "zoe"]

    def test_empty(self) -> None:
        store = _make_store_with_roles()
        assert store.users_for_doc("none") == []

    def test_isolated_per_doc(self) -> None:
        store = _make_store_with_roles()
        store.assign("d1", "u1", "reader")
        store.assign("d2", "u2", "reader")
        assert store.users_for_doc("d1") == ["u1"]


# ---------------------------------------------------------------- docs_for_user
class TestDocsForUser:
    def test_sorted(self) -> None:
        store = _make_store_with_roles()
        store.assign("zebra", "u1", "reader")
        store.assign("apple", "u1", "writer")
        store.assign("mango", "u1", "reader")
        assert store.docs_for_user("u1") == ["apple", "mango", "zebra"]

    def test_empty(self) -> None:
        store = _make_store_with_roles()
        assert store.docs_for_user("ghost") == []

    def test_isolated_per_user(self) -> None:
        store = _make_store_with_roles()
        store.assign("d1", "u1", "reader")
        store.assign("d2", "u2", "reader")
        assert store.docs_for_user("u2") == ["d2"]


# ---------------------------------------------------------------- users_with_permission
class TestUsersWithPermission:
    def test_filters_by_permission(self) -> None:
        store = _make_store_with_roles()
        store.assign("d1", "u_read", "reader")
        store.assign("d1", "u_write", "writer")
        store.assign("d1", "u_admin", "admin")
        assert store.users_with_permission("d1", "read") == [
            "u_admin",
            "u_read",
            "u_write",
        ]
        assert store.users_with_permission("d1", "write") == [
            "u_admin",
            "u_write",
        ]
        assert store.users_with_permission("d1", "delete") == ["u_admin"]

    def test_empty_for_missing_doc(self) -> None:
        store = _make_store_with_roles()
        assert store.users_with_permission("none", "read") == []

    def test_empty_for_unknown_permission(self) -> None:
        store = _make_store_with_roles()
        store.assign("d1", "u1", "reader")
        assert store.users_with_permission("d1", "publish") == []


# ---------------------------------------------------------------- has_permission
class TestHasPermission:
    def test_true_when_granted(self) -> None:
        store = _make_store_with_roles()
        store.assign("d1", "u1", "writer")
        assert store.has_permission("u1", "d1", "read") is True
        assert store.has_permission("u1", "d1", "write") is True

    def test_false_when_not_granted(self) -> None:
        store = _make_store_with_roles()
        store.assign("d1", "u1", "reader")
        assert store.has_permission("u1", "d1", "write") is False

    def test_false_when_no_assignment(self) -> None:
        store = _make_store_with_roles()
        assert store.has_permission("u1", "d1", "read") is False

    def test_false_when_role_removed(self) -> None:
        store = _make_store_with_roles()
        store.assign("d1", "u1", "reader")
        # Sneak-remove the role from the underlying map (simulating race);
        # supported path: undefine_role wipes assignments too, so use that.
        store.undefine_role("reader")
        assert store.has_permission("u1", "d1", "read") is False


# ---------------------------------------------------------------- assignments_for_role
class TestAssignmentsForRole:
    def test_sorted(self) -> None:
        store = _make_store_with_roles()
        store.assign("zdoc", "u1", "reader")
        store.assign("adoc", "u2", "reader")
        store.assign("adoc", "u1", "reader")
        assignments = store.assignments_for_role("reader")
        keys = [(a.doc_id, a.user_id) for a in assignments]
        assert keys == [("adoc", "u1"), ("adoc", "u2"), ("zdoc", "u1")]

    def test_empty_for_unknown_role(self) -> None:
        store = _make_store_with_roles()
        assert store.assignments_for_role("ghost") == []

    def test_only_matching_role(self) -> None:
        store = _make_store_with_roles()
        store.assign("d1", "u1", "reader")
        store.assign("d2", "u2", "writer")
        assert len(store.assignments_for_role("reader")) == 1
        assert len(store.assignments_for_role("writer")) == 1


# ---------------------------------------------------------------- clear_doc
class TestClearDoc:
    def test_returns_count(self) -> None:
        store = _make_store_with_roles()
        store.assign("d1", "u1", "reader")
        store.assign("d1", "u2", "writer")
        store.assign("d2", "u1", "reader")
        assert store.clear_doc("d1") == 2

    def test_zero_for_missing_doc(self) -> None:
        store = _make_store_with_roles()
        assert store.clear_doc("none") == 0

    def test_does_not_touch_other_docs(self) -> None:
        store = _make_store_with_roles()
        store.assign("d1", "u1", "reader")
        store.assign("d2", "u1", "reader")
        store.clear_doc("d1")
        assert store.get_assignment("d2", "u1") is not None


# ---------------------------------------------------------------- clear_user
class TestClearUser:
    def test_returns_count(self) -> None:
        store = _make_store_with_roles()
        store.assign("d1", "u1", "reader")
        store.assign("d2", "u1", "writer")
        store.assign("d1", "u2", "reader")
        assert store.clear_user("u1") == 2

    def test_zero_for_missing_user(self) -> None:
        store = _make_store_with_roles()
        assert store.clear_user("ghost") == 0

    def test_does_not_touch_other_users(self) -> None:
        store = _make_store_with_roles()
        store.assign("d1", "u1", "reader")
        store.assign("d1", "u2", "reader")
        store.clear_user("u1")
        assert store.get_assignment("d1", "u2") is not None


# ---------------------------------------------------------------- stats
class TestStats:
    def test_empty_store(self) -> None:
        stats = DocRoleStore().stats()
        assert stats == RoleStats(0, 0, 0, 0)

    def test_counts_roles(self) -> None:
        store = _make_store_with_roles()
        assert store.stats().total_roles == 3

    def test_counts_assignments_and_uniques(self) -> None:
        store = _make_store_with_roles()
        store.assign("d1", "u1", "reader")
        store.assign("d1", "u2", "writer")
        store.assign("d2", "u1", "admin")
        stats = store.stats()
        assert stats.total_assignments == 3
        assert stats.unique_users == 2
        assert stats.unique_docs == 2

    def test_replacement_does_not_inflate_count(self) -> None:
        store = _make_store_with_roles()
        store.assign("d1", "u1", "reader")
        store.assign("d1", "u1", "writer")
        assert store.stats().total_assignments == 1


# ---------------------------------------------------------------- thread safety
class TestThreadSafety:
    def test_concurrent_assigns(self) -> None:
        store = DocRoleStore()
        store.define_role(Role(name="reader", permissions=["read"]))

        n_threads = 8
        per_thread = 50
        errors: list[BaseException] = []

        def worker(idx: int) -> None:
            try:
                for i in range(per_thread):
                    store.assign(f"doc{idx}", f"user{i}", "reader")
            except BaseException as exc:  # pragma: no cover - sanity
                errors.append(exc)

        threads = [
            threading.Thread(target=worker, args=(t,))
            for t in range(n_threads)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
        stats = store.stats()
        assert stats.total_assignments == n_threads * per_thread
        assert stats.unique_docs == n_threads
        assert stats.unique_users == per_thread

    def test_concurrent_assign_and_unassign(self) -> None:
        store = DocRoleStore()
        store.define_role(Role(name="reader", permissions=["read"]))

        def assigner() -> None:
            for i in range(200):
                store.assign("d", f"u{i}", "reader")

        def unassigner() -> None:
            for i in range(200):
                store.unassign("d", f"u{i}")

        threads = [
            threading.Thread(target=assigner),
            threading.Thread(target=unassigner),
            threading.Thread(target=assigner),
            threading.Thread(target=unassigner),
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # No crashes is the main outcome; state is consistent.
        stats = store.stats()
        assert stats.total_assignments >= 0
        assert stats.total_roles == 1
