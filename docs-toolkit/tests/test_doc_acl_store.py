"""Tests for E356 DocAclStore."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_acl_store import AclEntry, AclStats, DocAclStore


# ---------------------------------------------------------------- dataclasses
class TestAclEntryDataclass:
    def test_construct_minimal(self):
        e = AclEntry(doc_id="d1", principal="user:1")
        assert e.doc_id == "d1"
        assert e.principal == "user:1"
        assert e.permissions == []
        assert e.granted_at == 0.0
        assert e.granted_by == ""

    def test_construct_full(self):
        e = AclEntry(
            doc_id="d1",
            principal="user:1",
            permissions=["read", "write"],
            granted_at=123.0,
            granted_by="admin",
        )
        assert e.permissions == ["read", "write"]
        assert e.granted_at == 123.0
        assert e.granted_by == "admin"

    def test_permissions_default_is_independent(self):
        a = AclEntry(doc_id="d", principal="p")
        b = AclEntry(doc_id="d2", principal="p2")
        a.permissions.append("read")
        assert b.permissions == []

    def test_is_dataclass(self):
        import dataclasses

        assert dataclasses.is_dataclass(AclEntry)


class TestAclStatsDataclass:
    def test_construct(self):
        s = AclStats(total_entries=3, unique_docs=2, unique_principals=2)
        assert s.total_entries == 3
        assert s.unique_docs == 2
        assert s.unique_principals == 2

    def test_is_dataclass(self):
        import dataclasses

        assert dataclasses.is_dataclass(AclStats)

    def test_equality(self):
        assert AclStats(1, 1, 1) == AclStats(1, 1, 1)
        assert AclStats(1, 1, 1) != AclStats(1, 1, 2)


# --------------------------------------------------------------- construction
class TestConstruction:
    def test_empty_store(self):
        store = DocAclStore()
        s = store.stats()
        assert s.total_entries == 0
        assert s.unique_docs == 0
        assert s.unique_principals == 0

    def test_independent_instances(self):
        a = DocAclStore()
        b = DocAclStore()
        a.grant("d1", "u1", ["read"])
        assert b.stats().total_entries == 0

    def test_wildcard_constant(self):
        assert DocAclStore.WILDCARD == "*"


# ----------------------------------------------------------------------- grant
class TestGrant:
    def test_grant_new_entry(self):
        store = DocAclStore()
        entry = store.grant("d1", "user:1", ["read"], granted_by="admin", now=42.0)
        assert entry.doc_id == "d1"
        assert entry.principal == "user:1"
        assert entry.permissions == ["read"]
        assert entry.granted_by == "admin"
        assert entry.granted_at == 42.0

    def test_grant_replaces_existing(self):
        store = DocAclStore()
        store.grant("d1", "u1", ["read"], now=1.0)
        new = store.grant("d1", "u1", ["write"], granted_by="root", now=2.0)
        assert new.permissions == ["write"]
        assert new.granted_at == 2.0
        assert new.granted_by == "root"
        assert store.stats().total_entries == 1

    def test_grant_uses_time_if_now_none(self):
        store = DocAclStore()
        entry = store.grant("d1", "u1", ["read"])
        assert entry.granted_at > 0

    def test_grant_updates_indexes(self):
        store = DocAclStore()
        store.grant("d1", "u1", ["read"])
        store.grant("d1", "u2", ["read"])
        store.grant("d2", "u1", ["write"])
        s = store.stats()
        assert s.total_entries == 3
        assert s.unique_docs == 2
        assert s.unique_principals == 2

    def test_grant_dedupes_permissions(self):
        store = DocAclStore()
        entry = store.grant("d1", "u1", ["read", "read", "write", "read"])
        assert entry.permissions == ["read", "write"]


# ---------------------------------------------------------------------- revoke
class TestRevoke:
    def test_revoke_existing_returns_true(self):
        store = DocAclStore()
        store.grant("d1", "u1", ["read"])
        assert store.revoke("d1", "u1") is True
        assert store.get_entry("d1", "u1") is None

    def test_revoke_missing_returns_false(self):
        store = DocAclStore()
        assert store.revoke("d1", "u1") is False

    def test_revoke_cleans_indexes(self):
        store = DocAclStore()
        store.grant("d1", "u1", ["read"])
        store.revoke("d1", "u1")
        assert store.docs_for_principal("u1") == []
        assert store.principals_for("d1") == []

    def test_revoke_keeps_other_entries_for_same_doc(self):
        store = DocAclStore()
        store.grant("d1", "u1", ["read"])
        store.grant("d1", "u2", ["read"])
        store.revoke("d1", "u1")
        assert len(store.principals_for("d1")) == 1
        assert store.principals_for("d1")[0].principal == "u2"

    def test_revoke_twice_second_is_false(self):
        store = DocAclStore()
        store.grant("d1", "u1", ["read"])
        assert store.revoke("d1", "u1") is True
        assert store.revoke("d1", "u1") is False


class TestRevokePrincipal:
    def test_zero_when_missing(self):
        store = DocAclStore()
        assert store.revoke_principal("ghost") == 0

    def test_counts_all_entries(self):
        store = DocAclStore()
        store.grant("d1", "u1", ["read"])
        store.grant("d2", "u1", ["read"])
        store.grant("d3", "u1", ["write"])
        store.grant("d1", "u2", ["read"])
        assert store.revoke_principal("u1") == 3
        assert store.docs_for_principal("u1") == []
        assert store.principals_for("d1") == [store.get_entry("d1", "u2")]

    def test_index_cleared(self):
        store = DocAclStore()
        store.grant("d1", "u1", ["read"])
        store.revoke_principal("u1")
        assert store.stats().unique_principals == 0


class TestRevokeDoc:
    def test_zero_when_missing(self):
        store = DocAclStore()
        assert store.revoke_doc("ghost") == 0

    def test_counts_all_entries(self):
        store = DocAclStore()
        store.grant("d1", "u1", ["read"])
        store.grant("d1", "u2", ["read"])
        store.grant("d1", "u3", ["write"])
        store.grant("d2", "u1", ["read"])
        assert store.revoke_doc("d1") == 3
        assert store.principals_for("d1") == []
        assert store.docs_for_principal("u1") == ["d2"]

    def test_index_cleared(self):
        store = DocAclStore()
        store.grant("d1", "u1", ["read"])
        store.revoke_doc("d1")
        assert store.stats().unique_docs == 0


# -------------------------------------------------------------- add_permission
class TestAddPermission:
    def test_add_new_permission_returns_true(self):
        store = DocAclStore()
        store.grant("d1", "u1", ["read"])
        assert store.add_permission("d1", "u1", "write") is True
        assert "write" in store.get_entry("d1", "u1").permissions

    def test_add_duplicate_returns_false(self):
        store = DocAclStore()
        store.grant("d1", "u1", ["read"])
        assert store.add_permission("d1", "u1", "read") is False

    def test_add_to_missing_entry_returns_false(self):
        store = DocAclStore()
        assert store.add_permission("d1", "u1", "read") is False

    def test_add_preserves_existing(self):
        store = DocAclStore()
        store.grant("d1", "u1", ["read"])
        store.add_permission("d1", "u1", "write")
        entry = store.get_entry("d1", "u1")
        assert entry.permissions == ["read", "write"]


# ----------------------------------------------------------- remove_permission
class TestRemovePermission:
    def test_remove_existing_returns_true(self):
        store = DocAclStore()
        store.grant("d1", "u1", ["read", "write"])
        assert store.remove_permission("d1", "u1", "write") is True
        assert store.get_entry("d1", "u1").permissions == ["read"]

    def test_remove_missing_perm_returns_false(self):
        store = DocAclStore()
        store.grant("d1", "u1", ["read"])
        assert store.remove_permission("d1", "u1", "write") is False

    def test_remove_from_missing_entry_returns_false(self):
        store = DocAclStore()
        assert store.remove_permission("d1", "u1", "read") is False

    def test_remove_then_add(self):
        store = DocAclStore()
        store.grant("d1", "u1", ["read"])
        assert store.remove_permission("d1", "u1", "read") is True
        assert store.add_permission("d1", "u1", "read") is True


# ------------------------------------------------------------------ get_entry
class TestGetEntry:
    def test_found(self):
        store = DocAclStore()
        store.grant("d1", "u1", ["read"], granted_by="admin", now=10.0)
        entry = store.get_entry("d1", "u1")
        assert entry is not None
        assert entry.granted_by == "admin"
        assert entry.granted_at == 10.0

    def test_missing_doc(self):
        store = DocAclStore()
        store.grant("d1", "u1", ["read"])
        assert store.get_entry("d2", "u1") is None

    def test_missing_principal(self):
        store = DocAclStore()
        store.grant("d1", "u1", ["read"])
        assert store.get_entry("d1", "u2") is None

    def test_missing_both(self):
        store = DocAclStore()
        assert store.get_entry("d1", "u1") is None


# -------------------------------------------------------------- has_permission
class TestHasPermission:
    def test_direct(self):
        store = DocAclStore()
        store.grant("d1", "u1", ["read"])
        assert store.has_permission("d1", "u1", "read") is True
        assert store.has_permission("d1", "u1", "write") is False

    def test_missing_entry(self):
        store = DocAclStore()
        assert store.has_permission("d1", "u1", "read") is False

    def test_via_wildcard(self):
        store = DocAclStore()
        store.grant("d1", "*", ["read"])
        assert store.has_permission("d1", "u1", "read") is True

    def test_wildcard_does_not_grant_write_when_only_read(self):
        store = DocAclStore()
        store.grant("d1", "*", ["read"])
        assert store.has_permission("d1", "u1", "write") is False

    def test_direct_overrides_missing_wildcard(self):
        store = DocAclStore()
        store.grant("d1", "u1", ["write"])
        store.grant("d1", "*", ["read"])
        assert store.has_permission("d1", "u1", "write") is True
        assert store.has_permission("d1", "u1", "read") is True

    def test_wildcard_check_for_wildcard_itself(self):
        store = DocAclStore()
        store.grant("d1", "*", ["read"])
        assert store.has_permission("d1", "*", "read") is True
        assert store.has_permission("d1", "*", "write") is False


# ------------------------------------------------------------- permissions_for
class TestPermissionsFor:
    def test_only_direct(self):
        store = DocAclStore()
        store.grant("d1", "u1", ["write", "read"])
        assert store.permissions_for("d1", "u1") == ["read", "write"]

    def test_only_wildcard(self):
        store = DocAclStore()
        store.grant("d1", "*", ["read"])
        assert store.permissions_for("d1", "u1") == ["read"]

    def test_union_sorted(self):
        store = DocAclStore()
        store.grant("d1", "u1", ["write"])
        store.grant("d1", "*", ["read"])
        assert store.permissions_for("d1", "u1") == ["read", "write"]

    def test_no_entries_returns_empty(self):
        store = DocAclStore()
        assert store.permissions_for("d1", "u1") == []

    def test_wildcard_principal_returns_only_its_perms(self):
        store = DocAclStore()
        store.grant("d1", "*", ["read"])
        assert store.permissions_for("d1", "*") == ["read"]


# ------------------------------------------------------------- principals_for
class TestPrincipalsFor:
    def test_sorted_by_principal(self):
        store = DocAclStore()
        store.grant("d1", "user:c", ["read"])
        store.grant("d1", "user:a", ["read"])
        store.grant("d1", "user:b", ["read"])
        principals = [e.principal for e in store.principals_for("d1")]
        assert principals == ["user:a", "user:b", "user:c"]

    def test_returns_entries(self):
        store = DocAclStore()
        store.grant("d1", "u1", ["read"], granted_by="admin")
        result = store.principals_for("d1")
        assert len(result) == 1
        assert result[0].granted_by == "admin"

    def test_empty_for_missing_doc(self):
        store = DocAclStore()
        assert store.principals_for("none") == []

    def test_isolation_between_docs(self):
        store = DocAclStore()
        store.grant("d1", "u1", ["read"])
        store.grant("d2", "u2", ["read"])
        assert len(store.principals_for("d1")) == 1
        assert store.principals_for("d1")[0].principal == "u1"


# ------------------------------------------------------------ docs_for_principal
class TestDocsForPrincipal:
    def test_sorted(self):
        store = DocAclStore()
        store.grant("d3", "u1", ["read"])
        store.grant("d1", "u1", ["read"])
        store.grant("d2", "u1", ["read"])
        assert store.docs_for_principal("u1") == ["d1", "d2", "d3"]

    def test_missing_principal(self):
        store = DocAclStore()
        assert store.docs_for_principal("ghost") == []

    def test_isolation_between_principals(self):
        store = DocAclStore()
        store.grant("d1", "u1", ["read"])
        store.grant("d2", "u2", ["read"])
        assert store.docs_for_principal("u1") == ["d1"]
        assert store.docs_for_principal("u2") == ["d2"]


# ----------------------------------------------------- principals_with_permission
class TestPrincipalsWithPermission:
    def test_sorted_including_wildcard(self):
        store = DocAclStore()
        store.grant("d1", "user:b", ["read"])
        store.grant("d1", "*", ["read"])
        store.grant("d1", "user:a", ["read"])
        assert store.principals_with_permission("d1", "read") == [
            "*",
            "user:a",
            "user:b",
        ]

    def test_filters_by_permission(self):
        store = DocAclStore()
        store.grant("d1", "u1", ["read"])
        store.grant("d1", "u2", ["write"])
        store.grant("d1", "u3", ["read", "write"])
        assert store.principals_with_permission("d1", "read") == ["u1", "u3"]
        assert store.principals_with_permission("d1", "write") == ["u2", "u3"]

    def test_empty_when_no_one(self):
        store = DocAclStore()
        store.grant("d1", "u1", ["read"])
        assert store.principals_with_permission("d1", "delete") == []

    def test_empty_for_missing_doc(self):
        store = DocAclStore()
        assert store.principals_with_permission("none", "read") == []


# ------------------------------------------------------------------ stats
class TestStats:
    def test_returns_aclstats(self):
        store = DocAclStore()
        store.grant("d1", "u1", ["read"])
        s = store.stats()
        assert isinstance(s, AclStats)

    def test_counts_correctly(self):
        store = DocAclStore()
        store.grant("d1", "u1", ["read"])
        store.grant("d1", "u2", ["read"])
        store.grant("d2", "u1", ["read"])
        s = store.stats()
        assert s.total_entries == 3
        assert s.unique_docs == 2
        assert s.unique_principals == 2

    def test_zero_after_revoke_all(self):
        store = DocAclStore()
        store.grant("d1", "u1", ["read"])
        store.revoke("d1", "u1")
        s = store.stats()
        assert s.total_entries == 0
        assert s.unique_docs == 0
        assert s.unique_principals == 0

    def test_replace_does_not_inflate(self):
        store = DocAclStore()
        store.grant("d1", "u1", ["read"])
        store.grant("d1", "u1", ["write"])
        s = store.stats()
        assert s.total_entries == 1


# --------------------------------------------------------------- thread safety
class TestThreadSafety:
    def test_concurrent_grants(self):
        store = DocAclStore()

        def worker(start: int) -> None:
            for i in range(start, start + 50):
                store.grant(f"d{i}", f"u{i}", ["read"])

        threads = [threading.Thread(target=worker, args=(i * 50,)) for i in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        s = store.stats()
        assert s.total_entries == 8 * 50
        assert s.unique_docs == 8 * 50
        assert s.unique_principals == 8 * 50

    def test_concurrent_grant_and_revoke(self):
        store = DocAclStore()
        for i in range(200):
            store.grant(f"d{i}", "u1", ["read"])

        results = {"granted": 0, "revoked": 0}
        lock = threading.Lock()

        def grant_more() -> None:
            count = 0
            for i in range(200, 400):
                store.grant(f"d{i}", "u1", ["read"])
                count += 1
            with lock:
                results["granted"] += count

        def revoke_some() -> None:
            count = 0
            for i in range(0, 200):
                if store.revoke(f"d{i}", "u1"):
                    count += 1
            with lock:
                results["revoked"] += count

        threads = [
            threading.Thread(target=grant_more),
            threading.Thread(target=revoke_some),
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert results["granted"] == 200
        assert results["revoked"] == 200
        assert store.stats().total_entries == 200

    def test_concurrent_add_permission(self):
        store = DocAclStore()
        store.grant("d1", "u1", [])

        def worker(perm: str) -> None:
            store.add_permission("d1", "u1", perm)

        perms = [f"perm{i}" for i in range(100)]
        threads = [threading.Thread(target=worker, args=(p,)) for p in perms]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        entry = store.get_entry("d1", "u1")
        assert sorted(entry.permissions) == sorted(perms)
