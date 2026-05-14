"""Tests for docstoolkit.doc_distribution."""
from __future__ import annotations

import pytest

from docstoolkit.doc_distribution import (
    Channel,
    ChannelType,
    Delivery,
    DeliveryStatus,
    DistributionStats,
    DocDistribution,
)


# ---------------- enums ----------------


class TestChannelType:
    def test_members(self):
        assert ChannelType.EMAIL.value == "email"
        assert ChannelType.RSS.value == "rss"
        assert ChannelType.WEBHOOK.value == "webhook"
        assert ChannelType.IN_APP.value == "in_app"
        assert ChannelType.SLACK.value == "slack"
        assert ChannelType.DIGEST.value == "digest"

    def test_count(self):
        assert len(list(ChannelType)) == 6


class TestDeliveryStatus:
    def test_members(self):
        assert DeliveryStatus.QUEUED.value == "queued"
        assert DeliveryStatus.IN_FLIGHT.value == "in_flight"
        assert DeliveryStatus.DELIVERED.value == "delivered"
        assert DeliveryStatus.FAILED.value == "failed"

    def test_count(self):
        assert len(list(DeliveryStatus)) == 4


# ---------------- dataclasses ----------------


class TestChannel:
    def test_default_construction(self):
        ch = Channel(
            channel_id="c1",
            channel_type=ChannelType.EMAIL,
            name="newsletter",
            endpoint="news@example.com",
        )
        assert ch.enabled is True
        assert ch.subscribers == set()
        assert ch.metadata == {}

    def test_custom_fields(self):
        ch = Channel(
            channel_id="c2",
            channel_type=ChannelType.SLACK,
            name="team",
            endpoint="https://hooks.slack.com/x",
            enabled=False,
            subscribers={"alice"},
            metadata={"region": "eu"},
        )
        assert ch.enabled is False
        assert "alice" in ch.subscribers
        assert ch.metadata["region"] == "eu"


class TestDelivery:
    def test_default_fields(self):
        d = Delivery(
            delivery_id=1,
            channel_id="c1",
            doc_id="d1",
            recipient="alice",
            status=DeliveryStatus.QUEUED,
        )
        assert d.attempts == 0
        assert d.queued_at == 0.0
        assert d.delivered_at is None
        assert d.last_error is None


class TestDistributionStats:
    def test_delivery_rate_zero(self):
        s = DistributionStats(0, 0, 0, 0, 0, 0)
        assert s.delivery_rate == 0.0

    def test_delivery_rate_nonzero(self):
        s = DistributionStats(1, 5, 10, 7, 2, 1)
        assert s.delivery_rate == 0.7

    def test_delivery_rate_full(self):
        s = DistributionStats(1, 2, 4, 4, 0, 0)
        assert s.delivery_rate == 1.0


# ---------------- channel management ----------------


class TestAddChannel:
    def test_add_returns_channel(self):
        dd = DocDistribution()
        ch = dd.add_channel(ChannelType.EMAIL, "n1", "a@b.c")
        assert isinstance(ch, Channel)
        assert ch.name == "n1"
        assert ch.endpoint == "a@b.c"
        assert ch.channel_type == ChannelType.EMAIL
        assert ch.enabled is True

    def test_channel_id_unique(self):
        dd = DocDistribution()
        c1 = dd.add_channel(ChannelType.EMAIL, "n1", "x")
        c2 = dd.add_channel(ChannelType.EMAIL, "n2", "y")
        assert c1.channel_id != c2.channel_id

    def test_metadata_default(self):
        dd = DocDistribution()
        ch = dd.add_channel(ChannelType.RSS, "feed", "/rss.xml")
        assert ch.metadata == {}

    def test_metadata_custom(self):
        dd = DocDistribution()
        ch = dd.add_channel(ChannelType.WEBHOOK, "wh", "http://x", metadata={"k": "v"})
        assert ch.metadata == {"k": "v"}

    def test_total_increments(self):
        dd = DocDistribution()
        dd.add_channel(ChannelType.EMAIL, "n", "a")
        dd.add_channel(ChannelType.RSS, "n", "a")
        assert dd.total_channels == 2


class TestRemoveChannel:
    def test_remove_existing(self):
        dd = DocDistribution()
        ch = dd.add_channel(ChannelType.EMAIL, "n", "a")
        assert dd.remove_channel(ch.channel_id) is True
        assert dd.total_channels == 0

    def test_remove_missing(self):
        dd = DocDistribution()
        assert dd.remove_channel("missing") is False


