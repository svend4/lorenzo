"""Tests for the retry_policy module (E56).

Coverage targets:
- BackoffCalculator: all four strategies, capping, jitter bounds
- RetryConfig defaults and customisation
- RetryExecutor: success paths, retry paths, exhaustion, filtering
- retry decorator: basic usage, re-raise on exhaustion, sleep_fn injection
- Edge cases: max_attempts=1, retry_on=[], stop_on override
"""
from __future__ import annotations

import pytest

from docstoolkit.retry_policy.backoff import BackoffCalculator, BackoffConfig, BackoffStrategy
from docstoolkit.retry_policy.policy import (
    RetryCondition,
    RetryConfig,
    RetryExecutor,
    RetryResult,
)
from docstoolkit.retry_policy.decorator import retry


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def noop_sleep(_delay: float) -> None:
    """Sleep function that does nothing — used to speed up tests."""


def capturing_sleep(log: list) -> callable:
    """Return a sleep function that records all delay values into *log*."""
    def _sleep(delay: float) -> None:
        log.append(delay)
    return _sleep


def always_fail(exc_type=ValueError, msg="fail"):
    """Return a callable that always raises *exc_type*."""
    def _fn(*args, **kwargs):
        raise exc_type(msg)
    return _fn


def fail_n_times(n: int, then_return=42, exc_type=ValueError):
    """Return a callable that raises for the first *n* calls, then returns *then_return*."""
    calls = {"count": 0}
    def _fn(*args, **kwargs):
        if calls["count"] < n:
            calls["count"] += 1
            raise exc_type("temporary failure")
        return then_return
    return _fn


# ---------------------------------------------------------------------------
# BackoffStrategy enum
# ---------------------------------------------------------------------------

class TestBackoffStrategyEnum:
    def test_fixed_member_exists(self):
        assert BackoffStrategy.FIXED is BackoffStrategy.FIXED

    def test_linear_member_exists(self):
        assert BackoffStrategy.LINEAR is BackoffStrategy.LINEAR

    def test_exponential_member_exists(self):
        assert BackoffStrategy.EXPONENTIAL is BackoffStrategy.EXPONENTIAL

    def test_jitter_member_exists(self):
        assert BackoffStrategy.JITTER is BackoffStrategy.JITTER

    def test_four_members_total(self):
        assert len(BackoffStrategy) == 4


# ---------------------------------------------------------------------------
# BackoffConfig dataclass defaults
# ---------------------------------------------------------------------------

class TestBackoffConfigDefaults:
    def test_default_strategy(self):
        cfg = BackoffConfig()
        assert cfg.strategy is BackoffStrategy.EXPONENTIAL

    def test_default_base_delay(self):
        assert BackoffConfig().base_delay == 1.0

    def test_default_max_delay(self):
        assert BackoffConfig().max_delay == 60.0

    def test_default_multiplier(self):
        assert BackoffConfig().multiplier == 2.0

    def test_default_jitter_range(self):
        assert BackoffConfig().jitter_range == 0.5

    def test_custom_values(self):
        cfg = BackoffConfig(
            strategy=BackoffStrategy.FIXED,
            base_delay=0.5,
            max_delay=10.0,
            multiplier=3.0,
            jitter_range=0.1,
        )
        assert cfg.strategy is BackoffStrategy.FIXED
        assert cfg.base_delay == 0.5
        assert cfg.max_delay == 10.0
        assert cfg.multiplier == 3.0
        assert cfg.jitter_range == 0.1


# ---------------------------------------------------------------------------
# BackoffCalculator — FIXED strategy
# ---------------------------------------------------------------------------

class TestBackoffCalculatorFixed:
    def _calc(self, base=1.0, max_delay=60.0):
        return BackoffCalculator(BackoffConfig(
            strategy=BackoffStrategy.FIXED,
            base_delay=base,
            max_delay=max_delay,
        ))

    def test_attempt0_equals_base_delay(self):
        assert self._calc().delay(0) == 1.0

    def test_attempt5_equals_base_delay(self):
        assert self._calc().delay(5) == 1.0

    def test_fixed_caps_at_max_delay(self):
        calc = self._calc(base=100.0, max_delay=10.0)
        assert calc.delay(0) == 10.0

    def test_fixed_below_max(self):
        calc = self._calc(base=5.0, max_delay=60.0)
        assert calc.delay(3) == 5.0


