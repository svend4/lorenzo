"""Tests for E379 DocHistoryPruner."""

from __future__ import annotations

import threading
import time

import pytest

from docstoolkit.doc_history_pruner import (
    DocHistoryPruner,
    HistoryVersion,
    PruneResult,
    PruneRule,
    PrunerStats,
)


# --------------------------------------------------------------------------- #
# Dataclass tests
# --------------------------------------------------------------------------- #


class TestHistoryVersionDataclass:
    def test_create_minimal(self):
        v = HistoryVersion(version_id="v1", doc_id="d1", created_at=10.0)
        assert v.version_id == "v1"
        assert v.doc_id == "d1"
        assert v.created_at == 10.0

    def test_default_size_bytes(self):
        v = HistoryVersion(version_id="v1", doc_id="d1", created_at=10.0)
        assert v.size_bytes == 0

    def test_default_kept(self):
        v = HistoryVersion(version_id="v1", doc_id="d1", created_at=10.0)
        assert v.kept is True

    def test_custom_size_bytes(self):
        v = HistoryVersion(version_id="v1", doc_id="d1", created_at=10.0, size_bytes=512)
        assert v.size_bytes == 512

    def test_kept_false(self):
        v = HistoryVersion(version_id="v1", doc_id="d1", created_at=10.0, kept=False)
        assert v.kept is False

    def test_equality(self):
        a = HistoryVersion(version_id="v1", doc_id="d1", created_at=10.0)
        b = HistoryVersion(version_id="v1", doc_id="d1", created_at=10.0)
        assert a == b


class TestPruneRuleDataclass:
    def test_create_minimal(self):
        r = PruneRule(rule_id="r1", pattern="*")
        assert r.rule_id == "r1"
        assert r.pattern == "*"

    def test_default_max_versions(self):
        r = PruneRule(rule_id="r1", pattern="*")
        assert r.max_versions is None

    def test_default_max_age(self):
        r = PruneRule(rule_id="r1", pattern="*")
        assert r.max_age_seconds is None

    def test_default_priority(self):
        r = PruneRule(rule_id="r1", pattern="*")
        assert r.priority == 0

    def test_custom_max_versions(self):
        r = PruneRule(rule_id="r1", pattern="*", max_versions=5)
        assert r.max_versions == 5

    def test_custom_max_age(self):
        r = PruneRule(rule_id="r1", pattern="*", max_age_seconds=3600.0)
        assert r.max_age_seconds == 3600.0


class TestPruneResultDataclass:
    def test_create_minimal(self):
        r = PruneResult(doc_id="d1")
        assert r.doc_id == "d1"

    def test_default_pruned_versions(self):
        r = PruneResult(doc_id="d1")
        assert r.pruned_versions == []

    def test_default_kept_versions(self):
        r = PruneResult(doc_id="d1")
        assert r.kept_versions == []

    def test_default_applied_rule(self):
        r = PruneResult(doc_id="d1")
        assert r.applied_rule is None

    def test_default_pruned_count(self):
        r = PruneResult(doc_id="d1")
        assert r.pruned_count == 0

    def test_default_lists_distinct(self):
        a = PruneResult(doc_id="a")
        b = PruneResult(doc_id="b")
        a.pruned_versions.append("v1")
        assert b.pruned_versions == []


class TestPrunerStatsDataclass:
    def test_create(self):
        s = PrunerStats(total_versions=10, total_rules=2, unique_docs=3, total_pruned=4)
        assert s.total_versions == 10
        assert s.total_rules == 2
        assert s.unique_docs == 3
        assert s.total_pruned == 4

    def test_equality(self):
        a = PrunerStats(total_versions=1, total_rules=2, unique_docs=3, total_pruned=4)
        b = PrunerStats(total_versions=1, total_rules=2, unique_docs=3, total_pruned=4)
        assert a == b


# --------------------------------------------------------------------------- #
# Construction
# --------------------------------------------------------------------------- #


class TestConstruction:
    def test_empty(self):
        p = DocHistoryPruner()
        assert p.all_doc_ids() == []

    def test_no_rules(self):
        p = DocHistoryPruner()
        assert p.list_rules() == []

    def test_stats_empty(self):
        p = DocHistoryPruner()
        s = p.stats()
        assert s.total_versions == 0
        assert s.total_rules == 0
        assert s.unique_docs == 0
        assert s.total_pruned == 0


