"""Tests for docstoolkit.doc_subscriber."""
import pytest

from docstoolkit.doc_subscriber import (
    ChangeKind,
    DocChange,
    DocSubscriber,
    Subscription,
    SubscriptionFilter,
)


def make_change(doc_id="d1", kind=ChangeKind.UPDATED, ts=1.0, **details):
    return DocChange(doc_id=doc_id, kind=kind, timestamp=ts, details=dict(details))


class TestChangeKind:
    def test_values_exist(self):
        assert ChangeKind.CREATED
        assert ChangeKind.UPDATED
        assert ChangeKind.DELETED
        assert ChangeKind.TAGGED
        assert ChangeKind.MOVED

    def test_unique(self):
        values = {k.value for k in ChangeKind}
        assert len(values) == 5

    def test_is_enum(self):
        from enum import Enum
        assert issubclass(ChangeKind, Enum)


class TestDocChange:
    def test_create(self):
        c = DocChange(doc_id="x", kind=ChangeKind.CREATED, timestamp=1.0)
        assert c.doc_id == "x"
        assert c.kind == ChangeKind.CREATED
        assert c.timestamp == 1.0
        assert c.details == {}

    def test_details_default_factory(self):
        a = DocChange(doc_id="a", kind=ChangeKind.UPDATED, timestamp=0.0)
        b = DocChange(doc_id="b", kind=ChangeKind.UPDATED, timestamp=0.0)
        a.details["k"] = 1
        assert b.details == {}

    def test_details_passed(self):
        c = DocChange("x", ChangeKind.TAGGED, 1.0, {"tags": ["a"]})
        assert c.details == {"tags": ["a"]}


class TestSubscriptionFilter:
    def test_default(self):
        f = SubscriptionFilter()
        assert f.doc_ids is None
        assert f.kinds is None
        assert f.tags is None
        assert f.min_priority == 0

    def test_with_doc_ids(self):
        f = SubscriptionFilter(doc_ids=["a", "b"])
        assert f.doc_ids == ["a", "b"]

    def test_with_kinds(self):
        f = SubscriptionFilter(kinds=[ChangeKind.CREATED])
        assert f.kinds == [ChangeKind.CREATED]

    def test_with_tags(self):
        f = SubscriptionFilter(tags=["t1"])
        assert f.tags == ["t1"]

    def test_min_priority(self):
        f = SubscriptionFilter(min_priority=5)
        assert f.min_priority == 5


class TestSubscribe:
    def test_returns_sub_id(self):
        s = DocSubscriber()
        sid = s.subscribe("u1", lambda c: None)
        assert isinstance(sid, str)
        assert len(sid) > 0

    def test_unique_sub_ids(self):
        s = DocSubscriber()
        ids = {s.subscribe(f"u{i}", lambda c: None) for i in range(10)}
        assert len(ids) == 10

    def test_subscription_stored(self):
        s = DocSubscriber()
        sid = s.subscribe("u1", lambda c: None)
        assert s.subscription_count == 1

    def test_default_filter(self):
        s = DocSubscriber()
        sid = s.subscribe("u1", lambda c: None)
        subs = s.subscriptions_for("u1")
        assert subs[0].filter.doc_ids is None
        assert subs[0].filter.kinds is None

    def test_with_filter(self):
        s = DocSubscriber()
        f = SubscriptionFilter(doc_ids=["d1"])
        sid = s.subscribe("u1", lambda c: None, filter=f)
        subs = s.subscriptions_for("u1")
        assert subs[0].filter.doc_ids == ["d1"]

    def test_batch_size_stored(self):
        s = DocSubscriber()
        sid = s.subscribe("u1", lambda c: None, batch_size=5)
        subs = s.subscriptions_for("u1")
        assert subs[0].batch_size == 5

    def test_now_stored(self):
        s = DocSubscriber()
        sid = s.subscribe("u1", lambda c: None, now=42.0)
        assert s.subscriptions_for("u1")[0].created_at == 42.0

    def test_invalid_batch_size(self):
        s = DocSubscriber()
        with pytest.raises(ValueError):
            s.subscribe("u1", lambda c: None, batch_size=0)