class TestEnableDisableChannel:
    def test_disable(self):
        dd = DocDistribution()
        ch = dd.add_channel(ChannelType.EMAIL, "n", "a")
        assert dd.disable_channel(ch.channel_id) is True
        assert dd._channels[ch.channel_id].enabled is False

    def test_enable(self):
        dd = DocDistribution()
        ch = dd.add_channel(ChannelType.EMAIL, "n", "a")
        dd.disable_channel(ch.channel_id)
        assert dd.enable_channel(ch.channel_id) is True
        assert dd._channels[ch.channel_id].enabled is True

    def test_disable_missing(self):
        dd = DocDistribution()
        assert dd.disable_channel("missing") is False

    def test_enable_missing(self):
        dd = DocDistribution()
        assert dd.enable_channel("missing") is False


# ---------------- subscriptions ----------------


class TestSubscribe:
    def test_subscribe_new(self):
        dd = DocDistribution()
        ch = dd.add_channel(ChannelType.EMAIL, "n", "a")
        assert dd.subscribe(ch.channel_id, "alice") is True
        assert "alice" in dd._channels[ch.channel_id].subscribers

    def test_subscribe_duplicate(self):
        dd = DocDistribution()
        ch = dd.add_channel(ChannelType.EMAIL, "n", "a")
        dd.subscribe(ch.channel_id, "alice")
        assert dd.subscribe(ch.channel_id, "alice") is False

    def test_subscribe_missing_channel(self):
        dd = DocDistribution()
        assert dd.subscribe("missing", "alice") is False


class TestUnsubscribe:
    def test_unsubscribe_existing(self):
        dd = DocDistribution()
        ch = dd.add_channel(ChannelType.EMAIL, "n", "a")
        dd.subscribe(ch.channel_id, "alice")
        assert dd.unsubscribe(ch.channel_id, "alice") is True

    def test_unsubscribe_not_present(self):
        dd = DocDistribution()
        ch = dd.add_channel(ChannelType.EMAIL, "n", "a")
        assert dd.unsubscribe(ch.channel_id, "alice") is False

    def test_unsubscribe_missing_channel(self):
        dd = DocDistribution()
        assert dd.unsubscribe("missing", "alice") is False


# ---------------- distribute ----------------


class TestDistribute:
    def test_distribute_all_channels(self):
        dd = DocDistribution()
        c1 = dd.add_channel(ChannelType.EMAIL, "n1", "a")
        c2 = dd.add_channel(ChannelType.RSS, "n2", "b")
        dd.subscribe(c1.channel_id, "alice")
        dd.subscribe(c2.channel_id, "bob")
        deliveries = dd.distribute("doc1", now=10.0)
        assert len(deliveries) == 2
        recipients = {d.recipient for d in deliveries}
        assert recipients == {"alice", "bob"}

    def test_distribute_no_subscribers(self):
        dd = DocDistribution()
        dd.add_channel(ChannelType.EMAIL, "n", "a")
        assert dd.distribute("doc1") == []

    def test_distribute_queued_status(self):
        dd = DocDistribution()
        ch = dd.add_channel(ChannelType.EMAIL, "n", "a")
        dd.subscribe(ch.channel_id, "alice")
        d = dd.distribute("doc1", now=5.0)[0]
        assert d.status == DeliveryStatus.QUEUED
        assert d.queued_at == 5.0
        assert d.attempts == 0

    def test_distribute_skips_disabled(self):
        dd = DocDistribution()
        c1 = dd.add_channel(ChannelType.EMAIL, "n1", "a")
        c2 = dd.add_channel(ChannelType.RSS, "n2", "b")
        dd.subscribe(c1.channel_id, "alice")
        dd.subscribe(c2.channel_id, "bob")
        dd.disable_channel(c2.channel_id)
        result = dd.distribute("d1")
        assert len(result) == 1
        assert result[0].recipient == "alice"

    def test_distribute_assigns_ids(self):
        dd = DocDistribution()
        ch = dd.add_channel(ChannelType.EMAIL, "n", "a")
        dd.subscribe(ch.channel_id, "a")
        dd.subscribe(ch.channel_id, "b")
        ds = dd.distribute("d1")
        ids = sorted(d.delivery_id for d in ds)
        assert ids == [1, 2]


