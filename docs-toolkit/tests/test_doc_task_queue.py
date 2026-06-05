"""Tests for docstoolkit.doc_task_queue (E352)."""
from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_task_queue import DocTaskQueue, QueueItem, QueueStats


# ---------------------------------------------------------------------------
class TestQueueItemDataclass:
    def test_defaults(self):
        item = QueueItem()
        assert item.item_id == 0
        assert item.doc_id == ""
        assert item.payload == {}
        assert item.priority == 0
        assert item.enqueued_at == 0.0
        assert item.status == "queued"

    def test_construct_with_values(self):
        item = QueueItem(item_id=3, doc_id="d", priority=5, enqueued_at=1.5)
        assert item.item_id == 3
        assert item.doc_id == "d"
        assert item.priority == 5
        assert item.enqueued_at == 1.5

    def test_payload_default_is_independent(self):
        a = QueueItem()
        b = QueueItem()
        a.payload["x"] = 1
        assert b.payload == {}

    def test_status_default_queued(self):
        assert QueueItem().status == "queued"

    def test_set_status(self):
        item = QueueItem()
        item.status = "processed"
        assert item.status == "processed"


# ---------------------------------------------------------------------------
class TestQueueStatsDataclass:
    def test_defaults(self):
        s = QueueStats()
        assert s.total == 0
        assert s.queued == 0
        assert s.processed == 0
        assert s.skipped == 0

    def test_construct(self):
        s = QueueStats(total=5, queued=2, processed=2, skipped=1)
        assert s.total == 5
        assert s.queued == 2
        assert s.processed == 2
        assert s.skipped == 1


# ---------------------------------------------------------------------------
class TestConstruction:
    def test_empty_queue(self):
        q = DocTaskQueue()
        assert q.queue_size() == 0

    def test_initial_stats_zero(self):
        q = DocTaskQueue()
        s = q.stats()
        assert s.total == 0 and s.queued == 0

    def test_pop_empty_returns_none(self):
        assert DocTaskQueue().pop() is None

    def test_peek_empty_returns_none(self):
        assert DocTaskQueue().peek() is None


# ---------------------------------------------------------------------------
class TestEnqueue:
    def test_returns_queue_item(self):
        q = DocTaskQueue()
        item = q.enqueue("doc1")
        assert isinstance(item, QueueItem)

    def test_first_id_is_one(self):
        q = DocTaskQueue()
        assert q.enqueue("d").item_id == 1

    def test_id_increments(self):
        q = DocTaskQueue()
        ids = [q.enqueue("d").item_id for _ in range(4)]
        assert ids == [1, 2, 3, 4]

    def test_status_queued(self):
        assert DocTaskQueue().enqueue("d").status == "queued"

    def test_payload_stored(self):
        q = DocTaskQueue()
        item = q.enqueue("d", payload={"k": "v"})
        assert item.payload == {"k": "v"}

    def test_payload_default_empty(self):
        assert DocTaskQueue().enqueue("d").payload == {}

    def test_priority_default_zero(self):
        assert DocTaskQueue().enqueue("d").priority == 0

    def test_priority_stored(self):
        assert DocTaskQueue().enqueue("d", priority=7).priority == 7

    def test_enqueued_at_uses_now_arg(self):
        item = DocTaskQueue().enqueue("d", now=123.5)
        assert item.enqueued_at == 123.5

    def test_doc_id_stored(self):
        assert DocTaskQueue().enqueue("docX").doc_id == "docX"

    def test_increments_queue_size(self):
        q = DocTaskQueue()
        q.enqueue("a")
        q.enqueue("b")
        assert q.queue_size() == 2

    def test_payload_is_copied(self):
        p = {"k": 1}
        q = DocTaskQueue()
        item = q.enqueue("d", payload=p)
        p["k"] = 999
        assert item.payload["k"] == 1


