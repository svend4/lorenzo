"""Tests for docstoolkit.doc_health (E271)."""
from __future__ import annotations

import time

import pytest

from docstoolkit.doc_health import (
    CheckResult,
    DocHealth,
    HealthCheck,
    HealthReport,
    HealthStatus,
)


# ---- helpers ------------------------------------------------------------
def make_check(name: str, status: HealthStatus, message: str = "ok"):
    def _fn() -> CheckResult:
        return CheckResult(check_name=name, status=status, message=message)
    return _fn


def healthy(name="c") -> CheckResult:
    return CheckResult(check_name=name, status=HealthStatus.HEALTHY, message="ok")


def degraded(name="c") -> CheckResult:
    return CheckResult(check_name=name, status=HealthStatus.DEGRADED, message="warn")


def unhealthy(name="c") -> CheckResult:
    return CheckResult(check_name=name, status=HealthStatus.UNHEALTHY, message="bad")


# ---- TestHealthStatus ---------------------------------------------------
class TestHealthStatus:
    def test_values_exist(self):
        assert HealthStatus.HEALTHY
        assert HealthStatus.DEGRADED
        assert HealthStatus.UNHEALTHY
        assert HealthStatus.UNKNOWN

    def test_distinct_values(self):
        s = {HealthStatus.HEALTHY, HealthStatus.DEGRADED,
             HealthStatus.UNHEALTHY, HealthStatus.UNKNOWN}
        assert len(s) == 4

    def test_string_enum(self):
        assert HealthStatus.HEALTHY.value == "healthy"


# ---- TestCheckResult ----------------------------------------------------
class TestCheckResult:
    def test_basic(self):
        r = CheckResult(check_name="x", status=HealthStatus.HEALTHY, message="ok")
        assert r.check_name == "x"
        assert r.status == HealthStatus.HEALTHY
        assert r.message == "ok"

    def test_default_details(self):
        r = CheckResult(check_name="x", status=HealthStatus.HEALTHY, message="ok")
        assert r.details == {}

    def test_default_timestamp_and_duration(self):
        r = CheckResult(check_name="x", status=HealthStatus.HEALTHY, message="ok")
        assert r.timestamp == 0.0
        assert r.duration_ms == 0.0

    def test_with_details(self):
        r = CheckResult(check_name="x", status=HealthStatus.HEALTHY, message="ok",
                        details={"k": 1})
        assert r.details["k"] == 1


# ---- TestHealthCheck ----------------------------------------------------
class TestHealthCheck:
    def test_basic(self):
        fn = lambda: healthy()
        c = HealthCheck(name="x", check_func=fn)
        assert c.name == "x"
        assert c.check_func is fn

    def test_defaults(self):
        c = HealthCheck(name="x", check_func=lambda: healthy())
        assert c.interval_seconds == 60.0
        assert c.enabled is True
        assert c.critical is True

    def test_overrides(self):
        c = HealthCheck(name="x", check_func=lambda: healthy(),
                        interval_seconds=10.0, enabled=False, critical=False)
        assert c.interval_seconds == 10.0
        assert c.enabled is False
        assert c.critical is False


# ---- TestHealthReport ---------------------------------------------------
class TestHealthReport:
    def test_basic(self):
        r = HealthReport(
            overall_status=HealthStatus.HEALTHY,
            checks=[],
            timestamp=1.0,
            degraded_count=0,
            unhealthy_count=0,
            healthy_count=0,
        )
        assert r.overall_status == HealthStatus.HEALTHY
        assert r.checks == []
        assert r.timestamp == 1.0

    def test_counts(self):
        r = HealthReport(
            overall_status=HealthStatus.DEGRADED,
            checks=[healthy(), degraded()],
            timestamp=2.0,
            degraded_count=1,
            unhealthy_count=0,
            healthy_count=1,
        )
        assert r.degraded_count == 1
        assert r.healthy_count == 1


