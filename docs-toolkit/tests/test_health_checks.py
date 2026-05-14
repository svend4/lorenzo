"""Tests for docstoolkit/health_checks/ — 72+ tests."""
from __future__ import annotations

import time

import pytest

from docstoolkit.health_checks.check import (
    CheckResult,
    FunctionCheck,
    HealthCheck,
    HealthStatus,
)
from docstoolkit.health_checks.registry import HealthReport, HealthRegistry
from docstoolkit.health_checks import (
    CheckResult as CRExport,
    FunctionCheck as FCExport,
    HealthCheck as HCExport,
    HealthReport as HRExport,
    HealthRegistry as HRegExport,
    HealthStatus as HSExport,
)


# ---------------------------------------------------------------------------
# HealthStatus enum
# ---------------------------------------------------------------------------

class TestHealthStatus:
    def test_healthy_value(self):
        assert HealthStatus.HEALTHY == "healthy"

    def test_degraded_value(self):
        assert HealthStatus.DEGRADED == "degraded"

    def test_unhealthy_value(self):
        assert HealthStatus.UNHEALTHY == "unhealthy"

    def test_three_members(self):
        assert len(HealthStatus) == 3

    def test_is_str_enum(self):
        assert isinstance(HealthStatus.HEALTHY, str)

    def test_distinct_values(self):
        vals = {s.value for s in HealthStatus}
        assert len(vals) == 3


# ---------------------------------------------------------------------------
# CheckResult
# ---------------------------------------------------------------------------

class TestCheckResult:
    def test_fields_stored(self):
        r = CheckResult(name="db", status=HealthStatus.HEALTHY, message="ok",
                        duration_ms=1.5, details={"host": "localhost"})
        assert r.name == "db"
        assert r.status == HealthStatus.HEALTHY
        assert r.message == "ok"
        assert r.duration_ms == 1.5
        assert r.details == {"host": "localhost"}

    def test_message_default_empty(self):
        r = CheckResult(name="x", status=HealthStatus.HEALTHY)
        assert r.message == ""

    def test_duration_ms_default_zero(self):
        r = CheckResult(name="x", status=HealthStatus.HEALTHY)
        assert r.duration_ms == 0.0

    def test_details_default_empty_dict(self):
        r = CheckResult(name="x", status=HealthStatus.HEALTHY)
        assert r.details == {}

    def test_details_not_shared_between_instances(self):
        r1 = CheckResult(name="a", status=HealthStatus.HEALTHY)
        r2 = CheckResult(name="b", status=HealthStatus.HEALTHY)
        r1.details["k"] = "v"
        assert "k" not in r2.details

    def test_is_healthy_when_healthy(self):
        r = CheckResult(name="x", status=HealthStatus.HEALTHY)
        assert r.is_healthy() is True

    def test_is_healthy_when_degraded(self):
        r = CheckResult(name="x", status=HealthStatus.DEGRADED)
        assert r.is_healthy() is False

    def test_is_healthy_when_unhealthy(self):
        r = CheckResult(name="x", status=HealthStatus.UNHEALTHY)
        assert r.is_healthy() is False

    def test_is_degraded_when_degraded(self):
        r = CheckResult(name="x", status=HealthStatus.DEGRADED)
        assert r.is_degraded() is True

    def test_is_degraded_when_healthy(self):
        r = CheckResult(name="x", status=HealthStatus.HEALTHY)
        assert r.is_degraded() is False

    def test_is_degraded_when_unhealthy(self):
        r = CheckResult(name="x", status=HealthStatus.UNHEALTHY)
        assert r.is_degraded() is False


# ---------------------------------------------------------------------------
# FunctionCheck — construction
# ---------------------------------------------------------------------------

