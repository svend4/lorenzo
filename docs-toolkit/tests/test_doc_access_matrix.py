"""Tests for docstoolkit.doc_access_matrix (E284).

Coverage:
- Permission dataclass
- RolePolicy dataclass
- AccessDecision dataclass
- MatrixStats dataclass
- DocAccessMatrix: define_role, assign_role, revoke_role, grant, deny,
  revoke_explicit, check (explicit priority, role-based, default_deny),
  roles_for, principals_with_role, delete_role, delete_principal, stats
- Thread safety
"""

from __future__ import annotations

import threading
from dataclasses import fields

import pytest

from docstoolkit.doc_access_matrix import (
    AccessDecision,
    DocAccessMatrix,
    MatrixStats,
    Permission,
    RolePolicy,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_matrix() -> DocAccessMatrix:
    return DocAccessMatrix()


def matrix_with_reader_writer() -> DocAccessMatrix:
    m = make_matrix()
    m.define_role("reader", {"read": True, "write": False})
    m.define_role("writer", {"read": True, "write": True, "delete": False})
    return m


# ---------------------------------------------------------------------------
# Permission dataclass (6 tests)
# ---------------------------------------------------------------------------

class TestPermission:
    def test_action_stored(self):
        p = Permission(action="read", allowed=True)
        assert p.action == "read"

    def test_allowed_true(self):
        p = Permission(action="read", allowed=True)
        assert p.allowed is True

    def test_allowed_false(self):
        p = Permission(action="delete", allowed=False)
        assert p.allowed is False

    def test_action_arbitrary_string(self):
        p = Permission(action="publish", allowed=True)
        assert p.action == "publish"

    def test_is_dataclass(self):
        # dataclasses.fields works only on dataclass instances/types
        assert len(fields(Permission)) == 2

    def test_field_names(self):
        fnames = {f.name for f in fields(Permission)}
        assert fnames == {"action", "allowed"}


# ---------------------------------------------------------------------------
# RolePolicy dataclass (6 tests)
# ---------------------------------------------------------------------------

class TestRolePolicy:
    def test_role_stored(self):
        rp = RolePolicy(role="editor", permissions={"write": True})
        assert rp.role == "editor"

    def test_permissions_stored(self):
        rp = RolePolicy(role="editor", permissions={"write": True, "read": True})
        assert rp.permissions["write"] is True

    def test_permissions_default_empty(self):
        rp = RolePolicy(role="guest")
        assert rp.permissions == {}

    def test_is_dataclass(self):
        assert len(fields(RolePolicy)) == 2

    def test_field_names(self):
        fnames = {f.name for f in fields(RolePolicy)}
        assert fnames == {"role", "permissions"}

    def test_permissions_independent_instances(self):
        rp1 = RolePolicy(role="a")
        rp2 = RolePolicy(role="b")
        rp1.permissions["x"] = True
        assert "x" not in rp2.permissions


# ---------------------------------------------------------------------------
# AccessDecision dataclass (7 tests)
# ---------------------------------------------------------------------------

class TestAccessDecision:
    def test_principal_stored(self):
        d = AccessDecision(principal="alice", doc_id="d1", action="read", allowed=True, reason="explicit")
        assert d.principal == "alice"

    def test_doc_id_stored(self):
        d = AccessDecision(principal="alice", doc_id="doc42", action="read", allowed=True, reason="explicit")
        assert d.doc_id == "doc42"

    def test_action_stored(self):
        d = AccessDecision(principal="alice", doc_id="d1", action="write", allowed=False, reason="default_deny")
        assert d.action == "write"

    def test_allowed_true(self):
        d = AccessDecision(principal="u", doc_id="d", action="read", allowed=True, reason="role:admin")
        assert d.allowed is True

    def test_allowed_false(self):
        d = AccessDecision(principal="u", doc_id="d", action="delete", allowed=False, reason="default_deny")
        assert d.allowed is False

    def test_reason_stored(self):
        d = AccessDecision(principal="u", doc_id="d", action="read", allowed=True, reason="role:editor")
        assert d.reason == "role:editor"

    def test_is_dataclass(self):
        assert len(fields(AccessDecision)) == 5


# ---------------------------------------------------------------------------
# MatrixStats dataclass (5 tests)
# ---------------------------------------------------------------------------

class TestMatrixStats:
    def test_total_roles(self):
        s = MatrixStats(total_roles=3, total_principals=2, total_explicit_grants=1)
        assert s.total_roles == 3

    def test_total_principals(self):
        s = MatrixStats(total_roles=0, total_principals=5, total_explicit_grants=0)
        assert s.total_principals == 5

    def test_total_explicit_grants(self):
        s = MatrixStats(total_roles=1, total_principals=1, total_explicit_grants=7)
        assert s.total_explicit_grants == 7

    def test_zero_values(self):
        s = MatrixStats(total_roles=0, total_principals=0, total_explicit_grants=0)
        assert s.total_roles == 0
        assert s.total_principals == 0
        assert s.total_explicit_grants == 0

    def test_is_dataclass(self):
        assert len(fields(MatrixStats)) == 3


# ---------------------------------------------------------------------------
# define_role (7 tests)
# ---------------------------------------------------------------------------

class TestDefineRole:
    def test_returns_role_policy(self):
        m = make_matrix()
        rp = m.define_role("reader", {"read": True})
        assert isinstance(rp, RolePolicy)

    def test_role_name_in_result(self):
        m = make_matrix()
        rp = m.define_role("admin", {"read": True, "write": True})
        assert rp.role == "admin"

    def test_permissions_in_result(self):
        m = make_matrix()
        rp = m.define_role("editor", {"write": True, "read": False})
        assert rp.permissions["write"] is True
        assert rp.permissions["read"] is False

    def test_role_available_after_define(self):
        m = make_matrix()
        m.define_role("viewer", {"read": True})
        # role should be usable for assignment
        assert m.assign_role("alice", "viewer") is True

    def test_redefine_replaces_permissions(self):
        m = make_matrix()
        m.define_role("mod", {"read": True, "delete": False})
        m.define_role("mod", {"read": True, "delete": True})  # redefined
        m.assign_role("bob", "mod")
        decision = m.check("bob", "doc1", "delete")
        assert decision.allowed is True

    def test_multiple_roles_coexist(self):
        m = matrix_with_reader_writer()
        assert m.assign_role("alice", "reader") is True
        assert m.assign_role("alice", "writer") is True

    def test_permissions_copy_is_independent(self):
        m = make_matrix()
        perms = {"read": True}
        m.define_role("r", perms)
        perms["write"] = True  # mutate original dict
        m.assign_role("u", "r")
        decision = m.check("u", "d", "write")
        # stored copy should not be affected by external mutation
        assert decision.allowed is False


# ---------------------------------------------------------------------------
# assign_role / revoke_role (8 tests)
# ---------------------------------------------------------------------------

class TestAssignRevokeRole:
    def test_assign_returns_true_for_known_role(self):
        m = matrix_with_reader_writer()
        assert m.assign_role("alice", "reader") is True

    def test_assign_returns_false_for_unknown_role(self):
        m = make_matrix()
        assert m.assign_role("alice", "ghost") is False

    def test_assigned_role_visible_in_roles_for(self):
        m = matrix_with_reader_writer()
        m.assign_role("bob", "writer")
        assert "writer" in m.roles_for("bob")

    def test_assign_same_role_twice_idempotent(self):
        m = matrix_with_reader_writer()
        m.assign_role("alice", "reader")
        m.assign_role("alice", "reader")
        assert m.roles_for("alice").count("reader") == 1

    def test_revoke_returns_true_when_existed(self):
        m = matrix_with_reader_writer()
        m.assign_role("alice", "reader")
        assert m.revoke_role("alice", "reader") is True

    def test_revoke_returns_false_when_not_assigned(self):
        m = matrix_with_reader_writer()
        assert m.revoke_role("alice", "reader") is False

    def test_revoke_removes_role_from_roles_for(self):
        m = matrix_with_reader_writer()
        m.assign_role("alice", "reader")
        m.revoke_role("alice", "reader")
        assert "reader" not in m.roles_for("alice")

    def test_revoke_one_role_leaves_others(self):
        m = matrix_with_reader_writer()
        m.assign_role("alice", "reader")
        m.assign_role("alice", "writer")
        m.revoke_role("alice", "reader")
        assert "writer" in m.roles_for("alice")
        assert "reader" not in m.roles_for("alice")


# ---------------------------------------------------------------------------
# grant / deny / revoke_explicit (9 tests)
# ---------------------------------------------------------------------------

class TestExplicitPermissions:
    def test_grant_makes_check_allowed(self):
        m = make_matrix()
        m.grant("alice", "doc1", "read")
        d = m.check("alice", "doc1", "read")
        assert d.allowed is True

    def test_grant_reason_is_explicit(self):
        m = make_matrix()
        m.grant("alice", "doc1", "read")
        d = m.check("alice", "doc1", "read")
        assert d.reason == "explicit"

    def test_deny_makes_check_not_allowed(self):
        m = make_matrix()
        m.deny("alice", "doc1", "write")
        d = m.check("alice", "doc1", "write")
        assert d.allowed is False

    def test_deny_reason_is_explicit(self):
        m = make_matrix()
        m.deny("alice", "doc1", "write")
        d = m.check("alice", "doc1", "write")
        assert d.reason == "explicit"

    def test_explicit_deny_overrides_role(self):
        m = matrix_with_reader_writer()
        m.assign_role("alice", "reader")      # reader: read=True
        m.deny("alice", "doc1", "read")       # explicit deny
        d = m.check("alice", "doc1", "read")
        assert d.allowed is False
        assert d.reason == "explicit"

    def test_explicit_grant_overrides_role_deny(self):
        m = make_matrix()
        m.define_role("restricted", {"read": False})
        m.assign_role("bob", "restricted")
        m.grant("bob", "doc2", "read")
        d = m.check("bob", "doc2", "read")
        assert d.allowed is True
        assert d.reason == "explicit"

    def test_revoke_explicit_returns_true_when_existed(self):
        m = make_matrix()
        m.grant("alice", "doc1", "read")
        assert m.revoke_explicit("alice", "doc1", "read") is True

    def test_revoke_explicit_returns_false_when_not_present(self):
        m = make_matrix()
        assert m.revoke_explicit("alice", "doc1", "read") is False

    def test_revoke_explicit_removes_override(self):
        m = matrix_with_reader_writer()
        m.assign_role("alice", "reader")
        m.deny("alice", "doc1", "read")
        m.revoke_explicit("alice", "doc1", "read")
        # now falls back to role
        d = m.check("alice", "doc1", "read")
        assert d.allowed is True
        assert d.reason.startswith("role:")


# ---------------------------------------------------------------------------
# check — default_deny (4 tests)
# ---------------------------------------------------------------------------

class TestCheckDefaultDeny:
    def test_unknown_principal_default_deny(self):
        m = make_matrix()
        d = m.check("nobody", "doc1", "read")
        assert d.allowed is False
        assert d.reason == "default_deny"

    def test_principal_with_no_roles_default_deny(self):
        m = matrix_with_reader_writer()
        # principal exists but has no roles
        d = m.check("ghost", "doc1", "read")
        assert d.allowed is False
        assert d.reason == "default_deny"

    def test_role_without_action_default_deny(self):
        m = make_matrix()
        m.define_role("viewer", {"read": True})
        m.assign_role("alice", "viewer")
        d = m.check("alice", "doc1", "delete")
        assert d.allowed is False
        assert d.reason == "default_deny"

    def test_action_explicitly_false_in_role_default_deny(self):
        m = make_matrix()
        m.define_role("limited", {"read": False})
        m.assign_role("bob", "limited")
        d = m.check("bob", "doc1", "read")
        assert d.allowed is False
        # no role granted it, so default_deny
        assert d.reason == "default_deny"


# ---------------------------------------------------------------------------
# check — role-based (5 tests)
# ---------------------------------------------------------------------------

class TestCheckRoleBased:
    def test_single_role_allows(self):
        m = matrix_with_reader_writer()
        m.assign_role("alice", "reader")
        d = m.check("alice", "doc1", "read")
        assert d.allowed is True
        assert d.reason == "role:reader"

    def test_any_role_allows(self):
        m = matrix_with_reader_writer()
        m.assign_role("alice", "reader")
        m.assign_role("alice", "writer")
        d = m.check("alice", "doc1", "write")
        assert d.allowed is True
        assert d.reason.startswith("role:")

    def test_multiple_roles_none_grants_action(self):
        m = matrix_with_reader_writer()
        m.assign_role("alice", "reader")
        m.assign_role("alice", "writer")
        d = m.check("alice", "doc1", "publish")
        assert d.allowed is False

    def test_reason_contains_role_name(self):
        m = make_matrix()
        m.define_role("admin", {"delete": True})
        m.assign_role("root", "admin")
        d = m.check("root", "doc99", "delete")
        assert d.reason == "role:admin"

    def test_first_matching_role_used_alphabetically(self):
        m = make_matrix()
        m.define_role("alpha", {"read": True})
        m.define_role("beta", {"read": True})
        m.assign_role("u", "alpha")
        m.assign_role("u", "beta")
        d = m.check("u", "d", "read")
        # roles are evaluated in sorted order; "alpha" comes before "beta"
        assert d.reason == "role:alpha"


# ---------------------------------------------------------------------------
# roles_for / principals_with_role (6 tests)
# ---------------------------------------------------------------------------

class TestRolesForAndPrincipals:
    def test_roles_for_empty_principal(self):
        m = make_matrix()
        assert m.roles_for("nobody") == []

    def test_roles_for_single_role(self):
        m = matrix_with_reader_writer()
        m.assign_role("alice", "reader")
        assert m.roles_for("alice") == ["reader"]

    def test_roles_for_sorted(self):
        m = matrix_with_reader_writer()
        m.assign_role("alice", "writer")
        m.assign_role("alice", "reader")
        assert m.roles_for("alice") == ["reader", "writer"]

    def test_principals_with_role_empty(self):
        m = matrix_with_reader_writer()
        assert m.principals_with_role("reader") == []

    def test_principals_with_role_sorted(self):
        m = matrix_with_reader_writer()
        m.assign_role("charlie", "reader")
        m.assign_role("alice", "reader")
        m.assign_role("bob", "reader")
        assert m.principals_with_role("reader") == ["alice", "bob", "charlie"]

    def test_principals_with_role_unknown_role(self):
        m = make_matrix()
        assert m.principals_with_role("ghost") == []


# ---------------------------------------------------------------------------
# delete_role (6 tests)
# ---------------------------------------------------------------------------

class TestDeleteRole:
    def test_delete_returns_true_when_existed(self):
        m = matrix_with_reader_writer()
        assert m.delete_role("reader") is True

    def test_delete_returns_false_when_not_existed(self):
        m = make_matrix()
        assert m.delete_role("nonexistent") is False

    def test_deleted_role_cannot_be_assigned(self):
        m = matrix_with_reader_writer()
        m.delete_role("reader")
        assert m.assign_role("alice", "reader") is False

    def test_deleted_role_removed_from_principals(self):
        m = matrix_with_reader_writer()
        m.assign_role("alice", "reader")
        m.delete_role("reader")
        assert "reader" not in m.roles_for("alice")

    def test_deleted_role_permissions_no_longer_apply(self):
        m = matrix_with_reader_writer()
        m.assign_role("alice", "reader")
        m.delete_role("reader")
        d = m.check("alice", "doc1", "read")
        assert d.allowed is False

    def test_delete_only_removes_target_role(self):
        m = matrix_with_reader_writer()
        m.assign_role("alice", "reader")
        m.assign_role("alice", "writer")
        m.delete_role("reader")
        assert "writer" in m.roles_for("alice")
        d = m.check("alice", "doc1", "write")
        assert d.allowed is True


# ---------------------------------------------------------------------------
# delete_principal (6 tests)
# ---------------------------------------------------------------------------

class TestDeletePrincipal:
    def test_delete_removes_roles(self):
        m = matrix_with_reader_writer()
        m.assign_role("alice", "reader")
        m.delete_principal("alice")
        assert m.roles_for("alice") == []

    def test_delete_removes_explicit_grants(self):
        m = make_matrix()
        m.grant("alice", "doc1", "read")
        m.delete_principal("alice")
        d = m.check("alice", "doc1", "read")
        assert d.allowed is False

    def test_delete_removes_explicit_denies(self):
        m = matrix_with_reader_writer()
        m.assign_role("alice", "reader")
        m.deny("alice", "doc1", "read")
        m.delete_principal("alice")
        # role was also removed, so default_deny
        d = m.check("alice", "doc1", "read")
        assert d.reason == "default_deny"

    def test_delete_nonexistent_principal_no_error(self):
        m = make_matrix()
        m.delete_principal("ghost")  # should not raise

    def test_delete_does_not_affect_other_principals(self):
        m = matrix_with_reader_writer()
        m.assign_role("alice", "reader")
        m.assign_role("bob", "reader")
        m.delete_principal("alice")
        assert "reader" in m.roles_for("bob")

    def test_delete_principal_not_in_principals_with_role(self):
        m = matrix_with_reader_writer()
        m.assign_role("alice", "reader")
        m.delete_principal("alice")
        assert "alice" not in m.principals_with_role("reader")


# ---------------------------------------------------------------------------
# stats (5 tests)
# ---------------------------------------------------------------------------

class TestStats:
    def test_empty_matrix_stats(self):
        m = make_matrix()
        s = m.stats()
        assert s.total_roles == 0
        assert s.total_principals == 0
        assert s.total_explicit_grants == 0

    def test_stats_counts_roles(self):
        m = matrix_with_reader_writer()
        s = m.stats()
        assert s.total_roles == 2

    def test_stats_counts_principals(self):
        m = matrix_with_reader_writer()
        m.assign_role("alice", "reader")
        m.assign_role("bob", "writer")
        s = m.stats()
        assert s.total_principals == 2

    def test_stats_counts_explicit_grants_only(self):
        m = make_matrix()
        m.grant("alice", "doc1", "read")   # grant → counted
        m.deny("alice", "doc2", "write")   # deny → NOT counted
        s = m.stats()
        assert s.total_explicit_grants == 1

    def test_stats_returns_matrix_stats_instance(self):
        m = make_matrix()
        assert isinstance(m.stats(), MatrixStats)


# ---------------------------------------------------------------------------
# Thread safety (5 tests)
# ---------------------------------------------------------------------------

class TestThreadSafety:
    def test_concurrent_assign_roles(self):
        m = make_matrix()
        m.define_role("r", {"read": True})
        errors = []

        def worker(name: str) -> None:
            try:
                m.assign_role(name, "r")
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=worker, args=(f"user{i}",)) for i in range(50)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
        assert len(m.principals_with_role("r")) == 50

    def test_concurrent_grant_and_check(self):
        m = make_matrix()
        m.define_role("editor", {"write": True})
        m.assign_role("alice", "editor")
        results = []
        errors = []

        def granter() -> None:
            try:
                for i in range(20):
                    m.grant("alice", f"doc{i}", "read")
            except Exception as exc:
                errors.append(exc)

        def checker() -> None:
            try:
                for i in range(20):
                    d = m.check("alice", f"doc{i}", "write")
                    results.append(d.allowed)
            except Exception as exc:
                errors.append(exc)

        t1 = threading.Thread(target=granter)
        t2 = threading.Thread(target=checker)
        t1.start(); t2.start()
        t1.join(); t2.join()

        assert errors == []

    def test_concurrent_define_and_assign(self):
        m = make_matrix()
        errors = []

        def definer() -> None:
            try:
                for i in range(20):
                    m.define_role(f"role{i}", {"read": True})
            except Exception as exc:
                errors.append(exc)

        def assigner() -> None:
            try:
                for i in range(20):
                    m.assign_role(f"user{i}", f"role{i}")
            except Exception as exc:
                errors.append(exc)

        t1 = threading.Thread(target=definer)
        t2 = threading.Thread(target=assigner)
        t1.start(); t2.start()
        t1.join(); t2.join()

        assert errors == []

    def test_concurrent_delete_role(self):
        m = make_matrix()
        m.define_role("temp", {"read": True})
        errors = []

        def deleter() -> None:
            try:
                m.delete_role("temp")
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=deleter) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []

    def test_concurrent_grant_revoke(self):
        m = make_matrix()
        errors = []

        def worker(i: int) -> None:
            try:
                m.grant("alice", f"doc{i}", "read")
                m.revoke_explicit("alice", f"doc{i}", "read")
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(30)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []


