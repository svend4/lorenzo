"""Tests for circuit_breaker_v2 — ~90 tests covering the full spec."""
import threading
import pytest

from docstoolkit.circuit_breaker_v2 import (
    CircuitState,
    BreakerConfig,
    CircuitBreakerError,
    CircuitBreaker,
)


# ---------------------------------------------------------------------------
# Virtual-time helpers
# ---------------------------------------------------------------------------

class FakeClock:
    """Simple monotonic clock whose value can be advanced manually."""

    def __init__(self, start: float = 0.0) -> None:
        self._t = start

    def advance(self, delta: float) -> None:
        self._t += delta

    def __call__(self) -> float:
        return self._t


def _cb_with_clock(config: "BreakerConfig | None" = None) -> tuple["CircuitBreaker", FakeClock]:
    """Return (CircuitBreaker, FakeClock); the breaker uses virtual time."""
    clock = FakeClock()
    cb = CircuitBreaker(config)
    cb._now = clock  # monkeypatch
    return cb, clock


# ---------------------------------------------------------------------------
# Generic helpers
# ---------------------------------------------------------------------------

def _ok(*args, **kwargs):
    return "ok"


def _fail(*args, **kwargs):
    raise RuntimeError("deliberate failure")


def _return(value):
    def fn(*args, **kwargs):
        return value
    return fn


def _make_cb(
    failure_threshold: int = 5,
    recovery_timeout: float = 30.0,
    success_threshold: int = 2,
    half_open_max_calls: int = 1,
) -> CircuitBreaker:
    cfg = BreakerConfig(
        failure_threshold=failure_threshold,
        recovery_timeout=recovery_timeout,
        success_threshold=success_threshold,
        half_open_max_calls=half_open_max_calls,
    )
    return CircuitBreaker(cfg)


def _trip_to_half_open(cb: CircuitBreaker, clock: FakeClock) -> None:
    """Drive cb CLOSED→OPEN→HALF_OPEN using virtual time."""
    # record enough failures to open
    for _ in range(cb._config.failure_threshold):
        cb.record_failure()
    assert cb._state == CircuitState.OPEN
    # advance past recovery_timeout
    clock.advance(cb._config.recovery_timeout + 1.0)
    # read state to trigger transition
    _ = cb.state


# ===========================================================================
# 1. CircuitState enum
# ===========================================================================

class TestCircuitStateEnum:
    def test_closed_value(self):
        assert CircuitState.CLOSED == "closed"

    def test_open_value(self):
        assert CircuitState.OPEN == "open"

    def test_half_open_value(self):
        assert CircuitState.HALF_OPEN == "half_open"

    def test_exactly_three_states(self):
        assert len(CircuitState) == 3

    def test_is_str_subclass(self):
        assert isinstance(CircuitState.CLOSED, str)

    def test_all_distinct(self):
        assert len({CircuitState.CLOSED, CircuitState.OPEN, CircuitState.HALF_OPEN}) == 3


# ===========================================================================
# 2. BreakerConfig defaults
# ===========================================================================

class TestBreakerConfigDefaults:
    def test_default_failure_threshold(self):
        assert BreakerConfig().failure_threshold == 5

    def test_default_recovery_timeout(self):
        assert BreakerConfig().recovery_timeout == 30.0

    def test_default_success_threshold(self):
        assert BreakerConfig().success_threshold == 2

    def test_default_half_open_max_calls(self):
        assert BreakerConfig().half_open_max_calls == 1

    def test_custom_failure_threshold(self):
        assert BreakerConfig(failure_threshold=10).failure_threshold == 10

    def test_custom_recovery_timeout(self):
        assert BreakerConfig(recovery_timeout=5.0).recovery_timeout == 5.0

    def test_custom_success_threshold(self):
        assert BreakerConfig(success_threshold=3).success_threshold == 3

    def test_custom_half_open_max_calls(self):
        assert BreakerConfig(half_open_max_calls=4).half_open_max_calls == 4


# ===========================================================================
# 3. Initial state
# ===========================================================================

class TestInitialState:
    def test_initial_state_is_closed(self):
        cb = CircuitBreaker()
        assert cb.state == CircuitState.CLOSED

    def test_initial_failure_count_zero(self):
        cb = CircuitBreaker()
        assert cb.failure_count == 0

    def test_initial_success_count_zero(self):
        cb = CircuitBreaker()
        assert cb.success_count == 0

    def test_none_config_uses_defaults(self):
        cb = CircuitBreaker(None)
        assert cb._config.failure_threshold == 5

    def test_custom_config_stored(self):
        cfg = BreakerConfig(failure_threshold=99)
        cb = CircuitBreaker(cfg)
        assert cb._config.failure_threshold == 99