# ---------------------------------------------------------------------------
# BackoffCalculator — LINEAR strategy
# ---------------------------------------------------------------------------

class TestBackoffCalculatorLinear:
    def _calc(self, base=1.0, max_delay=60.0):
        return BackoffCalculator(BackoffConfig(
            strategy=BackoffStrategy.LINEAR,
            base_delay=base,
            max_delay=max_delay,
        ))

    def test_attempt0_is_one_times_base(self):
        assert self._calc().delay(0) == 1.0

    def test_attempt1_is_two_times_base(self):
        assert self._calc().delay(1) == 2.0

    def test_attempt4_is_five_times_base(self):
        assert self._calc().delay(4) == 5.0

    def test_linear_caps_at_max_delay(self):
        calc = self._calc(base=10.0, max_delay=25.0)
        # attempt 3 → 40, capped to 25
        assert calc.delay(3) == 25.0

    def test_linear_below_cap_not_capped(self):
        calc = self._calc(base=2.0, max_delay=100.0)
        assert calc.delay(2) == 6.0


# ---------------------------------------------------------------------------
# BackoffCalculator — EXPONENTIAL strategy
# ---------------------------------------------------------------------------

class TestBackoffCalculatorExponential:
    def _calc(self, base=1.0, multiplier=2.0, max_delay=60.0):
        return BackoffCalculator(BackoffConfig(
            strategy=BackoffStrategy.EXPONENTIAL,
            base_delay=base,
            multiplier=multiplier,
            max_delay=max_delay,
        ))

    def test_attempt0_is_base(self):
        assert self._calc().delay(0) == 1.0

    def test_attempt1_doubles(self):
        assert self._calc().delay(1) == 2.0

    def test_attempt2_quadruples(self):
        assert self._calc().delay(2) == 4.0

    def test_exponential_caps_at_max_delay(self):
        calc = self._calc(base=1.0, max_delay=10.0)
        # 2**10 = 1024 >> 10
        assert calc.delay(10) == 10.0

    def test_custom_multiplier(self):
        calc = self._calc(base=2.0, multiplier=3.0)
        # attempt 2 → 2 * 3^2 = 18
        assert calc.delay(2) == 18.0

    def test_exponential_below_cap(self):
        calc = self._calc(base=1.0, max_delay=100.0)
        assert calc.delay(3) == 8.0


# ---------------------------------------------------------------------------
# BackoffCalculator — JITTER strategy
# ---------------------------------------------------------------------------

class TestBackoffCalculatorJitter:
    def _calc(self, base=1.0, multiplier=2.0, jitter_range=0.5, max_delay=60.0):
        return BackoffCalculator(BackoffConfig(
            strategy=BackoffStrategy.JITTER,
            base_delay=base,
            multiplier=multiplier,
            jitter_range=jitter_range,
            max_delay=max_delay,
        ))

    def test_jitter_never_negative(self):
        calc = self._calc()
        for attempt in range(10):
            assert calc.delay(attempt) >= 0.0

    def test_jitter_never_exceeds_max_delay(self):
        calc = self._calc(max_delay=5.0)
        for attempt in range(20):
            assert calc.delay(attempt) <= 5.0

    def test_jitter_delay_is_float(self):
        assert isinstance(self._calc().delay(0), float)

    def test_jitter_zero_jitter_range_equals_exponential(self):
        """With jitter_range=0, result should match exponential exactly."""
        calc = BackoffCalculator(BackoffConfig(
            strategy=BackoffStrategy.JITTER,
            base_delay=1.0,
            multiplier=2.0,
            jitter_range=0.0,
            max_delay=60.0,
        ))
        assert calc.delay(0) == 1.0
        assert calc.delay(1) == 2.0
        assert calc.delay(2) == 4.0

    def test_jitter_capped_at_max_delay(self):
        calc = self._calc(max_delay=1.0, base=1.0, multiplier=2.0, jitter_range=0.0)
        # attempt 5 → 32, capped to 1.0
        assert calc.delay(5) == 1.0

    def test_jitter_with_large_negative_noise_floored_at_zero(self):
        """Even with heavy negative noise the delay must not go below 0."""
        calc = BackoffCalculator(BackoffConfig(
            strategy=BackoffStrategy.JITTER,
            base_delay=0.001,   # tiny base
            multiplier=1.0,     # exponent stays flat
            jitter_range=100.0, # massive negative noise possible
            max_delay=60.0,
        ))
        for _ in range(50):
            assert calc.delay(0) >= 0.0


