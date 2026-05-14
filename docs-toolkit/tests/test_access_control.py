"""Tests for docstoolkit.access_control (E61)."""

from __future__ import annotations

import pytest

from docstoolkit.access_control import (
    AccessDecision,
    AccessDeniedError,
    AccessEnforcer,
    AccessPolicy,
    DenyAllPolicy,
    OwnerPolicy,
    Permission,
    Resource,
    Role,
    RolePolicy,
    Subject,
)


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

def make_reader_role() -> Role:
    return Role(name="reader", permissions={Permission.READ, Permission.SEARCH})


def make_writer_role() -> Role:
    return Role(name="writer", permissions={Permission.READ, Permission.WRITE})


def make_admin_role() -> Role:
    return Role(
        name="admin",
        permissions=set(Permission),  # all permissions
        description="Full access",
    )


def make_subject(subject_id: str = "u1", roles: list[str] | None = None) -> Subject:
    return Subject(subject_id=subject_id, roles=roles or [])


def make_resource(resource_id: str = "doc1", owner_id: str = "") -> Resource:
    return Resource(resource_id=resource_id, resource_type="document", owner_id=owner_id)


# ---------------------------------------------------------------------------
# Permission enum (6 tests)
# ---------------------------------------------------------------------------

class TestPermissionEnum:
    def test_enum_has_read(self):
        assert Permission.READ.value == "read"

    def test_enum_has_write(self):
        assert Permission.WRITE.value == "write"

    def test_enum_has_delete(self):
        assert Permission.DELETE.value == "delete"

    def test_enum_has_admin(self):
        assert Permission.ADMIN.value == "admin"

    def test_enum_has_search(self):
        assert Permission.SEARCH.value == "search"

    def test_enum_has_export(self):
        assert Permission.EXPORT.value == "export"

    def test_enum_total_members(self):
        assert len(Permission) == 6

    def test_permissions_are_unique(self):
        values = [p.value for p in Permission]
        assert len(values) == len(set(values))


# ---------------------------------------------------------------------------
# Role dataclass (18 tests)
# ---------------------------------------------------------------------------

class TestRole:
    def test_role_name(self):
        r = Role(name="viewer")
        assert r.name == "viewer"

    def test_role_default_permissions_empty(self):
        r = Role(name="viewer")
        assert r.permissions == set()

    def test_role_default_description_empty(self):
        r = Role(name="viewer")
        assert r.description == ""

    def test_role_description_stored(self):
        r = Role(name="viewer", description="Can view docs")
        assert r.description == "Can view docs"

    def test_role_permissions_stored(self):
        r = Role(name="reader", permissions={Permission.READ})
        assert Permission.READ in r.permissions

    def test_has_permission_true(self):
        r = make_reader_role()
        assert r.has_permission(Permission.READ) is True

    def test_has_permission_false(self):
        r = make_reader_role()
        assert r.has_permission(Permission.DELETE) is False

    def test_has_permission_search_true(self):
        r = make_reader_role()
        assert r.has_permission(Permission.SEARCH) is True

    def test_grant_adds_permission(self):
        r = Role(name="viewer")
        r.grant(Permission.READ)
        assert r.has_permission(Permission.READ) is True

    def test_grant_multiple(self):
        r = Role(name="viewer")
        r.grant(Permission.READ)
        r.grant(Permission.EXPORT)
        assert r.has_permission(Permission.READ) is True
        assert r.has_permission(Permission.EXPORT) is True

    def test_grant_idempotent(self):
        r = Role(name="viewer", permissions={Permission.READ})
        r.grant(Permission.READ)
        assert r.permissions == {Permission.READ}

    def test_revoke_removes_permission(self):
        r = make_reader_role()
        r.revoke(Permission.READ)
        assert r.has_permission(Permission.READ) is False

    def test_revoke_leaves_others(self):
        r = make_reader_role()
        r.revoke(Permission.READ)
        assert r.has_permission(Permission.SEARCH) is True

    def test_revoke_absent_no_error(self):
        r = Role(name="viewer")
        r.revoke(Permission.DELETE)  # should not raise

    def test_revoke_all(self):
        r = make_admin_role()
        for perm in Permission:
            r.revoke(perm)
        assert r.permissions == set()

    def test_roles_have_independent_permissions(self):
        r1 = Role(name="a")
        r2 = Role(name="b")
        r1.grant(Permission.READ)
        assert not r2.has_permission(Permission.READ)

    def test_role_with_all_permissions(self):
        r = make_admin_role()
        for perm in Permission:
            assert r.has_permission(perm) is True

    def test_role_permissions_is_set_type(self):
        r = Role(name="x")
        assert isinstance(r.permissions, set)


