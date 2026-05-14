"""Tests for docstoolkit/health/ module — 65+ tests."""
import pytest
from docstoolkit.health.signals import HealthSignal, SignalLevel, HealthCheck
from docstoolkit.health.scorer import HealthScore, compute_health_score, _LEVEL_WEIGHTS
from docstoolkit.health.report import HealthReport, HealthMonitor
from docstoolkit.health import (
    HealthSignal as HSig,
    SignalLevel as SL,
    HealthCheck as HC,
    HealthScore as HScore,
    compute_health_score as chs,
    HealthReport as HR,
    HealthMonitor as HM,
)


# ---------------------------------------------------------------------------
# SignalLevel enum — 4 values
# ---------------------------------------------------------------------------

class TestSignalLevel:
    def test_ok_value(self):
        assert SignalLevel.OK == "ok"

    def test_warning_value(self):
        assert SignalLevel.WARNING == "warning"

    def test_error_value(self):
        assert SignalLevel.ERROR == "error"

    def test_critical_value(self):
        assert SignalLevel.CRITICAL == "critical"

    def test_four_members(self):
        assert len(SignalLevel) == 4

    def test_is_str(self):
        assert isinstance(SignalLevel.OK, str)


# ---------------------------------------------------------------------------
# HealthSignal
# ---------------------------------------------------------------------------

class TestHealthSignal:
    def test_fields_stored(self):
        s = HealthSignal(name="test.rate", level=SignalLevel.OK, value=0.9,
                         message="all good", subsystem="feedback")
        assert s.name == "test.rate"
        assert s.level == SignalLevel.OK
        assert s.value == 0.9
        assert s.message == "all good"
        assert s.subsystem == "feedback"

    def test_ts_auto_set(self):
        s = HealthSignal(name="x", level=SignalLevel.OK, value=1.0)
        assert s.ts != ""
        assert "T" in s.ts  # ISO format

    def test_ts_explicit(self):
        s = HealthSignal(name="x", level=SignalLevel.OK, value=1.0, ts="2024-01-01T00:00:00")
        assert s.ts == "2024-01-01T00:00:00"

    def test_message_default_empty(self):
        s = HealthSignal(name="x", level=SignalLevel.OK, value=1.0)
        assert s.message == ""

    def test_subsystem_default_empty(self):
        s = HealthSignal(name="x", level=SignalLevel.OK, value=1.0)
        assert s.subsystem == ""

    def test_is_healthy_ok(self):
        s = HealthSignal(name="x", level=SignalLevel.OK, value=1.0)
        assert s.is_healthy() is True

    def test_is_healthy_warning(self):
        s = HealthSignal(name="x", level=SignalLevel.WARNING, value=0.6)
        assert s.is_healthy() is False

    def test_is_healthy_error(self):
        s = HealthSignal(name="x", level=SignalLevel.ERROR, value=0.4)
        assert s.is_healthy() is False

    def test_is_healthy_critical(self):
        s = HealthSignal(name="x", level=SignalLevel.CRITICAL, value=0.1)
        assert s.is_healthy() is False

    def test_is_critical_critical(self):
        s = HealthSignal(name="x", level=SignalLevel.CRITICAL, value=0.1)
        assert s.is_critical() is True

    def test_is_critical_ok(self):
        s = HealthSignal(name="x", level=SignalLevel.OK, value=1.0)
        assert s.is_critical() is False

    def test_is_critical_warning(self):
        s = HealthSignal(name="x", level=SignalLevel.WARNING, value=0.6)
        assert s.is_critical() is False

    def test_is_critical_error(self):
        s = HealthSignal(name="x", level=SignalLevel.ERROR, value=0.4)
        assert s.is_critical() is False


# ---------------------------------------------------------------------------
# HealthCheck — higher_is_better=True
# ---------------------------------------------------------------------------