# ---------------------------------------------------------------------------
class TestPop:
    def test_highest_priority_first(self):
        q = DocTaskQueue()
        q.enqueue("low", priority=1, now=1.0)
        hi = q.enqueue("hi", priority=10, now=2.0)
        out = q.pop()
        assert out.item_id == hi.item_id

    def test_fifo_within_same_priority(self):
        q = DocTaskQueue()
        a = q.enqueue("a", priority=5, now=1.0)
        b = q.enqueue("b", priority=5, now=2.0)
        first = q.pop()
        second = q.pop()
        assert first.item_id == a.item_id
        assert second.item_id == b.item_id

    def test_marks_processed(self):
        q = DocTaskQueue()
        item = q.enqueue("a")
        popped = q.pop()
        assert popped.status == "processed"
        assert q.get(item.item_id).status == "processed"

    def test_none_when_empty(self):
        assert DocTaskQueue().pop() is None

    def test_pops_until_empty_then_none(self):
        q = DocTaskQueue()
        q.enqueue("a")
        q.enqueue("b")
        q.pop()
        q.pop()
        assert q.pop() is None

    def test_skips_stale_items(self):
        q = DocTaskQueue()
        a = q.enqueue("a", priority=5, now=1.0)
        b = q.enqueue("b", priority=3, now=2.0)
        # Externally mark a as skipped — heap still has its entry.
        assert q.mark_skipped(a.item_id) is True
        out = q.pop()
        assert out.item_id == b.item_id

    def test_decreases_queue_size(self):
        q = DocTaskQueue()
        q.enqueue("a")
        q.enqueue("b")
        q.pop()
        assert q.queue_size() == 1

    def test_negative_priority_works(self):
        q = DocTaskQueue()
        q.enqueue("neg", priority=-5, now=1.0)
        hi = q.enqueue("hi", priority=0, now=2.0)
        out = q.pop()
        assert out.item_id == hi.item_id


# ---------------------------------------------------------------------------
class TestPeek:
    def test_returns_top_item(self):
        q = DocTaskQueue()
        q.enqueue("low", priority=1, now=1.0)
        hi = q.enqueue("hi", priority=10, now=2.0)
        assert q.peek().item_id == hi.item_id

    def test_no_state_change(self):
        q = DocTaskQueue()
        item = q.enqueue("a")
        q.peek()
        assert q.get(item.item_id).status == "queued"
        assert q.queue_size() == 1

    def test_peek_twice_returns_same(self):
        q = DocTaskQueue()
        q.enqueue("a", priority=5)
        first = q.peek()
        second = q.peek()
        assert first.item_id == second.item_id

    def test_none_when_empty(self):
        assert DocTaskQueue().peek() is None

    def test_peek_skips_stale(self):
        q = DocTaskQueue()
        a = q.enqueue("a", priority=10, now=1.0)
        b = q.enqueue("b", priority=5, now=2.0)
        q.mark_skipped(a.item_id)
        assert q.peek().item_id == b.item_id


# ---------------------------------------------------------------------------
class TestMarkProcessed:
    def test_returns_true_when_queued(self):
        q = DocTaskQueue()
        item = q.enqueue("a")
        assert q.mark_processed(item.item_id) is True

    def test_status_becomes_processed(self):
        q = DocTaskQueue()
        item = q.enqueue("a")
        q.mark_processed(item.item_id)
        assert q.get(item.item_id).status == "processed"

    def test_returns_false_for_unknown_id(self):
        assert DocTaskQueue().mark_processed(999) is False

    def test_returns_false_if_already_processed(self):
        q = DocTaskQueue()
        item = q.enqueue("a")
        q.mark_processed(item.item_id)
        assert q.mark_processed(item.item_id) is False

    def test_returns_false_if_skipped(self):
        q = DocTaskQueue()
        item = q.enqueue("a")
        q.mark_skipped(item.item_id)
        assert q.mark_processed(item.item_id) is False


# ---------------------------------------------------------------------------
class TestMarkSkipped:
    def test_returns_true_when_queued(self):
        q = DocTaskQueue()
        item = q.enqueue("a")
        assert q.mark_skipped(item.item_id) is True

    def test_status_becomes_skipped(self):
        q = DocTaskQueue()
        item = q.enqueue("a")
        q.mark_skipped(item.item_id)
        assert q.get(item.item_id).status == "skipped"

    def test_returns_false_for_unknown_id(self):
        assert DocTaskQueue().mark_skipped(999) is False

    def test_returns_false_if_already_skipped(self):
        q = DocTaskQueue()
        item = q.enqueue("a")
        q.mark_skipped(item.item_id)
        assert q.mark_skipped(item.item_id) is False

    def test_returns_false_if_processed(self):
        q = DocTaskQueue()
        item = q.enqueue("a")
        q.mark_processed(item.item_id)
        assert q.mark_skipped(item.item_id) is False


