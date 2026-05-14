"""Tests for E202 docstoolkit.doc_publish."""
from __future__ import annotations

import pytest

from docstoolkit.doc_publish import (
    DocPublish,
    Publication,
    PublishState,
    PublishStats,
)


# ---------------------------------------------------------------------------
# PublishState
# ---------------------------------------------------------------------------


class TestPublishState:
    def test_values_exist(self):
        assert PublishState.DRAFT.value == "draft"
        assert PublishState.SCHEDULED.value == "scheduled"
        assert PublishState.PUBLISHED.value == "published"
        assert PublishState.EMBARGOED.value == "embargoed"
        assert PublishState.REVOKED.value == "revoked"
        assert PublishState.EXPIRED.value == "expired"

    def test_state_count(self):
        assert len(list(PublishState)) == 6


# ---------------------------------------------------------------------------
# Publication
# ---------------------------------------------------------------------------


class TestPublication:
    def test_minimal_construction(self):
        p = Publication(pub_id="x", doc_id="d", state=PublishState.DRAFT)
        assert p.pub_id == "x"
        assert p.doc_id == "d"
        assert p.state == PublishState.DRAFT
        assert p.scheduled_for is None
        assert p.published_at is None
        assert p.expires_at is None
        assert p.revoked_at is None
        assert p.revoked_by is None
        assert p.author is None
        assert p.embargo_until is None

    def test_full_construction(self):
        p = Publication(
            pub_id="x",
            doc_id="d",
            state=PublishState.PUBLISHED,
            scheduled_for=10.0,
            published_at=20.0,
            expires_at=30.0,
            revoked_at=None,
            revoked_by=None,
            author="alice",
            embargo_until=15.0,
        )
        assert p.scheduled_for == 10.0
        assert p.published_at == 20.0
        assert p.expires_at == 30.0
        assert p.author == "alice"
        assert p.embargo_until == 15.0


# ---------------------------------------------------------------------------
# PublishStats
# ---------------------------------------------------------------------------


class TestPublishStats:
    def test_defaults(self):
        s = PublishStats(total=0)
        assert s.total == 0
        assert s.by_state == {}
        assert s.scheduled_count == 0
        assert s.published_count == 0

    def test_full(self):
        s = PublishStats(total=3, by_state={"draft": 1, "published": 2},
                        scheduled_count=0, published_count=2)
        assert s.total == 3
        assert s.by_state["published"] == 2


# ---------------------------------------------------------------------------
# submit_draft
# ---------------------------------------------------------------------------


class TestSubmitDraft:
    def test_returns_publication(self):
        m = DocPublish()
        p = m.submit_draft("d1")
        assert isinstance(p, Publication)
        assert p.doc_id == "d1"
        assert p.state == PublishState.DRAFT

    def test_sets_author(self):
        m = DocPublish()
        p = m.submit_draft("d1", author="bob")
        assert p.author == "bob"

    def test_pub_id_unique(self):
        m = DocPublish()
        p1 = m.submit_draft("d1")
        p2 = m.submit_draft("d2")
        assert p1.pub_id != p2.pub_id

    def test_replaces_existing(self):
        m = DocPublish()
        p1 = m.submit_draft("d1", author="a")
        p2 = m.submit_draft("d1", author="b")
        assert m.get("d1").author == "b"
        assert p2.pub_id != p1.pub_id

    def test_total_publications_increments(self):
        m = DocPublish()
        m.submit_draft("d1")
        m.submit_draft("d2")
        m.submit_draft("d3")
        assert m.total_publications == 3


# ---------------------------------------------------------------------------
# schedule
# ---------------------------------------------------------------------------