class TestUnsubscribe:
    def test_existing(self):
        s = DocSubscriber()
        sid = s.subscribe("u1", lambda c: None)
        assert s.unsubscribe(sid) is True
        assert s.subscription_count == 0

    def test_missing(self):
        s = DocSubscriber()
        assert s.unsubscribe("nope") is False

    def test_double_unsubscribe(self):
        s = DocSubscriber()
        sid = s.subscribe("u1", lambda c: None)
        s.unsubscribe(sid)
        assert s.unsubscribe(sid) is False


class TestUnsubscribeAll:
    def test_removes_all_for_subscriber(self):
        s = DocSubscriber()
        s.subscribe("u1", lambda c: None)
        s.subscribe("u1", lambda c: None)
        s.subscribe("u2", lambda c: None)
        n = s.unsubscribe_all("u1")
        assert n == 2
        assert s.subscription_count == 1

    def test_unknown_subscriber(self):
        s = DocSubscriber()
        assert s.unsubscribe_all("ghost") == 0

    def test_only_target_removed(self):
        s = DocSubscriber()
        s.subscribe("u1", lambda c: None)
        s.subscribe("u2", lambda c: None)
        s.unsubscribe_all("u1")
        assert s.subscriber_count == 1


class TestNotifyBasic:
    def test_callback_called(self):
        s = DocSubscriber()
        got = []
        s.subscribe("u1", lambda c: got.append(c))
        change = make_change()
        n = s.notify(change)
        assert n == 1
        assert got == [change]

    def test_no_subscribers(self):
        s = DocSubscriber()
        assert s.notify(make_change()) == 0

    def test_callback_receives_doc_change_instance(self):
        s = DocSubscriber()
        got = []
        s.subscribe("u1", lambda c: got.append(c))
        s.notify(make_change(doc_id="x"))
        assert isinstance(got[0], DocChange)
        assert got[0].doc_id == "x"


class TestNotifyMultipleSubs:
    def test_multiple_called(self):
        s = DocSubscriber()
        calls = []
        s.subscribe("u1", lambda c: calls.append("u1"))
        s.subscribe("u2", lambda c: calls.append("u2"))
        n = s.notify(make_change())
        assert n == 2
        assert sorted(calls) == ["u1", "u2"]

    def test_same_subscriber_multiple_subs(self):
        s = DocSubscriber()
        calls = []
        s.subscribe("u1", lambda c: calls.append("a"))
        s.subscribe("u1", lambda c: calls.append("b"))
        s.notify(make_change())
        assert sorted(calls) == ["a", "b"]


class TestNotifyBatchInput:
    def test_multiple_changes(self):
        s = DocSubscriber()
        got = []
        s.subscribe("u1", lambda c: got.append(c))
        changes = [make_change(doc_id=f"d{i}") for i in range(3)]
        n = s.notify_batch(changes)
        assert n == 3
        assert len(got) == 3

    def test_empty_list(self):
        s = DocSubscriber()
        assert s.notify_batch([]) == 0

    def test_multiple_subs_batch_input(self):
        s = DocSubscriber()
        a, b = [], []
        s.subscribe("u1", lambda c: a.append(c))
        s.subscribe("u2", lambda c: b.append(c))
        s.notify_batch([make_change(), make_change()])
        assert len(a) == 2 and len(b) == 2