# ---- TestRegisterCheck --------------------------------------------------
class TestRegisterCheck:
    def test_register_returns_healthcheck(self):
        dh = DocHealth()
        c = dh.register_check("a", lambda: healthy())
        assert isinstance(c, HealthCheck)
        assert c.name == "a"

    def test_register_adds_to_checks(self):
        dh = DocHealth()
        dh.register_check("a", lambda: healthy())
        assert dh.total_checks == 1

    def test_register_with_interval(self):
        dh = DocHealth()
        c = dh.register_check("a", lambda: healthy(), interval_seconds=5.0)
        assert c.interval_seconds == 5.0

    def test_register_with_critical_false(self):
        dh = DocHealth()
        c = dh.register_check("a", lambda: healthy(), critical=False)
        assert c.critical is False

    def test_register_multiple(self):
        dh = DocHealth()
        dh.register_check("a", lambda: healthy())
        dh.register_check("b", lambda: healthy())
        dh.register_check("c", lambda: healthy())
        assert dh.total_checks == 3


# ---- TestUnregisterCheck ------------------------------------------------
class TestUnregisterCheck:
    def test_unregister_existing(self):
        dh = DocHealth()
        dh.register_check("a", lambda: healthy())
        assert dh.unregister_check("a") is True
        assert dh.total_checks == 0

    def test_unregister_missing(self):
        dh = DocHealth()
        assert dh.unregister_check("missing") is False

    def test_unregister_clears_history(self):
        dh = DocHealth()
        dh.register_check("a", lambda: healthy())
        dh.run_check("a")
        dh.unregister_check("a")
        assert dh.history("a") == []
        assert dh.last_result("a") is None


# ---- TestEnableDisable --------------------------------------------------
class TestEnableDisable:
    def test_disable_existing(self):
        dh = DocHealth()
        dh.register_check("a", lambda: healthy())
        assert dh.disable_check("a") is True
        assert dh.checks()[0].enabled is False

    def test_enable_existing(self):
        dh = DocHealth()
        dh.register_check("a", lambda: healthy())
        dh.disable_check("a")
        assert dh.enable_check("a") is True
        assert dh.checks()[0].enabled is True

    def test_disable_missing(self):
        dh = DocHealth()
        assert dh.disable_check("none") is False

    def test_enable_missing(self):
        dh = DocHealth()
        assert dh.enable_check("none") is False


# ---- TestRunCheck -------------------------------------------------------
class TestRunCheck:
    def test_run_check_returns_result(self):
        dh = DocHealth()
        dh.register_check("a", lambda: healthy("a"))
        r = dh.run_check("a")
        assert r is not None
        assert r.status == HealthStatus.HEALTHY

    def test_run_check_missing(self):
        dh = DocHealth()
        assert dh.run_check("missing") is None

    def test_run_check_sets_timestamp(self):
        dh = DocHealth()
        dh.register_check("a", lambda: healthy("a"))
        r = dh.run_check("a", now=123.45)
        assert r.timestamp == 123.45

    def test_run_check_default_now(self):
        dh = DocHealth()
        dh.register_check("a", lambda: healthy("a"))
        before = time.time()
        r = dh.run_check("a")
        after = time.time()
        assert before <= r.timestamp <= after

    def test_run_check_sets_duration(self):
        dh = DocHealth()
        dh.register_check("a", lambda: healthy("a"))
        r = dh.run_check("a")
        assert r.duration_ms >= 0.0

    def test_run_check_sets_check_name(self):
        dh = DocHealth()

        def fn():
            return CheckResult(check_name="wrong", status=HealthStatus.HEALTHY, message="ok")

        dh.register_check("right", fn)
        r = dh.run_check("right")
        assert r.check_name == "right"

    def test_run_check_stores_last_result(self):
        dh = DocHealth()
        dh.register_check("a", lambda: healthy("a"))
        dh.run_check("a")
        assert dh.last_result("a") is not None


# ---- TestRunCheckException ----------------------------------------------
class TestRunCheckException:
    def test_exception_yields_unknown(self):
        dh = DocHealth()

        def boom():
            raise RuntimeError("boom")

        dh.register_check("a", boom)
        r = dh.run_check("a")
        assert r.status == HealthStatus.UNKNOWN

    def test_exception_message_captured(self):
        dh = DocHealth()

        def boom():
            raise ValueError("specific error")

        dh.register_check("a", boom)
        r = dh.run_check("a")
        assert "specific error" in r.message

    def test_exception_still_records(self):
        dh = DocHealth()

        def boom():
            raise Exception("x")

        dh.register_check("a", boom)
        dh.run_check("a")
        assert dh.last_result("a") is not None
        assert len(dh.history("a")) == 1


