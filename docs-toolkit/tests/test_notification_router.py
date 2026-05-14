"""Tests for docstoolkit.notification_router (E111)."""

from __future__ import annotations

import pytest

from docstoolkit.notification_router import (
    DeliveryStatus,
    DeliveryRecord,
    HandlerConfig,
    Notification,
    NotificationRouter,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_router() -> NotificationRouter:
    """Return a fresh router with a fixed clock."""
    return NotificationRouter(now_fn=lambda: 1_000_000.0)


def _collector() -> tuple[list[Notification], callable]:
    """Return (received_list, handler_fn)."""
    received: list[Notification] = []
    return received, lambda n: received.append(n)


# ---------------------------------------------------------------------------
# 1. Basic register + send
# ---------------------------------------------------------------------------

class TestRegisterAndSend:
    def test_single_handler_receives_notification(self):
        router = _make_router()
        received, handler = _collector()
        router.register(HandlerConfig(name="h1", channel="email", handler=handler))
        records = router.send("user.created", "email", {"user": "alice"})
        assert len(records) == 1
        assert records[0].status == DeliveryStatus.SENT
        assert len(received) == 1

    def test_handler_receives_correct_notification_fields(self):
        router = _make_router()
        received, handler = _collector()
        router.register(HandlerConfig(name="h1", channel="email", handler=handler))
        router.send("order.placed", "email", {"order_id": 42})
        notif = received[0]
        assert notif.event_type == "order.placed"
        assert notif.channel == "email"
        assert notif.payload == {"order_id": 42}

    def test_send_returns_list_of_delivery_records(self):
        router = _make_router()
        _, handler = _collector()
        router.register(HandlerConfig(name="h1", channel="log", handler=handler))
        result = router.send("x", "log")
        assert isinstance(result, list)
        assert all(isinstance(r, DeliveryRecord) for r in result)

    def test_send_with_no_payload_defaults_to_empty_dict(self):
        router = _make_router()
        received, handler = _collector()
        router.register(HandlerConfig(name="h1", channel="log", handler=handler))
        router.send("ping", "log")
        assert received[0].payload == {}

    def test_send_no_matching_handler_returns_empty_list(self):
        router = _make_router()
        records = router.send("x", "email")
        assert records == []

    def test_handler_on_different_channel_not_called(self):
        router = _make_router()
        received, handler = _collector()
        router.register(HandlerConfig(name="h1", channel="webhook", handler=handler))
        records = router.send("x", "email")
        assert records == []
        assert received == []

    def test_notification_timestamp_set_by_now_fn(self):
        router = NotificationRouter(now_fn=lambda: 99.0)
        received, handler = _collector()
        router.register(HandlerConfig(name="h1", channel="log", handler=handler))
        router.send("ping", "log")
        assert received[0].timestamp == 99.0


# ---------------------------------------------------------------------------
# 2. Multiple handlers on the same channel
# ---------------------------------------------------------------------------

class TestMultipleHandlers:
    def test_two_handlers_same_channel_both_called(self):
        router = _make_router()
        r1, h1 = _collector()
        r2, h2 = _collector()
        router.register(HandlerConfig(name="h1", channel="email", handler=h1))
        router.register(HandlerConfig(name="h2", channel="email", handler=h2))
        records = router.send("evt", "email")
        assert len(records) == 2
        assert len(r1) == 1
        assert len(r2) == 1

    def test_three_handlers_all_receive(self):
        router = _make_router()
        buckets = []
        for i in range(3):
            lst, fn = _collector()
            buckets.append(lst)
            router.register(HandlerConfig(name=f"h{i}", channel="log", handler=fn))
        router.send("evt", "log")
        assert all(len(b) == 1 for b in buckets)

    def test_records_have_correct_handler_names(self):
        router = _make_router()
        _, h1 = _collector()
        _, h2 = _collector()
        router.register(HandlerConfig(name="alpha", channel="sms", handler=h1))
        router.register(HandlerConfig(name="beta", channel="sms", handler=h2))
        records = router.send("evt", "sms")
        names = {r.handler_name for r in records}
        assert names == {"alpha", "beta"}


# ---------------------------------------------------------------------------
# 3. event_types filter on HandlerConfig
# ---------------------------------------------------------------------------

class TestEventTypesFilter:
    def test_handler_receives_matching_event_type(self):
        router = _make_router()
        received, handler = _collector()
        router.register(HandlerConfig(
            name="h1", channel="email", handler=handler,
            event_types=["order.placed"],
        ))
        router.send("order.placed", "email")
        assert len(received) == 1

    def test_handler_not_called_for_non_matching_event_type(self):
        router = _make_router()
        received, handler = _collector()
        router.register(HandlerConfig(
            name="h1", channel="email", handler=handler,
            event_types=["order.placed"],
        ))
        records = router.send("user.created", "email")
        assert records == []
        assert received == []

    def test_handler_with_none_event_types_receives_all(self):
        router = _make_router()
        received, handler = _collector()
        router.register(HandlerConfig(
            name="h1", channel="log", handler=handler,
            event_types=None,
        ))
        router.send("a.b", "log")
        router.send("c.d", "log")
        assert len(received) == 2

    def test_handler_with_multiple_event_types(self):
        router = _make_router()
        received, handler = _collector()
        router.register(HandlerConfig(
            name="h1", channel="log", handler=handler,
            event_types=["a", "b", "c"],
        ))
        router.send("b", "log")
        router.send("z", "log")
        assert len(received) == 1
        assert received[0].event_type == "b"

    def test_two_handlers_different_event_types_selective(self):
        router = _make_router()
        r1, h1 = _collector()
        r2, h2 = _collector()
        router.register(HandlerConfig(name="h1", channel="ch", handler=h1, event_types=["A"]))
        router.register(HandlerConfig(name="h2", channel="ch", handler=h2, event_types=["B"]))
        router.send("A", "ch")
        assert len(r1) == 1
        assert len(r2) == 0


# ---------------------------------------------------------------------------
# 4. filter_fn
# ---------------------------------------------------------------------------

class TestFilterFn:
    def test_filter_fn_true_handler_called(self):
        router = _make_router()
        received, handler = _collector()
        router.register(HandlerConfig(
            name="h1", channel="email", handler=handler,
            filter_fn=lambda n: True,
        ))
        records = router.send("evt", "email")
        assert records[0].status == DeliveryStatus.SENT
        assert len(received) == 1

    def test_filter_fn_false_handler_not_called(self):
        router = _make_router()
        received, handler = _collector()
        router.register(HandlerConfig(
            name="h1", channel="email", handler=handler,
            filter_fn=lambda n: False,
        ))
        records = router.send("evt", "email")
        assert len(received) == 0
        assert records[0].status == DeliveryStatus.FILTERED

    def test_filtered_record_has_correct_fields(self):
        router = _make_router()
        _, handler = _collector()
        router.register(HandlerConfig(
            name="myhandler", channel="sms", handler=handler,
            filter_fn=lambda n: False,
        ))
        records = router.send("evt", "sms", {"k": "v"})
        r = records[0]
        assert r.status == DeliveryStatus.FILTERED
        assert r.handler_name == "myhandler"
        assert r.channel == "sms"

    def test_filter_fn_receives_notification(self):
        router = _make_router()
        seen: list[Notification] = []
        _, handler = _collector()
        router.register(HandlerConfig(
            name="h1", channel="log", handler=handler,
            filter_fn=lambda n: (seen.append(n), True)[1],
        ))
        router.send("evt", "log", {"x": 1})
        assert seen[0].payload == {"x": 1}

    def test_filter_fn_payload_based_filter(self):
        router = _make_router()
        received, handler = _collector()
        router.register(HandlerConfig(
            name="h1", channel="email", handler=handler,
            filter_fn=lambda n: n.payload.get("priority") == "high",
        ))
        router.send("alert", "email", {"priority": "low"})
        router.send("alert", "email", {"priority": "high"})
        assert len(received) == 1
        assert received[0].payload["priority"] == "high"

    def test_filter_fn_exception_treated_as_filtered(self):
        """If filter_fn itself raises, treat result as filtered (not failed)."""
        router = _make_router()
        received, handler = _collector()
        def bad_filter(n: Notification) -> bool:
            raise RuntimeError("filter broken")
        router.register(HandlerConfig(
            name="h1", channel="log", handler=handler,
            filter_fn=bad_filter,
        ))
        records = router.send("evt", "log")
        assert records[0].status == DeliveryStatus.FILTERED
        assert len(received) == 0


# ---------------------------------------------------------------------------
# 5. Handler raises → FAILED, other handlers still called
# ---------------------------------------------------------------------------

class TestHandlerFailure:
    def test_handler_exception_produces_failed_record(self):
        router = _make_router()
        def bad_handler(n: Notification) -> None:
            raise ValueError("boom")
        router.register(HandlerConfig(name="bad", channel="log", handler=bad_handler))
        records = router.send("evt", "log")
        assert records[0].status == DeliveryStatus.FAILED

    def test_failed_record_stores_error_message(self):
        router = _make_router()
        def bad_handler(n: Notification) -> None:
            raise RuntimeError("something went wrong")
        router.register(HandlerConfig(name="bad", channel="log", handler=bad_handler))
        records = router.send("evt", "log")
        assert "something went wrong" in records[0].error

    def test_other_handlers_called_after_failure(self):
        router = _make_router()
        def bad_handler(n: Notification) -> None:
            raise ValueError("oops")
        received, good_handler = _collector()
        router.register(HandlerConfig(name="bad", channel="ch", handler=bad_handler))
        router.register(HandlerConfig(name="good", channel="ch", handler=good_handler))
        records = router.send("evt", "ch")
        assert any(r.status == DeliveryStatus.FAILED for r in records)
        assert any(r.status == DeliveryStatus.SENT for r in records)
        assert len(received) == 1

    def test_failed_record_has_correct_handler_name(self):
        router = _make_router()
        def bad_handler(n: Notification) -> None:
            raise Exception("err")
        router.register(HandlerConfig(name="crasher", channel="log", handler=bad_handler))
        records = router.send("evt", "log")
        assert records[0].handler_name == "crasher"

    def test_sent_record_has_empty_error_string(self):
        router = _make_router()
        _, handler = _collector()
        router.register(HandlerConfig(name="ok", channel="log", handler=handler))
        records = router.send("evt", "log")
        assert records[0].error == ""


# ---------------------------------------------------------------------------
# 6. unregister
# ---------------------------------------------------------------------------

class TestUnregister:
    def test_unregister_existing_returns_true(self):
        router = _make_router()
        _, handler = _collector()
        router.register(HandlerConfig(name="h1", channel="log", handler=handler))
        assert router.unregister("h1") is True

    def test_unregister_nonexistent_returns_false(self):
        router = _make_router()
        assert router.unregister("ghost") is False

    def test_unregistered_handler_not_called(self):
        router = _make_router()
        received, handler = _collector()
        router.register(HandlerConfig(name="h1", channel="log", handler=handler))
        router.unregister("h1")
        records = router.send("evt", "log")
        assert records == []
        assert received == []

    def test_unregister_one_of_two(self):
        router = _make_router()
        r1, h1 = _collector()
        r2, h2 = _collector()
        router.register(HandlerConfig(name="h1", channel="ch", handler=h1))
        router.register(HandlerConfig(name="h2", channel="ch", handler=h2))
        router.unregister("h1")
        router.send("evt", "ch")
        assert len(r1) == 0
        assert len(r2) == 1


# ---------------------------------------------------------------------------
# 7. history()
# ---------------------------------------------------------------------------

class TestHistory:
    def test_history_no_filter_returns_all_records(self):
        router = _make_router()
        _, h = _collector()
        router.register(HandlerConfig(name="h1", channel="log", handler=h))
        router.send("e1", "log")
        router.send("e2", "log")
        hist = router.history()
        assert len(hist) == 2

    def test_history_filter_by_notification_id(self):
        router = _make_router()
        _, h = _collector()
        router.register(HandlerConfig(name="h1", channel="log", handler=h))
        r1 = router.send("e1", "log")
        router.send("e2", "log")
        nid = r1[0].notification_id
        hist = router.history(notification_id=nid)
        assert all(r.notification_id == nid for r in hist)
        assert len(hist) == 1

    def test_history_filter_by_channel(self):
        router = _make_router()
        _, h1 = _collector()
        _, h2 = _collector()
        router.register(HandlerConfig(name="h1", channel="email", handler=h1))
        router.register(HandlerConfig(name="h2", channel="sms", handler=h2))
        router.send("evt", "email")
        router.send("evt", "sms")
        email_hist = router.history(channel="email")
        assert all(r.channel == "email" for r in email_hist)
        assert len(email_hist) == 1

    def test_history_filter_by_status_sent(self):
        router = _make_router()
        _, good = _collector()
        def bad(n: Notification) -> None:
            raise Exception("x")
        router.register(HandlerConfig(name="good", channel="ch", handler=good))
        router.register(HandlerConfig(name="bad", channel="ch", handler=bad))
        router.send("evt", "ch")
        sent = router.history(status=DeliveryStatus.SENT)
        assert all(r.status == DeliveryStatus.SENT for r in sent)

    def test_history_filter_by_status_failed(self):
        router = _make_router()
        def bad(n: Notification) -> None:
            raise Exception("x")
        router.register(HandlerConfig(name="bad", channel="ch", handler=bad))
        router.send("evt", "ch")
        failed = router.history(status=DeliveryStatus.FAILED)
        assert len(failed) == 1
        assert failed[0].status == DeliveryStatus.FAILED

    def test_history_filter_by_status_filtered(self):
        router = _make_router()
        _, handler = _collector()
        router.register(HandlerConfig(
            name="h1", channel="ch", handler=handler,
            filter_fn=lambda n: False,
        ))
        router.send("evt", "ch")
        filtered = router.history(status=DeliveryStatus.FILTERED)
        assert len(filtered) == 1
        assert filtered[0].status == DeliveryStatus.FILTERED

    def test_history_combined_filters(self):
        router = _make_router()
        _, h = _collector()
        router.register(HandlerConfig(name="h1", channel="email", handler=h))
        records = router.send("evt", "email")
        nid = records[0].notification_id
        hist = router.history(notification_id=nid, channel="email", status=DeliveryStatus.SENT)
        assert len(hist) == 1

    def test_history_combined_filters_no_match(self):
        router = _make_router()
        _, h = _collector()
        router.register(HandlerConfig(name="h1", channel="email", handler=h))
        router.send("evt", "email")
        hist = router.history(channel="sms")
        assert hist == []

    def test_history_returns_list_copy(self):
        router = _make_router()
        _, h = _collector()
        router.register(HandlerConfig(name="h1", channel="log", handler=h))
        router.send("evt", "log")
        h1 = router.history()
        h2 = router.history()
        assert h1 is not h2


# ---------------------------------------------------------------------------
# 8. clear_history
# ---------------------------------------------------------------------------

class TestClearHistory:
    def test_clear_history_empties_all_records(self):
        router = _make_router()
        _, h = _collector()
        router.register(HandlerConfig(name="h1", channel="log", handler=h))
        router.send("evt", "log")
        assert len(router.history()) == 1
        router.clear_history()
        assert router.history() == []

    def test_new_records_added_after_clear(self):
        router = _make_router()
        _, h = _collector()
        router.register(HandlerConfig(name="h1", channel="log", handler=h))
        router.send("e1", "log")
        router.clear_history()
        router.send("e2", "log")
        assert len(router.history()) == 1

    def test_clear_does_not_unregister_handlers(self):
        router = _make_router()
        _, h = _collector()
        router.register(HandlerConfig(name="h1", channel="log", handler=h))
        router.send("e1", "log")
        router.clear_history()
        router.send("e2", "log")
        # handler still fires
        assert len(router.history()) == 1


# ---------------------------------------------------------------------------
# 9. handler_names
# ---------------------------------------------------------------------------

class TestHandlerNames:
    def test_empty_router_returns_empty_list(self):
        router = _make_router()
        assert router.handler_names() == []

    def test_single_handler_returns_its_name(self):
        router = _make_router()
        _, h = _collector()
        router.register(HandlerConfig(name="alpha", channel="log", handler=h))
        assert router.handler_names() == ["alpha"]

    def test_multiple_handlers_all_names_returned(self):
        router = _make_router()
        for name in ["a", "b", "c"]:
            _, h = _collector()
            router.register(HandlerConfig(name=name, channel="log", handler=h))
        assert set(router.handler_names()) == {"a", "b", "c"}

    def test_handler_names_excludes_unregistered(self):
        router = _make_router()
        _, h = _collector()
        router.register(HandlerConfig(name="keep", channel="log", handler=h))
        router.register(HandlerConfig(name="remove", channel="log", handler=h))
        router.unregister("remove")
        assert "remove" not in router.handler_names()
        assert "keep" in router.handler_names()


# ---------------------------------------------------------------------------
# 10. Duplicate handler name (overwrite)
# ---------------------------------------------------------------------------

class TestDuplicateHandlerOverwrite:
    def test_register_duplicate_name_overwrites(self):
        router = _make_router()
        r1, h1 = _collector()
        r2, h2 = _collector()
        router.register(HandlerConfig(name="h1", channel="log", handler=h1))
        router.register(HandlerConfig(name="h1", channel="log", handler=h2))
        router.send("evt", "log")
        assert len(r1) == 0   # old handler replaced
        assert len(r2) == 1   # new handler called

    def test_duplicate_name_still_single_entry(self):
        router = _make_router()
        _, h = _collector()
        router.register(HandlerConfig(name="h1", channel="log", handler=h))
        router.register(HandlerConfig(name="h1", channel="log", handler=h))
        assert router.handler_names().count("h1") == 1

    def test_duplicate_name_different_channel(self):
        """Same name, different channel — second registration wins."""
        router = _make_router()
        r1, h1 = _collector()
        r2, h2 = _collector()
        router.register(HandlerConfig(name="h1", channel="email", handler=h1))
        router.register(HandlerConfig(name="h1", channel="sms", handler=h2))
        # After overwrite, h1 on email is gone; h2 on sms takes its slot.
        router.send("evt", "email")
        router.send("evt", "sms")
        assert len(r1) == 0
        assert len(r2) == 1


# ---------------------------------------------------------------------------
# 11. Multiple channels (isolation)
# ---------------------------------------------------------------------------

class TestMultipleChannelIsolation:
    def test_handlers_only_receive_their_channel(self):
        router = _make_router()
        email_recv, email_h = _collector()
        sms_recv, sms_h = _collector()
        router.register(HandlerConfig(name="email_h", channel="email", handler=email_h))
        router.register(HandlerConfig(name="sms_h", channel="sms", handler=sms_h))
        router.send("evt", "email")
        assert len(email_recv) == 1
        assert len(sms_recv) == 0

    def test_send_to_channel_with_no_handlers_returns_empty(self):
        router = _make_router()
        _, h = _collector()
        router.register(HandlerConfig(name="h1", channel="webhook", handler=h))
        records = router.send("evt", "slack")
        assert records == []

    def test_cross_channel_records_independent(self):
        router = _make_router()
        _, h1 = _collector()
        _, h2 = _collector()
        router.register(HandlerConfig(name="h1", channel="email", handler=h1))
        router.register(HandlerConfig(name="h2", channel="sms", handler=h2))
        r_email = router.send("evt", "email")
        r_sms = router.send("evt", "sms")
        assert len(r_email) == 1
        assert len(r_sms) == 1
        assert r_email[0].channel == "email"
        assert r_sms[0].channel == "sms"


# ---------------------------------------------------------------------------
# 12. send_notification with pre-built Notification
# ---------------------------------------------------------------------------

class TestSendNotification:
    def test_send_notification_routes_to_correct_channel(self):
        router = _make_router()
        received, handler = _collector()
        router.register(HandlerConfig(name="h1", channel="email", handler=handler))
        notif = Notification(event_type="welcome", channel="email", payload={"to": "bob"})
        records = router.send_notification(notif)
        assert len(records) == 1
        assert records[0].status == DeliveryStatus.SENT
        assert received[0] is notif

    def test_send_notification_preserves_notification_id(self):
        router = _make_router()
        _, handler = _collector()
        router.register(HandlerConfig(name="h1", channel="log", handler=handler))
        notif = Notification(event_type="e", channel="log", notification_id="custom123")
        records = router.send_notification(notif)
        assert records[0].notification_id == "custom123"

    def test_send_notification_event_type_filter_respected(self):
        router = _make_router()
        received, handler = _collector()
        router.register(HandlerConfig(
            name="h1", channel="log", handler=handler,
            event_types=["only.this"],
        ))
        notif = Notification(event_type="other", channel="log")
        records = router.send_notification(notif)
        assert records == []
        assert received == []

    def test_send_notification_filter_fn_respected(self):
        router = _make_router()
        received, handler = _collector()
        router.register(HandlerConfig(
            name="h1", channel="log", handler=handler,
            filter_fn=lambda n: False,
        ))
        notif = Notification(event_type="e", channel="log")
        records = router.send_notification(notif)
        assert records[0].status == DeliveryStatus.FILTERED
        assert received == []

    def test_send_notification_stored_in_history(self):
        router = _make_router()
        _, handler = _collector()
        router.register(HandlerConfig(name="h1", channel="log", handler=handler))
        notif = Notification(event_type="e", channel="log", notification_id="abc123")
        router.send_notification(notif)
        hist = router.history(notification_id="abc123")
        assert len(hist) == 1


# ---------------------------------------------------------------------------
# 13. Notification dataclass
# ---------------------------------------------------------------------------

class TestNotificationDataclass:
    def test_notification_has_auto_id(self):
        n = Notification(event_type="e", channel="ch")
        assert isinstance(n.notification_id, str)
        assert len(n.notification_id) == 12

    def test_notifications_have_unique_ids(self):
        ids = {Notification(event_type="e", channel="ch").notification_id for _ in range(50)}
        assert len(ids) == 50

    def test_notification_default_payload_is_empty_dict(self):
        n = Notification(event_type="e", channel="ch")
        assert n.payload == {}

    def test_notification_payload_not_shared_between_instances(self):
        n1 = Notification(event_type="e", channel="ch")
        n2 = Notification(event_type="e", channel="ch")
        n1.payload["k"] = 1
        assert "k" not in n2.payload

    def test_notification_timestamp_nonzero_by_default(self):
        n = Notification(event_type="e", channel="ch")
        assert n.timestamp > 0


# ---------------------------------------------------------------------------
# 14. DeliveryRecord dataclass
# ---------------------------------------------------------------------------

class TestDeliveryRecord:
    def test_delivery_record_default_error_empty(self):
        r = DeliveryRecord(
            notification_id="x", channel="log",
            handler_name="h", status=DeliveryStatus.SENT,
        )
        assert r.error == ""

    def test_delivery_record_fields_accessible(self):
        r = DeliveryRecord(
            notification_id="abc", channel="email",
            handler_name="mailer", status=DeliveryStatus.FAILED,
            error="timeout",
        )
        assert r.notification_id == "abc"
        assert r.channel == "email"
        assert r.handler_name == "mailer"
        assert r.status == DeliveryStatus.FAILED
        assert r.error == "timeout"


# ---------------------------------------------------------------------------
# 15. DeliveryStatus enum
# ---------------------------------------------------------------------------

class TestDeliveryStatusEnum:
    def test_sent_value(self):
        assert DeliveryStatus.SENT == "sent"

    def test_failed_value(self):
        assert DeliveryStatus.FAILED == "failed"

    def test_filtered_value(self):
        assert DeliveryStatus.FILTERED == "filtered"

    def test_is_str_subclass(self):
        assert isinstance(DeliveryStatus.SENT, str)


# ---------------------------------------------------------------------------
# 16. Payload passthrough
# ---------------------------------------------------------------------------

class TestPayloadPassthrough:
    def test_payload_passed_unchanged_to_handler(self):
        router = _make_router()
        received, handler = _collector()
        router.register(HandlerConfig(name="h1", channel="log", handler=handler))
        payload = {"nested": {"a": [1, 2, 3]}, "count": 5}
        router.send("evt", "log", payload)
        assert received[0].payload == payload

    def test_payload_is_same_object_as_sent(self):
        """Router does not deep-copy payload."""
        router = _make_router()
        received, handler = _collector()
        router.register(HandlerConfig(name="h1", channel="log", handler=handler))
        payload = {"key": "value"}
        router.send("evt", "log", payload)
        assert received[0].payload is payload


# ---------------------------------------------------------------------------
# 17. Integration / edge cases
# ---------------------------------------------------------------------------

class TestIntegration:
    def test_many_sends_accumulate_history(self):
        router = _make_router()
        _, h = _collector()
        router.register(HandlerConfig(name="h1", channel="log", handler=h))
        for _ in range(10):
            router.send("evt", "log")
        assert len(router.history()) == 10

    def test_handler_names_after_multiple_registers_and_unregisters(self):
        router = _make_router()
        _, h = _collector()
        for name in ["a", "b", "c", "d"]:
            router.register(HandlerConfig(name=name, channel="log", handler=h))
        router.unregister("b")
        router.unregister("d")
        names = router.handler_names()
        assert set(names) == {"a", "c"}

    def test_send_after_all_unregistered_returns_empty(self):
        router = _make_router()
        _, h = _collector()
        router.register(HandlerConfig(name="h1", channel="log", handler=h))
        router.unregister("h1")
        assert router.send("evt", "log") == []

    def test_history_reflects_all_statuses_correctly(self):
        router = _make_router()
        _, good = _collector()
        def bad(n: Notification) -> None:
            raise RuntimeError("err")
        router.register(HandlerConfig(name="good", channel="ch", handler=good))
        router.register(HandlerConfig(name="bad", channel="ch", handler=bad))
        router.register(HandlerConfig(
            name="filtered", channel="ch", handler=good,
            filter_fn=lambda n: False,
        ))
        router.send("evt", "ch")
        statuses = {r.handler_name: r.status for r in router.history()}
        assert statuses["good"] == DeliveryStatus.SENT
        assert statuses["bad"] == DeliveryStatus.FAILED
        assert statuses["filtered"] == DeliveryStatus.FILTERED

    def test_notification_id_in_records_matches_notification(self):
        router = _make_router()
        received, handler = _collector()
        router.register(HandlerConfig(name="h1", channel="log", handler=handler))
        records = router.send("evt", "log")
        assert records[0].notification_id == received[0].notification_id