class TestFilterByDocId:
    def test_match(self):
        s = DocSubscriber()
        got = []
        s.subscribe("u1", lambda c: got.append(c),
                    filter=SubscriptionFilter(doc_ids=["d1"]))
        s.notify(make_change(doc_id="d1"))
        assert len(got) == 1

    def test_no_match(self):
        s = DocSubscriber()
        got = []
        s.subscribe("u1", lambda c: got.append(c),
                    filter=SubscriptionFilter(doc_ids=["d1"]))
        s.notify(make_change(doc_id="d2"))
        assert got == []

    def test_none_matches_all(self):
        s = DocSubscriber()
        got = []
        s.subscribe("u1", lambda c: got.append(c),
                    filter=SubscriptionFilter(doc_ids=None))
        s.notify(make_change(doc_id="any"))
        assert len(got) == 1

    def test_multiple_doc_ids(self):
        s = DocSubscriber()
        got = []
        s.subscribe("u1", lambda c: got.append(c),
                    filter=SubscriptionFilter(doc_ids=["a", "b"]))
        s.notify(make_change(doc_id="a"))
        s.notify(make_change(doc_id="b"))
        s.notify(make_change(doc_id="c"))
        assert len(got) == 2


class TestFilterByKind:
    def test_match(self):
        s = DocSubscriber()
        got = []
        s.subscribe("u1", lambda c: got.append(c),
                    filter=SubscriptionFilter(kinds=[ChangeKind.CREATED]))
        s.notify(make_change(kind=ChangeKind.CREATED))
        assert len(got) == 1

    def test_no_match(self):
        s = DocSubscriber()
        got = []
        s.subscribe("u1", lambda c: got.append(c),
                    filter=SubscriptionFilter(kinds=[ChangeKind.CREATED]))
        s.notify(make_change(kind=ChangeKind.DELETED))
        assert got == []

    def test_none_matches_all(self):
        s = DocSubscriber()
        got = []
        s.subscribe("u1", lambda c: got.append(c),
                    filter=SubscriptionFilter(kinds=None))
        s.notify(make_change(kind=ChangeKind.MOVED))
        assert len(got) == 1

    def test_multiple_kinds(self):
        s = DocSubscriber()
        got = []
        s.subscribe("u1", lambda c: got.append(c),
                    filter=SubscriptionFilter(
                        kinds=[ChangeKind.CREATED, ChangeKind.DELETED]))
        s.notify(make_change(kind=ChangeKind.CREATED))
        s.notify(make_change(kind=ChangeKind.UPDATED))
        s.notify(make_change(kind=ChangeKind.DELETED))
        assert len(got) == 2


class TestFilterByTags:
    def test_match_any(self):
        s = DocSubscriber()
        got = []
        s.subscribe("u1", lambda c: got.append(c),
                    filter=SubscriptionFilter(tags=["t1"]))
        s.notify(make_change(tags=["t1", "t2"]))
        assert len(got) == 1

    def test_no_overlap(self):
        s = DocSubscriber()
        got = []
        s.subscribe("u1", lambda c: got.append(c),
                    filter=SubscriptionFilter(tags=["t1"]))
        s.notify(make_change(tags=["t2"]))
        assert got == []

    def test_no_tags_in_details(self):
        s = DocSubscriber()
        got = []
        s.subscribe("u1", lambda c: got.append(c),
                    filter=SubscriptionFilter(tags=["t1"]))
        s.notify(make_change())  # no tags
        assert got == []

    def test_tags_none_ignored(self):
        s = DocSubscriber()
        got = []
        s.subscribe("u1", lambda c: got.append(c),
                    filter=SubscriptionFilter(tags=None))
        s.notify(make_change(tags=["anything"]))
        assert len(got) == 1


class TestBatchSize:
    def test_single_delivered_immediately(self):
        s = DocSubscriber()
        got = []
        s.subscribe("u1", lambda c: got.append(c), batch_size=1)
        s.notify(make_change())
        assert len(got) == 1

    def test_buffers_until_full(self):
        s = DocSubscriber()
        got = []
        s.subscribe("u1", lambda batch: got.append(batch), batch_size=3)
        s.notify(make_change(doc_id="a"))
        s.notify(make_change(doc_id="b"))
        assert got == []
        s.notify(make_change(doc_id="c"))
        assert len(got) == 1
        assert isinstance(got[0], list)
        assert len(got[0]) == 3

    def test_buffer_resets_after_delivery(self):
        s = DocSubscriber()
        got = []
        sid = s.subscribe("u1", lambda b: got.append(b), batch_size=2)
        s.notify(make_change())
        s.notify(make_change())  # triggers
        assert s.pending_count(sid) == 0
        s.notify(make_change())
        assert s.pending_count(sid) == 1

    def test_batch_callback_receives_list(self):
        s = DocSubscriber()
        captured = []
        s.subscribe("u1", lambda b: captured.append(b), batch_size=2)
        s.notify(make_change(doc_id="x"))
        s.notify(make_change(doc_id="y"))
        assert isinstance(captured[0], list)
        assert [c.doc_id for c in captured[0]] == ["x", "y"]


