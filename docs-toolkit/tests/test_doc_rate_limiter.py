"""Tests for E280 DocRateLimiter."""
import threading
from docstoolkit.doc_rate_limiter import AllowResult, DocRateLimiter, RateLimit, RateLimiterStats

T0 = 1_700_000_000.0


def _limiter() -> DocRateLimiter:
    return DocRateLimiter()


# ---------------------------------------------------------------------------
# configure
# ---------------------------------------------------------------------------


def test_configure_returns_rate_limit():
    r = _limiter()
    rl = r.configure("doc:1", capacity=5.0, refill_rate=1.0, now=T0)
    assert isinstance(rl, RateLimit)


def test_configure_stores_capacity():
    r = _limiter()
    r.configure("doc:1", capacity=5.0, refill_rate=1.0, now=T0)
    rl = r.get_limit("doc:1")
    assert rl.capacity == 5.0


def test_configure_stores_refill_rate():
    r = _limiter()
    r.configure("doc:1", capacity=5.0, refill_rate=2.0, now=T0)
    rl = r.get_limit("doc:1")
    assert rl.refill_rate == 2.0


def test_configure_starts_at_full_capacity():
    r = _limiter()
    r.configure("doc:1", capacity=10.0, refill_rate=1.0, now=T0)
    rl = r.get_limit("doc:1")
    assert rl.current_tokens == 10.0


def test_configure_overwrites_existing():
    r = _limiter()
    r.configure("doc:1", capacity=5.0, refill_rate=1.0, now=T0)
    r.configure("doc:1", capacity=20.0, refill_rate=2.0, now=T0)
    rl = r.get_limit("doc:1")
    assert rl.capacity == 20.0
    assert rl.refill_rate == 2.0


def test_configure_sets_last_refill_at():
    r = _limiter()
    r.configure("doc:1", capacity=5.0, refill_rate=1.0, now=T0)
    rl = r.get_limit("doc:1")
    assert rl.last_refill_at == T0


# ---------------------------------------------------------------------------
# allow — basic
# ---------------------------------------------------------------------------


def test_allow_returns_allow_result():
    r = _limiter()
    result = r.allow("doc:1", now=T0)
    assert isinstance(result, AllowResult)


def test_allow_first_call_is_allowed():
    r = _limiter()
    result = r.allow("doc:1", now=T0)
    assert result.allowed is True


def test_allow_wait_seconds_zero_when_allowed():
    r = _limiter()
    result = r.allow("doc:1", now=T0)
    assert result.wait_seconds == 0.0


def test_allow_reduces_tokens():
    r = _limiter()
    r.configure("doc:1", capacity=5.0, refill_rate=1.0, now=T0)
    r.allow("doc:1", tokens=2.0, now=T0)
    rl = r.get_limit("doc:1")
    assert rl.current_tokens == 3.0


def test_allow_denied_when_insufficient_tokens():
    r = _limiter()
    r.configure("doc:1", capacity=2.0, refill_rate=1.0, now=T0)
    r.allow("doc:1", tokens=2.0, now=T0)
    result = r.allow("doc:1", tokens=1.0, now=T0)
    assert result.allowed is False


def test_allow_denied_tokens_remaining_unchanged():
    r = _limiter()
    r.configure("doc:1", capacity=1.0, refill_rate=1.0, now=T0)
    r.allow("doc:1", tokens=1.0, now=T0)
    result = r.allow("doc:1", tokens=1.0, now=T0)
    assert result.tokens_remaining == 0.0


def test_allow_wait_seconds_positive_when_denied():
    r = _limiter()
    r.configure("doc:1", capacity=1.0, refill_rate=1.0, now=T0)
    r.allow("doc:1", tokens=1.0, now=T0)
    result = r.allow("doc:1", tokens=1.0, now=T0)
    assert result.wait_seconds > 0.0


def test_allow_wait_seconds_formula():
    r = _limiter()
    r.configure("doc:1", capacity=2.0, refill_rate=2.0, now=T0)
    r.allow("doc:1", tokens=2.0, now=T0)
    result = r.allow("doc:1", tokens=1.0, now=T0)
    assert abs(result.wait_seconds - 0.5) < 1e-9


