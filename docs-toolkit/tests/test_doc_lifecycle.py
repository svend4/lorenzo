"""Tests for docstoolkit.doc_lifecycle — document lifecycle management."""

import threading

import pytest

from docstoolkit.doc_lifecycle import (
    DocLifecycle,
    DocLifecycleManager,
    LifecyclePolicy,
    LifecycleStage,
    LifecycleStats,
)


DAY = 86400.0


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def manager() -> DocLifecycleManager:
    return DocLifecycleManager()


# ---------------------------------------------------------------------------

class TestLifecycleStage:
    def test_values(self):
        assert LifecycleStage.NEW.value == "new"
        assert LifecycleStage.ACTIVE.value == "active"
        assert LifecycleStage.INACTIVE.value == "inactive"
        assert LifecycleStage.ARCHIVED.value == "archived"
        assert LifecycleStage.EXPIRED.value == "expired"
        assert LifecycleStage.DELETED.value == "deleted"

    def test_is_str_enum(self):
        # str subclass for serialization friendliness
        assert isinstance(LifecycleStage.NEW, str)

    def test_membership(self):
        assert LifecycleStage("active") == LifecycleStage.ACTIVE


class TestLifecyclePolicy:
    def test_defaults(self):
        p = LifecyclePolicy(policy_id="p1", name="basic")
        assert p.policy_id == "p1"
        assert p.name == "basic"
        assert p.inactive_after_days is None
        assert p.archive_after_days is None
        assert p.delete_after_days is None
        assert p.categories == []
        assert p.enabled is True

    def test_with_fields(self):
        p = LifecyclePolicy(
            policy_id="p2",
            name="full",
            inactive_after_days=30,
            archive_after_days=60,
            delete_after_days=365,
            categories=["draft"],
        )
        assert p.inactive_after_days == 30
        assert p.archive_after_days == 60
        assert p.delete_after_days == 365
        assert p.categories == ["draft"]


class TestDocLifecycle:
    def test_defaults(self):
        d = DocLifecycle(doc_id="doc1", stage=LifecycleStage.NEW, created_at=100.0)
        assert d.doc_id == "doc1"
        assert d.stage == LifecycleStage.NEW
        assert d.created_at == 100.0
        assert d.last_accessed == 0.0
        assert d.inactive_since is None
        assert d.archived_at is None
        assert d.expires_at is None
        assert d.deleted_at is None
        assert d.categories == []
        assert d.policy_id is None

    def test_with_fields(self):
        d = DocLifecycle(
            doc_id="doc2",
            stage=LifecycleStage.ACTIVE,
            created_at=0,
            categories=["x"],
            policy_id="p1",
        )
        assert d.categories == ["x"]
        assert d.policy_id == "p1"


class TestLifecycleStats:
    def test_construct(self):
        s = LifecycleStats(
            total=10,
            by_stage={"active": 5, "archived": 5},
            policies_count=2,
            eligible_for_archive=1,
            eligible_for_deletion=0,
        )
        assert s.total == 10
        assert s.policies_count == 2
        assert s.by_stage["active"] == 5


class TestAddPolicy:
    def test_add_policy_minimal(self, manager):
        p = manager.add_policy(name="basic")
        assert p.name == "basic"
        assert p.policy_id
        assert manager.policy_count == 1

    def test_add_policy_full(self, manager):
        p = manager.add_policy(
            name="legal",
            inactive_after_days=30,
            archive_after_days=60,
            delete_after_days=365,
            categories=["legal", "compliance"],
        )
        assert p.inactive_after_days == 30
        assert p.archive_after_days == 60
        assert p.delete_after_days == 365
        assert p.categories == ["legal", "compliance"]
        assert p.enabled is True

    def test_add_multiple_policies(self, manager):
        manager.add_policy(name="a")
        manager.add_policy(name="b")
        manager.add_policy(name="c")
        assert manager.policy_count == 3

    def test_add_policy_unique_ids(self, manager):
        p1 = manager.add_policy(name="a")
        p2 = manager.add_policy(name="b")
        assert p1.policy_id != p2.policy_id


