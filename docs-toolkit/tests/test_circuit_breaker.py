"""Tests for the circuit_breaker module — 65+ tests."""
import time
import pytest

from docstoolkit.circuit_breaker import (
    CircuitState, CircuitStats,
    CircuitBreaker, CircuitBreakerConfig, CallResult,
    CircuitBreakerRegistry,
)


# ---------------------------------------------------------------------------
# CircuitState enum
# ---------------------------------------------------------------------------

class TestCircuitState:
    def test_closed_value(self):
        assert CircuitState.CLOSED == "closed"

    def test_open_value(self):
        assert CircuitState.OPEN == "open"

    def test_half_open_value(self):
        assert CircuitState.HALF_OPEN == "half_open"

    def test_three_members(self):
        assert len(CircuitState) == 3

    def test_is_str_enum(self):
        assert isinstance(CircuitState.CLOSED, str)


# ---------------------------------------------------------------------------
# CircuitStats
# ---------------------------------------------------------------------------

class TestCircuitStats:
    def test_defaults_zero(self):
        s = CircuitStats()
        assert s.total_calls == 0
        assert s.success_count == 0
        assert s.failure_count == 0
        assert s.rejected_count == 0
        assert s.last_failure_ts == ""
        assert s.last_success_ts == ""

    def test_failure_rate_no_calls(self):
        s = CircuitStats()
        assert s.failure_rate() == 0.0

    def test_failure_rate_all_success(self):
        s = CircuitStats()
        s.record_success()
        s.record_success()
        assert s.failure_rate() == 0.0

    def test_failure_rate_all_failures(self):
        s = CircuitStats()
        s.record_failure()
        s.record_failure()
        assert s.failure_rate() == 1.0

    def test_failure_rate_mixed(self):
        s = CircuitStats()
        s.record_success()
        s.record_failure()
        assert s.failure_rate() == pytest.approx(0.5)

    def test_failure_rate_excludes_rejected(self):
        # rejected calls do not count toward failure_rate denominator
        s = CircuitStats()
        s.record_success()
        s.record_rejected()
        assert s.failure_rate() == 0.0

    def test_record_success_increments(self):
        s = CircuitStats()
        s.record_success()
        assert s.total_calls == 1
        assert s.success_count == 1
        assert s.failure_count == 0

    def test_record_failure_increments(self):
        s = CircuitStats()
        s.record_failure()
        assert s.total_calls == 1
        assert s.failure_count == 1
        assert s.success_count == 0

    def test_record_rejected_increments(self):
        s = CircuitStats()
        s.record_rejected()
        assert s.total_calls == 1
        assert s.rejected_count == 1

    def test_last_success_ts_set(self):
        s = CircuitStats()
        assert s.last_success_ts == ""
        s.record_success()
        assert s.last_success_ts != ""

    def test_last_failure_ts_set(self):
        s = CircuitStats()
        assert s.last_failure_ts == ""
        s.record_failure()
        assert s.last_failure_ts != ""

    def test_reset_clears_all(self):
        s = CircuitStats()
        s.record_success()
        s.record_failure()
        s.record_rejected()
        s.reset()
        assert s.total_calls == 0
        assert s.success_count == 0
        assert s.failure_count == 0
        assert s.rejected_count == 0
        assert s.last_success_ts == ""
        assert s.last_failure_ts == ""

    def test_multiple_records_accumulate(self):
        s = CircuitStats()
        for _ in range(3):
            s.record_success()
        for _ in range(2):
            s.record_failure()
        assert s.total_calls == 5
        assert s.success_count == 3
        assert s.failure_count == 2


# ---------------------------------------------------------------------------
# CircuitBreakerConfig defaults
# ---------------------------------------------------------------------------

