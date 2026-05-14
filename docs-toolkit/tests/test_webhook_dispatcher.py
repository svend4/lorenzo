"""Tests for docstoolkit.webhook_dispatcher."""

from __future__ import annotations

import pytest

from docstoolkit.webhook_dispatcher import (
    Delivery,
    DeliveryStatus,
    DispatcherStats,
    Subscription,
    WebhookDispatcher,
)


class MockTransport:
    """Records calls and returns programmed responses."""

    def __init__(self, default=(True, None)):
        self.calls: list = []
        self.default = default
        self.responses: list = []

    def queue(self, response):
        self.responses.append(response)

    def __call__(self, url, payload, signature, headers):
        self.calls.append(
            {"url": url, "payload": payload, "signature": signature, "headers": headers}
        )
        if self.responses:
            return self.responses.pop(0)
        return self.default


# ----------------------------------------------------------------------
class TestDeliveryStatus:
    def test_has_pending(self):
        assert DeliveryStatus.PENDING.value == "pending"

    def test_has_in_flight(self):
        assert DeliveryStatus.IN_FLIGHT.value == "in_flight"

    def test_has_delivered(self):
        assert DeliveryStatus.DELIVERED.value == "delivered"

    def test_has_failed(self):
        assert DeliveryStatus.FAILED.value == "failed"

    def test_has_abandoned(self):
        assert DeliveryStatus.ABANDONED.value == "abandoned"

    def test_distinct_values(self):
        values = {s.value for s in DeliveryStatus}
        assert len(values) == 5


# ----------------------------------------------------------------------
class TestSubscription:
    def test_create(self):
        s = Subscription(sub_id="s1", url="http://x", secret="k", event_types={"a"})
        assert s.sub_id == "s1"
        assert s.url == "http://x"
        assert s.enabled is True

    def test_default_enabled(self):
        s = Subscription(sub_id="s1", url="u", secret="k", event_types=set())
        assert s.enabled is True

    def test_default_created_at(self):
        s = Subscription(sub_id="s1", url="u", secret="k", event_types=set())
        assert s.created_at == 0.0


# ----------------------------------------------------------------------
class TestDelivery:
    def test_create(self):
        d = Delivery(
            delivery_id=1,
            sub_id="s1",
            event_type="doc.created",
            payload={"x": 1},
            status=DeliveryStatus.PENDING,
        )
        assert d.delivery_id == 1
        assert d.attempts == 0
        assert d.last_error is None

    def test_defaults(self):
        d = Delivery(
            delivery_id=1,
            sub_id="s1",
            event_type="e",
            payload={},
            status=DeliveryStatus.PENDING,
        )
        assert d.signature == ""
        assert d.next_retry_at == 0.0


# ----------------------------------------------------------------------
class TestDispatcherStats:
    def test_create_defaults(self):
        s = DispatcherStats()
        assert s.total_subscriptions == 0
        assert s.total_deliveries == 0

    def test_success_rate_zero(self):
        s = DispatcherStats()
        assert s.success_rate == 0.0

    def test_success_rate_nonzero(self):
        s = DispatcherStats(total_deliveries=10, delivered=7)
        assert s.success_rate == 0.7


# ----------------------------------------------------------------------
class TestSubscribe:
    def test_returns_subscription(self):
        d = WebhookDispatcher()
        s = d.subscribe("http://x", "k", {"e"})
        assert isinstance(s, Subscription)

    def test_unique_ids(self):
        d = WebhookDispatcher()
        s1 = d.subscribe("u", "k", {"e"})
        s2 = d.subscribe("u", "k", {"e"})
        assert s1.sub_id != s2.sub_id

    def test_records_url(self):
        d = WebhookDispatcher()
        s = d.subscribe("http://hook", "k", {"e"})
        assert s.url == "http://hook"

    def test_records_secret(self):
        d = WebhookDispatcher()
        s = d.subscribe("u", "topsecret", {"e"})
        assert s.secret == "topsecret"

    def test_records_event_types(self):
        d = WebhookDispatcher()
        s = d.subscribe("u", "k", {"a", "b"})
        assert s.event_types == {"a", "b"}

    def test_now_propagated(self):
        d = WebhookDispatcher()
        s = d.subscribe("u", "k", {"e"}, now=100.0)
        assert s.created_at == 100.0

    def test_increments_count(self):
        d = WebhookDispatcher()
        assert d.subscription_count == 0
        d.subscribe("u", "k", {"e"})
        assert d.subscription_count == 1


