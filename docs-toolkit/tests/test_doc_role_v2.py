"""Tests for E236 doc_role_v2."""
from __future__ import annotations

import pytest

from docstoolkit.doc_role_v2 import (
    AccessDecision,
    AccessRequest,
    DocRoleV2,
    Permission,
    Policy,
    RoleDefinition,
    UserBinding,
)


# ---------------------------------------------------------------- Permission
class TestPermission:
    def test_has_read(self):
        assert Permission.READ.value == "read"

    def test_has_write(self):
        assert Permission.WRITE.value == "write"

    def test_has_delete(self):
        assert Permission.DELETE.value == "delete"

    def test_has_admin(self):
        assert Permission.ADMIN.value == "admin"

    def test_has_share(self):
        assert Permission.SHARE.value == "share"

    def test_has_comment(self):
        assert Permission.COMMENT.value == "comment"

    def test_has_publish(self):
        assert Permission.PUBLISH.value == "publish"

    def test_distinct_values(self):
        assert len({p.value for p in Permission}) == 7


# ------------------------------------------------------------ RoleDefinition
class TestRoleDefinition:
    def test_create_minimal(self):
        role = RoleDefinition(name="r", permissions={Permission.READ})
        assert role.name == "r"
        assert role.permissions == {Permission.READ}
        assert role.parent_roles == []
        assert role.description == ""

    def test_create_with_parents(self):
        role = RoleDefinition(
            name="editor", permissions={Permission.WRITE}, parent_roles=["viewer"]
        )
        assert role.parent_roles == ["viewer"]

    def test_with_description(self):
        role = RoleDefinition(name="r", permissions=set(), description="hello")
        assert role.description == "hello"


# --------------------------------------------------------------- UserBinding
class TestUserBinding:
    def test_default(self):
        u = UserBinding(user_id="u1")
        assert u.user_id == "u1"
        assert u.roles == set()
        assert u.attributes == {}

    def test_with_data(self):
        u = UserBinding(user_id="u1", roles={"r1"}, attributes={"dept": "eng"})
        assert "r1" in u.roles
        assert u.attributes["dept"] == "eng"


# ---------------------------------------------------------------------- Policy
class TestPolicy:
    def test_create(self):
        cond = lambda ctx: True
        p = Policy(policy_id="x", name="n", permission=Permission.READ, condition=cond)
        assert p.policy_id == "x"
        assert p.priority == 0

    def test_priority(self):
        p = Policy(
            policy_id="x",
            name="n",
            permission=Permission.READ,
            condition=lambda c: True,
            priority=5,
        )
        assert p.priority == 5


# ---------------------------------------------------------------- AccessRequest
class TestAccessRequest:
    def test_create(self):
        r = AccessRequest(user_id="u", resource_id="doc1", permission=Permission.READ)
        assert r.resource_attributes == {}

    def test_with_attrs(self):
        r = AccessRequest(
            user_id="u",
            resource_id="doc1",
            permission=Permission.READ,
            resource_attributes={"owner": "u"},
        )
        assert r.resource_attributes == {"owner": "u"}


# ---------------------------------------------------------------- AccessDecision
class TestAccessDecision:
    def test_grant(self):
        d = AccessDecision(granted=True, reason="role:admin", matched_role="admin")
        assert d.granted
        assert d.matched_role == "admin"
        assert d.matched_policy is None

    def test_deny(self):
        d = AccessDecision(granted=False, reason="no")
        assert not d.granted


# -------------------------------------------------------------- DefineRole
class TestDefineRole:
    def test_basic(self):
        m = DocRoleV2()
        role = m.define_role("viewer", {Permission.READ})
        assert role.name == "viewer"
        assert m.total_roles == 1

    def test_with_parent(self):
        m = DocRoleV2()
        m.define_role("viewer", {Permission.READ})
        role = m.define_role("editor", {Permission.WRITE}, parent_roles=["viewer"])
        assert role.parent_roles == ["viewer"]

    def test_invalid_name(self):
        m = DocRoleV2()
        with pytest.raises(ValueError):
            m.define_role("", {Permission.READ})

    def test_self_parent_rejected(self):
        m = DocRoleV2()
        with pytest.raises(ValueError):
            m.define_role("r", {Permission.READ}, parent_roles=["r"])