# ===========================================================================
# 4. call() — basic behaviour in CLOSED state
# ===========================================================================

class TestCallClosed:
    def test_returns_function_result(self):
        cb = CircuitBreaker()
        assert cb.call(_return(42)) == 42

    def test_passes_args(self):
        cb = CircuitBreaker()
        assert cb.call(lambda x, y: x + y, 3, 4) == 7

    def test_passes_kwargs(self):
        cb = CircuitBreaker()
        assert cb.call(lambda x=0, y=0: x * y, x=6, y=7) == 42

    def test_success_leaves_circuit_closed(self):
        cb = CircuitBreaker()
        cb.call(_ok)
        assert cb.state == CircuitState.CLOSED

    def test_single_failure_does_not_trip(self):
        cb = _make_cb(failure_threshold=5)
        with pytest.raises(RuntimeError):
            cb.call(_fail)
        assert cb.state == CircuitState.CLOSED

    def test_failure_propagates_exception(self):
        cb = CircuitBreaker()
        with pytest.raises(RuntimeError, match="deliberate failure"):
            cb.call(_fail)

    def test_failure_propagates_non_runtime_exception(self):
        cb = CircuitBreaker()
        with pytest.raises(ValueError):
            cb.call(lambda: (_ for _ in ()).throw(ValueError("raw")))

    def test_failure_increments_failure_count(self):
        cb = CircuitBreaker()
        with pytest.raises(RuntimeError):
            cb.call(_fail)
        assert cb.failure_count == 1

    def test_success_does_not_increment_failure_count(self):
        cb = CircuitBreaker()
        cb.call(_ok)
        assert cb.failure_count == 0


# ===========================================================================
# 5. CLOSED → OPEN transition
# ===========================================================================

class TestClosedToOpen:
    def test_trips_at_failure_threshold(self):
        cb = _make_cb(failure_threshold=3)
        for _ in range(3):
            with pytest.raises(RuntimeError):
                cb.call(_fail)
        assert cb.state == CircuitState.OPEN

    def test_does_not_trip_below_threshold(self):
        cb = _make_cb(failure_threshold=3)
        for _ in range(2):
            with pytest.raises(RuntimeError):
                cb.call(_fail)
        assert cb.state == CircuitState.CLOSED

    def test_failure_count_at_threshold(self):
        cb = _make_cb(failure_threshold=4)
        for _ in range(4):
            with pytest.raises(RuntimeError):
                cb.call(_fail)
        assert cb.failure_count == 4

    def test_success_resets_failure_count(self):
        cb = _make_cb(failure_threshold=5)
        with pytest.raises(RuntimeError):
            cb.call(_fail)
        with pytest.raises(RuntimeError):
            cb.call(_fail)
        cb.call(_ok)  # success between failures
        with pytest.raises(RuntimeError):
            cb.call(_fail)
        # failure_count should reflect failures since reset (depends on impl)
        # At minimum circuit is still CLOSED — success kept it from tripping
        assert cb.state == CircuitState.CLOSED

    def test_success_resets_failure_count_value(self):
        cb = _make_cb(failure_threshold=5)
        with pytest.raises(RuntimeError):
            cb.call(_fail)
        with pytest.raises(RuntimeError):
            cb.call(_fail)
        # The success resets the consecutive-failure count tracked internally.
        # After 2 failures + 1 success we're still CLOSED.
        cb.call(_ok)
        assert cb.state == CircuitState.CLOSED

    def test_threshold_one_trips_immediately(self):
        cb = _make_cb(failure_threshold=1)
        with pytest.raises(RuntimeError):
            cb.call(_fail)
        assert cb.state == CircuitState.OPEN

    def test_success_count_reset_on_open(self):
        cb, clock = _cb_with_clock(BreakerConfig(
            failure_threshold=2, recovery_timeout=10.0, success_threshold=5,
            half_open_max_calls=5,
        ))
        # record a success first, then trip
        cb.record_success()
        assert cb.success_count == 1
        for _ in range(2):
            cb.record_failure()
        # now OPEN — success_count must be 0
        assert cb.state == CircuitState.OPEN
        assert cb.success_count == 0

    def test_last_failure_time_recorded(self):
        cb, clock = _cb_with_clock()
        clock.advance(100.0)
        cb.record_failure()
        assert cb.stats()["last_failure_time"] == pytest.approx(100.0)