class TestSchedule:
    def test_future_schedule(self):
        m = DocPublish()
        m.submit_draft("d1")
        p = m.schedule("d1", scheduled_for=100.0, now=10.0)
        assert p is not None
        assert p.state == PublishState.SCHEDULED
        assert p.scheduled_for == 100.0

    def test_past_schedule_publishes(self):
        m = DocPublish()
        m.submit_draft("d1")
        p = m.schedule("d1", scheduled_for=5.0, now=10.0)
        assert p.state == PublishState.PUBLISHED
        assert p.published_at == 10.0

    def test_zero_schedule_publishes(self):
        m = DocPublish()
        m.submit_draft("d1")
        p = m.schedule("d1", scheduled_for=0.0, now=10.0)
        assert p.state == PublishState.PUBLISHED

    def test_schedule_with_embargo_in_future(self):
        m = DocPublish()
        m.submit_draft("d1")
        # past schedule but embargo active → EMBARGOED
        p = m.schedule("d1", scheduled_for=5.0, embargo_until=20.0, now=10.0)
        assert p.state == PublishState.EMBARGOED
        assert p.embargo_until == 20.0

    def test_schedule_with_expires_at(self):
        m = DocPublish()
        m.submit_draft("d1")
        p = m.schedule("d1", scheduled_for=100.0, expires_at=200.0, now=10.0)
        assert p.expires_at == 200.0

    def test_schedule_unknown_doc(self):
        m = DocPublish()
        assert m.schedule("nope", scheduled_for=5.0, now=0.0) is None

    def test_schedule_revoked_returns_none(self):
        m = DocPublish()
        m.submit_draft("d1")
        m.revoke("d1", revoked_by="admin")
        assert m.schedule("d1", scheduled_for=100.0, now=10.0) is None

    def test_schedule_already_published(self):
        m = DocPublish()
        m.submit_draft("d1")
        m.publish_now("d1", now=5.0)
        # Already PUBLISHED, schedule should not transition
        assert m.schedule("d1", scheduled_for=200.0, now=10.0) is None


# ---------------------------------------------------------------------------
# publish_now
# ---------------------------------------------------------------------------


class TestPublishNow:
    def test_publish_from_draft(self):
        m = DocPublish()
        m.submit_draft("d1")
        p = m.publish_now("d1", now=50.0)
        assert p.state == PublishState.PUBLISHED
        assert p.published_at == 50.0

    def test_publish_from_scheduled(self):
        m = DocPublish()
        m.submit_draft("d1")
        m.schedule("d1", scheduled_for=100.0, now=10.0)
        p = m.publish_now("d1", now=20.0)
        assert p.state == PublishState.PUBLISHED

    def test_publish_with_expires_at(self):
        m = DocPublish()
        m.submit_draft("d1")
        p = m.publish_now("d1", expires_at=500.0, now=10.0)
        assert p.expires_at == 500.0

    def test_publish_unknown(self):
        m = DocPublish()
        assert m.publish_now("none") is None

    def test_publish_revoked(self):
        m = DocPublish()
        m.submit_draft("d1")
        m.revoke("d1", revoked_by="admin")
        assert m.publish_now("d1") is None

    def test_publish_clears_embargo(self):
        m = DocPublish()
        m.submit_draft("d1")
        m.schedule("d1", scheduled_for=5.0, embargo_until=100.0, now=10.0)
        # currently EMBARGOED — publish_now should force publication
        p = m.publish_now("d1", now=20.0)
        assert p.state == PublishState.PUBLISHED
        assert p.embargo_until is None


# ---------------------------------------------------------------------------
# embargo
# ---------------------------------------------------------------------------


class TestEmbargo:
    def test_embargo_published(self):
        m = DocPublish()
        m.submit_draft("d1")
        m.publish_now("d1", now=10.0)
        assert m.embargo("d1", embargo_until=100.0) is True
        assert m.get("d1").state == PublishState.EMBARGOED
        assert m.get("d1").embargo_until == 100.0

    def test_embargo_draft_fails(self):
        m = DocPublish()
        m.submit_draft("d1")
        assert m.embargo("d1", embargo_until=100.0) is False

    def test_embargo_scheduled_fails(self):
        m = DocPublish()
        m.submit_draft("d1")
        m.schedule("d1", scheduled_for=100.0, now=10.0)
        assert m.embargo("d1", embargo_until=200.0) is False

    def test_embargo_unknown(self):
        m = DocPublish()
        assert m.embargo("nope", embargo_until=100.0) is False

    def test_embargo_revoked(self):
        m = DocPublish()
        m.submit_draft("d1")
        m.publish_now("d1", now=10.0)
        m.revoke("d1", revoked_by="admin")
        assert m.embargo("d1", embargo_until=100.0) is False


