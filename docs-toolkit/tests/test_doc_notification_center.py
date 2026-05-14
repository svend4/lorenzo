"""Tests for E282 DocNotificationCenter."""
import threading
from docstoolkit.doc_notification_center import (
    DocNotificationCenter,
    Notification,
    NotifStats,
    Subscription,
)

T0 = 1_700_000_000.0


def _center() -> DocNotificationCenter:
    return DocNotificationCenter()


# ---------------------------------------------------------------------------
# subscribe
# ---------------------------------------------------------------------------


def test_subscribe_returns_subscription():
    c = _center()
    sub = c.subscribe("doc.created", lambda n: None)
    assert isinstance(sub, Subscription)


def test_subscribe_stores_topic():
    c = _center()
    sub = c.subscribe("doc.*", lambda n: None)
    assert sub.topic == "doc.*"


def test_subscribe_generates_sub_id():
    c = _center()
    sub = c.subscribe("t", lambda n: None)
    assert sub.sub_id is not None and len(sub.sub_id) > 0


def test_subscribe_custom_sub_id():
    c = _center()
    sub = c.subscribe("t", lambda n: None, sub_id="my-sub")
    assert sub.sub_id == "my-sub"


def test_subscribe_active_by_default():
    c = _center()
    sub = c.subscribe("t", lambda n: None)
    assert sub.active is True


def test_subscribe_increments_total():
    c = _center()
    c.subscribe("a", lambda n: None)
    c.subscribe("b", lambda n: None)
    assert c.total_subscriptions == 2


# ---------------------------------------------------------------------------
# unsubscribe
# ---------------------------------------------------------------------------


def test_unsubscribe_returns_true():
    c = _center()
    sub = c.subscribe("t", lambda n: None)
    assert c.unsubscribe(sub.sub_id) is True


def test_unsubscribe_removes_subscription():
    c = _center()
    sub = c.subscribe("t", lambda n: None)
    c.unsubscribe(sub.sub_id)
    assert c.total_subscriptions == 0


def test_unsubscribe_missing_returns_false():
    c = _center()
    assert c.unsubscribe("no-such") is False


def test_unsubscribe_stops_delivery():
    c = _center()
    received = []
    sub = c.subscribe("t", lambda n: received.append(n))
    c.unsubscribe(sub.sub_id)
    c.publish("t", {}, now=T0)
    assert received == []


# ---------------------------------------------------------------------------
# pause / resume
# ---------------------------------------------------------------------------


def test_pause_returns_true():
    c = _center()
    sub = c.subscribe("t", lambda n: None)
    assert c.pause(sub.sub_id) is True


def test_pause_sets_inactive():
    c = _center()
    sub = c.subscribe("t", lambda n: None)
    c.pause(sub.sub_id)
    subs = c.subscriptions()
    assert not subs[0].active


def test_pause_suppresses_delivery():
    c = _center()
    received = []
    sub = c.subscribe("t", lambda n: received.append(n))
    c.pause(sub.sub_id)
    c.publish("t", {}, now=T0)
    assert received == []


def test_pause_missing_returns_false():
    c = _center()
    assert c.pause("no-such") is False


def test_resume_returns_true():
    c = _center()
    sub = c.subscribe("t", lambda n: None)
    c.pause(sub.sub_id)
    assert c.resume(sub.sub_id) is True


def test_resume_restores_delivery():
    c = _center()
    received = []
    sub = c.subscribe("t", lambda n: received.append(n))
    c.pause(sub.sub_id)
    c.resume(sub.sub_id)
    c.publish("t", {}, now=T0)
    assert len(received) == 1


def test_resume_missing_returns_false():
    c = _center()
    assert c.resume("no-such") is False


# ---------------------------------------------------------------------------
# publish
# ---------------------------------------------------------------------------


def test_publish_returns_notification():
    c = _center()
    n = c.publish("doc.created", {"id": "1"}, now=T0)
    assert isinstance(n, Notification)


def test_publish_notif_id_starts_at_1():
    c = _center()
    n = c.publish("t", {}, now=T0)
    assert n.notif_id == 1


def test_publish_second_notif_id_is_2():
    c = _center()
    c.publish("t", {}, now=T0)
    n2 = c.publish("t", {}, now=T0 + 1)
    assert n2.notif_id == 2


def test_publish_stores_topic():
    c = _center()
    n = c.publish("doc.updated", {}, now=T0)
    assert n.topic == "doc.updated"


def test_publish_stores_payload():
    c = _center()
    n = c.publish("t", {"key": "val"}, now=T0)
    assert n.payload == {"key": "val"}


def test_publish_stores_sender():
    c = _center()
    n = c.publish("t", {}, sender="api", now=T0)
    assert n.sender == "api"


def test_publish_stores_timestamp():
    c = _center()
    n = c.publish("t", {}, now=T0)
    assert n.timestamp == T0