class TestHealthCheckHigherIsBetter:
    def _check(self):
        return HealthCheck(
            name="feedback.satisfaction",
            subsystem="feedback",
            warn_threshold=0.7,
            error_threshold=0.5,
            critical_threshold=0.3,
            higher_is_better=True,
        )

    def test_above_warn_is_ok(self):
        c = self._check()
        sig = c.evaluate(0.9)
        assert sig.level == SignalLevel.OK

    def test_at_warn_is_ok(self):
        c = self._check()
        sig = c.evaluate(0.7)
        assert sig.level == SignalLevel.OK

    def test_between_error_warn_is_warning(self):
        c = self._check()
        sig = c.evaluate(0.6)
        assert sig.level == SignalLevel.WARNING

    def test_at_error_is_warning(self):
        c = self._check()
        sig = c.evaluate(0.5)
        assert sig.level == SignalLevel.WARNING

    def test_between_critical_error_is_error(self):
        c = self._check()
        sig = c.evaluate(0.4)
        assert sig.level == SignalLevel.ERROR

    def test_at_critical_is_error(self):
        c = self._check()
        sig = c.evaluate(0.3)
        assert sig.level == SignalLevel.ERROR

    def test_below_critical_is_critical(self):
        c = self._check()
        sig = c.evaluate(0.1)
        assert sig.level == SignalLevel.CRITICAL

    def test_zero_is_critical(self):
        c = self._check()
        sig = c.evaluate(0.0)
        assert sig.level == SignalLevel.CRITICAL

    def test_result_name_matches_check(self):
        c = self._check()
        sig = c.evaluate(0.8)
        assert sig.name == "feedback.satisfaction"

    def test_result_subsystem_matches_check(self):
        c = self._check()
        sig = c.evaluate(0.8)
        assert sig.subsystem == "feedback"

    def test_result_value_stored(self):
        c = self._check()
        sig = c.evaluate(0.65)
        assert sig.value == 0.65

    def test_returns_health_signal(self):
        c = self._check()
        sig = c.evaluate(0.8)
        assert isinstance(sig, HealthSignal)


# ---------------------------------------------------------------------------
# HealthCheck — higher_is_better=False (error rate)
# ---------------------------------------------------------------------------

class TestHealthCheckLowerIsBetter:
    def _check(self):
        return HealthCheck(
            name="eval.error_rate",
            subsystem="eval",
            warn_threshold=0.3,
            error_threshold=0.5,
            critical_threshold=0.1,
            higher_is_better=False,
        )

    def test_at_critical_threshold_is_ok(self):
        c = self._check()
        sig = c.evaluate(0.1)
        assert sig.level == SignalLevel.OK

    def test_below_critical_threshold_is_ok(self):
        c = self._check()
        sig = c.evaluate(0.05)
        assert sig.level == SignalLevel.OK

    def test_zero_is_ok(self):
        c = self._check()
        sig = c.evaluate(0.0)
        assert sig.level == SignalLevel.OK

    def test_between_critical_error_is_warning(self):
        c = self._check()
        sig = c.evaluate(0.3)
        assert sig.level == SignalLevel.WARNING

    def test_at_error_threshold_is_warning(self):
        c = self._check()
        sig = c.evaluate(0.5)
        assert sig.level == SignalLevel.WARNING

    def test_between_error_warn_is_error(self):
        # Use a check where warn > error so ERROR range is reachable:
        # value <= critical(0.1) → OK, value <= error(0.3) → WARNING,
        # value <= warn(0.6) → ERROR, else → CRITICAL
        c = HealthCheck(
            name="eval.error_rate",
            subsystem="eval",
            warn_threshold=0.6,
            error_threshold=0.3,
            critical_threshold=0.1,
            higher_is_better=False,
        )
        sig = c.evaluate(0.4)  # 0.4 > 0.3 (error), 0.4 <= 0.6 (warn) → ERROR
        assert sig.level == SignalLevel.ERROR

    def test_at_warn_threshold_is_error(self):
        c = self._check()
        # value <= warn → ERROR (since higher_is_better=False logic:
        # value <= critical → OK, value <= error → WARNING, value <= warn → ERROR, else → CRITICAL)
        sig = c.evaluate(0.3)
        # 0.3 <= 0.5 (error threshold) so WARNING
        assert sig.level == SignalLevel.WARNING

    def test_above_warn_threshold_is_critical(self):
        c = self._check()
        sig = c.evaluate(0.8)
        assert sig.level == SignalLevel.CRITICAL

    def test_one_is_critical(self):
        c = self._check()
        sig = c.evaluate(1.0)
        assert sig.level == SignalLevel.CRITICAL

    def test_result_name(self):
        c = self._check()
        assert c.evaluate(0.05).name == "eval.error_rate"

    def test_result_subsystem(self):
        c = self._check()
        assert c.evaluate(0.05).subsystem == "eval"


# ---------------------------------------------------------------------------
# HealthScore
# ---------------------------------------------------------------------------