# ---------------------------------------------------------------------------
# revoke
# ---------------------------------------------------------------------------


class TestRevoke:
    def test_revoke_published(self):
        m = DocPublish()
        m.submit_draft("d1")
        m.publish_now("d1", now=10.0)
        assert m.revoke("d1", revoked_by="admin", now=20.0) is True
        p = m.get("d1")
        assert p.state == PublishState.REVOKED
        assert p.revoked_at == 20.0
        assert p.revoked_by == "admin"

    def test_revoke_draft(self):
        m = DocPublish()
        m.submit_draft("d1")
        assert m.revoke("d1", revoked_by="admin") is True
        assert m.get("d1").state == PublishState.REVOKED

    def test_revoke_scheduled(self):
        m = DocPublish()
        m.submit_draft("d1")
        m.schedule("d1", scheduled_for=100.0, now=10.0)
        assert m.revoke("d1", revoked_by="admin") is True

    def test_revoke_unknown(self):
        m = DocPublish()
        assert m.revoke("nope", revoked_by="admin") is False

    def test_double_revoke_returns_false(self):
        m = DocPublish()
        m.submit_draft("d1")
        m.revoke("d1", revoked_by="admin")
        assert m.revoke("d1", revoked_by="admin") is False


# ---------------------------------------------------------------------------
# release_for_publish
# ---------------------------------------------------------------------------


class TestReleaseForPublish:
    def test_releases_due(self):
        m = DocPublish()
        m.submit_draft("d1")
        m.schedule("d1", scheduled_for=50.0, now=10.0)
        released = m.release_for_publish(now=60.0)
        assert len(released) == 1
        assert released[0].state == PublishState.PUBLISHED
        assert released[0].published_at == 60.0

    def test_not_due_yet(self):
        m = DocPublish()
        m.submit_draft("d1")
        m.schedule("d1", scheduled_for=100.0, now=10.0)
        released = m.release_for_publish(now=50.0)
        assert released == []
        assert m.get("d1").state == PublishState.SCHEDULED

    def test_embargo_blocks_release(self):
        m = DocPublish()
        m.submit_draft("d1")
        m.schedule("d1", scheduled_for=50.0, embargo_until=200.0, now=10.0)
        released = m.release_for_publish(now=60.0)
        assert released == []
        assert m.get("d1").state == PublishState.EMBARGOED

    def test_multiple_releases(self):
        m = DocPublish()
        for i in range(5):
            m.submit_draft(f"d{i}")
            m.schedule(f"d{i}", scheduled_for=10.0 * i + 1.0, now=0.0)
        released = m.release_for_publish(now=25.0)
        # d0, d1, d2 are due (1.0, 11.0, 21.0); d3, d4 are not
        assert len(released) == 3

    def test_release_ignores_drafts(self):
        m = DocPublish()
        m.submit_draft("d1")
        released = m.release_for_publish(now=100.0)
        assert released == []
        assert m.get("d1").state == PublishState.DRAFT


# ---------------------------------------------------------------------------
# expire_overdue
# ---------------------------------------------------------------------------


