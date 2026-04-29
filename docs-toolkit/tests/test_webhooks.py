"""Тесты webhook dispatcher."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.webhooks import (
    WebhookDispatcher, Subscription, Delivery, DeliveryStatus,
    sign_payload,
)


@pytest.fixture
def fake_http():
    """Mock http_send: tracks calls + ответ зависит от URL."""
    calls = []

    def send(url, payload, headers, timeout=10):
        calls.append({"url": url, "payload": payload, "headers": dict(headers)})
        if "fail500" in url:
            return 500, "Server Error"
        if "fail404" in url:
            return 404, "Not Found"
        if "neterror" in url:
            raise ConnectionError("network down")
        return 200, '{"ok":true}'

    send.calls = calls
    return send


@pytest.fixture
def wh(tmp_path, fake_http):
    d = WebhookDispatcher(db_path=tmp_path / "wh.sqlite", http_send=fake_http,
                           max_retries=3)
    yield d
    d.close()


# ---- sign ----

def test_sign_payload_empty_secret():
    assert sign_payload({"x": 1}, "") == ""


def test_sign_payload_deterministic():
    s1 = sign_payload({"x": 1, "y": 2}, "key")
    s2 = sign_payload({"y": 2, "x": 1}, "key")  # different order
    assert s1 == s2  # sort_keys ensures stability


def test_sign_payload_changes_with_secret():
    s1 = sign_payload({"x": 1}, "key1")
    s2 = sign_payload({"x": 1}, "key2")
    assert s1 != s2


# ---- subscription ----

def test_subscription_auto_id_ts():
    s = Subscription(url="http://x")
    assert s.id and len(s.id) == 12
    assert s.created_ts


def test_subscription_matches_wildcard():
    s = Subscription(url="x", events=["*"])
    assert s.matches("any.event")
    assert s.matches("foo")


def test_subscription_matches_exact():
    s = Subscription(url="x", events=["job.done"])
    assert s.matches("job.done")
    assert not s.matches("job.failed")


def test_subscription_matches_prefix():
    s = Subscription(url="x", events=["job.*"])
    assert s.matches("job.done")
    assert s.matches("job.failed")
    assert not s.matches("user.login")


def test_subscription_matches_multiple_patterns():
    s = Subscription(url="x", events=["job.*", "feedback.received"])
    assert s.matches("job.done")
    assert s.matches("feedback.received")
    assert not s.matches("user.login")


# ---- subscribe / unsubscribe ----

def test_subscribe_persists(wh):
    sid = wh.subscribe(Subscription(url="http://a", events=["x"]))
    assert sid
    subs = wh.list_subscriptions()
    assert len(subs) == 1
    assert subs[0].url == "http://a"


def test_unsubscribe(wh):
    sid = wh.subscribe(Subscription(url="http://a"))
    wh.unsubscribe(sid)
    assert wh.list_subscriptions() == []


def test_list_subscriptions_active_only(wh):
    sid_active = wh.subscribe(Subscription(url="http://a", active=True))
    sid_inactive = wh.subscribe(Subscription(url="http://b", active=False))
    active = wh.list_subscriptions(active_only=True)
    assert len(active) == 1
    all_ = wh.list_subscriptions(active_only=False)
    assert len(all_) == 2


def test_matching_subscriptions(wh):
    wh.subscribe(Subscription(url="http://a", events=["job.*"]))
    wh.subscribe(Subscription(url="http://b", events=["feedback.received"]))
    wh.subscribe(Subscription(url="http://c", events=["*"]))
    matched = wh.matching_subscriptions("job.completed")
    urls = {s.url for s in matched}
    assert "http://a" in urls
    assert "http://c" in urls
    assert "http://b" not in urls


# ---- dispatch ----

def test_dispatch_success(wh, fake_http):
    wh.subscribe(Subscription(url="http://hooks.example.com/ok",
                               events=["job.done"]))
    deliveries = wh.dispatch(event="job.done", payload={"id": "1"})
    assert len(deliveries) == 1
    assert deliveries[0].status == DeliveryStatus.SENT
    assert deliveries[0].response_code == 200
    assert deliveries[0].sent_ts


def test_dispatch_with_signature(wh, fake_http):
    wh.subscribe(Subscription(url="http://hooks/ok", events=["*"],
                               secret="topsecret"))
    wh.dispatch(event="x.y", payload={"k": "v"})
    last_call = fake_http.calls[-1]
    assert "X-Lorenzo-Signature" in last_call["headers"]
    expected = sign_payload({"k": "v"}, "topsecret")
    assert last_call["headers"]["X-Lorenzo-Signature"] == expected


def test_dispatch_failed_500(wh):
    wh.subscribe(Subscription(url="http://hooks/fail500", events=["*"]))
    deliveries = wh.dispatch(event="x", payload={})
    assert deliveries[0].status == DeliveryStatus.FAILED
    assert "500" in deliveries[0].last_error


def test_dispatch_failed_network(wh):
    wh.subscribe(Subscription(url="http://hooks/neterror", events=["*"]))
    deliveries = wh.dispatch(event="x", payload={})
    assert deliveries[0].status == DeliveryStatus.FAILED
    assert "network" in deliveries[0].last_error.lower() or \
           "ConnectionError" in deliveries[0].last_error


def test_dispatch_no_matching_subscriptions(wh):
    wh.subscribe(Subscription(url="http://x", events=["other.event"]))
    deliveries = wh.dispatch(event="job.done", payload={})
    assert deliveries == []


def test_dispatch_includes_meta_headers(wh, fake_http):
    wh.subscribe(Subscription(url="http://hooks/ok", events=["*"]))
    wh.dispatch(event="my.event", payload={})
    h = fake_http.calls[-1]["headers"]
    assert h["Content-Type"] == "application/json"
    assert h["X-Lorenzo-Event"] == "my.event"
    assert "X-Lorenzo-Delivery-Id" in h


# ---- retry ----

def test_retry_failed_eventually_marks_dead(wh):
    wh.subscribe(Subscription(url="http://hooks/fail500", events=["*"]))
    wh.dispatch(event="x", payload={})  # attempt 1 → failed
    wh.retry_failed()                     # attempt 2 → failed
    wh.retry_failed()                     # attempt 3 → dead (max_retries=3)
    dead = wh.list_deliveries(status=DeliveryStatus.DEAD)
    assert len(dead) == 1
    assert dead[0].attempts == 3


def test_retry_failed_skips_dead(wh):
    wh.subscribe(Subscription(url="http://hooks/fail500", events=["*"]))
    wh.dispatch(event="x", payload={})
    wh.retry_failed()
    wh.retry_failed()  # now dead
    n = wh.retry_failed()  # nothing to retry
    assert n == 0


def test_list_deliveries_filter_by_status(wh):
    wh.subscribe(Subscription(url="http://hooks/ok", events=["*"]))
    wh.subscribe(Subscription(url="http://hooks/fail500", events=["*"]))
    wh.dispatch(event="x", payload={})
    sent = wh.list_deliveries(status=DeliveryStatus.SENT)
    failed = wh.list_deliveries(status=DeliveryStatus.FAILED)
    assert len(sent) == 1
    assert len(failed) == 1


def test_stats(wh):
    wh.subscribe(Subscription(url="http://hooks/ok", events=["*"]))
    wh.dispatch(event="x", payload={})
    s = wh.stats()
    assert s["subscriptions"] == 1
    assert s["active_subscriptions"] == 1
    assert s["deliveries_sent"] == 1