# ---------------------------------------------------------------------------
class TestRequeue:
    def test_returns_false_for_unknown(self):
        assert DocTaskQueue().requeue(999) is False

    def test_returns_false_if_already_queued(self):
        q = DocTaskQueue()
        item = q.enqueue("a")
        assert q.requeue(item.item_id) is False

    def test_requeue_processed_returns_true(self):
        q = DocTaskQueue()
        item = q.enqueue("a")
        q.mark_processed(item.item_id)
        assert q.requeue(item.item_id) is True

    def test_requeue_skipped_returns_true(self):
        q = DocTaskQueue()
        item = q.enqueue("a")
        q.mark_skipped(item.item_id)
        assert q.requeue(item.item_id) is True

    def test_status_back_to_queued(self):
        q = DocTaskQueue()
        item = q.enqueue("a")
        q.mark_skipped(item.item_id)
        q.requeue(item.item_id)
        assert q.get(item.item_id).status == "queued"

    def test_requeue_updates_enqueued_at(self):
        q = DocTaskQueue()
        item = q.enqueue("a", now=1.0)
        q.mark_processed(item.item_id)
        q.requeue(item.item_id, now=999.0)
        assert q.get(item.item_id).enqueued_at == 999.0

    def test_requeue_pops_again(self):
        q = DocTaskQueue()
        item = q.enqueue("a")
        q.pop()
        q.requeue(item.item_id, now=5.0)
        out = q.pop()
        assert out.item_id == item.item_id


# ---------------------------------------------------------------------------
class TestGet:
    def test_returns_item(self):
        q = DocTaskQueue()
        item = q.enqueue("a")
        assert q.get(item.item_id) is item

    def test_returns_none_for_unknown(self):
        assert DocTaskQueue().get(9999) is None

    def test_returns_none_after_clear(self):
        q = DocTaskQueue()
        item = q.enqueue("a")
        q.mark_processed(item.item_id)
        q.clear_processed()
        assert q.get(item.item_id) is None


# ---------------------------------------------------------------------------
class TestQueuedItems:
    def test_empty(self):
        assert DocTaskQueue().queued_items() == []

    def test_sorted_by_priority_desc(self):
        q = DocTaskQueue()
        q.enqueue("a", priority=1, now=1.0)
        q.enqueue("b", priority=5, now=2.0)
        q.enqueue("c", priority=3, now=3.0)
        prios = [it.priority for it in q.queued_items()]
        assert prios == [5, 3, 1]

    def test_fifo_within_priority(self):
        q = DocTaskQueue()
        q.enqueue("a", priority=5, now=1.0)
        q.enqueue("b", priority=5, now=2.0)
        out = q.queued_items()
        assert [it.doc_id for it in out] == ["a", "b"]

    def test_excludes_processed(self):
        q = DocTaskQueue()
        item = q.enqueue("a")
        q.enqueue("b")
        q.mark_processed(item.item_id)
        assert [it.doc_id for it in q.queued_items()] == ["b"]

    def test_excludes_skipped(self):
        q = DocTaskQueue()
        item = q.enqueue("a")
        q.enqueue("b")
        q.mark_skipped(item.item_id)
        assert [it.doc_id for it in q.queued_items()] == ["b"]


# ---------------------------------------------------------------------------
class TestItemsForDoc:
    def test_empty(self):
        assert DocTaskQueue().items_for_doc("nope") == []

    def test_filters_by_doc(self):
        q = DocTaskQueue()
        q.enqueue("a", now=1.0)
        q.enqueue("b", now=2.0)
        q.enqueue("a", now=3.0)
        assert len(q.items_for_doc("a")) == 2

    def test_sorted_by_enqueued_at(self):
        q = DocTaskQueue()
        q.enqueue("a", now=3.0)
        q.enqueue("a", now=1.0)
        q.enqueue("a", now=2.0)
        times = [it.enqueued_at for it in q.items_for_doc("a")]
        assert times == [1.0, 2.0, 3.0]

    def test_includes_all_statuses(self):
        q = DocTaskQueue()
        a = q.enqueue("d", now=1.0)
        q.enqueue("d", now=2.0)
        q.mark_processed(a.item_id)
        assert len(q.items_for_doc("d")) == 2


# ---------------------------------------------------------------------------
class TestItemsByStatus:
    def test_empty(self):
        assert DocTaskQueue().items_by_status("queued") == []

    def test_filters_queued(self):
        q = DocTaskQueue()
        a = q.enqueue("a")
        q.enqueue("b")
        q.mark_processed(a.item_id)
        out = q.items_by_status("queued")
        assert [it.doc_id for it in out] == ["b"]

    def test_filters_processed(self):
        q = DocTaskQueue()
        a = q.enqueue("a")
        q.enqueue("b")
        q.mark_processed(a.item_id)
        out = q.items_by_status("processed")
        assert [it.doc_id for it in out] == ["a"]

    def test_filters_skipped(self):
        q = DocTaskQueue()
        a = q.enqueue("a")
        q.enqueue("b")
        q.mark_skipped(a.item_id)
        out = q.items_by_status("skipped")
        assert [it.doc_id for it in out] == ["a"]

    def test_sorted_by_enqueued_at(self):
        q = DocTaskQueue()
        q.enqueue("a", now=3.0)
        q.enqueue("b", now=1.0)
        q.enqueue("c", now=2.0)
        times = [it.enqueued_at for it in q.items_by_status("queued")]
        assert times == [1.0, 2.0, 3.0]