class TestRemovePolicy:
    def test_remove_existing(self, manager):
        p = manager.add_policy(name="x")
        assert manager.remove_policy(p.policy_id) is True
        assert manager.policy_count == 0

    def test_remove_nonexistent(self, manager):
        assert manager.remove_policy("missing") is False

    def test_remove_detaches_docs(self, manager):
        p = manager.add_policy(name="x")
        d = manager.register("doc1", policy_id=p.policy_id)
        assert d.policy_id == p.policy_id
        manager.remove_policy(p.policy_id)
        assert manager.get("doc1").policy_id is None


class TestRegister:
    def test_register_basic(self, manager):
        d = manager.register("doc1", now=100.0)
        assert d.doc_id == "doc1"
        assert d.stage == LifecycleStage.NEW
        assert d.created_at == 100.0
        assert d.last_accessed == 100.0

    def test_register_with_categories(self, manager):
        d = manager.register("doc1", categories=["draft"], now=10.0)
        assert d.categories == ["draft"]

    def test_register_with_explicit_policy(self, manager):
        p = manager.add_policy(name="x")
        d = manager.register("doc1", policy_id=p.policy_id)
        assert d.policy_id == p.policy_id

    def test_register_auto_matches_policy(self, manager):
        p = manager.add_policy(name="drafts", categories=["draft"])
        d = manager.register("doc1", categories=["draft"])
        assert d.policy_id == p.policy_id

    def test_register_invalid_policy_id_becomes_none(self, manager):
        d = manager.register("doc1", policy_id="bogus")
        assert d.policy_id is None

    def test_register_no_policy_match(self, manager):
        manager.add_policy(name="drafts", categories=["draft"])
        d = manager.register("doc1", categories=["other"])
        assert d.policy_id is None


class TestRecordAccess:
    def test_updates_last_accessed(self, manager):
        manager.register("doc1", now=0.0)
        assert manager.record_access("doc1", now=500.0) is True
        assert manager.get("doc1").last_accessed == 500.0

    def test_unknown_doc(self, manager):
        assert manager.record_access("missing", now=100.0) is False

    def test_new_becomes_active(self, manager):
        manager.register("doc1", now=0.0)
        manager.record_access("doc1", now=10.0)
        assert manager.get("doc1").stage == LifecycleStage.ACTIVE

    def test_deleted_not_accessible(self, manager):
        manager.register("doc1", now=0.0)
        manager.delete_now("doc1", now=10.0)
        assert manager.record_access("doc1", now=20.0) is False


class TestRecordAccessReactivates:
    def test_inactive_becomes_active(self, manager):
        p = manager.add_policy(name="p", inactive_after_days=1)
        manager.register("doc1", policy_id=p.policy_id, now=0.0)
        manager.record_access("doc1", now=0.0)  # ACTIVE
        manager.evaluate_policies(now=2 * DAY)
        assert manager.get("doc1").stage == LifecycleStage.INACTIVE
        manager.record_access("doc1", now=3 * DAY)
        d = manager.get("doc1")
        assert d.stage == LifecycleStage.ACTIVE
        assert d.inactive_since is None
        assert d.last_accessed == 3 * DAY


class TestGet:
    def test_get_existing(self, manager):
        manager.register("doc1")
        assert manager.get("doc1") is not None

    def test_get_missing(self, manager):
        assert manager.get("missing") is None


class TestArchiveNow:
    def test_archive_active(self, manager):
        manager.register("doc1", now=0.0)
        manager.record_access("doc1", now=10.0)
        assert manager.archive_now("doc1", now=20.0) is True
        d = manager.get("doc1")
        assert d.stage == LifecycleStage.ARCHIVED
        assert d.archived_at == 20.0

    def test_archive_unknown(self, manager):
        assert manager.archive_now("missing") is False

    def test_archive_already_archived(self, manager):
        manager.register("doc1")
        manager.archive_now("doc1", now=1.0)
        assert manager.archive_now("doc1", now=2.0) is False

    def test_archive_deleted_fails(self, manager):
        manager.register("doc1")
        manager.delete_now("doc1", now=1.0)
        assert manager.archive_now("doc1", now=2.0) is False


class TestDeleteNow:
    def test_delete_active(self, manager):
        manager.register("doc1", now=0.0)
        assert manager.delete_now("doc1", now=10.0) is True
        d = manager.get("doc1")
        assert d.stage == LifecycleStage.DELETED
        assert d.deleted_at == 10.0

    def test_delete_unknown(self, manager):
        assert manager.delete_now("missing") is False

    def test_delete_already_deleted(self, manager):
        manager.register("doc1")
        manager.delete_now("doc1", now=1.0)
        assert manager.delete_now("doc1", now=2.0) is False

    def test_delete_archived_ok(self, manager):
        manager.register("doc1")
        manager.archive_now("doc1", now=1.0)
        assert manager.delete_now("doc1", now=2.0) is True


