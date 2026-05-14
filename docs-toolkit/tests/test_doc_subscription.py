"""Tests for docstoolkit.doc_subscription."""
from __future__ import annotations

import pytest

from docstoolkit.doc_subscription import (
    DocSubscription,
    Frequency,
    Notification,
    NotificationChannel,
    Subscription,
    SubscriptionType,
    UserPreferences,
)


# Helpers --------------------------------------------------------------------

def _ts_for_hour(h: int) -> float:
    """Return a timestamp whose UTC hour is exactly h."""
    return float(h * 3600)


# Enums ----------------------------------------------------------------------

class TestSubscriptionType:
    def test_has_document(self):
        assert SubscriptionType.DOCUMENT.value == "document"

    def test_has_tag(self):
        assert SubscriptionType.TAG.value == "tag"

    def test_has_topic(self):
        assert SubscriptionType.TOPIC.value == "topic"

    def test_has_author(self):
        assert SubscriptionType.AUTHOR.value == "author"

    def test_has_keyword(self):
        assert SubscriptionType.KEYWORD.value == "keyword"

    def test_unique_values(self):
        vals = {st.value for st in SubscriptionType}
        assert len(vals) == 5


class TestNotificationChannel:
    def test_email(self):
        assert NotificationChannel.EMAIL.value == "email"

    def test_in_app(self):
        assert NotificationChannel.IN_APP.value == "in_app"

    def test_sms(self):
        assert NotificationChannel.SMS.value == "sms"

    def test_webhook(self):
        assert NotificationChannel.WEBHOOK.value == "webhook"

    def test_digest(self):
        assert NotificationChannel.DIGEST.value == "digest"


class TestFrequency:
    def test_immediate(self):
        assert Frequency.IMMEDIATE.value == "immediate"

    def test_hourly(self):
        assert Frequency.HOURLY.value == "hourly"

    def test_daily(self):
        assert Frequency.DAILY.value == "daily"

    def test_weekly(self):
        assert Frequency.WEEKLY.value == "weekly"

    def test_off(self):
        assert Frequency.OFF.value == "off"


# Dataclasses ----------------------------------------------------------------

class TestSubscription:
    def test_basic_construction(self):
        sub = Subscription(
            sub_id="abc",
            user_id="u1",
            subscription_type=SubscriptionType.DOCUMENT,
            target="d1",
        )
        assert sub.sub_id == "abc"
        assert sub.user_id == "u1"
        assert sub.enabled is True
        assert sub.frequency == Frequency.IMMEDIATE
        assert sub.channels == set()
        assert sub.created_at == 0.0

    def test_channels_default_independent(self):
        a = Subscription(
            sub_id="a", user_id="u", subscription_type=SubscriptionType.TAG, target="t"
        )
        b = Subscription(
            sub_id="b", user_id="u", subscription_type=SubscriptionType.TAG, target="t"
        )
        a.channels.add(NotificationChannel.EMAIL)
        assert NotificationChannel.EMAIL not in b.channels


class TestUserPreferences:
    def test_defaults(self):
        p = UserPreferences(user_id="u")
        assert p.user_id == "u"
        assert p.default_channels == set()
        assert p.default_frequency == Frequency.IMMEDIATE
        assert p.quiet_hours is None
        assert p.do_not_disturb is False

    def test_with_quiet_hours(self):
        p = UserPreferences(user_id="u", quiet_hours=(22, 7))
        assert p.quiet_hours == (22, 7)


class TestNotification:
    def test_basic(self):
        sub = Subscription(
            sub_id="s", user_id="u", subscription_type=SubscriptionType.DOCUMENT, target="d"
        )
        n = Notification(
            notification_id=1,
            subscription=sub,
            subject_doc_id="d",
            event="updated",
            timestamp=10.0,
            channels=[NotificationChannel.EMAIL],
        )
        assert n.notification_id == 1
        assert n.event == "updated"
        assert n.timestamp == 10.0
        assert n.channels == [NotificationChannel.EMAIL]


# DocSubscription: subscribe -------------------------------------------------

