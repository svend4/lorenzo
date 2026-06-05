"""Tests for E381 DocKeywordAlert module."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_keyword_alert import (
    AlertStats,
    DocKeywordAlert,
    KeywordMatch,
    KeywordRule,
)


# ---------------------------------------------------------------------------
# Dataclass tests
# ---------------------------------------------------------------------------


class TestKeywordRuleDataclass:
    def test_required_fields(self) -> None:
        r = KeywordRule(rule_id="r1", keyword="error")
        assert r.rule_id == "r1"
        assert r.keyword == "error"

    def test_default_case_sensitive(self) -> None:
        r = KeywordRule(rule_id="r1", keyword="x")
        assert r.case_sensitive is False

    def test_default_whole_word(self) -> None:
        r = KeywordRule(rule_id="r1", keyword="x")
        assert r.whole_word is False

    def test_default_severity(self) -> None:
        r = KeywordRule(rule_id="r1", keyword="x")
        assert r.severity == "info"

    def test_default_enabled(self) -> None:
        r = KeywordRule(rule_id="r1", keyword="x")
        assert r.enabled is True

    def test_custom_values(self) -> None:
        r = KeywordRule(
            rule_id="r1",
            keyword="X",
            case_sensitive=True,
            whole_word=True,
            severity="alert",
            enabled=False,
        )
        assert r.case_sensitive is True
        assert r.whole_word is True
        assert r.severity == "alert"
        assert r.enabled is False


class TestKeywordMatchDataclass:
    def test_required_fields(self) -> None:
        m = KeywordMatch(
            rule_id="r1",
            doc_id="d1",
            keyword="error",
            position=10,
            severity="warning",
        )
        assert m.rule_id == "r1"
        assert m.doc_id == "d1"
        assert m.keyword == "error"
        assert m.position == 10
        assert m.severity == "warning"

    def test_default_detected_at(self) -> None:
        m = KeywordMatch(
            rule_id="r1", doc_id="d1", keyword="x", position=0, severity="info"
        )
        assert m.detected_at == 0.0

    def test_detected_at_custom(self) -> None:
        m = KeywordMatch(
            rule_id="r1",
            doc_id="d1",
            keyword="x",
            position=0,
            severity="info",
            detected_at=123.45,
        )
        assert m.detected_at == 123.45


class TestAlertStatsDataclass:
    def test_required_fields(self) -> None:
        s = AlertStats(total_rules=1, enabled_rules=1, total_matches=0)
        assert s.total_rules == 1
        assert s.enabled_rules == 1
        assert s.total_matches == 0

    def test_default_matches_by_severity(self) -> None:
        s = AlertStats(total_rules=0, enabled_rules=0, total_matches=0)
        assert s.matches_by_severity == {}

    def test_custom_matches_by_severity(self) -> None:
        s = AlertStats(
            total_rules=2,
            enabled_rules=2,
            total_matches=3,
            matches_by_severity={"info": 2, "warning": 1},
        )
        assert s.matches_by_severity["info"] == 2
        assert s.matches_by_severity["warning"] == 1


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------


class TestConstruction:
    def test_create_empty(self) -> None:
        a = DocKeywordAlert()
        assert a.list_rules() == []

    def test_no_matches_initially(self) -> None:
        a = DocKeywordAlert()
        assert a.matches_for_doc("d1") == []

    def test_initial_stats(self) -> None:
        a = DocKeywordAlert()
        s = a.stats()
        assert s.total_rules == 0
        assert s.enabled_rules == 0
        assert s.total_matches == 0
        assert s.matches_by_severity == {}


# ---------------------------------------------------------------------------
# add_rule
# ---------------------------------------------------------------------------


class TestAddRule:
    def test_add_single(self) -> None:
        a = DocKeywordAlert()
        a.add_rule(KeywordRule(rule_id="r1", keyword="bug"))
        assert len(a.list_rules()) == 1

    def test_add_multiple(self) -> None:
        a = DocKeywordAlert()
        a.add_rule(KeywordRule(rule_id="r1", keyword="bug"))
        a.add_rule(KeywordRule(rule_id="r2", keyword="error"))
        assert len(a.list_rules()) == 2

    def test_overwrite_same_id(self) -> None:
        a = DocKeywordAlert()
        a.add_rule(KeywordRule(rule_id="r1", keyword="bug"))
        a.add_rule(KeywordRule(rule_id="r1", keyword="error"))
        rules = a.list_rules()
        assert len(rules) == 1
        assert rules[0].keyword == "error"


# ---------------------------------------------------------------------------
# remove_rule
# ---------------------------------------------------------------------------


class TestRemoveRule:
    def test_remove_existing(self) -> None:
        a = DocKeywordAlert()
        a.add_rule(KeywordRule(rule_id="r1", keyword="bug"))
        assert a.remove_rule("r1") is True
        assert a.list_rules() == []

    def test_remove_missing(self) -> None:
        a = DocKeywordAlert()
        assert a.remove_rule("nope") is False

    def test_remove_one_keeps_others(self) -> None:
        a = DocKeywordAlert()
        a.add_rule(KeywordRule(rule_id="r1", keyword="x"))
        a.add_rule(KeywordRule(rule_id="r2", keyword="y"))
        a.remove_rule("r1")
        rules = a.list_rules()
        assert len(rules) == 1
        assert rules[0].rule_id == "r2"


# ---------------------------------------------------------------------------
# enable / disable
# ---------------------------------------------------------------------------


class TestEnableDisable:
    def test_disable_existing(self) -> None:
        a = DocKeywordAlert()
        a.add_rule(KeywordRule(rule_id="r1", keyword="x"))
        assert a.disable_rule("r1") is True
        assert a.get_rule("r1").enabled is False

    def test_enable_existing(self) -> None:
        a = DocKeywordAlert()
        a.add_rule(KeywordRule(rule_id="r1", keyword="x", enabled=False))
        assert a.enable_rule("r1") is True
        assert a.get_rule("r1").enabled is True

    def test_disable_missing(self) -> None:
        a = DocKeywordAlert()
        assert a.disable_rule("nope") is False

    def test_enable_missing(self) -> None:
        a = DocKeywordAlert()
        assert a.enable_rule("nope") is False


# ---------------------------------------------------------------------------
# get_rule
# ---------------------------------------------------------------------------


class TestGetRule:
    def test_get_existing(self) -> None:
        a = DocKeywordAlert()
        a.add_rule(KeywordRule(rule_id="r1", keyword="bug"))
        rule = a.get_rule("r1")
        assert rule is not None
        assert rule.keyword == "bug"

    def test_get_missing_returns_none(self) -> None:
        a = DocKeywordAlert()
        assert a.get_rule("nope") is None


# ---------------------------------------------------------------------------
# list_rules
# ---------------------------------------------------------------------------


class TestListRules:
    def test_empty(self) -> None:
        a = DocKeywordAlert()
        assert a.list_rules() == []

    def test_sorted_by_id(self) -> None:
        a = DocKeywordAlert()
        a.add_rule(KeywordRule(rule_id="rb", keyword="x"))
        a.add_rule(KeywordRule(rule_id="ra", keyword="y"))
        a.add_rule(KeywordRule(rule_id="rc", keyword="z"))
        ids = [r.rule_id for r in a.list_rules()]
        assert ids == ["ra", "rb", "rc"]


# ---------------------------------------------------------------------------
# scan
# ---------------------------------------------------------------------------


class TestScan:
    def test_no_rules_no_matches(self) -> None:
        a = DocKeywordAlert()
        assert a.scan("d1", "some text with error") == []

    def test_finds_match(self) -> None:
        a = DocKeywordAlert()
        a.add_rule(KeywordRule(rule_id="r1", keyword="error"))
        ms = a.scan("d1", "this has an error in it")
        assert len(ms) == 1
        assert ms[0].keyword == "error"

    def test_position_correct(self) -> None:
        a = DocKeywordAlert()
        a.add_rule(KeywordRule(rule_id="r1", keyword="bug"))
        ms = a.scan("d1", "a bug here")
        assert ms[0].position == 2

    def test_multiple_occurrences(self) -> None:
        a = DocKeywordAlert()
        a.add_rule(KeywordRule(rule_id="r1", keyword="x"))
        ms = a.scan("d1", "x and x and x")
        assert len(ms) == 3
        assert [m.position for m in ms] == [0, 6, 12]

    def test_doc_id_in_match(self) -> None:
        a = DocKeywordAlert()
        a.add_rule(KeywordRule(rule_id="r1", keyword="x"))
        ms = a.scan("doc-42", "xx")
        for m in ms:
            assert m.doc_id == "doc-42"

    def test_severity_propagated(self) -> None:
        a = DocKeywordAlert()
        a.add_rule(KeywordRule(rule_id="r1", keyword="x", severity="alert"))
        ms = a.scan("d", "x")
        assert ms[0].severity == "alert"

    def test_now_param_used(self) -> None:
        a = DocKeywordAlert()
        a.add_rule(KeywordRule(rule_id="r1", keyword="x"))
        ms = a.scan("d", "x", now=1234.5)
        assert ms[0].detected_at == 1234.5

    def test_appended_to_global_list(self) -> None:
        a = DocKeywordAlert()
        a.add_rule(KeywordRule(rule_id="r1", keyword="x"))
        a.scan("d1", "x")
        a.scan("d2", "x x")
        assert a.stats().total_matches == 3


class TestScanCaseSensitive:
    def test_insensitive_default(self) -> None:
        a = DocKeywordAlert()
        a.add_rule(KeywordRule(rule_id="r1", keyword="Error"))
        ms = a.scan("d", "an error and ERROR and Error")
        assert len(ms) == 3

    def test_case_sensitive_only_exact(self) -> None:
        a = DocKeywordAlert()
        a.add_rule(
            KeywordRule(rule_id="r1", keyword="Error", case_sensitive=True)
        )
        ms = a.scan("d", "error Error ERROR")
        assert len(ms) == 1
        assert ms[0].position == 6


class TestScanWholeWord:
    def test_whole_word_only(self) -> None:
        a = DocKeywordAlert()
        a.add_rule(KeywordRule(rule_id="r1", keyword="cat", whole_word=True))
        ms = a.scan("d", "cat and category and cat-fish")
        # 'cat' (word) at 0, 'category' excluded, 'cat' in 'cat-fish' at 21
        positions = sorted(m.position for m in ms)
        assert 0 in positions
        assert 21 in positions
        # 'category' starts at 8 should NOT be a match
        assert 8 not in positions

    def test_without_whole_word_matches_substring(self) -> None:
        a = DocKeywordAlert()
        a.add_rule(KeywordRule(rule_id="r1", keyword="cat"))
        ms = a.scan("d", "category")
        assert len(ms) == 1
        assert ms[0].position == 0


class TestScanDisabled:
    def test_disabled_rule_skipped(self) -> None:
        a = DocKeywordAlert()
        a.add_rule(KeywordRule(rule_id="r1", keyword="x", enabled=False))
        ms = a.scan("d", "x x x")
        assert ms == []

    def test_enabled_rule_works_disabled_skipped(self) -> None:
        a = DocKeywordAlert()
        a.add_rule(KeywordRule(rule_id="r1", keyword="x"))
        a.add_rule(KeywordRule(rule_id="r2", keyword="y", enabled=False))
        ms = a.scan("d", "x y x y")
        kws = {m.keyword for m in ms}
        assert kws == {"x"}


# ---------------------------------------------------------------------------
# matches_for_doc
# ---------------------------------------------------------------------------


class TestMatchesForDoc:
    def test_empty(self) -> None:
        a = DocKeywordAlert()
        assert a.matches_for_doc("d") == []

    def test_filter_by_doc(self) -> None:
        a = DocKeywordAlert()
        a.add_rule(KeywordRule(rule_id="r1", keyword="x"))
        a.scan("d1", "x x", now=1.0)
        a.scan("d2", "x", now=2.0)
        assert len(a.matches_for_doc("d1")) == 2
        assert len(a.matches_for_doc("d2")) == 1

    def test_sorted_by_detected_at(self) -> None:
        a = DocKeywordAlert()
        a.add_rule(KeywordRule(rule_id="r1", keyword="x"))
        a.scan("d1", "x", now=5.0)
        a.scan("d1", "x", now=1.0)
        a.scan("d1", "x", now=3.0)
        ts = [m.detected_at for m in a.matches_for_doc("d1")]
        assert ts == sorted(ts)


# ---------------------------------------------------------------------------
# matches_for_rule
# ---------------------------------------------------------------------------


class TestMatchesForRule:
    def test_empty(self) -> None:
        a = DocKeywordAlert()
        assert a.matches_for_rule("r1") == []

    def test_filter_by_rule(self) -> None:
        a = DocKeywordAlert()
        a.add_rule(KeywordRule(rule_id="r1", keyword="x"))
        a.add_rule(KeywordRule(rule_id="r2", keyword="y"))
        a.scan("d", "x y x", now=1.0)
        assert len(a.matches_for_rule("r1")) == 2
        assert len(a.matches_for_rule("r2")) == 1

    def test_sorted_by_detected_at(self) -> None:
        a = DocKeywordAlert()
        a.add_rule(KeywordRule(rule_id="r1", keyword="x"))
        a.scan("d", "x", now=10.0)
        a.scan("d", "x", now=2.0)
        ts = [m.detected_at for m in a.matches_for_rule("r1")]
        assert ts == sorted(ts)


# ---------------------------------------------------------------------------
# matches_by_severity
# ---------------------------------------------------------------------------


class TestMatchesBySeverity:
    def test_empty(self) -> None:
        a = DocKeywordAlert()
        assert a.matches_by_severity("alert") == []

    def test_filter_by_severity(self) -> None:
        a = DocKeywordAlert()
        a.add_rule(KeywordRule(rule_id="r1", keyword="x", severity="alert"))
        a.add_rule(KeywordRule(rule_id="r2", keyword="y", severity="warning"))
        a.scan("d", "x y x", now=1.0)
        assert len(a.matches_by_severity("alert")) == 2
        assert len(a.matches_by_severity("warning")) == 1
        assert len(a.matches_by_severity("info")) == 0

    def test_sorted_by_detected_at(self) -> None:
        a = DocKeywordAlert()
        a.add_rule(KeywordRule(rule_id="r1", keyword="x", severity="info"))
        a.scan("d", "x", now=9.0)
        a.scan("d", "x", now=3.0)
        a.scan("d", "x", now=7.0)
        ts = [m.detected_at for m in a.matches_by_severity("info")]
        assert ts == sorted(ts)


# ---------------------------------------------------------------------------
# clear_matches / clear_rules
# ---------------------------------------------------------------------------


class TestClearMatches:
    def test_clear_empty(self) -> None:
        a = DocKeywordAlert()
        assert a.clear_matches() == 0

    def test_clear_returns_count(self) -> None:
        a = DocKeywordAlert()
        a.add_rule(KeywordRule(rule_id="r1", keyword="x"))
        a.scan("d", "x x x")
        assert a.clear_matches() == 3
        assert a.stats().total_matches == 0

    def test_clear_does_not_remove_rules(self) -> None:
        a = DocKeywordAlert()
        a.add_rule(KeywordRule(rule_id="r1", keyword="x"))
        a.scan("d", "x")
        a.clear_matches()
        assert len(a.list_rules()) == 1


class TestClearRules:
    def test_clear_empty(self) -> None:
        a = DocKeywordAlert()
        assert a.clear_rules() == 0

    def test_clear_returns_count(self) -> None:
        a = DocKeywordAlert()
        a.add_rule(KeywordRule(rule_id="r1", keyword="x"))
        a.add_rule(KeywordRule(rule_id="r2", keyword="y"))
        assert a.clear_rules() == 2
        assert a.list_rules() == []

    def test_clear_rules_does_not_clear_matches(self) -> None:
        a = DocKeywordAlert()
        a.add_rule(KeywordRule(rule_id="r1", keyword="x"))
        a.scan("d", "x")
        a.clear_rules()
        # matches remain
        assert a.stats().total_matches == 1


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------


class TestStats:
    def test_empty(self) -> None:
        s = DocKeywordAlert().stats()
        assert s.total_rules == 0
        assert s.enabled_rules == 0
        assert s.total_matches == 0
        assert s.matches_by_severity == {}

    def test_total_and_enabled(self) -> None:
        a = DocKeywordAlert()
        a.add_rule(KeywordRule(rule_id="r1", keyword="x"))
        a.add_rule(KeywordRule(rule_id="r2", keyword="y", enabled=False))
        s = a.stats()
        assert s.total_rules == 2
        assert s.enabled_rules == 1

    def test_severity_counts(self) -> None:
        a = DocKeywordAlert()
        a.add_rule(KeywordRule(rule_id="r1", keyword="x", severity="alert"))
        a.add_rule(KeywordRule(rule_id="r2", keyword="y", severity="info"))
        a.scan("d", "x x y")
        s = a.stats()
        assert s.matches_by_severity["alert"] == 2
        assert s.matches_by_severity["info"] == 1
        assert s.total_matches == 3

    def test_returns_alertstats_type(self) -> None:
        s = DocKeywordAlert().stats()
        assert isinstance(s, AlertStats)


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------


class TestThreadSafety:
    def test_concurrent_scans(self) -> None:
        a = DocKeywordAlert()
        a.add_rule(KeywordRule(rule_id="r1", keyword="x"))

        def worker(doc_id: str) -> None:
            for _ in range(20):
                a.scan(doc_id, "x x x x x")

        threads = [
            threading.Thread(target=worker, args=(f"d{i}",)) for i in range(8)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # 8 threads * 20 calls * 5 matches each = 800
        assert a.stats().total_matches == 800

    def test_concurrent_add_and_scan(self) -> None:
        a = DocKeywordAlert()

        def adder() -> None:
            for i in range(50):
                a.add_rule(KeywordRule(rule_id=f"r{i}", keyword=f"k{i}"))

        def scanner() -> None:
            for _ in range(50):
                a.scan("d", "k0 k1 k2 k3")

        threads = [
            threading.Thread(target=adder),
            threading.Thread(target=scanner),
            threading.Thread(target=adder),
            threading.Thread(target=scanner),
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Sanity: state remains consistent, no exceptions.
        assert isinstance(a.stats(), AlertStats)
        assert len(a.list_rules()) > 0


if __name__ == "__main__":  # pragma: no cover
    pytest.main([__file__, "-q"])