# ---- TestRunAll ---------------------------------------------------------
class TestRunAll:
    def test_run_all_returns_report(self):
        dh = DocHealth()
        dh.register_check("a", lambda: healthy("a"))
        dh.register_check("b", lambda: healthy("b"))
        rep = dh.run_all()
        assert isinstance(rep, HealthReport)
        assert len(rep.checks) == 2

    def test_run_all_skips_disabled(self):
        dh = DocHealth()
        dh.register_check("a", lambda: healthy("a"))
        dh.register_check("b", lambda: healthy("b"))
        dh.disable_check("b")
        rep = dh.run_all()
        assert len(rep.checks) == 1
        assert rep.checks[0].check_name == "a"

    def test_run_all_counts(self):
        dh = DocHealth()
        dh.register_check("a", lambda: healthy("a"))
        dh.register_check("b", lambda: degraded("b"))
        dh.register_check("c", lambda: unhealthy("c"))
        rep = dh.run_all()
        assert rep.healthy_count == 1
        assert rep.degraded_count == 1
        assert rep.unhealthy_count == 1

    def test_run_all_empty(self):
        dh = DocHealth()
        rep = dh.run_all()
        assert rep.checks == []
        assert rep.overall_status == HealthStatus.HEALTHY

    def test_run_all_uses_now(self):
        dh = DocHealth()
        dh.register_check("a", lambda: healthy("a"))
        rep = dh.run_all(now=100.0)
        assert rep.timestamp == 100.0


# ---- TestLastResult -----------------------------------------------------
class TestLastResult:
    def test_last_result_after_run(self):
        dh = DocHealth()
        dh.register_check("a", lambda: healthy("a"))
        dh.run_check("a")
        assert dh.last_result("a").status == HealthStatus.HEALTHY

    def test_last_result_before_run(self):
        dh = DocHealth()
        dh.register_check("a", lambda: healthy("a"))
        assert dh.last_result("a") is None

    def test_last_result_missing_check(self):
        dh = DocHealth()
        assert dh.last_result("nope") is None

    def test_last_result_updates(self):
        dh = DocHealth()
        state = {"calls": 0}

        def fn():
            state["calls"] += 1
            if state["calls"] == 1:
                return healthy("a")
            return unhealthy("a")

        dh.register_check("a", fn)
        dh.run_check("a")
        dh.run_check("a")
        assert dh.last_result("a").status == HealthStatus.UNHEALTHY


# ---- TestHistory --------------------------------------------------------
class TestHistory:
    def test_history_accumulates(self):
        dh = DocHealth()
        dh.register_check("a", lambda: healthy("a"))
        dh.run_check("a")
        dh.run_check("a")
        dh.run_check("a")
        assert len(dh.history("a")) == 3

    def test_history_limit(self):
        dh = DocHealth()
        dh.register_check("a", lambda: healthy("a"))
        for _ in range(5):
            dh.run_check("a")
        h = dh.history("a", limit=2)
        assert len(h) == 2

    def test_history_unknown_check(self):
        dh = DocHealth()
        assert dh.history("none") == []

    def test_history_no_runs(self):
        dh = DocHealth()
        dh.register_check("a", lambda: healthy("a"))
        assert dh.history("a") == []


# ---- TestOverallStatusHealthy -------------------------------------------
class TestOverallStatusHealthy:
    def test_all_healthy(self):
        dh = DocHealth()
        dh.register_check("a", lambda: healthy("a"))
        dh.register_check("b", lambda: healthy("b"))
        dh.run_all()
        assert dh.overall_status() == HealthStatus.HEALTHY

    def test_no_checks(self):
        dh = DocHealth()
        assert dh.overall_status() == HealthStatus.HEALTHY

    def test_report_healthy(self):
        dh = DocHealth()
        dh.register_check("a", lambda: healthy("a"))
        rep = dh.run_all()
        assert rep.overall_status == HealthStatus.HEALTHY