# --------------------------------------------------------------------------- #
# add_version
# --------------------------------------------------------------------------- #


class TestAddVersion:
    def test_add_single(self):
        p = DocHistoryPruner()
        v = p.add_version("d1", "v1", 10.0)
        assert v.version_id == "v1"
        assert v.doc_id == "d1"
        assert v.created_at == 10.0

    def test_add_returns_kept(self):
        p = DocHistoryPruner()
        v = p.add_version("d1", "v1", 10.0)
        assert v.kept is True

    def test_add_with_size(self):
        p = DocHistoryPruner()
        v = p.add_version("d1", "v1", 10.0, size_bytes=42)
        assert v.size_bytes == 42

    def test_add_multiple(self):
        p = DocHistoryPruner()
        p.add_version("d1", "v1", 10.0)
        p.add_version("d1", "v2", 20.0)
        assert len(p.versions_for("d1")) == 2

    def test_add_duplicate_replaces(self):
        p = DocHistoryPruner()
        p.add_version("d1", "v1", 10.0, size_bytes=1)
        p.add_version("d1", "v1", 10.0, size_bytes=99)
        versions = p.versions_for("d1")
        assert len(versions) == 1
        assert versions[0].size_bytes == 99

    def test_add_updates_unique_docs(self):
        p = DocHistoryPruner()
        p.add_version("d1", "v1", 10.0)
        p.add_version("d2", "v1", 10.0)
        assert p.stats().unique_docs == 2


# --------------------------------------------------------------------------- #
# remove_version
# --------------------------------------------------------------------------- #


class TestRemoveVersion:
    def test_remove_existing(self):
        p = DocHistoryPruner()
        p.add_version("d1", "v1", 10.0)
        assert p.remove_version("d1", "v1") is True

    def test_remove_unknown(self):
        p = DocHistoryPruner()
        assert p.remove_version("d1", "v1") is False

    def test_remove_cleans_doc_index(self):
        p = DocHistoryPruner()
        p.add_version("d1", "v1", 10.0)
        p.remove_version("d1", "v1")
        assert p.all_doc_ids() == []

    def test_remove_keeps_other_versions(self):
        p = DocHistoryPruner()
        p.add_version("d1", "v1", 10.0)
        p.add_version("d1", "v2", 20.0)
        p.remove_version("d1", "v1")
        assert len(p.versions_for("d1")) == 1


# --------------------------------------------------------------------------- #
# add_rule
# --------------------------------------------------------------------------- #


class TestAddRule:
    def test_add_rule(self):
        p = DocHistoryPruner()
        p.add_rule(PruneRule(rule_id="r1", pattern="*"))
        assert len(p.list_rules()) == 1

    def test_add_rule_replaces(self):
        p = DocHistoryPruner()
        p.add_rule(PruneRule(rule_id="r1", pattern="*", max_versions=1))
        p.add_rule(PruneRule(rule_id="r1", pattern="*", max_versions=5))
        rules = p.list_rules()
        assert len(rules) == 1
        assert rules[0].max_versions == 5

    def test_stats_total_rules(self):
        p = DocHistoryPruner()
        p.add_rule(PruneRule(rule_id="r1", pattern="*"))
        p.add_rule(PruneRule(rule_id="r2", pattern="x*"))
        assert p.stats().total_rules == 2


# --------------------------------------------------------------------------- #
# remove_rule
# --------------------------------------------------------------------------- #


class TestRemoveRule:
    def test_remove_existing(self):
        p = DocHistoryPruner()
        p.add_rule(PruneRule(rule_id="r1", pattern="*"))
        assert p.remove_rule("r1") is True

    def test_remove_unknown(self):
        p = DocHistoryPruner()
        assert p.remove_rule("rx") is False

    def test_remove_decrements_count(self):
        p = DocHistoryPruner()
        p.add_rule(PruneRule(rule_id="r1", pattern="*"))
        p.remove_rule("r1")
        assert p.stats().total_rules == 0