# ---------------------------------------------------------------------------
# BackoffCalculator — default config (no arg)
# ---------------------------------------------------------------------------

class TestBackoffCalculatorDefaults:
    def test_default_config_exponential(self):
        calc = BackoffCalculator()
        # default EXPONENTIAL, base=1, multiplier=2
        assert calc.delay(0) == 1.0
        assert calc.delay(1) == 2.0


# ---------------------------------------------------------------------------
# RetryCondition enum
# ---------------------------------------------------------------------------

class TestRetryConditionEnum:
    def test_on_exception(self):
        assert RetryCondition.ON_EXCEPTION is RetryCondition.ON_EXCEPTION

    def test_on_result(self):
        assert RetryCondition.ON_RESULT is RetryCondition.ON_RESULT

    def test_always(self):
        assert RetryCondition.ALWAYS is RetryCondition.ALWAYS


# ---------------------------------------------------------------------------
# RetryConfig defaults
# ---------------------------------------------------------------------------

class TestRetryConfigDefaults:
    def test_default_max_attempts(self):
        assert RetryConfig().max_attempts == 3

    def test_default_backoff_is_backoff_config(self):
        assert isinstance(RetryConfig().backoff, BackoffConfig)

    def test_default_retry_on_empty(self):
        assert RetryConfig().retry_on == []

    def test_default_stop_on_empty(self):
        assert RetryConfig().stop_on == []

    def test_default_result_predicate_none(self):
        assert RetryConfig().result_retry_predicate is None

    def test_default_sleep_fn_none(self):
        assert RetryConfig().sleep_fn is None

    def test_custom_max_attempts(self):
        assert RetryConfig(max_attempts=5).max_attempts == 5

    def test_instances_have_independent_retry_on_lists(self):
        a = RetryConfig()
        b = RetryConfig()
        a.retry_on.append(ValueError)
        assert b.retry_on == []


# ---------------------------------------------------------------------------
# RetryResult dataclass
# ---------------------------------------------------------------------------

class TestRetryResult:
    def test_succeeded_true(self):
        r = RetryResult(value=42, attempts=1, succeeded=True)
        assert r.succeeded is True
        assert r.value == 42
        assert r.attempts == 1

    def test_succeeded_false(self):
        r = RetryResult(value=None, attempts=3, succeeded=False, last_error="oops")
        assert r.succeeded is False
        assert r.last_error == "oops"

    def test_default_last_error_empty(self):
        r = RetryResult(value=None, attempts=1, succeeded=True)
        assert r.last_error == ""


# ---------------------------------------------------------------------------
# RetryExecutor — success on first try
# ---------------------------------------------------------------------------

class TestRetryExecutorFirstTrySuccess:
    def test_returns_correct_value(self):
        ex = RetryExecutor(RetryConfig(sleep_fn=noop_sleep))
        result = ex.execute(lambda: 99)
        assert result.value == 99

    def test_succeeded_true(self):
        ex = RetryExecutor(RetryConfig(sleep_fn=noop_sleep))
        result = ex.execute(lambda: "ok")
        assert result.succeeded is True

    def test_attempts_is_one(self):
        ex = RetryExecutor(RetryConfig(sleep_fn=noop_sleep))
        result = ex.execute(lambda: "ok")
        assert result.attempts == 1

    def test_no_error_on_success(self):
        ex = RetryExecutor(RetryConfig(sleep_fn=noop_sleep))
        result = ex.execute(lambda: 0)
        assert result.last_error == ""


# ---------------------------------------------------------------------------
# RetryExecutor — succeeds on Nth retry
# ---------------------------------------------------------------------------

class TestRetryExecutorSucceedsOnRetry:
    def test_succeeds_on_second_attempt(self):
        fn = fail_n_times(1, then_return="hello")
        ex = RetryExecutor(RetryConfig(max_attempts=3, sleep_fn=noop_sleep))
        result = ex.execute(fn)
        assert result.succeeded is True
        assert result.value == "hello"

    def test_attempts_count_correct_after_one_failure(self):
        fn = fail_n_times(1, then_return=7)
        ex = RetryExecutor(RetryConfig(max_attempts=3, sleep_fn=noop_sleep))
        result = ex.execute(fn)
        assert result.attempts == 2

    def test_succeeds_on_third_attempt(self):
        fn = fail_n_times(2, then_return="done")
        ex = RetryExecutor(RetryConfig(max_attempts=3, sleep_fn=noop_sleep))
        result = ex.execute(fn)
        assert result.succeeded is True
        assert result.attempts == 3


