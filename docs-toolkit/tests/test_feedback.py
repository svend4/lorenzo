"""Тесты feedback store + Wilson quality score."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.feedback import FeedbackStore, Feedback


@pytest.fixture
def store(tmp_path):
    db = tmp_path / "fb.sqlite"
    s = FeedbackStore(db_path=db)
    yield s
    s.close()


def test_feedback_dataclass_auto_id_ts():
    fb = Feedback(request="q", response_text="a")
    assert fb.id  # auto-generated hex
    assert len(fb.id) == 12
    assert fb.ts  # auto ISO timestamp


def test_feedback_explicit_values_kept():
    fb = Feedback(id="abc", ts="2026-01-01T00:00:00",
                  request="q", thumbs="up")
    assert fb.id == "abc"
    assert fb.ts == "2026-01-01T00:00:00"
    assert fb.thumbs == "up"


def test_record_and_get(store):
    fb = Feedback(request="?", response_text="!", thumbs="up", skill="rag")
    fb_id = store.record(fb)
    got = store.get(fb_id)
    assert got is not None
    assert got.request == "?"
    assert got.thumbs == "up"
    assert got.skill == "rag"


def test_get_missing_returns_none(store):
    assert store.get("nonexistent") is None


def test_list_recent_orders_by_ts_desc(store):
    store.record(Feedback(request="a", ts="2026-01-01T00:00:00"))
    store.record(Feedback(request="b", ts="2026-01-02T00:00:00"))
    store.record(Feedback(request="c", ts="2026-01-03T00:00:00"))
    items = store.list_recent(limit=10)
    assert len(items) == 3
    assert items[0].request == "c"
    assert items[2].request == "a"


def test_list_recent_filter_by_skill(store):
    store.record(Feedback(request="x", skill="rag"))
    store.record(Feedback(request="y", skill="search"))
    rag = store.list_recent(skill="rag")
    assert len(rag) == 1
    assert rag[0].skill == "rag"


def test_list_recent_filter_by_thumbs(store):
    store.record(Feedback(request="x", thumbs="up"))
    store.record(Feedback(request="y", thumbs="down"))
    ups = store.list_recent(thumbs="up")
    assert len(ups) == 1
    assert ups[0].thumbs == "up"


def test_aggregate_per_skill(store):
    store.record(Feedback(skill="rag", thumbs="up", duration_ms=100, cost=0.01))
    store.record(Feedback(skill="rag", thumbs="up", duration_ms=200, cost=0.02))
    store.record(Feedback(skill="rag", thumbs="down", duration_ms=300))
    store.record(Feedback(skill="search", thumbs="up"))
    agg = store.aggregate_per_skill()
    assert "rag" in agg
    assert agg["rag"]["total"] == 3
    assert agg["rag"]["up"] == 2
    assert agg["rag"]["down"] == 1
    assert agg["rag"]["total_cost"] == pytest.approx(0.03)
    assert "search" in agg
    assert agg["search"]["total"] == 1
    assert "quality_score" in agg["rag"]


def test_quality_score_zero_when_empty(store):
    assert store.quality_score() == 0.0


def test_quality_score_increases_with_more_ups(store):
    # 1 up, 0 down: lower bound is small
    store.record(Feedback(thumbs="up"))
    q1 = store.quality_score()
    # 9 more ups, no down: should grow
    for _ in range(9):
        store.record(Feedback(thumbs="up"))
    q2 = store.quality_score()
    assert q2 > q1


def test_quality_score_decreases_with_downs(store):
    for _ in range(10):
        store.record(Feedback(thumbs="up"))
    q_pure = store.quality_score()
    for _ in range(5):
        store.record(Feedback(thumbs="down"))
    q_mixed = store.quality_score()
    assert q_mixed < q_pure


def test_calc_quality_zero_total():
    assert FeedbackStore._calc_quality(0, 0, 0) == 0.0


def test_calc_quality_no_signal_returns_50():
    # total > 0 but n=0 (no thumbs) — but в коде total == n всегда; смотрим контракт
    # _calc_quality(0, 0, total>0) → n=0 → returns 50.0
    assert FeedbackStore._calc_quality(0, 0, 5) == 50.0


def test_calc_quality_all_ups_high():
    # 10 ups, 0 downs → высокий, но не 100 (Wilson lower)
    q = FeedbackStore._calc_quality(10, 0, 10)
    assert 50.0 < q < 100.0


def test_calc_quality_all_downs_zero():
    q = FeedbackStore._calc_quality(0, 10, 10)
    assert q == 0.0  # max(0, lower) clipped


def test_record_with_citations(store):
    fb = Feedback(request="?",
                  citations=[{"n": 1, "doc_id": "d1", "title": "X"}])
    fb_id = store.record(fb)
    got = store.get(fb_id)
    assert len(got.citations) == 1
    assert got.citations[0]["doc_id"] == "d1"


def test_record_truncates_long_request(store):
    long_q = "x" * 1000
    fb = Feedback(request=long_q)
    fb_id = store.record(fb)
    got = store.get(fb_id)
    assert len(got.request) <= 500
