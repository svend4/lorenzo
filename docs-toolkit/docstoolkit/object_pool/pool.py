"""Object pool: reusable resource pool with thread-safe acquire/release.

Provides bounded, validated, idle-expiring pooling of arbitrary resources
(database connections, HTTP sessions, expensive parsers, etc.). Pure stdlib —
synchronisation via ``threading.Lock`` + ``threading.Condition``.
"""
from __future__ import annotations

import threading
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any, Callable, Iterator, List, Optional


class PoolExhausted(Exception):
    """Raised when no objects are available within the acquire timeout."""


@dataclass
class PoolConfig:
    """Configuration for an :class:`ObjectPool`."""

    min_size: int = 0
    max_size: int = 10
    max_idle_time: float = 0.0
    validate_on_acquire: bool = True
    validate_on_release: bool = False


@dataclass
class PooledObject:
    """A pooled resource together with bookkeeping metadata."""

    obj: Any
    created_at: float = field(default_factory=time.monotonic)
    last_used_at: float = field(default_factory=time.monotonic)
    use_count: int = 0


class ObjectPool:
    """Thread-safe object pool with optional validation and idle expiry.

    Resources are produced lazily via ``factory()``; up to ``config.max_size``
    objects may exist concurrently. ``acquire()`` returns an idle resource if
    one is available, creates a new one if under the max, or blocks waiting
    for a release (raising :class:`PoolExhausted` on timeout).
    """

    def __init__(
        self,
        factory: Callable[[], Any],
        config: Optional[PoolConfig] = None,
        validator: Optional[Callable[[Any], bool]] = None,
        destroyer: Optional[Callable[[Any], None]] = None,
    ) -> None:
        if factory is None:
            raise ValueError("factory is required")
        self._factory = factory
        self._config: PoolConfig = config if config is not None else PoolConfig()
        self._validator = validator
        self._destroyer = destroyer

        if self._config.min_size < 0:
            raise ValueError("min_size must be >= 0")
        if self._config.max_size < 1:
            raise ValueError("max_size must be >= 1")
        if self._config.min_size > self._config.max_size:
            raise ValueError("min_size must be <= max_size")

        self._lock = threading.Lock()
        self._cond = threading.Condition(self._lock)
        self._idle: List[PooledObject] = []
        self._in_use: List[PooledObject] = []
        # Objects whose destruction should occur on release (after clear()).
        self._doomed: set = set()
        self._closed = False

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    def size(self) -> int:
        """Total objects currently held by the pool (idle + in-use)."""
        with self._lock:
            return len(self._idle) + len(self._in_use)

    def idle_count(self) -> int:
        """Number of idle, ready-to-acquire objects."""
        with self._lock:
            return len(self._idle)

    def in_use_count(self) -> int:
        """Number of currently checked-out objects."""
        with self._lock:
            return len(self._in_use)

    # ------------------------------------------------------------------
    # Acquire / release / destroy
    # ------------------------------------------------------------------

    def acquire(self, timeout: float = 0.0) -> PooledObject:
        """Acquire a pooled object.

        - If an idle object is available (and passes validation), return it.
        - Otherwise, if total size < max_size, create a new one.
        - Otherwise, wait up to *timeout* seconds for a release.
        - If timeout elapses with no available object, raise
          :class:`PoolExhausted`. ``timeout=0`` means a single non-blocking
          attempt.
        """
        deadline = time.monotonic() + timeout if timeout > 0 else None
        with self._cond:
            while True:
                # Expire idle objects past max_idle_time.
                self._expire_idle_locked()

                # 1) Reuse an idle object.
                while self._idle:
                    pooled = self._idle.pop()
                    if self._config.validate_on_acquire and self._validator is not None:
                        try:
                            ok = bool(self._validator(pooled.obj))
                        except Exception:
                            ok = False
                        if not ok:
                            self._destroy_locked(pooled)
                            continue
                    self._in_use.append(pooled)
                    pooled.last_used_at = time.monotonic()
                    pooled.use_count += 1
                    return pooled

                # 2) Create a new object if there is headroom.
                if (
                    len(self._idle) + len(self._in_use)
                ) < self._config.max_size:
                    obj = self._factory()
                    pooled = PooledObject(obj=obj)
                    pooled.use_count = 1
                    self._in_use.append(pooled)
                    return pooled

                # 3) Wait for a release (or fail fast if timeout==0).
                if timeout <= 0:
                    raise PoolExhausted(
                        "ObjectPool exhausted: no idle objects and max_size reached"
                    )
                remaining = deadline - time.monotonic() if deadline else 0.0
                if remaining <= 0:
                    raise PoolExhausted(
                        "ObjectPool exhausted: timed out waiting for an object"
                    )
                self._cond.wait(timeout=remaining)

    def release(self, pooled: PooledObject) -> None:
        """Return a previously acquired object to the idle queue.

        If ``validate_on_release`` is enabled and the validator rejects the
        object, the resource is destroyed instead of being returned.
        If the object was marked for destruction via :meth:`clear`, it is
        destroyed.
        """
        with self._cond:
            if pooled not in self._in_use:
                # Already released/destroyed — ignore double-release silently.
                return
            self._in_use.remove(pooled)

            # If clear() marked it for destruction, destroy now.
            if id(pooled) in self._doomed:
                self._doomed.discard(id(pooled))
                self._destroy_locked(pooled)
                self._cond.notify_all()
                return

            if self._config.validate_on_release and self._validator is not None:
                try:
                    ok = bool(self._validator(pooled.obj))
                except Exception:
                    ok = False
                if not ok:
                    self._destroy_locked(pooled)
                    self._cond.notify_all()
                    return

            pooled.last_used_at = time.monotonic()
            self._idle.append(pooled)
            self._cond.notify()

    def destroy(self, pooled: PooledObject) -> None:
        """Explicitly destroy an object and remove it from the pool."""
        with self._cond:
            if pooled in self._in_use:
                self._in_use.remove(pooled)
            elif pooled in self._idle:
                self._idle.remove(pooled)
            self._doomed.discard(id(pooled))
            self._destroy_locked(pooled)
            self._cond.notify_all()

    # ------------------------------------------------------------------
    # Lifecycle helpers
    # ------------------------------------------------------------------

    def clear(self) -> None:
        """Destroy all idle objects; mark in-use objects for destruction on release."""
        with self._cond:
            # Destroy idle objects right now.
            while self._idle:
                pooled = self._idle.pop()
                self._destroy_locked(pooled)
            # In-use objects: mark them for destruction on release.
            for pooled in self._in_use:
                self._doomed.add(id(pooled))
            self._cond.notify_all()

    def prefill(self) -> int:
        """Create up to ``min_size`` resources eagerly. Returns count created."""
        created = 0
        with self._cond:
            need = self._config.min_size - (len(self._idle) + len(self._in_use))
            if need <= 0:
                return 0
            for _ in range(need):
                if (
                    len(self._idle) + len(self._in_use)
                ) >= self._config.max_size:
                    break
                obj = self._factory()
                pooled = PooledObject(obj=obj)
                self._idle.append(pooled)
                created += 1
            if created:
                self._cond.notify_all()
        return created

    @contextmanager
    def with_object(self, timeout: float = 0.0) -> Iterator[PooledObject]:
        """Context manager that auto-releases on exit (including exceptions)."""
        pooled = self.acquire(timeout=timeout)
        try:
            yield pooled
        finally:
            self.release(pooled)

    # ------------------------------------------------------------------
    # Internal helpers (lock held)
    # ------------------------------------------------------------------

    def _destroy_locked(self, pooled: PooledObject) -> None:
        """Invoke the destroyer for *pooled* outside of the visible pool state."""
        if self._destroyer is None:
            return
        try:
            self._destroyer(pooled.obj)
        except Exception:
            # Destroyer failures must not break pool invariants.
            pass

    def _expire_idle_locked(self) -> None:
        """Drop idle objects that have exceeded ``max_idle_time``."""
        max_idle = self._config.max_idle_time
        if max_idle <= 0:
            return
        now = time.monotonic()
        kept: List[PooledObject] = []
        for pooled in self._idle:
            if now - pooled.last_used_at >= max_idle:
                self._destroy_locked(pooled)
            else:
                kept.append(pooled)
        self._idle = kept