class TestSubscribe:
    def test_basic_subscribe(self):
        ds = DocSubscription()
        sub = ds.subscribe("u1", SubscriptionType.DOCUMENT, "d1")
        assert sub.user_id == "u1"
        assert sub.target == "d1"
        assert sub.subscription_type == SubscriptionType.DOCUMENT
        assert sub.enabled is True
        assert ds.subscription_count == 1

    def test_subscribe_returns_unique_ids(self):
        ds = DocSubscription()
        s1 = ds.subscribe("u1", SubscriptionType.TAG, "ai")
        s2 = ds.subscribe("u1", SubscriptionType.TAG, "ai")
        assert s1.sub_id != s2.sub_id

    def test_subscribe_default_channels_no_prefs(self):
        ds = DocSubscription()
        sub = ds.subscribe("u1", SubscriptionType.TAG, "x")
        # falls back to IN_APP when nothing else is configured
        assert NotificationChannel.IN_APP in sub.channels

    def test_subscribe_explicit_channels(self):
        ds = DocSubscription()
        sub = ds.subscribe(
            "u1",
            SubscriptionType.TAG,
            "x",
            channels={NotificationChannel.EMAIL, NotificationChannel.SMS},
        )
        assert sub.channels == {NotificationChannel.EMAIL, NotificationChannel.SMS}

    def test_subscribe_uses_prefs_for_channels(self):
        ds = DocSubscription()
        ds.set_user_preferences(
            "u1", default_channels={NotificationChannel.WEBHOOK}
        )
        sub = ds.subscribe("u1", SubscriptionType.TAG, "x")
        assert sub.channels == {NotificationChannel.WEBHOOK}

    def test_subscribe_uses_prefs_for_frequency(self):
        ds = DocSubscription()
        ds.set_user_preferences("u1", default_frequency=Frequency.DAILY)
        sub = ds.subscribe("u1", SubscriptionType.TAG, "x")
        assert sub.frequency == Frequency.DAILY

    def test_subscribe_explicit_frequency_overrides_prefs(self):
        ds = DocSubscription()
        ds.set_user_preferences("u1", default_frequency=Frequency.DAILY)
        sub = ds.subscribe(
            "u1", SubscriptionType.TAG, "x", frequency=Frequency.HOURLY
        )
        assert sub.frequency == Frequency.HOURLY

    def test_subscribe_with_now(self):
        ds = DocSubscription()
        sub = ds.subscribe("u1", SubscriptionType.TOPIC, "ml", now=123.4)
        assert sub.created_at == 123.4


# Unsubscribe ----------------------------------------------------------------

class TestUnsubscribe:
    def test_unsubscribe_existing(self):
        ds = DocSubscription()
        sub = ds.subscribe("u", SubscriptionType.DOCUMENT, "d")
        assert ds.unsubscribe(sub.sub_id) is True
        assert ds.subscription_count == 0

    def test_unsubscribe_missing(self):
        ds = DocSubscription()
        assert ds.unsubscribe("nope") is False

    def test_unsubscribe_twice(self):
        ds = DocSubscription()
        sub = ds.subscribe("u", SubscriptionType.DOCUMENT, "d")
        ds.unsubscribe(sub.sub_id)
        assert ds.unsubscribe(sub.sub_id) is False


class TestUnsubscribeAll:
    def test_removes_only_target_user(self):
        ds = DocSubscription()
        ds.subscribe("u1", SubscriptionType.DOCUMENT, "d1")
        ds.subscribe("u1", SubscriptionType.TAG, "t")
        ds.subscribe("u2", SubscriptionType.DOCUMENT, "d2")
        removed = ds.unsubscribe_all("u1")
        assert removed == 2
        assert ds.subscription_count == 1
        remaining = ds.subscriptions_for_user("u2")
        assert len(remaining) == 1

    def test_no_subs_returns_zero(self):
        ds = DocSubscription()
        assert ds.unsubscribe_all("ghost") == 0


# Preferences ----------------------------------------------------------------