class TestFunctionCheckInit:
    def test_name_stored(self):
        fc = FunctionCheck("mycheck", lambda: True)
        assert fc.name == "mycheck"

    def test_default_timeout(self):
        fc = FunctionCheck("x", lambda: True)
        assert fc._timeout_ms == 5000.0

    def test_custom_timeout(self):
        fc = FunctionCheck("x", lambda: True, timeout_ms=1234.5)
        assert fc._timeout_ms == 1234.5

    def test_is_healthcheck_subclass(self):
        fc = FunctionCheck("x", lambda: True)
        assert isinstance(fc, HealthCheck)


# ---------------------------------------------------------------------------
# FunctionCheck — bool-returning func
# ---------------------------------------------------------------------------

class TestFunctionCheckBoolReturn:
    def test_true_returns_healthy(self):
        fc = FunctionCheck("chk", lambda: True)
        result = fc.run()
        assert result.status == HealthStatus.HEALTHY

    def test_false_returns_unhealthy(self):
        fc = FunctionCheck("chk", lambda: False)
        result = fc.run()
        assert result.status == HealthStatus.UNHEALTHY

    def test_name_propagated_true(self):
        fc = FunctionCheck("db.ping", lambda: True)
        assert fc.run().name == "db.ping"

    def test_name_propagated_false(self):
        fc = FunctionCheck("db.ping", lambda: False)
        assert fc.run().name == "db.ping"

    def test_message_empty_on_bool_true(self):
        fc = FunctionCheck("x", lambda: True)
        assert fc.run().message == ""

    def test_message_empty_on_bool_false(self):
        fc = FunctionCheck("x", lambda: False)
        assert fc.run().message == ""

    def test_returns_check_result(self):
        fc = FunctionCheck("x", lambda: True)
        assert isinstance(fc.run(), CheckResult)


# ---------------------------------------------------------------------------
# FunctionCheck — tuple-returning func
# ---------------------------------------------------------------------------

class TestFunctionCheckTupleReturn:
    def test_healthy_tuple(self):
        fc = FunctionCheck("x", lambda: (HealthStatus.HEALTHY, "all good"))
        result = fc.run()
        assert result.status == HealthStatus.HEALTHY
        assert result.message == "all good"

    def test_degraded_tuple(self):
        fc = FunctionCheck("x", lambda: (HealthStatus.DEGRADED, "slow"))
        result = fc.run()
        assert result.status == HealthStatus.DEGRADED
        assert result.message == "slow"

    def test_unhealthy_tuple(self):
        fc = FunctionCheck("x", lambda: (HealthStatus.UNHEALTHY, "down"))
        result = fc.run()
        assert result.status == HealthStatus.UNHEALTHY
        assert result.message == "down"

    def test_tuple_name_propagated(self):
        fc = FunctionCheck("cache.hit", lambda: (HealthStatus.HEALTHY, "ok"))
        assert fc.run().name == "cache.hit"

    def test_tuple_message_stored_as_str(self):
        fc = FunctionCheck("x", lambda: (HealthStatus.DEGRADED, 42))
        result = fc.run()
        assert result.message == "42"


# ---------------------------------------------------------------------------
# FunctionCheck — exception → UNHEALTHY
# ---------------------------------------------------------------------------

class TestFunctionCheckException:
    def test_exception_gives_unhealthy(self):
        def boom():
            raise RuntimeError("connection refused")
        fc = FunctionCheck("db", boom)
        result = fc.run()
        assert result.status == HealthStatus.UNHEALTHY

    def test_exception_message_propagated(self):
        def boom():
            raise ValueError("bad config")
        fc = FunctionCheck("cfg", boom)
        result = fc.run()
        assert "bad config" in result.message

    def test_exception_name_propagated(self):
        def boom():
            raise RuntimeError("oops")
        fc = FunctionCheck("svc.up", boom)
        assert fc.run().name == "svc.up"

    def test_zero_division_exception(self):
        def boom():
            return 1 / 0
        fc = FunctionCheck("math", boom)
        result = fc.run()
        assert result.status == HealthStatus.UNHEALTHY

    def test_exception_returns_check_result(self):
        def boom():
            raise RuntimeError()
        fc = FunctionCheck("x", boom)
        assert isinstance(fc.run(), CheckResult)


