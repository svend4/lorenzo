"""Tests for E329 DocOutbox module."""

from __future__ import annotations

import threading
import uuid

import pytest

from docstoolkit.doc_outbox import DocOutbox, OutboxMessage, OutboxStats


class TestOutboxMessageDataclass:
    def test_construct_minimal(self):
        msg = OutboxMessage(message_id="m1", doc_id="d1", destination="email:a@b.c")
        assert msg.message_id == "m1"
        assert msg.doc_id == "d1"
        assert msg.destination == "email:a@b.c"

    def test_default_payload_is_dict(self):
        msg = OutboxMessage(message_id="m1", doc_id="d1", destination="x")
        assert msg.payload == {}
        assert isinstance(msg.payload, dict)

    def test_default_status_pending(self):
        msg = OutboxMessage(message_id="m1", doc_id="d1", destination="x")
        assert msg.status == "pending"

    def test_default_attempts_zero(self):
        msg = OutboxMessage(message_id="m1", doc_id="d1", destination="x")
        assert msg.attempts == 0

    def test_default_last_attempt_none(self):
        msg = OutboxMessage(message_id="m1", doc_id="d1", destination="x")
        assert msg.last_attempt_at is None

    def test_default_last_error_empty(self):
        msg = OutboxMessage(message_id="m1", doc_id="d1", destination="x")
        assert msg.last_error == ""

    def test_default_created_at_zero(self):
        msg = OutboxMessage(message_id="m1", doc_id="d1", destination="x")
        assert msg.created_at == 0.0

    def test_independent_payload_per_instance(self):
        m1 = OutboxMessage(message_id="a", doc_id="d", destination="x")
        m2 = OutboxMessage(message_id="b", doc_id="d", destination="x")
        m1.payload["k"] = 1
        assert m2.payload == {}


class TestOutboxStatsDataclass:
    def test_construct(self):
        s = OutboxStats(total=10, pending=3, sent=5, failed=1, abandoned=1)
        assert s.total == 10
        assert s.pending == 3
        assert s.sent == 5
        assert s.failed == 1
        assert s.abandoned == 1

    def test_equality(self):
        a = OutboxStats(1, 1, 0, 0, 0)
        b = OutboxStats(1, 1, 0, 0, 0)
        assert a == b


class TestConstruction:
    def test_empty_on_init(self):
        ob = DocOutbox()
        assert ob.stats().total == 0

    def test_independent_instances(self):
        a = DocOutbox()
        b = DocOutbox()
        a.enqueue("d1", "email:x@y")
        assert b.stats().total == 0


class TestEnqueue:
    def test_returns_message(self):
        ob = DocOutbox()
        msg = ob.enqueue("d1", "email:a@b")
        assert isinstance(msg, OutboxMessage)

    def test_message_id_is_uuid(self):
        ob = DocOutbox()
        msg = ob.enqueue("d1", "email:a@b")
        # Should parse as UUID
        uuid.UUID(msg.message_id)

    def test_status_pending(self):
        ob = DocOutbox()
        msg = ob.enqueue("d1", "email:a@b")
        assert msg.status == "pending"

    def test_attempts_zero(self):
        ob = DocOutbox()
        msg = ob.enqueue("d1", "email:a@b")
        assert msg.attempts == 0

    def test_payload_stored(self):
        ob = DocOutbox()
        msg = ob.enqueue("d1", "email:a@b", payload={"hello": "world"})
        assert msg.payload == {"hello": "world"}

    def test_payload_default_empty(self):
        ob = DocOutbox()
        msg = ob.enqueue("d1", "email:a@b")
        assert msg.payload == {}

    def test_payload_copied(self):
        ob = DocOutbox()
        original = {"k": 1}
        msg = ob.enqueue("d1", "email:a@b", payload=original)
        original["k"] = 999
        assert msg.payload["k"] == 1

    def test_created_at_set(self):
        ob = DocOutbox()
        msg = ob.enqueue("d1", "email:a@b", now=100.0)
        assert msg.created_at == 100.0

    def test_unique_ids(self):
        ob = DocOutbox()
        ids = {ob.enqueue("d", "x").message_id for _ in range(50)}
        assert len(ids) == 50

    def test_stored_in_outbox(self):
        ob = DocOutbox()
        msg = ob.enqueue("d1", "email:a@b")
        assert ob.get(msg.message_id) is msg