def test_allow_key_stored_in_result():
    r = _limiter()
    result = r.allow("mykey", now=T0)
    assert result.key == "mykey"


# ---------------------------------------------------------------------------
# auto-configure on first allow
# ---------------------------------------------------------------------------


def test_allow_auto_configures_unknown_key():
    r = _limiter()
    r.allow("newkey", now=T0)
    assert r.get_limit("newkey") is not None


def test_allow_auto_configured_capacity_is_10():
    r = _limiter()
    r.allow("newkey", now=T0)
    assert r.get_limit("newkey").capacity == 10.0


def test_allow_auto_configured_refill_rate_is_1():
    r = _limiter()
    r.allow("newkey", now=T0)
    assert r.get_limit("newkey").refill_rate == 1.0


# ---------------------------------------------------------------------------
# refill over time
# ---------------------------------------------------------------------------


def test_allow_refills_over_time():
    r = _limiter()
    r.configure("doc:1", capacity=2.0, refill_rate=1.0, now=T0)
    r.allow("doc:1", tokens=2.0, now=T0)
    # 2 seconds later → refill 2 tokens
    result = r.allow("doc:1", tokens=2.0, now=T0 + 2.0)
    assert result.allowed is True


def test_allow_partial_refill():
    r = _limiter()
    r.configure("doc:1", capacity=10.0, refill_rate=1.0, now=T0)
    r.allow("doc:1", tokens=10.0, now=T0)
    # 3 seconds later → 3 tokens refilled
    result = r.allow("doc:1", tokens=3.0, now=T0 + 3.0)
    assert result.allowed is True


def test_refill_does_not_exceed_capacity():
    r = _limiter()
    r.configure("doc:1", capacity=5.0, refill_rate=100.0, now=T0)
    r.allow("doc:1", tokens=5.0, now=T0)
    # huge time gap
    r.allow("doc:1", tokens=0.0, now=T0 + 1000.0)
    rl = r.get_limit("doc:1")
    assert rl.current_tokens <= 5.0


# ---------------------------------------------------------------------------
# reset
# ---------------------------------------------------------------------------


def test_reset_returns_true_for_known_key():
    r = _limiter()
    r.configure("doc:1", capacity=5.0, refill_rate=1.0, now=T0)
    assert r.reset("doc:1", now=T0) is True


def test_reset_refills_to_capacity():
    r = _limiter()
    r.configure("doc:1", capacity=5.0, refill_rate=1.0, now=T0)
    r.allow("doc:1", tokens=5.0, now=T0)
    r.reset("doc:1", now=T0 + 1)
    rl = r.get_limit("doc:1")
    assert rl.current_tokens == 5.0


def test_reset_returns_false_for_unknown_key():
    r = _limiter()
    assert r.reset("no-such", now=T0) is False


# ---------------------------------------------------------------------------
# delete
# ---------------------------------------------------------------------------


def test_delete_returns_true_for_existing():
    r = _limiter()
    r.configure("doc:1", capacity=5.0, refill_rate=1.0, now=T0)
    assert r.delete("doc:1") is True


def test_delete_removes_key():
    r = _limiter()
    r.configure("doc:1", capacity=5.0, refill_rate=1.0, now=T0)
    r.delete("doc:1")
    assert r.get_limit("doc:1") is None


def test_delete_returns_false_for_missing():
    r = _limiter()
    assert r.delete("no-such") is False


# ---------------------------------------------------------------------------
# get_limit
# ---------------------------------------------------------------------------


def test_get_limit_returns_rate_limit():
    r = _limiter()
    r.configure("doc:1", capacity=3.0, refill_rate=0.5, now=T0)
    rl = r.get_limit("doc:1")
    assert isinstance(rl, RateLimit)


def test_get_limit_missing_returns_none():
    r = _limiter()
    assert r.get_limit("no-such") is None