# ---------------------------------------------------------------------------
# FunctionCheck — duration_ms measured
# ---------------------------------------------------------------------------

class TestFunctionCheckDuration:
    def test_duration_ms_positive(self):
        fc = FunctionCheck("x", lambda: True)
        result = fc.run()
        assert result.duration_ms >= 0.0

    def test_duration_ms_reflects_sleep(self):
        def slow():
            time.sleep(0.05)
            return True
        fc = FunctionCheck("slow", slow)
        result = fc.run()
        assert result.duration_ms >= 40.0  # at least 40 ms

    def test_duration_ms_exception_measured(self):
        def boom():
            time.sleep(0.02)
            raise RuntimeError("x")
        fc = FunctionCheck("x", boom)
        result = fc.run()
        assert result.duration_ms >= 10.0

    def test_duration_ms_is_float(self):
        fc = FunctionCheck("x", lambda: True)
        assert isinstance(fc.run().duration_ms, float)


# ---------------------------------------------------------------------------
# HealthReport
# ---------------------------------------------------------------------------

def _make_result(name, status, message=""):
    return CheckResult(name=name, status=status, message=message, duration_ms=1.0)


class TestHealthReport:
    def test_overall_all_healthy(self):
        report = HealthReport(timestamp=1.0, checks=[
            _make_result("a", HealthStatus.HEALTHY),
            _make_result("b", HealthStatus.HEALTHY),
        ])
        assert report.overall_status() == HealthStatus.HEALTHY

    def test_overall_any_unhealthy(self):
        report = HealthReport(timestamp=1.0, checks=[
            _make_result("a", HealthStatus.HEALTHY),
            _make_result("b", HealthStatus.UNHEALTHY),
        ])
        assert report.overall_status() == HealthStatus.UNHEALTHY

    def test_overall_unhealthy_wins_over_degraded(self):
        report = HealthReport(timestamp=1.0, checks=[
            _make_result("a", HealthStatus.DEGRADED),
            _make_result("b", HealthStatus.UNHEALTHY),
        ])
        assert report.overall_status() == HealthStatus.UNHEALTHY

    def test_overall_any_degraded_no_unhealthy(self):
        report = HealthReport(timestamp=1.0, checks=[
            _make_result("a", HealthStatus.HEALTHY),
            _make_result("b", HealthStatus.DEGRADED),
        ])
        assert report.overall_status() == HealthStatus.DEGRADED

    def test_overall_empty_is_healthy(self):
        report = HealthReport(timestamp=1.0, checks=[])
        assert report.overall_status() == HealthStatus.HEALTHY

    def test_healthy_count(self):
        report = HealthReport(timestamp=1.0, checks=[
            _make_result("a", HealthStatus.HEALTHY),
            _make_result("b", HealthStatus.HEALTHY),
            _make_result("c", HealthStatus.UNHEALTHY),
        ])
        assert report.healthy_count() == 2

    def test_unhealthy_count(self):
        report = HealthReport(timestamp=1.0, checks=[
            _make_result("a", HealthStatus.HEALTHY),
            _make_result("b", HealthStatus.UNHEALTHY),
            _make_result("c", HealthStatus.UNHEALTHY),
        ])
        assert report.unhealthy_count() == 2

    def test_degraded_count(self):
        report = HealthReport(timestamp=1.0, checks=[
            _make_result("a", HealthStatus.DEGRADED),
            _make_result("b", HealthStatus.HEALTHY),
            _make_result("c", HealthStatus.DEGRADED),
        ])
        assert report.degraded_count() == 2

    def test_counts_all_zero_when_empty(self):
        report = HealthReport(timestamp=1.0, checks=[])
        assert report.healthy_count() == 0
        assert report.unhealthy_count() == 0
        assert report.degraded_count() == 0

    def test_to_dict_keys(self):
        report = HealthReport(timestamp=1.0, checks=[_make_result("x", HealthStatus.HEALTHY)])
        d = report.to_dict()
        for key in ("timestamp", "overall_status", "total", "healthy", "degraded", "unhealthy", "checks"):
            assert key in d, f"Missing key: {key}"

    def test_to_dict_timestamp(self):
        report = HealthReport(timestamp=42.5, checks=[])
        assert report.to_dict()["timestamp"] == 42.5

    def test_to_dict_overall_status_value(self):
        report = HealthReport(timestamp=1.0, checks=[_make_result("x", HealthStatus.UNHEALTHY)])
        d = report.to_dict()
        assert d["overall_status"] == "unhealthy"

    def test_to_dict_total_count(self):
        report = HealthReport(timestamp=1.0, checks=[
            _make_result("a", HealthStatus.HEALTHY),
            _make_result("b", HealthStatus.DEGRADED),
        ])
        assert report.to_dict()["total"] == 2

    def test_to_dict_checks_list(self):
        report = HealthReport(timestamp=1.0, checks=[_make_result("db", HealthStatus.HEALTHY)])
        d = report.to_dict()
        assert isinstance(d["checks"], list)
        assert d["checks"][0]["name"] == "db"
        assert d["checks"][0]["status"] == "healthy"

    def test_to_dict_is_serialisable(self):
        import json
        report = HealthReport(timestamp=1.0, checks=[
            _make_result("a", HealthStatus.HEALTHY),
            _make_result("b", HealthStatus.UNHEALTHY, "oops"),
        ])
        serialised = json.dumps(report.to_dict())
        assert "unhealthy" in serialised


