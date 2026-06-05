"""Tests for M6 Active Learning Queue (25+ tests).

Covers:
- LearningItem dataclass auto-fields
- LearningQueue: add / get / list_pending (priority ordering)
- LearningQueue: label / skip status changes
- LearningQueue: export_golden writes valid YAML
- LearningQueue: stats breakdown by status and reason
- LowConfidenceTrigger: fires below threshold, silent above
- DownThumbTrigger: fires on down, silent on up
- GoldenMismatchTrigger: fires on Jaccard match with wrong top-1
- CompositeTrigger: fires if any fires, uses max priority
- auto_enqueue: returns item_id when triggered, None when not
"""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.active_learning import (
    LearningItem,
    LearningQueue,
    LowConfidenceTrigger,
    DownThumbTrigger,
    GoldenMismatchTrigger,
    CompositeTrigger,
    auto_enqueue,
)
from docstoolkit.rag.types import Passage


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def queue(tmp_path):
    db = tmp_path / "al_test.sqlite"
    q = LearningQueue(db_path=db)
    yield q
    q.close()


def make_passage(doc_id: str = "doc1", score: float = 0.5, text: str = "some text") -> Passage:
    return Passage(text=text, doc_id=doc_id, score=score)


def make_item(
    query: str = "test query",
    priority: float = 0.5,
    reason: str = "low_confidence",
    status: str = "pending",
) -> LearningItem:
    return LearningItem(
        id="",
        query=query,
        passages_json=json.dumps([]),
        suggested_answer="",
        priority=priority,
        reason=reason,
        status=status,
    )


# ---------------------------------------------------------------------------
# LearningItem dataclass
# ---------------------------------------------------------------------------

def test_learning_item_auto_id():
    item = make_item()
    assert item.id  # auto-generated via __post_init__
    assert len(item.id) == 16


def test_learning_item_auto_created_ts():
    item = make_item()
    assert item.created_ts  # set in __post_init__
    assert "T" in item.created_ts  # ISO format has 'T'


def test_learning_item_explicit_id_preserved():
    item = LearningItem(
        id="myid",
        query="q",
        passages_json="[]",
        suggested_answer="",
        priority=0.7,
        reason="manual",
        created_ts="2026-01-01T00:00:00",
    )
    assert item.id == "myid"
    assert item.created_ts == "2026-01-01T00:00:00"


def test_learning_item_default_status_pending():
    item = make_item()
    assert item.status == "pending"


def test_learning_item_passages_property():
    passages_data = [{"text": "hello", "doc_id": "doc1", "score": 0.9}]
    item = LearningItem(
        id="x",
        query="q",
        passages_json=json.dumps(passages_data),
        suggested_answer="",
        priority=0.5,
        reason="manual",
        created_ts="2026-01-01T00:00:00",
    )
    assert item.passages == passages_data


def test_learning_item_passages_property_invalid_json():
    item = LearningItem(
        id="x",
        query="q",
        passages_json="NOT JSON",
        suggested_answer="",
        priority=0.5,
        reason="manual",
        created_ts="2026-01-01T00:00:00",
    )
    assert item.passages == []


# ---------------------------------------------------------------------------
# LearningQueue: add / get
# ---------------------------------------------------------------------------

def test_queue_add_returns_id(queue):
    item = make_item("what is RAG?")
    returned_id = queue.add(item)
    assert returned_id == item.id


def test_queue_get_returns_item(queue):
    item = make_item("what is RAG?", priority=0.7)
    queue.add(item)
    got = queue.get(item.id)
    assert got is not None
    assert got.query == "what is RAG?"
    assert got.priority == pytest.approx(0.7)
    assert got.reason == "low_confidence"


def test_queue_get_missing_returns_none(queue):
    assert queue.get("nonexistent_id") is None


# ---------------------------------------------------------------------------
# LearningQueue: list_pending ordering
# ---------------------------------------------------------------------------

def test_queue_list_pending_priority_descending(queue):
    queue.add(make_item("low", priority=0.2))
    queue.add(make_item("high", priority=0.9))
    queue.add(make_item("mid", priority=0.5))
    items = queue.list_pending()
    assert len(items) == 3
    assert items[0].query == "high"
    assert items[1].query == "mid"
    assert items[2].query == "low"