class TestFlush:
    def test_flush_single_sub(self):
        s = DocSubscriber()
        got = []
        sid = s.subscribe("u1", lambda b: got.append(b), batch_size=10)
        s.notify(make_change())
        s.notify(make_change())
        n = s.flush(sid)
        assert n == 2
        assert len(got) == 1 and len(got[0]) == 2

    def test_flush_all(self):
        s = DocSubscriber()
        got = []
        s.subscribe("u1", lambda b: got.append(("u1", b)), batch_size=5)
        s.subscribe("u2", lambda b: got.append(("u2", b)), batch_size=5)
        s.notify(make_change())
        n = s.flush()
        assert n == 2  # one buffered change for each sub
        assert len(got) == 2

    def test_flush_empty_buffer(self):
        s = DocSubscriber()
        got = []
        sid = s.subscribe("u1", lambda b: got.append(b), batch_size=5)
        n = s.flush(sid)
        assert n == 0
        assert got == []

    def test_flush_unknown_id(self):
        s = DocSubscriber()
        assert s.flush("nope") == 0

    def test_flush_clears_buffer(self):
        s = DocSubscriber()
        sid = s.subscribe("u1", lambda b: None, batch_size=5)
        s.notify(make_change())
        s.flush(sid)
        assert s.pending_count(sid) == 0


class TestMatchesFilter:
    def test_empty_filter_matches(self):
        c = make_change()
        assert DocSubscriber.matches_filter(c, SubscriptionFilter()) is True

    def test_doc_id_mismatch(self):
        c = make_change(doc_id="a")
        f = SubscriptionFilter(doc_ids=["b"])
        assert DocSubscriber.matches_filter(c, f) is False

    def test_kind_mismatch(self):
        c = make_change(kind=ChangeKind.CREATED)
        f = SubscriptionFilter(kinds=[ChangeKind.DELETED])
        assert DocSubscriber.matches_filter(c, f) is False

    def test_priority_below_min(self):
        c = make_change(priority=1)
        f = SubscriptionFilter(min_priority=5)
        assert DocSubscriber.matches_filter(c, f) is False

    def test_priority_meets_min(self):
        c = make_change(priority=5)
        f = SubscriptionFilter(min_priority=5)
        assert DocSubscriber.matches_filter(c, f) is True

    def test_priority_default_zero(self):
        c = make_change()  # no priority => 0
        f = SubscriptionFilter(min_priority=0)
        assert DocSubscriber.matches_filter(c, f) is True


class TestSubscriptionsFor:
    def test_returns_list(self):
        s = DocSubscriber()
        s.subscribe("u1", lambda c: None)
        result = s.subscriptions_for("u1")
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Subscription)

    def test_no_subscriptions(self):
        s = DocSubscriber()
        assert s.subscriptions_for("ghost") == []

    def test_only_target_subscriber(self):
        s = DocSubscriber()
        s.subscribe("u1", lambda c: None)
        s.subscribe("u2", lambda c: None)
        assert len(s.subscriptions_for("u1")) == 1


class TestSubscriptionCount:
    def test_zero(self):
        assert DocSubscriber().subscription_count == 0

    def test_grows(self):
        s = DocSubscriber()
        for i in range(5):
            s.subscribe(f"u{i}", lambda c: None)
        assert s.subscription_count == 5

    def test_decreases_on_unsubscribe(self):
        s = DocSubscriber()
        sid = s.subscribe("u1", lambda c: None)
        s.unsubscribe(sid)
        assert s.subscription_count == 0