# ---------------------------------------------------------------------------
# HealthRegistry — register / unregister / get / names
# ---------------------------------------------------------------------------

class TestHealthRegistryManagement:
    def test_register_single(self):
        reg = HealthRegistry()
        fc = FunctionCheck("ping", lambda: True)
        reg.register(fc)
        assert reg.get("ping") is fc

    def test_register_multiple(self):
        reg = HealthRegistry()
        reg.register(FunctionCheck("a", lambda: True))
        reg.register(FunctionCheck("b", lambda: True))
        assert set(reg.names()) == {"a", "b"}

    def test_overwrite_same_name(self):
        reg = HealthRegistry()
        fc1 = FunctionCheck("x", lambda: True)
        fc2 = FunctionCheck("x", lambda: False)
        reg.register(fc1)
        reg.register(fc2)
        assert reg.get("x") is fc2

    def test_unregister_existing_returns_true(self):
        reg = HealthRegistry()
        reg.register(FunctionCheck("x", lambda: True))
        assert reg.unregister("x") is True

    def test_unregister_existing_removes(self):
        reg = HealthRegistry()
        reg.register(FunctionCheck("x", lambda: True))
        reg.unregister("x")
        assert reg.get("x") is None

    def test_unregister_missing_returns_false(self):
        reg = HealthRegistry()
        assert reg.unregister("nonexistent") is False

    def test_get_missing_returns_none(self):
        reg = HealthRegistry()
        assert reg.get("missing") is None

    def test_names_empty(self):
        reg = HealthRegistry()
        assert reg.names() == []

    def test_names_sorted(self):
        reg = HealthRegistry()
        reg.register(FunctionCheck("z", lambda: True))
        reg.register(FunctionCheck("a", lambda: True))
        reg.register(FunctionCheck("m", lambda: True))
        assert reg.names() == ["a", "m", "z"]

    def test_names_returns_list(self):
        reg = HealthRegistry()
        assert isinstance(reg.names(), list)


# ---------------------------------------------------------------------------
# HealthRegistry — run_one
# ---------------------------------------------------------------------------