# ---- TestOverallStatusDegraded ------------------------------------------
class TestOverallStatusDegraded:
    def test_one_degraded(self):
        dh = DocHealth()
        dh.register_check("a", lambda: healthy("a"))
        dh.register_check("b", lambda: degraded("b"))
        dh.run_all()
        assert dh.overall_status() == HealthStatus.DEGRADED

    def test_noncritical_unhealthy_degrades(self):
        dh = DocHealth()
        dh.register_check("a", lambda: healthy("a"))
        dh.register_check("b", lambda: unhealthy("b"), critical=False)
        rep = dh.run_all()
        assert rep.overall_status == HealthStatus.DEGRADED

    def test_degraded_in_report(self):
        dh = DocHealth()
        dh.register_check("a", lambda: degraded("a"))
        rep = dh.run_all()
        assert rep.overall_status == HealthStatus.DEGRADED


# ---- TestOverallStatusUnhealthy -----------------------------------------
class TestOverallStatusUnhealthy:
    def test_critical_unhealthy(self):
        dh = DocHealth()
        dh.register_check("a", lambda: healthy("a"))
        dh.register_check("b", lambda: unhealthy("b"), critical=True)
        dh.run_all()
        assert dh.overall_status() == HealthStatus.UNHEALTHY

    def test_unhealthy_dominates_degraded(self):
        dh = DocHealth()
        dh.register_check("a", lambda: degraded("a"))
        dh.register_check("b", lambda: unhealthy("b"), critical=True)
        rep = dh.run_all()
        assert rep.overall_status == HealthStatus.UNHEALTHY

    def test_report_unhealthy(self):
        dh = DocHealth()
        dh.register_check("a", lambda: unhealthy("a"))
        rep = dh.run_all()
        assert rep.overall_status == HealthStatus.UNHEALTHY


# ---- TestChecks ---------------------------------------------------------
class TestChecks:
    def test_checks_all(self):
        dh = DocHealth()
        dh.register_check("a", lambda: healthy("a"))
        dh.register_check("b", lambda: healthy("b"))
        assert len(dh.checks()) == 2

    def test_checks_enabled_only(self):
        dh = DocHealth()
        dh.register_check("a", lambda: healthy("a"))
        dh.register_check("b", lambda: healthy("b"))
        dh.disable_check("b")
        enabled = dh.checks(enabled_only=True)
        assert len(enabled) == 1
        assert enabled[0].name == "a"

    def test_checks_empty(self):
        dh = DocHealth()
        assert dh.checks() == []


# ---- TestUnhealthyChecks ------------------------------------------------
class TestUnhealthyChecks:
    def test_unhealthy_listed(self):
        dh = DocHealth()
        dh.register_check("a", lambda: unhealthy("a"))
        dh.register_check("b", lambda: healthy("b"))
        dh.run_all()
        names = {r.check_name for r in dh.unhealthy_checks()}
        assert names == {"a"}

    def test_no_unhealthy(self):
        dh = DocHealth()
        dh.register_check("a", lambda: healthy("a"))
        dh.run_all()
        assert dh.unhealthy_checks() == []

    def test_unhealthy_before_run(self):
        dh = DocHealth()
        dh.register_check("a", lambda: unhealthy("a"))
        assert dh.unhealthy_checks() == []


# ---- TestDegradedChecks -------------------------------------------------
class TestDegradedChecks:
    def test_degraded_listed(self):
        dh = DocHealth()
        dh.register_check("a", lambda: degraded("a"))
        dh.register_check("b", lambda: healthy("b"))
        dh.run_all()
        names = {r.check_name for r in dh.degraded_checks()}
        assert names == {"a"}

    def test_no_degraded(self):
        dh = DocHealth()
        dh.register_check("a", lambda: healthy("a"))
        dh.run_all()
        assert dh.degraded_checks() == []