class TestExpireOverdue:
    def test_expire_published(self):
        m = DocPublish()
        m.submit_draft("d1")
        m.publish_now("d1", expires_at=100.0, now=10.0)
        count = m.expire_overdue(now=200.0)
        assert count == 1
        assert m.get("d1").state == PublishState.EXPIRED

    def test_no_expires_at(self):
        m = DocPublish()
        m.submit_draft("d1")
        m.publish_now("d1", now=10.0)
        assert m.expire_overdue(now=1000.0) == 0
        assert m.get("d1").state == PublishState.PUBLISHED

    def test_not_yet_expired(self):
        m = DocPublish()
        m.submit_draft("d1")
        m.publish_now("d1", expires_at=500.0, now=10.0)
        assert m.expire_overdue(now=100.0) == 0
        assert m.get("d1").state == PublishState.PUBLISHED

    def test_only_published_expires(self):
        m = DocPublish()
        m.submit_draft("d1")
        m.schedule("d1", scheduled_for=100.0, expires_at=50.0, now=10.0)
        # Currently SCHEDULED, not PUBLISHED — should not expire
        assert m.expire_overdue(now=200.0) == 0
        assert m.get("d1").state == PublishState.SCHEDULED

    def test_multi_expire(self):
        m = DocPublish()
        for i in range(3):
            m.submit_draft(f"d{i}")
            m.publish_now(f"d{i}", expires_at=10.0 + i, now=0.0)
        assert m.expire_overdue(now=100.0) == 3


# ---------------------------------------------------------------------------
# get
# ---------------------------------------------------------------------------


class TestGet:
    def test_returns_publication(self):
        m = DocPublish()
        m.submit_draft("d1")
        assert m.get("d1") is not None

    def test_unknown_returns_none(self):
        m = DocPublish()
        assert m.get("nope") is None


# ---------------------------------------------------------------------------
# state_of
# ---------------------------------------------------------------------------


class TestStateOf:
    def test_draft(self):
        m = DocPublish()
        m.submit_draft("d1")
        assert m.state_of("d1") == PublishState.DRAFT

    def test_unknown_none(self):
        m = DocPublish()
        assert m.state_of("nope") is None

    def test_scheduled_visible_as_published_when_due(self):
        m = DocPublish()
        m.submit_draft("d1")
        m.schedule("d1", scheduled_for=50.0, now=10.0)
        # state_of considers dynamic state — past schedule with no embargo
        assert m.state_of("d1", now=100.0) == PublishState.PUBLISHED

    def test_published_visible_as_expired_after_expiry(self):
        m = DocPublish()
        m.submit_draft("d1")
        m.publish_now("d1", expires_at=100.0, now=10.0)
        assert m.state_of("d1", now=200.0) == PublishState.EXPIRED

    def test_published_under_embargo_appears_embargoed(self):
        m = DocPublish()
        m.submit_draft("d1")
        m.publish_now("d1", now=10.0)
        m.embargo("d1", embargo_until=100.0)
        assert m.state_of("d1", now=20.0) == PublishState.EMBARGOED
        assert m.state_of("d1", now=200.0) == PublishState.PUBLISHED


# ---------------------------------------------------------------------------
# is_public
# ---------------------------------------------------------------------------


class TestIsPublic:
    def test_draft_not_public(self):
        m = DocPublish()
        m.submit_draft("d1")
        assert m.is_public("d1") is False

    def test_scheduled_not_public(self):
        m = DocPublish()
        m.submit_draft("d1")
        m.schedule("d1", scheduled_for=100.0, now=10.0)
        assert m.is_public("d1", now=20.0) is False

    def test_published_is_public(self):
        m = DocPublish()
        m.submit_draft("d1")
        m.publish_now("d1", now=10.0)
        assert m.is_public("d1", now=20.0) is True

    def test_embargoed_not_public(self):
        m = DocPublish()
        m.submit_draft("d1")
        m.publish_now("d1", now=10.0)
        m.embargo("d1", embargo_until=100.0)
        assert m.is_public("d1", now=50.0) is False

    def test_revoked_not_public(self):
        m = DocPublish()
        m.submit_draft("d1")
        m.publish_now("d1", now=10.0)
        m.revoke("d1", revoked_by="admin", now=20.0)
        assert m.is_public("d1", now=30.0) is False

    def test_expired_not_public(self):
        m = DocPublish()
        m.submit_draft("d1")
        m.publish_now("d1", expires_at=50.0, now=10.0)
        assert m.is_public("d1", now=100.0) is False

    def test_unknown_not_public(self):
        m = DocPublish()
        assert m.is_public("nope") is False


