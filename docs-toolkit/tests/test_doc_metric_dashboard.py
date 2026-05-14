"""Tests for E382 DocMetricDashboard."""
from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_metric_dashboard import (
    DashboardSnapshot,
    DashboardStats,
    DocMetricDashboard,
    MetricCard,
)


# --------------------------------------------------------------------- helpers


def _seed(dash: DocMetricDashboard) -> None:
    dash.set_card("docs", "Total Docs", 100.0, unit="files", now=100.0)
    dash.set_card("words", "Total Words", 5000.0, unit="words", now=100.0)
    dash.set_card("readability", "Readability", 65.0, unit="score", now=100.0)


# ============================================================ dataclass tests


class TestMetricCardDataclass:
    def test_basic_construction(self) -> None:
        c = MetricCard(card_id="a", title="A", value=1.5)
        assert c.card_id == "a"
        assert c.title == "A"
        assert c.value == 1.5
        assert c.unit == ""
        assert c.trend == "flat"
        assert c.updated_at == 0.0

    def test_full_construction(self) -> None:
        c = MetricCard(
            card_id="b",
            title="B",
            value=2.0,
            unit="kg",
            trend="up",
            updated_at=42.0,
        )
        assert c.unit == "kg"
        assert c.trend == "up"
        assert c.updated_at == 42.0

    def test_equality(self) -> None:
        a = MetricCard(card_id="x", title="X", value=1.0)
        b = MetricCard(card_id="x", title="X", value=1.0)
        assert a == b

    def test_inequality_on_value(self) -> None:
        a = MetricCard(card_id="x", title="X", value=1.0)
        b = MetricCard(card_id="x", title="X", value=2.0)
        assert a != b


class TestDashboardSnapshotDataclass:
    def test_construction(self) -> None:
        s = DashboardSnapshot(snapshot_id="sid", created_at=10.0)
        assert s.snapshot_id == "sid"
        assert s.created_at == 10.0
        assert s.cards == {}

    def test_with_cards(self) -> None:
        s = DashboardSnapshot(
            snapshot_id="sid",
            created_at=5.0,
            cards={"a": 1.0, "b": 2.0},
        )
        assert s.cards == {"a": 1.0, "b": 2.0}

    def test_default_cards_independent(self) -> None:
        a = DashboardSnapshot(snapshot_id="a")
        b = DashboardSnapshot(snapshot_id="b")
        a.cards["x"] = 1.0
        assert b.cards == {}


class TestDashboardStatsDataclass:
    def test_construction(self) -> None:
        s = DashboardStats(
            total_cards=3,
            total_snapshots=2,
            cards_up=1,
            cards_down=1,
            cards_flat=1,
        )
        assert s.total_cards == 3
        assert s.total_snapshots == 2
        assert s.cards_up == 1
        assert s.cards_down == 1
        assert s.cards_flat == 1

    def test_equality(self) -> None:
        a = DashboardStats(0, 0, 0, 0, 0)
        b = DashboardStats(0, 0, 0, 0, 0)
        assert a == b


# ================================================================ construction


class TestConstruction:
    def test_default_empty(self) -> None:
        d = DocMetricDashboard()
        assert d.list_cards() == []
        assert d.list_snapshots() == []

    def test_initial_stats(self) -> None:
        d = DocMetricDashboard()
        s = d.stats()
        assert s.total_cards == 0
        assert s.total_snapshots == 0
        assert s.cards_up == 0
        assert s.cards_down == 0
        assert s.cards_flat == 0

    def test_independent_state(self) -> None:
        a = DocMetricDashboard()
        b = DocMetricDashboard()
        a.set_card("x", "X", 1.0)
        assert b.list_cards() == []


# ===================================================================== set_card