# ----------------------------------------------------------------------
class TestUnsubscribe:
    def test_returns_true(self):
        d = WebhookDispatcher()
        s = d.subscribe("u", "k", {"e"})
        assert d.unsubscribe(s.sub_id) is True

    def test_removes_from_count(self):
        d = WebhookDispatcher()
        s = d.subscribe("u", "k", {"e"})
        d.unsubscribe(s.sub_id)
        assert d.subscription_count == 0

    def test_returns_false_unknown(self):
        d = WebhookDispatcher()
        assert d.unsubscribe("nope") is False


# ----------------------------------------------------------------------
class TestEnableDisable:
    def test_disable_returns_true(self):
        d = WebhookDispatcher()
        s = d.subscribe("u", "k", {"e"})
        assert d.disable_subscription(s.sub_id) is True

    def test_disable_flag(self):
        d = WebhookDispatcher()
        s = d.subscribe("u", "k", {"e"})
        d.disable_subscription(s.sub_id)
        assert s.enabled is False

    def test_enable_flag(self):
        d = WebhookDispatcher()
        s = d.subscribe("u", "k", {"e"})
        d.disable_subscription(s.sub_id)
        d.enable_subscription(s.sub_id)
        assert s.enabled is True

    def test_disable_unknown(self):
        d = WebhookDispatcher()
        assert d.disable_subscription("nope") is False

    def test_enable_unknown(self):
        d = WebhookDispatcher()
        assert d.enable_subscription("nope") is False

    def test_disabled_does_not_dispatch(self):
        d = WebhookDispatcher()
        s = d.subscribe("u", "k", {"e"})
        d.disable_subscription(s.sub_id)
        created = d.dispatch("e", {"x": 1})
        assert created == []


# ----------------------------------------------------------------------
class TestDispatch:
    def test_creates_delivery(self):
        d = WebhookDispatcher()
        d.subscribe("u", "k", {"e"})
        created = d.dispatch("e", {"x": 1})
        assert len(created) == 1

    def test_status_pending(self):
        d = WebhookDispatcher()
        d.subscribe("u", "k", {"e"})
        created = d.dispatch("e", {"x": 1})
        assert created[0].status == DeliveryStatus.PENDING

    def test_no_match_no_delivery(self):
        d = WebhookDispatcher()
        d.subscribe("u", "k", {"other"})
        created = d.dispatch("e", {"x": 1})
        assert created == []

    def test_signed(self):
        d = WebhookDispatcher()
        d.subscribe("u", "k", {"e"})
        created = d.dispatch("e", {"x": 1})
        assert created[0].signature != ""

    def test_multiple_subs(self):
        d = WebhookDispatcher()
        d.subscribe("u1", "k", {"e"})
        d.subscribe("u2", "k", {"e"})
        created = d.dispatch("e", {"x": 1})
        assert len(created) == 2

    def test_records_event_type(self):
        d = WebhookDispatcher()
        d.subscribe("u", "k", {"e"})
        created = d.dispatch("e", {"x": 1})
        assert created[0].event_type == "e"

    def test_payload_copied(self):
        d = WebhookDispatcher()
        d.subscribe("u", "k", {"e"})
        payload = {"x": 1}
        created = d.dispatch("e", payload)
        payload["x"] = 2
        assert created[0].payload["x"] == 1