# ---------------------------------------------------------------------------
class TestClearProcessed:
    def test_empty_returns_zero(self):
        assert DocTaskQueue().clear_processed() == 0

    def test_removes_processed(self):
        q = DocTaskQueue()
        a = q.enqueue("a")
        b = q.enqueue("b")
        q.mark_processed(a.item_id)
        q.mark_processed(b.item_id)
        assert q.clear_processed() == 2

    def test_removes_skipped(self):
        q = DocTaskQueue()
        a = q.enqueue("a")
        q.mark_skipped(a.item_id)
        assert q.clear_processed() == 1

    def test_keeps_queued(self):
        q = DocTaskQueue()
        a = q.enqueue("a")
        b = q.enqueue("b")
        q.mark_processed(a.item_id)
        q.clear_processed()
        assert q.get(b.item_id) is not None
        assert q.get(a.item_id) is None

    def test_count_correct_mixed(self):
        q = DocTaskQueue()
        a = q.enqueue("a")
        b = q.enqueue("b")
        c = q.enqueue("c")
        q.mark_processed(a.item_id)
        q.mark_skipped(b.item_id)
        # c stays queued
        assert q.clear_processed() == 2
        assert q.queue_size() == 1


# ---------------------------------------------------------------------------
class TestQueueSize:
    def test_zero_empty(self):
        assert DocTaskQueue().queue_size() == 0

    def test_counts_only_queued(self):
        q = DocTaskQueue()
        a = q.enqueue("a")
        q.enqueue("b")
        q.mark_processed(a.item_id)
        assert q.queue_size() == 1

    def test_after_pop(self):
        q = DocTaskQueue()
        q.enqueue("a")
        q.enqueue("b")
        q.pop()
        assert q.queue_size() == 1

    def test_after_requeue(self):
        q = DocTaskQueue()
        item = q.enqueue("a")
        q.pop()
        assert q.queue_size() == 0
        q.requeue(item.item_id)
        assert q.queue_size() == 1


# ---------------------------------------------------------------------------
class TestStats:
    def test_empty(self):
        s = DocTaskQueue().stats()
        assert (s.total, s.queued, s.processed, s.skipped) == (0, 0, 0, 0)

    def test_only_queued(self):
        q = DocTaskQueue()
        q.enqueue("a")
        q.enqueue("b")
        s = q.stats()
        assert s.total == 2 and s.queued == 2

    def test_mixed(self):
        q = DocTaskQueue()
        a = q.enqueue("a")
        b = q.enqueue("b")
        q.enqueue("c")
        q.mark_processed(a.item_id)
        q.mark_skipped(b.item_id)
        s = q.stats()
        assert s.total == 3
        assert s.queued == 1
        assert s.processed == 1
        assert s.skipped == 1

    def test_after_clear(self):
        q = DocTaskQueue()
        a = q.enqueue("a")
        q.mark_processed(a.item_id)
        q.clear_processed()
        s = q.stats()
        assert s.total == 0


# ---------------------------------------------------------------------------
class TestThreadSafety:
    def test_concurrent_enqueue_unique_ids(self):
        q = DocTaskQueue()
        results: list[int] = []
        lock = threading.Lock()

        def worker():
            for _ in range(50):
                item = q.enqueue("d")
                with lock:
                    results.append(item.item_id)

        threads = [threading.Thread(target=worker) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(results) == 200
        assert len(set(results)) == 200  # all unique

    def test_concurrent_enqueue_size(self):
        q = DocTaskQueue()

        def worker():
            for _ in range(25):
                q.enqueue("d")

        threads = [threading.Thread(target=worker) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert q.queue_size() == 100

    def test_concurrent_enqueue_pop(self):
        q = DocTaskQueue()
        for _ in range(200):
            q.enqueue("d")

        popped: list = []
        lock = threading.Lock()

        def worker():
            while True:
                item = q.pop()
                if item is None:
                    return
                with lock:
                    popped.append(item.item_id)

        threads = [threading.Thread(target=worker) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert len(popped) == 200
        assert len(set(popped)) == 200
