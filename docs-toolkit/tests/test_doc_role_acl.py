"""Tests for the ``doc_role_acl`` module (E190)."""
from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_role_acl import (
    AccessResult,
    Acl,
    DocRoleAcl,
    Permission,
    Role,
    User,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def acl_mgr() -> DocRoleAcl:
    """Fresh DocRoleAcl with a couple of common roles defined."""
    mgr = DocRoleAcl()
    mgr.define_role("editor", {Permission.READ, Permission.WRITE})
    mgr.define_role("viewer", {Permission.READ})
    mgr.define_role("admin", {Permission.ADMIN})
    mgr.set_owner("doc1", "alice")
    return mgr


# ---------------------------------------------------------------------------
# TestPermission
# ---------------------------------------------------------------------------


class TestPermission:
    def test_members(self) -> None:
        names = {p.name for p in Permission}
        assert names == {"READ", "WRITE", "DELETE", "SHARE", "ADMIN"}

    def test_values_are_lowercase(self) -> None:
        assert Permission.READ.value == "read"
        assert Permission.ADMIN.value == "admin"

    def test_distinct(self) -> None:
        assert Permission.READ != Permission.WRITE

    def test_hashable(self) -> None:
        s = {Permission.READ, Permission.READ, Permission.WRITE}
        assert s == {Permission.READ, Permission.WRITE}


# ---------------------------------------------------------------------------
# TestRole
# ---------------------------------------------------------------------------


class TestRole:
    def test_default_factory(self) -> None:
        r = Role(name="r")
        assert r.permissions == set()
        assert r.description == ""

    def test_with_perms(self) -> None:
        r = Role(name="ed", permissions={Permission.READ})
        assert Permission.READ in r.permissions

    def test_description(self) -> None:
        r = Role(name="x", description="hello")
        assert r.description == "hello"

    def test_independent_default_factories(self) -> None:
        a = Role(name="a")
        b = Role(name="b")
        a.permissions.add(Permission.READ)
        assert Permission.READ not in b.permissions


# ---------------------------------------------------------------------------
# TestUser
# ---------------------------------------------------------------------------


class TestUser:
    def test_default(self) -> None:
        u = User(user_id="alice")
        assert u.roles == set()

    def test_with_roles(self) -> None:
        u = User(user_id="bob", roles={"editor"})
        assert "editor" in u.roles

    def test_independent_default_factories(self) -> None:
        a = User(user_id="a")
        b = User(user_id="b")
        a.roles.add("editor")
        assert "editor" not in b.roles


# ---------------------------------------------------------------------------
# TestAcl
# ---------------------------------------------------------------------------


class TestAcl:
    def test_defaults(self) -> None:
        a = Acl(doc_id="d", owner="alice")
        assert a.doc_id == "d"
        assert a.owner == "alice"
        assert a.role_grants == {}
        assert a.user_grants == {}
        assert a.public_perms == set()

    def test_independent_factories(self) -> None:
        a = Acl(doc_id="d1", owner="a")
        b = Acl(doc_id="d2", owner="b")
        a.user_grants["x"] = {Permission.READ}
        assert "x" not in b.user_grants


# ---------------------------------------------------------------------------
# TestAccessResult
# ---------------------------------------------------------------------------


class TestAccessResult:
    def test_allowed(self) -> None:
        r = AccessResult(allowed=True, reason="ok", via="owner")
        assert r.allowed and r.via == "owner"

    def test_denied_default_via_is_none(self) -> None:
        r = AccessResult(allowed=False, reason="nope")
        assert r.via is None


# ---------------------------------------------------------------------------
# TestDefineRole
# ---------------------------------------------------------------------------


class TestDefineRole:
    def test_define_returns_role(self) -> None:
        mgr = DocRoleAcl()
        role = mgr.define_role("ed", {Permission.READ})
        assert isinstance(role, Role)
        assert role.name == "ed"

    def test_define_stores_role(self) -> None:
        mgr = DocRoleAcl()
        mgr.define_role("ed", {Permission.READ}, description="Editors")
        # We can assign it -> exists.
        assert mgr.assign_role("alice", "ed") is True

    def test_redefine_overwrites(self) -> None:
        mgr = DocRoleAcl()
        mgr.define_role("ed", {Permission.READ})
        mgr.define_role("ed", {Permission.WRITE})
        mgr.assign_role("alice", "ed")
        mgr.set_owner("d", "owner")
        mgr.grant_role("d", "ed", {Permission.WRITE})
        # Old perms not present (we replaced role definition).
        # The role's stored set should be {WRITE} only; we can't see it
        # directly but we can verify behavior via effective_permissions.
        # (Permissions on docs are tracked separately, so this is more of a
        # sanity check that redefining doesn't raise.)
        assert mgr.has_permission("alice", "d", Permission.WRITE)


# ---------------------------------------------------------------------------
# TestRemoveRole
# ---------------------------------------------------------------------------


class TestRemoveRole:
    def test_remove_existing(self) -> None:
        mgr = DocRoleAcl()
        mgr.define_role("ed", {Permission.READ})
        assert mgr.remove_role("ed") is True

    def test_remove_missing(self) -> None:
        mgr = DocRoleAcl()
        assert mgr.remove_role("nope") is False

    def test_remove_unassigns_users(self) -> None:
        mgr = DocRoleAcl()
        mgr.define_role("ed", {Permission.READ})
        mgr.assign_role("alice", "ed")
        mgr.remove_role("ed")
        # Re-define then re-assign should still work cleanly.
        mgr.define_role("ed", {Permission.READ})
        assert mgr.assign_role("alice", "ed") is True

    def test_remove_revokes_acl_grants(self) -> None:
        mgr = DocRoleAcl()
        mgr.define_role("ed", {Permission.WRITE})
        mgr.set_owner("d", "owner")
        mgr.grant_role("d", "ed", {Permission.WRITE})
        mgr.assign_role("alice", "ed")
        assert mgr.has_permission("alice", "d", Permission.WRITE)
        mgr.remove_role("ed")
        # After removal, the role is no longer in acl.role_grants and the
        # user no longer has the role: no permission.
        assert not mgr.has_permission("alice", "d", Permission.WRITE)


# ---------------------------------------------------------------------------
# TestAssignRevokeRole
# ---------------------------------------------------------------------------


class TestAssignRevokeRole:
    def test_assign_unknown_role(self) -> None:
        mgr = DocRoleAcl()
        assert mgr.assign_role("alice", "ghost") is False

    def test_assign_known(self, acl_mgr: DocRoleAcl) -> None:
        assert acl_mgr.assign_role("bob", "editor") is True

    def test_assign_idempotent(self, acl_mgr: DocRoleAcl) -> None:
        acl_mgr.assign_role("bob", "editor")
        assert acl_mgr.assign_role("bob", "editor") is True

    def test_revoke_unknown_user(self, acl_mgr: DocRoleAcl) -> None:
        assert acl_mgr.revoke_role("ghost", "editor") is False

    def test_revoke_role_not_held(self, acl_mgr: DocRoleAcl) -> None:
        acl_mgr.assign_role("bob", "editor")
        assert acl_mgr.revoke_role("bob", "viewer") is False

    def test_revoke_success(self, acl_mgr: DocRoleAcl) -> None:
        acl_mgr.assign_role("bob", "editor")
        assert acl_mgr.revoke_role("bob", "editor") is True


# ---------------------------------------------------------------------------
# TestGrantUser
# ---------------------------------------------------------------------------


class TestGrantUser:
    def test_grant_creates_acl_when_missing(self) -> None:
        mgr = DocRoleAcl()
        mgr.grant_user("d", "bob", {Permission.READ})
        acl = mgr.acl_for("d")
        assert acl is not None
        assert acl.user_grants["bob"] == {Permission.READ}

    def test_grant_unions(self, acl_mgr: DocRoleAcl) -> None:
        acl_mgr.grant_user("doc1", "bob", {Permission.READ})
        acl_mgr.grant_user("doc1", "bob", {Permission.WRITE})
        assert acl_mgr.acl_for("doc1").user_grants["bob"] == {
            Permission.READ,
            Permission.WRITE,
        }


# ---------------------------------------------------------------------------
# TestGrantRole
# ---------------------------------------------------------------------------


class TestGrantRole:
    def test_grant_creates_acl(self) -> None:
        mgr = DocRoleAcl()
        mgr.grant_role("d", "editor", {Permission.WRITE})
        assert mgr.acl_for("d").role_grants["editor"] == {Permission.WRITE}

    def test_grant_unions(self, acl_mgr: DocRoleAcl) -> None:
        acl_mgr.grant_role("doc1", "viewer", {Permission.READ})
        acl_mgr.grant_role("doc1", "viewer", {Permission.SHARE})
        assert acl_mgr.acl_for("doc1").role_grants["viewer"] == {
            Permission.READ,
            Permission.SHARE,
        }


# ---------------------------------------------------------------------------
# TestGrantPublic
# ---------------------------------------------------------------------------


class TestGrantPublic:
    def test_grant_creates_acl(self) -> None:
        mgr = DocRoleAcl()
        mgr.grant_public("d", {Permission.READ})
        assert mgr.acl_for("d").public_perms == {Permission.READ}

    def test_grant_unions(self, acl_mgr: DocRoleAcl) -> None:
        acl_mgr.grant_public("doc1", {Permission.READ})
        acl_mgr.grant_public("doc1", {Permission.SHARE})
        assert acl_mgr.acl_for("doc1").public_perms == {
            Permission.READ,
            Permission.SHARE,
        }


# ---------------------------------------------------------------------------
# TestRevoke
# ---------------------------------------------------------------------------


class TestRevoke:
    def test_revoke_user_all(self, acl_mgr: DocRoleAcl) -> None:
        acl_mgr.grant_user("doc1", "bob", {Permission.READ, Permission.WRITE})
        assert acl_mgr.revoke_user("doc1", "bob") is True
        assert "bob" not in acl_mgr.acl_for("doc1").user_grants

    def test_revoke_user_specific(self, acl_mgr: DocRoleAcl) -> None:
        acl_mgr.grant_user("doc1", "bob", {Permission.READ, Permission.WRITE})
        assert acl_mgr.revoke_user("doc1", "bob", {Permission.READ}) is True
        assert acl_mgr.acl_for("doc1").user_grants["bob"] == {Permission.WRITE}

    def test_revoke_user_specific_all(self, acl_mgr: DocRoleAcl) -> None:
        acl_mgr.grant_user("doc1", "bob", {Permission.READ})
        acl_mgr.revoke_user("doc1", "bob", {Permission.READ})
        # Empty entry should be removed entirely.
        assert "bob" not in acl_mgr.acl_for("doc1").user_grants

    def test_revoke_user_missing_doc(self, acl_mgr: DocRoleAcl) -> None:
        assert acl_mgr.revoke_user("ghost", "bob") is False

    def test_revoke_user_missing_user(self, acl_mgr: DocRoleAcl) -> None:
        assert acl_mgr.revoke_user("doc1", "nobody") is False

    def test_revoke_role_all(self, acl_mgr: DocRoleAcl) -> None:
        acl_mgr.grant_role("doc1", "editor", {Permission.WRITE})
        assert acl_mgr.revoke_role("doc1", "editor") is True
        assert "editor" not in acl_mgr.acl_for("doc1").role_grants

    def test_revoke_role_specific(self, acl_mgr: DocRoleAcl) -> None:
        acl_mgr.grant_role(
            "doc1", "editor", {Permission.READ, Permission.WRITE}
        )
        acl_mgr.revoke_role("doc1", "editor", {Permission.READ})
        assert acl_mgr.acl_for("doc1").role_grants["editor"] == {Permission.WRITE}

    def test_revoke_role_specific_emptied(self, acl_mgr: DocRoleAcl) -> None:
        acl_mgr.grant_role("doc1", "editor", {Permission.WRITE})
        acl_mgr.revoke_role("doc1", "editor", {Permission.WRITE})
        assert "editor" not in acl_mgr.acl_for("doc1").role_grants

    def test_revoke_role_missing(self, acl_mgr: DocRoleAcl) -> None:
        assert acl_mgr.revoke_role("doc1", "ghost") is False


# ---------------------------------------------------------------------------
# TestSetOwner
# ---------------------------------------------------------------------------


class TestSetOwner:
    def test_set_owner_creates_acl(self) -> None:
        mgr = DocRoleAcl()
        acl = mgr.set_owner("d", "alice")
        assert isinstance(acl, Acl)
        assert acl.owner == "alice"
        assert mgr.acl_for("d").owner == "alice"

    def test_set_owner_updates_existing(self, acl_mgr: DocRoleAcl) -> None:
        acl_mgr.set_owner("doc1", "bob")
        assert acl_mgr.acl_for("doc1").owner == "bob"

    def test_set_owner_preserves_grants(self, acl_mgr: DocRoleAcl) -> None:
        acl_mgr.grant_user("doc1", "carol", {Permission.READ})
        acl_mgr.set_owner("doc1", "bob")
        assert "carol" in acl_mgr.acl_for("doc1").user_grants


# ---------------------------------------------------------------------------
# TestCheckOwner
# ---------------------------------------------------------------------------


class TestCheckOwner:
    def test_owner_has_read(self, acl_mgr: DocRoleAcl) -> None:
        result = acl_mgr.check("alice", "doc1", Permission.READ)
        assert result.allowed and result.via == "owner"

    def test_owner_has_admin(self, acl_mgr: DocRoleAcl) -> None:
        assert acl_mgr.has_permission("alice", "doc1", Permission.ADMIN)

    def test_owner_has_delete(self, acl_mgr: DocRoleAcl) -> None:
        assert acl_mgr.has_permission("alice", "doc1", Permission.DELETE)


# ---------------------------------------------------------------------------
# TestCheckUserGrant
# ---------------------------------------------------------------------------


class TestCheckUserGrant:
    def test_user_grant_allows(self, acl_mgr: DocRoleAcl) -> None:
        acl_mgr.grant_user("doc1", "bob", {Permission.READ})
        result = acl_mgr.check("bob", "doc1", Permission.READ)
        assert result.allowed and result.via == "user_grant"

    def test_user_grant_does_not_imply_other(self, acl_mgr: DocRoleAcl) -> None:
        acl_mgr.grant_user("doc1", "bob", {Permission.READ})
        assert not acl_mgr.has_permission("bob", "doc1", Permission.WRITE)

    def test_user_grant_for_unrelated_user(self, acl_mgr: DocRoleAcl) -> None:
        acl_mgr.grant_user("doc1", "bob", {Permission.READ})
        assert not acl_mgr.has_permission("carol", "doc1", Permission.READ)


# ---------------------------------------------------------------------------
# TestCheckRoleGrant
# ---------------------------------------------------------------------------


class TestCheckRoleGrant:
    def test_role_grant_allows(self, acl_mgr: DocRoleAcl) -> None:
        acl_mgr.grant_role("doc1", "viewer", {Permission.READ})
        acl_mgr.assign_role("bob", "viewer")
        result = acl_mgr.check("bob", "doc1", Permission.READ)
        assert result.allowed and result.via == "role_grant:viewer"

    def test_role_grant_requires_role_assignment(
        self, acl_mgr: DocRoleAcl
    ) -> None:
        acl_mgr.grant_role("doc1", "viewer", {Permission.READ})
        # bob has no role assigned.
        assert not acl_mgr.has_permission("bob", "doc1", Permission.READ)

    def test_user_with_multiple_roles(self, acl_mgr: DocRoleAcl) -> None:
        acl_mgr.grant_role("doc1", "viewer", {Permission.READ})
        acl_mgr.grant_role("doc1", "editor", {Permission.WRITE})
        acl_mgr.assign_role("bob", "viewer")
        acl_mgr.assign_role("bob", "editor")
        assert acl_mgr.has_permission("bob", "doc1", Permission.READ)
        assert acl_mgr.has_permission("bob", "doc1", Permission.WRITE)


# ---------------------------------------------------------------------------
# TestCheckPublic
# ---------------------------------------------------------------------------


class TestCheckPublic:
    def test_public_allows_anyone(self, acl_mgr: DocRoleAcl) -> None:
        acl_mgr.grant_public("doc1", {Permission.READ})
        result = acl_mgr.check("stranger", "doc1", Permission.READ)
        assert result.allowed and result.via == "public"

    def test_public_does_not_imply_others(self, acl_mgr: DocRoleAcl) -> None:
        acl_mgr.grant_public("doc1", {Permission.READ})
        assert not acl_mgr.has_permission("stranger", "doc1", Permission.WRITE)


# ---------------------------------------------------------------------------
# TestAdminImpliesAll
# ---------------------------------------------------------------------------


class TestAdminImpliesAll:
    def test_admin_user_grant_implies_all(self, acl_mgr: DocRoleAcl) -> None:
        acl_mgr.grant_user("doc1", "bob", {Permission.ADMIN})
        for p in Permission:
            assert acl_mgr.has_permission("bob", "doc1", p)

    def test_admin_role_grant_implies_all(self, acl_mgr: DocRoleAcl) -> None:
        acl_mgr.grant_role("doc1", "admin", {Permission.ADMIN})
        acl_mgr.assign_role("bob", "admin")
        for p in Permission:
            assert acl_mgr.has_permission("bob", "doc1", p)

    def test_admin_public_implies_all(self, acl_mgr: DocRoleAcl) -> None:
        acl_mgr.grant_public("doc1", {Permission.ADMIN})
        for p in Permission:
            assert acl_mgr.has_permission("stranger", "doc1", p)


# ---------------------------------------------------------------------------
# TestEffectivePermissions
# ---------------------------------------------------------------------------


class TestEffectivePermissions:
    def test_owner_gets_all(self, acl_mgr: DocRoleAcl) -> None:
        perms = acl_mgr.effective_permissions("alice", "doc1")
        assert perms == {
            Permission.READ,
            Permission.WRITE,
            Permission.DELETE,
            Permission.SHARE,
            Permission.ADMIN,
        }

    def test_union_of_sources(self, acl_mgr: DocRoleAcl) -> None:
        acl_mgr.grant_user("doc1", "bob", {Permission.READ})
        acl_mgr.grant_role("doc1", "editor", {Permission.WRITE})
        acl_mgr.assign_role("bob", "editor")
        acl_mgr.grant_public("doc1", {Permission.SHARE})
        perms = acl_mgr.effective_permissions("bob", "doc1")
        assert perms == {Permission.READ, Permission.WRITE, Permission.SHARE}

    def test_unknown_doc_returns_empty(self, acl_mgr: DocRoleAcl) -> None:
        assert acl_mgr.effective_permissions("bob", "ghost") == set()

    def test_admin_expands(self, acl_mgr: DocRoleAcl) -> None:
        acl_mgr.grant_user("doc1", "bob", {Permission.ADMIN})
        perms = acl_mgr.effective_permissions("bob", "doc1")
        assert perms == {
            Permission.READ,
            Permission.WRITE,
            Permission.DELETE,
            Permission.SHARE,
            Permission.ADMIN,
        }


# ---------------------------------------------------------------------------
# TestDocsAccessibleTo
# ---------------------------------------------------------------------------


class TestDocsAccessibleTo:
    def test_owner_listed(self, acl_mgr: DocRoleAcl) -> None:
        docs = acl_mgr.docs_accessible_to("alice", Permission.READ)
        assert "doc1" in docs

    def test_default_perm_is_read(self, acl_mgr: DocRoleAcl) -> None:
        acl_mgr.grant_user("doc1", "bob", {Permission.READ})
        assert acl_mgr.docs_accessible_to("bob") == ["doc1"]

    def test_filters_by_perm(self, acl_mgr: DocRoleAcl) -> None:
        acl_mgr.set_owner("doc2", "carol")
        acl_mgr.grant_user("doc1", "bob", {Permission.READ})
        acl_mgr.grant_user("doc2", "bob", {Permission.WRITE})
        read_docs = sorted(acl_mgr.docs_accessible_to("bob", Permission.READ))
        assert read_docs == ["doc1"]
        write_docs = sorted(acl_mgr.docs_accessible_to("bob", Permission.WRITE))
        assert write_docs == ["doc2"]

    def test_unknown_user_empty(self, acl_mgr: DocRoleAcl) -> None:
        assert acl_mgr.docs_accessible_to("ghost") == []


# ---------------------------------------------------------------------------
# TestClear
# ---------------------------------------------------------------------------


class TestClear:
    def test_clear_wipes_state(self, acl_mgr: DocRoleAcl) -> None:
        acl_mgr.grant_user("doc1", "bob", {Permission.READ})
        acl_mgr.assign_role("bob", "editor")
        acl_mgr.clear()
        assert acl_mgr.acl_for("doc1") is None
        assert acl_mgr.assign_role("bob", "editor") is False  # role gone too

    def test_clear_then_reuse(self, acl_mgr: DocRoleAcl) -> None:
        acl_mgr.clear()
        acl_mgr.define_role("r", {Permission.READ})
        acl_mgr.set_owner("d", "alice")
        assert acl_mgr.has_permission("alice", "d", Permission.READ)


# ---------------------------------------------------------------------------
# TestEdgeCases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_check_unknown_doc(self) -> None:
        mgr = DocRoleAcl()
        result = mgr.check("alice", "ghost", Permission.READ)
        assert not result.allowed
        assert result.via is None

    def test_check_no_grants(self, acl_mgr: DocRoleAcl) -> None:
        result = acl_mgr.check("stranger", "doc1", Permission.READ)
        assert not result.allowed

    def test_unknown_user_has_no_roles(self, acl_mgr: DocRoleAcl) -> None:
        acl_mgr.grant_role("doc1", "editor", {Permission.WRITE})
        assert not acl_mgr.has_permission("ghost", "doc1", Permission.WRITE)

    def test_role_grant_for_unknown_role_name_is_inert(
        self, acl_mgr: DocRoleAcl
    ) -> None:
        # Granting to a role no user holds doesn't crash.
        acl_mgr.grant_role("doc1", "ghost_role", {Permission.WRITE})
        assert not acl_mgr.has_permission("bob", "doc1", Permission.WRITE)

    def test_revoke_user_perms_keeps_other_perms(
        self, acl_mgr: DocRoleAcl
    ) -> None:
        acl_mgr.grant_user(
            "doc1", "bob", {Permission.READ, Permission.WRITE, Permission.SHARE}
        )
        acl_mgr.revoke_user("doc1", "bob", {Permission.WRITE})
        perms = acl_mgr.effective_permissions("bob", "doc1")
        assert perms == {Permission.READ, Permission.SHARE}

    def test_owner_check_with_no_owner_value(self) -> None:
        mgr = DocRoleAcl()
        # grant_user creates an ACL with owner="".
        mgr.grant_user("d", "bob", {Permission.READ})
        # Empty owner is not treated as user_id match.
        result = mgr.check("", "d", Permission.READ)
        assert not result.allowed

    def test_thread_safety_smoke(self) -> None:
        mgr = DocRoleAcl()
        mgr.define_role("ed", {Permission.WRITE})
        mgr.set_owner("d", "alice")

        def worker(uid: str) -> None:
            for _ in range(50):
                mgr.assign_role(uid, "ed")
                mgr.grant_user("d", uid, {Permission.READ})
                mgr.has_permission(uid, "d", Permission.READ)
                mgr.revoke_user("d", uid, {Permission.READ})

        threads = [
            threading.Thread(target=worker, args=(f"u{i}",)) for i in range(8)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        # The doc still exists and alice (owner) still has full access.
        assert mgr.has_permission("alice", "d", Permission.ADMIN)

    def test_acl_for_returns_same_object(self, acl_mgr: DocRoleAcl) -> None:
        a1 = acl_mgr.acl_for("doc1")
        a2 = acl_mgr.acl_for("doc1")
        assert a1 is a2

    def test_acl_for_unknown_returns_none(self, acl_mgr: DocRoleAcl) -> None:
        assert acl_mgr.acl_for("ghost") is None