class TestSubscriberCount:
    def test_zero(self):
        assert DocSubscriber().subscriber_count == 0

    def test_distinct(self):
        s = DocSubscriber()
        s.subscribe("u1", lambda c: None)
        s.subscribe("u1", lambda c: None)
        s.subscribe("u2", lambda c: None)
        assert s.subscriber_count == 2

    def test_after_unsubscribe_all(self):
        s = DocSubscriber()
        s.subscribe("u1", lambda c: None)
        s.unsubscribe_all("u1")
        assert s.subscriber_count == 0


class TestClear:
    def test_clears_all(self):
        s = DocSubscriber()
        s.subscribe("u1", lambda c: None)
        s.subscribe("u2", lambda c: None)
        s.clear()
        assert s.subscription_count == 0
        assert s.subscriber_count == 0

    def test_clear_empty(self):
        s = DocSubscriber()
        s.clear()
        assert s.subscription_count == 0

    def test_clear_then_subscribe(self):
        s = DocSubscriber()
        s.subscribe("u1", lambda c: None)
        s.clear()
        s.subscribe("u2", lambda c: None)
        assert s.subscription_count == 1


class TestPendingCount:
    def test_initial_zero(self):
        s = DocSubscriber()
        sid = s.subscribe("u1", lambda c: None, batch_size=5)
        assert s.pending_count(sid) == 0

    def test_grows_with_buffered(self):
        s = DocSubscriber()
        sid = s.subscribe("u1", lambda b: None, batch_size=10)
        s.notify(make_change())
        s.notify(make_change())
        assert s.pending_count(sid) == 2

    def test_unknown_sub_id(self):
        s = DocSubscriber()
        assert s.pending_count("nope") == 0

    def test_resets_when_batch_delivered(self):
        s = DocSubscriber()
        sid = s.subscribe("u1", lambda b: None, batch_size=2)
        s.notify(make_change())
        s.notify(make_change())
        assert s.pending_count(sid) == 0


class TestEdgeCases:
    def test_callback_exception_does_not_break(self):
        s = DocSubscriber()
        good = []

        def bad(c):
            raise RuntimeError("boom")

        s.subscribe("u1", bad)
        s.subscribe("u2", lambda c: good.append(c))
        # should not raise
        n = s.notify(make_change())
        assert n == 2
        assert len(good) == 1

    def test_notify_with_no_subscribers(self):
        s = DocSubscriber()
        assert s.notify(make_change()) == 0

    def test_filter_combination(self):
        s = DocSubscriber()
        got = []
        f = SubscriptionFilter(
            doc_ids=["d1"],
            kinds=[ChangeKind.UPDATED],
            tags=["t1"],
            min_priority=5,
        )
        s.subscribe("u1", lambda c: got.append(c), filter=f)
        # all match
        s.notify(make_change(doc_id="d1", kind=ChangeKind.UPDATED,
                             tags=["t1"], priority=10))
        # doc_id wrong
        s.notify(make_change(doc_id="d2", kind=ChangeKind.UPDATED,
                             tags=["t1"], priority=10))
        # priority too low
        s.notify(make_change(doc_id="d1", kind=ChangeKind.UPDATED,
                             tags=["t1"], priority=1))
        assert len(got) == 1

    def test_batch_callback_exception(self):
        s = DocSubscriber()

        def bad(b):
            raise RuntimeError("boom")

        sid = s.subscribe("u1", bad, batch_size=2)
        s.notify(make_change())
        # should not raise on delivery
        s.notify(make_change())
        assert s.pending_count(sid) == 0

    def test_flush_callback_exception(self):
        s = DocSubscriber()

        def bad(b):
            raise RuntimeError("boom")

        sid = s.subscribe("u1", bad, batch_size=10)
        s.notify(make_change())
        # should not raise
        n = s.flush(sid)
        assert n == 1