# ----------------------------------------------------------------------
class TestDeliverPending:
    def test_no_pending(self):
        d = WebhookDispatcher()
        assert d.deliver_pending() == 0

    def test_processes_one(self):
        t = MockTransport()
        d = WebhookDispatcher(transport=t)
        d.subscribe("u", "k", {"e"})
        d.dispatch("e", {"x": 1})
        n = d.deliver_pending()
        assert n == 1

    def test_calls_transport(self):
        t = MockTransport()
        d = WebhookDispatcher(transport=t)
        d.subscribe("http://hook", "k", {"e"})
        d.dispatch("e", {"x": 1})
        d.deliver_pending()
        assert len(t.calls) == 1
        assert t.calls[0]["url"] == "http://hook"

    def test_status_delivered_on_success(self):
        t = MockTransport(default=(True, None))
        d = WebhookDispatcher(transport=t)
        d.subscribe("u", "k", {"e"})
        created = d.dispatch("e", {"x": 1})
        d.deliver_pending()
        assert created[0].status == DeliveryStatus.DELIVERED

    def test_attempts_incremented(self):
        t = MockTransport()
        d = WebhookDispatcher(transport=t)
        d.subscribe("u", "k", {"e"})
        created = d.dispatch("e", {"x": 1})
        d.deliver_pending()
        assert created[0].attempts == 1

    def test_batch_size_limit(self):
        t = MockTransport()
        d = WebhookDispatcher(transport=t)
        d.subscribe("u", "k", {"e"})
        for _ in range(5):
            d.dispatch("e", {"x": 1})
        n = d.deliver_pending(batch_size=2)
        assert n == 2

    def test_skips_not_ready(self):
        t = MockTransport()
        d = WebhookDispatcher(transport=t)
        d.subscribe("u", "k", {"e"})
        d.dispatch("e", {"x": 1}, now=100.0)
        n = d.deliver_pending(now=50.0)
        assert n == 0

    def test_signature_passed_to_transport(self):
        t = MockTransport()
        d = WebhookDispatcher(transport=t)
        d.subscribe("u", "k", {"e"})
        created = d.dispatch("e", {"x": 1})
        d.deliver_pending()
        assert t.calls[0]["signature"] == created[0].signature

    def test_headers_include_event(self):
        t = MockTransport()
        d = WebhookDispatcher(transport=t)
        d.subscribe("u", "k", {"e"})
        d.dispatch("e", {"x": 1})
        d.deliver_pending()
        assert t.calls[0]["headers"]["X-Webhook-Event"] == "e"


# ----------------------------------------------------------------------
class TestSignPayload:
    def test_returns_hex(self):
        d = WebhookDispatcher()
        sig = d.sign_payload({"x": 1}, "k")
        assert all(c in "0123456789abcdef" for c in sig)

    def test_length_sha256(self):
        d = WebhookDispatcher()
        sig = d.sign_payload({"x": 1}, "k")
        assert len(sig) == 64

    def test_deterministic(self):
        d = WebhookDispatcher()
        a = d.sign_payload({"x": 1, "y": 2}, "k")
        b = d.sign_payload({"y": 2, "x": 1}, "k")
        assert a == b

    def test_secret_matters(self):
        d = WebhookDispatcher()
        a = d.sign_payload({"x": 1}, "k1")
        b = d.sign_payload({"x": 1}, "k2")
        assert a != b

    def test_payload_matters(self):
        d = WebhookDispatcher()
        a = d.sign_payload({"x": 1}, "k")
        b = d.sign_payload({"x": 2}, "k")
        assert a != b


# ----------------------------------------------------------------------
class TestVerifySignature:
    def test_valid(self):
        d = WebhookDispatcher()
        sig = d.sign_payload({"x": 1}, "k")
        assert d.verify_signature({"x": 1}, sig, "k") is True

    def test_wrong_secret(self):
        d = WebhookDispatcher()
        sig = d.sign_payload({"x": 1}, "k")
        assert d.verify_signature({"x": 1}, sig, "other") is False

    def test_tampered_payload(self):
        d = WebhookDispatcher()
        sig = d.sign_payload({"x": 1}, "k")
        assert d.verify_signature({"x": 2}, sig, "k") is False

    def test_bad_signature(self):
        d = WebhookDispatcher()
        assert d.verify_signature({"x": 1}, "bad", "k") is False


# ----------------------------------------------------------------------
class TestGetDelivery:
    def test_existing(self):
        d = WebhookDispatcher()
        d.subscribe("u", "k", {"e"})
        created = d.dispatch("e", {"x": 1})
        got = d.get_delivery(created[0].delivery_id)
        assert got is created[0]

    def test_unknown(self):
        d = WebhookDispatcher()
        assert d.get_delivery(9999) is None


