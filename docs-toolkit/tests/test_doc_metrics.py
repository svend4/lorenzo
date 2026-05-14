"""Tests for docstoolkit.doc_metrics."""
from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_metrics import (
    DocEvent,
    DocMetrics,
    DocMetricsSnapshot,
    EngagementScore,
    EventType,
)


class TestEventType:
    def test_has_view(self):
        assert EventType.VIEW.value == "view"

    def test_has_edit(self):
        assert EventType.EDIT.value == "edit"

    def test_has_all_seven(self):
        names = {e.name for e in EventType}
        assert names == {
            "VIEW",
            "EDIT",
            "COMMENT",
            "SHARE",
            "EXPORT",
            "DOWNLOAD",
            "REACTION",
        }

    def test_is_enum(self):
        from enum import Enum

        assert issubclass(EventType, Enum)


class TestDocEvent:
    def test_construct(self):
        e = DocEvent(
            event_id=1,
            doc_id="d1",
            event_type=EventType.VIEW,
            user_id="u",
            timestamp=10.0,
        )
        assert e.event_id == 1
        assert e.doc_id == "d1"
        assert e.event_type == EventType.VIEW
        assert e.user_id == "u"
        assert e.timestamp == 10.0

    def test_default_user_none(self):
        e = DocEvent(event_id=2, doc_id="d", event_type=EventType.VIEW)
        assert e.user_id is None

    def test_default_metadata_empty(self):
        e = DocEvent(event_id=3, doc_id="d", event_type=EventType.VIEW)
        assert e.metadata == {}

    def test_metadata_independent_instances(self):
        a = DocEvent(event_id=4, doc_id="d", event_type=EventType.VIEW)
        b = DocEvent(event_id=5, doc_id="d", event_type=EventType.VIEW)
        a.metadata["k"] = 1
        assert b.metadata == {}


class TestDocMetricsSnapshot:
    def test_construct(self):
        s = DocMetricsSnapshot(
            doc_id="d",
            view_count=1,
            edit_count=2,
            comment_count=3,
            share_count=4,
            unique_viewers=5,
            unique_editors=6,
        )
        assert s.doc_id == "d"
        assert s.view_count == 1
        assert s.comment_count == 3

    def test_default_last_times(self):
        s = DocMetricsSnapshot(
            doc_id="d",
            view_count=0,
            edit_count=0,
            comment_count=0,
            share_count=0,
            unique_viewers=0,
            unique_editors=0,
        )
        assert s.last_view is None
        assert s.last_edit is None


class TestEngagementScoreDataclass:
    def test_construct(self):
        e = EngagementScore(doc_id="d", score=5.0)
        assert e.doc_id == "d"
        assert e.score == 5.0

    def test_default_weights(self):
        e = EngagementScore(doc_id="d", score=0.0)
        assert e.view_weight == 1.0
        assert e.edit_weight == 5.0
        assert e.comment_weight == 3.0
        assert e.share_weight == 4.0


class TestRecordView:
    def test_record_returns_event(self):
        m = DocMetrics()
        ev = m.record_view("d1", user_id="u1", now=10.0)
        assert isinstance(ev, DocEvent)
        assert ev.event_type == EventType.VIEW
        assert ev.doc_id == "d1"
        assert ev.user_id == "u1"
        assert ev.timestamp == 10.0

    def test_increments_event_id(self):
        m = DocMetrics()
        e1 = m.record_view("d", now=1.0)
        e2 = m.record_view("d", now=2.0)
        assert e2.event_id == e1.event_id + 1

    def test_metadata_stored(self):
        m = DocMetrics()
        ev = m.record_view("d", metadata={"src": "rss"}, now=1.0)
        assert ev.metadata == {"src": "rss"}

    def test_default_now_uses_clock(self):
        m = DocMetrics()
        ev = m.record_view("d")
        assert ev.timestamp > 0


class TestRecordEdit:
    def test_record_edit(self):
        m = DocMetrics()
        ev = m.record_edit("d", user_id="u", now=5.0)
        assert ev.event_type == EventType.EDIT
        assert ev.user_id == "u"