# ---------------------------------------------------------------------------
# Subject dataclass (6 tests)
# ---------------------------------------------------------------------------

class TestSubject:
    def test_subject_id_stored(self):
        s = Subject(subject_id="alice")
        assert s.subject_id == "alice"

    def test_subject_default_roles_empty(self):
        s = Subject(subject_id="alice")
        assert s.roles == []

    def test_subject_default_attributes_empty(self):
        s = Subject(subject_id="alice")
        assert s.attributes == {}

    def test_subject_roles_stored(self):
        s = Subject(subject_id="alice", roles=["admin", "reader"])
        assert "admin" in s.roles

    def test_subject_attributes_stored(self):
        s = Subject(subject_id="alice", attributes={"dept": "eng"})
        assert s.attributes["dept"] == "eng"

    def test_subjects_independent_roles(self):
        s1 = Subject(subject_id="a")
        s2 = Subject(subject_id="b")
        s1.roles.append("admin")
        assert "admin" not in s2.roles


# ---------------------------------------------------------------------------
# Resource dataclass (7 tests)
# ---------------------------------------------------------------------------

class TestResource:
    def test_resource_id_stored(self):
        r = Resource(resource_id="doc1", resource_type="document")
        assert r.resource_id == "doc1"

    def test_resource_type_stored(self):
        r = Resource(resource_id="doc1", resource_type="document")
        assert r.resource_type == "document"

    def test_resource_default_owner_empty(self):
        r = Resource(resource_id="doc1", resource_type="document")
        assert r.owner_id == ""

    def test_resource_owner_stored(self):
        r = Resource(resource_id="doc1", resource_type="document", owner_id="alice")
        assert r.owner_id == "alice"

    def test_resource_default_attributes_empty(self):
        r = Resource(resource_id="doc1", resource_type="document")
        assert r.attributes == {}

    def test_resource_attributes_stored(self):
        r = Resource(resource_id="doc1", resource_type="document", attributes={"sensitive": True})
        assert r.attributes["sensitive"] is True

    def test_resource_type_variety(self):
        r = Resource(resource_id="idx1", resource_type="index")
        assert r.resource_type == "index"


# ---------------------------------------------------------------------------
# AccessDecision enum (3 tests)
# ---------------------------------------------------------------------------

class TestAccessDecision:
    def test_allow_value(self):
        assert AccessDecision.ALLOW.value == "allow"

    def test_deny_value(self):
        assert AccessDecision.DENY.value == "deny"

    def test_not_applicable_value(self):
        assert AccessDecision.NOT_APPLICABLE.value == "not_applicable"


# ---------------------------------------------------------------------------
# OwnerPolicy (6 tests)
# ---------------------------------------------------------------------------

class TestOwnerPolicy:
    def setup_method(self):
        self.policy = OwnerPolicy()

    def test_owner_gets_allow(self):
        s = make_subject("alice")
        r = make_resource(owner_id="alice")
        assert self.policy.evaluate(s, r, Permission.READ) is AccessDecision.ALLOW

    def test_non_owner_gets_not_applicable(self):
        s = make_subject("bob")
        r = make_resource(owner_id="alice")
        assert self.policy.evaluate(s, r, Permission.READ) is AccessDecision.NOT_APPLICABLE

    def test_owner_allow_on_write(self):
        s = make_subject("alice")
        r = make_resource(owner_id="alice")
        assert self.policy.evaluate(s, r, Permission.WRITE) is AccessDecision.ALLOW

    def test_owner_allow_on_delete(self):
        s = make_subject("alice")
        r = make_resource(owner_id="alice")
        assert self.policy.evaluate(s, r, Permission.DELETE) is AccessDecision.ALLOW

    def test_empty_owner_id_not_applicable(self):
        s = make_subject("")
        r = make_resource(owner_id="")  # no owner set
        assert self.policy.evaluate(s, r, Permission.READ) is AccessDecision.NOT_APPLICABLE

    def test_owner_id_case_sensitive(self):
        s = make_subject("Alice")
        r = make_resource(owner_id="alice")
        assert self.policy.evaluate(s, r, Permission.READ) is AccessDecision.NOT_APPLICABLE