# ----------------------------------------------------------------------
class TestPendingDeliveries:
    def test_empty(self):
        d = WebhookDispatcher()
        assert d.pending_deliveries() == []

    def test_includes_pending(self):
        d = WebhookDispatcher()
        d.subscribe("u", "k", {"e"})
        d.dispatch("e", {"x": 1})
        assert len(d.pending_deliveries()) == 1

    def test_excludes_delivered(self):
        t = MockTransport()
        d = WebhookDispatcher(transport=t)
        d.subscribe("u", "k", {"e"})
        d.dispatch("e", {"x": 1})
        d.deliver_pending()
        assert d.pending_deliveries() == []

    def test_respects_now(self):
        d = WebhookDispatcher()
        d.subscribe("u", "k", {"e"})
        d.dispatch("e", {"x": 1}, now=100.0)
        assert d.pending_deliveries(now=50.0) == []
        assert len(d.pending_deliveries(now=200.0)) == 1


# ----------------------------------------------------------------------
class TestDeliveriesForSubscription:
    def test_empty(self):
        d = WebhookDispatcher()
        s = d.subscribe("u", "k", {"e"})
        assert d.deliveries_for_subscription(s.sub_id) == []

    def test_one(self):
        d = WebhookDispatcher()
        s = d.subscribe("u", "k", {"e"})
        d.dispatch("e", {"x": 1})
        assert len(d.deliveries_for_subscription(s.sub_id)) == 1

    def test_only_for_that_sub(self):
        d = WebhookDispatcher()
        s1 = d.subscribe("u1", "k", {"e"})
        s2 = d.subscribe("u2", "k", {"e"})
        d.dispatch("e", {"x": 1})
        assert len(d.deliveries_for_subscription(s1.sub_id)) == 1
        assert len(d.deliveries_for_subscription(s2.sub_id)) == 1


# ----------------------------------------------------------------------
class TestMatchesEventStar:
    def test_star_matches_any(self):
        d = WebhookDispatcher()
        sub = Subscription(sub_id="s", url="u", secret="k", event_types={"*"})
        assert d.matches_event(sub, "doc.created") is True

    def test_star_matches_empty(self):
        d = WebhookDispatcher()
        sub = Subscription(sub_id="s", url="u", secret="k", event_types={"*"})
        assert d.matches_event(sub, "anything") is True


# ----------------------------------------------------------------------
class TestMatchesEventWildcard:
    def test_prefix_matches(self):
        d = WebhookDispatcher()
        sub = Subscription(sub_id="s", url="u", secret="k", event_types={"doc.*"})
        assert d.matches_event(sub, "doc.created") is True

    def test_prefix_matches_updated(self):
        d = WebhookDispatcher()
        sub = Subscription(sub_id="s", url="u", secret="k", event_types={"doc.*"})
        assert d.matches_event(sub, "doc.updated") is True

    def test_prefix_no_match_other_namespace(self):
        d = WebhookDispatcher()
        sub = Subscription(sub_id="s", url="u", secret="k", event_types={"doc.*"})
        assert d.matches_event(sub, "user.created") is False

    def test_prefix_does_not_match_base(self):
        d = WebhookDispatcher()
        sub = Subscription(sub_id="s", url="u", secret="k", event_types={"doc.*"})
        assert d.matches_event(sub, "doc") is False


# ----------------------------------------------------------------------
class TestMatchesEventExact:
    def test_exact_match(self):
        d = WebhookDispatcher()
        sub = Subscription(sub_id="s", url="u", secret="k", event_types={"doc.deleted"})
        assert d.matches_event(sub, "doc.deleted") is True

    def test_exact_no_match(self):
        d = WebhookDispatcher()
        sub = Subscription(sub_id="s", url="u", secret="k", event_types={"doc.deleted"})
        assert d.matches_event(sub, "doc.created") is False

    def test_empty_event_types(self):
        d = WebhookDispatcher()
        sub = Subscription(sub_id="s", url="u", secret="k", event_types=set())
        assert d.matches_event(sub, "anything") is False