# --------------------------------------------------------------------------- #
# versions_for
# --------------------------------------------------------------------------- #


class TestVersionsFor:
    def test_empty(self):
        p = DocHistoryPruner()
        assert p.versions_for("d1") == []

    def test_sorted_desc(self):
        p = DocHistoryPruner()
        p.add_version("d1", "old", 1.0)
        p.add_version("d1", "new", 100.0)
        p.add_version("d1", "mid", 50.0)
        ids = [v.version_id for v in p.versions_for("d1")]
        assert ids == ["new", "mid", "old"]

    def test_isolated_per_doc(self):
        p = DocHistoryPruner()
        p.add_version("d1", "v1", 10.0)
        p.add_version("d2", "v2", 20.0)
        assert len(p.versions_for("d1")) == 1
        assert len(p.versions_for("d2")) == 1


# --------------------------------------------------------------------------- #
# prune by max_versions
# --------------------------------------------------------------------------- #


class TestPruneByMaxVersions:
    def test_keeps_newest(self):
        p = DocHistoryPruner()
        for i in range(5):
            p.add_version("d1", f"v{i}", float(i))
        p.add_rule(PruneRule(rule_id="r1", pattern="d1", max_versions=2))
        result = p.prune("d1")
        assert sorted(result.kept_versions) == ["v3", "v4"]

    def test_prunes_older(self):
        p = DocHistoryPruner()
        for i in range(5):
            p.add_version("d1", f"v{i}", float(i))
        p.add_rule(PruneRule(rule_id="r1", pattern="d1", max_versions=2))
        result = p.prune("d1")
        assert sorted(result.pruned_versions) == ["v0", "v1", "v2"]

    def test_pruned_count(self):
        p = DocHistoryPruner()
        for i in range(5):
            p.add_version("d1", f"v{i}", float(i))
        p.add_rule(PruneRule(rule_id="r1", pattern="d1", max_versions=2))
        result = p.prune("d1")
        assert result.pruned_count == 3

    def test_no_pruning_needed(self):
        p = DocHistoryPruner()
        p.add_version("d1", "v0", 0.0)
        p.add_rule(PruneRule(rule_id="r1", pattern="d1", max_versions=10))
        result = p.prune("d1")
        assert result.pruned_count == 0

    def test_marks_kept_false(self):
        p = DocHistoryPruner()
        for i in range(3):
            p.add_version("d1", f"v{i}", float(i))
        p.add_rule(PruneRule(rule_id="r1", pattern="d1", max_versions=1))
        p.prune("d1")
        kept_flags = {v.version_id: v.kept for v in p.versions_for("d1")}
        assert kept_flags == {"v0": False, "v1": False, "v2": True}


# --------------------------------------------------------------------------- #
# prune by max_age
# --------------------------------------------------------------------------- #


class TestPruneByMaxAge:
    def test_drops_old(self):
        p = DocHistoryPruner()
        p.add_version("d1", "vold", 0.0)
        p.add_version("d1", "vnew", 100.0)
        p.add_rule(PruneRule(rule_id="r1", pattern="d1", max_age_seconds=50.0))
        result = p.prune("d1", now=110.0)
        assert "vold" in result.pruned_versions
        assert "vnew" not in result.pruned_versions

    def test_keeps_recent(self):
        p = DocHistoryPruner()
        p.add_version("d1", "vnew", 100.0)
        p.add_rule(PruneRule(rule_id="r1", pattern="d1", max_age_seconds=50.0))
        result = p.prune("d1", now=120.0)
        assert result.pruned_count == 0
        assert result.kept_versions == ["vnew"]

    def test_all_old(self):
        p = DocHistoryPruner()
        p.add_version("d1", "a", 0.0)
        p.add_version("d1", "b", 1.0)
        p.add_rule(PruneRule(rule_id="r1", pattern="d1", max_age_seconds=0.5))
        result = p.prune("d1", now=1000.0)
        assert result.pruned_count == 2

    def test_combined_with_max_versions(self):
        p = DocHistoryPruner()
        # created_at values close to "now" so age check leaves recent ones alone
        for i in range(5):
            p.add_version("d1", f"v{i}", 100.0 + float(i))
        p.add_rule(
            PruneRule(
                rule_id="r1",
                pattern="d1",
                max_versions=3,
                max_age_seconds=10.0,
            )
        )
        result = p.prune("d1", now=105.0)
        # max_versions=3 keeps v2,v3,v4. Threshold = 105 - 10 = 95, all survive.
        assert "v4" in result.kept_versions
        assert "v0" in result.pruned_versions