class TestCircuitBreakerConfig:
    def test_default_failure_threshold(self):
        cfg = CircuitBreakerConfig()
        assert cfg.failure_threshold == 5

    def test_default_success_threshold(self):
        cfg = CircuitBreakerConfig()
        assert cfg.success_threshold == 2

    def test_default_timeout_seconds(self):
        cfg = CircuitBreakerConfig()
        assert cfg.timeout_seconds == 30.0

    def test_default_max_half_open_calls(self):
        cfg = CircuitBreakerConfig()
        assert cfg.max_half_open_calls == 1

    def test_custom_values(self):
        cfg = CircuitBreakerConfig(failure_threshold=3, success_threshold=1,
                                   timeout_seconds=10.0, max_half_open_calls=2)
        assert cfg.failure_threshold == 3
        assert cfg.success_threshold == 1
        assert cfg.timeout_seconds == 10.0
        assert cfg.max_half_open_calls == 2


# ---------------------------------------------------------------------------
# CallResult
# ---------------------------------------------------------------------------

class TestCallResult:
    def test_success_fields(self):
        r = CallResult(success=True, result=42)
        assert r.success is True
        assert r.result == 42
        assert r.error == ""
        assert r.rejected is False

    def test_failure_fields(self):
        r = CallResult(success=False, error="boom")
        assert r.success is False
        assert r.error == "boom"
        assert r.result is None

    def test_rejected_default_false(self):
        r = CallResult(success=True)
        assert r.rejected is False

    def test_rejected_can_be_set(self):
        r = CallResult(success=False, rejected=True, error="Circuit is OPEN")
        assert r.rejected is True

    def test_state_after_default(self):
        r = CallResult(success=True)
        assert r.state_after == CircuitState.CLOSED


# ---------------------------------------------------------------------------
# CircuitBreaker — core behaviour
# ---------------------------------------------------------------------------

def _fail():
    raise ValueError("deliberate failure")

def _ok():
    return "ok"

def _ok_val(v):
    return v


class TestCircuitBreakerBasics:
    def test_initial_state_closed(self):
        cb = CircuitBreaker("svc")
        assert cb.state == CircuitState.CLOSED

    def test_name_stored(self):
        cb = CircuitBreaker("my-service")
        assert cb.name == "my-service"

    def test_successful_call_returns_success(self):
        cb = CircuitBreaker("svc")
        res = cb.call(_ok)
        assert res.success is True
        assert res.result == "ok"
        assert res.rejected is False

    def test_successful_call_with_args(self):
        cb = CircuitBreaker("svc")
        res = cb.call(_ok_val, 99)
        assert res.result == 99

    def test_successful_call_increments_stats(self):
        cb = CircuitBreaker("svc")
        cb.call(_ok)
        assert cb.stats.success_count == 1

    def test_exception_returns_failure(self):
        cb = CircuitBreaker("svc")
        res = cb.call(_fail)
        assert res.success is False
        assert "deliberate failure" in res.error

    def test_exception_increments_failure_count(self):
        cb = CircuitBreaker("svc")
        cb.call(_fail)
        assert cb.stats.failure_count == 1

    def test_state_after_is_current_state(self):
        cb = CircuitBreaker("svc")
        res = cb.call(_ok)
        assert res.state_after == CircuitState.CLOSED


class TestCircuitBreakerOpening:
    def _cb(self, threshold=3):
        return CircuitBreaker("svc", CircuitBreakerConfig(failure_threshold=threshold,
                                                          timeout_seconds=60.0))

    def test_opens_after_threshold_failures(self):
        cb = self._cb(3)
        for _ in range(3):
            cb.call(_fail)
        assert cb.state == CircuitState.OPEN

    def test_does_not_open_before_threshold(self):
        cb = self._cb(3)
        for _ in range(2):
            cb.call(_fail)
        assert cb.state == CircuitState.CLOSED

    def test_open_call_returns_rejected(self):
        cb = self._cb(1)
        cb.call(_fail)
        assert cb.state == CircuitState.OPEN
        res = cb.call(_ok)
        assert res.rejected is True
        assert res.success is False

    def test_open_call_increments_rejected_count(self):
        cb = self._cb(1)
        cb.call(_fail)
        cb.call(_ok)  # rejected
        assert cb.stats.rejected_count == 1

    def test_open_call_does_not_execute_fn(self):
        calls = []
        cb = self._cb(1)
        cb.call(_fail)
        cb.call(lambda: calls.append(1))
        assert calls == []

    def test_state_after_on_open_rejection(self):
        cb = self._cb(1)
        cb.call(_fail)
        res = cb.call(_ok)
        assert res.state_after == CircuitState.OPEN