# ----------------------------------------------------------------------
class TestRetry:
    def test_failure_marks_failed(self):
        t = MockTransport(default=(False, "boom"))
        d = WebhookDispatcher(transport=t, max_retries=3)
        d.subscribe("u", "k", {"e"})
        created = d.dispatch("e", {"x": 1})
        d.deliver_pending()
        assert created[0].status == DeliveryStatus.FAILED

    def test_failure_records_error(self):
        t = MockTransport(default=(False, "boom"))
        d = WebhookDispatcher(transport=t)
        d.subscribe("u", "k", {"e"})
        created = d.dispatch("e", {"x": 1})
        d.deliver_pending()
        assert created[0].last_error == "boom"

    def test_next_retry_at_exponential(self):
        t = MockTransport(default=(False, "boom"))
        d = WebhookDispatcher(transport=t)
        d.subscribe("u", "k", {"e"})
        created = d.dispatch("e", {"x": 1}, now=0.0)
        d.deliver_pending(now=0.0)
        # attempts=1, so 2^1 = 2
        assert created[0].next_retry_at == 0.0 + 2

    def test_retries_succeed_eventually(self):
        t = MockTransport()
        t.queue((False, "err"))
        t.queue((True, None))
        d = WebhookDispatcher(transport=t, max_retries=3)
        d.subscribe("u", "k", {"e"})
        created = d.dispatch("e", {"x": 1}, now=0.0)
        d.deliver_pending(now=0.0)
        assert created[0].status == DeliveryStatus.FAILED
        # advance time and retry
        d.deliver_pending(now=100.0)
        assert created[0].status == DeliveryStatus.DELIVERED

    def test_retry_increments_attempts(self):
        t = MockTransport(default=(False, "err"))
        d = WebhookDispatcher(transport=t, max_retries=5)
        d.subscribe("u", "k", {"e"})
        created = d.dispatch("e", {"x": 1}, now=0.0)
        d.deliver_pending(now=0.0)
        d.deliver_pending(now=100.0)
        assert created[0].attempts == 2


# ----------------------------------------------------------------------
class TestAbandoned:
    def test_after_max_retries(self):
        t = MockTransport(default=(False, "err"))
        d = WebhookDispatcher(transport=t, max_retries=2)
        d.subscribe("u", "k", {"e"})
        created = d.dispatch("e", {"x": 1}, now=0.0)
        # attempt 1
        d.deliver_pending(now=0.0)
        # attempt 2
        d.deliver_pending(now=100.0)
        # attempt 3 → abandoned (attempts > max_retries=2)
        d.deliver_pending(now=200.0)
        assert created[0].status == DeliveryStatus.ABANDONED

    def test_abandoned_no_more_retries(self):
        t = MockTransport(default=(False, "err"))
        d = WebhookDispatcher(transport=t, max_retries=1)
        d.subscribe("u", "k", {"e"})
        created = d.dispatch("e", {"x": 1}, now=0.0)
        d.deliver_pending(now=0.0)
        d.deliver_pending(now=100.0)
        assert created[0].status == DeliveryStatus.ABANDONED
        # Further deliver_pending should not process abandoned
        n = d.deliver_pending(now=1000.0)
        assert n == 0

    def test_abandoned_when_subscription_removed(self):
        t = MockTransport()
        d = WebhookDispatcher(transport=t)
        s = d.subscribe("u", "k", {"e"})
        created = d.dispatch("e", {"x": 1})
        d.unsubscribe(s.sub_id)
        d.deliver_pending()
        assert created[0].status == DeliveryStatus.ABANDONED