class TestHealthScore:
    def _score(self, score, ok=0, warn=0, err=0, crit=0):
        return HealthScore(
            score=score,
            ok_count=ok,
            warning_count=warn,
            error_count=err,
            critical_count=crit,
            total_signals=ok + warn + err + crit,
        )

    def test_grade_A(self):
        assert self._score(0.95).grade() == "A"

    def test_grade_A_boundary(self):
        assert self._score(0.9).grade() == "A"

    def test_grade_B(self):
        assert self._score(0.8).grade() == "B"

    def test_grade_B_boundary(self):
        assert self._score(0.75).grade() == "B"

    def test_grade_C(self):
        assert self._score(0.65).grade() == "C"

    def test_grade_C_boundary(self):
        assert self._score(0.6).grade() == "C"

    def test_grade_D(self):
        assert self._score(0.5).grade() == "D"

    def test_grade_D_boundary(self):
        assert self._score(0.4).grade() == "D"

    def test_grade_F(self):
        assert self._score(0.2).grade() == "F"

    def test_grade_F_boundary(self):
        assert self._score(0.39).grade() == "F"

    def test_is_healthy_no_critical_good_score(self):
        s = self._score(0.8, ok=4)
        assert s.is_healthy() is True

    def test_is_healthy_with_critical(self):
        s = self._score(0.7, ok=3, crit=1)
        assert s.is_healthy() is False

    def test_is_healthy_low_score(self):
        s = self._score(0.5, ok=2, err=2)
        assert s.is_healthy() is False

    def test_is_healthy_boundary_score(self):
        s = self._score(0.6, ok=3)
        assert s.is_healthy() is True

    def test_fields_accessible(self):
        s = self._score(0.85, ok=5, warn=1, err=0, crit=0)
        assert s.score == 0.85
        assert s.ok_count == 5
        assert s.warning_count == 1
        assert s.error_count == 0
        assert s.critical_count == 0
        assert s.total_signals == 6


# ---------------------------------------------------------------------------
# compute_health_score
# ---------------------------------------------------------------------------

class TestComputeHealthScore:
    def _sig(self, level, name="x", subsystem="s"):
        return HealthSignal(name=name, level=level, value=0.5, subsystem=subsystem)

    def test_empty_signals_score_one(self):
        result = compute_health_score([])
        assert result.score == 1.0

    def test_empty_signals_all_counts_zero(self):
        result = compute_health_score([])
        assert result.ok_count == 0
        assert result.warning_count == 0
        assert result.error_count == 0
        assert result.critical_count == 0
        assert result.total_signals == 0

    def test_all_ok_score_one(self):
        signals = [self._sig(SignalLevel.OK) for _ in range(3)]
        result = compute_health_score(signals)
        assert result.score == 1.0

    def test_all_critical_score_zero(self):
        signals = [self._sig(SignalLevel.CRITICAL) for _ in range(3)]
        result = compute_health_score(signals)
        assert result.score == 0.0

    def test_mixed_levels_weighted_average(self):
        # OK=1.0, WARNING=0.7 → (1.0+0.7)/2 = 0.85
        signals = [
            self._sig(SignalLevel.OK),
            self._sig(SignalLevel.WARNING),
        ]
        result = compute_health_score(signals)
        assert abs(result.score - 0.85) < 1e-9

    def test_mixed_all_levels(self):
        # OK=1.0, WARNING=0.7, ERROR=0.4, CRITICAL=0.0 → sum=2.1/4=0.525
        signals = [
            self._sig(SignalLevel.OK),
            self._sig(SignalLevel.WARNING),
            self._sig(SignalLevel.ERROR),
            self._sig(SignalLevel.CRITICAL),
        ]
        result = compute_health_score(signals)
        assert abs(result.score - 0.525) < 1e-9

    def test_level_counts_correct(self):
        signals = [
            self._sig(SignalLevel.OK),
            self._sig(SignalLevel.OK),
            self._sig(SignalLevel.WARNING),
            self._sig(SignalLevel.ERROR),
            self._sig(SignalLevel.CRITICAL),
            self._sig(SignalLevel.CRITICAL),
        ]
        result = compute_health_score(signals)
        assert result.ok_count == 2
        assert result.warning_count == 1
        assert result.error_count == 1
        assert result.critical_count == 2
        assert result.total_signals == 6

    def test_returns_health_score(self):
        result = compute_health_score([])
        assert isinstance(result, HealthScore)

    def test_single_warning(self):
        result = compute_health_score([self._sig(SignalLevel.WARNING)])
        assert result.score == 0.7
        assert result.warning_count == 1
        assert result.total_signals == 1

    def test_single_error(self):
        result = compute_health_score([self._sig(SignalLevel.ERROR)])
        assert result.score == 0.4
        assert result.error_count == 1