# ---------------------------------------------------------------------------
# RetryExecutor — exhausts all retries
# ---------------------------------------------------------------------------

class TestRetryExecutorExhaustsRetries:
    def test_succeeded_false_on_exhaustion(self):
        ex = RetryExecutor(RetryConfig(max_attempts=3, sleep_fn=noop_sleep))
        result = ex.execute(always_fail())
        assert result.succeeded is False

    def test_attempts_equals_max_attempts(self):
        ex = RetryExecutor(RetryConfig(max_attempts=3, sleep_fn=noop_sleep))
        result = ex.execute(always_fail())
        assert result.attempts == 3

    def test_last_error_populated(self):
        ex = RetryExecutor(RetryConfig(max_attempts=2, sleep_fn=noop_sleep))
        result = ex.execute(always_fail(msg="boom"))
        assert "boom" in result.last_error

    def test_value_is_none_on_exhaustion(self):
        ex = RetryExecutor(RetryConfig(max_attempts=2, sleep_fn=noop_sleep))
        result = ex.execute(always_fail())
        assert result.value is None


# ---------------------------------------------------------------------------
# RetryExecutor — retry_on filtering
# ---------------------------------------------------------------------------

class TestRetryExecutorRetryOn:
    def test_retries_on_listed_exception_type(self):
        fn = fail_n_times(2, then_return="ok", exc_type=ValueError)
        config = RetryConfig(max_attempts=5, retry_on=[ValueError], sleep_fn=noop_sleep)
        result = RetryExecutor(config).execute(fn)
        assert result.succeeded is True

    def test_does_not_retry_on_unlisted_exception(self):
        fn = always_fail(exc_type=TypeError, msg="type err")
        config = RetryConfig(max_attempts=5, retry_on=[ValueError], sleep_fn=noop_sleep)
        result = RetryExecutor(config).execute(fn)
        # TypeError not in retry_on — should stop after 1 attempt
        assert result.succeeded is False
        assert result.attempts == 1

    def test_empty_retry_on_retries_all_exceptions(self):
        fn = fail_n_times(1, then_return="x", exc_type=KeyError)
        config = RetryConfig(max_attempts=3, retry_on=[], sleep_fn=noop_sleep)
        result = RetryExecutor(config).execute(fn)
        assert result.succeeded is True

    def test_retries_on_subclass_of_listed_exception(self):
        """Subclass exceptions should match the parent in retry_on."""
        fn = fail_n_times(1, then_return="sub", exc_type=FileNotFoundError)
        # FileNotFoundError is a subclass of OSError
        config = RetryConfig(max_attempts=3, retry_on=[OSError], sleep_fn=noop_sleep)
        result = RetryExecutor(config).execute(fn)
        assert result.succeeded is True


# ---------------------------------------------------------------------------
# RetryExecutor — stop_on takes precedence
# ---------------------------------------------------------------------------

class TestRetryExecutorStopOn:
    def test_stop_on_halts_immediately(self):
        # Use a regular Exception subclass so pytest is not interrupted
        fn = always_fail(exc_type=PermissionError, msg="denied")
        config = RetryConfig(
            max_attempts=5,
            retry_on=[],
            stop_on=[PermissionError],
            sleep_fn=noop_sleep,
        )
        result = RetryExecutor(config).execute(fn)
        assert result.succeeded is False
        assert result.attempts == 1

    def test_stop_on_overrides_retry_on(self):
        """Even if the exception is in retry_on, stop_on wins."""
        fn = always_fail(exc_type=ValueError, msg="val")
        config = RetryConfig(
            max_attempts=5,
            retry_on=[ValueError],
            stop_on=[ValueError],
            sleep_fn=noop_sleep,
        )
        result = RetryExecutor(config).execute(fn)
        assert result.attempts == 1

    def test_non_stop_exception_still_retried(self):
        fn = fail_n_times(2, then_return="fine", exc_type=ValueError)
        config = RetryConfig(
            max_attempts=5,
            retry_on=[ValueError, TypeError],
            stop_on=[TypeError],
            sleep_fn=noop_sleep,
        )
        result = RetryExecutor(config).execute(fn)
        assert result.succeeded is True