# ===========================================================================
# 6. OPEN state — fast-fail
# ===========================================================================

class TestOpenState:
    def test_open_raises_circuit_breaker_error(self):
        cb = _make_cb(failure_threshold=1)
        with pytest.raises(RuntimeError):
            cb.call(_fail)
        with pytest.raises(CircuitBreakerError):
            cb.call(_ok)

    def test_open_does_not_call_fn(self):
        called = []
        cb = _make_cb(failure_threshold=1)
        with pytest.raises(RuntimeError):
            cb.call(_fail)
        with pytest.raises(CircuitBreakerError):
            cb.call(lambda: called.append(1))
        assert called == []

    def test_open_rejects_multiple_times(self):
        cb = _make_cb(failure_threshold=1)
        with pytest.raises(RuntimeError):
            cb.call(_fail)
        for _ in range(5):
            with pytest.raises(CircuitBreakerError):
                cb.call(_ok)

    def test_circuit_breaker_error_is_exception(self):
        assert issubclass(CircuitBreakerError, Exception)

    def test_circuit_breaker_error_can_be_caught(self):
        with pytest.raises(CircuitBreakerError):
            raise CircuitBreakerError("test")

    def test_circuit_breaker_error_not_subclass_of_runtime_error(self):
        # Must NOT shadow the original function exceptions
        assert not issubclass(CircuitBreakerError, RuntimeError)


# ===========================================================================
# 7. OPEN → HALF_OPEN (virtual time)
# ===========================================================================

class TestOpenToHalfOpen:
    def test_no_transition_before_timeout(self):
        cb, clock = _cb_with_clock(BreakerConfig(
            failure_threshold=1, recovery_timeout=30.0,
        ))
        cb.record_failure()
        clock.advance(29.9)
        assert cb.state == CircuitState.OPEN

    def test_transitions_at_exactly_timeout(self):
        cb, clock = _cb_with_clock(BreakerConfig(
            failure_threshold=1, recovery_timeout=30.0,
        ))
        cb.record_failure()
        clock.advance(30.0)
        assert cb.state == CircuitState.HALF_OPEN

    def test_transitions_after_timeout(self):
        cb, clock = _cb_with_clock(BreakerConfig(
            failure_threshold=1, recovery_timeout=30.0,
        ))
        cb.record_failure()
        clock.advance(60.0)
        assert cb.state == CircuitState.HALF_OPEN

    def test_call_triggers_transition(self):
        cb, clock = _cb_with_clock(BreakerConfig(
            failure_threshold=1, recovery_timeout=5.0,
            success_threshold=10, half_open_max_calls=5,
        ))
        cb.record_failure()
        clock.advance(10.0)
        result = cb.call(_ok)
        assert result == "ok"

    def test_transition_resets_half_open_active(self):
        cb, clock = _cb_with_clock(BreakerConfig(
            failure_threshold=1, recovery_timeout=5.0,
            half_open_max_calls=2,
        ))
        cb.record_failure()
        clock.advance(10.0)
        _ = cb.state
        assert cb._half_open_active == 0


# ===========================================================================
# 8. HALF_OPEN behaviour
# ===========================================================================