# --------------------------------------------------------------- RemoveRole
class TestRemoveRole:
    def test_existing(self):
        m = DocRoleV2()
        m.define_role("r", {Permission.READ})
        assert m.remove_role("r")
        assert m.total_roles == 0

    def test_missing(self):
        m = DocRoleV2()
        assert m.remove_role("missing") is False

    def test_detaches_from_children(self):
        m = DocRoleV2()
        m.define_role("p", {Permission.READ})
        m.define_role("c", {Permission.WRITE}, parent_roles=["p"])
        m.remove_role("p")
        assert m._roles["c"].parent_roles == []

    def test_revokes_from_users(self):
        m = DocRoleV2()
        m.define_role("r", {Permission.READ})
        m.bind_user("u1", roles={"r"})
        m.remove_role("r")
        assert m.user_roles("u1") == set()


# ----------------------------------------------------- UpdateRolePermissions
class TestUpdateRolePermissions:
    def test_update(self):
        m = DocRoleV2()
        m.define_role("r", {Permission.READ})
        assert m.update_role_permissions("r", {Permission.WRITE, Permission.READ})
        assert m.effective_permissions("r") == {Permission.WRITE, Permission.READ}

    def test_missing(self):
        m = DocRoleV2()
        assert not m.update_role_permissions("nope", set())


# ------------------------------------------------------------- AddParentRole
class TestAddParentRole:
    def test_add(self):
        m = DocRoleV2()
        m.define_role("p", {Permission.READ})
        m.define_role("c", {Permission.WRITE})
        assert m.add_parent_role("c", "p")
        assert "p" in m._roles["c"].parent_roles

    def test_idempotent(self):
        m = DocRoleV2()
        m.define_role("p", {Permission.READ})
        m.define_role("c", {Permission.WRITE}, parent_roles=["p"])
        assert m.add_parent_role("c", "p")
        assert m._roles["c"].parent_roles.count("p") == 1

    def test_missing_role(self):
        m = DocRoleV2()
        m.define_role("p", {Permission.READ})
        assert not m.add_parent_role("missing", "p")

    def test_self_parent(self):
        m = DocRoleV2()
        m.define_role("r", {Permission.READ})
        assert not m.add_parent_role("r", "r")


# ------------------------------------------------------------- AddParentCycle
class TestAddParentCycle:
    def test_direct_cycle(self):
        m = DocRoleV2()
        m.define_role("a", {Permission.READ})
        m.define_role("b", {Permission.WRITE}, parent_roles=["a"])
        # a -> b (b is parent of a) would cycle since b already inherits from a
        assert not m.add_parent_role("a", "b")

    def test_indirect_cycle(self):
        m = DocRoleV2()
        m.define_role("a", set())
        m.define_role("b", set(), parent_roles=["a"])
        m.define_role("c", set(), parent_roles=["b"])
        # adding c as parent of a -> a→c→b→a cycle
        assert not m.add_parent_role("a", "c")

    def test_define_with_cyclic_parent(self):
        m = DocRoleV2()
        m.define_role("a", set())
        m.define_role("b", set(), parent_roles=["a"])
        with pytest.raises(ValueError):
            m.define_role("a", set(), parent_roles=["b"])  # would re-create cycle