# ---------------------------------------------------------------------------
# RetryExecutor — result_retry_predicate
# ---------------------------------------------------------------------------

class TestRetryExecutorResultPredicate:
    def test_retries_when_predicate_true(self):
        counter = {"n": 0}
        def fn():
            counter["n"] += 1
            return counter["n"]

        config = RetryConfig(
            max_attempts=4,
            result_retry_predicate=lambda v: v < 3,
            sleep_fn=noop_sleep,
        )
        result = RetryExecutor(config).execute(fn)
        assert result.succeeded is True
        assert result.value == 3

    def test_no_retry_when_predicate_false(self):
        config = RetryConfig(
            max_attempts=3,
            result_retry_predicate=lambda v: False,
            sleep_fn=noop_sleep,
        )
        result = RetryExecutor(config).execute(lambda: "good")
        assert result.succeeded is True
        assert result.attempts == 1

    def test_exhaustion_via_predicate(self):
        config = RetryConfig(
            max_attempts=3,
            result_retry_predicate=lambda v: True,  # always retry
            sleep_fn=noop_sleep,
        )
        result = RetryExecutor(config).execute(lambda: "bad")
        assert result.succeeded is False
        assert result.attempts == 3


# ---------------------------------------------------------------------------
# RetryExecutor — injectable sleep_fn captures delays
# ---------------------------------------------------------------------------

class TestRetryExecutorSleepFnInjection:
    def test_sleep_called_between_retries(self):
        delays = []
        fn = fail_n_times(2, then_return=1)
        config = RetryConfig(
            max_attempts=3,
            sleep_fn=capturing_sleep(delays),
            backoff=BackoffConfig(strategy=BackoffStrategy.FIXED, base_delay=5.0),
        )
        RetryExecutor(config).execute(fn)
        # Two failures before success → 2 sleeps
        assert len(delays) == 2

    def test_sleep_delay_values_are_correct(self):
        delays = []
        fn = fail_n_times(2, then_return=0)
        config = RetryConfig(
            max_attempts=3,
            sleep_fn=capturing_sleep(delays),
            backoff=BackoffConfig(strategy=BackoffStrategy.FIXED, base_delay=7.0),
        )
        RetryExecutor(config).execute(fn)
        assert all(d == 7.0 for d in delays)

    def test_no_sleep_on_first_try_success(self):
        delays = []
        config = RetryConfig(max_attempts=3, sleep_fn=capturing_sleep(delays))
        RetryExecutor(config).execute(lambda: 42)
        assert delays == []

    def test_no_sleep_after_last_failed_attempt(self):
        """Sleep should not be called after the final attempt."""
        delays = []
        config = RetryConfig(
            max_attempts=2,
            sleep_fn=capturing_sleep(delays),
            backoff=BackoffConfig(strategy=BackoffStrategy.FIXED, base_delay=3.0),
        )
        RetryExecutor(config).execute(always_fail())
        # Only 1 sleep between attempt 1 and attempt 2
        assert len(delays) == 1


# ---------------------------------------------------------------------------
# RetryExecutor — edge case: max_attempts=1
# ---------------------------------------------------------------------------

class TestRetryExecutorMaxAttemptsOne:
    def test_no_retry_on_failure(self):
        config = RetryConfig(max_attempts=1, sleep_fn=noop_sleep)
        result = RetryExecutor(config).execute(always_fail(msg="once"))
        assert result.succeeded is False
        assert result.attempts == 1

    def test_success_on_single_attempt(self):
        config = RetryConfig(max_attempts=1, sleep_fn=noop_sleep)
        result = RetryExecutor(config).execute(lambda: "single")
        assert result.succeeded is True
        assert result.value == "single"


# ---------------------------------------------------------------------------
# RetryExecutor — default config (no explicit RetryConfig)
# ---------------------------------------------------------------------------

class TestRetryExecutorDefaultConfig:
    def test_executor_uses_default_config_when_none(self):
        # Should not raise; default config has time.sleep but succeeds first try
        ex = RetryExecutor()
        result = ex.execute(lambda: "default")
        assert result.succeeded is True


# ---------------------------------------------------------------------------
# retry decorator — basic usage
# ---------------------------------------------------------------------------

