"""E423 DocInboxRouter — route incoming document messages to inboxes.

A :class:`RoutingRule` consists of:
- a ``rule_id``
- a ``pattern`` (fnmatch-style, matched against ``doc_id``)
- an ``inbox`` (the target inbox name)
- a ``priority`` (higher = applied first)
- a ``stop_on_match`` flag (if True, stop trying further rules after a match)
- an ``enabled`` flag

Routing a ``doc_id`` (with optional ``payload``) iterates the enabled rules
in priority order, creating a :class:`RoutedMessage` for each match, and
short-circuiting if a matched rule has ``stop_on_match=True``.

Thread-safe: every mutation is protected by an internal :class:`threading.Lock`.
"""
from __future__ import annotations

import fnmatch
import threading
import time
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass
class RoutingRule:
    """A routing rule mapping a ``doc_id`` pattern to an inbox."""

    rule_id: str
    pattern: str
    inbox: str
    priority: int = 0
    stop_on_match: bool = False
    enabled: bool = True


@dataclass
class RoutedMessage:
    """A message that has been routed and delivered to an inbox."""

    message_id: int
    doc_id: str
    inbox: str
    rule_id: str
    delivered_at: float = 0.0
    payload: dict = field(default_factory=dict)


@dataclass
class RouterStats:
    """Aggregate statistics for a :class:`DocInboxRouter`."""

    total_rules: int
    enabled_rules: int
    total_routings: int
    total_deliveries: int
    unique_inboxes: int


# ---------------------------------------------------------------------------
# Main engine
# ---------------------------------------------------------------------------


class DocInboxRouter:
    """Routes incoming document messages to inboxes via declarative rules."""

    def __init__(self) -> None:
        self._rules: dict[str, RoutingRule] = {}
        self._messages: list[RoutedMessage] = []
        self._by_inbox: dict[str, list[int]] = {}
        self._next_id: int = 1
        self._total_routings: int = 0
        self._lock = threading.Lock()

    # ---- rule management -------------------------------------------------

    def add_rule(self, rule: RoutingRule) -> None:
        """Add or replace a rule (keyed by ``rule_id``)."""
        if not isinstance(rule, RoutingRule):
            raise TypeError("rule must be a RoutingRule")
        with self._lock:
            self._rules[rule.rule_id] = rule

    def remove_rule(self, rule_id: str) -> bool:
        """Remove a rule by id. Returns ``True`` if it existed."""
        with self._lock:
            return self._rules.pop(rule_id, None) is not None

    def enable_rule(self, rule_id: str) -> bool:
        """Mark rule ``rule_id`` enabled. Returns ``True`` if it existed."""
        with self._lock:
            rule = self._rules.get(rule_id)
            if rule is None:
                return False
            rule.enabled = True
            return True

    def disable_rule(self, rule_id: str) -> bool:
        """Mark rule ``rule_id`` disabled. Returns ``True`` if it existed."""
        with self._lock:
            rule = self._rules.get(rule_id)
            if rule is None:
                return False
            rule.enabled = False
            return True

    def get_rule(self, rule_id: str) -> Optional[RoutingRule]:
        """Return rule ``rule_id`` or ``None`` if absent."""
        with self._lock:
            return self._rules.get(rule_id)

    def list_rules(self) -> list[RoutingRule]:
        """Return all rules sorted by (-priority, rule_id)."""
        with self._lock:
            rules = list(self._rules.values())
        rules.sort(key=lambda r: (-r.priority, r.rule_id))
        return rules

    # ---- routing ---------------------------------------------------------

    def route(
        self,
        doc_id: str,
        payload: Optional[dict] = None,
        now: Optional[float] = None,
    ) -> list[RoutedMessage]:
        """Route ``doc_id`` through the rule set.

        Iterates enabled rules ordered by priority (desc). For each rule whose
        pattern matches ``doc_id``, a :class:`RoutedMessage` is created and
        delivered. If the matched rule has ``stop_on_match=True``, routing
        halts after that delivery.

        Returns the list of delivered messages (possibly empty).
        """
        if now is None:
            now = time.time()
        if payload is None:
            payload = {}

        delivered: list[RoutedMessage] = []
        with self._lock:
            self._total_routings += 1
            # Snapshot of enabled rules, sorted deterministically.
            rules = [r for r in self._rules.values() if r.enabled]
            rules.sort(key=lambda r: (-r.priority, r.rule_id))

            for rule in rules:
                if not fnmatch.fnmatchcase(doc_id, rule.pattern):
                    continue
                message = RoutedMessage(
                    message_id=self._next_id,
                    doc_id=doc_id,
                    inbox=rule.inbox,
                    rule_id=rule.rule_id,
                    delivered_at=now,
                    payload=dict(payload),
                )
                self._next_id += 1
                self._messages.append(message)
                self._by_inbox.setdefault(rule.inbox, []).append(message.message_id)
                delivered.append(message)
                if rule.stop_on_match:
                    break

        return delivered

    # ---- message queries -------------------------------------------------

    def messages_for_inbox(
        self, inbox: str, limit: Optional[int] = None
    ) -> list[RoutedMessage]:
        """Return messages delivered to ``inbox``, most recent first."""
        with self._lock:
            ids = list(self._by_inbox.get(inbox, []))
            # Build a quick lookup over current messages.
            by_id = {m.message_id: m for m in self._messages}
        messages = [by_id[i] for i in ids if i in by_id]
        messages.sort(key=lambda m: m.message_id, reverse=True)
        if limit is not None:
            if limit < 0:
                limit = 0
            messages = messages[:limit]
        return messages

    def messages_for_doc(self, doc_id: str) -> list[RoutedMessage]:
        """Return messages routed for ``doc_id``, most recent first."""
        with self._lock:
            matches = [m for m in self._messages if m.doc_id == doc_id]
        matches.sort(key=lambda m: m.message_id, reverse=True)
        return matches

    def clear_inbox(self, inbox: str) -> int:
        """Remove all messages for ``inbox``. Returns number cleared."""
        with self._lock:
            ids = self._by_inbox.pop(inbox, None)
            if not ids:
                return 0
            id_set = set(ids)
            before = len(self._messages)
            self._messages = [m for m in self._messages if m.message_id not in id_set]
            return before - len(self._messages)

    def clear_all_messages(self) -> int:
        """Remove all stored messages. Returns number cleared."""
        with self._lock:
            count = len(self._messages)
            self._messages.clear()
            self._by_inbox.clear()
            return count

    # ---- introspection ---------------------------------------------------

    def inbox_count(self) -> int:
        """Return the number of distinct inboxes that have received messages."""
        with self._lock:
            return sum(1 for ids in self._by_inbox.values() if ids)

    def stats(self) -> RouterStats:
        """Return aggregate router statistics."""
        with self._lock:
            total_rules = len(self._rules)
            enabled_rules = sum(1 for r in self._rules.values() if r.enabled)
            total_routings = self._total_routings
            total_deliveries = len(self._messages)
            unique_inboxes = sum(1 for ids in self._by_inbox.values() if ids)
        return RouterStats(
            total_rules=total_rules,
            enabled_rules=enabled_rules,
            total_routings=total_routings,
            total_deliveries=total_deliveries,
            unique_inboxes=unique_inboxes,
        )