# ---------------------------------------------------------------------------
# RolePolicy (10 tests)
# ---------------------------------------------------------------------------

class TestRolePolicy:
    def setup_method(self):
        reader = make_reader_role()
        writer = make_writer_role()
        self.policy = RolePolicy(roles={"reader": reader, "writer": writer})

    def test_role_with_permission_allows(self):
        s = make_subject(roles=["reader"])
        r = make_resource()
        assert self.policy.evaluate(s, r, Permission.READ) is AccessDecision.ALLOW

    def test_role_without_permission_not_applicable(self):
        s = make_subject(roles=["reader"])
        r = make_resource()
        assert self.policy.evaluate(s, r, Permission.DELETE) is AccessDecision.NOT_APPLICABLE

    def test_no_roles_not_applicable(self):
        s = make_subject(roles=[])
        r = make_resource()
        assert self.policy.evaluate(s, r, Permission.READ) is AccessDecision.NOT_APPLICABLE

    def test_unknown_role_not_applicable(self):
        s = make_subject(roles=["superadmin"])
        r = make_resource()
        assert self.policy.evaluate(s, r, Permission.READ) is AccessDecision.NOT_APPLICABLE

    def test_writer_role_allows_write(self):
        s = make_subject(roles=["writer"])
        r = make_resource()
        assert self.policy.evaluate(s, r, Permission.WRITE) is AccessDecision.ALLOW

    def test_writer_role_not_applicable_for_delete(self):
        s = make_subject(roles=["writer"])
        r = make_resource()
        assert self.policy.evaluate(s, r, Permission.DELETE) is AccessDecision.NOT_APPLICABLE

    def test_multiple_roles_one_matches(self):
        s = make_subject(roles=["reader", "writer"])
        r = make_resource()
        assert self.policy.evaluate(s, r, Permission.WRITE) is AccessDecision.ALLOW

    def test_roles_property_returns_registry(self):
        assert "reader" in self.policy.roles
        assert "writer" in self.policy.roles

    def test_never_returns_deny(self):
        s = make_subject(roles=["reader"])
        r = make_resource()
        result = self.policy.evaluate(s, r, Permission.ADMIN)
        assert result is not AccessDecision.DENY

    def test_empty_role_registry(self):
        policy = RolePolicy(roles={})
        s = make_subject(roles=["reader"])
        r = make_resource()
        assert policy.evaluate(s, r, Permission.READ) is AccessDecision.NOT_APPLICABLE


# ---------------------------------------------------------------------------
# DenyAllPolicy (4 tests)
# ---------------------------------------------------------------------------

class TestDenyAllPolicy:
    def setup_method(self):
        self.policy = DenyAllPolicy()

    def test_denies_read(self):
        s = make_subject()
        r = make_resource()
        assert self.policy.evaluate(s, r, Permission.READ) is AccessDecision.DENY

    def test_denies_write(self):
        s = make_subject()
        r = make_resource()
        assert self.policy.evaluate(s, r, Permission.WRITE) is AccessDecision.DENY

    def test_denies_admin(self):
        s = make_subject()
        r = make_resource()
        assert self.policy.evaluate(s, r, Permission.ADMIN) is AccessDecision.DENY

    def test_denies_regardless_of_subject(self):
        s = make_subject("superuser", roles=["admin"])
        r = make_resource(owner_id="superuser")
        assert self.policy.evaluate(s, r, Permission.DELETE) is AccessDecision.DENY