# --------------------------------------------------------------------------- #
# prune no rule
# --------------------------------------------------------------------------- #


class TestPruneNoRule:
    def test_no_rule_empty_result(self):
        p = DocHistoryPruner()
        p.add_version("d1", "v1", 1.0)
        result = p.prune("d1")
        assert result.applied_rule is None
        assert result.pruned_count == 0
        assert result.pruned_versions == []
        assert result.kept_versions == []

    def test_no_matching_rule(self):
        p = DocHistoryPruner()
        p.add_version("d1", "v1", 1.0)
        p.add_rule(PruneRule(rule_id="r1", pattern="other*", max_versions=1))
        result = p.prune("d1")
        assert result.applied_rule is None

    def test_priority_picks_highest(self):
        p = DocHistoryPruner()
        for i in range(5):
            p.add_version("d1", f"v{i}", float(i))
        p.add_rule(PruneRule(rule_id="low", pattern="*", max_versions=4, priority=1))
        p.add_rule(PruneRule(rule_id="high", pattern="*", max_versions=1, priority=10))
        result = p.prune("d1")
        assert result.applied_rule == "high"
        assert result.pruned_count == 4


# --------------------------------------------------------------------------- #
# prune_all
# --------------------------------------------------------------------------- #


class TestPruneAll:
    def test_prune_all_returns_only_matching(self):
        p = DocHistoryPruner()
        p.add_version("d1", "v1", 1.0)
        p.add_version("d2", "v1", 1.0)
        p.add_rule(PruneRule(rule_id="r1", pattern="d1", max_versions=0))
        results = p.prune_all()
        ids = [r.doc_id for r in results]
        assert ids == ["d1"]

    def test_prune_all_multiple(self):
        p = DocHistoryPruner()
        for d in ["a", "b", "c"]:
            for i in range(3):
                p.add_version(d, f"v{i}", float(i))
        p.add_rule(PruneRule(rule_id="r1", pattern="*", max_versions=1))
        results = p.prune_all()
        assert len(results) == 3

    def test_prune_all_empty(self):
        p = DocHistoryPruner()
        assert p.prune_all() == []


# --------------------------------------------------------------------------- #
# delete_pruned
# --------------------------------------------------------------------------- #


class TestDeletePruned:
    def test_returns_count(self):
        p = DocHistoryPruner()
        for i in range(3):
            p.add_version("d1", f"v{i}", float(i))
        p.add_rule(PruneRule(rule_id="r1", pattern="d1", max_versions=1))
        p.prune("d1")
        assert p.delete_pruned("d1") == 2

    def test_removes_from_store(self):
        p = DocHistoryPruner()
        for i in range(3):
            p.add_version("d1", f"v{i}", float(i))
        p.add_rule(PruneRule(rule_id="r1", pattern="d1", max_versions=1))
        p.prune("d1")
        p.delete_pruned("d1")
        assert len(p.versions_for("d1")) == 1

    def test_does_not_affect_kept(self):
        p = DocHistoryPruner()
        p.add_version("d1", "v1", 1.0)
        assert p.delete_pruned("d1") == 0
        assert len(p.versions_for("d1")) == 1

    def test_unknown_doc(self):
        p = DocHistoryPruner()
        assert p.delete_pruned("nope") == 0


# --------------------------------------------------------------------------- #
# kept_versions_for
# --------------------------------------------------------------------------- #


class TestKeptVersionsFor:
    def test_only_kept(self):
        p = DocHistoryPruner()
        for i in range(3):
            p.add_version("d1", f"v{i}", float(i))
        p.add_rule(PruneRule(rule_id="r1", pattern="d1", max_versions=1))
        p.prune("d1")
        kept = p.kept_versions_for("d1")
        assert [v.version_id for v in kept] == ["v2"]

    def test_sorted_desc(self):
        p = DocHistoryPruner()
        p.add_version("d1", "a", 1.0)
        p.add_version("d1", "b", 5.0)
        p.add_version("d1", "c", 3.0)
        ids = [v.version_id for v in p.kept_versions_for("d1")]
        assert ids == ["b", "c", "a"]

    def test_empty(self):
        p = DocHistoryPruner()
        assert p.kept_versions_for("nope") == []