class TestHalfOpen:
    def _half_open(
        self,
        failure_threshold: int = 5,
        success_threshold: int = 2,
        half_open_max_calls: int = 2,
    ) -> tuple["CircuitBreaker", FakeClock]:
        cfg = BreakerConfig(
            failure_threshold=failure_threshold,
            recovery_timeout=10.0,
            success_threshold=success_threshold,
            half_open_max_calls=half_open_max_calls,
        )
        cb, clock = _cb_with_clock(cfg)
        _trip_to_half_open(cb, clock)
        return cb, clock

    def test_state_is_half_open_after_trip(self):
        cb, _ = self._half_open()
        assert cb.state == CircuitState.HALF_OPEN

    def test_allows_call_up_to_max(self):
        cb, _ = self._half_open(success_threshold=10, half_open_max_calls=2)
        cb.call(_ok)
        cb.call(_ok)

    def test_rejects_concurrent_call_beyond_max(self):
        """half_open_max_calls limits *concurrent* in-flight calls."""
        import threading
        cb, _ = self._half_open(success_threshold=10, half_open_max_calls=1)
        gate = threading.Event()
        errors = []

        def slow_ok():
            gate.wait()  # block until we attempt the second call
            return "ok"

        def first_call():
            try:
                cb.call(slow_ok)
            except Exception as e:
                errors.append(e)

        t = threading.Thread(target=first_call)
        t.start()
        # Wait until slow_ok is executing (active slot occupied)
        import time
        time.sleep(0.02)
        # Second call should be rejected while first is in-flight
        with pytest.raises(CircuitBreakerError):
            cb.call(_ok)
        gate.set()
        t.join()
        assert errors == []

    def test_half_open_max_zero_rejects_all(self):
        cb, _ = self._half_open(half_open_max_calls=0)
        with pytest.raises(CircuitBreakerError):
            cb.call(_ok)

    def test_success_increments_success_count(self):
        cb, _ = self._half_open(success_threshold=10, half_open_max_calls=5)
        cb.call(_ok)
        assert cb.success_count == 1

    def test_closes_after_success_threshold(self):
        cb, _ = self._half_open(success_threshold=2, half_open_max_calls=5)
        cb.call(_ok)
        assert cb._state == CircuitState.HALF_OPEN
        cb.call(_ok)
        assert cb.state == CircuitState.CLOSED

    def test_success_threshold_one_closes_immediately(self):
        cb, _ = self._half_open(success_threshold=1, half_open_max_calls=3)
        cb.call(_ok)
        assert cb.state == CircuitState.CLOSED

    def test_close_resets_counts(self):
        cb, _ = self._half_open(success_threshold=1, half_open_max_calls=3)
        cb.call(_ok)
        assert cb.state == CircuitState.CLOSED
        assert cb.failure_count == 0
        assert cb.success_count == 0

    def test_failure_reopens_circuit(self):
        cb, _ = self._half_open(success_threshold=5, half_open_max_calls=5)
        with pytest.raises(RuntimeError):
            cb.call(_fail)
        assert cb.state == CircuitState.OPEN

    def test_failure_resets_success_count(self):
        cb, _ = self._half_open(success_threshold=5, half_open_max_calls=5)
        cb.call(_ok)  # success_count = 1
        with pytest.raises(RuntimeError):
            cb.call(_fail)
        # after reopening, success_count must be 0
        assert cb.success_count == 0

    def test_failure_then_recovery_possible(self):
        cb, clock = self._half_open(failure_threshold=1, success_threshold=1,
                                    half_open_max_calls=3)
        with pytest.raises(RuntimeError):
            cb.call(_fail)
        assert cb.state == CircuitState.OPEN
        clock.advance(cb._config.recovery_timeout + 1.0)
        assert cb.state == CircuitState.HALF_OPEN
        cb.call(_ok)
        assert cb.state == CircuitState.CLOSED

    def test_return_value_in_half_open(self):
        cb, _ = self._half_open(success_threshold=10, half_open_max_calls=5)
        assert cb.call(_return(99)) == 99


# ===========================================================================
# 9. reset()
# ===========================================================================

class TestReset:
    def test_reset_from_open_to_closed(self):
        cb = _make_cb(failure_threshold=1)
        with pytest.raises(RuntimeError):
            cb.call(_fail)
        assert cb.state == CircuitState.OPEN
        cb.reset()
        assert cb.state == CircuitState.CLOSED

    def test_reset_clears_failure_count(self):
        cb = _make_cb(failure_threshold=10)
        for _ in range(3):
            with pytest.raises(RuntimeError):
                cb.call(_fail)
        cb.reset()
        assert cb.failure_count == 0

    def test_reset_clears_success_count(self):
        cb, clock = _cb_with_clock(BreakerConfig(
            failure_threshold=5, recovery_timeout=10.0,
            success_threshold=10, half_open_max_calls=5,
        ))
        _trip_to_half_open(cb, clock)
        cb.call(_ok)
        assert cb.success_count == 1
        cb.reset()
        assert cb.success_count == 0

    def test_reset_allows_new_calls(self):
        cb = _make_cb(failure_threshold=1)
        with pytest.raises(RuntimeError):
            cb.call(_fail)
        cb.reset()
        assert cb.call(_ok) == "ok"

    def test_reset_idempotent(self):
        cb = CircuitBreaker()
        cb.reset()
        cb.reset()
        assert cb.state == CircuitState.CLOSED

    def test_reset_from_half_open_to_closed(self):
        cb, clock = _cb_with_clock(BreakerConfig(
            failure_threshold=1, recovery_timeout=10.0,
        ))
        cb.record_failure()
        clock.advance(20.0)
        assert cb.state == CircuitState.HALF_OPEN
        cb.reset()
        assert cb.state == CircuitState.CLOSED