class TestCircuitBreakerForce:
    def test_force_open(self):
        cb = CircuitBreaker("svc")
        cb.force_open()
        assert cb.state == CircuitState.OPEN

    def test_force_close(self):
        cb = CircuitBreaker("svc")
        cb.force_open()
        cb.force_close()
        assert cb.state == CircuitState.CLOSED

    def test_force_close_resets_stats(self):
        cb = CircuitBreaker("svc", CircuitBreakerConfig(failure_threshold=2))
        cb.call(_fail)
        cb.call(_fail)
        assert cb.stats.failure_count == 2
        cb.force_close()
        assert cb.stats.failure_count == 0

    def test_force_close_allows_calls(self):
        cb = CircuitBreaker("svc", CircuitBreakerConfig(failure_threshold=1))
        cb.call(_fail)
        assert cb.state == CircuitState.OPEN
        cb.force_close()
        res = cb.call(_ok)
        assert res.success is True


# ---------------------------------------------------------------------------
# CircuitBreaker — HALF_OPEN behaviour
# ---------------------------------------------------------------------------

class TestCircuitBreakerHalfOpen:
    def _open_cb(self, failure_threshold=1, success_threshold=2,
                 max_half_open_calls=1):
        cfg = CircuitBreakerConfig(failure_threshold=failure_threshold,
                                   success_threshold=success_threshold,
                                   timeout_seconds=60.0,
                                   max_half_open_calls=max_half_open_calls)
        cb = CircuitBreaker("svc", cfg)
        # Force into HALF_OPEN directly
        cb._state = CircuitState.HALF_OPEN
        cb._half_open_successes = 0
        cb._half_open_calls = 0
        return cb

    def test_half_open_allows_probe(self):
        cb = self._open_cb()
        res = cb.call(_ok)
        assert res.success is True
        assert res.rejected is False

    def test_half_open_success_increments_counter(self):
        cb = self._open_cb()
        cb.call(_ok)
        assert cb._half_open_successes == 1

    def test_half_open_closes_after_success_threshold(self):
        cb = self._open_cb(success_threshold=2, max_half_open_calls=2)
        cb.call(_ok)
        assert cb._state == CircuitState.HALF_OPEN  # still half-open after 1
        cb.call(_ok)
        assert cb.state == CircuitState.CLOSED

    def test_half_open_stats_reset_on_close(self):
        cb = self._open_cb(success_threshold=1)
        # Add some stats first
        cb._stats.record_failure()
        cb.call(_ok)
        assert cb.state == CircuitState.CLOSED
        # After close, stats are reset
        assert cb.stats.failure_count == 0

    def test_half_open_failure_reopens(self):
        cb = self._open_cb(failure_threshold=1)
        cb.call(_fail)
        assert cb.state == CircuitState.OPEN

    def test_half_open_max_probes_reached_rejects(self):
        cb = self._open_cb(max_half_open_calls=1)
        # first probe is allowed (will succeed but state stays HALF_OPEN with threshold=2)
        cfg = CircuitBreakerConfig(failure_threshold=1, success_threshold=2,
                                   timeout_seconds=60.0, max_half_open_calls=1)
        cb2 = CircuitBreaker("svc2", cfg)
        cb2._state = CircuitState.HALF_OPEN
        cb2._half_open_calls = 1  # already at max
        res = cb2.call(_ok)
        assert res.rejected is True
        assert res.state_after == CircuitState.HALF_OPEN

    def test_timeout_transitions_open_to_half_open(self):
        cfg = CircuitBreakerConfig(failure_threshold=1, timeout_seconds=0.01)
        cb = CircuitBreaker("svc", cfg)
        cb.call(_fail)
        assert cb._state == CircuitState.OPEN
        time.sleep(0.05)
        # accessing .state triggers _check_timeout
        assert cb.state == CircuitState.HALF_OPEN

    def test_no_transition_before_timeout(self):
        cfg = CircuitBreakerConfig(failure_threshold=1, timeout_seconds=60.0)
        cb = CircuitBreaker("svc", cfg)
        cb.call(_fail)
        assert cb.state == CircuitState.OPEN  # timeout not elapsed


