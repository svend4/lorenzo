"""Webhook dispatcher with delivery tracking, retries, and HMAC signing."""

from __future__ import annotations

import hashlib
import hmac
import json
import threading
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Optional


class DeliveryStatus(Enum):
    PENDING = "pending"
    IN_FLIGHT = "in_flight"
    DELIVERED = "delivered"
    FAILED = "failed"
    ABANDONED = "abandoned"


@dataclass
class Subscription:
    sub_id: str
    url: str
    secret: str
    event_types: set = field(default_factory=set)
    enabled: bool = True
    created_at: float = 0.0


@dataclass
class Delivery:
    delivery_id: int
    sub_id: str
    event_type: str
    payload: dict
    status: DeliveryStatus
    attempts: int = 0
    created_at: float = 0.0
    last_attempt_at: float = 0.0
    next_retry_at: float = 0.0
    signature: str = ""
    last_error: Optional[str] = None


@dataclass
class DispatcherStats:
    total_subscriptions: int = 0
    total_deliveries: int = 0
    delivered: int = 0
    failed: int = 0
    pending: int = 0

    @property
    def success_rate(self) -> float:
        if self.total_deliveries == 0:
            return 0.0
        return self.delivered / self.total_deliveries


def _default_transport(url: str, payload: dict, signature: str, headers: dict):
    """No-op default transport; always succeeds."""
    return True, None


def _serialize_payload(payload: dict) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


