"""User subscription management to documents/tags/topics with notification preferences."""
from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class SubscriptionType(Enum):
    """Type of entity a user can subscribe to."""

    DOCUMENT = "document"
    TAG = "tag"
    TOPIC = "topic"
    AUTHOR = "author"
    KEYWORD = "keyword"


class NotificationChannel(Enum):
    """Channel through which a notification is delivered."""

    EMAIL = "email"
    IN_APP = "in_app"
    SMS = "sms"
    WEBHOOK = "webhook"
    DIGEST = "digest"


class Frequency(Enum):
    """How often a user wants to receive notifications."""

    IMMEDIATE = "immediate"
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    OFF = "off"


@dataclass
class Subscription:
    """A single user's subscription to a target."""

    sub_id: str
    user_id: str
    subscription_type: SubscriptionType
    target: str
    channels: set = field(default_factory=set)
    frequency: Frequency = Frequency.IMMEDIATE
    enabled: bool = True
    created_at: float = 0.0


@dataclass
class UserPreferences:
    """Per-user notification preferences."""

    user_id: str
    default_channels: set = field(default_factory=set)
    default_frequency: Frequency = Frequency.IMMEDIATE
    quiet_hours: Optional[tuple] = None
    do_not_disturb: bool = False


@dataclass
class Notification:
    """A prepared notification for delivery."""

    notification_id: int
    subscription: Subscription
    subject_doc_id: str
    event: str
    timestamp: float
    channels: list


