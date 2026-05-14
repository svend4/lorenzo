"""Tests for E420 DocHealthMonitor."""
from __future__ import annotations

import threading
import time

import pytest

from docstoolkit.doc_health_monitor import (
    DocHealthMonitor,
    HealthCheck,
    HealthResult,
    MonitorStats,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def always_healthy(doc_id, content):
    return True


def always_unhealthy(doc_id, content):
    return False


def has_title(doc_id, content):
    return content.startswith("# ")


def long_enough(doc_id, content):
    return len(content) >= 10


def raises(doc_id, content):
    raise RuntimeError("boom")


# ---------------------------------------------------------------------------
# Public API surface
# ---------------------------------------------------------------------------

def test_public_exports():
    from docstoolkit import doc_health_monitor as mod

    assert set(mod.__all__) == {
        "HealthCheck",
        "HealthResult",
        "MonitorStats",
        "DocHealthMonitor",
    }


def test_health_check_dataclass_defaults():
    hc = HealthCheck(check_id="c1", name="Check 1")
    assert hc.check_id == "c1"
    assert hc.name == "Check 1"
    assert hc.severity == "info"
    assert hc.enabled is True
    assert hc.check is None


def test_health_check_custom_fields():
    hc = HealthCheck(
        check_id="c", name="n", severity="critical", enabled=False, check=always_healthy
    )
    assert hc.severity == "critical"
    assert hc.enabled is False
    assert hc.check is always_healthy


def test_health_result_defaults():
    r = HealthResult(doc_id="d", check_id="c", healthy=True, severity="info")
    assert r.checked_at == 0.0
    assert r.message == ""


def test_monitor_stats_dataclass():
    s = MonitorStats(
        total_checks=1, enabled_checks=1, total_evaluations=2, unhealthy_count=0
    )
    assert s.total_checks == 1
    assert s.unhealthy_count == 0


# ---------------------------------------------------------------------------
# register / unregister / enable / disable
# ---------------------------------------------------------------------------

def test_register_single_check():
    m = DocHealthMonitor()
    m.register_check(HealthCheck("c1", "Check 1", check=always_healthy))
    assert m.get_check("c1") is not None


def test_register_check_replaces_existing():
    m = DocHealthMonitor()
    m.register_check(HealthCheck("c1", "First"))
    m.register_check(HealthCheck("c1", "Second"))
    c = m.get_check("c1")
    assert c.name == "Second"


def test_register_rejects_non_healthcheck():
    m = DocHealthMonitor()
    with pytest.raises(TypeError):
        m.register_check("not a check")  # type: ignore[arg-type]


def test_register_rejects_empty_id():
    m = DocHealthMonitor()
    with pytest.raises(ValueError):
        m.register_check(HealthCheck("", "name"))


def test_register_rejects_bad_severity():
    m = DocHealthMonitor()
    with pytest.raises(ValueError):
        m.register_check(HealthCheck("c", "n", severity="urgent"))


def test_register_accepts_all_valid_severities():
    m = DocHealthMonitor()
    for sev in ("info", "warning", "critical"):
        m.register_check(HealthCheck(f"c-{sev}", "n", severity=sev))
    assert len(m.list_checks()) == 3


def test_unregister_existing_check():
    m = DocHealthMonitor()
    m.register_check(HealthCheck("c1", "n"))
    assert m.unregister_check("c1") is True
    assert m.get_check("c1") is None


def test_unregister_missing_check_returns_false():
    m = DocHealthMonitor()
    assert m.unregister_check("nope") is False


def test_unregister_removes_related_results():
    m = DocHealthMonitor()
    m.register_check(HealthCheck("c1", "n1", check=always_healthy))
    m.register_check(HealthCheck("c2", "n2", check=always_healthy))
    m.evaluate("d1", "x")
    assert len(m.results_for_doc("d1")) == 2
    m.unregister_check("c1")
    res = m.results_for_doc("d1")
    assert len(res) == 1
    assert res[0].check_id == "c2"


def test_enable_check_true_when_present():
    m = DocHealthMonitor()
    m.register_check(HealthCheck("c1", "n", enabled=False))
    assert m.enable_check("c1") is True
    assert m.get_check("c1").enabled is True


def test_enable_check_false_when_missing():
    m = DocHealthMonitor()
    assert m.enable_check("nope") is False


def test_disable_check_true_when_present():
    m = DocHealthMonitor()
    m.register_check(HealthCheck("c1", "n"))
    assert m.disable_check("c1") is True
    assert m.get_check("c1").enabled is False


def test_disable_check_false_when_missing():
    m = DocHealthMonitor()
    assert m.disable_check("nope") is False


def test_get_check_returns_none_when_missing():
    m = DocHealthMonitor()
    assert m.get_check("nope") is None


def test_list_checks_sorted_by_id():
    m = DocHealthMonitor()
    m.register_check(HealthCheck("zeta", "z"))
    m.register_check(HealthCheck("alpha", "a"))
    m.register_check(HealthCheck("mu", "m"))
    ids = [c.check_id for c in m.list_checks()]
    assert ids == ["alpha", "mu", "zeta"]


def test_list_checks_empty():
    m = DocHealthMonitor()
    assert m.list_checks() == []


# ---------------------------------------------------------------------------
# evaluate
# ---------------------------------------------------------------------------

def test_evaluate_runs_all_enabled_checks():
    m = DocHealthMonitor()
    m.register_check(HealthCheck("c1", "n1", check=always_healthy))
    m.register_check(HealthCheck("c2", "n2", check=always_healthy))
    results = m.evaluate("d1", "content")
    assert len(results) == 2
    assert all(r.healthy for r in results)


def test_evaluate_skips_disabled_checks():
    m = DocHealthMonitor()
    m.register_check(HealthCheck("c1", "n1", check=always_healthy))
    m.register_check(HealthCheck("c2", "n2", check=always_healthy, enabled=False))
    results = m.evaluate("d", "x")
    assert len(results) == 1
    assert results[0].check_id == "c1"


def test_evaluate_filter_by_check_ids():
    m = DocHealthMonitor()
    m.register_check(HealthCheck("c1", "n1", check=always_healthy))
    m.register_check(HealthCheck("c2", "n2", check=always_healthy))
    m.register_check(HealthCheck("c3", "n3", check=always_healthy))
    results = m.evaluate("d", "x", check_ids=["c1", "c3"])
    ids = {r.check_id for r in results}
    assert ids == {"c1", "c3"}


def test_evaluate_filter_ignores_unknown_ids():
    m = DocHealthMonitor()
    m.register_check(HealthCheck("c1", "n1", check=always_healthy))
    results = m.evaluate("d", "x", check_ids=["c1", "missing"])
    assert len(results) == 1


def test_evaluate_with_explicit_now_sets_timestamp():
    m = DocHealthMonitor()
    m.register_check(HealthCheck("c1", "n", check=always_healthy))
    results = m.evaluate("d", "x", now=12345.0)
    assert results[0].checked_at == 12345.0


def test_evaluate_default_now_uses_time_time():
    m = DocHealthMonitor()
    m.register_check(HealthCheck("c1", "n", check=always_healthy))
    before = time.time()
    results = m.evaluate("d", "x")
    after = time.time()
    assert before <= results[0].checked_at <= after


def test_evaluate_records_unhealthy_when_callback_returns_false():
    m = DocHealthMonitor()
    m.register_check(HealthCheck("c1", "n", check=always_unhealthy))
    results = m.evaluate("d", "x")
    assert results[0].healthy is False


def test_evaluate_handles_callback_exception():
    m = DocHealthMonitor()
    m.register_check(HealthCheck("c1", "n", check=raises))
    results = m.evaluate("d", "x")
    assert len(results) == 1
    assert results[0].healthy is False
    assert "RuntimeError" in results[0].message
    assert "boom" in results[0].message


def test_evaluate_check_with_none_callback_is_healthy():
    m = DocHealthMonitor()
    m.register_check(HealthCheck("c1", "n", check=None))
    results = m.evaluate("d", "x")
    assert results[0].healthy is True


def test_evaluate_results_ordered_by_check_id():
    m = DocHealthMonitor()
    m.register_check(HealthCheck("zeta", "z", check=always_healthy))
    m.register_check(HealthCheck("alpha", "a", check=always_healthy))
    results = m.evaluate("d", "x")
    assert [r.check_id for r in results] == ["alpha", "zeta"]


def test_evaluate_with_actual_content_logic():
    m = DocHealthMonitor()
    m.register_check(HealthCheck("title", "t", check=has_title))
    m.register_check(HealthCheck("length", "l", check=long_enough))
    results = m.evaluate("d", "# Hello world!")
    assert all(r.healthy for r in results)


def test_evaluate_mixed_pass_fail():
    m = DocHealthMonitor()
    m.register_check(HealthCheck("title", "t", check=has_title))
    m.register_check(HealthCheck("length", "l", check=long_enough))
    results = m.evaluate("d", "short")
    by_id = {r.check_id: r.healthy for r in results}
    assert by_id["title"] is False
    assert by_id["length"] is False


def test_evaluate_persists_results():
    m = DocHealthMonitor()
    m.register_check(HealthCheck("c1", "n", check=always_healthy))
    m.evaluate("d", "x")
    r = m.latest_result("d", "c1")
    assert r is not None
    assert r.healthy is True


def test_evaluate_overwrites_previous_result():
    m = DocHealthMonitor()
    flips = [True, False]

    def flip(_doc, _content):
        return flips.pop(0)

    m.register_check(HealthCheck("c1", "n", check=flip))
    m.evaluate("d", "x")
    m.evaluate("d", "x")
    r = m.latest_result("d", "c1")
    assert r.healthy is False


def test_evaluate_uses_check_severity():
    m = DocHealthMonitor()
    m.register_check(HealthCheck("c1", "n", severity="critical", check=always_unhealthy))
    results = m.evaluate("d", "x")
    assert results[0].severity == "critical"


def test_evaluate_no_checks_returns_empty():
    m = DocHealthMonitor()
    assert m.evaluate("d", "x") == []


def test_evaluate_increments_total_evaluations():
    m = DocHealthMonitor()
    m.register_check(HealthCheck("c1", "n", check=always_healthy))
    m.register_check(HealthCheck("c2", "n", check=always_healthy))
    m.evaluate("d", "x")
    assert m.stats().total_evaluations == 2
    m.evaluate("d", "x")
    assert m.stats().total_evaluations == 4


def test_evaluate_passes_doc_id_to_callback():
    seen = []

    def spy(doc_id, content):
        seen.append((doc_id, content))
        return True

    m = DocHealthMonitor()
    m.register_check(HealthCheck("c1", "n", check=spy))
    m.evaluate("doc-42", "payload")
    assert seen == [("doc-42", "payload")]


# ---------------------------------------------------------------------------
# Result access
# ---------------------------------------------------------------------------

def test_latest_result_missing_returns_none():
    m = DocHealthMonitor()
    assert m.latest_result("d", "c") is None


def test_latest_result_returns_stored():
    m = DocHealthMonitor()
    m.register_check(HealthCheck("c1", "n", check=always_healthy))
    m.evaluate("d1", "x")
    r = m.latest_result("d1", "c1")
    assert r is not None and r.doc_id == "d1"


def test_results_for_doc_empty():
    m = DocHealthMonitor()
    assert m.results_for_doc("nope") == []


def test_results_for_doc_sorted():
    m = DocHealthMonitor()
    m.register_check(HealthCheck("zeta", "z", check=always_healthy))
    m.register_check(HealthCheck("alpha", "a", check=always_healthy))
    m.evaluate("d", "x")
    res = m.results_for_doc("d")
    assert [r.check_id for r in res] == ["alpha", "zeta"]


def test_results_for_doc_isolated_by_doc():
    m = DocHealthMonitor()
    m.register_check(HealthCheck("c1", "n", check=always_healthy))
    m.evaluate("d1", "x")
    m.evaluate("d2", "y")
    assert len(m.results_for_doc("d1")) == 1
    assert len(m.results_for_doc("d2")) == 1


# ---------------------------------------------------------------------------
# unhealthy_docs
# ---------------------------------------------------------------------------

def test_unhealthy_docs_empty():
    m = DocHealthMonitor()
    assert m.unhealthy_docs() == []


def test_unhealthy_docs_lists_failing_docs():
    m = DocHealthMonitor()
    m.register_check(HealthCheck("c1", "n", check=always_unhealthy))
    m.evaluate("d1", "x")
    m.evaluate("d2", "x")
    assert m.unhealthy_docs() == ["d1", "d2"]


def test_unhealthy_docs_excludes_healthy_docs():
    m = DocHealthMonitor()

    def passes_for_d2(doc_id, content):
        return doc_id == "d2"

    m.register_check(HealthCheck("c1", "n", check=passes_for_d2))
    m.evaluate("d1", "x")
    m.evaluate("d2", "x")
    assert m.unhealthy_docs() == ["d1"]


def test_unhealthy_docs_sorted_alphabetically():
    m = DocHealthMonitor()
    m.register_check(HealthCheck("c1", "n", check=always_unhealthy))
    for doc in ["delta", "alpha", "charlie", "bravo"]:
        m.evaluate(doc, "x")
    assert m.unhealthy_docs() == ["alpha", "bravo", "charlie", "delta"]


def test_unhealthy_docs_filter_by_severity():
    m = DocHealthMonitor()
    m.register_check(
        HealthCheck("c1", "n", severity="critical", check=always_unhealthy)
    )
    m.register_check(
        HealthCheck("c2", "n", severity="warning", check=always_unhealthy)
    )
    m.evaluate("d1", "x", check_ids=["c1"])
    m.evaluate("d2", "x", check_ids=["c2"])
    assert m.unhealthy_docs(severity="critical") == ["d1"]
    assert m.unhealthy_docs(severity="warning") == ["d2"]
    assert m.unhealthy_docs(severity="info") == []


def test_unhealthy_docs_rejects_bad_severity():
    m = DocHealthMonitor()
    with pytest.raises(ValueError):
        m.unhealthy_docs(severity="urgent")


def test_unhealthy_docs_unique_doc_ids():
    m = DocHealthMonitor()
    m.register_check(HealthCheck("c1", "n", check=always_unhealthy))
    m.register_check(HealthCheck("c2", "n", check=always_unhealthy))
    m.evaluate("d1", "x")
    assert m.unhealthy_docs() == ["d1"]


# ---------------------------------------------------------------------------
# health_score
# ---------------------------------------------------------------------------

def test_health_score_no_results_returns_one():
    m = DocHealthMonitor()
    assert m.health_score("d") == 1.0


def test_health_score_all_healthy():
    m = DocHealthMonitor()
    m.register_check(HealthCheck("c1", "n", check=always_healthy))
    m.register_check(HealthCheck("c2", "n", check=always_healthy))
    m.evaluate("d", "x")
    assert m.health_score("d") == 1.0


def test_health_score_all_unhealthy():
    m = DocHealthMonitor()
    m.register_check(HealthCheck("c1", "n", check=always_unhealthy))
    m.evaluate("d", "x")
    assert m.health_score("d") == 0.0


def test_health_score_partial():
    m = DocHealthMonitor()
    m.register_check(HealthCheck("c1", "n", check=always_healthy))
    m.register_check(HealthCheck("c2", "n", check=always_unhealthy))
    m.register_check(HealthCheck("c3", "n", check=always_unhealthy))
    m.evaluate("d", "x")
    assert m.health_score("d") == pytest.approx(1 / 3)


def test_health_score_isolated_per_doc():
    m = DocHealthMonitor()
    m.register_check(HealthCheck("c1", "n", check=always_healthy))
    m.register_check(HealthCheck("c2", "n", check=always_unhealthy))
    m.evaluate("d1", "x")
    m.evaluate("d2", "x", check_ids=["c1"])
    assert m.health_score("d1") == 0.5
    assert m.health_score("d2") == 1.0


# ---------------------------------------------------------------------------
# clear_results
# ---------------------------------------------------------------------------

def test_clear_results_returns_count():
    m = DocHealthMonitor()
    m.register_check(HealthCheck("c1", "n", check=always_healthy))
    m.register_check(HealthCheck("c2", "n", check=always_healthy))
    m.evaluate("d1", "x")
    m.evaluate("d2", "x")
    assert m.clear_results() == 4


def test_clear_results_when_empty():
    m = DocHealthMonitor()
    assert m.clear_results() == 0


def test_clear_results_drops_stored():
    m = DocHealthMonitor()
    m.register_check(HealthCheck("c1", "n", check=always_healthy))
    m.evaluate("d", "x")
    m.clear_results()
    assert m.results_for_doc("d") == []


def test_clear_results_keeps_checks_registered():
    m = DocHealthMonitor()
    m.register_check(HealthCheck("c1", "n", check=always_healthy))
    m.evaluate("d", "x")
    m.clear_results()
    assert m.get_check("c1") is not None


def test_clear_results_preserves_total_evaluations():
    m = DocHealthMonitor()
    m.register_check(HealthCheck("c1", "n", check=always_healthy))
    m.evaluate("d", "x")
    m.clear_results()
    assert m.stats().total_evaluations == 1


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------

def test_stats_initial():
    m = DocHealthMonitor()
    s = m.stats()
    assert s == MonitorStats(0, 0, 0, 0)


def test_stats_counts_checks():
    m = DocHealthMonitor()
    m.register_check(HealthCheck("c1", "n"))
    m.register_check(HealthCheck("c2", "n", enabled=False))
    s = m.stats()
    assert s.total_checks == 2
    assert s.enabled_checks == 1


def test_stats_counts_unhealthy():
    m = DocHealthMonitor()
    m.register_check(HealthCheck("c1", "n", check=always_unhealthy))
    m.register_check(HealthCheck("c2", "n", check=always_healthy))
    m.evaluate("d", "x")
    s = m.stats()
    assert s.unhealthy_count == 1


def test_stats_tracks_total_evaluations_across_calls():
    m = DocHealthMonitor()
    m.register_check(HealthCheck("c1", "n", check=always_healthy))
    m.evaluate("d", "x")
    m.evaluate("d", "x")
    m.evaluate("e", "x")
    assert m.stats().total_evaluations == 3


def test_stats_returns_monitor_stats_instance():
    m = DocHealthMonitor()
    assert isinstance(m.stats(), MonitorStats)


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------

def test_thread_safety_register_concurrent():
    m = DocHealthMonitor()
    N = 100

    def worker(idx):
        m.register_check(HealthCheck(f"c{idx}", f"n{idx}", check=always_healthy))

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(N)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert len(m.list_checks()) == N


def test_thread_safety_evaluate_concurrent():
    m = DocHealthMonitor()
    m.register_check(HealthCheck("c1", "n", check=always_healthy))
    m.register_check(HealthCheck("c2", "n", check=always_unhealthy))

    def worker(idx):
        m.evaluate(f"doc-{idx}", "content")

    N = 50
    threads = [threading.Thread(target=worker, args=(i,)) for i in range(N)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    s = m.stats()
    # Each thread executed 2 checks
    assert s.total_evaluations == N * 2
    assert len(m.unhealthy_docs()) == N


def test_thread_safety_mixed_operations():
    m = DocHealthMonitor()
    for i in range(5):
        m.register_check(HealthCheck(f"c{i}", "n", check=always_healthy))

    stop = threading.Event()
    errors = []

    def reader():
        try:
            while not stop.is_set():
                m.list_checks()
                m.stats()
                m.unhealthy_docs()
        except Exception as exc:  # noqa: BLE001
            errors.append(exc)

    def writer(idx):
        try:
            for j in range(20):
                m.evaluate(f"d{idx}-{j}", "x")
        except Exception as exc:  # noqa: BLE001
            errors.append(exc)

    readers = [threading.Thread(target=reader) for _ in range(3)]
    writers = [threading.Thread(target=writer, args=(i,)) for i in range(3)]
    for t in readers + writers:
        t.start()
    for t in writers:
        t.join()
    stop.set()
    for t in readers:
        t.join()

    assert not errors


def test_thread_safety_clear_during_evaluate():
    m = DocHealthMonitor()
    m.register_check(HealthCheck("c1", "n", check=always_healthy))

    def writer():
        for i in range(50):
            m.evaluate(f"d{i}", "x")

    def cleaner():
        for _ in range(10):
            m.clear_results()

    threads = [
        threading.Thread(target=writer),
        threading.Thread(target=cleaner),
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    # No assertion on final size — just ensuring no exception/race.


# ---------------------------------------------------------------------------
# Integration / scenarios
# ---------------------------------------------------------------------------

def test_scenario_lifecycle_complete():
    m = DocHealthMonitor()
    m.register_check(HealthCheck("title", "title", severity="warning", check=has_title))
    m.register_check(HealthCheck("length", "length", severity="info", check=long_enough))

    # All pass
    m.evaluate("good", "# A nice long title")
    assert m.health_score("good") == 1.0

    # Title fails
    m.evaluate("untitled", "Just some content here")
    assert m.health_score("untitled") == 0.5

    # All fail
    m.evaluate("bad", "no")
    assert m.health_score("bad") == 0.0

    # Filtering
    assert m.unhealthy_docs() == ["bad", "untitled"]
    assert m.unhealthy_docs(severity="info") == ["bad"]
    assert m.unhealthy_docs(severity="warning") == ["bad", "untitled"]


def test_scenario_disable_then_enable():
    m = DocHealthMonitor()
    m.register_check(HealthCheck("c1", "n", check=always_unhealthy))
    m.disable_check("c1")
    assert m.evaluate("d", "x") == []
    m.enable_check("c1")
    assert len(m.evaluate("d", "x")) == 1


def test_scenario_remove_check_resets_score():
    m = DocHealthMonitor()
    m.register_check(HealthCheck("c1", "n", check=always_unhealthy))
    m.register_check(HealthCheck("c2", "n", check=always_healthy))
    m.evaluate("d", "x")
    assert m.health_score("d") == 0.5
    m.unregister_check("c1")
    assert m.health_score("d") == 1.0