class TestRestore:
    def test_restore_archived(self, manager):
        manager.register("doc1", now=0.0)
        manager.archive_now("doc1", now=10.0)
        assert manager.restore("doc1", now=20.0) is True
        d = manager.get("doc1")
        assert d.stage == LifecycleStage.ACTIVE
        assert d.archived_at is None
        assert d.last_accessed == 20.0

    def test_restore_active_fails(self, manager):
        manager.register("doc1")
        manager.record_access("doc1", now=1.0)
        assert manager.restore("doc1", now=2.0) is False

    def test_restore_unknown(self, manager):
        assert manager.restore("missing") is False

    def test_restore_deleted_fails(self, manager):
        manager.register("doc1")
        manager.delete_now("doc1", now=1.0)
        assert manager.restore("doc1", now=2.0) is False


class TestEvaluatePolicies:
    def test_active_to_inactive(self, manager):
        p = manager.add_policy(name="p", inactive_after_days=7)
        manager.register("doc1", policy_id=p.policy_id, now=0.0)
        manager.record_access("doc1", now=0.0)
        result = manager.evaluate_policies(now=8 * DAY)
        assert result["inactivated"] == 1
        assert manager.get("doc1").stage == LifecycleStage.INACTIVE

    def test_inactive_to_archived(self, manager):
        p = manager.add_policy(
            name="p", inactive_after_days=1, archive_after_days=3
        )
        manager.register("doc1", policy_id=p.policy_id, now=0.0)
        manager.record_access("doc1", now=0.0)
        # Step 1: become inactive at t=2*DAY
        manager.evaluate_policies(now=2 * DAY)
        # Step 2: 4 days later, should be archived
        result = manager.evaluate_policies(now=6 * DAY)
        assert result["archived"] == 1
        assert manager.get("doc1").stage == LifecycleStage.ARCHIVED

    def test_archived_to_deleted(self, manager):
        p = manager.add_policy(name="p", delete_after_days=10)
        manager.register("doc1", policy_id=p.policy_id, now=0.0)
        manager.archive_now("doc1", now=0.0)
        result = manager.evaluate_policies(now=11 * DAY)
        assert result["deleted"] == 1
        assert manager.get("doc1").stage == LifecycleStage.DELETED

    def test_full_chain(self, manager):
        p = manager.add_policy(
            name="p",
            inactive_after_days=1,
            archive_after_days=1,
            delete_after_days=1,
        )
        manager.register("doc1", policy_id=p.policy_id, now=0.0)
        manager.record_access("doc1", now=0.0)
        # Run sequentially
        manager.evaluate_policies(now=2 * DAY)
        assert manager.get("doc1").stage == LifecycleStage.INACTIVE
        manager.evaluate_policies(now=4 * DAY)
        assert manager.get("doc1").stage == LifecycleStage.ARCHIVED
        manager.evaluate_policies(now=6 * DAY)
        assert manager.get("doc1").stage == LifecycleStage.DELETED

    def test_no_policy_no_change(self, manager):
        manager.register("doc1", now=0.0)
        manager.record_access("doc1", now=0.0)
        result = manager.evaluate_policies(now=100 * DAY)
        assert result == {"inactivated": 0, "archived": 0, "deleted": 0}
        assert manager.get("doc1").stage == LifecycleStage.ACTIVE

    def test_disabled_policy_skipped(self, manager):
        p = manager.add_policy(name="p", inactive_after_days=1)
        manager.register("doc1", policy_id=p.policy_id, now=0.0)
        manager.record_access("doc1", now=0.0)
        p.enabled = False
        manager.evaluate_policies(now=10 * DAY)
        assert manager.get("doc1").stage == LifecycleStage.ACTIVE

    def test_not_yet_inactive(self, manager):
        p = manager.add_policy(name="p", inactive_after_days=10)
        manager.register("doc1", policy_id=p.policy_id, now=0.0)
        manager.record_access("doc1", now=0.0)
        result = manager.evaluate_policies(now=1 * DAY)
        assert result["inactivated"] == 0
        assert manager.get("doc1").stage == LifecycleStage.ACTIVE