class TestHealthRegistryRunOne:
    def test_run_one_success(self):
        reg = HealthRegistry()
        reg.register(FunctionCheck("db", lambda: True))
        result = reg.run_one("db")
        assert result.status == HealthStatus.HEALTHY

    def test_run_one_name_propagated(self):
        reg = HealthRegistry()
        reg.register(FunctionCheck("svc", lambda: False))
        result = reg.run_one("svc")
        assert result.name == "svc"

    def test_run_one_keyerror_if_missing(self):
        reg = HealthRegistry()
        with pytest.raises(KeyError):
            reg.run_one("ghost")

    def test_run_one_returns_check_result(self):
        reg = HealthRegistry()
        reg.register(FunctionCheck("x", lambda: True))
        assert isinstance(reg.run_one("x"), CheckResult)

    def test_run_one_after_unregister_raises(self):
        reg = HealthRegistry()
        reg.register(FunctionCheck("x", lambda: True))
        reg.unregister("x")
        with pytest.raises(KeyError):
            reg.run_one("x")


# ---------------------------------------------------------------------------
# HealthRegistry — run_all sequential
# ---------------------------------------------------------------------------

class TestHealthRegistryRunAllSequential:
    def test_run_all_empty_registry(self):
        reg = HealthRegistry()
        report = reg.run_all()
        assert isinstance(report, HealthReport)
        assert report.checks == []

    def test_run_all_empty_overall_healthy(self):
        reg = HealthRegistry()
        report = reg.run_all()
        assert report.overall_status() == HealthStatus.HEALTHY

    def test_run_all_single_healthy(self):
        reg = HealthRegistry()
        reg.register(FunctionCheck("a", lambda: True))
        report = reg.run_all()
        assert report.healthy_count() == 1

    def test_run_all_multiple_checks(self):
        reg = HealthRegistry()
        for name in ("a", "b", "c"):
            reg.register(FunctionCheck(name, lambda: True))
        report = reg.run_all()
        assert len(report.checks) == 3

    def test_run_all_mixed_statuses(self):
        reg = HealthRegistry()
        reg.register(FunctionCheck("ok", lambda: True))
        reg.register(FunctionCheck("bad", lambda: False))
        reg.register(FunctionCheck("deg", lambda: (HealthStatus.DEGRADED, "slow")))
        report = reg.run_all()
        assert report.healthy_count() == 1
        assert report.unhealthy_count() == 1
        assert report.degraded_count() == 1

    def test_run_all_overall_unhealthy_with_bad_check(self):
        reg = HealthRegistry()
        reg.register(FunctionCheck("good", lambda: True))
        reg.register(FunctionCheck("bad", lambda: False))
        report = reg.run_all()
        assert report.overall_status() == HealthStatus.UNHEALTHY

    def test_run_all_timestamp_is_float(self):
        reg = HealthRegistry()
        report = reg.run_all()
        assert isinstance(report.timestamp, float)

    def test_run_all_timestamp_recent(self):
        reg = HealthRegistry()
        before = time.time()
        report = reg.run_all()
        after = time.time()
        assert before <= report.timestamp <= after


# ---------------------------------------------------------------------------
# HealthRegistry — run_all parallel
# ---------------------------------------------------------------------------

