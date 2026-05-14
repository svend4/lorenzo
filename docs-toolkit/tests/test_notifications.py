"""Tests for docstoolkit.notifications — E11 notification dispatcher."""
import time
import pytest

from docstoolkit.notifications import (
    Notification, NotificationLevel, Channel,
    NotificationHandler, LogHandler, StoreHandler, NullHandler,
    NotificationDispatcher, RoutingRule,
)


# ---------------------------------------------------------------------------
# NotificationLevel enum
# ---------------------------------------------------------------------------

class TestNotificationLevel:
    def test_has_five_values(self):
        assert len(NotificationLevel) == 5

    def test_debug_value(self):
        assert NotificationLevel.DEBUG == "debug"

    def test_info_value(self):
        assert NotificationLevel.INFO == "info"

    def test_warning_value(self):
        assert NotificationLevel.WARNING == "warning"

    def test_error_value(self):
        assert NotificationLevel.ERROR == "error"

    def test_critical_value(self):
        assert NotificationLevel.CRITICAL == "critical"

    def test_is_str_subclass(self):
        assert isinstance(NotificationLevel.INFO, str)


# ---------------------------------------------------------------------------
# Channel enum
# ---------------------------------------------------------------------------

class TestChannel:
    def test_has_five_values(self):
        assert len(Channel) == 5

    def test_log_value(self):
        assert Channel.LOG == "log"

    def test_store_value(self):
        assert Channel.STORE == "store"

    def test_email_value(self):
        assert Channel.EMAIL == "email"

    def test_slack_value(self):
        assert Channel.SLACK == "slack"

    def test_null_value(self):
        assert Channel.NULL == "null"


# ---------------------------------------------------------------------------
# Notification dataclass
# ---------------------------------------------------------------------------

class TestNotification:
    def test_required_fields(self):
        n = Notification(title="Hello", body="World")
        assert n.title == "Hello"
        assert n.body == "World"

    def test_default_level_is_info(self):
        n = Notification(title="t", body="b")
        assert n.level == NotificationLevel.INFO

    def test_default_source_empty(self):
        n = Notification(title="t", body="b")
        assert n.source == ""

    def test_default_tags_empty_list(self):
        n = Notification(title="t", body="b")
        assert n.tags == []

    def test_ts_auto_set(self):
        n = Notification(title="t", body="b")
        assert n.ts != ""

    def test_ts_format_isoformat(self):
        n = Notification(title="t", body="b")
        # Should be parseable ISO format with seconds precision
        from datetime import datetime
        dt = datetime.fromisoformat(n.ts)
        assert dt is not None

    def test_notification_id_auto_generated(self):
        n = Notification(title="t", body="b")
        assert n.notification_id != ""
        assert len(n.notification_id) == 12

    def test_notification_id_is_hex(self):
        n = Notification(title="t", body="b")
        int(n.notification_id, 16)  # should not raise

    def test_explicit_ts_preserved(self):
        n = Notification(title="t", body="b", ts="2025-01-01T00:00:00")
        assert n.ts == "2025-01-01T00:00:00"

    def test_explicit_notification_id_preserved(self):
        n = Notification(title="t", body="b", notification_id="abc123def456")
        assert n.notification_id == "abc123def456"

    def test_is_urgent_error(self):
        n = Notification(title="t", body="b", level=NotificationLevel.ERROR)
        assert n.is_urgent() is True

    def test_is_urgent_critical(self):
        n = Notification(title="t", body="b", level=NotificationLevel.CRITICAL)
        assert n.is_urgent() is True

    def test_is_urgent_false_for_info(self):
        n = Notification(title="t", body="b", level=NotificationLevel.INFO)
        assert n.is_urgent() is False

    def test_is_urgent_false_for_warning(self):
        n = Notification(title="t", body="b", level=NotificationLevel.WARNING)
        assert n.is_urgent() is False

    def test_is_urgent_false_for_debug(self):
        n = Notification(title="t", body="b", level=NotificationLevel.DEBUG)
        assert n.is_urgent() is False

    def test_to_dict_keys(self):
        n = Notification(title="t", body="b")
        d = n.to_dict()
        expected_keys = {"notification_id", "title", "body", "level", "source", "tags", "ts"}
        assert set(d.keys()) == expected_keys

    def test_to_dict_level_is_string(self):
        n = Notification(title="t", body="b", level=NotificationLevel.WARNING)
        assert n.to_dict()["level"] == "warning"

    def test_to_dict_values_match(self):
        n = Notification(title="Hello", body="World", source="rag", tags=["a", "b"])
        d = n.to_dict()
        assert d["title"] == "Hello"
        assert d["body"] == "World"
        assert d["source"] == "rag"
        assert d["tags"] == ["a", "b"]

    def test_different_titles_different_ids(self):
        n1 = Notification(title="Title A", body="b", ts="2025-01-01T00:00:00")
        n2 = Notification(title="Title B", body="b", ts="2025-01-01T00:00:00")
        assert n1.notification_id != n2.notification_id

    def test_different_ts_different_ids(self):
        n1 = Notification(title="Same", body="b", ts="2025-01-01T00:00:00")
        n2 = Notification(title="Same", body="b", ts="2025-01-02T00:00:00")
        assert n1.notification_id != n2.notification_id

    def test_tags_mutable_default_safe(self):
        n1 = Notification(title="t", body="b")
        n2 = Notification(title="t", body="b")
        n1.tags.append("x")
        assert n2.tags == []