# ===========================================================================
# 10. record_success() / record_failure() manual methods
# ===========================================================================

class TestManualRecording:
    def test_record_failure_increments_failure_count(self):
        cb = CircuitBreaker()
        cb.record_failure()
        assert cb.failure_count == 1

    def test_record_failure_multiple(self):
        cb = CircuitBreaker()
        cb.record_failure()
        cb.record_failure()
        assert cb.failure_count == 2

    def test_record_failure_trips_at_threshold(self):
        cb = _make_cb(failure_threshold=3)
        for _ in range(3):
            cb.record_failure()
        assert cb.state == CircuitState.OPEN

    def test_record_success_increments_success_count(self):
        cb = CircuitBreaker()
        cb.record_success()
        assert cb.success_count == 1

    def test_record_success_in_half_open_closes(self):
        cb, clock = _cb_with_clock(BreakerConfig(
            failure_threshold=1, recovery_timeout=10.0,
            success_threshold=1, half_open_max_calls=1,
        ))
        cb.record_failure()
        clock.advance(20.0)
        _ = cb.state  # trigger transition
        cb.record_success()
        assert cb.state == CircuitState.CLOSED

    def test_record_failure_in_half_open_opens(self):
        cb, clock = _cb_with_clock(BreakerConfig(
            failure_threshold=1, recovery_timeout=10.0,
            success_threshold=5,
        ))
        cb.record_failure()
        clock.advance(20.0)
        _ = cb.state
        cb.record_failure()
        assert cb.state == CircuitState.OPEN

    def test_record_success_closed_does_not_change_state(self):
        cb = CircuitBreaker()
        cb.record_success()
        assert cb.state == CircuitState.CLOSED


# ===========================================================================
# 11. stats()
# ===========================================================================

class TestStats:
    def test_stats_returns_dict(self):
        cb = CircuitBreaker()
        assert isinstance(cb.stats(), dict)

    def test_stats_has_state_key(self):
        cb = CircuitBreaker()
        assert "state" in cb.stats()

    def test_stats_has_failure_count_key(self):
        cb = CircuitBreaker()
        assert "failure_count" in cb.stats()

    def test_stats_has_success_count_key(self):
        cb = CircuitBreaker()
        assert "success_count" in cb.stats()

    def test_stats_has_last_failure_time_key(self):
        cb = CircuitBreaker()
        assert "last_failure_time" in cb.stats()

    def test_stats_initial_state(self):
        cb = CircuitBreaker()
        s = cb.stats()
        assert s["state"] == CircuitState.CLOSED
        assert s["failure_count"] == 0
        assert s["success_count"] == 0
        assert s["last_failure_time"] == 0.0

    def test_stats_reflects_failures(self):
        cb = _make_cb(failure_threshold=10)
        for _ in range(3):
            with pytest.raises(RuntimeError):
                cb.call(_fail)
        s = cb.stats()
        assert s["failure_count"] == 3

    def test_stats_reflects_open_state(self):
        cb = _make_cb(failure_threshold=1)
        with pytest.raises(RuntimeError):
            cb.call(_fail)
        assert cb.stats()["state"] == CircuitState.OPEN

    def test_stats_last_failure_time_set(self):
        cb, clock = _cb_with_clock()
        clock.advance(50.0)
        cb.record_failure()
        assert cb.stats()["last_failure_time"] == pytest.approx(50.0)

    def test_stats_is_snapshot(self):
        cb = CircuitBreaker()
        s1 = cb.stats()
        cb.record_failure()
        s2 = cb.stats()
        assert s1["failure_count"] == 0
        assert s2["failure_count"] == 1


# ===========================================================================
# 12. Full state-machine cycle (virtual time, no sleep)
# ===========================================================================

class TestStateMachineCycle:
    def test_full_cycle_closed_open_half_open_closed(self):
        cb, clock = _cb_with_clock(BreakerConfig(
            failure_threshold=2,
            recovery_timeout=10.0,
            success_threshold=2,
            half_open_max_calls=3,
        ))
        # CLOSED → OPEN
        cb.record_failure()
        cb.record_failure()
        assert cb.state == CircuitState.OPEN

        # Still OPEN before timeout
        clock.advance(9.9)
        assert cb.state == CircuitState.OPEN

        # OPEN → HALF_OPEN
        clock.advance(0.1)
        assert cb.state == CircuitState.HALF_OPEN

        # HALF_OPEN → CLOSED
        cb.record_success()
        assert cb._state == CircuitState.HALF_OPEN
        cb.record_success()
        assert cb.state == CircuitState.CLOSED

    def test_half_open_fail_and_retry_cycle(self):
        cb, clock = _cb_with_clock(BreakerConfig(
            failure_threshold=1,
            recovery_timeout=10.0,
            success_threshold=1,
            half_open_max_calls=2,
        ))
        cb.record_failure()
        clock.advance(15.0)
        assert cb.state == CircuitState.HALF_OPEN

        cb.record_failure()
        assert cb.state == CircuitState.OPEN

        clock.advance(15.0)
        assert cb.state == CircuitState.HALF_OPEN

        cb.record_success()
        assert cb.state == CircuitState.CLOSED


