"""Tests for the object_pool module — 90+ tests covering all spec requirements."""
from __future__ import annotations

import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import pytest

from docstoolkit.object_pool import (
    ObjectPool,
    PoolConfig,
    PoolExhausted,
    PooledObject,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


class _Counter:
    """Thread-safe counting factory."""

    def __init__(self, start: int = 0):
        self._n = start
        self._lock = threading.Lock()

    def __call__(self):
        with self._lock:
            self._n += 1
            return self._n


def _make_pool(
    factory=None,
    *,
    min_size=0,
    max_size=10,
    max_idle_time=0.0,
    validate_on_acquire=True,
    validate_on_release=False,
    validator=None,
    destroyer=None,
):
    cfg = PoolConfig(
        min_size=min_size,
        max_size=max_size,
        max_idle_time=max_idle_time,
        validate_on_acquire=validate_on_acquire,
        validate_on_release=validate_on_release,
    )
    return ObjectPool(
        factory=factory or _Counter(),
        config=cfg,
        validator=validator,
        destroyer=destroyer,
    )


# ---------------------------------------------------------------------------
# 1. PoolConfig dataclass
# ---------------------------------------------------------------------------


class TestPoolConfig:
    def test_default_min_size(self):
        assert PoolConfig().min_size == 0

    def test_default_max_size(self):
        assert PoolConfig().max_size == 10

    def test_default_max_idle_time(self):
        assert PoolConfig().max_idle_time == 0.0

    def test_default_validate_on_acquire_true(self):
        assert PoolConfig().validate_on_acquire is True

    def test_default_validate_on_release_false(self):
        assert PoolConfig().validate_on_release is False

    def test_custom_min_size(self):
        assert PoolConfig(min_size=3).min_size == 3

    def test_custom_max_size(self):
        assert PoolConfig(max_size=42).max_size == 42

    def test_custom_max_idle_time(self):
        assert PoolConfig(max_idle_time=12.5).max_idle_time == 12.5

    def test_validate_on_acquire_can_be_false(self):
        assert PoolConfig(validate_on_acquire=False).validate_on_acquire is False

    def test_validate_on_release_can_be_true(self):
        assert PoolConfig(validate_on_release=True).validate_on_release is True

    def test_is_dataclass(self):
        from dataclasses import is_dataclass

        assert is_dataclass(PoolConfig)


# ---------------------------------------------------------------------------
# 2. PooledObject dataclass
# ---------------------------------------------------------------------------


class TestPooledObject:
    def test_holds_underlying_obj(self):
        po = PooledObject(obj="resource")
        assert po.obj == "resource"

    def test_default_use_count_zero(self):
        po = PooledObject(obj=object())
        assert po.use_count == 0

    def test_default_created_at_is_recent(self):
        before = time.monotonic()
        po = PooledObject(obj=object())
        after = time.monotonic()
        assert before <= po.created_at <= after

    def test_default_last_used_at_is_recent(self):
        before = time.monotonic()
        po = PooledObject(obj=object())
        after = time.monotonic()
        assert before <= po.last_used_at <= after

    def test_custom_use_count(self):
        po = PooledObject(obj=1, use_count=5)
        assert po.use_count == 5

    def test_custom_created_at(self):
        po = PooledObject(obj=1, created_at=100.0)
        assert po.created_at == 100.0

    def test_custom_last_used_at(self):
        po = PooledObject(obj=1, last_used_at=200.0)
        assert po.last_used_at == 200.0

    def test_can_mutate_use_count(self):
        po = PooledObject(obj=1)
        po.use_count += 1
        assert po.use_count == 1

    def test_is_dataclass(self):
        from dataclasses import is_dataclass

        assert is_dataclass(PooledObject)


# ---------------------------------------------------------------------------
# 3. PoolExhausted exception
# ---------------------------------------------------------------------------


class TestPoolExhausted:
    def test_is_exception(self):
        assert issubclass(PoolExhausted, Exception)

    def test_raised_with_message(self):
        with pytest.raises(PoolExhausted, match="boom"):
            raise PoolExhausted("boom")

    def test_can_be_caught_as_exception(self):
        try:
            raise PoolExhausted("x")
        except Exception as e:
            assert isinstance(e, PoolExhausted)


# ---------------------------------------------------------------------------
# 4. ObjectPool construction and validation
# ---------------------------------------------------------------------------


class TestObjectPoolInit:
    def test_factory_required(self):
        with pytest.raises((TypeError, ValueError)):
            ObjectPool(factory=None)

    def test_uses_default_config(self):
        pool = ObjectPool(factory=lambda: 1)
        assert pool._config.max_size == 10
        assert pool._config.min_size == 0

    def test_accepts_explicit_config(self):
        cfg = PoolConfig(max_size=3)
        pool = ObjectPool(factory=lambda: 1, config=cfg)
        assert pool._config is cfg

    def test_rejects_negative_min_size(self):
        with pytest.raises(ValueError):
            ObjectPool(factory=lambda: 1, config=PoolConfig(min_size=-1))

    def test_rejects_zero_max_size(self):
        with pytest.raises(ValueError):
            ObjectPool(factory=lambda: 1, config=PoolConfig(max_size=0))

    def test_rejects_min_greater_than_max(self):
        with pytest.raises(ValueError):
            ObjectPool(
                factory=lambda: 1,
                config=PoolConfig(min_size=5, max_size=3),
            )

    def test_initial_size_is_zero(self):
        assert _make_pool().size() == 0

    def test_initial_idle_count_zero(self):
        assert _make_pool().idle_count() == 0

    def test_initial_in_use_count_zero(self):
        assert _make_pool().in_use_count() == 0

    def test_validator_optional(self):
        pool = ObjectPool(factory=lambda: 1)
        assert pool._validator is None

    def test_destroyer_optional(self):
        pool = ObjectPool(factory=lambda: 1)
        assert pool._destroyer is None


# ---------------------------------------------------------------------------
# 5. acquire(): creates new under max_size
# ---------------------------------------------------------------------------


class TestAcquireCreate:
    def test_returns_pooled_object(self):
        pool = _make_pool()
        po = pool.acquire()
        assert isinstance(po, PooledObject)

    def test_obj_from_factory(self):
        pool = _make_pool(factory=lambda: "hello")
        assert pool.acquire().obj == "hello"

    def test_factory_called_distinct_objects(self):
        pool = _make_pool(factory=_Counter())
        a = pool.acquire().obj
        b = pool.acquire().obj
        assert a != b

    def test_increments_size(self):
        pool = _make_pool()
        pool.acquire()
        assert pool.size() == 1

    def test_increments_in_use(self):
        pool = _make_pool()
        pool.acquire()
        assert pool.in_use_count() == 1

    def test_does_not_increment_idle(self):
        pool = _make_pool()
        pool.acquire()
        assert pool.idle_count() == 0

    def test_use_count_starts_at_one(self):
        pool = _make_pool()
        po = pool.acquire()
        assert po.use_count == 1

    def test_multiple_acquires_under_max(self):
        pool = _make_pool(max_size=5)
        for _ in range(5):
            pool.acquire()
        assert pool.size() == 5


# ---------------------------------------------------------------------------
# 6. acquire(): reuses idle objects
# ---------------------------------------------------------------------------


class TestAcquireReuse:
    def test_reuses_after_release(self):
        pool = _make_pool(factory=_Counter())
        po1 = pool.acquire()
        pool.release(po1)
        po2 = pool.acquire()
        assert po1.obj == po2.obj

    def test_use_count_increments_on_reuse(self):
        pool = _make_pool()
        po = pool.acquire()
        pool.release(po)
        pool.acquire()
        assert po.use_count == 2

    def test_reuse_does_not_grow_size(self):
        pool = _make_pool()
        po = pool.acquire()
        pool.release(po)
        pool.acquire()
        assert pool.size() == 1

    def test_reuse_decreases_idle(self):
        pool = _make_pool()
        po = pool.acquire()
        pool.release(po)
        assert pool.idle_count() == 1
        pool.acquire()
        assert pool.idle_count() == 0

    def test_factory_not_called_on_reuse(self):
        factory = _Counter()
        pool = _make_pool(factory=factory)
        po = pool.acquire()
        pool.release(po)
        before = factory._n
        pool.acquire()
        assert factory._n == before


# ---------------------------------------------------------------------------
# 7. acquire(): PoolExhausted at max_size
# ---------------------------------------------------------------------------


class TestAcquireExhausted:
    def test_raises_at_max_with_no_idle_timeout_zero(self):
        pool = _make_pool(max_size=2)
        pool.acquire()
        pool.acquire()
        with pytest.raises(PoolExhausted):
            pool.acquire(timeout=0)

    def test_raises_at_max_short_timeout(self):
        pool = _make_pool(max_size=1)
        pool.acquire()
        with pytest.raises(PoolExhausted):
            pool.acquire(timeout=0.05)

    def test_timeout_blocks_until_release(self):
        pool = _make_pool(max_size=1)
        po = pool.acquire()

        def releaser():
            time.sleep(0.05)
            pool.release(po)

        t = threading.Thread(target=releaser)
        t.start()
        got = pool.acquire(timeout=2.0)
        t.join()
        assert got is po

    def test_timeout_negative_treated_as_immediate(self):
        pool = _make_pool(max_size=1)
        pool.acquire()
        with pytest.raises(PoolExhausted):
            pool.acquire(timeout=-1)

    def test_no_extra_objects_after_failure(self):
        pool = _make_pool(max_size=1)
        pool.acquire()
        with pytest.raises(PoolExhausted):
            pool.acquire(timeout=0)
        assert pool.size() == 1


# ---------------------------------------------------------------------------
# 8. release(): returns to idle and bookkeeping
# ---------------------------------------------------------------------------


class TestRelease:
    def test_moves_to_idle(self):
        pool = _make_pool()
        po = pool.acquire()
        pool.release(po)
        assert pool.idle_count() == 1
        assert pool.in_use_count() == 0

    def test_total_size_unchanged(self):
        pool = _make_pool()
        po = pool.acquire()
        pool.release(po)
        assert pool.size() == 1

    def test_double_release_is_noop(self):
        pool = _make_pool()
        po = pool.acquire()
        pool.release(po)
        # second release should not change state
        pool.release(po)
        assert pool.idle_count() == 1
        assert pool.in_use_count() == 0

    def test_release_updates_last_used_at(self):
        pool = _make_pool()
        po = pool.acquire()
        old = po.last_used_at
        time.sleep(0.001)
        pool.release(po)
        assert po.last_used_at > old

    def test_release_validates_when_configured(self):
        validator = lambda o: o != "bad"
        destroyed = []
        pool = _make_pool(
            factory=lambda: "bad",
            validate_on_release=True,
            validator=validator,
            destroyer=destroyed.append,
        )
        po = pool.acquire()
        pool.release(po)
        # invalid → destroyed, not idle
        assert pool.idle_count() == 0
        assert destroyed == ["bad"]

    def test_release_skips_validation_when_disabled(self):
        validator = lambda o: False  # always invalid
        pool = _make_pool(
            validate_on_release=False,
            validator=validator,
        )
        po = pool.acquire()
        pool.release(po)
        # validator should NOT have been called
        assert pool.idle_count() == 1


# ---------------------------------------------------------------------------
# 9. destroy()
# ---------------------------------------------------------------------------


class TestDestroy:
    def test_calls_destroyer(self):
        destroyed = []
        pool = _make_pool(destroyer=destroyed.append)
        po = pool.acquire()
        pool.destroy(po)
        assert destroyed == [po.obj]

    def test_removes_from_pool(self):
        pool = _make_pool()
        po = pool.acquire()
        pool.destroy(po)
        assert pool.size() == 0

    def test_destroy_idle_object(self):
        destroyed = []
        pool = _make_pool(destroyer=destroyed.append)
        po = pool.acquire()
        pool.release(po)
        pool.destroy(po)
        assert destroyed == [po.obj]
        assert pool.idle_count() == 0

    def test_destroy_makes_room_for_new(self):
        pool = _make_pool(max_size=1)
        po = pool.acquire()
        pool.destroy(po)
        # under cap again
        po2 = pool.acquire()
        assert po2 is not po

    def test_destroy_notifies_waiters(self):
        pool = _make_pool(max_size=1)
        held = pool.acquire()

        def destroyer():
            time.sleep(0.05)
            pool.destroy(held)

        t = threading.Thread(target=destroyer)
        t.start()
        po = pool.acquire(timeout=2.0)
        t.join()
        assert po is not held

    def test_destroy_without_destroyer_callback(self):
        pool = _make_pool()
        po = pool.acquire()
        # no destroyer set; should not raise
        pool.destroy(po)
        assert pool.size() == 0

    def test_destroyer_exception_suppressed(self):
        def bad_destroyer(_obj):
            raise RuntimeError("oops")

        pool = _make_pool(destroyer=bad_destroyer)
        po = pool.acquire()
        # must not raise
        pool.destroy(po)
        assert pool.size() == 0


# ---------------------------------------------------------------------------
# 10. count consistency
# ---------------------------------------------------------------------------


class TestCounts:
    def test_size_equals_idle_plus_in_use(self):
        pool = _make_pool(max_size=5)
        a = pool.acquire()
        b = pool.acquire()
        c = pool.acquire()
        pool.release(a)
        pool.release(b)
        assert pool.size() == pool.idle_count() + pool.in_use_count()
        assert pool.size() == 3

    def test_size_after_destroy(self):
        pool = _make_pool()
        a = pool.acquire()
        b = pool.acquire()
        pool.destroy(a)
        assert pool.size() == 1
        pool.release(b)
        assert pool.size() == 1

    def test_in_use_count_decreases_on_release(self):
        pool = _make_pool()
        a = pool.acquire()
        b = pool.acquire()
        assert pool.in_use_count() == 2
        pool.release(a)
        assert pool.in_use_count() == 1

    def test_idle_count_zero_when_all_in_use(self):
        pool = _make_pool(max_size=3)
        for _ in range(3):
            pool.acquire()
        assert pool.idle_count() == 0
        assert pool.in_use_count() == 3


# ---------------------------------------------------------------------------
# 11. clear()
# ---------------------------------------------------------------------------


class TestClear:
    def test_destroys_all_idle(self):
        destroyed = []
        pool = _make_pool(destroyer=destroyed.append)
        a = pool.acquire()
        b = pool.acquire()
        pool.release(a)
        pool.release(b)
        pool.clear()
        assert pool.idle_count() == 0
        assert pool.size() == 0
        assert sorted(destroyed) == sorted([a.obj, b.obj])

    def test_does_not_destroy_in_use(self):
        pool = _make_pool()
        a = pool.acquire()
        pool.clear()
        # still in-use
        assert pool.in_use_count() == 1

    def test_in_use_destroyed_on_release(self):
        destroyed = []
        pool = _make_pool(destroyer=destroyed.append)
        a = pool.acquire()
        pool.clear()
        pool.release(a)
        # released doomed object must be destroyed
        assert destroyed == [a.obj]
        assert pool.size() == 0

    def test_clear_empty_pool(self):
        pool = _make_pool()
        pool.clear()
        assert pool.size() == 0

    def test_clear_with_no_destroyer(self):
        pool = _make_pool()
        po = pool.acquire()
        pool.release(po)
        pool.clear()
        assert pool.idle_count() == 0

    def test_clear_notifies_waiters(self):
        pool = _make_pool(max_size=1)
        held = pool.acquire()

        def clearer():
            time.sleep(0.05)
            # clear marks held for destruction; then we release.
            pool.clear()
            pool.release(held)

        t = threading.Thread(target=clearer)
        t.start()
        # waiter should eventually be able to acquire a new resource
        po = pool.acquire(timeout=2.0)
        t.join()
        assert po is not held


# ---------------------------------------------------------------------------
# 12. prefill()
# ---------------------------------------------------------------------------


class TestPrefill:
    def test_creates_min_size_objects(self):
        pool = _make_pool(min_size=3, max_size=5)
        created = pool.prefill()
        assert created == 3
        assert pool.idle_count() == 3

    def test_returns_zero_when_already_filled(self):
        pool = _make_pool(min_size=2, max_size=5)
        assert pool.prefill() == 2
        # second call: no new objects needed
        assert pool.prefill() == 0

    def test_prefill_with_min_zero(self):
        pool = _make_pool(min_size=0)
        assert pool.prefill() == 0
        assert pool.idle_count() == 0

    def test_prefill_does_not_exceed_max(self):
        pool = _make_pool(min_size=0, max_size=3)
        # manually push pool to capacity
        for _ in range(3):
            pool.acquire()
        # change min to 5, but pool is already at max_size
        pool._config.min_size = 5
        assert pool.prefill() == 0

    def test_prefill_counts_existing_in_use(self):
        pool = _make_pool(min_size=3, max_size=5)
        pool.acquire()  # 1 in-use
        # need 2 more to reach min_size=3
        assert pool.prefill() == 2
        assert pool.size() == 3

    def test_prefill_idle_objects_use_count_zero(self):
        pool = _make_pool(min_size=2)
        pool.prefill()
        # we can acquire one of them and confirm use_count incremented from 0
        po = pool.acquire()
        assert po.use_count == 1


# ---------------------------------------------------------------------------
# 13. with_object context manager
# ---------------------------------------------------------------------------


class TestWithObject:
    def test_yields_pooled_object(self):
        pool = _make_pool()
        with pool.with_object() as po:
            assert isinstance(po, PooledObject)

    def test_auto_release_on_exit(self):
        pool = _make_pool()
        with pool.with_object():
            pass
        assert pool.idle_count() == 1
        assert pool.in_use_count() == 0

    def test_auto_release_on_exception(self):
        pool = _make_pool()
        with pytest.raises(RuntimeError):
            with pool.with_object():
                raise RuntimeError("kaboom")
        assert pool.in_use_count() == 0
        assert pool.idle_count() == 1

    def test_propagates_pool_exhausted(self):
        pool = _make_pool(max_size=1)
        pool.acquire()
        with pytest.raises(PoolExhausted):
            with pool.with_object(timeout=0):
                pass

    def test_object_reused_across_context_blocks(self):
        pool = _make_pool()
        with pool.with_object() as a:
            obj_a = a.obj
        with pool.with_object() as b:
            assert b.obj == obj_a

    def test_timeout_passed_through(self):
        pool = _make_pool(max_size=1)
        pool.acquire()
        start = time.monotonic()
        with pytest.raises(PoolExhausted):
            with pool.with_object(timeout=0.05):
                pass
        elapsed = time.monotonic() - start
        assert elapsed >= 0.04


# ---------------------------------------------------------------------------
# 14. validate_on_acquire: invalid objects destroyed and replaced
# ---------------------------------------------------------------------------


class TestValidateOnAcquire:
    def test_invalid_idle_destroyed_and_replaced(self):
        destroyed = []
        factory = _Counter()
        # treat 1 as invalid, others as valid
        validator = lambda o: o != 1
        pool = _make_pool(
            factory=factory,
            validate_on_acquire=True,
            validator=validator,
            destroyer=destroyed.append,
        )
        po1 = pool.acquire()
        assert po1.obj == 1
        pool.release(po1)
        po2 = pool.acquire()
        assert po2.obj == 2
        assert destroyed == [1]

    def test_validator_raising_treated_as_invalid(self):
        destroyed = []

        def validator(_o):
            raise RuntimeError("nope")

        pool = _make_pool(
            factory=_Counter(),
            validate_on_acquire=True,
            validator=validator,
            destroyer=destroyed.append,
        )
        po1 = pool.acquire()
        pool.release(po1)
        po2 = pool.acquire()
        assert po1.obj != po2.obj
        assert destroyed == [po1.obj]

    def test_validate_on_acquire_disabled(self):
        validator = lambda o: False  # always reject
        pool = _make_pool(
            validate_on_acquire=False,
            validator=validator,
        )
        po1 = pool.acquire()
        pool.release(po1)
        # validator should not run — same object returned
        po2 = pool.acquire()
        assert po1 is po2

    def test_no_validator_means_always_valid(self):
        pool = _make_pool(validate_on_acquire=True, validator=None)
        po1 = pool.acquire()
        pool.release(po1)
        po2 = pool.acquire()
        assert po1 is po2

    def test_all_invalid_creates_new_until_max(self):
        validator = lambda o: False
        destroyed = []
        pool = _make_pool(
            factory=_Counter(),
            max_size=2,
            validate_on_acquire=True,
            validator=validator,
            destroyer=destroyed.append,
        )
        a = pool.acquire()
        b = pool.acquire()
        # release both → idle, but invalid
        pool.release(a)
        pool.release(b)
        # next acquire: drains idle (destroys both), then creates one new
        c = pool.acquire()
        assert c.obj not in (a.obj, b.obj)
        assert sorted(destroyed) == sorted([a.obj, b.obj])


# ---------------------------------------------------------------------------
# 15. max_idle_time: expiry on acquire
# ---------------------------------------------------------------------------


class TestIdleExpiry:
    def test_expired_idle_destroyed_on_acquire(self):
        destroyed = []
        pool = _make_pool(
            factory=_Counter(),
            max_idle_time=0.05,
            destroyer=destroyed.append,
        )
        po1 = pool.acquire()
        pool.release(po1)
        time.sleep(0.08)
        po2 = pool.acquire()
        assert po2.obj != po1.obj
        assert destroyed == [po1.obj]

    def test_not_expired_reused(self):
        pool = _make_pool(
            factory=_Counter(),
            max_idle_time=1.0,
        )
        po1 = pool.acquire()
        pool.release(po1)
        po2 = pool.acquire()
        assert po2 is po1

    def test_max_idle_zero_disables_expiry(self):
        pool = _make_pool(factory=_Counter(), max_idle_time=0.0)
        po1 = pool.acquire()
        pool.release(po1)
        time.sleep(0.05)
        po2 = pool.acquire()
        assert po2 is po1

    def test_expired_objects_freed_for_new(self):
        pool = _make_pool(
            factory=_Counter(),
            max_size=1,
            max_idle_time=0.02,
        )
        po1 = pool.acquire()
        pool.release(po1)
        time.sleep(0.05)
        # should not raise — expired idle made room
        po2 = pool.acquire()
        assert po2.obj != po1.obj

    def test_multiple_expired_destroyed(self):
        destroyed = []
        pool = _make_pool(
            factory=_Counter(),
            max_size=3,
            max_idle_time=0.05,
            destroyer=destroyed.append,
        )
        objs = [pool.acquire() for _ in range(3)]
        for po in objs:
            pool.release(po)
        time.sleep(0.08)
        # one more acquire will sweep all expired
        pool.acquire()
        assert len(destroyed) == 3


# ---------------------------------------------------------------------------
# 16. Concurrent acquire/release
# ---------------------------------------------------------------------------


class TestConcurrency:
    def test_concurrent_acquires_unique_objects(self):
        pool = _make_pool(factory=_Counter(), max_size=20)
        with ThreadPoolExecutor(max_workers=10) as ex:
            futures = [ex.submit(pool.acquire) for _ in range(10)]
            pooled = [f.result() for f in as_completed(futures)]
        objs = [p.obj for p in pooled]
        assert len(set(objs)) == len(objs)
        assert pool.in_use_count() == 10

    def test_concurrent_acquire_release_cycle(self):
        pool = _make_pool(factory=_Counter(), max_size=5)

        def worker():
            for _ in range(20):
                with pool.with_object(timeout=2.0):
                    time.sleep(0.001)

        with ThreadPoolExecutor(max_workers=10) as ex:
            futures = [ex.submit(worker) for _ in range(10)]
            for f in as_completed(futures):
                f.result()  # raises if anything failed

        assert pool.in_use_count() == 0
        assert pool.size() <= 5

    def test_blocked_acquire_unblocks_on_release(self):
        pool = _make_pool(factory=_Counter(), max_size=2)
        a = pool.acquire()
        b = pool.acquire()

        results = []

        def waiter():
            results.append(pool.acquire(timeout=2.0))

        t = threading.Thread(target=waiter)
        t.start()
        time.sleep(0.05)
        pool.release(a)
        t.join(timeout=2.0)
        assert not t.is_alive()
        assert len(results) == 1
        assert results[0] is a or results[0].obj == a.obj
        pool.release(b)
        pool.release(results[0])

    def test_concurrent_clear_safe(self):
        pool = _make_pool(factory=_Counter(), max_size=5)

        def cycler():
            for _ in range(50):
                try:
                    po = pool.acquire(timeout=2.0)
                except PoolExhausted:
                    continue
                pool.release(po)

        threads = [threading.Thread(target=cycler) for _ in range(5)]
        for t in threads:
            t.start()
        # interleave with clears
        for _ in range(5):
            time.sleep(0.005)
            pool.clear()
        for t in threads:
            t.join()
        # final invariants
        assert pool.in_use_count() == 0
        assert pool.size() == pool.idle_count() + pool.in_use_count()

    def test_max_size_enforced_under_load(self):
        max_size = 4
        pool = _make_pool(factory=_Counter(), max_size=max_size)
        peak = []
        peak_lock = threading.Lock()

        def worker():
            for _ in range(30):
                with pool.with_object(timeout=2.0):
                    with peak_lock:
                        peak.append(pool.in_use_count())
                    time.sleep(0.0005)

        with ThreadPoolExecutor(max_workers=8) as ex:
            futs = [ex.submit(worker) for _ in range(8)]
            for f in as_completed(futs):
                f.result()
        assert max(peak) <= max_size


# ---------------------------------------------------------------------------
# 17. Misc invariants
# ---------------------------------------------------------------------------


class TestMisc:
    def test_release_unknown_object_is_noop(self):
        pool = _make_pool()
        # a PooledObject never returned by this pool's acquire
        rogue = PooledObject(obj="rogue")
        pool.release(rogue)
        assert pool.size() == 0

    def test_destroy_unknown_object_safe(self):
        pool = _make_pool()
        rogue = PooledObject(obj="rogue")
        # destroyer set: should attempt to call it, even for unknown
        destroyed = []
        pool._destroyer = destroyed.append
        pool.destroy(rogue)
        # destroyer invoked
        assert destroyed == ["rogue"]
        # pool size still zero
        assert pool.size() == 0

    def test_use_count_grows_on_each_acquire(self):
        pool = _make_pool()
        po = pool.acquire()
        pool.release(po)
        for expected in (2, 3, 4):
            pool.acquire()
            assert po.use_count == expected
            pool.release(po)

    def test_validator_not_required(self):
        pool = _make_pool(validator=None)
        po = pool.acquire()
        pool.release(po)
        assert pool.acquire() is po

    def test_factory_exception_propagates(self):
        def bad_factory():
            raise RuntimeError("factory failure")

        pool = ObjectPool(factory=bad_factory)
        with pytest.raises(RuntimeError):
            pool.acquire()
        assert pool.size() == 0

    def test_prefill_then_acquire_uses_prefilled(self):
        pool = _make_pool(min_size=2, max_size=5)
        pool.prefill()
        before = pool.idle_count()
        pool.acquire()
        assert pool.idle_count() == before - 1

    def test_release_after_clear_idle_object(self):
        pool = _make_pool()
        po = pool.acquire()
        pool.release(po)
        pool.clear()  # destroys idle
        # nothing crashes if we attempt to release the already-destroyed PO
        pool.release(po)
        assert pool.size() == 0

    def test_idle_lifo_order(self):
        """Implementation reuses most recently released object (LIFO)."""
        pool = _make_pool(factory=_Counter())
        a = pool.acquire()
        b = pool.acquire()
        pool.release(a)
        pool.release(b)
        assert pool.acquire() is b

    def test_with_object_release_only_once(self):
        pool = _make_pool()
        with pool.with_object() as po:
            assert pool.in_use_count() == 1
        assert pool.in_use_count() == 0
        assert pool.idle_count() == 1
        # try to release again manually — no double-add
        pool.release(po)
        assert pool.idle_count() == 1

    def test_destroy_during_validation_failure_chain(self):
        destroyed = []
        bad = {"x"}

        def validator(o):
            return o not in bad

        factory = _Counter()
        pool = _make_pool(
            factory=factory,
            validate_on_acquire=True,
            validator=validator,
            destroyer=destroyed.append,
        )
        po = pool.acquire()
        pool.release(po)
        # Mark this object's value as bad and re-acquire — should destroy + replace
        bad.add(po.obj)
        po2 = pool.acquire()
        assert po2.obj != po.obj
        assert po.obj in destroyed

    def test_acquire_create_under_concurrency_capped(self):
        pool = _make_pool(factory=_Counter(), max_size=3)
        results = []
        lock = threading.Lock()

        def worker():
            try:
                po = pool.acquire(timeout=2.0)
                with lock:
                    results.append(po)
            except PoolExhausted:
                pass

        threads = [threading.Thread(target=worker) for _ in range(3)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert len(results) == 3
        assert pool.size() == 3

    def test_size_after_clear_with_in_use(self):
        pool = _make_pool()
        a = pool.acquire()
        b = pool.acquire()
        pool.release(b)
        pool.clear()
        # idle b destroyed, in-use a remains
        assert pool.size() == 1
        assert pool.in_use_count() == 1
        pool.release(a)
        # released doomed a destroyed
        assert pool.size() == 0