# ---------------------------------------------------------------------------
# LogHandler
# ---------------------------------------------------------------------------

class TestLogHandler:
    def test_channel_is_log(self):
        h = LogHandler()
        assert h.channel == Channel.LOG

    def test_send_returns_true(self):
        h = LogHandler()
        n = Notification(title="t", body="b")
        assert h.send(n) is True

    def test_messages_empty_initially(self):
        h = LogHandler()
        assert h.messages() == []

    def test_messages_grows_after_send(self):
        h = LogHandler()
        n = Notification(title="t", body="b")
        h.send(n)
        assert len(h.messages()) == 1

    def test_messages_contains_notification(self):
        h = LogHandler()
        n = Notification(title="Hello", body="Body")
        h.send(n)
        assert h.messages()[0] is n

    def test_messages_multiple(self):
        h = LogHandler()
        for i in range(3):
            h.send(Notification(title=f"t{i}", body="b"))
        assert len(h.messages()) == 3

    def test_clear_empties_log(self):
        h = LogHandler()
        h.send(Notification(title="t", body="b"))
        h.clear()
        assert h.messages() == []

    def test_messages_returns_copy(self):
        h = LogHandler()
        h.send(Notification(title="t", body="b"))
        lst = h.messages()
        lst.clear()
        assert len(h.messages()) == 1

    def test_is_handler_subclass(self):
        assert issubclass(LogHandler, NotificationHandler)


# ---------------------------------------------------------------------------
# NullHandler
# ---------------------------------------------------------------------------

class TestNullHandler:
    def test_channel_is_null(self):
        h = NullHandler()
        assert h.channel == Channel.NULL

    def test_send_returns_true(self):
        h = NullHandler()
        n = Notification(title="t", body="b")
        assert h.send(n) is True

    def test_send_multiple_returns_true(self):
        h = NullHandler()
        for _ in range(5):
            assert h.send(Notification(title="t", body="b")) is True

    def test_is_handler_subclass(self):
        assert issubclass(NullHandler, NotificationHandler)


# ---------------------------------------------------------------------------
# StoreHandler
# ---------------------------------------------------------------------------