class TestDistributeWithFilter:
    def test_filter_includes_only_listed(self):
        dd = DocDistribution()
        ch = dd.add_channel(ChannelType.EMAIL, "n", "a")
        dd.subscribe(ch.channel_id, "alice")
        dd.subscribe(ch.channel_id, "bob")
        result = dd.distribute("d1", recipients_filter={"alice"})
        assert len(result) == 1
        assert result[0].recipient == "alice"

    def test_filter_empty_set(self):
        dd = DocDistribution()
        ch = dd.add_channel(ChannelType.EMAIL, "n", "a")
        dd.subscribe(ch.channel_id, "alice")
        assert dd.distribute("d1", recipients_filter=set()) == []


class TestDistributeSelectChannels:
    def test_select_specific(self):
        dd = DocDistribution()
        c1 = dd.add_channel(ChannelType.EMAIL, "n1", "a")
        c2 = dd.add_channel(ChannelType.RSS, "n2", "b")
        dd.subscribe(c1.channel_id, "alice")
        dd.subscribe(c2.channel_id, "bob")
        result = dd.distribute("d1", channel_ids=[c1.channel_id])
        assert len(result) == 1
        assert result[0].recipient == "alice"

    def test_select_missing(self):
        dd = DocDistribution()
        assert dd.distribute("d1", channel_ids=["nope"]) == []

    def test_select_disabled_excluded(self):
        dd = DocDistribution()
        c1 = dd.add_channel(ChannelType.EMAIL, "n", "a")
        dd.subscribe(c1.channel_id, "alice")
        dd.disable_channel(c1.channel_id)
        assert dd.distribute("d1", channel_ids=[c1.channel_id]) == []


# ---------------- delivery state ----------------


class TestMarkDelivered:
    def test_mark_delivered(self):
        dd = DocDistribution()
        ch = dd.add_channel(ChannelType.EMAIL, "n", "a")
        dd.subscribe(ch.channel_id, "alice")
        d = dd.distribute("doc1")[0]
        assert dd.mark_delivered(d.delivery_id, now=12.5) is True
        updated = dd._deliveries[d.delivery_id]
        assert updated.status == DeliveryStatus.DELIVERED
        assert updated.attempts == 1
        assert updated.delivered_at == 12.5

    def test_mark_delivered_missing(self):
        dd = DocDistribution()
        assert dd.mark_delivered(999) is False


class TestMarkFailed:
    def test_mark_failed_with_error(self):
        dd = DocDistribution()
        ch = dd.add_channel(ChannelType.EMAIL, "n", "a")
        dd.subscribe(ch.channel_id, "alice")
        d = dd.distribute("doc1")[0]
        assert dd.mark_failed(d.delivery_id, error="smtp down") is True
        upd = dd._deliveries[d.delivery_id]
        assert upd.status == DeliveryStatus.FAILED
        assert upd.attempts == 1
        assert upd.last_error == "smtp down"

    def test_mark_failed_missing(self):
        dd = DocDistribution()
        assert dd.mark_failed(999) is False

    def test_mark_failed_no_error_arg(self):
        dd = DocDistribution()
        ch = dd.add_channel(ChannelType.EMAIL, "n", "a")
        dd.subscribe(ch.channel_id, "a")
        d = dd.distribute("d1")[0]
        assert dd.mark_failed(d.delivery_id) is True
        assert dd._deliveries[d.delivery_id].last_error is None


class TestRetryFailed:
    def test_retry_resets_status(self):
        dd = DocDistribution()
        ch = dd.add_channel(ChannelType.EMAIL, "n", "a")
        dd.subscribe(ch.channel_id, "alice")
        d = dd.distribute("d1")[0]
        dd.mark_failed(d.delivery_id, error="oops")
        assert dd.retry_failed(d.delivery_id, now=20.0) is True
        upd = dd._deliveries[d.delivery_id]
        assert upd.status == DeliveryStatus.QUEUED
        assert upd.queued_at == 20.0
        assert upd.last_error is None

    def test_retry_not_failed(self):
        dd = DocDistribution()
        ch = dd.add_channel(ChannelType.EMAIL, "n", "a")
        dd.subscribe(ch.channel_id, "alice")
        d = dd.distribute("d1")[0]
        assert dd.retry_failed(d.delivery_id) is False

    def test_retry_missing(self):
        dd = DocDistribution()
        assert dd.retry_failed(999) is False


