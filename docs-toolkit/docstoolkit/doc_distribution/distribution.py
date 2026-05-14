"""Distribution channel manager with delivery tracking.

Provides multi-channel document distribution (email, RSS, webhook, in-app, slack,
digest) with per-delivery status tracking, retries, and stats.
"""
from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class ChannelType(Enum):
    """Supported distribution channel types."""

    EMAIL = "email"
    RSS = "rss"
    WEBHOOK = "webhook"
    IN_APP = "in_app"
    SLACK = "slack"
    DIGEST = "digest"


class DeliveryStatus(Enum):
    """Lifecycle status of a single delivery."""

    QUEUED = "queued"
    IN_FLIGHT = "in_flight"
    DELIVERED = "delivered"
    FAILED = "failed"


@dataclass
class Channel:
    """A distribution channel configuration."""

    channel_id: str
    channel_type: ChannelType
    name: str
    endpoint: str
    enabled: bool = True
    subscribers: set = field(default_factory=set)
    metadata: dict = field(default_factory=dict)


@dataclass
class Delivery:
    """A single delivery attempt to a recipient through a channel."""

    delivery_id: int
    channel_id: str
    doc_id: str
    recipient: str
    status: DeliveryStatus
    attempts: int = 0
    queued_at: float = 0.0
    delivered_at: Optional[float] = None
    last_error: Optional[str] = None


@dataclass
class DistributionStats:
    """Aggregate statistics across all channels and deliveries."""

    total_channels: int
    total_subscribers: int
    total_deliveries: int
    delivered: int
    failed: int
    queued: int

    @property
    def delivery_rate(self) -> float:
        if self.total_deliveries == 0:
            return 0.0
        return self.delivered / self.total_deliveries