class TestRecordComment:
    def test_record_comment(self):
        m = DocMetrics()
        ev = m.record_comment("d", user_id="u", now=1.0)
        assert ev.event_type == EventType.COMMENT


class TestRecordShare:
    def test_record_share(self):
        m = DocMetrics()
        ev = m.record_share("d", user_id="u", now=1.0)
        assert ev.event_type == EventType.SHARE


class TestRecordEvent:
    def test_generic_record(self):
        m = DocMetrics()
        ev = m.record_event("d", EventType.EXPORT, user_id="u", now=2.0)
        assert ev.event_type == EventType.EXPORT

    def test_download_and_reaction(self):
        m = DocMetrics()
        a = m.record_event("d", EventType.DOWNLOAD, now=1.0)
        b = m.record_event("d", EventType.REACTION, now=2.0)
        assert a.event_type == EventType.DOWNLOAD
        assert b.event_type == EventType.REACTION

    def test_invalid_event_type_raises(self):
        m = DocMetrics()
        with pytest.raises(TypeError):
            m.record_event("d", "not-an-enum")  # type: ignore[arg-type]


class TestEventsForDoc:
    def test_returns_all_for_doc(self):
        m = DocMetrics()
        m.record_view("a", now=1.0)
        m.record_view("b", now=2.0)
        m.record_edit("a", now=3.0)
        assert len(m.events_for_doc("a")) == 2
        assert len(m.events_for_doc("b")) == 1

    def test_filter_by_event_type(self):
        m = DocMetrics()
        m.record_view("a", now=1.0)
        m.record_edit("a", now=2.0)
        assert len(m.events_for_doc("a", event_type=EventType.VIEW)) == 1
        assert len(m.events_for_doc("a", event_type=EventType.EDIT)) == 1

    def test_unknown_doc_empty(self):
        m = DocMetrics()
        assert m.events_for_doc("missing") == []


class TestEventsByUser:
    def test_returns_for_user(self):
        m = DocMetrics()
        m.record_view("d1", user_id="alice", now=1.0)
        m.record_view("d2", user_id="bob", now=2.0)
        m.record_edit("d1", user_id="alice", now=3.0)
        assert len(m.events_by_user("alice")) == 2
        assert len(m.events_by_user("bob")) == 1

    def test_unknown_user(self):
        m = DocMetrics()
        m.record_view("d", user_id="x", now=1.0)
        assert m.events_by_user("ghost") == []


class TestEventsInRange:
    def test_inclusive_bounds(self):
        m = DocMetrics()
        m.record_view("d", now=1.0)
        m.record_view("d", now=5.0)
        m.record_view("d", now=10.0)
        evs = m.events_in_range(1.0, 10.0)
        assert len(evs) == 3

    def test_partial(self):
        m = DocMetrics()
        m.record_view("d", now=1.0)
        m.record_view("d", now=5.0)
        m.record_view("d", now=10.0)
        assert len(m.events_in_range(4.0, 6.0)) == 1

    def test_invalid_range(self):
        m = DocMetrics()
        with pytest.raises(ValueError):
            m.events_in_range(10.0, 1.0)


class TestSnapshot:
    def test_counts(self):
        m = DocMetrics()
        m.record_view("d", user_id="a", now=1.0)
        m.record_view("d", user_id="a", now=2.0)
        m.record_view("d", user_id="b", now=3.0)
        m.record_edit("d", user_id="a", now=4.0)
        m.record_comment("d", user_id="b", now=5.0)
        m.record_share("d", user_id="c", now=6.0)
        s = m.snapshot("d")
        assert s.view_count == 3
        assert s.edit_count == 1
        assert s.comment_count == 1
        assert s.share_count == 1
        assert s.unique_viewers == 2
        assert s.unique_editors == 1

    def test_last_times(self):
        m = DocMetrics()
        m.record_view("d", now=1.0)
        m.record_view("d", now=10.0)
        m.record_edit("d", now=5.0)
        m.record_edit("d", now=7.0)
        s = m.snapshot("d")
        assert s.last_view == 10.0
        assert s.last_edit == 7.0

    def test_empty_doc(self):
        m = DocMetrics()
        s = m.snapshot("missing")
        assert s.view_count == 0
        assert s.last_view is None
        assert s.unique_viewers == 0