class TestSetUserPreferences:
    def test_create_new_prefs(self):
        ds = DocSubscription()
        p = ds.set_user_preferences(
            "u", default_channels={NotificationChannel.EMAIL}
        )
        assert p.user_id == "u"
        assert p.default_channels == {NotificationChannel.EMAIL}

    def test_partial_update_keeps_other_fields(self):
        ds = DocSubscription()
        ds.set_user_preferences(
            "u",
            default_channels={NotificationChannel.EMAIL},
            default_frequency=Frequency.DAILY,
        )
        ds.set_user_preferences("u", quiet_hours=(22, 7))
        p = ds.get_preferences("u")
        assert p.default_channels == {NotificationChannel.EMAIL}
        assert p.default_frequency == Frequency.DAILY
        assert p.quiet_hours == (22, 7)

    def test_set_do_not_disturb(self):
        ds = DocSubscription()
        p = ds.set_user_preferences("u", do_not_disturb=True)
        assert p.do_not_disturb is True

    def test_set_quiet_hours(self):
        ds = DocSubscription()
        p = ds.set_user_preferences("u", quiet_hours=(0, 6))
        assert p.quiet_hours == (0, 6)


class TestGetPreferences:
    def test_missing_returns_none(self):
        ds = DocSubscription()
        assert ds.get_preferences("ghost") is None

    def test_returns_prefs(self):
        ds = DocSubscription()
        ds.set_user_preferences("u", default_frequency=Frequency.WEEKLY)
        p = ds.get_preferences("u")
        assert p is not None
        assert p.default_frequency == Frequency.WEEKLY


# Listings -------------------------------------------------------------------

class TestSubscriptionsForUser:
    def test_returns_user_subs(self):
        ds = DocSubscription()
        ds.subscribe("u1", SubscriptionType.DOCUMENT, "d1")
        ds.subscribe("u1", SubscriptionType.TAG, "t")
        ds.subscribe("u2", SubscriptionType.DOCUMENT, "d2")
        subs = ds.subscriptions_for_user("u1")
        assert len(subs) == 2
        assert all(s.user_id == "u1" for s in subs)

    def test_empty_for_unknown_user(self):
        ds = DocSubscription()
        assert ds.subscriptions_for_user("ghost") == []


class TestSubscribersForDoc:
    def test_returns_doc_subs(self):
        ds = DocSubscription()
        ds.subscribe("u1", SubscriptionType.DOCUMENT, "d1")
        ds.subscribe("u2", SubscriptionType.DOCUMENT, "d1")
        ds.subscribe("u3", SubscriptionType.DOCUMENT, "d2")
        ds.subscribe("u4", SubscriptionType.TAG, "d1")  # not a DOCUMENT sub
        subs = ds.subscribers_for_doc("d1")
        assert len(subs) == 2
        assert {s.user_id for s in subs} == {"u1", "u2"}

    def test_empty(self):
        ds = DocSubscription()
        assert ds.subscribers_for_doc("none") == []


class TestSubscribersForTag:
    def test_returns_tag_subs(self):
        ds = DocSubscription()
        ds.subscribe("u1", SubscriptionType.TAG, "ai")
        ds.subscribe("u2", SubscriptionType.TAG, "ai")
        ds.subscribe("u3", SubscriptionType.TAG, "ml")
        ds.subscribe("u4", SubscriptionType.DOCUMENT, "ai")
        subs = ds.subscribers_for_tag("ai")
        assert len(subs) == 2
        assert {s.user_id for s in subs} == {"u1", "u2"}

    def test_empty(self):
        ds = DocSubscription()
        assert ds.subscribers_for_tag("nope") == []


# find_matching --------------------------------------------------------------

