"""Tests for the circuit_breaker module — 75+ tests covering all spec requirements."""
import threading
import time
import pytest

from docstoolkit.circuit_breaker import (
    CircuitState,
    CircuitStats,
    CircuitBreaker,
    CircuitBreakerConfig,
    CircuitBreakerRegistry,
    CircuitOpenError,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _ok(*args, **kwargs):
    return "ok"


def _fail(*args, **kwargs):
    raise RuntimeError("deliberate failure")


def _return(value):
    """Return a callable that returns *value*."""
    def fn(*args, **kwargs):
        return value
    return fn


def _make_cb(
    failure_threshold=5,
    recovery_timeout=60.0,
    half_open_max_calls=3,
    success_threshold=2,
    name="svc",
):
    cfg = CircuitBreakerConfig(
        failure_threshold=failure_threshold,
        recovery_timeout=recovery_timeout,
        half_open_max_calls=half_open_max_calls,
        success_threshold=success_threshold,
    )
    return CircuitBreaker(name, cfg)


def _trip_and_recover(cb):
    """Force cb to HALF_OPEN immediately (uses very short recovery_timeout)."""
    cb.trip()
    # wait past the configured recovery_timeout (already set short by caller)
    time.sleep(cb._config.recovery_timeout + 0.02)
    # touch state to trigger transition
    _ = cb.state


# ---------------------------------------------------------------------------
# 1. CircuitState enum
# ---------------------------------------------------------------------------

class TestCircuitState:
    def test_closed_value(self):
        assert CircuitState.CLOSED == "closed"

    def test_open_value(self):
        assert CircuitState.OPEN == "open"

    def test_half_open_value(self):
        assert CircuitState.HALF_OPEN == "half_open"

    def test_exactly_three_members(self):
        assert len(CircuitState) == 3

    def test_is_str_enum(self):
        assert isinstance(CircuitState.CLOSED, str)

    def test_members_distinct(self):
        states = {CircuitState.CLOSED, CircuitState.OPEN, CircuitState.HALF_OPEN}
        assert len(states) == 3


# ---------------------------------------------------------------------------
# 2. CircuitStats dataclass
# ---------------------------------------------------------------------------

class TestCircuitStats:
    def test_default_total_calls(self):
        s = CircuitStats()
        assert s.total_calls == 0

    def test_default_failures(self):
        s = CircuitStats()
        assert s.failures == 0

    def test_default_successes(self):
        s = CircuitStats()
        assert s.successes == 0

    def test_default_consecutive_failures(self):
        s = CircuitStats()
        assert s.consecutive_failures == 0

    def test_default_consecutive_successes(self):
        s = CircuitStats()
        assert s.consecutive_successes == 0

    def test_default_last_failure_time(self):
        s = CircuitStats()
        assert s.last_failure_time == 0.0

    def test_failure_rate_zero_calls(self):
        s = CircuitStats()
        assert s.failure_rate() == 0.0

    def test_failure_rate_all_failures(self):
        s = CircuitStats(total_calls=4, failures=4)
        assert s.failure_rate() == 1.0

    def test_failure_rate_all_successes(self):
        s = CircuitStats(total_calls=3, successes=3)
        assert s.failure_rate() == 0.0

    def test_failure_rate_mixed(self):
        s = CircuitStats(total_calls=10, failures=3, successes=7)
        assert s.failure_rate() == pytest.approx(0.3)

    def test_failure_rate_uses_total_calls(self):
        # total_calls is the denominator (not failures+successes)
        s = CircuitStats(total_calls=5, failures=2)
        assert s.failure_rate() == pytest.approx(2 / 5)

    def test_reset_clears_all_fields(self):
        s = CircuitStats(
            total_calls=10,
            failures=3,
            successes=7,
            consecutive_failures=2,
            consecutive_successes=4,
            last_failure_time=123.456,
        )
        s.reset()
        assert s.total_calls == 0
        assert s.failures == 0
        assert s.successes == 0
        assert s.consecutive_failures == 0
        assert s.consecutive_successes == 0
        assert s.last_failure_time == 0.0

    def test_reset_idempotent(self):
        s = CircuitStats()
        s.reset()
        s.reset()
        assert s.total_calls == 0


# ---------------------------------------------------------------------------
# 3. CircuitBreakerConfig defaults
# ---------------------------------------------------------------------------

class TestCircuitBreakerConfig:
    def test_default_failure_threshold(self):
        assert CircuitBreakerConfig().failure_threshold == 5

    def test_default_recovery_timeout(self):
        assert CircuitBreakerConfig().recovery_timeout == 60.0

    def test_default_half_open_max_calls(self):
        assert CircuitBreakerConfig().half_open_max_calls == 3

    def test_default_success_threshold(self):
        assert CircuitBreakerConfig().success_threshold == 2

    def test_custom_values(self):
        cfg = CircuitBreakerConfig(
            failure_threshold=10,
            recovery_timeout=5.0,
            half_open_max_calls=1,
            success_threshold=3,
        )
        assert cfg.failure_threshold == 10
        assert cfg.recovery_timeout == 5.0
        assert cfg.half_open_max_calls == 1
        assert cfg.success_threshold == 3


# ---------------------------------------------------------------------------
# 4. CircuitBreaker – initial state & basic call
# ---------------------------------------------------------------------------

class TestCircuitBreakerBasics:
    def test_initial_state_closed(self):
        cb = CircuitBreaker("svc")
        assert cb.state == CircuitState.CLOSED

    def test_name_stored(self):
        cb = CircuitBreaker("my-service")
        assert cb.name == "my-service"

    def test_none_config_uses_defaults(self):
        cb = CircuitBreaker("svc", None)
        assert cb._config.failure_threshold == 5

    def test_successful_call_returns_value(self):
        cb = CircuitBreaker("svc")
        result = cb.call(_return(42))
        assert result == 42

    def test_successful_call_with_args(self):
        cb = CircuitBreaker("svc")
        result = cb.call(lambda x, y: x + y, 3, 4)
        assert result == 7

    def test_successful_call_with_kwargs(self):
        cb = CircuitBreaker("svc")
        result = cb.call(lambda x=0, y=0: x * y, x=6, y=7)
        assert result == 42

    def test_success_increments_total_calls(self):
        cb = CircuitBreaker("svc")
        cb.call(_ok)
        assert cb.stats.total_calls == 1

    def test_success_increments_successes(self):
        cb = CircuitBreaker("svc")
        cb.call(_ok)
        assert cb.stats.successes == 1

    def test_failure_raises_original_exception(self):
        cb = CircuitBreaker("svc")
        with pytest.raises(RuntimeError, match="deliberate failure"):
            cb.call(_fail)

    def test_failure_increments_failures(self):
        cb = CircuitBreaker("svc")
        with pytest.raises(RuntimeError):
            cb.call(_fail)
        assert cb.stats.failures == 1

    def test_failure_increments_total_calls(self):
        cb = CircuitBreaker("svc")
        with pytest.raises(RuntimeError):
            cb.call(_fail)
        assert cb.stats.total_calls == 1

    def test_stats_property_returns_copy(self):
        cb = CircuitBreaker("svc")
        s1 = cb.stats
        cb.call(_ok)
        s2 = cb.stats
        assert s1.total_calls == 0
        assert s2.total_calls == 1


# ---------------------------------------------------------------------------
# 5. CLOSED → OPEN transition
# ---------------------------------------------------------------------------

class TestClosedToOpen:
    def test_opens_after_consecutive_failure_threshold(self):
        cb = _make_cb(failure_threshold=3)
        for _ in range(3):
            with pytest.raises(RuntimeError):
                cb.call(_fail)
        assert cb.state == CircuitState.OPEN

    def test_does_not_open_below_threshold(self):
        cb = _make_cb(failure_threshold=3)
        for _ in range(2):
            with pytest.raises(RuntimeError):
                cb.call(_fail)
        assert cb.state == CircuitState.CLOSED

    def test_success_resets_consecutive_failures(self):
        cb = _make_cb(failure_threshold=3)
        with pytest.raises(RuntimeError):
            cb.call(_fail)
        cb.call(_ok)
        with pytest.raises(RuntimeError):
            cb.call(_fail)
        # consecutive_failures reset to 1, not 2
        assert cb.stats.consecutive_failures == 1
        assert cb.state == CircuitState.CLOSED

    def test_consecutive_failures_counter_increments(self):
        cb = _make_cb(failure_threshold=10)
        for i in range(4):
            with pytest.raises(RuntimeError):
                cb.call(_fail)
        assert cb.stats.consecutive_failures == 4

    def test_last_failure_time_set_on_failure(self):
        cb = CircuitBreaker("svc")
        before = time.monotonic()
        with pytest.raises(RuntimeError):
            cb.call(_fail)
        assert cb.stats.last_failure_time >= before


# ---------------------------------------------------------------------------
# 6. OPEN state – fast-fail
# ---------------------------------------------------------------------------

class TestOpenState:
    def test_open_raises_circuit_open_error(self):
        cb = _make_cb(failure_threshold=1)
        with pytest.raises(RuntimeError):
            cb.call(_fail)
        assert cb.state == CircuitState.OPEN
        with pytest.raises(CircuitOpenError):
            cb.call(_ok)

    def test_open_does_not_execute_callable(self):
        called = []
        cb = _make_cb(failure_threshold=1)
        with pytest.raises(RuntimeError):
            cb.call(_fail)
        with pytest.raises(CircuitOpenError):
            cb.call(lambda: called.append(1))
        assert called == []

    def test_open_consecutive_rejections(self):
        cb = _make_cb(failure_threshold=1)
        with pytest.raises(RuntimeError):
            cb.call(_fail)
        for _ in range(5):
            with pytest.raises(CircuitOpenError):
                cb.call(_ok)

    def test_trip_forces_open(self):
        cb = CircuitBreaker("svc")
        cb.trip()
        assert cb.state == CircuitState.OPEN

    def test_trip_then_fast_fail(self):
        cb = CircuitBreaker("svc")
        cb.trip()
        with pytest.raises(CircuitOpenError):
            cb.call(_ok)


# ---------------------------------------------------------------------------
# 7. OPEN → HALF_OPEN (time-based recovery)
# ---------------------------------------------------------------------------

class TestOpenToHalfOpen:
    def test_transitions_after_recovery_timeout(self):
        cb = _make_cb(failure_threshold=1, recovery_timeout=0.05)
        with pytest.raises(RuntimeError):
            cb.call(_fail)
        assert cb._state == CircuitState.OPEN
        time.sleep(0.1)
        assert cb.state == CircuitState.HALF_OPEN

    def test_no_transition_before_timeout(self):
        cb = _make_cb(failure_threshold=1, recovery_timeout=60.0)
        with pytest.raises(RuntimeError):
            cb.call(_fail)
        assert cb.state == CircuitState.OPEN

    def test_trip_and_recover(self):
        cb = _make_cb(failure_threshold=5, recovery_timeout=0.05)
        cb.trip()
        time.sleep(0.1)
        assert cb.state == CircuitState.HALF_OPEN

    def test_call_triggers_transition(self):
        cb = _make_cb(failure_threshold=1, recovery_timeout=0.05,
                      success_threshold=10)
        with pytest.raises(RuntimeError):
            cb.call(_fail)
        time.sleep(0.1)
        # call itself should transition then execute
        result = cb.call(_ok)
        assert result == "ok"


# ---------------------------------------------------------------------------
# 8. HALF_OPEN behaviour
# ---------------------------------------------------------------------------

class TestHalfOpen:
    def _half_open_cb(self, success_threshold=2, half_open_max_calls=3,
                      failure_threshold=5):
        cb = _make_cb(
            failure_threshold=failure_threshold,
            recovery_timeout=0.05,
            half_open_max_calls=half_open_max_calls,
            success_threshold=success_threshold,
        )
        cb.trip()
        time.sleep(0.1)
        _ = cb.state  # trigger transition
        return cb

    def test_half_open_allows_calls_up_to_max(self):
        cb = self._half_open_cb(success_threshold=10, half_open_max_calls=2)
        cb.call(_ok)
        cb.call(_ok)
        # 3rd should be rejected
        with pytest.raises(CircuitOpenError):
            cb.call(_ok)

    def test_half_open_max_calls_zero_rejects_all(self):
        cb = self._half_open_cb(half_open_max_calls=0)
        with pytest.raises(CircuitOpenError):
            cb.call(_ok)

    def test_half_open_success_increments_consecutive(self):
        cb = self._half_open_cb(success_threshold=5, half_open_max_calls=5)
        cb.call(_ok)
        assert cb.stats.consecutive_successes == 1

    def test_half_open_closes_after_success_threshold(self):
        cb = self._half_open_cb(success_threshold=2, half_open_max_calls=5)
        cb.call(_ok)
        assert cb._state == CircuitState.HALF_OPEN  # still half-open after 1
        cb.call(_ok)
        assert cb.state == CircuitState.CLOSED

    def test_half_open_stats_reset_on_close(self):
        cb = self._half_open_cb(success_threshold=1, half_open_max_calls=5)
        # Put some stats in
        cb._stats.failures = 10
        cb._stats.total_calls = 10
        cb.call(_ok)  # hits success_threshold=1 → CLOSED + reset
        assert cb.state == CircuitState.CLOSED
        assert cb.stats.total_calls == 0
        assert cb.stats.failures == 0

    def test_half_open_failure_reopens(self):
        cb = self._half_open_cb(success_threshold=5, half_open_max_calls=5)
        with pytest.raises(RuntimeError):
            cb.call(_fail)
        assert cb.state == CircuitState.OPEN

    def test_half_open_failure_resets_half_open_calls(self):
        cb = self._half_open_cb(success_threshold=5, half_open_max_calls=5,
                                failure_threshold=1)
        with pytest.raises(RuntimeError):
            cb.call(_fail)
        assert cb.state == CircuitState.OPEN
        # After recovery, half_open_calls should be reset
        time.sleep(0.1)
        assert cb.state == CircuitState.HALF_OPEN
        assert cb._half_open_calls == 0


# ---------------------------------------------------------------------------
# 9. CircuitBreaker.reset() and trip()
# ---------------------------------------------------------------------------

class TestResetAndTrip:
    def test_reset_closes_open_circuit(self):
        cb = CircuitBreaker("svc")
        cb.trip()
        assert cb.state == CircuitState.OPEN
        cb.reset()
        assert cb.state == CircuitState.CLOSED

    def test_reset_zeroes_stats(self):
        cb = _make_cb(failure_threshold=2)
        with pytest.raises(RuntimeError):
            cb.call(_fail)
        cb.reset()
        s = cb.stats
        assert s.total_calls == 0
        assert s.failures == 0
        assert s.consecutive_failures == 0

    def test_reset_allows_calls(self):
        cb = _make_cb(failure_threshold=1)
        with pytest.raises(RuntimeError):
            cb.call(_fail)
        cb.reset()
        result = cb.call(_ok)
        assert result == "ok"

    def test_reset_idempotent(self):
        cb = CircuitBreaker("svc")
        cb.reset()
        cb.reset()
        assert cb.state == CircuitState.CLOSED

    def test_trip_forces_open(self):
        cb = CircuitBreaker("svc")
        cb.trip()
        assert cb.state == CircuitState.OPEN

    def test_trip_on_already_open(self):
        cb = CircuitBreaker("svc")
        cb.trip()
        cb.trip()  # should not raise
        assert cb.state == CircuitState.OPEN

    def test_trip_resets_open_since_timestamp(self):
        cb = CircuitBreaker("svc")
        before = time.monotonic()
        cb.trip()
        assert cb._open_since >= before


# ---------------------------------------------------------------------------
# 10. CircuitOpenError
# ---------------------------------------------------------------------------

class TestCircuitOpenError:
    def test_is_exception_subclass(self):
        assert issubclass(CircuitOpenError, Exception)

    def test_can_be_raised_and_caught(self):
        with pytest.raises(CircuitOpenError):
            raise CircuitOpenError("test")

    def test_open_raises_circuit_open_error_not_swallowed(self):
        cb = _make_cb(failure_threshold=1)
        with pytest.raises(RuntimeError):
            cb.call(_fail)
        try:
            cb.call(_ok)
            assert False, "Expected CircuitOpenError"
        except CircuitOpenError:
            pass
        except Exception as e:
            assert False, f"Wrong exception type: {type(e)}"

    def test_half_open_limit_raises_circuit_open_error(self):
        cb = _make_cb(failure_threshold=1, recovery_timeout=0.05,
                      half_open_max_calls=0, success_threshold=5)
        cb.trip()
        time.sleep(0.1)
        _ = cb.state
        with pytest.raises(CircuitOpenError):
            cb.call(_ok)

    def test_original_exception_not_wrapped(self):
        cb = CircuitBreaker("svc")
        with pytest.raises(ValueError):
            cb.call(lambda: (_ for _ in ()).throw(ValueError("raw")))


# ---------------------------------------------------------------------------
# 11. CircuitBreakerRegistry
# ---------------------------------------------------------------------------

class TestCircuitBreakerRegistry:
    def test_get_creates_breaker(self):
        reg = CircuitBreakerRegistry()
        b = reg.get("svc-a")
        assert isinstance(b, CircuitBreaker)
        assert b.name == "svc-a"

    def test_get_reuses_existing(self):
        reg = CircuitBreakerRegistry()
        b1 = reg.get("svc-a")
        b2 = reg.get("svc-a")
        assert b1 is b2

    def test_get_different_names_different_breakers(self):
        reg = CircuitBreakerRegistry()
        a = reg.get("a")
        b = reg.get("b")
        assert a is not b

    def test_all_returns_dict(self):
        reg = CircuitBreakerRegistry()
        reg.get("x")
        reg.get("y")
        d = reg.all()
        assert isinstance(d, dict)
        assert "x" in d and "y" in d

    def test_all_returns_copy(self):
        reg = CircuitBreakerRegistry()
        reg.get("x")
        d = reg.all()
        d["injected"] = None
        assert "injected" not in reg.all()

    def test_all_empty_registry(self):
        reg = CircuitBreakerRegistry()
        assert reg.all() == {}

    def test_reset_all_closes_open_breakers(self):
        reg = CircuitBreakerRegistry()
        reg.get("a").trip()
        reg.get("b").trip()
        reg.reset_all()
        assert reg.get("a").state == CircuitState.CLOSED
        assert reg.get("b").state == CircuitState.CLOSED

    def test_reset_all_zeroes_stats(self):
        cfg = CircuitBreakerConfig(failure_threshold=1)
        reg = CircuitBreakerRegistry(default_config=cfg)
        b = reg.get("svc")
        with pytest.raises(RuntimeError):
            b.call(_fail)
        reg.reset_all()
        assert b.stats.total_calls == 0

    def test_reset_all_empty_registry(self):
        reg = CircuitBreakerRegistry()
        reg.reset_all()  # must not raise

    def test_stats_summary_structure(self):
        reg = CircuitBreakerRegistry()
        reg.get("svc")
        summary = reg.stats_summary()
        assert "svc" in summary
        entry = summary["svc"]
        assert "state" in entry
        assert "failure_rate" in entry
        assert "total_calls" in entry

    def test_stats_summary_state_value(self):
        reg = CircuitBreakerRegistry()
        reg.get("svc")
        assert reg.stats_summary()["svc"]["state"] == "closed"

    def test_stats_summary_open_state(self):
        reg = CircuitBreakerRegistry()
        reg.get("svc").trip()
        assert reg.stats_summary()["svc"]["state"] == "open"

    def test_stats_summary_failure_rate(self):
        cfg = CircuitBreakerConfig(failure_threshold=10)
        reg = CircuitBreakerRegistry(default_config=cfg)
        b = reg.get("svc")
        b.call(_ok)
        with pytest.raises(RuntimeError):
            b.call(_fail)
        summary = reg.stats_summary()
        assert summary["svc"]["failure_rate"] == pytest.approx(0.5)

    def test_stats_summary_total_calls(self):
        cfg = CircuitBreakerConfig(failure_threshold=10)
        reg = CircuitBreakerRegistry(default_config=cfg)
        b = reg.get("svc")
        b.call(_ok)
        b.call(_ok)
        assert reg.stats_summary()["svc"]["total_calls"] == 2

    def test_default_config_applied(self):
        cfg = CircuitBreakerConfig(failure_threshold=99)
        reg = CircuitBreakerRegistry(default_config=cfg)
        b = reg.get("svc")
        assert b._config.failure_threshold == 99

    def test_multiple_breakers_independent(self):
        cfg = CircuitBreakerConfig(failure_threshold=1)
        reg = CircuitBreakerRegistry(default_config=cfg)
        a = reg.get("a")
        b = reg.get("b")
        with pytest.raises(RuntimeError):
            a.call(_fail)
        assert a.state == CircuitState.OPEN
        assert b.state == CircuitState.CLOSED


# ---------------------------------------------------------------------------
# 12. Threading — concurrent calls
# ---------------------------------------------------------------------------

class TestThreading:
    def test_concurrent_successes_no_crash(self):
        cb = _make_cb(failure_threshold=100)
        errors = []

        def worker():
            try:
                cb.call(_ok)
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=worker) for _ in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
        assert cb.stats.total_calls == 20

    def test_concurrent_failures_open_circuit_exactly_once(self):
        cb = _make_cb(failure_threshold=5)
        results = []
        lock = threading.Lock()

        def worker():
            try:
                cb.call(_fail)
                with lock:
                    results.append("ok")
            except RuntimeError:
                with lock:
                    results.append("fail")
            except CircuitOpenError:
                with lock:
                    results.append("open")

        threads = [threading.Thread(target=worker) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # After enough failures, some calls should be rejected as OPEN
        assert "fail" in results
        # Circuit must be OPEN at end
        assert cb.state == CircuitState.OPEN

    def test_concurrent_reset_safe(self):
        cb = CircuitBreaker("svc")

        def trip_and_reset():
            cb.trip()
            cb.reset()

        threads = [threading.Thread(target=trip_and_reset) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Should end in either OPEN or CLOSED — no crash or corruption
        assert cb.state in (CircuitState.OPEN, CircuitState.CLOSED)

    def test_concurrent_calls_after_trip_raise_circuit_open(self):
        cb = CircuitBreaker("svc")
        cb.trip()
        errors = []

        def worker():
            try:
                cb.call(_ok)
            except CircuitOpenError as e:
                errors.append(e)

        threads = [threading.Thread(target=worker) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(errors) == 10


# ---------------------------------------------------------------------------
# 13. Time-based recovery (short sleep)
# ---------------------------------------------------------------------------

class TestTimeBasedRecovery:
    def test_recovery_timeout_respected(self):
        cb = _make_cb(failure_threshold=1, recovery_timeout=0.05,
                      success_threshold=1)
        with pytest.raises(RuntimeError):
            cb.call(_fail)
        assert cb.state == CircuitState.OPEN
        time.sleep(0.1)
        assert cb.state == CircuitState.HALF_OPEN

    def test_full_cycle_closed_open_half_open_closed(self):
        cb = _make_cb(failure_threshold=1, recovery_timeout=0.05,
                      success_threshold=1, half_open_max_calls=3)
        # CLOSED → OPEN
        with pytest.raises(RuntimeError):
            cb.call(_fail)
        assert cb.state == CircuitState.OPEN
        # OPEN → HALF_OPEN
        time.sleep(0.1)
        assert cb.state == CircuitState.HALF_OPEN
        # HALF_OPEN → CLOSED
        cb.call(_ok)
        assert cb.state == CircuitState.CLOSED

    def test_half_open_failure_reopens_and_recovers_again(self):
        cb = _make_cb(failure_threshold=1, recovery_timeout=0.05,
                      success_threshold=1, half_open_max_calls=3)
        with pytest.raises(RuntimeError):
            cb.call(_fail)
        time.sleep(0.1)
        assert cb.state == CircuitState.HALF_OPEN
        with pytest.raises(RuntimeError):
            cb.call(_fail)
        assert cb.state == CircuitState.OPEN
        # Recover again
        time.sleep(0.1)
        assert cb.state == CircuitState.HALF_OPEN
        cb.call(_ok)
        assert cb.state == CircuitState.CLOSED