# ---------------------------------------------------------------------------
# AccessEnforcer (22 tests)
# ---------------------------------------------------------------------------

class TestAccessEnforcer:
    # --- basic setup -------------------------------------------------------

    def test_empty_policies_check_returns_false(self):
        e = AccessEnforcer()
        s = make_subject()
        r = make_resource()
        assert e.check(s, r, Permission.READ) is False

    def test_empty_policies_require_raises(self):
        e = AccessEnforcer()
        s = make_subject()
        r = make_resource()
        with pytest.raises(AccessDeniedError):
            e.require(s, r, Permission.READ)

    def test_add_policy_appends(self):
        e = AccessEnforcer()
        p = DenyAllPolicy()
        e.add_policy(p)
        assert e.check(make_subject(), make_resource(), Permission.READ) is False

    def test_constructor_accepts_policy_list(self):
        reader = make_reader_role()
        policy = RolePolicy({"reader": reader})
        e = AccessEnforcer(policies=[policy])
        s = make_subject(roles=["reader"])
        r = make_resource()
        assert e.check(s, r, Permission.READ) is True

    # --- first-ALLOW-wins --------------------------------------------------

    def test_first_allow_wins_over_later_deny(self):
        owner_policy = OwnerPolicy()
        deny_policy = DenyAllPolicy()
        e = AccessEnforcer(policies=[owner_policy, deny_policy])
        s = make_subject("alice")
        r = make_resource(owner_id="alice")
        assert e.check(s, r, Permission.READ) is True

    def test_first_deny_wins_over_later_allow(self):
        deny_policy = DenyAllPolicy()
        reader = make_reader_role()
        role_policy = RolePolicy({"reader": reader})
        e = AccessEnforcer(policies=[deny_policy, role_policy])
        s = make_subject(roles=["reader"])
        r = make_resource()
        assert e.check(s, r, Permission.READ) is False

    # --- all NOT_APPLICABLE → DENY ----------------------------------------

    def test_all_not_applicable_yields_deny(self):
        owner_policy = OwnerPolicy()  # subject is not owner → NOT_APPLICABLE
        reader = make_reader_role()
        role_policy = RolePolicy({"reader": reader})  # no matching role → NOT_APPLICABLE
        e = AccessEnforcer(policies=[owner_policy, role_policy])
        s = make_subject("bob", roles=["superuser"])  # unknown role
        r = make_resource(owner_id="alice")
        assert e.check(s, r, Permission.READ) is False

    # --- check return type -------------------------------------------------

    def test_check_returns_bool_true(self):
        e = AccessEnforcer(policies=[OwnerPolicy()])
        s = make_subject("alice")
        r = make_resource(owner_id="alice")
        result = e.check(s, r, Permission.READ)
        assert isinstance(result, bool)
        assert result is True

    def test_check_returns_bool_false(self):
        e = AccessEnforcer(policies=[DenyAllPolicy()])
        result = e.check(make_subject(), make_resource(), Permission.READ)
        assert isinstance(result, bool)
        assert result is False

    # --- require -----------------------------------------------------------

    def test_require_passes_when_allowed(self):
        e = AccessEnforcer(policies=[OwnerPolicy()])
        s = make_subject("alice")
        r = make_resource(owner_id="alice")
        e.require(s, r, Permission.READ)  # should not raise

    def test_require_raises_access_denied_error(self):
        e = AccessEnforcer(policies=[DenyAllPolicy()])
        s = make_subject("bob")
        r = make_resource()
        with pytest.raises(AccessDeniedError):
            e.require(s, r, Permission.WRITE)

    def test_access_denied_error_message_contains_subject(self):
        e = AccessEnforcer(policies=[DenyAllPolicy()])
        s = make_subject("charlie")
        r = make_resource("secret_doc")
        with pytest.raises(AccessDeniedError) as exc_info:
            e.require(s, r, Permission.DELETE)
        assert "charlie" in str(exc_info.value)

    def test_access_denied_error_message_contains_resource(self):
        e = AccessEnforcer(policies=[DenyAllPolicy()])
        s = make_subject("charlie")
        r = make_resource("secret_doc")
        with pytest.raises(AccessDeniedError) as exc_info:
            e.require(s, r, Permission.DELETE)
        assert "secret_doc" in str(exc_info.value)

    def test_access_denied_error_attributes(self):
        e = AccessEnforcer(policies=[DenyAllPolicy()])
        s = make_subject("charlie")
        r = make_resource("res42")
        with pytest.raises(AccessDeniedError) as exc_info:
            e.require(s, r, Permission.READ)
        err = exc_info.value
        assert err.subject_id == "charlie"
        assert err.resource_id == "res42"
        assert err.permission is Permission.READ

    # --- roles property ----------------------------------------------------

    def test_roles_property_empty_when_no_role_policy(self):
        e = AccessEnforcer(policies=[DenyAllPolicy()])
        assert e.roles == {}

    def test_roles_property_combines_role_policies(self):
        r1 = RolePolicy({"reader": make_reader_role()})
        r2 = RolePolicy({"writer": make_writer_role()})
        e = AccessEnforcer(policies=[r1, r2])
        assert "reader" in e.roles
        assert "writer" in e.roles

    def test_roles_property_returns_dict(self):
        e = AccessEnforcer()
        assert isinstance(e.roles, dict)

    # --- combined scenarios ------------------------------------------------

    def test_owner_policy_before_role_policy(self):
        owner_policy = OwnerPolicy()
        reader = make_reader_role()
        role_policy = RolePolicy({"reader": reader})
        e = AccessEnforcer(policies=[owner_policy, role_policy])
        # owner match wins before role check even matters
        s = make_subject("alice", roles=["reader"])
        r = make_resource(owner_id="alice")
        assert e.check(s, r, Permission.DELETE) is True  # owner → ALLOW

    def test_deny_all_as_final_sentinel(self):
        owner_policy = OwnerPolicy()
        reader = make_reader_role()
        role_policy = RolePolicy({"reader": reader})
        deny_policy = DenyAllPolicy()
        e = AccessEnforcer(policies=[owner_policy, role_policy, deny_policy])
        # bob is not owner, not reader → falls through to DenyAllPolicy
        s = make_subject("bob", roles=[])
        r = make_resource(owner_id="alice")
        assert e.check(s, r, Permission.READ) is False

    def test_role_policy_before_deny_all(self):
        reader = make_reader_role()
        role_policy = RolePolicy({"reader": reader})
        deny_policy = DenyAllPolicy()
        e = AccessEnforcer(policies=[role_policy, deny_policy])
        s = make_subject(roles=["reader"])
        r = make_resource()
        assert e.check(s, r, Permission.READ) is True

    def test_subject_with_multiple_roles(self):
        reader = make_reader_role()
        writer = make_writer_role()
        role_policy = RolePolicy({"reader": reader, "writer": writer})
        e = AccessEnforcer(policies=[role_policy])
        s = make_subject(roles=["reader", "writer"])
        r = make_resource()
        # both READ (via reader or writer) and WRITE (via writer) should pass
        assert e.check(s, r, Permission.READ) is True
        assert e.check(s, r, Permission.WRITE) is True

    def test_subject_with_multiple_roles_still_denied_for_missing(self):
        reader = make_reader_role()
        writer = make_writer_role()
        role_policy = RolePolicy({"reader": reader, "writer": writer})
        e = AccessEnforcer(policies=[role_policy])
        s = make_subject(roles=["reader", "writer"])
        r = make_resource()
        # neither reader nor writer has DELETE
        assert e.check(s, r, Permission.DELETE) is False

    def test_admin_role_with_all_permissions(self):
        admin = make_admin_role()
        role_policy = RolePolicy({"admin": admin})
        e = AccessEnforcer(policies=[role_policy])
        s = make_subject(roles=["admin"])
        r = make_resource()
        for perm in Permission:
            assert e.check(s, r, perm) is True