def test_queue_list_pending_limit(queue):
    for i in range(10):
        queue.add(make_item(f"query {i}", priority=float(i) / 10))
    items = queue.list_pending(limit=3)
    assert len(items) == 3
    # Top 3 priorities: 0.9, 0.8, 0.7
    assert items[0].priority == pytest.approx(0.9)


def test_queue_list_pending_excludes_labelled(queue):
    item = make_item("labelled query")
    queue.add(item)
    queue.label(item.id, ["doc1"])
    pending = queue.list_pending()
    assert all(i.id != item.id for i in pending)


def test_queue_list_pending_excludes_skipped(queue):
    item = make_item("skipped query")
    queue.add(item)
    queue.skip(item.id)
    pending = queue.list_pending()
    assert all(i.id != item.id for i in pending)


# ---------------------------------------------------------------------------
# LearningQueue: label / skip
# ---------------------------------------------------------------------------

def test_queue_label_changes_status(queue):
    item = make_item("to label")
    queue.add(item)
    queue.label(item.id, ["doc1", "doc2"], labelled_by="tester")
    got = queue.get(item.id)
    assert got.status == "labelled"
    assert got.labelled_by == "tester"
    assert "doc1" in got.golden_doc_ids
    assert "doc2" in got.golden_doc_ids
    assert got.label_ts  # timestamp set


def test_queue_label_default_labelled_by(queue):
    item = make_item("auto label")
    queue.add(item)
    queue.label(item.id, [])
    got = queue.get(item.id)
    assert got.labelled_by == "human"


def test_queue_skip_changes_status(queue):
    item = make_item("to skip")
    queue.add(item)
    queue.skip(item.id)
    got = queue.get(item.id)
    assert got.status == "skipped"


# ---------------------------------------------------------------------------
# LearningQueue: export_golden
# ---------------------------------------------------------------------------

def test_queue_export_golden_writes_yaml(queue, tmp_path):
    item = make_item("what is RAG?", reason="manual")
    queue.add(item)
    queue.label(item.id, ["doc1.md"], labelled_by="human")

    out_path = tmp_path / "golden.yaml"
    count = queue.export_golden(out_path)
    assert count == 1
    assert out_path.exists()

    content = out_path.read_text(encoding="utf-8")
    assert "what is RAG?" in content
    assert "doc1.md" in content
    assert "golden_doc_ids" in content
    assert "items:" in content


def test_queue_export_golden_only_labelled(queue, tmp_path):
    item1 = make_item("labelled query")
    item2 = make_item("pending query")
    queue.add(item1)
    queue.add(item2)
    queue.label(item1.id, ["doc_a"])

    out_path = tmp_path / "golden2.yaml"
    count = queue.export_golden(out_path)
    assert count == 1

    content = out_path.read_text(encoding="utf-8")
    assert "labelled query" in content
    assert "pending query" not in content


def test_queue_export_golden_empty(queue, tmp_path):
    out_path = tmp_path / "golden_empty.yaml"
    count = queue.export_golden(out_path)
    assert count == 0
    content = out_path.read_text(encoding="utf-8")
    assert "items:" in content


# ---------------------------------------------------------------------------
# LearningQueue: stats
# ---------------------------------------------------------------------------

def test_queue_stats_empty(queue):
    s = queue.stats()
    assert s["total"] == 0
    assert s["by_reason"] == {}


def test_queue_stats_counts_by_status(queue):
    queue.add(make_item("p1", reason="low_confidence"))
    item2 = make_item("p2", reason="down_thumb")
    queue.add(item2)
    queue.label(item2.id, [])
    item3 = make_item("p3", reason="manual")
    queue.add(item3)
    queue.skip(item3.id)

    s = queue.stats()
    assert s["total"] == 3
    assert s.get("pending", 0) == 1
    assert s.get("labelled", 0) == 1
    assert s.get("skipped", 0) == 1


def test_queue_stats_by_reason(queue):
    queue.add(make_item("a", reason="low_confidence"))
    queue.add(make_item("b", reason="low_confidence"))
    queue.add(make_item("c", reason="down_thumb"))

    s = queue.stats()
    assert s["by_reason"]["low_confidence"] == 2
    assert s["by_reason"]["down_thumb"] == 1


# ---------------------------------------------------------------------------
# LowConfidenceTrigger
# ---------------------------------------------------------------------------