class TestViewCount:
    def test_basic(self):
        m = DocMetrics()
        for _ in range(4):
            m.record_view("d", now=1.0)
        assert m.view_count("d") == 4

    def test_since_filter(self):
        m = DocMetrics()
        m.record_view("d", now=1.0)
        m.record_view("d", now=10.0)
        assert m.view_count("d", since=5.0) == 1

    def test_other_docs_ignored(self):
        m = DocMetrics()
        m.record_view("d1", now=1.0)
        m.record_view("d2", now=1.0)
        assert m.view_count("d1") == 1


class TestEditCount:
    def test_basic(self):
        m = DocMetrics()
        m.record_edit("d", now=1.0)
        m.record_edit("d", now=2.0)
        m.record_view("d", now=3.0)
        assert m.edit_count("d") == 2

    def test_since(self):
        m = DocMetrics()
        m.record_edit("d", now=1.0)
        m.record_edit("d", now=10.0)
        assert m.edit_count("d", since=5.0) == 1


class TestUniqueViewers:
    def test_basic(self):
        m = DocMetrics()
        m.record_view("d", user_id="a", now=1.0)
        m.record_view("d", user_id="a", now=2.0)
        m.record_view("d", user_id="b", now=3.0)
        assert m.unique_viewers("d") == {"a", "b"}

    def test_anonymous_excluded(self):
        m = DocMetrics()
        m.record_view("d", user_id=None, now=1.0)
        m.record_view("d", user_id="a", now=2.0)
        assert m.unique_viewers("d") == {"a"}

    def test_since(self):
        m = DocMetrics()
        m.record_view("d", user_id="a", now=1.0)
        m.record_view("d", user_id="b", now=10.0)
        assert m.unique_viewers("d", since=5.0) == {"b"}


class TestUniqueEditors:
    def test_basic(self):
        m = DocMetrics()
        m.record_edit("d", user_id="a", now=1.0)
        m.record_edit("d", user_id="b", now=2.0)
        assert m.unique_editors("d") == {"a", "b"}

    def test_views_not_counted(self):
        m = DocMetrics()
        m.record_view("d", user_id="a", now=1.0)
        assert m.unique_editors("d") == set()


class TestMostViewedDocs:
    def test_ranking(self):
        m = DocMetrics()
        for _ in range(5):
            m.record_view("a", now=1.0)
        for _ in range(2):
            m.record_view("b", now=1.0)
        m.record_view("c", now=1.0)
        top = m.most_viewed_docs(top_k=10)
        assert top[0] == ("a", 5)
        assert top[1] == ("b", 2)
        assert top[2] == ("c", 1)

    def test_top_k_truncates(self):
        m = DocMetrics()
        for d in ("a", "b", "c"):
            m.record_view(d, now=1.0)
        assert len(m.most_viewed_docs(top_k=2)) == 2

    def test_since(self):
        m = DocMetrics()
        m.record_view("a", now=1.0)
        m.record_view("b", now=10.0)
        result = m.most_viewed_docs(since=5.0)
        assert result == [("b", 1)]


class TestMostEditedDocs:
    def test_ranking(self):
        m = DocMetrics()
        for _ in range(3):
            m.record_edit("a", now=1.0)
        m.record_edit("b", now=1.0)
        top = m.most_edited_docs()
        assert top[0] == ("a", 3)

    def test_empty(self):
        m = DocMetrics()
        assert m.most_edited_docs() == []


class TestEngagementScore:
    def test_default_weights(self):
        m = DocMetrics()
        m.record_view("d", now=1.0)  # +1
        m.record_view("d", now=2.0)  # +1
        m.record_edit("d", now=3.0)  # +5
        m.record_comment("d", now=4.0)  # +3
        m.record_share("d", now=5.0)  # +4
        es = m.engagement_score("d")
        assert isinstance(es, EngagementScore)
        assert es.score == 2 * 1.0 + 1 * 5.0 + 1 * 3.0 + 1 * 4.0

    def test_custom_weights(self):
        m = DocMetrics()
        m.record_view("d", now=1.0)
        m.record_edit("d", now=2.0)
        es = m.engagement_score(
            "d", view_weight=2.0, edit_weight=10.0
        )
        assert es.score == 2.0 + 10.0
        assert es.view_weight == 2.0
        assert es.edit_weight == 10.0

    def test_zero_for_missing_doc(self):
        m = DocMetrics()
        assert m.engagement_score("missing").score == 0.0