# -------------------------------------------------------- EffectivePermissions
class TestEffectivePermissions:
    def test_direct(self):
        m = DocRoleV2()
        m.define_role("r", {Permission.READ, Permission.WRITE})
        assert m.effective_permissions("r") == {Permission.READ, Permission.WRITE}

    def test_inherited(self):
        m = DocRoleV2()
        m.define_role("base", {Permission.READ})
        m.define_role("ext", {Permission.WRITE}, parent_roles=["base"])
        assert m.effective_permissions("ext") == {Permission.READ, Permission.WRITE}

    def test_deep_chain(self):
        m = DocRoleV2()
        m.define_role("a", {Permission.READ})
        m.define_role("b", {Permission.WRITE}, parent_roles=["a"])
        m.define_role("c", {Permission.DELETE}, parent_roles=["b"])
        assert m.effective_permissions("c") == {
            Permission.READ,
            Permission.WRITE,
            Permission.DELETE,
        }

    def test_multiple_parents(self):
        m = DocRoleV2()
        m.define_role("a", {Permission.READ})
        m.define_role("b", {Permission.WRITE})
        m.define_role("c", {Permission.DELETE}, parent_roles=["a", "b"])
        assert m.effective_permissions("c") == {
            Permission.READ,
            Permission.WRITE,
            Permission.DELETE,
        }

    def test_missing(self):
        m = DocRoleV2()
        assert m.effective_permissions("nope") == set()


# ------------------------------------------------------------------ BindUser
class TestBindUser:
    def test_basic(self):
        m = DocRoleV2()
        b = m.bind_user("u1")
        assert b.user_id == "u1"
        assert m.total_users == 1

    def test_with_roles_attrs(self):
        m = DocRoleV2()
        m.define_role("r", {Permission.READ})
        b = m.bind_user("u1", roles={"r"}, attributes={"k": 1})
        assert b.roles == {"r"}
        assert b.attributes == {"k": 1}

    def test_invalid(self):
        m = DocRoleV2()
        with pytest.raises(ValueError):
            m.bind_user("")


# ------------------------------------------------------------------ AssignRole
class TestAssignRole:
    def test_assign(self):
        m = DocRoleV2()
        m.define_role("r", {Permission.READ})
        m.bind_user("u")
        assert m.assign_role("u", "r")
        assert "r" in m.user_roles("u")

    def test_no_user(self):
        m = DocRoleV2()
        m.define_role("r", {Permission.READ})
        assert not m.assign_role("missing", "r")

    def test_no_role(self):
        m = DocRoleV2()
        m.bind_user("u")
        assert not m.assign_role("u", "nope")


# ----------------------------------------------------------------- RevokeRole
class TestRevokeRole:
    def test_revoke(self):
        m = DocRoleV2()
        m.define_role("r", {Permission.READ})
        m.bind_user("u", roles={"r"})
        assert m.revoke_role("u", "r")
        assert "r" not in m.user_roles("u")

    def test_no_user(self):
        m = DocRoleV2()
        assert not m.revoke_role("missing", "r")

    def test_no_role_on_user(self):
        m = DocRoleV2()
        m.bind_user("u")
        assert not m.revoke_role("u", "r")


# --------------------------------------------------------------- SetAttribute
class TestSetAttribute:
    def test_set(self):
        m = DocRoleV2()
        m.bind_user("u")
        assert m.set_attribute("u", "dept", "eng")
        assert m._users["u"].attributes["dept"] == "eng"

    def test_overwrite(self):
        m = DocRoleV2()
        m.bind_user("u", attributes={"k": 1})
        m.set_attribute("u", "k", 2)
        assert m._users["u"].attributes["k"] == 2

    def test_missing_user(self):
        m = DocRoleV2()
        assert not m.set_attribute("nope", "k", 1)


# ------------------------------------------------------------------ UserRoles
class TestUserRoles:
    def test_returns_roles(self):
        m = DocRoleV2()
        m.define_role("r", set())
        m.bind_user("u", roles={"r"})
        assert m.user_roles("u") == {"r"}

    def test_missing_user(self):
        m = DocRoleV2()
        assert m.user_roles("nope") == set()

    def test_copy_not_reference(self):
        m = DocRoleV2()
        m.define_role("r", set())
        m.bind_user("u", roles={"r"})
        result = m.user_roles("u")
        result.add("other")
        assert m.user_roles("u") == {"r"}