# ---------------------------------------------------------------------------
# published_docs
# ---------------------------------------------------------------------------


class TestPublishedDocs:
    def test_empty(self):
        m = DocPublish()
        assert m.published_docs() == []

    def test_lists_published(self):
        m = DocPublish()
        for i in range(3):
            m.submit_draft(f"d{i}")
            m.publish_now(f"d{i}", now=10.0)
        assert len(m.published_docs(now=20.0)) == 3

    def test_excludes_drafts(self):
        m = DocPublish()
        m.submit_draft("d1")
        m.submit_draft("d2")
        m.publish_now("d2", now=10.0)
        ids = [p.doc_id for p in m.published_docs(now=20.0)]
        assert ids == ["d2"]

    def test_excludes_expired(self):
        m = DocPublish()
        m.submit_draft("d1")
        m.publish_now("d1", expires_at=50.0, now=10.0)
        assert m.published_docs(now=100.0) == []


# ---------------------------------------------------------------------------
# scheduled_docs
# ---------------------------------------------------------------------------


class TestScheduledDocs:
    def test_empty(self):
        m = DocPublish()
        assert m.scheduled_docs() == []

    def test_lists_scheduled(self):
        m = DocPublish()
        for i in range(2):
            m.submit_draft(f"d{i}")
            m.schedule(f"d{i}", scheduled_for=100.0 + i, now=0.0)
        assert len(m.scheduled_docs()) == 2

    def test_does_not_include_published(self):
        m = DocPublish()
        m.submit_draft("d1")
        m.publish_now("d1", now=10.0)
        assert m.scheduled_docs() == []


# ---------------------------------------------------------------------------
# embargoed_docs
# ---------------------------------------------------------------------------


class TestEmbargoedDocs:
    def test_empty(self):
        m = DocPublish()
        assert m.embargoed_docs() == []

    def test_lists_embargoed(self):
        m = DocPublish()
        m.submit_draft("d1")
        m.publish_now("d1", now=10.0)
        m.embargo("d1", embargo_until=100.0)
        assert len(m.embargoed_docs(now=20.0)) == 1

    def test_dynamic_embargo_via_state_of(self):
        m = DocPublish()
        m.submit_draft("d1")
        m.publish_now("d1", now=10.0)
        m.embargo("d1", embargo_until=100.0)
        # After embargo passes the doc is effectively PUBLISHED again
        assert m.embargoed_docs(now=200.0) == []


# ---------------------------------------------------------------------------
# revoked_docs
# ---------------------------------------------------------------------------


class TestRevokedDocs:
    def test_empty(self):
        m = DocPublish()
        assert m.revoked_docs() == []

    def test_lists_revoked(self):
        m = DocPublish()
        m.submit_draft("d1")
        m.revoke("d1", revoked_by="admin")
        assert len(m.revoked_docs()) == 1


# ---------------------------------------------------------------------------
# next_scheduled
# ---------------------------------------------------------------------------


class TestNextScheduled:
    def test_empty(self):
        m = DocPublish()
        assert m.next_scheduled() is None

    def test_returns_earliest(self):
        m = DocPublish()
        m.submit_draft("a")
        m.submit_draft("b")
        m.submit_draft("c")
        m.schedule("a", scheduled_for=300.0, now=0.0)
        m.schedule("b", scheduled_for=100.0, now=0.0)
        m.schedule("c", scheduled_for=200.0, now=0.0)
        n = m.next_scheduled()
        assert n is not None
        assert n.doc_id == "b"

    def test_ignores_non_scheduled(self):
        m = DocPublish()
        m.submit_draft("a")
        m.publish_now("a", now=10.0)
        assert m.next_scheduled() is None


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------