class TestSetCard:
    def test_creates_new_card(self) -> None:
        d = DocMetricDashboard()
        c = d.set_card("a", "Alpha", 10.0, unit="px", now=100.0)
        assert isinstance(c, MetricCard)
        assert c.card_id == "a"
        assert c.title == "Alpha"
        assert c.value == 10.0
        assert c.unit == "px"
        assert c.updated_at == 100.0

    def test_new_card_trend_flat(self) -> None:
        d = DocMetricDashboard()
        c = d.set_card("a", "Alpha", 10.0)
        assert c.trend == "flat"

    def test_update_existing_value(self) -> None:
        d = DocMetricDashboard()
        d.set_card("a", "Alpha", 10.0, now=100.0)
        c2 = d.set_card("a", "Alpha", 20.0, now=200.0)
        assert c2.value == 20.0
        assert c2.updated_at == 200.0

    def test_trend_up(self) -> None:
        d = DocMetricDashboard()
        d.set_card("a", "Alpha", 10.0)
        c = d.set_card("a", "Alpha", 15.0)
        assert c.trend == "up"

    def test_trend_down(self) -> None:
        d = DocMetricDashboard()
        d.set_card("a", "Alpha", 10.0)
        c = d.set_card("a", "Alpha", 5.0)
        assert c.trend == "down"

    def test_trend_flat_on_equal(self) -> None:
        d = DocMetricDashboard()
        d.set_card("a", "Alpha", 10.0)
        c = d.set_card("a", "Alpha", 10.0)
        assert c.trend == "flat"

    def test_value_coerced_to_float(self) -> None:
        d = DocMetricDashboard()
        c = d.set_card("a", "Alpha", 7)
        assert isinstance(c.value, float)
        assert c.value == 7.0

    def test_history_appended(self) -> None:
        d = DocMetricDashboard()
        d.set_card("a", "Alpha", 1.0)
        d.set_card("a", "Alpha", 2.0)
        d.set_card("a", "Alpha", 3.0)
        h = d.history_for("a")
        assert h == [3.0, 2.0, 1.0]

    def test_uses_default_now(self) -> None:
        d = DocMetricDashboard()
        c = d.set_card("a", "Alpha", 1.0)
        assert c.updated_at > 0.0

    def test_title_can_change_on_update(self) -> None:
        d = DocMetricDashboard()
        d.set_card("a", "Old", 1.0)
        c = d.set_card("a", "New", 1.0)
        assert c.title == "New"


# =================================================================== remove_card


class TestRemoveCard:
    def test_returns_true_when_present(self) -> None:
        d = DocMetricDashboard()
        d.set_card("a", "A", 1.0)
        assert d.remove_card("a") is True

    def test_returns_false_when_missing(self) -> None:
        d = DocMetricDashboard()
        assert d.remove_card("nope") is False

    def test_card_gone_after_remove(self) -> None:
        d = DocMetricDashboard()
        d.set_card("a", "A", 1.0)
        d.remove_card("a")
        assert d.get_card("a") is None

    def test_history_also_removed(self) -> None:
        d = DocMetricDashboard()
        d.set_card("a", "A", 1.0)
        d.set_card("a", "A", 2.0)
        d.remove_card("a")
        assert d.history_for("a") == []


# ====================================================================== get_card


class TestGetCard:
    def test_returns_card(self) -> None:
        d = DocMetricDashboard()
        d.set_card("a", "Alpha", 1.0)
        c = d.get_card("a")
        assert c is not None
        assert c.card_id == "a"

    def test_returns_none_when_missing(self) -> None:
        d = DocMetricDashboard()
        assert d.get_card("nope") is None

    def test_reflects_latest_value(self) -> None:
        d = DocMetricDashboard()
        d.set_card("a", "A", 1.0)
        d.set_card("a", "A", 2.0)
        assert d.get_card("a").value == 2.0


# ==================================================================== list_cards


class TestListCards:
    def test_empty(self) -> None:
        d = DocMetricDashboard()
        assert d.list_cards() == []

    def test_sorted_by_card_id(self) -> None:
        d = DocMetricDashboard()
        d.set_card("c", "C", 3.0)
        d.set_card("a", "A", 1.0)
        d.set_card("b", "B", 2.0)
        ids = [c.card_id for c in d.list_cards()]
        assert ids == ["a", "b", "c"]

    def test_returns_list_copy_safe(self) -> None:
        d = DocMetricDashboard()
        d.set_card("a", "A", 1.0)
        lst = d.list_cards()
        lst.clear()
        assert len(d.list_cards()) == 1


# ================================================================ take_snapshot