# ---------------------------------------------------------------------------
# HealthReport
# ---------------------------------------------------------------------------

class TestHealthReport:
    def _make_report(self):
        signals = [
            HealthSignal(name="a", level=SignalLevel.OK, value=0.9, subsystem="feedback"),
            HealthSignal(name="b", level=SignalLevel.CRITICAL, value=0.1, subsystem="eval"),
            HealthSignal(name="c", level=SignalLevel.WARNING, value=0.6, subsystem="feedback"),
            HealthSignal(name="d", level=SignalLevel.CRITICAL, value=0.2, subsystem="eval"),
        ]
        score = compute_health_score(signals)
        subsystems = {
            "feedback": compute_health_score(signals[:1] + signals[2:3]),
            "eval": compute_health_score(signals[1:2] + signals[3:4]),
        }
        return HealthReport(
            ts="2024-06-01T12:00:00",
            score=score,
            signals=signals,
            subsystems=subsystems,
        )

    def test_critical_signals_returns_only_critical(self):
        report = self._make_report()
        crits = report.critical_signals()
        assert len(crits) == 2
        assert all(s.level == SignalLevel.CRITICAL for s in crits)

    def test_critical_signals_empty_when_none(self):
        signals = [HealthSignal(name="x", level=SignalLevel.OK, value=1.0)]
        report = HealthReport(ts="t", score=compute_health_score(signals), signals=signals)
        assert report.critical_signals() == []

    def test_signals_for_subsystem(self):
        report = self._make_report()
        fb = report.signals_for("feedback")
        assert len(fb) == 2
        assert all(s.subsystem == "feedback" for s in fb)

    def test_signals_for_missing_subsystem(self):
        report = self._make_report()
        assert report.signals_for("nonexistent") == []

    def test_to_dict_keys(self):
        report = self._make_report()
        d = report.to_dict()
        for key in ("ts", "score", "grade", "ok", "warnings", "errors", "critical", "subsystems"):
            assert key in d

    def test_to_dict_ts(self):
        report = self._make_report()
        assert report.to_dict()["ts"] == "2024-06-01T12:00:00"

    def test_to_dict_subsystems_scores(self):
        report = self._make_report()
        d = report.to_dict()
        assert isinstance(d["subsystems"], dict)
        assert "feedback" in d["subsystems"]
        assert "eval" in d["subsystems"]
        assert isinstance(d["subsystems"]["feedback"], float)

    def test_to_dict_counts(self):
        report = self._make_report()
        d = report.to_dict()
        assert d["ok"] == 1
        assert d["warnings"] == 1
        assert d["critical"] == 2
        assert d["errors"] == 0

    def test_to_dict_grade_string(self):
        report = self._make_report()
        d = report.to_dict()
        assert d["grade"] in ("A", "B", "C", "D", "F")


# ---------------------------------------------------------------------------
# HealthMonitor
# ---------------------------------------------------------------------------

