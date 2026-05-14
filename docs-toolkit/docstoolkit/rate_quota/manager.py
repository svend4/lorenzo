"""High-level quota manager combining definitions and a store."""
from __future__ import annotations

import math
import time
from typing import Optional, Tuple

from docstoolkit.rate_quota.quota import (
    QuotaDefinition,
    QuotaExceeded,
    QuotaPeriod,
    QuotaUsage,
)
from docstoolkit.rate_quota.store import QuotaStore


class QuotaManager:
    """Register quotas and enforce them against a persistent store."""

    def __init__(self, store: Optional[QuotaStore] = None):
        self._store = store if store is not None else QuotaStore()
        self._definitions: dict[str, QuotaDefinition] = {}

    # ------------------------------------------------------------------ #
    @property
    def store(self) -> QuotaStore:
        return self._store

    # ------------------------------------------------------------------ #
    def define(self, quota: QuotaDefinition) -> None:
        """Register a quota definition (overrides existing one for that key)."""
        self._definitions[quota.key] = quota

    # ------------------------------------------------------------------ #
    def get_definition(self, key: str) -> Optional[QuotaDefinition]:
        return self._definitions.get(key)

    # ------------------------------------------------------------------ #
    def list_definitions(self) -> list[QuotaDefinition]:
        return list(self._definitions.values())

    # ------------------------------------------------------------------ #
    def _resolve(self, key: str) -> QuotaDefinition:
        if key not in self._definitions:
            raise KeyError(f"Quota '{key}' is not defined")
        return self._definitions[key]

    # ------------------------------------------------------------------ #
    @staticmethod
    def _reset_at(now: float, period_seconds: float) -> float:
        window_start = math.floor(now / period_seconds) * period_seconds
        return window_start + period_seconds

    # ------------------------------------------------------------------ #
    def check(
        self,
        key: str,
        owner: str,
        now: Optional[float] = None,
    ) -> QuotaUsage:
        """Return current usage without modifying counters.

        Raises KeyError if the quota key is not defined.
        """
        definition = self._resolve(key)
        if now is None:
            now = time.time()
        period_seconds = float(definition.period.value)
        count = self._store.get_count(key, owner, period_seconds, now=now)
        return QuotaUsage(
            key=key,
            count=count,
            limit=definition.limit,
            period=definition.period,
            reset_at=self._reset_at(now, period_seconds),
        )

    # ------------------------------------------------------------------ #
    def consume(
        self,
        key: str,
        owner: str,
        now: Optional[float] = None,
        amount: int = 1,
    ) -> QuotaUsage:
        """Consume `amount` from the quota; raise QuotaExceeded if it would overflow."""
        definition = self._resolve(key)
        if now is None:
            now = time.time()
        period_seconds = float(definition.period.value)
        current = self._store.get_count(key, owner, period_seconds, now=now)
        if current + amount > definition.limit:
            usage = QuotaUsage(
                key=key,
                count=current,
                limit=definition.limit,
                period=definition.period,
                reset_at=self._reset_at(now, period_seconds),
            )
            raise QuotaExceeded(key, usage)
        new_count = self._store.record(
            key, owner, period_seconds, now=now, amount=amount
        )
        return QuotaUsage(
            key=key,
            count=new_count,
            limit=definition.limit,
            period=definition.period,
            reset_at=self._reset_at(now, period_seconds),
        )

    # ------------------------------------------------------------------ #
    def try_consume(
        self,
        key: str,
        owner: str,
        now: Optional[float] = None,
        amount: int = 1,
    ) -> Tuple[bool, QuotaUsage]:
        """Non-raising version of consume.

        Returns (True, usage_after_consume) on success,
        (False, usage_before_consume) when limit would be exceeded.
        """
        try:
            usage = self.consume(key, owner, now=now, amount=amount)
            return True, usage
        except QuotaExceeded as exc:
            return False, exc.usage

    # ------------------------------------------------------------------ #
    def reset(
        self,
        key: Optional[str] = None,
        owner: Optional[str] = None,
    ) -> int:
        """Proxy to store.reset(quota_key=key, owner=owner)."""
        return self._store.reset(quota_key=key, owner=owner)