class TestMarkSent:
    def test_returns_true_on_found(self):
        ob = DocOutbox()
        msg = ob.enqueue("d", "x")
        assert ob.mark_sent(msg.message_id) is True

    def test_status_becomes_sent(self):
        ob = DocOutbox()
        msg = ob.enqueue("d", "x")
        ob.mark_sent(msg.message_id)
        assert ob.get(msg.message_id).status == "sent"

    def test_attempts_incremented(self):
        ob = DocOutbox()
        msg = ob.enqueue("d", "x")
        ob.mark_sent(msg.message_id)
        assert ob.get(msg.message_id).attempts == 1

    def test_last_attempt_set(self):
        ob = DocOutbox()
        msg = ob.enqueue("d", "x")
        ob.mark_sent(msg.message_id, now=500.0)
        assert ob.get(msg.message_id).last_attempt_at == 500.0

    def test_returns_false_on_missing(self):
        ob = DocOutbox()
        assert ob.mark_sent("nope") is False


class TestMarkFailed:
    def test_returns_true_on_found(self):
        ob = DocOutbox()
        msg = ob.enqueue("d", "x")
        assert ob.mark_failed(msg.message_id, "boom") is True

    def test_status_becomes_failed(self):
        ob = DocOutbox()
        msg = ob.enqueue("d", "x")
        ob.mark_failed(msg.message_id, "boom")
        assert ob.get(msg.message_id).status == "failed"

    def test_error_stored(self):
        ob = DocOutbox()
        msg = ob.enqueue("d", "x")
        ob.mark_failed(msg.message_id, "timeout")
        assert ob.get(msg.message_id).last_error == "timeout"

    def test_attempts_incremented(self):
        ob = DocOutbox()
        msg = ob.enqueue("d", "x")
        ob.mark_failed(msg.message_id)
        ob.mark_failed(msg.message_id)
        assert ob.get(msg.message_id).attempts == 2

    def test_last_attempt_set(self):
        ob = DocOutbox()
        msg = ob.enqueue("d", "x")
        ob.mark_failed(msg.message_id, now=42.0)
        assert ob.get(msg.message_id).last_attempt_at == 42.0

    def test_returns_false_on_missing(self):
        ob = DocOutbox()
        assert ob.mark_failed("nope") is False


class TestAbandon:
    def test_returns_true_on_found(self):
        ob = DocOutbox()
        msg = ob.enqueue("d", "x")
        assert ob.abandon(msg.message_id, "gave up") is True

    def test_status_becomes_abandoned(self):
        ob = DocOutbox()
        msg = ob.enqueue("d", "x")
        ob.abandon(msg.message_id)
        assert ob.get(msg.message_id).status == "abandoned"

    def test_reason_stored(self):
        ob = DocOutbox()
        msg = ob.enqueue("d", "x")
        ob.abandon(msg.message_id, "too many retries")
        assert ob.get(msg.message_id).last_error == "too many retries"

    def test_returns_false_on_missing(self):
        ob = DocOutbox()
        assert ob.abandon("nope") is False


class TestRetry:
    def test_failed_to_pending(self):
        ob = DocOutbox()
        msg = ob.enqueue("d", "x")
        ob.mark_failed(msg.message_id, "err")
        assert ob.retry(msg.message_id) is True
        assert ob.get(msg.message_id).status == "pending"

    def test_no_op_when_pending(self):
        ob = DocOutbox()
        msg = ob.enqueue("d", "x")
        assert ob.retry(msg.message_id) is False
        assert ob.get(msg.message_id).status == "pending"

    def test_no_op_when_sent(self):
        ob = DocOutbox()
        msg = ob.enqueue("d", "x")
        ob.mark_sent(msg.message_id)
        assert ob.retry(msg.message_id) is False
        assert ob.get(msg.message_id).status == "sent"

    def test_no_op_when_abandoned(self):
        ob = DocOutbox()
        msg = ob.enqueue("d", "x")
        ob.abandon(msg.message_id)
        assert ob.retry(msg.message_id) is False
        assert ob.get(msg.message_id).status == "abandoned"

    def test_returns_false_on_missing(self):
        ob = DocOutbox()
        assert ob.retry("nope") is False


