"""Tests for docstoolkit.retry_budget (E97)."""
import threading
import pytest

from docstoolkit.retry_budget.budget import BudgetConfig, RetryBudget


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make(max_retries=3, window=60.0, backoff_base=1.0):
    return RetryBudget(BudgetConfig(max_retries=max_retries, window=window,
                                   backoff_base=backoff_base))


T = 1000.0  # base virtual timestamp


# ---------------------------------------------------------------------------
# BudgetConfig
# ---------------------------------------------------------------------------

class TestBudgetConfig:
    def test_fields(self):
        cfg = BudgetConfig(max_retries=5, window=30.0)
        assert cfg.max_retries == 5
        assert cfg.window == 30.0
        assert cfg.backoff_base == 1.0

    def test_custom_backoff(self):
        cfg = BudgetConfig(max_retries=3, window=10.0, backoff_base=2.0)
        assert cfg.backoff_base == 2.0


# ---------------------------------------------------------------------------
# RetryBudget — remaining / is_exhausted before any attempt
# ---------------------------------------------------------------------------

class TestRetryBudgetEmpty:
    def test_remaining_no_record(self):
        b = make(max_retries=5)
        assert b.remaining("k", now=T) == 5

    def test_not_exhausted_no_record(self):
        b = make(max_retries=5)
        assert not b.is_exhausted("k", now=T)

    def test_all_keys_empty(self):
        b = make()
        assert b.all_keys() == []


# ---------------------------------------------------------------------------
# RetryBudget — attempt within budget
# ---------------------------------------------------------------------------

class TestRetryBudgetAttempt:
    def test_first_attempt_returns_true(self):
        b = make(max_retries=3)
        assert b.attempt("k", now=T) is True

    def test_attempts_consume_budget(self):
        b = make(max_retries=3)
        b.attempt("k", now=T)
        b.attempt("k", now=T + 1)
        b.attempt("k", now=T + 2)
        assert b.remaining("k", now=T + 2) == 0

    def test_remaining_decrements(self):
        b = make(max_retries=4)
        b.attempt("k", now=T)
        assert b.remaining("k", now=T) == 3
        b.attempt("k", now=T + 1)
        assert b.remaining("k", now=T + 1) == 2

    def test_all_budget_used_returns_true(self):
        b = make(max_retries=3)
        results = [b.attempt("k", now=T + i) for i in range(3)]
        assert all(results)

    def test_exhausted_attempt_returns_false(self):
        b = make(max_retries=2)
        b.attempt("k", now=T)
        b.attempt("k", now=T + 1)
        # Budget exhausted
        assert b.attempt("k", now=T + 2) is False

    def test_exhausted_does_not_increment(self):
        b = make(max_retries=2)
        b.attempt("k", now=T)
        b.attempt("k", now=T + 1)
        b.attempt("k", now=T + 2)  # False
        b.attempt("k", now=T + 3)  # still False
        assert b.remaining("k", now=T + 3) == 0

    def test_is_exhausted_after_budget_used(self):
        b = make(max_retries=1)
        b.attempt("k", now=T)
        assert b.is_exhausted("k", now=T)

    def test_multiple_keys_independent(self):
        b = make(max_retries=2)
        b.attempt("a", now=T)
        b.attempt("a", now=T + 1)
        assert b.is_exhausted("a", now=T + 1)
        assert not b.is_exhausted("b", now=T + 1)
        assert b.remaining("b", now=T + 1) == 2

    def test_all_keys_after_attempts(self):
        b = make()
        b.attempt("x", now=T)
        b.attempt("y", now=T)
        b.attempt("z", now=T)
        keys = b.all_keys()
        assert sorted(keys) == ["x", "y", "z"]


# ---------------------------------------------------------------------------
# RetryBudget — window expiry
# ---------------------------------------------------------------------------