class TestStoreHandler:
    def test_channel_is_store(self):
        h = StoreHandler()
        assert h.channel == Channel.STORE

    def test_send_returns_true(self):
        h = StoreHandler()
        n = Notification(title="t", body="b")
        assert h.send(n) is True

    def test_count_starts_at_zero(self):
        h = StoreHandler()
        assert h.count() == 0

    def test_count_increases_after_send(self):
        h = StoreHandler()
        h.send(Notification(title="t", body="b"))
        assert h.count() == 1

    def test_count_multiple(self):
        h = StoreHandler()
        for i in range(4):
            h.send(Notification(title=f"t{i}", body="b", ts=f"2025-01-0{i+1}T00:00:00"))
        assert h.count() == 4

    def test_list_by_level_filters(self):
        h = StoreHandler()
        h.send(Notification(title="e1", body="b", level=NotificationLevel.ERROR, ts="2025-01-01T00:00:00"))
        h.send(Notification(title="i1", body="b", level=NotificationLevel.INFO, ts="2025-01-02T00:00:00"))
        h.send(Notification(title="e2", body="b", level=NotificationLevel.ERROR, ts="2025-01-03T00:00:00"))
        errors = h.list_by_level(NotificationLevel.ERROR)
        assert len(errors) == 2
        infos = h.list_by_level(NotificationLevel.INFO)
        assert len(infos) == 1

    def test_list_by_level_returns_dicts(self):
        h = StoreHandler()
        h.send(Notification(title="t", body="b", level=NotificationLevel.WARNING))
        rows = h.list_by_level(NotificationLevel.WARNING)
        assert isinstance(rows[0], dict)

    def test_duplicate_notification_id_ignored(self):
        h = StoreHandler()
        n = Notification(title="t", body="b", notification_id="fixed_id_001")
        h.send(n)
        # Send same notification again — INSERT OR IGNORE, count stays 1
        h.send(n)
        assert h.count() == 1

    def test_duplicate_send_returns_true(self):
        h = StoreHandler()
        n = Notification(title="t", body="b", notification_id="fixed_id_002")
        h.send(n)
        result = h.send(n)
        assert result is True

    def test_is_handler_subclass(self):
        assert issubclass(StoreHandler, NotificationHandler)

    def test_close_does_not_raise(self):
        h = StoreHandler()
        h.close()  # should not raise


# ---------------------------------------------------------------------------
# RoutingRule.matches
# ---------------------------------------------------------------------------