class TestDelete:
    def test_returns_true_on_found(self):
        ob = DocOutbox()
        msg = ob.enqueue("d", "x")
        assert ob.delete(msg.message_id) is True

    def test_removed_fully(self):
        ob = DocOutbox()
        msg = ob.enqueue("d", "x")
        ob.delete(msg.message_id)
        assert ob.get(msg.message_id) is None

    def test_returns_false_on_missing(self):
        ob = DocOutbox()
        assert ob.delete("nope") is False

    def test_stats_after_delete(self):
        ob = DocOutbox()
        msg = ob.enqueue("d", "x")
        ob.delete(msg.message_id)
        assert ob.stats().total == 0


class TestGet:
    def test_found(self):
        ob = DocOutbox()
        msg = ob.enqueue("d", "x")
        assert ob.get(msg.message_id) is msg

    def test_not_found(self):
        ob = DocOutbox()
        assert ob.get("nope") is None


class TestPending:
    def test_oldest_first(self):
        ob = DocOutbox()
        m1 = ob.enqueue("d", "x", now=10.0)
        m2 = ob.enqueue("d", "x", now=5.0)
        m3 = ob.enqueue("d", "x", now=20.0)
        result = ob.pending()
        assert [m.message_id for m in result] == [m2.message_id, m1.message_id, m3.message_id]

    def test_limit(self):
        ob = DocOutbox()
        for i in range(5):
            ob.enqueue("d", "x", now=float(i))
        assert len(ob.pending(limit=2)) == 2

    def test_only_pending(self):
        ob = DocOutbox()
        m1 = ob.enqueue("d", "x", now=1.0)
        m2 = ob.enqueue("d", "x", now=2.0)
        ob.mark_sent(m1.message_id)
        result = ob.pending()
        assert [m.message_id for m in result] == [m2.message_id]

    def test_empty(self):
        ob = DocOutbox()
        assert ob.pending() == []


class TestMessagesForDoc:
    def test_filtered_by_doc(self):
        ob = DocOutbox()
        m1 = ob.enqueue("a", "x", now=1.0)
        m2 = ob.enqueue("b", "x", now=2.0)
        m3 = ob.enqueue("a", "x", now=3.0)
        result = ob.messages_for_doc("a")
        assert [m.message_id for m in result] == [m1.message_id, m3.message_id]

    def test_sorted_by_created(self):
        ob = DocOutbox()
        m1 = ob.enqueue("a", "x", now=30.0)
        m2 = ob.enqueue("a", "x", now=10.0)
        m3 = ob.enqueue("a", "x", now=20.0)
        result = ob.messages_for_doc("a")
        assert [m.message_id for m in result] == [m2.message_id, m3.message_id, m1.message_id]

    def test_empty(self):
        ob = DocOutbox()
        assert ob.messages_for_doc("none") == []


class TestMessagesByStatus:
    def test_filter_sent(self):
        ob = DocOutbox()
        m1 = ob.enqueue("d", "x", now=1.0)
        m2 = ob.enqueue("d", "x", now=2.0)
        ob.mark_sent(m1.message_id)
        result = ob.messages_by_status("sent")
        assert [m.message_id for m in result] == [m1.message_id]

    def test_filter_pending(self):
        ob = DocOutbox()
        m1 = ob.enqueue("d", "x", now=1.0)
        m2 = ob.enqueue("d", "x", now=2.0)
        ob.mark_failed(m2.message_id)
        result = ob.messages_by_status("pending")
        assert [m.message_id for m in result] == [m1.message_id]

    def test_sorted_by_created(self):
        ob = DocOutbox()
        m1 = ob.enqueue("d", "x", now=30.0)
        m2 = ob.enqueue("d", "x", now=10.0)
        result = ob.messages_by_status("pending")
        assert result[0].message_id == m2.message_id

    def test_empty(self):
        ob = DocOutbox()
        assert ob.messages_by_status("sent") == []