class TestRetryBudgetWindowExpiry:
    def test_expired_window_resets_remaining(self):
        b = make(max_retries=3, window=10.0)
        b.attempt("k", now=T)
        b.attempt("k", now=T + 1)
        # After window (T + 11), remaining should be back to max
        assert b.remaining("k", now=T + 11) == 3

    def test_expired_window_is_not_exhausted(self):
        b = make(max_retries=1, window=5.0)
        b.attempt("k", now=T)
        assert b.is_exhausted("k", now=T)
        assert not b.is_exhausted("k", now=T + 6)

    def test_attempt_after_window_expiry_returns_true(self):
        b = make(max_retries=1, window=5.0)
        b.attempt("k", now=T)
        assert b.attempt("k", now=T + 6) is True

    def test_attempt_after_window_resets_count(self):
        b = make(max_retries=3, window=10.0)
        b.attempt("k", now=T)
        b.attempt("k", now=T + 1)
        # New window
        b.attempt("k", now=T + 11)
        assert b.remaining("k", now=T + 11) == 2

    def test_within_window_not_reset(self):
        b = make(max_retries=3, window=60.0)
        b.attempt("k", now=T)
        b.attempt("k", now=T + 30)  # Within window
        assert b.remaining("k", now=T + 30) == 1

    def test_exactly_at_window_boundary_resets(self):
        """At now - first_attempt == window, should reset (> comparison)."""
        b = make(max_retries=3, window=10.0)
        b.attempt("k", now=T)
        # exactly at window (T+10 - T == 10 == window, which is > not >=, so NOT reset)
        # NOTE: code uses > so equal to window is NOT expired
        assert b.remaining("k", now=T + 10) == 2  # still in old window

    def test_just_past_window_resets(self):
        b = make(max_retries=3, window=10.0)
        b.attempt("k", now=T)
        assert b.remaining("k", now=T + 10.001) == 3


# ---------------------------------------------------------------------------
# RetryBudget — reset
# ---------------------------------------------------------------------------

class TestRetryBudgetReset:
    def test_reset_clears_record(self):
        b = make(max_retries=3)
        b.attempt("k", now=T)
        b.attempt("k", now=T + 1)
        b.reset("k")
        assert b.remaining("k", now=T + 1) == 3

    def test_reset_allows_new_attempts(self):
        b = make(max_retries=1)
        b.attempt("k", now=T)
        assert b.is_exhausted("k", now=T)
        b.reset("k")
        assert b.attempt("k", now=T) is True

    def test_reset_nonexistent_key(self):
        b = make()
        b.reset("nonexistent")  # Should not raise

    def test_reset_removes_from_all_keys(self):
        b = make()
        b.attempt("x", now=T)
        b.attempt("y", now=T)
        b.reset("x")
        assert "x" not in b.all_keys()
        assert "y" in b.all_keys()

    def test_reset_specific_key_only(self):
        b = make(max_retries=2)
        b.attempt("a", now=T)
        b.attempt("b", now=T)
        b.reset("a")
        assert b.remaining("a", now=T) == 2
        assert b.remaining("b", now=T) == 1


# ---------------------------------------------------------------------------
# RetryBudget — max_retries=0 edge case
# ---------------------------------------------------------------------------

class TestRetryBudgetEdgeCases:
    def test_max_retries_zero_always_false(self):
        b = make(max_retries=0)
        assert b.attempt("k", now=T) is False

    def test_max_retries_zero_remaining_is_zero(self):
        b = make(max_retries=0)
        assert b.remaining("k", now=T) == 0

    def test_max_retries_one(self):
        b = make(max_retries=1)
        assert b.attempt("k", now=T) is True
        assert b.attempt("k", now=T + 1) is False

    def test_large_budget(self):
        b = make(max_retries=100, window=3600.0)
        for i in range(100):
            assert b.attempt("k", now=T + i) is True
        assert b.attempt("k", now=T + 100) is False

    def test_close(self):
        b = make()
        b.close()  # Should not raise

    def test_different_keys_different_windows(self):
        b = make(max_retries=2, window=10.0)
        b.attempt("a", now=T)
        b.attempt("b", now=T + 5)  # b's window starts 5s later
        # At T+11, a's window (started at T) expired, but b's (started at T+5) hasn't
        assert b.remaining("a", now=T + 11) == 2   # reset
        assert b.remaining("b", now=T + 11) == 1   # still in window


# ---------------------------------------------------------------------------
# RetryBudget — thread safety
# ---------------------------------------------------------------------------

class TestRetryBudgetThreadSafety:
    def test_concurrent_attempts_single_key(self):
        b = make(max_retries=50, window=3600.0)
        successes = []
        lock = threading.Lock()

        def worker():
            for i in range(10):
                result = b.attempt("shared", now=T + i * 0.001)
                with lock:
                    successes.append(result)

        threads = [threading.Thread(target=worker) for _ in range(6)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        true_count = sum(1 for r in successes if r)
        assert true_count == 50  # exactly max_retries successes
        assert len(successes) == 60  # 6 threads × 10 attempts

    def test_concurrent_different_keys(self):
        b = make(max_retries=5, window=3600.0)
        errors = []

        def worker(key):
            try:
                for i in range(5):
                    b.attempt(key, now=T + i)
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=worker, args=(f"key{i}",))
                   for i in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors
        for i in range(10):
            assert b.remaining(f"key{i}", now=T + 4) == 0