# ---------------------------------------------------------------------------
# AccessDeniedError (4 tests)
# ---------------------------------------------------------------------------

class TestAccessDeniedError:
    def test_is_exception(self):
        err = AccessDeniedError("u1", "r1", Permission.READ)
        assert isinstance(err, Exception)

    def test_subject_id_stored(self):
        err = AccessDeniedError("u1", "r1", Permission.WRITE)
        assert err.subject_id == "u1"

    def test_resource_id_stored(self):
        err = AccessDeniedError("u1", "r1", Permission.WRITE)
        assert err.resource_id == "r1"

    def test_permission_stored(self):
        err = AccessDeniedError("u1", "r1", Permission.EXPORT)
        assert err.permission is Permission.EXPORT


# ---------------------------------------------------------------------------
# Edge-case / integration tests (additional coverage)
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_policy_order_matters_allow_before_deny(self):
        allow_p = OwnerPolicy()
        deny_p = DenyAllPolicy()
        e_allow_first = AccessEnforcer(policies=[allow_p, deny_p])
        e_deny_first = AccessEnforcer(policies=[deny_p, allow_p])
        s = make_subject("alice")
        r = make_resource(owner_id="alice")
        assert e_allow_first.check(s, r, Permission.READ) is True
        assert e_deny_first.check(s, r, Permission.READ) is False

    def test_add_policy_after_construction(self):
        e = AccessEnforcer()
        assert e.check(make_subject(), make_resource(), Permission.READ) is False
        e.add_policy(OwnerPolicy())
        s = make_subject("alice")
        r = make_resource(owner_id="alice")
        assert e.check(s, r, Permission.READ) is True

    def test_subject_no_roles_all_permissions_denied_with_role_policy(self):
        reader = make_reader_role()
        e = AccessEnforcer(policies=[RolePolicy({"reader": reader})])
        s = make_subject(roles=[])
        r = make_resource()
        for perm in Permission:
            assert e.check(s, r, perm) is False

    def test_role_policy_with_single_permission(self):
        exporter = Role(name="exporter", permissions={Permission.EXPORT})
        e = AccessEnforcer(policies=[RolePolicy({"exporter": exporter})])
        s = make_subject(roles=["exporter"])
        r = make_resource()
        assert e.check(s, r, Permission.EXPORT) is True
        assert e.check(s, r, Permission.READ) is False

    def test_owner_policy_not_applicable_for_no_owner_resource(self):
        e = AccessEnforcer(policies=[OwnerPolicy()])
        s = make_subject("alice")
        r = make_resource(owner_id="")  # no owner
        # OwnerPolicy → NOT_APPLICABLE → fall-through → DENY
        assert e.check(s, r, Permission.READ) is False

    def test_resource_attributes_do_not_affect_policies(self):
        owner = OwnerPolicy()
        e = AccessEnforcer(policies=[owner])
        s = make_subject("alice")
        r = Resource(
            resource_id="doc1",
            resource_type="document",
            owner_id="alice",
            attributes={"confidential": True, "level": 5},
        )
        assert e.check(s, r, Permission.READ) is True

    def test_subject_attributes_do_not_affect_built_in_policies(self):
        reader = make_reader_role()
        e = AccessEnforcer(policies=[RolePolicy({"reader": reader})])
        s = Subject(subject_id="alice", roles=["reader"], attributes={"clearance": "top-secret"})
        r = make_resource()
        assert e.check(s, r, Permission.READ) is True

    def test_multiple_role_policies_combined_roles_property(self):
        p1 = RolePolicy({"reader": make_reader_role()})
        p2 = RolePolicy({"admin": make_admin_role()})
        e = AccessEnforcer(policies=[p1, p2])
        combined = e.roles
        assert "reader" in combined
        assert "admin" in combined

    def test_require_does_not_raise_on_allowed(self):
        admin = make_admin_role()
        e = AccessEnforcer(policies=[RolePolicy({"admin": admin})])
        s = make_subject(roles=["admin"])
        r = make_resource()
        for perm in Permission:
            e.require(s, r, perm)  # should not raise for any permission

    def test_access_denied_error_is_subclass_of_exception(self):
        assert issubclass(AccessDeniedError, Exception)