# ---- TestShouldRun ------------------------------------------------------
class TestShouldRun:
    def test_should_run_never_run(self):
        dh = DocHealth()
        dh.register_check("a", lambda: healthy("a"), interval_seconds=10.0)
        assert dh.should_run("a") is True

    def test_should_not_run_within_interval(self):
        dh = DocHealth()
        dh.register_check("a", lambda: healthy("a"), interval_seconds=10.0)
        dh.run_check("a", now=100.0)
        assert dh.should_run("a", now=105.0) is False

    def test_should_run_past_interval(self):
        dh = DocHealth()
        dh.register_check("a", lambda: healthy("a"), interval_seconds=10.0)
        dh.run_check("a", now=100.0)
        assert dh.should_run("a", now=120.0) is True

    def test_should_run_missing(self):
        dh = DocHealth()
        assert dh.should_run("none") is False

    def test_should_run_at_exact_interval_is_false(self):
        dh = DocHealth()
        dh.register_check("a", lambda: healthy("a"), interval_seconds=10.0)
        dh.run_check("a", now=100.0)
        # delta == interval is not > interval
        assert dh.should_run("a", now=110.0) is False


# ---- TestTotalChecks ----------------------------------------------------
class TestTotalChecks:
    def test_zero(self):
        dh = DocHealth()
        assert dh.total_checks == 0

    def test_after_register(self):
        dh = DocHealth()
        dh.register_check("a", lambda: healthy("a"))
        assert dh.total_checks == 1

    def test_after_unregister(self):
        dh = DocHealth()
        dh.register_check("a", lambda: healthy("a"))
        dh.register_check("b", lambda: healthy("b"))
        dh.unregister_check("a")
        assert dh.total_checks == 1


# ---- TestClear ----------------------------------------------------------
class TestClear:
    def test_clear_removes_checks(self):
        dh = DocHealth()
        dh.register_check("a", lambda: healthy("a"))
        dh.register_check("b", lambda: healthy("b"))
        dh.clear()
        assert dh.total_checks == 0

    def test_clear_removes_history(self):
        dh = DocHealth()
        dh.register_check("a", lambda: healthy("a"))
        dh.run_check("a")
        dh.clear()
        assert dh.history("a") == []
        assert dh.last_result("a") is None

    def test_clear_on_empty(self):
        dh = DocHealth()
        dh.clear()
        assert dh.total_checks == 0


# ---- TestEdgeCases ------------------------------------------------------
class TestEdgeCases:
    def test_re_register_overwrites(self):
        dh = DocHealth()
        dh.register_check("a", lambda: healthy("a"))
        dh.register_check("a", lambda: unhealthy("a"))
        r = dh.run_check("a")
        assert r.status == HealthStatus.UNHEALTHY
        assert dh.total_checks == 1

    def test_check_func_returns_non_checkresult(self):
        dh = DocHealth()
        dh.register_check("a", lambda: "not a result")  # type: ignore
        r = dh.run_check("a")
        assert r.status == HealthStatus.UNKNOWN

    def test_history_limit_zero(self):
        dh = DocHealth()
        dh.register_check("a", lambda: healthy("a"))
        dh.run_check("a")
        assert dh.history("a", limit=0) == []

    def test_run_all_does_not_run_disabled(self):
        dh = DocHealth()
        called = {"count": 0}

        def fn():
            called["count"] += 1
            return healthy("a")

        dh.register_check("a", fn)
        dh.disable_check("a")
        dh.run_all()
        assert called["count"] == 0

    def test_unknown_status_does_not_make_unhealthy(self):
        dh = DocHealth()

        def boom():
            raise RuntimeError("x")

        dh.register_check("a", boom, critical=True)
        rep = dh.run_all()
        # UNKNOWN is not UNHEALTHY, so should not flip overall to UNHEALTHY
        assert rep.overall_status == HealthStatus.HEALTHY

    def test_mixed_critical_noncritical(self):
        dh = DocHealth()
        dh.register_check("a", lambda: unhealthy("a"), critical=False)
        dh.register_check("b", lambda: healthy("b"))
        rep = dh.run_all()
        # Non-critical unhealthy => DEGRADED, not UNHEALTHY
        assert rep.overall_status == HealthStatus.DEGRADED