class TestRoutingRule:
    def _notif(self, level=NotificationLevel.INFO, source="", tags=None):
        return Notification(
            title="t", body="b", level=level,
            source=source, tags=tags or []
        )

    def test_level_below_min_returns_false(self):
        rule = RoutingRule(min_level=NotificationLevel.WARNING)
        assert rule.matches(self._notif(level=NotificationLevel.INFO)) is False

    def test_level_debug_below_info_returns_false(self):
        rule = RoutingRule(min_level=NotificationLevel.INFO)
        assert rule.matches(self._notif(level=NotificationLevel.DEBUG)) is False

    def test_level_at_min_returns_true(self):
        rule = RoutingRule(min_level=NotificationLevel.WARNING)
        assert rule.matches(self._notif(level=NotificationLevel.WARNING)) is True

    def test_level_above_min_returns_true(self):
        rule = RoutingRule(min_level=NotificationLevel.WARNING)
        assert rule.matches(self._notif(level=NotificationLevel.ERROR)) is True

    def test_level_critical_above_all(self):
        rule = RoutingRule(min_level=NotificationLevel.DEBUG)
        assert rule.matches(self._notif(level=NotificationLevel.CRITICAL)) is True

    def test_source_filter_empty_matches_any(self):
        rule = RoutingRule(min_level=NotificationLevel.DEBUG, sources=[])
        assert rule.matches(self._notif(source="anything")) is True

    def test_source_filter_matches_listed_source(self):
        rule = RoutingRule(min_level=NotificationLevel.DEBUG, sources=["rag"])
        assert rule.matches(self._notif(source="rag")) is True

    def test_source_filter_rejects_unlisted_source(self):
        rule = RoutingRule(min_level=NotificationLevel.DEBUG, sources=["rag"])
        assert rule.matches(self._notif(source="ingest")) is False

    def test_source_filter_empty_source_in_notification(self):
        rule = RoutingRule(min_level=NotificationLevel.DEBUG, sources=["rag"])
        assert rule.matches(self._notif(source="")) is False

    def test_tags_filter_empty_matches_any(self):
        rule = RoutingRule(min_level=NotificationLevel.DEBUG, tags=[])
        assert rule.matches(self._notif(tags=["x", "y"])) is True

    def test_tags_filter_notification_must_have_tag(self):
        rule = RoutingRule(min_level=NotificationLevel.DEBUG, tags=["urgent"])
        assert rule.matches(self._notif(tags=["urgent"])) is True

    def test_tags_filter_notification_missing_tag(self):
        rule = RoutingRule(min_level=NotificationLevel.DEBUG, tags=["urgent"])
        assert rule.matches(self._notif(tags=["low-prio"])) is False

    def test_tags_filter_all_tags_required(self):
        rule = RoutingRule(min_level=NotificationLevel.DEBUG, tags=["a", "b"])
        assert rule.matches(self._notif(tags=["a"])) is False  # missing "b"

    def test_tags_filter_all_tags_present(self):
        rule = RoutingRule(min_level=NotificationLevel.DEBUG, tags=["a", "b"])
        assert rule.matches(self._notif(tags=["a", "b", "c"])) is True

    def test_combined_level_and_source(self):
        rule = RoutingRule(min_level=NotificationLevel.ERROR, sources=["rag"])
        # level OK, source OK
        assert rule.matches(self._notif(level=NotificationLevel.ERROR, source="rag")) is True
        # level too low
        assert rule.matches(self._notif(level=NotificationLevel.INFO, source="rag")) is False
        # wrong source
        assert rule.matches(self._notif(level=NotificationLevel.ERROR, source="other")) is False

    def test_combined_level_source_tags(self):
        rule = RoutingRule(
            min_level=NotificationLevel.WARNING,
            sources=["monitor"],
            tags=["critical"],
        )
        assert rule.matches(self._notif(
            level=NotificationLevel.WARNING, source="monitor", tags=["critical"]
        )) is True
        assert rule.matches(self._notif(
            level=NotificationLevel.WARNING, source="monitor", tags=[]
        )) is False


# ---------------------------------------------------------------------------
# NotificationDispatcher
# ---------------------------------------------------------------------------