def test_low_confidence_fires_below_threshold():
    trigger = LowConfidenceTrigger(threshold=0.4)
    passages = [make_passage(score=0.2)]
    should, priority, reason = trigger.should_queue("q", passages, {})
    assert should is True
    assert reason == "low_confidence"
    assert priority == pytest.approx(1.0 - 0.2)


def test_low_confidence_fires_at_zero():
    trigger = LowConfidenceTrigger(threshold=0.4)
    passages = [make_passage(score=0.0)]
    should, priority, reason = trigger.should_queue("q", passages, {})
    assert should is True
    assert priority == pytest.approx(1.0)


def test_low_confidence_silent_above_threshold():
    trigger = LowConfidenceTrigger(threshold=0.4)
    passages = [make_passage(score=0.8)]
    should, priority, reason = trigger.should_queue("q", passages, {})
    assert should is False


def test_low_confidence_fires_on_empty_passages():
    trigger = LowConfidenceTrigger(threshold=0.4)
    should, priority, reason = trigger.should_queue("q", [], {})
    assert should is True
    assert priority == pytest.approx(1.0)


def test_low_confidence_uses_max_score():
    trigger = LowConfidenceTrigger(threshold=0.4)
    passages = [make_passage(score=0.1), make_passage(score=0.5)]
    should, _, _ = trigger.should_queue("q", passages, {})
    assert should is False  # max score 0.5 >= 0.4


# ---------------------------------------------------------------------------
# DownThumbTrigger
# ---------------------------------------------------------------------------

def test_down_thumb_fires_on_down():
    trigger = DownThumbTrigger()
    should, priority, reason = trigger.should_queue("q", [], {"thumbs": "down"})
    assert should is True
    assert priority == pytest.approx(0.8)
    assert reason == "down_thumb"


def test_down_thumb_silent_on_up():
    trigger = DownThumbTrigger()
    should, _, _ = trigger.should_queue("q", [], {"thumbs": "up"})
    assert should is False


def test_down_thumb_silent_on_missing_key():
    trigger = DownThumbTrigger()
    should, _, _ = trigger.should_queue("q", [], {})
    assert should is False


def test_down_thumb_silent_on_neutral():
    trigger = DownThumbTrigger()
    should, _, _ = trigger.should_queue("q", [], {"thumbs": "neutral"})
    assert should is False


# ---------------------------------------------------------------------------
# GoldenMismatchTrigger
# ---------------------------------------------------------------------------

def test_golden_mismatch_fires_on_similar_query_wrong_doc():
    golden = {"what is rag retrieval": ["correct_doc"]}
    trigger = GoldenMismatchTrigger(golden)
    # Similar query (Jaccard > 0.6), wrong top-1
    passages = [make_passage(doc_id="wrong_doc", score=0.9)]
    should, priority, reason = trigger.should_queue(
        "what is rag retrieval augmented", passages, {}
    )
    assert should is True
    assert priority == pytest.approx(0.9)
    assert reason == "golden_mismatch"


def test_golden_mismatch_silent_on_correct_doc():
    golden = {"what is rag retrieval": ["correct_doc"]}
    trigger = GoldenMismatchTrigger(golden)
    passages = [make_passage(doc_id="correct_doc", score=0.9)]
    should, _, _ = trigger.should_queue("what is rag retrieval", passages, {})
    assert should is False


def test_golden_mismatch_silent_on_dissimilar_query():
    golden = {"what is rag retrieval": ["correct_doc"]}
    trigger = GoldenMismatchTrigger(golden)
    passages = [make_passage(doc_id="wrong_doc", score=0.9)]
    should, _, _ = trigger.should_queue(
        "completely different topic about weather forecasting", passages, {}
    )
    assert should is False


def test_golden_mismatch_accepts_set_of_queries():
    """set[str] form (backward compat): fires when similar query found."""
    trigger = GoldenMismatchTrigger({"what is rag retrieval"})
    passages = [make_passage(doc_id="any_doc", score=0.9)]
    should, _, _ = trigger.should_queue("what is rag retrieval", passages, {})
    # No expected docs → fires anyway (spec: if not expected_docs, treat as hit)
    assert should is True


# ---------------------------------------------------------------------------
# CompositeTrigger
# ---------------------------------------------------------------------------