class TestFindMatching:
    def test_match_document(self):
        ds = DocSubscription()
        ds.subscribe("u1", SubscriptionType.DOCUMENT, "d1")
        ds.subscribe("u2", SubscriptionType.DOCUMENT, "d2")
        matches = ds.find_matching("d1")
        assert len(matches) == 1
        assert matches[0].user_id == "u1"

    def test_match_tag(self):
        ds = DocSubscription()
        ds.subscribe("u1", SubscriptionType.TAG, "ai")
        ds.subscribe("u2", SubscriptionType.TAG, "ml")
        matches = ds.find_matching("d_any", tags=["ai", "other"])
        assert len(matches) == 1
        assert matches[0].user_id == "u1"

    def test_match_author(self):
        ds = DocSubscription()
        ds.subscribe("u1", SubscriptionType.AUTHOR, "alice")
        ds.subscribe("u2", SubscriptionType.AUTHOR, "bob")
        matches = ds.find_matching("d", author="alice")
        assert len(matches) == 1
        assert matches[0].user_id == "u1"

    def test_match_topic(self):
        ds = DocSubscription()
        ds.subscribe("u1", SubscriptionType.TOPIC, "memory")
        matches = ds.find_matching("d", topic="memory")
        assert len(matches) == 1

    def test_no_match(self):
        ds = DocSubscription()
        ds.subscribe("u1", SubscriptionType.DOCUMENT, "d1")
        assert ds.find_matching("d2") == []

    def test_multiple_match_types_combine(self):
        ds = DocSubscription()
        ds.subscribe("u1", SubscriptionType.DOCUMENT, "d1")
        ds.subscribe("u2", SubscriptionType.TAG, "ai")
        ds.subscribe("u3", SubscriptionType.AUTHOR, "alice")
        matches = ds.find_matching("d1", tags=["ai"], author="alice")
        assert {m.user_id for m in matches} == {"u1", "u2", "u3"}

    def test_no_dup_for_same_sub(self):
        ds = DocSubscription()
        sub = ds.subscribe("u1", SubscriptionType.DOCUMENT, "d1")
        matches = ds.find_matching("d1", tags=["ai"])
        assert sum(1 for m in matches if m.sub_id == sub.sub_id) == 1


# should_notify --------------------------------------------------------------

class TestShouldNotify:
    def test_enabled_default(self):
        ds = DocSubscription()
        sub = ds.subscribe("u", SubscriptionType.DOCUMENT, "d")
        assert ds.should_notify(sub) is True

    def test_disabled(self):
        ds = DocSubscription()
        sub = ds.subscribe("u", SubscriptionType.DOCUMENT, "d")
        sub.enabled = False
        assert ds.should_notify(sub) is False

    def test_off_frequency(self):
        ds = DocSubscription()
        sub = ds.subscribe(
            "u", SubscriptionType.DOCUMENT, "d", frequency=Frequency.OFF
        )
        assert ds.should_notify(sub) is False

    def test_no_prefs_means_notify(self):
        ds = DocSubscription()
        sub = ds.subscribe("u", SubscriptionType.DOCUMENT, "d")
        assert ds.should_notify(sub, now=12345.0) is True


class TestShouldNotifyQuietHours:
    def test_wraparound_inside_quiet_blocks(self):
        ds = DocSubscription()
        ds.set_user_preferences("u", quiet_hours=(22, 7))
        sub = ds.subscribe("u", SubscriptionType.DOCUMENT, "d")
        # hour=23 is inside quiet window (22-7 wrap)
        assert ds.should_notify(sub, now=_ts_for_hour(23)) is False

    def test_wraparound_outside_quiet_allows(self):
        ds = DocSubscription()
        ds.set_user_preferences("u", quiet_hours=(22, 7))
        sub = ds.subscribe("u", SubscriptionType.DOCUMENT, "d")
        # hour=10 is outside quiet, ok
        assert ds.should_notify(sub, now=_ts_for_hour(10)) is True

    def test_wraparound_early_morning_blocked(self):
        ds = DocSubscription()
        ds.set_user_preferences("u", quiet_hours=(22, 7))
        sub = ds.subscribe("u", SubscriptionType.DOCUMENT, "d")
        # hour=5 is inside quiet
        assert ds.should_notify(sub, now=_ts_for_hour(5)) is False

    def test_wraparound_boundary_end(self):
        ds = DocSubscription()
        ds.set_user_preferences("u", quiet_hours=(22, 7))
        sub = ds.subscribe("u", SubscriptionType.DOCUMENT, "d")
        # hour=7 is no longer quiet (end exclusive)
        assert ds.should_notify(sub, now=_ts_for_hour(7)) is True

    def test_wraparound_boundary_start(self):
        ds = DocSubscription()
        ds.set_user_preferences("u", quiet_hours=(22, 7))
        sub = ds.subscribe("u", SubscriptionType.DOCUMENT, "d")
        # hour=22 is quiet (start inclusive)
        assert ds.should_notify(sub, now=_ts_for_hour(22)) is False

    def test_non_wraparound_inside(self):
        ds = DocSubscription()
        # (9, 17): active hours -> notify only 9..17
        ds.set_user_preferences("u", quiet_hours=(9, 17))
        sub = ds.subscribe("u", SubscriptionType.DOCUMENT, "d")
        assert ds.should_notify(sub, now=_ts_for_hour(10)) is True

    def test_non_wraparound_outside(self):
        ds = DocSubscription()
        ds.set_user_preferences("u", quiet_hours=(9, 17))
        sub = ds.subscribe("u", SubscriptionType.DOCUMENT, "d")
        assert ds.should_notify(sub, now=_ts_for_hour(20)) is False


