"""Tests for E342 DocAlertManager."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_alert_manager import (
    AlertOccurrence,
    AlertRule,
    AlertStats,
    DocAlertManager,
)


# --------------------------------------------------------------- dataclasses


class TestAlertRuleDataclass:
    def test_minimum_fields(self):
        r = AlertRule(rule_id="r1", name="High errors")
        assert r.rule_id == "r1"
        assert r.name == "High errors"
        assert r.severity == "info"
        assert r.condition == ""
        assert r.cooldown_seconds == 0.0
        assert r.enabled is True

    def test_all_fields(self):
        r = AlertRule(
            rule_id="r2",
            name="Critical",
            severity="critical",
            condition="errors > 10",
            cooldown_seconds=30.0,
            enabled=False,
        )
        assert r.severity == "critical"
        assert r.condition == "errors > 10"
        assert r.cooldown_seconds == 30.0
        assert r.enabled is False

    def test_severity_values(self):
        for sev in ("info", "warning", "error", "critical"):
            r = AlertRule(rule_id=f"r-{sev}", name="x", severity=sev)
            assert r.severity == sev


class TestAlertOccurrenceDataclass:
    def test_defaults(self):
        o = AlertOccurrence(occurrence_id=1, rule_id="r1", doc_id="d1")
        assert o.occurrence_id == 1
        assert o.rule_id == "r1"
        assert o.doc_id == "d1"
        assert o.message == ""
        assert o.fired_at == 0.0
        assert o.acknowledged is False
        assert o.metadata == {}

    def test_custom_metadata(self):
        o = AlertOccurrence(
            occurrence_id=2,
            rule_id="r1",
            doc_id="d1",
            message="boom",
            fired_at=123.4,
            acknowledged=True,
            metadata={"k": "v"},
        )
        assert o.metadata == {"k": "v"}
        assert o.message == "boom"
        assert o.fired_at == 123.4
        assert o.acknowledged is True

    def test_metadata_independent_per_instance(self):
        a = AlertOccurrence(occurrence_id=1, rule_id="r", doc_id="d")
        b = AlertOccurrence(occurrence_id=2, rule_id="r", doc_id="d")
        a.metadata["x"] = 1
        assert "x" not in b.metadata


class TestAlertStatsDataclass:
    def test_fields(self):
        s = AlertStats(
            total_rules=3, enabled_rules=2, total_occurrences=10, unacknowledged_count=4
        )
        assert s.total_rules == 3
        assert s.enabled_rules == 2
        assert s.total_occurrences == 10
        assert s.unacknowledged_count == 4


# --------------------------------------------------------------- construction


class TestConstruction:
    def test_construct_empty(self):
        m = DocAlertManager()
        assert m.list_rules() == []

    def test_initial_stats(self):
        m = DocAlertManager()
        s = m.stats()
        assert s.total_rules == 0
        assert s.enabled_rules == 0
        assert s.total_occurrences == 0
        assert s.unacknowledged_count == 0

    def test_initial_next_id_is_one(self):
        m = DocAlertManager()
        m.define_rule(AlertRule(rule_id="r1", name="n"))
        occ = m.fire("r1", "d1")
        assert occ is not None
        assert occ.occurrence_id == 1


# ------------------------------------------------------------- define_rule


class TestDefineRule:
    def test_define_new(self):
        m = DocAlertManager()
        m.define_rule(AlertRule(rule_id="r1", name="N"))
        assert m.get_rule("r1") is not None

    def test_define_replaces_existing(self):
        m = DocAlertManager()
        m.define_rule(AlertRule(rule_id="r1", name="Old"))
        m.define_rule(AlertRule(rule_id="r1", name="New", severity="error"))
        r = m.get_rule("r1")
        assert r.name == "New"
        assert r.severity == "error"

    def test_define_multiple(self):
        m = DocAlertManager()
        for i in range(5):
            m.define_rule(AlertRule(rule_id=f"r{i}", name=f"n{i}"))
        assert len(m.list_rules()) == 5


# ----------------------------------------------------------- undefine_rule


class TestUndefineRule:
    def test_undefine_existing(self):
        m = DocAlertManager()
        m.define_rule(AlertRule(rule_id="r1", name="n"))
        assert m.undefine_rule("r1") is True
        assert m.get_rule("r1") is None

    def test_undefine_unknown(self):
        m = DocAlertManager()
        assert m.undefine_rule("nope") is False

    def test_undefine_keeps_occurrences(self):
        m = DocAlertManager()
        m.define_rule(AlertRule(rule_id="r1", name="n"))
        m.fire("r1", "d1")
        m.undefine_rule("r1")
        assert len(m.occurrences_for_rule("r1")) == 1


# ----------------------------------------------------------- enable/disable


class TestEnableDisable:
    def test_disable_then_enable(self):
        m = DocAlertManager()
        m.define_rule(AlertRule(rule_id="r1", name="n"))
        assert m.disable_rule("r1") is True
        assert m.get_rule("r1").enabled is False
        assert m.enable_rule("r1") is True
        assert m.get_rule("r1").enabled is True

    def test_enable_unknown(self):
        m = DocAlertManager()
        assert m.enable_rule("nope") is False

    def test_disable_unknown(self):
        m = DocAlertManager()
        assert m.disable_rule("nope") is False

    def test_disabled_rule_does_not_fire(self):
        m = DocAlertManager()
        m.define_rule(AlertRule(rule_id="r1", name="n"))
        m.disable_rule("r1")
        assert m.fire("r1", "d1") is None


# --------------------------------------------------------------- get_rule


class TestGetRule:
    def test_found(self):
        m = DocAlertManager()
        m.define_rule(AlertRule(rule_id="r1", name="n"))
        assert m.get_rule("r1") is not None

    def test_not_found(self):
        m = DocAlertManager()
        assert m.get_rule("nope") is None


# --------------------------------------------------------------- list_rules


class TestListRules:
    def test_empty(self):
        m = DocAlertManager()
        assert m.list_rules() == []

    def test_sorted_by_id(self):
        m = DocAlertManager()
        for rid in ("c", "a", "b"):
            m.define_rule(AlertRule(rule_id=rid, name=rid))
        ids = [r.rule_id for r in m.list_rules()]
        assert ids == ["a", "b", "c"]


# --------------------------------------------------------------- fire


class TestFire:
    def test_fire_creates_occurrence(self):
        m = DocAlertManager()
        m.define_rule(AlertRule(rule_id="r1", name="n"))
        occ = m.fire("r1", "d1", message="hi")
        assert occ is not None
        assert occ.rule_id == "r1"
        assert occ.doc_id == "d1"
        assert occ.message == "hi"

    def test_fire_increments_id(self):
        m = DocAlertManager()
        m.define_rule(AlertRule(rule_id="r1", name="n"))
        a = m.fire("r1", "d1")
        b = m.fire("r1", "d2")
        c = m.fire("r1", "d3")
        assert a.occurrence_id == 1
        assert b.occurrence_id == 2
        assert c.occurrence_id == 3

    def test_fire_unknown_rule_returns_none(self):
        m = DocAlertManager()
        assert m.fire("nope", "d1") is None

    def test_fire_disabled_returns_none(self):
        m = DocAlertManager()
        m.define_rule(AlertRule(rule_id="r1", name="n", enabled=False))
        assert m.fire("r1", "d1") is None

    def test_fire_passes_metadata(self):
        m = DocAlertManager()
        m.define_rule(AlertRule(rule_id="r1", name="n"))
        occ = m.fire("r1", "d1", metadata={"x": 1})
        assert occ.metadata == {"x": 1}

    def test_fire_metadata_is_copied(self):
        m = DocAlertManager()
        m.define_rule(AlertRule(rule_id="r1", name="n"))
        md = {"x": 1}
        occ = m.fire("r1", "d1", metadata=md)
        md["y"] = 2
        assert occ.metadata == {"x": 1}

    def test_fire_uses_now_param(self):
        m = DocAlertManager()
        m.define_rule(AlertRule(rule_id="r1", name="n"))
        occ = m.fire("r1", "d1", now=1000.0)
        assert occ.fired_at == 1000.0


# --------------------------------------------------------------- cooldown


class TestCooldown:
    def test_second_fire_within_window_returns_none(self):
        m = DocAlertManager()
        m.define_rule(AlertRule(rule_id="r1", name="n", cooldown_seconds=10.0))
        a = m.fire("r1", "d1", now=100.0)
        b = m.fire("r1", "d1", now=105.0)
        assert a is not None
        assert b is None

    def test_fire_after_cooldown_succeeds(self):
        m = DocAlertManager()
        m.define_rule(AlertRule(rule_id="r1", name="n", cooldown_seconds=10.0))
        m.fire("r1", "d1", now=100.0)
        c = m.fire("r1", "d1", now=111.0)
        assert c is not None

    def test_cooldown_per_doc(self):
        m = DocAlertManager()
        m.define_rule(AlertRule(rule_id="r1", name="n", cooldown_seconds=10.0))
        a = m.fire("r1", "d1", now=100.0)
        b = m.fire("r1", "d2", now=101.0)
        assert a is not None
        assert b is not None

    def test_no_cooldown_when_zero(self):
        m = DocAlertManager()
        m.define_rule(AlertRule(rule_id="r1", name="n", cooldown_seconds=0.0))
        a = m.fire("r1", "d1", now=100.0)
        b = m.fire("r1", "d1", now=100.0)
        assert a is not None
        assert b is not None


# --------------------------------------------------------------- acknowledge


class TestAcknowledge:
    def test_acknowledge_existing(self):
        m = DocAlertManager()
        m.define_rule(AlertRule(rule_id="r1", name="n"))
        occ = m.fire("r1", "d1")
        assert m.acknowledge(occ.occurrence_id) is True
        assert occ.acknowledged is True

    def test_acknowledge_unknown(self):
        m = DocAlertManager()
        assert m.acknowledge(999) is False

    def test_acknowledge_idempotent(self):
        m = DocAlertManager()
        m.define_rule(AlertRule(rule_id="r1", name="n"))
        occ = m.fire("r1", "d1")
        m.acknowledge(occ.occurrence_id)
        assert m.acknowledge(occ.occurrence_id) is True


class TestAcknowledgeAllForDoc:
    def test_count_only_unack(self):
        m = DocAlertManager()
        m.define_rule(AlertRule(rule_id="r1", name="n"))
        m.fire("r1", "d1", now=1.0)
        m.fire("r1", "d1", now=2.0)
        m.fire("r1", "d2", now=3.0)
        count = m.acknowledge_all_for_doc("d1")
        assert count == 2

    def test_no_match(self):
        m = DocAlertManager()
        assert m.acknowledge_all_for_doc("missing") == 0

    def test_skips_already_acked(self):
        m = DocAlertManager()
        m.define_rule(AlertRule(rule_id="r1", name="n"))
        o1 = m.fire("r1", "d1", now=1.0)
        m.acknowledge(o1.occurrence_id)
        m.fire("r1", "d1", now=2.0)
        count = m.acknowledge_all_for_doc("d1")
        assert count == 1


# --------------------------------------------------------------- queries


class TestOccurrencesForDoc:
    def test_sorted_desc(self):
        m = DocAlertManager()
        m.define_rule(AlertRule(rule_id="r1", name="n"))
        m.fire("r1", "d1", now=1.0)
        m.fire("r1", "d1", now=3.0)
        m.fire("r1", "d1", now=2.0)
        out = m.occurrences_for_doc("d1")
        assert [o.fired_at for o in out] == [3.0, 2.0, 1.0]

    def test_filters_doc(self):
        m = DocAlertManager()
        m.define_rule(AlertRule(rule_id="r1", name="n"))
        m.fire("r1", "d1", now=1.0)
        m.fire("r1", "d2", now=2.0)
        out = m.occurrences_for_doc("d1")
        assert len(out) == 1
        assert out[0].doc_id == "d1"

    def test_unack_filter(self):
        m = DocAlertManager()
        m.define_rule(AlertRule(rule_id="r1", name="n"))
        o1 = m.fire("r1", "d1", now=1.0)
        m.fire("r1", "d1", now=2.0)
        m.acknowledge(o1.occurrence_id)
        out = m.occurrences_for_doc("d1", unacknowledged_only=True)
        assert len(out) == 1
        assert out[0].acknowledged is False


class TestOccurrencesForRule:
    def test_sorted_desc(self):
        m = DocAlertManager()
        m.define_rule(AlertRule(rule_id="r1", name="n"))
        m.fire("r1", "d1", now=1.0)
        m.fire("r1", "d2", now=5.0)
        m.fire("r1", "d3", now=3.0)
        out = m.occurrences_for_rule("r1")
        assert [o.fired_at for o in out] == [5.0, 3.0, 1.0]

    def test_filters_rule(self):
        m = DocAlertManager()
        m.define_rule(AlertRule(rule_id="r1", name="n"))
        m.define_rule(AlertRule(rule_id="r2", name="n2"))
        m.fire("r1", "d1", now=1.0)
        m.fire("r2", "d1", now=2.0)
        out = m.occurrences_for_rule("r1")
        assert len(out) == 1
        assert out[0].rule_id == "r1"

    def test_unack_filter(self):
        m = DocAlertManager()
        m.define_rule(AlertRule(rule_id="r1", name="n"))
        o1 = m.fire("r1", "d1", now=1.0)
        m.fire("r1", "d2", now=2.0)
        m.acknowledge(o1.occurrence_id)
        out = m.occurrences_for_rule("r1", unacknowledged_only=True)
        assert len(out) == 1


class TestOccurrencesBySeverity:
    def test_filter_by_severity(self):
        m = DocAlertManager()
        m.define_rule(AlertRule(rule_id="r1", name="n", severity="info"))
        m.define_rule(AlertRule(rule_id="r2", name="n", severity="error"))
        m.fire("r1", "d1", now=1.0)
        m.fire("r2", "d1", now=2.0)
        m.fire("r2", "d2", now=3.0)
        out = m.occurrences_by_severity("error")
        assert len(out) == 2
        assert all(o.rule_id == "r2" for o in out)

    def test_sorted_desc(self):
        m = DocAlertManager()
        m.define_rule(AlertRule(rule_id="r1", name="n", severity="critical"))
        m.fire("r1", "d1", now=1.0)
        m.fire("r1", "d2", now=10.0)
        m.fire("r1", "d3", now=5.0)
        out = m.occurrences_by_severity("critical")
        assert [o.fired_at for o in out] == [10.0, 5.0, 1.0]

    def test_no_match(self):
        m = DocAlertManager()
        m.define_rule(AlertRule(rule_id="r1", name="n", severity="info"))
        m.fire("r1", "d1")
        assert m.occurrences_by_severity("critical") == []

    def test_skips_unknown_rule(self):
        m = DocAlertManager()
        m.define_rule(AlertRule(rule_id="r1", name="n", severity="info"))
        m.fire("r1", "d1", now=1.0)
        m.undefine_rule("r1")
        # rule removed; severity lookup yields nothing
        assert m.occurrences_by_severity("info") == []


# --------------------------------------------------------------- clear/stats


class TestClearOccurrences:
    def test_clear_returns_count(self):
        m = DocAlertManager()
        m.define_rule(AlertRule(rule_id="r1", name="n"))
        m.fire("r1", "d1")
        m.fire("r1", "d2")
        assert m.clear_occurrences() == 2
        assert m.stats().total_occurrences == 0

    def test_clear_empty(self):
        m = DocAlertManager()
        assert m.clear_occurrences() == 0


class TestStats:
    def test_totals(self):
        m = DocAlertManager()
        m.define_rule(AlertRule(rule_id="r1", name="n"))
        m.define_rule(AlertRule(rule_id="r2", name="n", enabled=False))
        o1 = m.fire("r1", "d1")
        m.fire("r1", "d2")
        m.acknowledge(o1.occurrence_id)
        s = m.stats()
        assert s.total_rules == 2
        assert s.enabled_rules == 1
        assert s.total_occurrences == 2
        assert s.unacknowledged_count == 1

    def test_stats_empty(self):
        m = DocAlertManager()
        s = m.stats()
        assert s == AlertStats(0, 0, 0, 0)


# --------------------------------------------------------------- threading


class TestThreadSafety:
    def test_concurrent_fire_calls(self):
        m = DocAlertManager()
        m.define_rule(AlertRule(rule_id="r1", name="n"))

        N_THREADS = 10
        N_PER = 50

        def worker(tid):
            for i in range(N_PER):
                m.fire("r1", f"doc-{tid}-{i}")

        threads = [threading.Thread(target=worker, args=(t,)) for t in range(N_THREADS)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        total = N_THREADS * N_PER
        s = m.stats()
        assert s.total_occurrences == total

        # ids unique and contiguous
        ids = sorted(o.occurrence_id for o in m.occurrences_for_rule("r1"))
        assert ids == list(range(1, total + 1))

    def test_concurrent_define_and_fire(self):
        m = DocAlertManager()

        def define_worker():
            for i in range(20):
                m.define_rule(AlertRule(rule_id=f"r{i}", name="n"))

        def fire_worker():
            for i in range(20):
                m.fire(f"r{i % 5}", f"d{i}")

        t1 = threading.Thread(target=define_worker)
        t2 = threading.Thread(target=fire_worker)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        # should not raise; state coherent
        assert m.stats().total_rules == 20