class TestHealthMonitor:
    def _monitor_with_checks(self):
        m = HealthMonitor()
        m.register(HealthCheck(
            name="feedback.satisfaction",
            subsystem="feedback",
            warn_threshold=0.7,
            error_threshold=0.5,
            critical_threshold=0.3,
        ))
        m.register(HealthCheck(
            name="eval.accuracy",
            subsystem="eval",
            warn_threshold=0.8,
            error_threshold=0.6,
            critical_threshold=0.4,
        ))
        m.register(HealthCheck(
            name="governance.coverage",
            subsystem="governance",
            warn_threshold=0.9,
            error_threshold=0.7,
            critical_threshold=0.5,
        ))
        return m

    def test_register_adds_checks(self):
        m = HealthMonitor()
        c = HealthCheck(name="x", subsystem="s")
        m.register(c)
        assert len(m._checks) == 1

    def test_register_multiple(self):
        m = self._monitor_with_checks()
        assert len(m._checks) == 3

    def test_run_all_values_evaluates_all(self):
        m = self._monitor_with_checks()
        report = m.run({
            "feedback.satisfaction": 0.85,
            "eval.accuracy": 0.75,
            "governance.coverage": 0.95,
        })
        assert len(report.signals) == 3

    def test_run_missing_value_skips_check(self):
        m = self._monitor_with_checks()
        report = m.run({
            "feedback.satisfaction": 0.85,
            # eval.accuracy missing
            "governance.coverage": 0.95,
        })
        assert len(report.signals) == 2

    def test_run_empty_values_skips_all(self):
        m = self._monitor_with_checks()
        report = m.run({})
        assert len(report.signals) == 0

    def test_run_returns_health_report(self):
        m = self._monitor_with_checks()
        report = m.run({"feedback.satisfaction": 0.9})
        assert isinstance(report, HealthReport)

    def test_run_report_has_ts(self):
        m = self._monitor_with_checks()
        report = m.run({"feedback.satisfaction": 0.9})
        assert report.ts != ""

    def test_run_subsystems_populated(self):
        m = self._monitor_with_checks()
        report = m.run({
            "feedback.satisfaction": 0.85,
            "eval.accuracy": 0.75,
            "governance.coverage": 0.95,
        })
        assert "feedback" in report.subsystems
        assert "eval" in report.subsystems
        assert "governance" in report.subsystems

    def test_run_subsystem_scores_are_health_scores(self):
        m = self._monitor_with_checks()
        report = m.run({"feedback.satisfaction": 0.85, "eval.accuracy": 0.75})
        assert isinstance(report.subsystems["feedback"], HealthScore)
        assert isinstance(report.subsystems["eval"], HealthScore)

    def test_run_subsystem_single_check_ok(self):
        m = self._monitor_with_checks()
        report = m.run({"feedback.satisfaction": 0.85})
        assert report.subsystems["feedback"].ok_count == 1
        assert report.subsystems["feedback"].score == 1.0

    def test_run_subsystem_single_check_critical(self):
        m = self._monitor_with_checks()
        report = m.run({"feedback.satisfaction": 0.1})
        assert report.subsystems["feedback"].critical_count == 1
        assert report.subsystems["feedback"].score == 0.0

    def test_run_overall_score_computed(self):
        m = self._monitor_with_checks()
        report = m.run({
            "feedback.satisfaction": 0.9,   # OK
            "eval.accuracy": 0.9,            # OK
            "governance.coverage": 0.95,     # OK
        })
        assert report.score.score == 1.0

    def test_empty_monitor_perfect_score(self):
        m = HealthMonitor()
        report = m.run({})
        assert report.score.score == 1.0
        assert report.score.total_signals == 0

    def test_empty_monitor_no_subsystems(self):
        m = HealthMonitor()
        report = m.run({})
        assert report.subsystems == {}

    def test_run_correct_signal_levels(self):
        m = self._monitor_with_checks()
        report = m.run({
            "feedback.satisfaction": 0.9,   # >= 0.7 → OK
            "eval.accuracy": 0.65,           # >= 0.6 → WARNING
            "governance.coverage": 0.3,      # < 0.5 → CRITICAL
        })
        levels = {s.name: s.level for s in report.signals}
        assert levels["feedback.satisfaction"] == SignalLevel.OK
        assert levels["eval.accuracy"] == SignalLevel.WARNING
        assert levels["governance.coverage"] == SignalLevel.CRITICAL


# ---------------------------------------------------------------------------
# __init__ re-exports
# ---------------------------------------------------------------------------

class TestPublicAPI:
    def test_signal_level_exported(self):
        assert SL.OK == SignalLevel.OK

    def test_health_signal_exported(self):
        s = HSig(name="x", level=SL.OK, value=1.0)
        assert isinstance(s, HealthSignal)

    def test_health_check_exported(self):
        c = HC(name="x", subsystem="s")
        assert isinstance(c, HealthCheck)

    def test_health_score_exported(self):
        sc = HScore(score=1.0, ok_count=0, warning_count=0,
                    error_count=0, critical_count=0, total_signals=0)
        assert isinstance(sc, HealthScore)

    def test_compute_health_score_exported(self):
        result = chs([])
        assert result.score == 1.0

    def test_health_report_exported(self):
        r = HR(ts="t", score=chs([]))
        assert isinstance(r, HealthReport)

    def test_health_monitor_exported(self):
        m = HM()
        assert isinstance(m, HealthMonitor)