# ---------------------------------------------------------------------------
# Integration / edge-case tests (6 tests)
# ---------------------------------------------------------------------------

class TestIntegration:
    def test_full_workflow(self):
        m = make_matrix()
        m.define_role("editor", {"read": True, "write": True})
        m.define_role("viewer", {"read": True})
        m.assign_role("alice", "editor")
        m.assign_role("bob", "viewer")

        assert m.check("alice", "doc1", "write").allowed is True
        assert m.check("bob", "doc1", "write").allowed is False
        assert m.check("bob", "doc1", "read").allowed is True

        m.deny("alice", "doc1", "write")
        assert m.check("alice", "doc1", "write").allowed is False

        m.revoke_explicit("alice", "doc1", "write")
        assert m.check("alice", "doc1", "write").allowed is True

    def test_stats_after_operations(self):
        m = make_matrix()
        m.define_role("r1", {"read": True})
        m.define_role("r2", {"write": True})
        m.assign_role("alice", "r1")
        m.assign_role("bob", "r1")
        m.grant("alice", "doc1", "delete")
        m.grant("bob", "doc2", "delete")
        m.deny("bob", "doc3", "read")  # deny not counted in explicit_grants
        s = m.stats()
        assert s.total_roles == 2
        assert s.total_principals == 2
        assert s.total_explicit_grants == 2

    def test_delete_role_updates_stats(self):
        m = matrix_with_reader_writer()
        m.delete_role("reader")
        s = m.stats()
        assert s.total_roles == 1

    def test_delete_principal_updates_stats(self):
        m = matrix_with_reader_writer()
        m.assign_role("alice", "reader")
        m.delete_principal("alice")
        # alice had an entry; after deletion the set is empty and the key is gone
        assert "alice" not in m.principals_with_role("reader")

    def test_overwrite_explicit_grant_with_deny(self):
        m = make_matrix()
        m.grant("alice", "doc1", "read")
        m.deny("alice", "doc1", "read")  # overwrite
        d = m.check("alice", "doc1", "read")
        assert d.allowed is False
        assert d.reason == "explicit"

    def test_principal_with_many_roles_any_grants(self):
        m = make_matrix()
        m.define_role("r1", {"read": False})
        m.define_role("r2", {"read": False})
        m.define_role("r3", {"read": True})
        m.assign_role("alice", "r1")
        m.assign_role("alice", "r2")
        m.assign_role("alice", "r3")
        d = m.check("alice", "doc1", "read")
        assert d.allowed is True
        assert d.reason == "role:r3"