# ------------------------------------------------------------ UserPermissions
class TestUserPermissions:
    def test_direct(self):
        m = DocRoleV2()
        m.define_role("r", {Permission.READ})
        m.bind_user("u", roles={"r"})
        assert m.user_permissions("u") == {Permission.READ}

    def test_inherited(self):
        m = DocRoleV2()
        m.define_role("base", {Permission.READ})
        m.define_role("editor", {Permission.WRITE}, parent_roles=["base"])
        m.bind_user("u", roles={"editor"})
        assert m.user_permissions("u") == {Permission.READ, Permission.WRITE}

    def test_multiple_roles(self):
        m = DocRoleV2()
        m.define_role("a", {Permission.READ})
        m.define_role("b", {Permission.WRITE})
        m.bind_user("u", roles={"a", "b"})
        assert m.user_permissions("u") == {Permission.READ, Permission.WRITE}

    def test_missing_user(self):
        m = DocRoleV2()
        assert m.user_permissions("u") == set()


# -------------------------------------------------------------------- AddPolicy
class TestAddPolicy:
    def test_add(self):
        m = DocRoleV2()
        p = m.add_policy("n", Permission.READ, lambda c: True)
        assert p.name == "n"
        assert m.total_policies == 1

    def test_invalid_condition(self):
        m = DocRoleV2()
        with pytest.raises(ValueError):
            m.add_policy("n", Permission.READ, "not-callable")

    def test_invalid_permission(self):
        m = DocRoleV2()
        with pytest.raises(ValueError):
            m.add_policy("n", "read", lambda c: True)

    def test_priority(self):
        m = DocRoleV2()
        p = m.add_policy("n", Permission.READ, lambda c: True, priority=10)
        assert p.priority == 10


# ----------------------------------------------------------------- RemovePolicy
class TestRemovePolicy:
    def test_remove(self):
        m = DocRoleV2()
        p = m.add_policy("n", Permission.READ, lambda c: True)
        assert m.remove_policy(p.policy_id)
        assert m.total_policies == 0

    def test_missing(self):
        m = DocRoleV2()
        assert not m.remove_policy("x")


# ------------------------------------------------------------- CheckAccessRole
class TestCheckAccessRole:
    def test_granted_by_role(self):
        m = DocRoleV2()
        m.define_role("r", {Permission.READ})
        m.bind_user("u", roles={"r"})
        d = m.check_access(AccessRequest("u", "doc1", Permission.READ))
        assert d.granted
        assert d.matched_role == "r"

    def test_granted_via_inheritance(self):
        m = DocRoleV2()
        m.define_role("base", {Permission.READ})
        m.define_role("editor", {Permission.WRITE}, parent_roles=["base"])
        m.bind_user("u", roles={"editor"})
        d = m.check_access(AccessRequest("u", "doc1", Permission.READ))
        assert d.granted
        assert d.matched_role == "editor"