class TestChurnRate:
    def test_no_views_returns_zero(self):
        m = DocMetrics()
        assert m.churn_rate(0.0, 100.0) == 0.0

    def test_full_retention(self):
        m = DocMetrics()
        m.record_view("a", now=1.0)
        m.record_view("a", now=8.0)
        # midpoint = 5.0; a is in both halves
        assert m.churn_rate(0.0, 10.0) == 0.0

    def test_full_churn(self):
        m = DocMetrics()
        m.record_view("a", now=1.0)
        m.record_view("b", now=8.0)
        # midpoint=5; "a" only in start, "b" only in end -> churn 1.0
        assert m.churn_rate(0.0, 10.0) == 1.0

    def test_invalid_range(self):
        m = DocMetrics()
        with pytest.raises(ValueError):
            m.churn_rate(10.0, 1.0)


class TestRetention:
    def test_no_users_returns_zero(self):
        m = DocMetrics()
        assert m.retention(0.0, 100.0) == 0.0

    def test_full_retention(self):
        m = DocMetrics()
        m.record_view("d", user_id="a", now=1.0)
        m.record_view("d", user_id="a", now=8.0)
        assert m.retention(0.0, 10.0) == 1.0

    def test_zero_retention(self):
        m = DocMetrics()
        m.record_view("d", user_id="a", now=1.0)
        m.record_view("d", user_id="b", now=8.0)
        assert m.retention(0.0, 10.0) == 0.0

    def test_custom_midpoint(self):
        m = DocMetrics()
        m.record_view("d", user_id="a", now=2.0)
        m.record_view("d", user_id="a", now=4.0)
        # with midpoint=3, a appears in both halves
        assert m.retention(0.0, 10.0, midpoint=3.0) == 1.0


class TestTotalEvents:
    def test_increments(self):
        m = DocMetrics()
        assert m.total_events == 0
        m.record_view("d", now=1.0)
        m.record_edit("d", now=2.0)
        assert m.total_events == 2

    def test_capped_by_max_events(self):
        m = DocMetrics(max_events=3)
        for i in range(10):
            m.record_view("d", now=float(i))
        assert m.total_events == 3


class TestClear:
    def test_clears_all(self):
        m = DocMetrics()
        m.record_view("d", now=1.0)
        m.record_edit("d", now=2.0)
        m.clear()
        assert m.total_events == 0
        assert m.events_for_doc("d") == []

    def test_resets_event_id(self):
        m = DocMetrics()
        m.record_view("d", now=1.0)
        m.record_view("d", now=2.0)
        m.clear()
        ev = m.record_view("d", now=3.0)
        assert ev.event_id == 1


class TestEdgeCases:
    def test_max_events_must_be_positive(self):
        with pytest.raises(ValueError):
            DocMetrics(max_events=0)

    def test_concurrent_record(self):
        m = DocMetrics()

        def worker():
            for i in range(100):
                m.record_view("d", user_id="u", now=float(i))

        threads = [threading.Thread(target=worker) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert m.total_events == 500

    def test_metadata_copied(self):
        m = DocMetrics()
        meta = {"k": "v"}
        ev = m.record_view("d", metadata=meta, now=1.0)
        meta["k"] = "changed"
        assert ev.metadata["k"] == "v"

    def test_fifo_eviction_keeps_newest(self):
        m = DocMetrics(max_events=2)
        m.record_view("d", now=1.0)
        m.record_view("d", now=2.0)
        m.record_view("d", now=3.0)
        evs = m.events_for_doc("d")
        timestamps = sorted(e.timestamp for e in evs)
        assert timestamps == [2.0, 3.0]

    def test_top_k_zero(self):
        m = DocMetrics()
        m.record_view("a", now=1.0)
        assert m.most_viewed_docs(top_k=0) == []

    def test_top_k_negative_raises(self):
        m = DocMetrics()
        with pytest.raises(ValueError):
            m.most_viewed_docs(top_k=-1)