# ---------------------------------------------------------------------------
# CircuitBreaker — stats failure_rate
# ---------------------------------------------------------------------------

class TestCircuitBreakerStatsIntegration:
    def test_failure_rate_after_calls(self):
        cb = CircuitBreaker("svc", CircuitBreakerConfig(failure_threshold=10))
        cb.call(_ok)
        cb.call(_ok)
        cb.call(_fail)
        # 2 success, 1 failure → rate = 1/3
        assert cb.stats.failure_rate() == pytest.approx(1 / 3)

    def test_rejected_count_on_open(self):
        cb = CircuitBreaker("svc", CircuitBreakerConfig(failure_threshold=1))
        cb.call(_fail)
        cb.call(_ok)  # rejected
        cb.call(_ok)  # rejected
        assert cb.stats.rejected_count == 2


# ---------------------------------------------------------------------------
# CircuitBreakerRegistry
# ---------------------------------------------------------------------------

class TestCircuitBreakerRegistry:
    def test_get_or_create_returns_breaker(self):
        reg = CircuitBreakerRegistry()
        b = reg.get_or_create("svc-a")
        assert isinstance(b, CircuitBreaker)
        assert b.name == "svc-a"

    def test_get_or_create_same_instance(self):
        reg = CircuitBreakerRegistry()
        b1 = reg.get_or_create("svc-a")
        b2 = reg.get_or_create("svc-a")
        assert b1 is b2

    def test_get_missing_returns_none(self):
        reg = CircuitBreakerRegistry()
        assert reg.get("nonexistent") is None

    def test_get_existing(self):
        reg = CircuitBreakerRegistry()
        b = reg.get_or_create("svc-a")
        assert reg.get("svc-a") is b

    def test_list_names_sorted(self):
        reg = CircuitBreakerRegistry()
        reg.get_or_create("zebra")
        reg.get_or_create("alpha")
        reg.get_or_create("mango")
        assert reg.list_names() == ["alpha", "mango", "zebra"]

    def test_list_names_empty(self):
        reg = CircuitBreakerRegistry()
        assert reg.list_names() == []

    def test_open_circuits_empty_when_all_closed(self):
        reg = CircuitBreakerRegistry()
        reg.get_or_create("a")
        reg.get_or_create("b")
        assert reg.open_circuits() == []

    def test_open_circuits_after_force_open(self):
        reg = CircuitBreakerRegistry()
        reg.get_or_create("a").force_open()
        reg.get_or_create("b")
        assert "a" in reg.open_circuits()
        assert "b" not in reg.open_circuits()

    def test_health_summary_all_closed(self):
        reg = CircuitBreakerRegistry()
        reg.get_or_create("x")
        reg.get_or_create("y")
        summary = reg.health_summary()
        assert summary == {"x": "closed", "y": "closed"}

    def test_health_summary_mixed_states(self):
        reg = CircuitBreakerRegistry()
        reg.get_or_create("ok")
        reg.get_or_create("broken").force_open()
        summary = reg.health_summary()
        assert summary["ok"] == "closed"
        assert summary["broken"] == "open"

    def test_reset_all_closes_open_circuits(self):
        reg = CircuitBreakerRegistry()
        reg.get_or_create("a").force_open()
        reg.get_or_create("b").force_open()
        reg.reset_all()
        assert reg.get("a").state == CircuitState.CLOSED
        assert reg.get("b").state == CircuitState.CLOSED

    def test_reset_all_empty_registry(self):
        reg = CircuitBreakerRegistry()
        reg.reset_all()  # should not raise

    def test_default_config_applied_to_new_breakers(self):
        cfg = CircuitBreakerConfig(failure_threshold=99)
        reg = CircuitBreakerRegistry(default_config=cfg)
        b = reg.get_or_create("svc")
        assert b._config.failure_threshold == 99

    def test_multiple_breakers_independent(self):
        reg = CircuitBreakerRegistry(
            default_config=CircuitBreakerConfig(failure_threshold=1)
        )
        a = reg.get_or_create("a")
        b = reg.get_or_create("b")
        a.call(_fail)
        assert a.state == CircuitState.OPEN
        assert b.state == CircuitState.CLOSED