class TestFindMatchingPolicy:
    def test_no_policies(self, manager):
        assert manager.find_matching_policy(["x"]) is None

    def test_empty_categories_match_everything(self, manager):
        p = manager.add_policy(name="catch-all")
        assert manager.find_matching_policy(["any"]) == p

    def test_specific_match(self, manager):
        p = manager.add_policy(name="drafts", categories=["draft"])
        assert manager.find_matching_policy(["draft"]) == p

    def test_no_match(self, manager):
        manager.add_policy(name="drafts", categories=["draft"])
        assert manager.find_matching_policy(["other"]) is None

    def test_disabled_skipped(self, manager):
        p = manager.add_policy(name="drafts", categories=["draft"])
        p.enabled = False
        assert manager.find_matching_policy(["draft"]) is None

    def test_first_enabled_wins(self, manager):
        p1 = manager.add_policy(name="a", categories=["x"])
        manager.add_policy(name="b", categories=["x"])
        assert manager.find_matching_policy(["x"]) == p1


class TestDocsInStage:
    def test_empty(self, manager):
        assert manager.docs_in_stage(LifecycleStage.ACTIVE) == []

    def test_filters_by_stage(self, manager):
        manager.register("a", now=0.0)
        manager.register("b", now=0.0)
        manager.record_access("a", now=1.0)
        manager.archive_now("b", now=1.0)
        active = manager.docs_in_stage(LifecycleStage.ACTIVE)
        archived = manager.docs_in_stage(LifecycleStage.ARCHIVED)
        assert len(active) == 1 and active[0].doc_id == "a"
        assert len(archived) == 1 and archived[0].doc_id == "b"

    def test_new_stage(self, manager):
        manager.register("a")
        result = manager.docs_in_stage(LifecycleStage.NEW)
        assert len(result) == 1


class TestEligibleForArchive:
    def test_no_eligible(self, manager):
        manager.register("a", now=0.0)
        assert manager.eligible_for_archive(now=100 * DAY) == []

    def test_inactive_ready(self, manager):
        p = manager.add_policy(
            name="p", inactive_after_days=1, archive_after_days=3
        )
        manager.register("a", policy_id=p.policy_id, now=0.0)
        manager.record_access("a", now=0.0)
        manager.evaluate_policies(now=2 * DAY)  # → INACTIVE at t=2*DAY
        result = manager.eligible_for_archive(now=6 * DAY)
        assert len(result) == 1

    def test_inactive_not_yet(self, manager):
        p = manager.add_policy(
            name="p", inactive_after_days=1, archive_after_days=10
        )
        manager.register("a", policy_id=p.policy_id, now=0.0)
        manager.record_access("a", now=0.0)
        manager.evaluate_policies(now=2 * DAY)
        assert manager.eligible_for_archive(now=5 * DAY) == []

    def test_no_policy_excluded(self, manager):
        manager.register("a", now=0.0)
        # Manually mutate to INACTIVE without policy
        d = manager.get("a")
        d.stage = LifecycleStage.INACTIVE
        d.inactive_since = 0.0
        assert manager.eligible_for_archive(now=100 * DAY) == []


class TestEligibleForDeletion:
    def test_no_eligible(self, manager):
        manager.register("a", now=0.0)
        assert manager.eligible_for_deletion(now=100 * DAY) == []

    def test_archived_ready(self, manager):
        p = manager.add_policy(name="p", delete_after_days=5)
        manager.register("a", policy_id=p.policy_id, now=0.0)
        manager.archive_now("a", now=0.0)
        result = manager.eligible_for_deletion(now=6 * DAY)
        assert len(result) == 1

    def test_archived_not_yet(self, manager):
        p = manager.add_policy(name="p", delete_after_days=10)
        manager.register("a", policy_id=p.policy_id, now=0.0)
        manager.archive_now("a", now=0.0)
        assert manager.eligible_for_deletion(now=5 * DAY) == []

    def test_disabled_policy_excluded(self, manager):
        p = manager.add_policy(name="p", delete_after_days=1)
        manager.register("a", policy_id=p.policy_id, now=0.0)
        manager.archive_now("a", now=0.0)
        p.enabled = False
        assert manager.eligible_for_deletion(now=100 * DAY) == []