class TestTakeSnapshot:
    def test_captures_values(self) -> None:
        d = DocMetricDashboard()
        _seed(d)
        s = d.take_snapshot(now=500.0)
        assert s.cards == {"docs": 100.0, "words": 5000.0, "readability": 65.0}

    def test_unique_id_per_snapshot(self) -> None:
        d = DocMetricDashboard()
        s1 = d.take_snapshot()
        s2 = d.take_snapshot()
        assert s1.snapshot_id != s2.snapshot_id

    def test_uses_explicit_now(self) -> None:
        d = DocMetricDashboard()
        s = d.take_snapshot(now=999.0)
        assert s.created_at == 999.0

    def test_uses_default_now(self) -> None:
        d = DocMetricDashboard()
        s = d.take_snapshot()
        assert s.created_at > 0.0

    def test_empty_dashboard_snapshot(self) -> None:
        d = DocMetricDashboard()
        s = d.take_snapshot(now=1.0)
        assert s.cards == {}

    def test_snapshot_isolated_from_later_updates(self) -> None:
        d = DocMetricDashboard()
        d.set_card("a", "A", 10.0)
        s = d.take_snapshot(now=1.0)
        d.set_card("a", "A", 20.0)
        assert s.cards == {"a": 10.0}


# ================================================================= get_snapshot


class TestGetSnapshot:
    def test_returns_snapshot(self) -> None:
        d = DocMetricDashboard()
        s = d.take_snapshot(now=1.0)
        got = d.get_snapshot(s.snapshot_id)
        assert got is not None
        assert got.snapshot_id == s.snapshot_id

    def test_returns_none_when_missing(self) -> None:
        d = DocMetricDashboard()
        assert d.get_snapshot("nope") is None


# =============================================================== list_snapshots


class TestListSnapshots:
    def test_empty(self) -> None:
        d = DocMetricDashboard()
        assert d.list_snapshots() == []

    def test_sorted_desc_by_created_at(self) -> None:
        d = DocMetricDashboard()
        d.take_snapshot(now=100.0)
        d.take_snapshot(now=300.0)
        d.take_snapshot(now=200.0)
        ts = [s.created_at for s in d.list_snapshots()]
        assert ts == [300.0, 200.0, 100.0]


# =================================================================== history_for


class TestHistoryFor:
    def test_empty_when_no_card(self) -> None:
        d = DocMetricDashboard()
        assert d.history_for("nope") == []

    def test_most_recent_first(self) -> None:
        d = DocMetricDashboard()
        d.set_card("a", "A", 1.0)
        d.set_card("a", "A", 2.0)
        d.set_card("a", "A", 3.0)
        assert d.history_for("a") == [3.0, 2.0, 1.0]

    def test_limit_truncates(self) -> None:
        d = DocMetricDashboard()
        for v in [1.0, 2.0, 3.0, 4.0, 5.0]:
            d.set_card("a", "A", v)
        assert d.history_for("a", limit=2) == [5.0, 4.0]

    def test_limit_zero(self) -> None:
        d = DocMetricDashboard()
        d.set_card("a", "A", 1.0)
        assert d.history_for("a", limit=0) == []

    def test_negative_limit_raises(self) -> None:
        d = DocMetricDashboard()
        d.set_card("a", "A", 1.0)
        with pytest.raises(ValueError):
            d.history_for("a", limit=-1)

    def test_limit_exceeding_returns_all(self) -> None:
        d = DocMetricDashboard()
        d.set_card("a", "A", 1.0)
        d.set_card("a", "A", 2.0)
        assert d.history_for("a", limit=99) == [2.0, 1.0]


# ================================================================ cards_by_trend


class TestCardsByTrend:
    def test_filters_by_up(self) -> None:
        d = DocMetricDashboard()
        d.set_card("a", "A", 1.0)
        d.set_card("a", "A", 2.0)  # up
        d.set_card("b", "B", 5.0)
        d.set_card("b", "B", 3.0)  # down
        d.set_card("c", "C", 10.0)  # flat (new)
        up = d.cards_by_trend("up")
        assert [c.card_id for c in up] == ["a"]

    def test_filters_by_down(self) -> None:
        d = DocMetricDashboard()
        d.set_card("a", "A", 1.0)
        d.set_card("a", "A", 0.5)  # down
        d.set_card("b", "B", 1.0)
        d.set_card("b", "B", 0.1)  # down
        down = d.cards_by_trend("down")
        assert [c.card_id for c in down] == ["a", "b"]

    def test_filters_by_flat(self) -> None:
        d = DocMetricDashboard()
        d.set_card("a", "A", 1.0)  # flat
        d.set_card("b", "B", 1.0)
        d.set_card("b", "B", 2.0)  # up
        flat = d.cards_by_trend("flat")
        assert [c.card_id for c in flat] == ["a"]

    def test_unknown_trend_returns_empty(self) -> None:
        d = DocMetricDashboard()
        d.set_card("a", "A", 1.0)
        assert d.cards_by_trend("sideways") == []

    def test_results_sorted(self) -> None:
        d = DocMetricDashboard()
        d.set_card("z", "Z", 1.0)
        d.set_card("a", "A", 1.0)
        d.set_card("m", "M", 1.0)
        flat = d.cards_by_trend("flat")
        assert [c.card_id for c in flat] == ["a", "m", "z"]