class TestShouldNotifyDoNotDisturb:
    def test_dnd_blocks(self):
        ds = DocSubscription()
        ds.set_user_preferences("u", do_not_disturb=True)
        sub = ds.subscribe("u", SubscriptionType.DOCUMENT, "d")
        assert ds.should_notify(sub) is False

    def test_dnd_off_allows(self):
        ds = DocSubscription()
        ds.set_user_preferences("u", do_not_disturb=False)
        sub = ds.subscribe("u", SubscriptionType.DOCUMENT, "d")
        assert ds.should_notify(sub) is True


# prepare_notifications ------------------------------------------------------

class TestPrepareNotifications:
    def test_creates_notifications(self):
        ds = DocSubscription()
        ds.subscribe(
            "u1",
            SubscriptionType.DOCUMENT,
            "d1",
            channels={NotificationChannel.EMAIL},
        )
        notes = ds.prepare_notifications("d1", "updated", now=100.0)
        assert len(notes) == 1
        n = notes[0]
        assert n.subject_doc_id == "d1"
        assert n.event == "updated"
        assert n.timestamp == 100.0
        assert NotificationChannel.EMAIL in n.channels

    def test_skips_disabled(self):
        ds = DocSubscription()
        sub = ds.subscribe("u1", SubscriptionType.DOCUMENT, "d1")
        ds.disable_subscription(sub.sub_id)
        notes = ds.prepare_notifications("d1", "updated")
        assert notes == []

    def test_skips_dnd(self):
        ds = DocSubscription()
        ds.subscribe("u1", SubscriptionType.DOCUMENT, "d1")
        ds.set_user_preferences("u1", do_not_disturb=True)
        notes = ds.prepare_notifications("d1", "updated")
        assert notes == []

    def test_skips_off(self):
        ds = DocSubscription()
        ds.subscribe(
            "u1", SubscriptionType.DOCUMENT, "d1", frequency=Frequency.OFF
        )
        notes = ds.prepare_notifications("d1", "updated")
        assert notes == []

    def test_unique_ids(self):
        ds = DocSubscription()
        ds.subscribe("u1", SubscriptionType.DOCUMENT, "d1")
        ds.subscribe("u2", SubscriptionType.DOCUMENT, "d1")
        notes = ds.prepare_notifications("d1", "updated")
        assert len(notes) == 2
        assert notes[0].notification_id != notes[1].notification_id

    def test_combines_tags_and_doc(self):
        ds = DocSubscription()
        ds.subscribe("u1", SubscriptionType.DOCUMENT, "d1")
        ds.subscribe("u2", SubscriptionType.TAG, "ai")
        notes = ds.prepare_notifications("d1", "updated", tags=["ai"])
        assert len(notes) == 2


# enable/disable/update_frequency -------------------------------------------

class TestEnableDisable:
    def test_enable_existing(self):
        ds = DocSubscription()
        sub = ds.subscribe("u", SubscriptionType.DOCUMENT, "d")
        ds.disable_subscription(sub.sub_id)
        assert ds.enable_subscription(sub.sub_id) is True
        assert sub.enabled is True

    def test_disable_existing(self):
        ds = DocSubscription()
        sub = ds.subscribe("u", SubscriptionType.DOCUMENT, "d")
        assert ds.disable_subscription(sub.sub_id) is True
        assert sub.enabled is False

    def test_enable_missing(self):
        ds = DocSubscription()
        assert ds.enable_subscription("ghost") is False

    def test_disable_missing(self):
        ds = DocSubscription()
        assert ds.disable_subscription("ghost") is False