class TestFailedMessages:
    def test_only_failed(self):
        ob = DocOutbox()
        m1 = ob.enqueue("d", "x")
        m2 = ob.enqueue("d", "x")
        ob.mark_failed(m1.message_id, "e1", now=1.0)
        result = ob.failed_messages()
        assert [m.message_id for m in result] == [m1.message_id]

    def test_sorted_desc_by_last_attempt(self):
        ob = DocOutbox()
        m1 = ob.enqueue("d", "x")
        m2 = ob.enqueue("d", "x")
        m3 = ob.enqueue("d", "x")
        ob.mark_failed(m1.message_id, now=10.0)
        ob.mark_failed(m2.message_id, now=30.0)
        ob.mark_failed(m3.message_id, now=20.0)
        result = ob.failed_messages()
        assert [m.message_id for m in result] == [m2.message_id, m3.message_id, m1.message_id]

    def test_empty(self):
        ob = DocOutbox()
        assert ob.failed_messages() == []


class TestPurgeSent:
    def test_count_returned(self):
        ob = DocOutbox()
        ids = [ob.enqueue("d", "x").message_id for _ in range(3)]
        for mid in ids:
            ob.mark_sent(mid)
        assert ob.purge_sent() == 3

    def test_only_sent_removed(self):
        ob = DocOutbox()
        m1 = ob.enqueue("d", "x")
        m2 = ob.enqueue("d", "x")
        m3 = ob.enqueue("d", "x")
        ob.mark_sent(m1.message_id)
        ob.mark_failed(m2.message_id)
        ob.purge_sent()
        assert ob.get(m1.message_id) is None
        assert ob.get(m2.message_id) is not None
        assert ob.get(m3.message_id) is not None

    def test_zero_when_none_sent(self):
        ob = DocOutbox()
        ob.enqueue("d", "x")
        assert ob.purge_sent() == 0

    def test_empty_outbox(self):
        ob = DocOutbox()
        assert ob.purge_sent() == 0


class TestStats:
    def test_empty(self):
        ob = DocOutbox()
        s = ob.stats()
        assert s == OutboxStats(0, 0, 0, 0, 0)

    def test_counts_by_status(self):
        ob = DocOutbox()
        m1 = ob.enqueue("d", "x")
        m2 = ob.enqueue("d", "x")
        m3 = ob.enqueue("d", "x")
        m4 = ob.enqueue("d", "x")
        m5 = ob.enqueue("d", "x")
        ob.mark_sent(m1.message_id)
        ob.mark_sent(m2.message_id)
        ob.mark_failed(m3.message_id)
        ob.abandon(m4.message_id)
        s = ob.stats()
        assert s.total == 5
        assert s.sent == 2
        assert s.failed == 1
        assert s.abandoned == 1
        assert s.pending == 1

    def test_total_matches_dict_count(self):
        ob = DocOutbox()
        for _ in range(7):
            ob.enqueue("d", "x")
        assert ob.stats().total == 7


class TestThreadSafety:
    def test_concurrent_enqueue(self):
        ob = DocOutbox()
        N_THREADS = 8
        PER_THREAD = 50

        def worker():
            for _ in range(PER_THREAD):
                ob.enqueue("d", "email:x@y", payload={"v": 1})

        threads = [threading.Thread(target=worker) for _ in range(N_THREADS)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert ob.stats().total == N_THREADS * PER_THREAD
        assert ob.stats().pending == N_THREADS * PER_THREAD

    def test_concurrent_mixed_ops(self):
        ob = DocOutbox()
        msgs = [ob.enqueue("d", "x") for _ in range(100)]

        def sender():
            for m in msgs[:50]:
                ob.mark_sent(m.message_id)

        def failer():
            for m in msgs[50:]:
                ob.mark_failed(m.message_id, "err")

        t1 = threading.Thread(target=sender)
        t2 = threading.Thread(target=failer)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        s = ob.stats()
        assert s.sent == 50
        assert s.failed == 50
        assert s.total == 100