# ================================================================= clear_history


class TestClearHistory:
    def test_returns_count_cleared(self) -> None:
        d = DocMetricDashboard()
        d.set_card("a", "A", 1.0)
        d.set_card("a", "A", 2.0)
        d.set_card("a", "A", 3.0)
        assert d.clear_history("a") == 3

    def test_returns_zero_when_no_history(self) -> None:
        d = DocMetricDashboard()
        assert d.clear_history("nope") == 0

    def test_history_empty_after_clear(self) -> None:
        d = DocMetricDashboard()
        d.set_card("a", "A", 1.0)
        d.set_card("a", "A", 2.0)
        d.clear_history("a")
        assert d.history_for("a") == []

    def test_card_preserved_after_clear(self) -> None:
        d = DocMetricDashboard()
        d.set_card("a", "A", 5.0)
        d.clear_history("a")
        c = d.get_card("a")
        assert c is not None
        assert c.value == 5.0


# =============================================================== delete_snapshot


class TestDeleteSnapshot:
    def test_returns_true_when_present(self) -> None:
        d = DocMetricDashboard()
        s = d.take_snapshot()
        assert d.delete_snapshot(s.snapshot_id) is True

    def test_returns_false_when_missing(self) -> None:
        d = DocMetricDashboard()
        assert d.delete_snapshot("nope") is False

    def test_snapshot_gone_after_delete(self) -> None:
        d = DocMetricDashboard()
        s = d.take_snapshot()
        d.delete_snapshot(s.snapshot_id)
        assert d.get_snapshot(s.snapshot_id) is None


# ========================================================================= stats


class TestStats:
    def test_empty(self) -> None:
        d = DocMetricDashboard()
        s = d.stats()
        assert s == DashboardStats(0, 0, 0, 0, 0)

    def test_counts_cards(self) -> None:
        d = DocMetricDashboard()
        _seed(d)
        s = d.stats()
        assert s.total_cards == 3

    def test_counts_snapshots(self) -> None:
        d = DocMetricDashboard()
        d.take_snapshot()
        d.take_snapshot()
        s = d.stats()
        assert s.total_snapshots == 2

    def test_counts_trends(self) -> None:
        d = DocMetricDashboard()
        d.set_card("a", "A", 1.0)
        d.set_card("a", "A", 2.0)  # up
        d.set_card("b", "B", 5.0)
        d.set_card("b", "B", 3.0)  # down
        d.set_card("c", "C", 10.0)  # flat
        d.set_card("e", "E", 7.0)  # flat
        s = d.stats()
        assert s.cards_up == 1
        assert s.cards_down == 1
        assert s.cards_flat == 2

    def test_returns_dataclass_instance(self) -> None:
        d = DocMetricDashboard()
        assert isinstance(d.stats(), DashboardStats)


# ================================================================ thread safety


class TestThreadSafety:
    def test_concurrent_set_card(self) -> None:
        d = DocMetricDashboard()

        def worker(prefix: str) -> None:
            for i in range(50):
                d.set_card(f"{prefix}-{i}", f"T{prefix}{i}", float(i))

        threads = [
            threading.Thread(target=worker, args=(letter,))
            for letter in "abcd"
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert len(d.list_cards()) == 4 * 50

    def test_concurrent_updates_same_card(self) -> None:
        d = DocMetricDashboard()

        def worker(offset: float) -> None:
            for i in range(100):
                d.set_card("shared", "Shared", offset + i)

        threads = [
            threading.Thread(target=worker, args=(float(k * 1000),))
            for k in range(4)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        h = d.history_for("shared")
        assert len(h) == 400
        # Current card value should equal the most recent history value
        c = d.get_card("shared")
        assert c is not None
        assert c.value == h[0]

    def test_concurrent_snapshots(self) -> None:
        d = DocMetricDashboard()
        d.set_card("a", "A", 1.0)

        def worker() -> None:
            for _ in range(25):
                d.take_snapshot()

        threads = [threading.Thread(target=worker) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert len(d.list_snapshots()) == 100