def test_composite_fires_if_any_fires():
    low_conf = LowConfidenceTrigger(threshold=0.4)
    down_thumb = DownThumbTrigger()
    composite = CompositeTrigger([low_conf, down_thumb])
    # Only down_thumb fires (score is high)
    passages = [make_passage(score=0.9)]
    should, _, reason = composite.should_queue("q", passages, {"thumbs": "down"})
    assert should is True
    assert reason == "down_thumb"


def test_composite_silent_when_none_fires():
    low_conf = LowConfidenceTrigger(threshold=0.4)
    down_thumb = DownThumbTrigger()
    composite = CompositeTrigger([low_conf, down_thumb])
    passages = [make_passage(score=0.9)]
    should, _, _ = composite.should_queue("q", passages, {"thumbs": "up"})
    assert should is False


def test_composite_uses_max_priority():
    low_conf = LowConfidenceTrigger(threshold=0.4)  # priority = 1.0 - score
    down_thumb = DownThumbTrigger()  # priority = 0.8
    composite = CompositeTrigger([low_conf, down_thumb])
    # Both fire: low_conf with score 0.1 → priority 0.9, down_thumb → 0.8
    passages = [make_passage(score=0.1)]
    should, priority, _ = composite.should_queue("q", passages, {"thumbs": "down"})
    assert should is True
    assert priority == pytest.approx(0.9)


def test_composite_empty_triggers_never_fires():
    composite = CompositeTrigger([])
    should, _, _ = composite.should_queue("q", [], {})
    assert should is False


# ---------------------------------------------------------------------------
# auto_enqueue
# ---------------------------------------------------------------------------

def test_auto_enqueue_returns_id_when_triggered(queue):
    trigger = LowConfidenceTrigger(threshold=0.4)
    passages = [make_passage(score=0.1)]
    item_id = auto_enqueue("what is RAG?", passages, queue, trigger)
    assert item_id is not None
    assert len(item_id) == 16
    # Verify it's actually in the queue
    stored = queue.get(item_id)
    assert stored is not None
    assert stored.query == "what is RAG?"
    assert stored.reason == "low_confidence"


def test_auto_enqueue_returns_none_when_not_triggered(queue):
    trigger = LowConfidenceTrigger(threshold=0.4)
    passages = [make_passage(score=0.9)]  # above threshold
    result = auto_enqueue("what is RAG?", passages, queue, trigger)
    assert result is None


def test_auto_enqueue_stores_correct_priority(queue):
    trigger = LowConfidenceTrigger(threshold=0.4)
    passages = [make_passage(score=0.2)]  # priority = 1.0 - 0.2 = 0.8
    item_id = auto_enqueue("q", passages, queue, trigger)
    item = queue.get(item_id)
    assert item.priority == pytest.approx(0.8)


def test_auto_enqueue_uses_suggested_answer_from_context(queue):
    trigger = DownThumbTrigger()
    item_id = auto_enqueue(
        "q", [], queue, trigger,
        context={"thumbs": "down", "suggested_answer": "The answer is 42."}
    )
    item = queue.get(item_id)
    assert item.suggested_answer == "The answer is 42."


def test_auto_enqueue_stores_passages_json(queue):
    trigger = LowConfidenceTrigger(threshold=0.4)
    passages = [make_passage(doc_id="my_doc", score=0.1, text="relevant text")]
    item_id = auto_enqueue("test", passages, queue, trigger)
    item = queue.get(item_id)
    p_data = item.passages
    assert len(p_data) == 1
    assert p_data[0]["doc_id"] == "my_doc"
    assert p_data[0]["score"] == pytest.approx(0.1)


def test_auto_enqueue_none_context_defaults_to_empty(queue):
    trigger = DownThumbTrigger()
    # Should not crash even with context=None
    result = auto_enqueue("q", [], queue, trigger, context=None)
    assert result is None  # trigger didn't fire


def test_auto_enqueue_with_composite_trigger(queue):
    composite = CompositeTrigger([
        LowConfidenceTrigger(threshold=0.4),
        DownThumbTrigger(),
    ])
    passages = [make_passage(score=0.9)]  # low_conf won't fire
    item_id = auto_enqueue("q", passages, queue, composite, {"thumbs": "down"})
    assert item_id is not None
    item = queue.get(item_id)
    assert item.reason == "down_thumb"
