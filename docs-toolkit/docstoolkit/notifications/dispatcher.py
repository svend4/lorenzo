from dataclasses import dataclass, field
from docstoolkit.notifications.message import Notification, NotificationLevel, Channel
from docstoolkit.notifications.handlers import NotificationHandler

_LEVEL_ORDER = {
    NotificationLevel.DEBUG: 0,
    NotificationLevel.INFO: 1,
    NotificationLevel.WARNING: 2,
    NotificationLevel.ERROR: 3,
    NotificationLevel.CRITICAL: 4,
}


@dataclass
class RoutingRule:
    """Route notifications matching criteria to specific channels."""
    min_level: NotificationLevel = NotificationLevel.INFO
    channels: list = field(default_factory=list)   # list[Channel]
    sources: list = field(default_factory=list)    # if non-empty: only match these sources
    tags: list = field(default_factory=list)       # if non-empty: notification must have ALL tags

    def matches(self, notification: Notification) -> bool:
        """Return True if notification matches this rule."""
        if _LEVEL_ORDER[notification.level] < _LEVEL_ORDER[self.min_level]:
            return False
        if self.sources and notification.source not in self.sources:
            return False
        if self.tags and not all(t in notification.tags for t in self.tags):
            return False
        return True


class NotificationDispatcher:
    """Routes notifications to registered handlers via rules."""

    def __init__(self):
        self._handlers: dict = {}   # {Channel: NotificationHandler}
        self._rules: list = []       # list[RoutingRule]
        self._sent_count: int = 0
        self._failed_count: int = 0

    def register_handler(self, handler: NotificationHandler) -> None:
        self._handlers[handler.channel] = handler

    def add_rule(self, rule: RoutingRule) -> None:
        self._rules.append(rule)

    def dispatch(self, notification: Notification) -> dict:
        """Route notification through matching rules.

        For each rule that matches notification:
          For each channel in rule.channels:
            If handler registered for channel: call handler.send()

        Return {channel.value: bool (success)} for all attempted sends.
        """
        results = {}
        for rule in self._rules:
            if rule.matches(notification):
                for channel in rule.channels:
                    handler = self._handlers.get(channel)
                    if handler:
                        success = handler.send(notification)
                        results[channel.value] = success
                        if success:
                            self._sent_count += 1
                        else:
                            self._failed_count += 1
        return results

    def stats(self) -> dict:
        return {"sent": self._sent_count, "failed": self._failed_count}