# --------------------------------------------------------------------------- #
# all_doc_ids
# --------------------------------------------------------------------------- #


class TestAllDocIds:
    def test_empty(self):
        p = DocHistoryPruner()
        assert p.all_doc_ids() == []

    def test_sorted(self):
        p = DocHistoryPruner()
        p.add_version("zebra", "v1", 1.0)
        p.add_version("alpha", "v1", 1.0)
        p.add_version("beta", "v1", 1.0)
        assert p.all_doc_ids() == ["alpha", "beta", "zebra"]

    def test_no_duplicates(self):
        p = DocHistoryPruner()
        p.add_version("d1", "v1", 1.0)
        p.add_version("d1", "v2", 2.0)
        assert p.all_doc_ids() == ["d1"]


# --------------------------------------------------------------------------- #
# list_rules
# --------------------------------------------------------------------------- #


class TestListRules:
    def test_empty(self):
        p = DocHistoryPruner()
        assert p.list_rules() == []

    def test_sorted_by_priority_desc(self):
        p = DocHistoryPruner()
        p.add_rule(PruneRule(rule_id="a", pattern="*", priority=1))
        p.add_rule(PruneRule(rule_id="b", pattern="*", priority=10))
        p.add_rule(PruneRule(rule_id="c", pattern="*", priority=5))
        ids = [r.rule_id for r in p.list_rules()]
        assert ids == ["b", "c", "a"]

    def test_sorted_by_id_when_same_priority(self):
        p = DocHistoryPruner()
        p.add_rule(PruneRule(rule_id="zeta", pattern="*", priority=5))
        p.add_rule(PruneRule(rule_id="alpha", pattern="*", priority=5))
        ids = [r.rule_id for r in p.list_rules()]
        assert ids == ["alpha", "zeta"]


# --------------------------------------------------------------------------- #
# stats
# --------------------------------------------------------------------------- #


class TestStats:
    def test_totals(self):
        p = DocHistoryPruner()
        p.add_version("d1", "v1", 1.0)
        p.add_version("d1", "v2", 2.0)
        p.add_version("d2", "v1", 3.0)
        p.add_rule(PruneRule(rule_id="r1", pattern="*"))
        s = p.stats()
        assert s.total_versions == 3
        assert s.unique_docs == 2
        assert s.total_rules == 1

    def test_total_pruned_increases(self):
        p = DocHistoryPruner()
        for i in range(4):
            p.add_version("d1", f"v{i}", float(i))
        p.add_rule(PruneRule(rule_id="r1", pattern="d1", max_versions=1))
        p.prune("d1")
        assert p.stats().total_pruned == 3

    def test_total_pruned_stable_after_re_prune(self):
        p = DocHistoryPruner()
        for i in range(4):
            p.add_version("d1", f"v{i}", float(i))
        p.add_rule(PruneRule(rule_id="r1", pattern="d1", max_versions=1))
        p.prune("d1")
        p.prune("d1")  # nothing left to prune
        assert p.stats().total_pruned == 3


# --------------------------------------------------------------------------- #
# Thread safety
# --------------------------------------------------------------------------- #


class TestThreadSafety:
    def test_concurrent_add_version(self):
        p = DocHistoryPruner()

        def worker(start: int):
            for i in range(50):
                p.add_version(f"d{start}", f"v{i}", float(i))

        threads = [threading.Thread(target=worker, args=(t,)) for t in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        s = p.stats()
        assert s.unique_docs == 8
        assert s.total_versions == 8 * 50

    def test_concurrent_add_same_doc(self):
        p = DocHistoryPruner()

        def worker(start: int):
            for i in range(20):
                p.add_version("shared", f"t{start}-v{i}", float(i))

        threads = [threading.Thread(target=worker, args=(t,)) for t in range(6)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(p.versions_for("shared")) == 6 * 20