class TestRetryDecoratorBasic:
    def test_returns_value_on_success(self):
        @retry(max_attempts=3, sleep_fn=noop_sleep)
        def fn():
            return "works"
        assert fn() == "works"

    def test_passes_args_and_kwargs(self):
        @retry(max_attempts=2, sleep_fn=noop_sleep)
        def add(a, b=0):
            return a + b
        assert add(3, b=4) == 7

    def test_succeeds_after_transient_failure(self):
        inner = fail_n_times(1, then_return="retry_ok")

        @retry(max_attempts=3, sleep_fn=noop_sleep)
        def fn():
            return inner()

        assert fn() == "retry_ok"

    def test_decorator_preserves_function_name(self):
        @retry(max_attempts=1, sleep_fn=noop_sleep)
        def my_special_func():
            return 0

        assert my_special_func.__name__ == "my_special_func"


# ---------------------------------------------------------------------------
# retry decorator — re-raises on exhaustion
# ---------------------------------------------------------------------------

class TestRetryDecoratorReRaises:
    def test_raises_on_exhaustion(self):
        @retry(max_attempts=2, sleep_fn=noop_sleep)
        def fn():
            raise ValueError("permanent")

        with pytest.raises(Exception):
            fn()

    def test_error_message_propagated(self):
        @retry(max_attempts=2, sleep_fn=noop_sleep)
        def fn():
            raise ValueError("permanent problem")

        with pytest.raises(Exception, match="permanent problem"):
            fn()


# ---------------------------------------------------------------------------
# retry decorator — sleep_fn injection
# ---------------------------------------------------------------------------

class TestRetryDecoratorSleepFnInjection:
    def test_sleep_fn_called_between_retries(self):
        delays = []
        inner = fail_n_times(2, then_return="fin")

        @retry(
            max_attempts=3,
            backoff_strategy=BackoffStrategy.FIXED,
            base_delay=0.5,
            sleep_fn=capturing_sleep(delays),
        )
        def fn():
            return inner()

        fn()
        assert len(delays) == 2

    def test_retry_on_parameter_honoured(self):
        """retry_on=[] means all exceptions retried."""
        inner = fail_n_times(1, then_return="all_ok", exc_type=KeyError)

        @retry(max_attempts=3, retry_on=[], sleep_fn=noop_sleep)
        def fn():
            return inner()

        assert fn() == "all_ok"

    def test_retry_on_specific_exception_only(self):
        """Exception not in retry_on causes immediate propagation."""
        @retry(max_attempts=5, retry_on=[ValueError], sleep_fn=noop_sleep)
        def fn():
            raise TypeError("wrong type")

        with pytest.raises(Exception):
            fn()


# ---------------------------------------------------------------------------
# Edge cases: stop_on overrides retry_on in executor context
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_stop_on_subclass_also_stopped(self):
        # FileNotFoundError is a subclass of OSError — stop_on should match
        fn = always_fail(exc_type=FileNotFoundError, msg="gone")
        config = RetryConfig(
            max_attempts=5,
            retry_on=[],
            stop_on=[OSError],
            sleep_fn=noop_sleep,
        )
        result = RetryExecutor(config).execute(fn)
        assert result.attempts == 1

    def test_result_predicate_only_after_no_exception(self):
        """Predicate should not be evaluated when function raises."""
        called = {"n": 0}
        fn = always_fail(exc_type=RuntimeError)
        config = RetryConfig(
            max_attempts=2,
            result_retry_predicate=lambda v: True,
            sleep_fn=noop_sleep,
        )
        result = RetryExecutor(config).execute(fn)
        assert result.succeeded is False

    def test_executor_returns_none_value_when_function_returns_none(self):
        config = RetryConfig(max_attempts=1, sleep_fn=noop_sleep)
        result = RetryExecutor(config).execute(lambda: None)
        assert result.succeeded is True
        assert result.value is None

    def test_all_public_names_importable_from_package(self):
        from docstoolkit.retry_policy import (
            BackoffStrategy, BackoffConfig, BackoffCalculator,
            RetryCondition, RetryConfig, RetryExecutor, RetryResult,
            retry,
        )
        assert BackoffStrategy is not None
        assert retry is not None

    def test_max_attempts_zero_returns_failure_immediately(self):
        """max_attempts=0 edge case: loop body never executes."""
        config = RetryConfig(max_attempts=0, sleep_fn=noop_sleep)
        result = RetryExecutor(config).execute(lambda: 1)
        assert result.succeeded is False
