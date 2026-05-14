"""Tests for docstoolkit.doc_change_queue — E287.

Covers: enqueue, dequeue (priority order, FIFO within priority),
peek, dequeue_batch, ack, nack (requeue/no-requeue), remove,
find_by_doc, clear, stats, size, enqueue_many, thread safety.
"""
import threading
import time
import pytest

from docstoolkit.doc_change_queue import (
    ChangeItem,
    ProcessResult,
    QueueStats,
    DocChangeQueue,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def fresh() -> DocChangeQueue:
    return DocChangeQueue()


def enq(q: DocChangeQueue, doc_id: str = "doc1", change_type: str = "update",
        payload: dict = None, priority: int = 0, now: float = None) -> ChangeItem:
    return q.enqueue(doc_id, change_type, payload=payload, priority=priority, now=now)


# ---------------------------------------------------------------------------
# ChangeItem dataclass
# ---------------------------------------------------------------------------

class TestChangeItem:
    def test_item_id_is_uuid_string(self):
        q = fresh()
        item = enq(q)
        assert isinstance(item.item_id, str)
        assert len(item.item_id) == 36  # standard UUID format

    def test_doc_id_stored(self):
        q = fresh()
        item = enq(q, doc_id="my-doc")
        assert item.doc_id == "my-doc"

    def test_change_type_stored(self):
        q = fresh()
        item = enq(q, change_type="create")
        assert item.change_type == "create"

    def test_payload_defaults_to_empty_dict(self):
        q = fresh()
        item = enq(q)
        assert item.payload == {}

    def test_payload_stored(self):
        q = fresh()
        item = enq(q, payload={"key": "value"})
        assert item.payload == {"key": "value"}

    def test_priority_default_zero(self):
        q = fresh()
        item = enq(q)
        assert item.priority == 0

    def test_priority_stored(self):
        q = fresh()
        item = enq(q, priority=5)
        assert item.priority == 5

    def test_enqueued_at_set(self):
        q = fresh()
        before = time.time()
        item = enq(q)
        after = time.time()
        assert before <= item.enqueued_at <= after

    def test_attempts_default_zero(self):
        q = fresh()
        item = enq(q)
        assert item.attempts == 0

    def test_unique_item_ids(self):
        q = fresh()
        ids = {enq(q, doc_id=f"d{i}").item_id for i in range(20)}
        assert len(ids) == 20


# ---------------------------------------------------------------------------
# QueueStats dataclass
# ---------------------------------------------------------------------------

class TestQueueStats:
    def test_fields_exist(self):
        s = QueueStats(pending_count=1, processed_count=2, failed_count=3, total_enqueued=6)
        assert s.pending_count == 1
        assert s.processed_count == 2
        assert s.failed_count == 3
        assert s.total_enqueued == 6


# ---------------------------------------------------------------------------
# ProcessResult dataclass
# ---------------------------------------------------------------------------

class TestProcessResult:
    def test_success_fields(self):
        r = ProcessResult(item_id="x", doc_id="d", success=True, processed_at=1.0)
        assert r.success is True
        assert r.error is None

    def test_failure_fields(self):
        r = ProcessResult(item_id="x", doc_id="d", success=False, error="oops", processed_at=1.0)
        assert r.success is False
        assert r.error == "oops"


# ---------------------------------------------------------------------------
# enqueue
# ---------------------------------------------------------------------------

class TestEnqueue:
    def test_returns_change_item(self):
        q = fresh()
        item = enq(q)
        assert isinstance(item, ChangeItem)

    def test_size_increases(self):
        q = fresh()
        assert q.size == 0
        enq(q)
        assert q.size == 1
        enq(q)
        assert q.size == 2

    def test_total_enqueued_increases(self):
        q = fresh()
        enq(q)
        enq(q)
        assert q.stats().total_enqueued == 2

    def test_now_parameter_overrides_timestamp(self):
        q = fresh()
        item = enq(q, now=1000.0)
        assert item.enqueued_at == 1000.0

    def test_all_change_types_accepted(self):
        q = fresh()
        for ct in ("create", "update", "delete", "publish"):
            item = enq(q, change_type=ct)
            assert item.change_type == ct

    def test_negative_priority_accepted(self):
        q = fresh()
        item = enq(q, priority=-1)
        assert item.priority == -1


# ---------------------------------------------------------------------------
# enqueue_many
# ---------------------------------------------------------------------------

class TestEnqueueMany:
    def test_returns_list_of_items(self):
        q = fresh()
        results = q.enqueue_many([
            {"doc_id": "a", "change_type": "create"},
            {"doc_id": "b", "change_type": "update"},
        ])
        assert len(results) == 2
        assert all(isinstance(r, ChangeItem) for r in results)

    def test_size_increases_by_count(self):
        q = fresh()
        q.enqueue_many([
            {"doc_id": "a", "change_type": "create"},
            {"doc_id": "b", "change_type": "delete"},
            {"doc_id": "c", "change_type": "publish"},
        ])
        assert q.size == 3

    def test_optional_payload_and_priority(self):
        q = fresh()
        results = q.enqueue_many([
            {"doc_id": "x", "change_type": "update", "payload": {"v": 1}, "priority": 5},
        ])
        assert results[0].payload == {"v": 1}
        assert results[0].priority == 5

    def test_empty_list_returns_empty(self):
        q = fresh()
        results = q.enqueue_many([])
        assert results == []
        assert q.size == 0

    def test_now_parameter_applied_to_all(self):
        q = fresh()
        results = q.enqueue_many(
            [{"doc_id": "a", "change_type": "update"},
             {"doc_id": "b", "change_type": "update"}],
            now=9999.0,
        )
        assert all(r.enqueued_at == 9999.0 for r in results)


# ---------------------------------------------------------------------------
# dequeue
# ---------------------------------------------------------------------------

class TestDequeue:
    def test_returns_none_on_empty(self):
        q = fresh()
        assert q.dequeue() is None

    def test_returns_item(self):
        q = fresh()
        enq(q)
        item = q.dequeue()
        assert isinstance(item, ChangeItem)

    def test_size_decreases(self):
        q = fresh()
        enq(q)
        q.dequeue()
        assert q.size == 0

    def test_fifo_same_priority(self):
        q = fresh()
        first = enq(q, doc_id="first", now=1.0)
        _second = enq(q, doc_id="second", now=2.0)
        item = q.dequeue()
        assert item.doc_id == "first"

    def test_higher_priority_first(self):
        q = fresh()
        enq(q, doc_id="low", priority=0, now=1.0)
        enq(q, doc_id="high", priority=10, now=2.0)
        item = q.dequeue()
        assert item.doc_id == "high"

    def test_priority_ordering_multiple(self):
        q = fresh()
        enq(q, doc_id="p0", priority=0, now=1.0)
        enq(q, doc_id="p5", priority=5, now=2.0)
        enq(q, doc_id="p2", priority=2, now=3.0)
        enq(q, doc_id="p10", priority=10, now=4.0)
        order = [q.dequeue().doc_id for _ in range(4)]
        assert order == ["p10", "p5", "p2", "p0"]

    def test_fifo_within_same_priority_multiple(self):
        q = fresh()
        for i in range(5):
            enq(q, doc_id=f"d{i}", priority=0, now=float(i))
        order = [q.dequeue().doc_id for _ in range(5)]
        assert order == [f"d{i}" for i in range(5)]

    def test_second_dequeue_after_first(self):
        q = fresh()
        enq(q, doc_id="a", now=1.0)
        enq(q, doc_id="b", now=2.0)
        q.dequeue()
        item = q.dequeue()
        assert item.doc_id == "b"

    def test_dequeue_all_leaves_empty(self):
        q = fresh()
        enq(q)
        q.dequeue()
        assert q.dequeue() is None


# ---------------------------------------------------------------------------
# peek
# ---------------------------------------------------------------------------

class TestPeek:
    def test_peek_empty_returns_none(self):
        q = fresh()
        assert q.peek() is None

    def test_peek_returns_next_item(self):
        q = fresh()
        item = enq(q)
        peeked = q.peek()
        assert peeked.item_id == item.item_id

    def test_peek_does_not_remove(self):
        q = fresh()
        enq(q)
        q.peek()
        assert q.size == 1

    def test_peek_returns_highest_priority(self):
        q = fresh()
        enq(q, doc_id="low", priority=0, now=1.0)
        enq(q, doc_id="high", priority=9, now=2.0)
        peeked = q.peek()
        assert peeked.doc_id == "high"

    def test_peek_consistent_with_dequeue(self):
        q = fresh()
        enq(q, doc_id="x", priority=3)
        enq(q, doc_id="y", priority=1)
        peeked = q.peek()
        dequeued = q.dequeue()
        assert peeked.item_id == dequeued.item_id


# ---------------------------------------------------------------------------
# dequeue_batch
# ---------------------------------------------------------------------------

class TestDequeueBatch:
    def test_returns_up_to_max(self):
        q = fresh()
        for i in range(5):
            enq(q, doc_id=f"d{i}")
        batch = q.dequeue_batch(3)
        assert len(batch) == 3

    def test_returns_all_when_fewer_than_max(self):
        q = fresh()
        enq(q)
        enq(q)
        batch = q.dequeue_batch(10)
        assert len(batch) == 2

    def test_size_decreases_by_batch_size(self):
        q = fresh()
        for _ in range(6):
            enq(q)
        q.dequeue_batch(4)
        assert q.size == 2

    def test_returns_in_priority_order(self):
        q = fresh()
        enq(q, doc_id="p0", priority=0, now=1.0)
        enq(q, doc_id="p5", priority=5, now=2.0)
        enq(q, doc_id="p2", priority=2, now=3.0)
        batch = q.dequeue_batch(3)
        assert [b.doc_id for b in batch] == ["p5", "p2", "p0"]

    def test_empty_queue_returns_empty_list(self):
        q = fresh()
        assert q.dequeue_batch(5) == []

    def test_max_zero_returns_empty(self):
        q = fresh()
        enq(q)
        batch = q.dequeue_batch(0)
        assert batch == []
        assert q.size == 1


# ---------------------------------------------------------------------------
# ack
# ---------------------------------------------------------------------------

class TestAck:
    def test_ack_in_flight_item(self):
        q = fresh()
        enq(q)
        item = q.dequeue()
        result = q.ack(item.item_id)
        assert result.success is True
        assert result.item_id == item.item_id
        assert result.doc_id == item.doc_id

    def test_ack_increments_processed_count(self):
        q = fresh()
        enq(q)
        item = q.dequeue()
        q.ack(item.item_id)
        assert q.stats().processed_count == 1

    def test_ack_sets_processed_at(self):
        q = fresh()
        enq(q)
        item = q.dequeue()
        before = time.time()
        result = q.ack(item.item_id)
        after = time.time()
        assert before <= result.processed_at <= after

    def test_ack_with_now_parameter(self):
        q = fresh()
        enq(q)
        item = q.dequeue()
        result = q.ack(item.item_id, now=5000.0)
        assert result.processed_at == 5000.0

    def test_ack_unknown_item_id_returns_failure(self):
        q = fresh()
        result = q.ack("nonexistent-id")
        assert result.success is False
        assert result.error is not None

    def test_ack_does_not_requeue(self):
        q = fresh()
        enq(q)
        item = q.dequeue()
        q.ack(item.item_id)
        assert q.size == 0

    def test_ack_multiple_items(self):
        q = fresh()
        for i in range(3):
            enq(q, doc_id=f"d{i}")
        items = [q.dequeue() for _ in range(3)]
        for item in items:
            q.ack(item.item_id)
        assert q.stats().processed_count == 3


# ---------------------------------------------------------------------------
# nack
# ---------------------------------------------------------------------------

class TestNack:
    def test_nack_requeue_true_puts_back(self):
        q = fresh()
        enq(q)
        item = q.dequeue()
        assert q.size == 0
        q.nack(item.item_id, requeue=True)
        assert q.size == 1

    def test_nack_requeue_increments_attempts(self):
        q = fresh()
        enq(q)
        item = q.dequeue()
        q.nack(item.item_id, requeue=True)
        requeued = q.dequeue()
        assert requeued.attempts == 1

    def test_nack_requeue_false_does_not_put_back(self):
        q = fresh()
        enq(q)
        item = q.dequeue()
        q.nack(item.item_id, requeue=False)
        assert q.size == 0

    def test_nack_requeue_false_increments_failed_count(self):
        q = fresh()
        enq(q)
        item = q.dequeue()
        q.nack(item.item_id, requeue=False)
        assert q.stats().failed_count == 1

    def test_nack_requeue_true_does_not_increment_failed(self):
        q = fresh()
        enq(q)
        item = q.dequeue()
        q.nack(item.item_id, requeue=True)
        assert q.stats().failed_count == 0

    def test_nack_returns_failure_result(self):
        q = fresh()
        enq(q)
        item = q.dequeue()
        result = q.nack(item.item_id, error="timeout")
        assert result.success is False
        assert result.error == "timeout"

    def test_nack_unknown_item_id(self):
        q = fresh()
        result = q.nack("bad-id")
        assert result.success is False

    def test_nack_with_now_parameter(self):
        q = fresh()
        enq(q)
        item = q.dequeue()
        result = q.nack(item.item_id, now=7777.0)
        assert result.processed_at == 7777.0

    def test_nack_multiple_times_increments_attempts(self):
        q = fresh()
        enq(q)
        item = q.dequeue()
        for expected_attempts in range(1, 4):
            q.nack(item.item_id, requeue=True)
            item = q.dequeue()
            assert item.attempts == expected_attempts

    def test_nack_empty_error_string(self):
        q = fresh()
        enq(q)
        item = q.dequeue()
        result = q.nack(item.item_id, error="", requeue=False)
        # empty error string is falsy; result.error may be None or ""
        assert result.success is False


# ---------------------------------------------------------------------------
# remove
# ---------------------------------------------------------------------------

class TestRemove:
    def test_remove_existing_item_returns_true(self):
        q = fresh()
        item = enq(q)
        assert q.remove(item.item_id) is True

    def test_remove_decreases_size(self):
        q = fresh()
        item = enq(q)
        q.remove(item.item_id)
        assert q.size == 0

    def test_remove_missing_returns_false(self):
        q = fresh()
        assert q.remove("does-not-exist") is False

    def test_remove_correct_item_leaves_others(self):
        q = fresh()
        a = enq(q, doc_id="a")
        _b = enq(q, doc_id="b")
        q.remove(a.item_id)
        remaining = q.dequeue()
        assert remaining.doc_id == "b"

    def test_remove_in_flight_item_returns_false(self):
        q = fresh()
        item = enq(q)
        q.dequeue()  # moves to in-flight
        assert q.remove(item.item_id) is False


# ---------------------------------------------------------------------------
# find_by_doc
# ---------------------------------------------------------------------------

class TestFindByDoc:
    def test_find_returns_matching_items(self):
        q = fresh()
        enq(q, doc_id="target")
        enq(q, doc_id="target")
        enq(q, doc_id="other")
        result = q.find_by_doc("target")
        assert len(result) == 2
        assert all(r.doc_id == "target" for r in result)

    def test_find_returns_empty_for_unknown_doc(self):
        q = fresh()
        enq(q, doc_id="x")
        assert q.find_by_doc("y") == []

    def test_find_does_not_remove_items(self):
        q = fresh()
        enq(q, doc_id="doc")
        q.find_by_doc("doc")
        assert q.size == 1

    def test_find_excludes_in_flight(self):
        q = fresh()
        item = enq(q, doc_id="doc")
        q.dequeue()  # moves to in-flight
        result = q.find_by_doc("doc")
        assert result == []


# ---------------------------------------------------------------------------
# clear
# ---------------------------------------------------------------------------

class TestClear:
    def test_clear_returns_count(self):
        q = fresh()
        for _ in range(4):
            enq(q)
        count = q.clear()
        assert count == 4

    def test_clear_empties_queue(self):
        q = fresh()
        enq(q)
        enq(q)
        q.clear()
        assert q.size == 0

    def test_clear_empty_queue_returns_zero(self):
        q = fresh()
        assert q.clear() == 0

    def test_clear_does_not_affect_in_flight(self):
        q = fresh()
        enq(q)
        item = q.dequeue()  # in-flight
        enq(q)
        q.clear()
        # in-flight item can still be acked
        result = q.ack(item.item_id)
        assert result.success is True


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------

class TestStats:
    def test_initial_stats_all_zero(self):
        q = fresh()
        s = q.stats()
        assert s.pending_count == 0
        assert s.processed_count == 0
        assert s.failed_count == 0
        assert s.total_enqueued == 0

    def test_stats_pending_count(self):
        q = fresh()
        enq(q)
        enq(q)
        assert q.stats().pending_count == 2

    def test_stats_total_enqueued(self):
        q = fresh()
        for _ in range(5):
            enq(q)
        assert q.stats().total_enqueued == 5

    def test_stats_processed_count_after_ack(self):
        q = fresh()
        enq(q)
        item = q.dequeue()
        q.ack(item.item_id)
        assert q.stats().processed_count == 1

    def test_stats_failed_count_after_nack_no_requeue(self):
        q = fresh()
        enq(q)
        item = q.dequeue()
        q.nack(item.item_id, requeue=False)
        assert q.stats().failed_count == 1

    def test_stats_returns_queuestat_instance(self):
        q = fresh()
        assert isinstance(q.stats(), QueueStats)


# ---------------------------------------------------------------------------
# size property
# ---------------------------------------------------------------------------

class TestSize:
    def test_size_zero_initially(self):
        assert fresh().size == 0

    def test_size_after_enqueue(self):
        q = fresh()
        enq(q)
        assert q.size == 1

    def test_size_after_dequeue(self):
        q = fresh()
        enq(q)
        enq(q)
        q.dequeue()
        assert q.size == 1


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------

class TestThreadSafety:
    def test_concurrent_enqueue(self):
        q = fresh()
        errors = []

        def worker():
            try:
                for i in range(50):
                    enq(q, doc_id=f"d-{threading.get_ident()}-{i}")
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=worker) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
        assert q.size == 500

    def test_concurrent_enqueue_dequeue(self):
        q = fresh()
        enqueued = []
        dequeued = []
        lock = threading.Lock()

        def producer():
            for i in range(30):
                item = enq(q, doc_id=f"d{i}")
                with lock:
                    enqueued.append(item.item_id)

        def consumer():
            for _ in range(30):
                item = q.dequeue()
                if item is not None:
                    with lock:
                        dequeued.append(item.item_id)

        t1 = threading.Thread(target=producer)
        t2 = threading.Thread(target=consumer)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        # Drain remaining
        while True:
            item = q.dequeue()
            if item is None:
                break
            dequeued.append(item.item_id)

        assert len(dequeued) == 30

    def test_concurrent_ack_nack(self):
        """Multiple threads dequeue and ack/nack without raising."""
        q = fresh()
        for i in range(100):
            enq(q, doc_id=f"d{i}")

        errors = []

        def worker():
            try:
                item = q.dequeue()
                if item:
                    if hash(item.item_id) % 2 == 0:
                        q.ack(item.item_id)
                    else:
                        q.nack(item.item_id, requeue=False)
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=worker) for _ in range(50)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []

    def test_concurrent_stats_does_not_raise(self):
        q = fresh()
        for _ in range(20):
            enq(q)

        errors = []

        def reader():
            try:
                for _ in range(20):
                    q.stats()
            except Exception as e:
                errors.append(e)

        def writer():
            try:
                for _ in range(20):
                    enq(q)
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=reader) for _ in range(5)]
        threads += [threading.Thread(target=writer) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