# ---------------------------------------------------------------------------
# keys
# ---------------------------------------------------------------------------


def test_keys_returns_sorted():
    r = _limiter()
    r.configure("b", capacity=1.0, refill_rate=1.0, now=T0)
    r.configure("a", capacity=1.0, refill_rate=1.0, now=T0)
    assert r.keys() == ["a", "b"]


def test_keys_empty_initially():
    r = _limiter()
    assert r.keys() == []


def test_keys_after_delete():
    r = _limiter()
    r.configure("a", capacity=1.0, refill_rate=1.0, now=T0)
    r.delete("a")
    assert r.keys() == []


def test_keys_auto_configured_appear():
    r = _limiter()
    r.allow("auto", now=T0)
    assert "auto" in r.keys()


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------


def test_stats_returns_rate_limiter_stats():
    r = _limiter()
    assert isinstance(r.stats(), RateLimiterStats)


def test_stats_total_allowed():
    r = _limiter()
    r.allow("k", now=T0)
    r.allow("k", now=T0 + 1)
    assert r.stats().total_allowed == 2


def test_stats_total_denied():
    r = _limiter()
    r.configure("k", capacity=1.0, refill_rate=1.0, now=T0)
    r.allow("k", tokens=1.0, now=T0)
    r.allow("k", tokens=1.0, now=T0)
    assert r.stats().total_denied == 1


def test_stats_allow_rate_all_allowed():
    r = _limiter()
    r.allow("k", now=T0)
    assert r.stats().allow_rate == 1.0


def test_stats_allow_rate_mixed():
    r = _limiter()
    r.configure("k", capacity=1.0, refill_rate=1.0, now=T0)
    r.allow("k", tokens=1.0, now=T0)   # allowed
    r.allow("k", tokens=1.0, now=T0)   # denied
    st = r.stats()
    assert abs(st.allow_rate - 0.5) < 1e-9


def test_stats_allow_rate_no_calls_is_1():
    r = _limiter()
    assert r.stats().allow_rate == 1.0


def test_stats_total_keys():
    r = _limiter()
    r.configure("a", capacity=1.0, refill_rate=1.0, now=T0)
    r.configure("b", capacity=1.0, refill_rate=1.0, now=T0)
    assert r.stats().total_keys == 2


# ---------------------------------------------------------------------------
# total_keys property
# ---------------------------------------------------------------------------


def test_total_keys_property():
    r = _limiter()
    r.configure("a", capacity=1.0, refill_rate=1.0, now=T0)
    assert r.total_keys == 1


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------


def test_concurrent_allow():
    r = _limiter()
    r.configure("shared", capacity=1000.0, refill_rate=0.0, now=T0)
    errors = []

    def worker():
        try:
            for _ in range(20):
                r.allow("shared", tokens=1.0, now=T0)
        except Exception as exc:
            errors.append(exc)

    threads = [threading.Thread(target=worker) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert not errors
    st = r.stats()
    assert st.total_allowed + st.total_denied == 100


# ---------------------------------------------------------------------------
# Additional edge cases
# ---------------------------------------------------------------------------


def test_allow_tokens_remaining_in_allow_result():
    r = _limiter()
    r.configure("doc:1", capacity=8.0, refill_rate=1.0, now=T0)
    result = r.allow("doc:1", tokens=3.0, now=T0)
    assert result.tokens_remaining == 5.0


def test_reset_updates_last_refill_at():
    r = _limiter()
    r.configure("doc:1", capacity=5.0, refill_rate=1.0, now=T0)
    r.reset("doc:1", now=T0 + 50.0)
    rl = r.get_limit("doc:1")
    assert rl.last_refill_at == T0 + 50.0


def test_delete_then_auto_reconfigure_on_allow():
    r = _limiter()
    r.configure("doc:1", capacity=3.0, refill_rate=1.0, now=T0)
    r.delete("doc:1")
    result = r.allow("doc:1", tokens=1.0, now=T0)
    assert result.allowed is True
    assert r.get_limit("doc:1").capacity == 10.0