class TestStats:
    def test_empty(self, manager):
        s = manager.stats()
        assert s.total == 0
        assert s.policies_count == 0
        assert s.eligible_for_archive == 0
        assert s.eligible_for_deletion == 0

    def test_counts_by_stage(self, manager):
        manager.register("a")
        manager.register("b")
        manager.record_access("a", now=1.0)
        s = manager.stats()
        assert s.total == 2
        assert s.by_stage["active"] == 1
        assert s.by_stage["new"] == 1

    def test_with_policies(self, manager):
        manager.add_policy(name="p1")
        manager.add_policy(name="p2")
        s = manager.stats()
        assert s.policies_count == 2


class TestPolicyCount:
    def test_zero(self, manager):
        assert manager.policy_count == 0

    def test_increments(self, manager):
        manager.add_policy(name="x")
        assert manager.policy_count == 1
        manager.add_policy(name="y")
        assert manager.policy_count == 2

    def test_decrements(self, manager):
        p = manager.add_policy(name="x")
        manager.remove_policy(p.policy_id)
        assert manager.policy_count == 0


class TestDocCount:
    def test_zero(self, manager):
        assert manager.doc_count == 0

    def test_increments(self, manager):
        manager.register("a")
        assert manager.doc_count == 1
        manager.register("b")
        assert manager.doc_count == 2


class TestListPolicies:
    def test_empty(self, manager):
        assert manager.list_policies() == []

    def test_all(self, manager):
        manager.add_policy(name="a")
        manager.add_policy(name="b")
        assert len(manager.list_policies()) == 2

    def test_enabled_only(self, manager):
        p1 = manager.add_policy(name="a")
        p2 = manager.add_policy(name="b")
        p2.enabled = False
        enabled = manager.list_policies(enabled_only=True)
        assert len(enabled) == 1
        assert enabled[0].policy_id == p1.policy_id


class TestClear:
    def test_clears_all(self, manager):
        manager.add_policy(name="p")
        manager.register("doc1")
        manager.clear()
        assert manager.policy_count == 0
        assert manager.doc_count == 0

    def test_clear_empty(self, manager):
        manager.clear()
        assert manager.doc_count == 0


class TestEdgeCases:
    def test_register_duplicate_overwrites(self, manager):
        manager.register("doc1", now=0.0)
        manager.register("doc1", now=100.0)
        assert manager.get("doc1").created_at == 100.0
        assert manager.doc_count == 1

    def test_evaluate_with_no_docs(self, manager):
        manager.add_policy(name="p", inactive_after_days=1)
        result = manager.evaluate_policies(now=10 * DAY)
        assert result == {"inactivated": 0, "archived": 0, "deleted": 0}

    def test_evaluate_doc_without_inactive_since_baseline(self, manager):
        # Manually engineer an INACTIVE doc without inactive_since
        p = manager.add_policy(name="p", archive_after_days=1)
        manager.register("a", policy_id=p.policy_id, now=0.0)
        d = manager.get("a")
        d.stage = LifecycleStage.INACTIVE
        d.inactive_since = None
        result = manager.evaluate_policies(now=10 * DAY)
        # Should set baseline, not crash
        assert manager.get("a").inactive_since is not None
        assert result["archived"] == 0

    def test_thread_safety(self, manager):
        p = manager.add_policy(name="p")
        errors = []

        def worker(i):
            try:
                manager.register(f"doc-{i}", policy_id=p.policy_id, now=float(i))
                manager.record_access(f"doc-{i}", now=float(i) + 1)
            except Exception as e:  # pragma: no cover
                errors.append(e)

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(50)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert errors == []
        assert manager.doc_count == 50

    def test_remove_policy_keeps_docs(self, manager):
        p = manager.add_policy(name="x")
        manager.register("doc1", policy_id=p.policy_id)
        manager.remove_policy(p.policy_id)
        assert manager.doc_count == 1
        assert manager.get("doc1") is not None

    def test_categories_isolated(self, manager):
        cats = ["a", "b"]
        d = manager.register("doc1", categories=cats)
        cats.append("c")
        assert "c" not in d.categories

    def test_policy_categories_isolated(self, manager):
        cats = ["a"]
        p = manager.add_policy(name="x", categories=cats)
        cats.append("b")
        assert "b" not in p.categories