class WebhookDispatcher:
    def __init__(
        self,
        transport: Optional[Callable] = None,
        max_retries: int = 3,
    ):
        self._transport = transport if transport is not None else _default_transport
        self._max_retries = max_retries
        self._lock = threading.Lock()
        self._subscriptions: dict[str, Subscription] = {}
        self._deliveries: dict[int, Delivery] = {}
        self._next_sub_id = 1
        self._next_delivery_id = 1

    # ------------------------------------------------------------------
    # Subscriptions
    # ------------------------------------------------------------------
    def subscribe(
        self,
        url: str,
        secret: str,
        event_types: set,
        now: float = 0.0,
    ) -> Subscription:
        with self._lock:
            sub_id = f"sub_{self._next_sub_id}"
            self._next_sub_id += 1
            sub = Subscription(
                sub_id=sub_id,
                url=url,
                secret=secret,
                event_types=set(event_types),
                enabled=True,
                created_at=now,
            )
            self._subscriptions[sub_id] = sub
            return sub

    def unsubscribe(self, sub_id: str) -> bool:
        with self._lock:
            if sub_id in self._subscriptions:
                del self._subscriptions[sub_id]
                return True
            return False

    def enable_subscription(self, sub_id: str) -> bool:
        with self._lock:
            sub = self._subscriptions.get(sub_id)
            if sub is None:
                return False
            sub.enabled = True
            return True

    def disable_subscription(self, sub_id: str) -> bool:
        with self._lock:
            sub = self._subscriptions.get(sub_id)
            if sub is None:
                return False
            sub.enabled = False
            return True

    @property
    def subscription_count(self) -> int:
        with self._lock:
            return len(self._subscriptions)

    # ------------------------------------------------------------------
    # Event matching
    # ------------------------------------------------------------------
    def matches_event(self, sub: Subscription, event_type: str) -> bool:
        for pattern in sub.event_types:
            if pattern == "*":
                return True
            if pattern == event_type:
                return True
            if pattern.endswith(".*"):
                prefix = pattern[:-2]
                if event_type.startswith(prefix + "."):
                    return True
        return False

    # ------------------------------------------------------------------
    # Signing
    # ------------------------------------------------------------------
    def sign_payload(self, payload: dict, secret: str) -> str:
        msg = _serialize_payload(payload)
        key = secret.encode("utf-8")
        return hmac.new(key, msg, hashlib.sha256).hexdigest()

    def verify_signature(self, payload: dict, signature: str, secret: str) -> bool:
        expected = self.sign_payload(payload, secret)
        return hmac.compare_digest(expected, signature)

    # ------------------------------------------------------------------
    # Dispatch
    # ------------------------------------------------------------------
    def dispatch(
        self,
        event_type: str,
        payload: dict,
        now: float = 0.0,
    ) -> list:
        created: list = []
        with self._lock:
            for sub in self._subscriptions.values():
                if not sub.enabled:
                    continue
                if not self.matches_event(sub, event_type):
                    continue
                delivery_id = self._next_delivery_id
                self._next_delivery_id += 1
                signature = self.sign_payload(payload, sub.secret)
                delivery = Delivery(
                    delivery_id=delivery_id,
                    sub_id=sub.sub_id,
                    event_type=event_type,
                    payload=dict(payload),
                    status=DeliveryStatus.PENDING,
                    attempts=0,
                    created_at=now,
                    last_attempt_at=0.0,
                    next_retry_at=now,
                    signature=signature,
                    last_error=None,
                )
                self._deliveries[delivery_id] = delivery
                created.append(delivery)
        return created

    def deliver_pending(self, now: float = 0.0, batch_size: int = 10) -> int:
        processed = 0
        # Collect candidates under lock
        with self._lock:
            ready = [
                d
                for d in self._deliveries.values()
                if d.status in (DeliveryStatus.PENDING, DeliveryStatus.FAILED)
                and d.next_retry_at <= now
            ]
            ready.sort(key=lambda d: (d.next_retry_at, d.delivery_id))
            ready = ready[:batch_size]
            # Mark as IN_FLIGHT to avoid double-processing
            for d in ready:
                d.status = DeliveryStatus.IN_FLIGHT
                d.last_attempt_at = now

        for delivery in ready:
            sub = self._subscriptions.get(delivery.sub_id)
            if sub is None:
                with self._lock:
                    delivery.status = DeliveryStatus.ABANDONED
                    delivery.last_error = "subscription_removed"
                processed += 1
                continue

            headers = {
                "X-Webhook-Event": delivery.event_type,
                "X-Webhook-Signature": delivery.signature,
                "X-Webhook-Delivery": str(delivery.delivery_id),
            }

            success = False
            error: Optional[str] = None
            try:
                result = self._transport(sub.url, delivery.payload, delivery.signature, headers)
                if isinstance(result, tuple) and len(result) == 2:
                    success, error = result
                else:
                    success = bool(result)
                    error = None
            except Exception as exc:  # pragma: no cover - transport errors
                success = False
                error = str(exc)

            with self._lock:
                delivery.attempts += 1
                if success:
                    delivery.status = DeliveryStatus.DELIVERED
                    delivery.last_error = None
                else:
                    delivery.last_error = error
                    if delivery.attempts > self._max_retries:
                        delivery.status = DeliveryStatus.ABANDONED
                    else:
                        delivery.status = DeliveryStatus.FAILED
                        delivery.next_retry_at = now + (2 ** delivery.attempts)
            processed += 1

        return processed

    # ------------------------------------------------------------------
    # Inspection
    # ------------------------------------------------------------------
    def get_delivery(self, delivery_id: int) -> Optional[Delivery]:
        with self._lock:
            return self._deliveries.get(delivery_id)

    def pending_deliveries(self, now: float = 0.0) -> list:
        with self._lock:
            return [
                d
                for d in self._deliveries.values()
                if d.status in (DeliveryStatus.PENDING, DeliveryStatus.FAILED)
                and d.next_retry_at <= now
            ]

    def deliveries_for_subscription(self, sub_id: str) -> list:
        with self._lock:
            return [d for d in self._deliveries.values() if d.sub_id == sub_id]

    def stats(self) -> DispatcherStats:
        with self._lock:
            delivered = sum(
                1 for d in self._deliveries.values() if d.status == DeliveryStatus.DELIVERED
            )
            failed = sum(
                1
                for d in self._deliveries.values()
                if d.status in (DeliveryStatus.FAILED, DeliveryStatus.ABANDONED)
            )
            pending = sum(
                1
                for d in self._deliveries.values()
                if d.status in (DeliveryStatus.PENDING, DeliveryStatus.IN_FLIGHT)
            )
            return DispatcherStats(
                total_subscriptions=len(self._subscriptions),
                total_deliveries=len(self._deliveries),
                delivered=delivered,
                failed=failed,
                pending=pending,
            )

    def clear(self) -> None:
        with self._lock:
            self._subscriptions.clear()
            self._deliveries.clear()
            self._next_sub_id = 1
            self._next_delivery_id = 1