class TestNotificationDispatcher:
    def _dispatcher_with_log(self):
        d = NotificationDispatcher()
        h = LogHandler()
        d.register_handler(h)
        return d, h

    def test_register_and_dispatch(self):
        d, h = self._dispatcher_with_log()
        rule = RoutingRule(min_level=NotificationLevel.DEBUG, channels=[Channel.LOG])
        d.add_rule(rule)
        n = Notification(title="t", body="b")
        d.dispatch(n)
        assert len(h.messages()) == 1

    def test_no_rules_returns_empty_dict(self):
        d = NotificationDispatcher()
        n = Notification(title="t", body="b")
        result = d.dispatch(n)
        assert result == {}

    def test_no_matching_rule_returns_empty_dict(self):
        d, h = self._dispatcher_with_log()
        rule = RoutingRule(min_level=NotificationLevel.ERROR, channels=[Channel.LOG])
        d.add_rule(rule)
        n = Notification(title="t", body="b", level=NotificationLevel.DEBUG)
        result = d.dispatch(n)
        assert result == {}

    def test_dispatch_returns_channel_success_dict(self):
        d, h = self._dispatcher_with_log()
        rule = RoutingRule(min_level=NotificationLevel.DEBUG, channels=[Channel.LOG])
        d.add_rule(rule)
        n = Notification(title="t", body="b")
        result = d.dispatch(n)
        assert "log" in result
        assert result["log"] is True

    def test_handler_not_registered_skipped_silently(self):
        d = NotificationDispatcher()
        # Add rule targeting EMAIL but no email handler registered
        rule = RoutingRule(min_level=NotificationLevel.DEBUG, channels=[Channel.EMAIL])
        d.add_rule(rule)
        n = Notification(title="t", body="b")
        result = d.dispatch(n)
        # No handler registered for EMAIL → skip, result empty
        assert result == {}

    def test_multiple_rules_can_match(self):
        d = NotificationDispatcher()
        h1 = LogHandler()
        h2 = NullHandler()
        d.register_handler(h1)
        d.register_handler(h2)
        rule1 = RoutingRule(min_level=NotificationLevel.DEBUG, channels=[Channel.LOG])
        rule2 = RoutingRule(min_level=NotificationLevel.DEBUG, channels=[Channel.NULL])
        d.add_rule(rule1)
        d.add_rule(rule2)
        n = Notification(title="t", body="b")
        result = d.dispatch(n)
        assert "log" in result
        assert "null" in result

    def test_multiple_channels_in_one_rule(self):
        d = NotificationDispatcher()
        h_log = LogHandler()
        h_null = NullHandler()
        d.register_handler(h_log)
        d.register_handler(h_null)
        rule = RoutingRule(
            min_level=NotificationLevel.DEBUG,
            channels=[Channel.LOG, Channel.NULL],
        )
        d.add_rule(rule)
        n = Notification(title="t", body="b")
        result = d.dispatch(n)
        assert result.get("log") is True
        assert result.get("null") is True
        assert len(h_log.messages()) == 1

    def test_stats_initial(self):
        d = NotificationDispatcher()
        assert d.stats() == {"sent": 0, "failed": 0}

    def test_stats_sent_increments(self):
        d, h = self._dispatcher_with_log()
        rule = RoutingRule(min_level=NotificationLevel.DEBUG, channels=[Channel.LOG])
        d.add_rule(rule)
        d.dispatch(Notification(title="t", body="b"))
        d.dispatch(Notification(title="t2", body="b"))
        assert d.stats()["sent"] == 2

    def test_stats_failed_increments_on_handler_failure(self):
        class FailHandler(NotificationHandler):
            channel = Channel.EMAIL

            def send(self, notification):
                return False

        d = NotificationDispatcher()
        d.register_handler(FailHandler())
        rule = RoutingRule(min_level=NotificationLevel.DEBUG, channels=[Channel.EMAIL])
        d.add_rule(rule)
        d.dispatch(Notification(title="t", body="b"))
        assert d.stats()["failed"] == 1
        assert d.stats()["sent"] == 0

    def test_stats_sent_and_failed_independent(self):
        class FailHandler(NotificationHandler):
            channel = Channel.EMAIL

            def send(self, notification):
                return False

        d = NotificationDispatcher()
        h_log = LogHandler()
        d.register_handler(h_log)
        d.register_handler(FailHandler())
        rule = RoutingRule(
            min_level=NotificationLevel.DEBUG,
            channels=[Channel.LOG, Channel.EMAIL],
        )
        d.add_rule(rule)
        d.dispatch(Notification(title="t", body="b"))
        assert d.stats()["sent"] == 1
        assert d.stats()["failed"] == 1

    def test_dispatch_with_store_handler(self):
        d = NotificationDispatcher()
        store = StoreHandler()
        d.register_handler(store)
        rule = RoutingRule(min_level=NotificationLevel.DEBUG, channels=[Channel.STORE])
        d.add_rule(rule)
        d.dispatch(Notification(title="t", body="b"))
        assert store.count() == 1

    def test_dispatch_same_notification_to_multiple_handlers(self):
        d = NotificationDispatcher()
        h_log = LogHandler()
        store = StoreHandler()
        d.register_handler(h_log)
        d.register_handler(store)
        rule = RoutingRule(
            min_level=NotificationLevel.DEBUG,
            channels=[Channel.LOG, Channel.STORE],
        )
        d.add_rule(rule)
        n = Notification(title="t", body="b")
        d.dispatch(n)
        assert len(h_log.messages()) == 1
        assert store.count() == 1