# ---------------- queries ----------------


class TestPendingDeliveries:
    def test_pending_includes_queued(self):
        dd = DocDistribution()
        ch = dd.add_channel(ChannelType.EMAIL, "n", "a")
        dd.subscribe(ch.channel_id, "alice")
        dd.distribute("d1")
        assert len(dd.pending_deliveries()) == 1

    def test_pending_excludes_delivered(self):
        dd = DocDistribution()
        ch = dd.add_channel(ChannelType.EMAIL, "n", "a")
        dd.subscribe(ch.channel_id, "alice")
        d = dd.distribute("d1")[0]
        dd.mark_delivered(d.delivery_id)
        assert dd.pending_deliveries() == []


class TestFailedDeliveries:
    def test_failed_list(self):
        dd = DocDistribution()
        ch = dd.add_channel(ChannelType.EMAIL, "n", "a")
        dd.subscribe(ch.channel_id, "alice")
        dd.subscribe(ch.channel_id, "bob")
        ds = dd.distribute("d1")
        dd.mark_failed(ds[0].delivery_id)
        failed = dd.failed_deliveries()
        assert len(failed) == 1
        assert failed[0].delivery_id == ds[0].delivery_id


class TestDeliveriesForDoc:
    def test_filter_by_doc(self):
        dd = DocDistribution()
        ch = dd.add_channel(ChannelType.EMAIL, "n", "a")
        dd.subscribe(ch.channel_id, "alice")
        dd.distribute("doc1")
        dd.distribute("doc2")
        assert len(dd.deliveries_for_doc("doc1")) == 1
        assert len(dd.deliveries_for_doc("doc2")) == 1
        assert dd.deliveries_for_doc("nope") == []


class TestDeliveriesForRecipient:
    def test_filter_by_recipient(self):
        dd = DocDistribution()
        ch = dd.add_channel(ChannelType.EMAIL, "n", "a")
        dd.subscribe(ch.channel_id, "alice")
        dd.subscribe(ch.channel_id, "bob")
        dd.distribute("d1")
        assert len(dd.deliveries_for_recipient("alice")) == 1
        assert len(dd.deliveries_for_recipient("bob")) == 1
        assert dd.deliveries_for_recipient("nobody") == []


class TestChannelsForRecipient:
    def test_finds_subscribed_channels(self):
        dd = DocDistribution()
        c1 = dd.add_channel(ChannelType.EMAIL, "n1", "a")
        c2 = dd.add_channel(ChannelType.RSS, "n2", "b")
        c3 = dd.add_channel(ChannelType.SLACK, "n3", "c")
        dd.subscribe(c1.channel_id, "alice")
        dd.subscribe(c3.channel_id, "alice")
        chs = dd.channels_for_recipient("alice")
        ids = {c.channel_id for c in chs}
        assert ids == {c1.channel_id, c3.channel_id}

    def test_none(self):
        dd = DocDistribution()
        dd.add_channel(ChannelType.EMAIL, "n", "a")
        assert dd.channels_for_recipient("ghost") == []


class TestChannelsByType:
    def test_filter_email(self):
        dd = DocDistribution()
        dd.add_channel(ChannelType.EMAIL, "n1", "a")
        dd.add_channel(ChannelType.EMAIL, "n2", "b")
        dd.add_channel(ChannelType.RSS, "n3", "c")
        assert len(dd.channels_by_type(ChannelType.EMAIL)) == 2

    def test_filter_none(self):
        dd = DocDistribution()
        assert dd.channels_by_type(ChannelType.DIGEST) == []


class TestSubscriberCount:
    def test_count(self):
        dd = DocDistribution()
        ch = dd.add_channel(ChannelType.EMAIL, "n", "a")
        dd.subscribe(ch.channel_id, "alice")
        dd.subscribe(ch.channel_id, "bob")
        assert dd.subscriber_count(ch.channel_id) == 2

    def test_count_missing(self):
        dd = DocDistribution()
        assert dd.subscriber_count("missing") == 0


# ---------------- stats ----------------