# ------------------------------------------------------------ CheckAccessPolicy
class TestCheckAccessPolicy:
    def test_granted_by_policy(self):
        m = DocRoleV2()
        m.bind_user("u", attributes={"dept": "eng"})
        m.add_policy(
            "eng-readers",
            Permission.READ,
            lambda ctx: ctx.get("dept") == "eng",
            priority=10,
        )
        d = m.check_access(AccessRequest("u", "doc1", Permission.READ))
        assert d.granted
        assert d.matched_policy is not None
        assert "policy:" in d.reason

    def test_priority_order(self):
        m = DocRoleV2()
        m.bind_user("u")
        m.add_policy("low", Permission.READ, lambda c: True, priority=1)
        high = m.add_policy("high", Permission.READ, lambda c: True, priority=10)
        d = m.check_access(AccessRequest("u", "doc1", Permission.READ))
        assert d.matched_policy == high.policy_id

    def test_policy_uses_resource_attrs(self):
        m = DocRoleV2()
        m.bind_user("u", attributes={"user_id_attr": "u"})
        m.add_policy(
            "owner",
            Permission.WRITE,
            lambda ctx: ctx.get("owner") == ctx.get("user_id"),
        )
        d = m.check_access(
            AccessRequest("u", "doc1", Permission.WRITE, resource_attributes={"owner": "u"})
        )
        assert d.granted

    def test_policy_permission_mismatch(self):
        m = DocRoleV2()
        m.bind_user("u")
        m.add_policy("p", Permission.WRITE, lambda c: True)
        d = m.check_access(AccessRequest("u", "doc1", Permission.READ))
        assert not d.granted

    def test_policy_exception_treated_as_deny(self):
        m = DocRoleV2()
        m.bind_user("u")
        def boom(_):
            raise RuntimeError("nope")
        m.add_policy("p", Permission.READ, boom)
        d = m.check_access(AccessRequest("u", "doc1", Permission.READ))
        assert not d.granted


# ------------------------------------------------------------ CheckAccessDenied
class TestCheckAccessDenied:
    def test_unbound_user(self):
        m = DocRoleV2()
        d = m.check_access(AccessRequest("ghost", "doc1", Permission.READ))
        assert not d.granted
        assert d.reason == "user-not-bound"

    def test_user_lacks_permission(self):
        m = DocRoleV2()
        m.define_role("r", {Permission.READ})
        m.bind_user("u", roles={"r"})
        d = m.check_access(AccessRequest("u", "doc1", Permission.DELETE))
        assert not d.granted


# ---------------------------------------------------------------------- HasRole
class TestHasRole:
    def test_direct(self):
        m = DocRoleV2()
        m.define_role("r", set())
        m.bind_user("u", roles={"r"})
        assert m.has_role("u", "r")

    def test_inherited(self):
        m = DocRoleV2()
        m.define_role("base", set())
        m.define_role("ext", set(), parent_roles=["base"])
        m.bind_user("u", roles={"ext"})
        assert m.has_role("u", "base")

    def test_missing(self):
        m = DocRoleV2()
        m.define_role("r", set())
        m.bind_user("u", roles={"r"})
        assert not m.has_role("u", "other")

    def test_missing_user(self):
        m = DocRoleV2()
        assert not m.has_role("ghost", "r")


# ---------------------------------------------------------------- UsersWithRole
class TestUsersWithRole:
    def test_direct(self):
        m = DocRoleV2()
        m.define_role("r", set())
        m.bind_user("u1", roles={"r"})
        m.bind_user("u2", roles={"r"})
        m.bind_user("u3")
        result = m.users_with_role("r")
        assert set(result) == {"u1", "u2"}

    def test_inherited(self):
        m = DocRoleV2()
        m.define_role("base", set())
        m.define_role("ext", set(), parent_roles=["base"])
        m.bind_user("u", roles={"ext"})
        assert "u" in m.users_with_role("base")

    def test_no_users(self):
        m = DocRoleV2()
        m.define_role("r", set())
        assert m.users_with_role("r") == []


# ----------------------------------------------------------------- ChildRoles
class TestChildRoles:
    def test_one_child(self):
        m = DocRoleV2()
        m.define_role("p", set())
        m.define_role("c", set(), parent_roles=["p"])
        assert m.child_roles("p") == ["c"]

    def test_none(self):
        m = DocRoleV2()
        m.define_role("p", set())
        assert m.child_roles("p") == []

    def test_multiple(self):
        m = DocRoleV2()
        m.define_role("p", set())
        m.define_role("c1", set(), parent_roles=["p"])
        m.define_role("c2", set(), parent_roles=["p"])
        assert set(m.child_roles("p")) == {"c1", "c2"}