class TestUpdateFrequency:
    def test_update_existing(self):
        ds = DocSubscription()
        sub = ds.subscribe("u", SubscriptionType.DOCUMENT, "d")
        assert ds.update_frequency(sub.sub_id, Frequency.WEEKLY) is True
        assert sub.frequency == Frequency.WEEKLY

    def test_update_missing(self):
        ds = DocSubscription()
        assert ds.update_frequency("ghost", Frequency.DAILY) is False

    def test_update_to_off(self):
        ds = DocSubscription()
        sub = ds.subscribe("u", SubscriptionType.DOCUMENT, "d")
        ds.update_frequency(sub.sub_id, Frequency.OFF)
        assert ds.should_notify(sub) is False


# Counts and clear -----------------------------------------------------------

class TestCountProps:
    def test_subscription_count_zero(self):
        ds = DocSubscription()
        assert ds.subscription_count == 0

    def test_subscription_count_grows(self):
        ds = DocSubscription()
        ds.subscribe("u1", SubscriptionType.DOCUMENT, "d")
        ds.subscribe("u2", SubscriptionType.TAG, "t")
        assert ds.subscription_count == 2

    def test_user_count_from_subs(self):
        ds = DocSubscription()
        ds.subscribe("u1", SubscriptionType.DOCUMENT, "d")
        ds.subscribe("u1", SubscriptionType.TAG, "t")
        ds.subscribe("u2", SubscriptionType.DOCUMENT, "d2")
        assert ds.user_count == 2

    def test_user_count_includes_prefs_only(self):
        ds = DocSubscription()
        ds.subscribe("u1", SubscriptionType.DOCUMENT, "d")
        ds.set_user_preferences("u2", do_not_disturb=True)
        assert ds.user_count == 2

    def test_user_count_empty(self):
        ds = DocSubscription()
        assert ds.user_count == 0


class TestClear:
    def test_clear_subs(self):
        ds = DocSubscription()
        ds.subscribe("u", SubscriptionType.DOCUMENT, "d")
        ds.clear()
        assert ds.subscription_count == 0

    def test_clear_prefs(self):
        ds = DocSubscription()
        ds.set_user_preferences("u", do_not_disturb=True)
        ds.clear()
        assert ds.get_preferences("u") is None

    def test_clear_resets_notification_ids(self):
        ds = DocSubscription()
        ds.subscribe("u", SubscriptionType.DOCUMENT, "d")
        ds.prepare_notifications("d", "ev")
        ds.clear()
        ds.subscribe("u", SubscriptionType.DOCUMENT, "d")
        notes = ds.prepare_notifications("d", "ev")
        assert notes[0].notification_id == 1


# Edge cases -----------------------------------------------------------------

class TestEdgeCases:
    def test_frequency_off_blocks_notify(self):
        ds = DocSubscription()
        sub = ds.subscribe(
            "u", SubscriptionType.DOCUMENT, "d", frequency=Frequency.OFF
        )
        assert ds.should_notify(sub) is False

    def test_user_without_prefs_can_be_notified(self):
        ds = DocSubscription()
        sub = ds.subscribe("u", SubscriptionType.DOCUMENT, "d")
        assert ds.should_notify(sub, now=_ts_for_hour(3)) is True

    def test_quiet_hours_equal_bounds_no_block(self):
        ds = DocSubscription()
        ds.set_user_preferences("u", quiet_hours=(5, 5))
        sub = ds.subscribe("u", SubscriptionType.DOCUMENT, "d")
        # Degenerate bounds: don't apply quiet-hour filter
        assert ds.should_notify(sub, now=_ts_for_hour(5)) is True

    def test_prepare_notifications_no_match(self):
        ds = DocSubscription()
        ds.subscribe("u", SubscriptionType.DOCUMENT, "x")
        notes = ds.prepare_notifications("other", "ev")
        assert notes == []

    def test_subscribe_with_empty_channels(self):
        ds = DocSubscription()
        sub = ds.subscribe(
            "u", SubscriptionType.DOCUMENT, "d", channels=set()
        )
        # explicit empty channels respected
        assert sub.channels == set()

    def test_multiple_users_isolated(self):
        ds = DocSubscription()
        ds.set_user_preferences("u1", do_not_disturb=True)
        s2 = ds.subscribe("u2", SubscriptionType.DOCUMENT, "d")
        # u2 has no DND, should notify
        assert ds.should_notify(s2) is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