class TestStats:
    def test_empty(self):
        s = DocDistribution().stats()
        assert s.total_channels == 0
        assert s.total_subscribers == 0
        assert s.total_deliveries == 0
        assert s.delivery_rate == 0.0

    def test_after_operations(self):
        dd = DocDistribution()
        c1 = dd.add_channel(ChannelType.EMAIL, "n1", "a")
        c2 = dd.add_channel(ChannelType.RSS, "n2", "b")
        dd.subscribe(c1.channel_id, "alice")
        dd.subscribe(c2.channel_id, "alice")  # same recipient on both
        dd.subscribe(c2.channel_id, "bob")
        ds = dd.distribute("d1")  # 3 deliveries
        dd.mark_delivered(ds[0].delivery_id)
        dd.mark_failed(ds[1].delivery_id, "err")
        s = dd.stats()
        assert s.total_channels == 2
        assert s.total_subscribers == 2  # unique
        assert s.total_deliveries == 3
        assert s.delivered == 1
        assert s.failed == 1
        assert s.queued == 1


class TestTotalChannels:
    def test_property(self):
        dd = DocDistribution()
        assert dd.total_channels == 0
        dd.add_channel(ChannelType.EMAIL, "n", "a")
        assert dd.total_channels == 1


class TestTotalDeliveries:
    def test_property(self):
        dd = DocDistribution()
        assert dd.total_deliveries == 0
        ch = dd.add_channel(ChannelType.EMAIL, "n", "a")
        dd.subscribe(ch.channel_id, "alice")
        dd.distribute("d1")
        assert dd.total_deliveries == 1


# ---------------- clear ----------------


class TestClear:
    def test_clear_resets_state(self):
        dd = DocDistribution()
        ch = dd.add_channel(ChannelType.EMAIL, "n", "a")
        dd.subscribe(ch.channel_id, "alice")
        dd.distribute("d1")
        dd.clear()
        assert dd.total_channels == 0
        assert dd.total_deliveries == 0

    def test_clear_resets_id_counter(self):
        dd = DocDistribution()
        ch = dd.add_channel(ChannelType.EMAIL, "n", "a")
        dd.subscribe(ch.channel_id, "alice")
        dd.distribute("d1")
        dd.clear()
        ch2 = dd.add_channel(ChannelType.EMAIL, "n", "a")
        dd.subscribe(ch2.channel_id, "bob")
        new_ds = dd.distribute("d2")
        assert new_ds[0].delivery_id == 1


# ---------------- edge cases ----------------


class TestEdgeCases:
    def test_distribute_after_remove(self):
        dd = DocDistribution()
        ch = dd.add_channel(ChannelType.EMAIL, "n", "a")
        dd.subscribe(ch.channel_id, "alice")
        dd.remove_channel(ch.channel_id)
        assert dd.distribute("d1") == []

    def test_mark_delivered_increments_attempts(self):
        dd = DocDistribution()
        ch = dd.add_channel(ChannelType.EMAIL, "n", "a")
        dd.subscribe(ch.channel_id, "alice")
        d = dd.distribute("d1")[0]
        dd.mark_failed(d.delivery_id, "oops")
        dd.retry_failed(d.delivery_id)
        dd.mark_delivered(d.delivery_id)
        assert dd._deliveries[d.delivery_id].attempts == 2

    def test_retry_after_delivered(self):
        dd = DocDistribution()
        ch = dd.add_channel(ChannelType.EMAIL, "n", "a")
        dd.subscribe(ch.channel_id, "alice")
        d = dd.distribute("d1")[0]
        dd.mark_delivered(d.delivery_id)
        assert dd.retry_failed(d.delivery_id) is False

    def test_unique_subscriber_count_in_stats(self):
        dd = DocDistribution()
        c1 = dd.add_channel(ChannelType.EMAIL, "n1", "a")
        c2 = dd.add_channel(ChannelType.RSS, "n2", "b")
        dd.subscribe(c1.channel_id, "x")
        dd.subscribe(c2.channel_id, "x")
        assert dd.stats().total_subscribers == 1

    def test_distribute_increments_ids_across_calls(self):
        dd = DocDistribution()
        ch = dd.add_channel(ChannelType.EMAIL, "n", "a")
        dd.subscribe(ch.channel_id, "a")
        d1 = dd.distribute("doc1")[0]
        d2 = dd.distribute("doc2")[0]
        assert d2.delivery_id == d1.delivery_id + 1

    def test_metadata_isolated_per_channel(self):
        dd = DocDistribution()
        md = {"k": "v"}
        ch = dd.add_channel(ChannelType.EMAIL, "n", "a", metadata=md)
        md["k"] = "changed"
        assert ch.metadata["k"] == "v"