class TestStats:
    def test_empty(self):
        m = DocPublish()
        s = m.stats()
        assert s.total == 0
        assert s.scheduled_count == 0
        assert s.published_count == 0

    def test_counts(self):
        m = DocPublish()
        m.submit_draft("a")
        m.submit_draft("b")
        m.publish_now("b", now=10.0)
        m.submit_draft("c")
        m.schedule("c", scheduled_for=100.0, now=10.0)
        s = m.stats(now=20.0)
        assert s.total == 3
        assert s.scheduled_count == 1
        assert s.published_count == 1
        assert s.by_state["draft"] == 1

    def test_stats_reflects_dynamic_state(self):
        m = DocPublish()
        m.submit_draft("a")
        m.publish_now("a", expires_at=50.0, now=10.0)
        s = m.stats(now=100.0)
        # Should reflect EXPIRED effective state
        assert s.by_state["expired"] == 1
        assert s.published_count == 0


# ---------------------------------------------------------------------------
# clear
# ---------------------------------------------------------------------------


class TestClear:
    def test_clear_removes_all(self):
        m = DocPublish()
        m.submit_draft("d1")
        m.submit_draft("d2")
        m.clear()
        assert m.get("d1") is None
        assert m.get("d2") is None
        assert m.stats().total == 0

    def test_clear_resets_total(self):
        m = DocPublish()
        m.submit_draft("d1")
        m.clear()
        assert m.total_publications == 0


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_double_revoke(self):
        m = DocPublish()
        m.submit_draft("d1")
        assert m.revoke("d1", revoked_by="admin") is True
        assert m.revoke("d1", revoked_by="admin") is False

    def test_schedule_on_revoked(self):
        m = DocPublish()
        m.submit_draft("d1")
        m.revoke("d1", revoked_by="admin")
        assert m.schedule("d1", scheduled_for=100.0, now=10.0) is None

    def test_publish_now_on_revoked(self):
        m = DocPublish()
        m.submit_draft("d1")
        m.revoke("d1", revoked_by="admin")
        assert m.publish_now("d1") is None

    def test_embargo_on_revoked(self):
        m = DocPublish()
        m.submit_draft("d1")
        m.publish_now("d1", now=10.0)
        m.revoke("d1", revoked_by="admin", now=15.0)
        assert m.embargo("d1", embargo_until=100.0) is False

    def test_expire_on_revoked_no_change(self):
        m = DocPublish()
        m.submit_draft("d1")
        m.publish_now("d1", expires_at=100.0, now=10.0)
        m.revoke("d1", revoked_by="admin", now=20.0)
        # Revoked is terminal — expire shouldn't transition
        assert m.expire_overdue(now=200.0) == 0
        assert m.get("d1").state == PublishState.REVOKED

    def test_resubmit_after_revoke(self):
        m = DocPublish()
        m.submit_draft("d1")
        m.revoke("d1", revoked_by="admin")
        # resubmitting overwrites — new DRAFT
        p = m.submit_draft("d1")
        assert p.state == PublishState.DRAFT
        assert m.get("d1").state == PublishState.DRAFT

    def test_schedule_twice_only_first_applies(self):
        m = DocPublish()
        m.submit_draft("d1")
        m.schedule("d1", scheduled_for=100.0, now=0.0)
        # Once scheduled, second schedule call returns None (no longer DRAFT)
        assert m.schedule("d1", scheduled_for=200.0, now=0.0) is None
        assert m.get("d1").scheduled_for == 100.0

    def test_release_then_expire(self):
        m = DocPublish()
        m.submit_draft("d1")
        m.schedule("d1", scheduled_for=50.0, expires_at=100.0, now=0.0)
        released = m.release_for_publish(now=60.0)
        assert len(released) == 1
        assert m.expire_overdue(now=150.0) == 1
        assert m.get("d1").state == PublishState.EXPIRED

    def test_total_publications_does_not_decrement(self):
        m = DocPublish()
        m.submit_draft("d1")
        m.revoke("d1", revoked_by="admin")
        # total_publications only counts submissions, not active docs
        assert m.total_publications == 1