# ------------------------------------------------------------------ Ancestors
class TestAncestors:
    def test_chain(self):
        m = DocRoleV2()
        m.define_role("a", set())
        m.define_role("b", set(), parent_roles=["a"])
        m.define_role("c", set(), parent_roles=["b"])
        assert set(m.ancestors("c")) == {"a", "b"}

    def test_none(self):
        m = DocRoleV2()
        m.define_role("r", set())
        assert m.ancestors("r") == []

    def test_missing(self):
        m = DocRoleV2()
        assert m.ancestors("nope") == []


# ------------------------------------------------------------ TotalProperties
class TestTotalProperties:
    def test_counts(self):
        m = DocRoleV2()
        m.define_role("r", set())
        m.bind_user("u")
        m.add_policy("p", Permission.READ, lambda c: True)
        assert m.total_roles == 1
        assert m.total_users == 1
        assert m.total_policies == 1

    def test_zero(self):
        m = DocRoleV2()
        assert m.total_roles == 0
        assert m.total_users == 0
        assert m.total_policies == 0


# --------------------------------------------------------------------- Clear
class TestClear:
    def test_clear(self):
        m = DocRoleV2()
        m.define_role("r", set())
        m.bind_user("u")
        m.add_policy("p", Permission.READ, lambda c: True)
        m.clear()
        assert m.total_roles == 0
        assert m.total_users == 0
        assert m.total_policies == 0

    def test_clear_empty(self):
        m = DocRoleV2()
        m.clear()
        assert m.total_roles == 0


# ----------------------------------------------------------------- EdgeCases
class TestEdgeCases:
    def test_diamond_inheritance(self):
        m = DocRoleV2()
        m.define_role("top", {Permission.READ})
        m.define_role("l", {Permission.WRITE}, parent_roles=["top"])
        m.define_role("r", {Permission.DELETE}, parent_roles=["top"])
        m.define_role("bot", {Permission.SHARE}, parent_roles=["l", "r"])
        assert m.effective_permissions("bot") == {
            Permission.READ,
            Permission.WRITE,
            Permission.DELETE,
            Permission.SHARE,
        }

    def test_policy_overrides_missing_role_perm(self):
        m = DocRoleV2()
        m.define_role("viewer", {Permission.READ})
        m.bind_user("u", roles={"viewer"}, attributes={"is_owner": True})
        m.add_policy(
            "owner-write",
            Permission.WRITE,
            lambda ctx: bool(ctx.get("is_owner")),
        )
        d = m.check_access(AccessRequest("u", "doc1", Permission.WRITE))
        assert d.granted
        assert d.matched_policy is not None

    def test_revoke_then_check(self):
        m = DocRoleV2()
        m.define_role("r", {Permission.READ})
        m.bind_user("u", roles={"r"})
        m.revoke_role("u", "r")
        d = m.check_access(AccessRequest("u", "doc1", Permission.READ))
        assert not d.granted

    def test_remove_role_then_check_user(self):
        m = DocRoleV2()
        m.define_role("r", {Permission.READ})
        m.bind_user("u", roles={"r"})
        m.remove_role("r")
        assert m.user_permissions("u") == set()

    def test_no_cycle_when_unrelated_parent_added(self):
        m = DocRoleV2()
        m.define_role("a", set())
        m.define_role("b", set())
        m.define_role("c", set())
        assert m.add_parent_role("c", "a")
        assert m.add_parent_role("c", "b")
        assert set(m._roles["c"].parent_roles) == {"a", "b"}

    def test_check_access_resource_attribute_overrides_user_attribute(self):
        m = DocRoleV2()
        m.bind_user("u", attributes={"role_tag": "user"})
        m.add_policy(
            "tag-allow",
            Permission.READ,
            lambda ctx: ctx.get("role_tag") == "resource",
        )
        # resource attribute overrides user attribute with same key
        d = m.check_access(
            AccessRequest(
                "u",
                "doc1",
                Permission.READ,
                resource_attributes={"role_tag": "resource"},
            )
        )
        assert d.granted