class TestHealthRegistryRunAllParallel:
    def _make_registry(self):
        reg = HealthRegistry()
        reg.register(FunctionCheck("a", lambda: True))
        reg.register(FunctionCheck("b", lambda: (HealthStatus.DEGRADED, "slow response")))
        reg.register(FunctionCheck("c", lambda: False))
        return reg

    def test_parallel_same_count(self):
        reg = self._make_registry()
        seq_report = reg.run_all(parallel=False)
        par_report = reg.run_all(parallel=True)
        assert len(par_report.checks) == len(seq_report.checks)

    def test_parallel_same_overall_status(self):
        reg = self._make_registry()
        seq = reg.run_all(parallel=False)
        par = reg.run_all(parallel=True)
        assert par.overall_status() == seq.overall_status()

    def test_parallel_same_statuses(self):
        reg = self._make_registry()
        seq = reg.run_all(parallel=False)
        par = reg.run_all(parallel=True)
        seq_statuses = {c.name: c.status for c in seq.checks}
        par_statuses = {c.name: c.status for c in par.checks}
        assert seq_statuses == par_statuses

    def test_parallel_empty_registry(self):
        reg = HealthRegistry()
        report = reg.run_all(parallel=True)
        assert report.checks == []
        assert report.overall_status() == HealthStatus.HEALTHY

    def test_parallel_returns_health_report(self):
        reg = self._make_registry()
        assert isinstance(reg.run_all(parallel=True), HealthReport)

    def test_parallel_healthy_count(self):
        reg = self._make_registry()
        report = reg.run_all(parallel=True)
        assert report.healthy_count() == 1

    def test_parallel_degraded_count(self):
        reg = self._make_registry()
        report = reg.run_all(parallel=True)
        assert report.degraded_count() == 1

    def test_parallel_unhealthy_count(self):
        reg = self._make_registry()
        report = reg.run_all(parallel=True)
        assert report.unhealthy_count() == 1


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_same_name_overwrite_used_in_run_all(self):
        reg = HealthRegistry()
        reg.register(FunctionCheck("chk", lambda: False))  # unhealthy
        reg.register(FunctionCheck("chk", lambda: True))   # healthy — overwrites
        report = reg.run_all()
        assert len(report.checks) == 1
        assert report.checks[0].status == HealthStatus.HEALTHY

    def test_run_all_with_exception_in_func_is_unhealthy(self):
        reg = HealthRegistry()
        def boom():
            raise RuntimeError("crash")
        reg.register(FunctionCheck("crasher", boom))
        report = reg.run_all()
        assert report.overall_status() == HealthStatus.UNHEALTHY

    def test_mix_all_three_statuses_overall_unhealthy(self):
        reg = HealthRegistry()
        reg.register(FunctionCheck("h", lambda: True))
        reg.register(FunctionCheck("d", lambda: (HealthStatus.DEGRADED, "warn")))
        reg.register(FunctionCheck("u", lambda: False))
        report = reg.run_all()
        assert report.overall_status() == HealthStatus.UNHEALTHY
        assert report.healthy_count() == 1
        assert report.degraded_count() == 1
        assert report.unhealthy_count() == 1

    def test_function_check_with_none_return_treated_as_unhealthy(self):
        fc = FunctionCheck("x", lambda: None)
        result = fc.run()
        assert result.status == HealthStatus.UNHEALTHY

    def test_unregister_then_reregister(self):
        reg = HealthRegistry()
        reg.register(FunctionCheck("x", lambda: False))
        reg.unregister("x")
        reg.register(FunctionCheck("x", lambda: True))
        result = reg.run_one("x")
        assert result.status == HealthStatus.HEALTHY


# ---------------------------------------------------------------------------
# __init__ re-exports
# ---------------------------------------------------------------------------

class TestPublicAPI:
    def test_health_status_exported(self):
        assert HSExport.HEALTHY == HealthStatus.HEALTHY

    def test_check_result_exported(self):
        r = CRExport(name="x", status=HSExport.HEALTHY)
        assert isinstance(r, CheckResult)

    def test_function_check_exported(self):
        fc = FCExport("x", lambda: True)
        assert isinstance(fc, FunctionCheck)

    def test_health_check_exported(self):
        assert HCExport is HealthCheck

    def test_health_report_exported(self):
        r = HRExport(timestamp=1.0)
        assert isinstance(r, HealthReport)

    def test_health_registry_exported(self):
        reg = HRegExport()
        assert isinstance(reg, HealthRegistry)