# ----------------------------------------------------------------------
class TestStats:
    def test_initial(self):
        d = WebhookDispatcher()
        s = d.stats()
        assert s.total_subscriptions == 0
        assert s.total_deliveries == 0

    def test_after_subscribe(self):
        d = WebhookDispatcher()
        d.subscribe("u", "k", {"e"})
        assert d.stats().total_subscriptions == 1

    def test_after_dispatch(self):
        d = WebhookDispatcher()
        d.subscribe("u", "k", {"e"})
        d.dispatch("e", {"x": 1})
        s = d.stats()
        assert s.total_deliveries == 1
        assert s.pending == 1

    def test_after_delivery(self):
        t = MockTransport()
        d = WebhookDispatcher(transport=t)
        d.subscribe("u", "k", {"e"})
        d.dispatch("e", {"x": 1})
        d.deliver_pending()
        s = d.stats()
        assert s.delivered == 1
        assert s.pending == 0

    def test_failed_count(self):
        t = MockTransport(default=(False, "err"))
        d = WebhookDispatcher(transport=t)
        d.subscribe("u", "k", {"e"})
        d.dispatch("e", {"x": 1})
        d.deliver_pending()
        assert d.stats().failed == 1


# ----------------------------------------------------------------------
class TestSuccessRate:
    def test_zero_when_no_deliveries(self):
        d = WebhookDispatcher()
        assert d.stats().success_rate == 0.0

    def test_full_success(self):
        t = MockTransport()
        d = WebhookDispatcher(transport=t)
        d.subscribe("u", "k", {"e"})
        d.dispatch("e", {"x": 1})
        d.deliver_pending()
        assert d.stats().success_rate == 1.0

    def test_partial(self):
        t = MockTransport()
        t.queue((True, None))
        t.queue((False, "err"))
        d = WebhookDispatcher(transport=t)
        d.subscribe("u", "k", {"e"})
        d.dispatch("e", {"x": 1})
        d.dispatch("e", {"x": 2})
        d.deliver_pending()
        s = d.stats()
        assert s.success_rate == 0.5


# ----------------------------------------------------------------------
class TestClear:
    def test_subscriptions_cleared(self):
        d = WebhookDispatcher()
        d.subscribe("u", "k", {"e"})
        d.clear()
        assert d.subscription_count == 0

    def test_deliveries_cleared(self):
        d = WebhookDispatcher()
        d.subscribe("u", "k", {"e"})
        d.dispatch("e", {"x": 1})
        d.clear()
        assert d.stats().total_deliveries == 0

    def test_ids_reset(self):
        d = WebhookDispatcher()
        d.subscribe("u", "k", {"e"})
        d.clear()
        s = d.subscribe("u", "k", {"e"})
        assert s.sub_id == "sub_1"


# ----------------------------------------------------------------------
class TestEdgeCases:
    def test_dispatch_no_subscriptions(self):
        d = WebhookDispatcher()
        assert d.dispatch("e", {"x": 1}) == []

    def test_empty_payload(self):
        t = MockTransport()
        d = WebhookDispatcher(transport=t)
        d.subscribe("u", "k", {"e"})
        created = d.dispatch("e", {})
        d.deliver_pending()
        assert created[0].status == DeliveryStatus.DELIVERED

    def test_signature_consistency_across_dispatch(self):
        d = WebhookDispatcher()
        s = d.subscribe("u", "k", {"e"})
        c1 = d.dispatch("e", {"x": 1})
        c2 = d.dispatch("e", {"x": 1})
        assert c1[0].signature == c2[0].signature

    def test_multiple_patterns_one_subscription(self):
        d = WebhookDispatcher()
        sub = Subscription(
            sub_id="s", url="u", secret="k", event_types={"doc.*", "user.created"}
        )
        assert d.matches_event(sub, "doc.x") is True
        assert d.matches_event(sub, "user.created") is True
        assert d.matches_event(sub, "other") is False

    def test_in_flight_transient(self):
        # IN_FLIGHT is set during deliver_pending — verify a successful
        # call ends up DELIVERED (not stuck IN_FLIGHT).
        t = MockTransport()
        d = WebhookDispatcher(transport=t)
        d.subscribe("u", "k", {"e"})
        created = d.dispatch("e", {"x": 1})
        d.deliver_pending()
        assert created[0].status != DeliveryStatus.IN_FLIGHT

    def test_default_transport_succeeds(self):
        d = WebhookDispatcher()
        d.subscribe("u", "k", {"e"})
        created = d.dispatch("e", {"x": 1})
        d.deliver_pending()
        assert created[0].status == DeliveryStatus.DELIVERED


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