def test_publish_delivers_to_exact_subscriber():
    c = _center()
    received = []
    c.subscribe("doc.created", lambda n: received.append(n))
    c.publish("doc.created", {"id": "1"}, now=T0)
    assert len(received) == 1


def test_publish_does_not_deliver_to_other_topic():
    c = _center()
    received = []
    c.subscribe("doc.deleted", lambda n: received.append(n))
    c.publish("doc.created", {}, now=T0)
    assert received == []


def test_publish_delivers_to_wildcard_pattern():
    c = _center()
    received = []
    c.subscribe("doc.*", lambda n: received.append(n))
    c.publish("doc.created", {}, now=T0)
    c.publish("doc.updated", {}, now=T0 + 1)
    assert len(received) == 2


def test_publish_star_matches_all():
    c = _center()
    received = []
    c.subscribe("*", lambda n: received.append(n))
    c.publish("anything", {}, now=T0)
    assert len(received) == 1


def test_publish_delivers_to_multiple_subscribers():
    c = _center()
    r1, r2 = [], []
    c.subscribe("t", lambda n: r1.append(n))
    c.subscribe("t", lambda n: r2.append(n))
    c.publish("t", {}, now=T0)
    assert len(r1) == 1
    assert len(r2) == 1


# ---------------------------------------------------------------------------
# history
# ---------------------------------------------------------------------------


def test_history_returns_newest_first():
    c = _center()
    c.publish("t", {"n": 1}, now=T0)
    c.publish("t", {"n": 2}, now=T0 + 1)
    h = c.history()
    assert h[0].payload["n"] == 2
    assert h[1].payload["n"] == 1


def test_history_limit():
    c = _center()
    for i in range(10):
        c.publish("t", {"n": i}, now=T0 + i)
    assert len(c.history(limit=3)) == 3


def test_history_topic_filter():
    c = _center()
    c.publish("a", {}, now=T0)
    c.publish("b", {}, now=T0 + 1)
    c.publish("a", {}, now=T0 + 2)
    h = c.history(topic="a")
    assert all(n.topic == "a" for n in h)
    assert len(h) == 2


def test_history_empty_initially():
    c = _center()
    assert c.history() == []


# ---------------------------------------------------------------------------
# clear_history
# ---------------------------------------------------------------------------


def test_clear_history_all():
    c = _center()
    c.publish("t", {}, now=T0)
    c.publish("t", {}, now=T0 + 1)
    count = c.clear_history()
    assert count == 2
    assert c.history() == []


def test_clear_history_by_topic():
    c = _center()
    c.publish("a", {}, now=T0)
    c.publish("b", {}, now=T0 + 1)
    count = c.clear_history(topic="a")
    assert count == 1
    assert len(c.history()) == 1
    assert c.history()[0].topic == "b"


def test_clear_history_missing_topic_returns_zero():
    c = _center()
    c.publish("t", {}, now=T0)
    assert c.clear_history(topic="no-such") == 0


# ---------------------------------------------------------------------------
# subscriptions query
# ---------------------------------------------------------------------------


def test_subscriptions_returns_all():
    c = _center()
    c.subscribe("a", lambda n: None)
    c.subscribe("b", lambda n: None)
    assert len(c.subscriptions()) == 2


def test_subscriptions_topic_filter():
    c = _center()
    c.subscribe("doc.*", lambda n: None)
    c.subscribe("sys.*", lambda n: None)
    result = c.subscriptions(topic="doc.*")
    assert len(result) == 1
    assert result[0].topic == "doc.*"


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------


def test_stats_returns_notif_stats():
    c = _center()
    assert isinstance(c.stats(), NotifStats)


def test_stats_total_published():
    c = _center()
    c.publish("t", {}, now=T0)
    c.publish("t", {}, now=T0 + 1)
    assert c.stats().total_published == 2


def test_stats_total_delivered():
    c = _center()
    c.subscribe("t", lambda n: None)
    c.publish("t", {}, now=T0)
    c.publish("t", {}, now=T0 + 1)
    assert c.stats().total_delivered == 2


def test_stats_topics_seen_sorted():
    c = _center()
    c.publish("z.topic", {}, now=T0)
    c.publish("a.topic", {}, now=T0 + 1)
    topics = c.stats().topics_seen
    assert topics == sorted(topics)
    assert "a.topic" in topics


def test_stats_total_subscriptions():
    c = _center()
    c.subscribe("a", lambda n: None)
    c.subscribe("b", lambda n: None)
    assert c.stats().total_subscriptions == 2


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------


def test_concurrent_publish():
    c = _center()
    received = []
    lock = threading.Lock()
    c.subscribe("t", lambda n: (lock.acquire(), received.append(n), lock.release()))
    errors = []

    def worker():
        try:
            for i in range(10):
                c.publish("t", {"i": i}, now=T0 + i)
        except Exception as exc:
            errors.append(exc)

    threads = [threading.Thread(target=worker) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert not errors
    assert c.stats().total_published == 50