class DocSubscription:
    """Manage user subscriptions, preferences, and prepare notifications."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._subs: dict[str, Subscription] = {}
        self._prefs: dict[str, UserPreferences] = {}
        self._next_notification_id: int = 1

    def subscribe(
        self,
        user_id: str,
        subscription_type: SubscriptionType,
        target: str,
        channels: Optional[set] = None,
        frequency: Optional[Frequency] = None,
        now: float = 0.0,
    ) -> Subscription:
        """Create a new subscription for a user."""
        with self._lock:
            prefs = self._prefs.get(user_id)
            if channels is None:
                if prefs is not None and prefs.default_channels:
                    channels = set(prefs.default_channels)
                else:
                    channels = {NotificationChannel.IN_APP}
            else:
                channels = set(channels)
            if frequency is None:
                if prefs is not None:
                    frequency = prefs.default_frequency
                else:
                    frequency = Frequency.IMMEDIATE
            sub_id = uuid.uuid4().hex
            sub = Subscription(
                sub_id=sub_id,
                user_id=user_id,
                subscription_type=subscription_type,
                target=target,
                channels=channels,
                frequency=frequency,
                enabled=True,
                created_at=now,
            )
            self._subs[sub_id] = sub
            return sub

    def unsubscribe(self, sub_id: str) -> bool:
        """Remove a subscription by id. Returns True if removed."""
        with self._lock:
            return self._subs.pop(sub_id, None) is not None

    def unsubscribe_all(self, user_id: str) -> int:
        """Remove all subscriptions for a user. Returns count removed."""
        with self._lock:
            to_remove = [sid for sid, s in self._subs.items() if s.user_id == user_id]
            for sid in to_remove:
                del self._subs[sid]
            return len(to_remove)

    def set_user_preferences(
        self,
        user_id: str,
        default_channels: Optional[set] = None,
        default_frequency: Optional[Frequency] = None,
        quiet_hours: Optional[tuple] = None,
        do_not_disturb: Optional[bool] = None,
    ) -> UserPreferences:
        """Update or create user preferences. Only provided fields are changed."""
        with self._lock:
            prefs = self._prefs.get(user_id)
            if prefs is None:
                prefs = UserPreferences(user_id=user_id)
                self._prefs[user_id] = prefs
            if default_channels is not None:
                prefs.default_channels = set(default_channels)
            if default_frequency is not None:
                prefs.default_frequency = default_frequency
            if quiet_hours is not None:
                prefs.quiet_hours = quiet_hours
            if do_not_disturb is not None:
                prefs.do_not_disturb = do_not_disturb
            return prefs

    def get_preferences(self, user_id: str) -> Optional[UserPreferences]:
        """Return preferences for a user (or None)."""
        with self._lock:
            return self._prefs.get(user_id)

    def subscriptions_for_user(self, user_id: str) -> list:
        """Return all subscriptions for a user."""
        with self._lock:
            return [s for s in self._subs.values() if s.user_id == user_id]

    def subscribers_for_doc(self, doc_id: str) -> list:
        """Return all DOCUMENT-type subscriptions targeting a doc."""
        with self._lock:
            return [
                s
                for s in self._subs.values()
                if s.subscription_type == SubscriptionType.DOCUMENT
                and s.target == doc_id
            ]

    def subscribers_for_tag(self, tag: str) -> list:
        """Return all TAG-type subscriptions matching a tag."""
        with self._lock:
            return [
                s
                for s in self._subs.values()
                if s.subscription_type == SubscriptionType.TAG and s.target == tag
            ]

    def find_matching(
        self,
        event_doc_id: str,
        tags: Optional[list] = None,
        author: Optional[str] = None,
        topic: Optional[str] = None,
    ) -> list:
        """Find subscriptions whose target matches the event context."""
        tags_set = set(tags or [])
        with self._lock:
            matched: list = []
            seen: set = set()
            for s in self._subs.values():
                hit = False
                stype = s.subscription_type
                if stype == SubscriptionType.DOCUMENT and s.target == event_doc_id:
                    hit = True
                elif stype == SubscriptionType.TAG and s.target in tags_set:
                    hit = True
                elif stype == SubscriptionType.AUTHOR and author is not None and s.target == author:
                    hit = True
                elif stype == SubscriptionType.TOPIC and topic is not None and s.target == topic:
                    hit = True
                elif stype == SubscriptionType.KEYWORD and s.target == event_doc_id:
                    # Keyword matches when its target equals the doc id (simple heuristic);
                    # also match against tags for broader keyword coverage.
                    hit = True
                elif stype == SubscriptionType.KEYWORD and s.target in tags_set:
                    hit = True
                if hit and s.sub_id not in seen:
                    seen.add(s.sub_id)
                    matched.append(s)
            return matched

    def should_notify(self, sub: Subscription, now: float = 0.0) -> bool:
        """Check whether a subscription should fire a notification right now."""
        if not sub.enabled:
            return False
        if sub.frequency == Frequency.OFF:
            return False
        prefs = self._prefs.get(sub.user_id)
        if prefs is not None:
            if prefs.do_not_disturb:
                return False
            if prefs.quiet_hours is not None:
                start_h, end_h = prefs.quiet_hours
                try:
                    hour = datetime.fromtimestamp(now, tz=timezone.utc).hour
                except (OverflowError, OSError, ValueError):
                    hour = 0
                if start_h == end_h:
                    # Equal bounds: treat as no active quiet window
                    pass
                elif start_h < end_h:
                    # Active range [start_h, end_h): notify only when hour is in [start_h, end_h)
                    if not (start_h <= hour < end_h):
                        return False
                else:
                    # Wrap-around (e.g. 22, 7): active hours are [end_h, start_h)
                    # i.e. notify only when hour in [end_h, start_h)
                    if not (end_h <= hour < start_h):
                        return False
        return True

    def prepare_notifications(
        self,
        event_doc_id: str,
        event: str,
        tags: Optional[list] = None,
        author: Optional[str] = None,
        topic: Optional[str] = None,
        now: float = 0.0,
    ) -> list:
        """Find matching subs that should notify and build Notification objects."""
        matches = self.find_matching(
            event_doc_id=event_doc_id, tags=tags, author=author, topic=topic
        )
        notifications: list = []
        with self._lock:
            for sub in matches:
                if not self._should_notify_locked(sub, now):
                    continue
                nid = self._next_notification_id
                self._next_notification_id += 1
                notifications.append(
                    Notification(
                        notification_id=nid,
                        subscription=sub,
                        subject_doc_id=event_doc_id,
                        event=event,
                        timestamp=now,
                        channels=list(sub.channels),
                    )
                )
        return notifications

    def _should_notify_locked(self, sub: Subscription, now: float) -> bool:
        """Lock-free internal check for use inside prepare_notifications."""
        if not sub.enabled:
            return False
        if sub.frequency == Frequency.OFF:
            return False
        prefs = self._prefs.get(sub.user_id)
        if prefs is not None:
            if prefs.do_not_disturb:
                return False
            if prefs.quiet_hours is not None:
                start_h, end_h = prefs.quiet_hours
                try:
                    hour = datetime.fromtimestamp(now, tz=timezone.utc).hour
                except (OverflowError, OSError, ValueError):
                    hour = 0
                if start_h == end_h:
                    pass
                elif start_h < end_h:
                    if not (start_h <= hour < end_h):
                        return False
                else:
                    if not (end_h <= hour < start_h):
                        return False
        return True

    def enable_subscription(self, sub_id: str) -> bool:
        """Enable a subscription. Returns True if found."""
        with self._lock:
            sub = self._subs.get(sub_id)
            if sub is None:
                return False
            sub.enabled = True
            return True

    def disable_subscription(self, sub_id: str) -> bool:
        """Disable a subscription. Returns True if found."""
        with self._lock:
            sub = self._subs.get(sub_id)
            if sub is None:
                return False
            sub.enabled = False
            return True

    def update_frequency(self, sub_id: str, frequency: Frequency) -> bool:
        """Update frequency of a subscription. Returns True if found."""
        with self._lock:
            sub = self._subs.get(sub_id)
            if sub is None:
                return False
            sub.frequency = frequency
            return True

    @property
    def subscription_count(self) -> int:
        """Total number of subscriptions."""
        with self._lock:
            return len(self._subs)

    @property
    def user_count(self) -> int:
        """Number of distinct users with subscriptions or preferences."""
        with self._lock:
            users = {s.user_id for s in self._subs.values()}
            users.update(self._prefs.keys())
            return len(users)

    def clear(self) -> None:
        """Wipe all subscriptions and preferences."""
        with self._lock:
            self._subs.clear()
            self._prefs.clear()
            self._next_notification_id = 1