class DocDistribution:
    """Thread-safe distribution manager for documents across multiple channels."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._channels: dict[str, Channel] = {}
        self._deliveries: dict[int, Delivery] = {}
        self._next_delivery_id: int = 1

    # ----- channel management -----

    def add_channel(
        self,
        channel_type: ChannelType,
        name: str,
        endpoint: str,
        metadata: Optional[dict] = None,
    ) -> Channel:
        with self._lock:
            channel_id = uuid.uuid4().hex
            channel = Channel(
                channel_id=channel_id,
                channel_type=channel_type,
                name=name,
                endpoint=endpoint,
                enabled=True,
                subscribers=set(),
                metadata=dict(metadata) if metadata else {},
            )
            self._channels[channel_id] = channel
            return channel

    def remove_channel(self, channel_id: str) -> bool:
        with self._lock:
            if channel_id not in self._channels:
                return False
            del self._channels[channel_id]
            return True

    def enable_channel(self, channel_id: str) -> bool:
        with self._lock:
            ch = self._channels.get(channel_id)
            if ch is None:
                return False
            ch.enabled = True
            return True

    def disable_channel(self, channel_id: str) -> bool:
        with self._lock:
            ch = self._channels.get(channel_id)
            if ch is None:
                return False
            ch.enabled = False
            return True

    # ----- subscriptions -----

    def subscribe(self, channel_id: str, recipient: str) -> bool:
        with self._lock:
            ch = self._channels.get(channel_id)
            if ch is None:
                return False
            if recipient in ch.subscribers:
                return False
            ch.subscribers.add(recipient)
            return True

    def unsubscribe(self, channel_id: str, recipient: str) -> bool:
        with self._lock:
            ch = self._channels.get(channel_id)
            if ch is None:
                return False
            if recipient not in ch.subscribers:
                return False
            ch.subscribers.remove(recipient)
            return True

    # ----- distribution -----

    def distribute(
        self,
        doc_id: str,
        channel_ids: Optional[list] = None,
        recipients_filter: Optional[set] = None,
        now: float = 0.0,
    ) -> list:
        """Queue deliveries for a document.

        - channel_ids: limit to these channels (else all enabled)
        - recipients_filter: only queue for subscribers in this set
        """
        created: list[Delivery] = []
        with self._lock:
            if channel_ids is None:
                target_channels = [c for c in self._channels.values() if c.enabled]
            else:
                target_channels = []
                for cid in channel_ids:
                    ch = self._channels.get(cid)
                    if ch is not None and ch.enabled:
                        target_channels.append(ch)

            for ch in target_channels:
                for recipient in sorted(ch.subscribers):
                    if recipients_filter is not None and recipient not in recipients_filter:
                        continue
                    delivery_id = self._next_delivery_id
                    self._next_delivery_id += 1
                    delivery = Delivery(
                        delivery_id=delivery_id,
                        channel_id=ch.channel_id,
                        doc_id=doc_id,
                        recipient=recipient,
                        status=DeliveryStatus.QUEUED,
                        attempts=0,
                        queued_at=now,
                        delivered_at=None,
                        last_error=None,
                    )
                    self._deliveries[delivery_id] = delivery
                    created.append(delivery)
        return created

    def mark_delivered(self, delivery_id: int, now: float = 0.0) -> bool:
        with self._lock:
            d = self._deliveries.get(delivery_id)
            if d is None:
                return False
            d.status = DeliveryStatus.DELIVERED
            d.attempts += 1
            d.delivered_at = now
            d.last_error = None
            return True

    def mark_failed(self, delivery_id: int, error: Optional[str] = None) -> bool:
        with self._lock:
            d = self._deliveries.get(delivery_id)
            if d is None:
                return False
            d.status = DeliveryStatus.FAILED
            d.attempts += 1
            d.last_error = error
            return True

    def retry_failed(self, delivery_id: int, now: float = 0.0) -> bool:
        with self._lock:
            d = self._deliveries.get(delivery_id)
            if d is None:
                return False
            if d.status != DeliveryStatus.FAILED:
                return False
            d.status = DeliveryStatus.QUEUED
            d.queued_at = now
            d.last_error = None
            return True

    # ----- queries -----

    def pending_deliveries(self) -> list:
        with self._lock:
            return [
                d
                for d in self._deliveries.values()
                if d.status in (DeliveryStatus.QUEUED, DeliveryStatus.IN_FLIGHT)
            ]

    def failed_deliveries(self) -> list:
        with self._lock:
            return [d for d in self._deliveries.values() if d.status == DeliveryStatus.FAILED]

    def deliveries_for_doc(self, doc_id: str) -> list:
        with self._lock:
            return [d for d in self._deliveries.values() if d.doc_id == doc_id]

    def deliveries_for_recipient(self, recipient: str) -> list:
        with self._lock:
            return [d for d in self._deliveries.values() if d.recipient == recipient]

    def channels_for_recipient(self, recipient: str) -> list:
        with self._lock:
            return [c for c in self._channels.values() if recipient in c.subscribers]

    def channels_by_type(self, channel_type: ChannelType) -> list:
        with self._lock:
            return [c for c in self._channels.values() if c.channel_type == channel_type]

    def subscriber_count(self, channel_id: str) -> int:
        with self._lock:
            ch = self._channels.get(channel_id)
            if ch is None:
                return 0
            return len(ch.subscribers)

    def stats(self) -> DistributionStats:
        with self._lock:
            total_channels = len(self._channels)
            unique_subs: set = set()
            for ch in self._channels.values():
                unique_subs.update(ch.subscribers)
            total_subscribers = len(unique_subs)
            total_deliveries = len(self._deliveries)
            delivered = 0
            failed = 0
            queued = 0
            for d in self._deliveries.values():
                if d.status == DeliveryStatus.DELIVERED:
                    delivered += 1
                elif d.status == DeliveryStatus.FAILED:
                    failed += 1
                elif d.status == DeliveryStatus.QUEUED:
                    queued += 1
            return DistributionStats(
                total_channels=total_channels,
                total_subscribers=total_subscribers,
                total_deliveries=total_deliveries,
                delivered=delivered,
                failed=failed,
                queued=queued,
            )

    # ----- properties -----

    @property
    def total_channels(self) -> int:
        with self._lock:
            return len(self._channels)

    @property
    def total_deliveries(self) -> int:
        with self._lock:
            return len(self._deliveries)

    def clear(self) -> None:
        with self._lock:
            self._channels.clear()
            self._deliveries.clear()
            self._next_delivery_id = 1