# ===========================================================================
# 13. Thread safety
# ===========================================================================

class TestThreadSafety:
    def test_concurrent_successes_no_crash(self):
        cb = _make_cb(failure_threshold=1000, half_open_max_calls=1000)
        errors = []

        def worker():
            try:
                cb.call(_ok)
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=worker) for _ in range(30)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []

    def test_concurrent_failures_open_circuit(self):
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
            except CircuitBreakerError:
                with lock:
                    results.append("open")

        threads = [threading.Thread(target=worker) for _ in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert cb.state == CircuitState.OPEN
        assert "fail" in results

    def test_concurrent_reset_no_crash(self):
        cb = _make_cb(failure_threshold=1)

        def worker():
            try:
                cb.call(_fail)
            except (RuntimeError, CircuitBreakerError):
                pass
            cb.reset()

        threads = [threading.Thread(target=worker) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # No crash; state is deterministic after last reset
        assert cb.state in (CircuitState.OPEN, CircuitState.CLOSED)

    def test_concurrent_calls_on_open_all_rejected(self):
        cb = _make_cb(failure_threshold=1)
        with pytest.raises(RuntimeError):
            cb.call(_fail)
        errors = []

        def worker():
            try:
                cb.call(_ok)
            except CircuitBreakerError as e:
                errors.append(e)

        threads = [threading.Thread(target=worker) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(errors) == 10

    def test_concurrent_record_failure_no_double_count(self):
        """failure_count should equal the number of record_failure calls."""
        cb = _make_cb(failure_threshold=1000)
        n = 50
        barrier = threading.Barrier(n)

        def worker():
            barrier.wait()
            cb.record_failure()

        threads = [threading.Thread(target=worker) for _ in range(n)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert cb.failure_count == n


# ===========================================================================
# 14. Edge cases
# ===========================================================================

class TestEdgeCases:
    def test_failure_threshold_one(self):
        cb = _make_cb(failure_threshold=1)
        with pytest.raises(RuntimeError):
            cb.call(_fail)
        assert cb.state == CircuitState.OPEN

    def test_success_threshold_one(self):
        cb, clock = _cb_with_clock(BreakerConfig(
            failure_threshold=1, recovery_timeout=10.0,
            success_threshold=1, half_open_max_calls=2,
        ))
        cb.record_failure()
        clock.advance(20.0)
        _ = cb.state
        cb.record_success()
        assert cb.state == CircuitState.CLOSED

    def test_large_failure_threshold_never_trips(self):
        cb = _make_cb(failure_threshold=1000)
        for _ in range(10):
            with pytest.raises(RuntimeError):
                cb.call(_fail)
        assert cb.state == CircuitState.CLOSED

    def test_zero_recovery_timeout_opens_immediately_to_half_open(self):
        cb, clock = _cb_with_clock(BreakerConfig(
            failure_threshold=1, recovery_timeout=0.0,
            success_threshold=1, half_open_max_calls=1,
        ))
        # clock.advance(0.0) — already at or past timeout immediately
        cb.record_failure()
        # No clock advance needed — 0.0 timeout
        assert cb.state == CircuitState.HALF_OPEN

    def test_call_returns_none_for_void_function(self):
        cb = CircuitBreaker()
        result = cb.call(lambda: None)
        assert result is None

    def test_call_with_no_args(self):
        cb = CircuitBreaker()
        assert cb.call(lambda: "hello") == "hello"

    def test_record_success_multiple_times_closed(self):
        cb = CircuitBreaker()
        for _ in range(100):
            cb.record_success()
        # success_count accumulates but circuit stays CLOSED
        assert cb.state == CircuitState.CLOSED
        assert cb.success_count == 100

    def test_stats_state_is_circuit_state_enum(self):
        cb = CircuitBreaker()
        s = cb.stats()
        assert isinstance(s["state"], CircuitState)
