"""Comprehensive tests for the message_queue module (E74).

Coverage targets:
- MessagePriority / MessageStatus enums
- Message dataclass (fields, defaults, can_retry)
- MessageQueue: publish, consume, ack, nack, size, dead_letters, purge
- QueueFullError
- MessageBroker: lifecycle, publish, stats, queues
- Threading: concurrent publish + consume
- Scheduled messages (scheduled_at)
"""
from __future__ import annotations

import threading
import time
from uuid import uuid4

import pytest

from docstoolkit.message_queue import (
    Message,
    MessageBroker,
    MessagePriority,
    MessageQueue,
    MessageStatus,
    QueueConfig,
    QueueFullError,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_queue(name: str = "test", max_size: int = 0) -> MessageQueue:
    cfg = QueueConfig(max_size=max_size)
    return MessageQueue(name=name, config=cfg)


def make_message(topic: str = "t", priority: MessagePriority = MessagePriority.NORMAL,
                 scheduled_at: float = 0.0, max_retries: int = 3) -> Message:
    return Message(
        topic=topic,
        priority=priority,
        scheduled_at=scheduled_at,
        max_retries=max_retries,
    )


# ===========================================================================
# 1. MessagePriority enum
# ===========================================================================

class TestMessagePriority:
    def test_low_value(self):
        assert MessagePriority.LOW == 1

    def test_normal_value(self):
        assert MessagePriority.NORMAL == 5

    def test_high_value(self):
        assert MessagePriority.HIGH == 10

    def test_critical_value(self):
        assert MessagePriority.CRITICAL == 20

    def test_ordering(self):
        assert MessagePriority.LOW < MessagePriority.NORMAL
        assert MessagePriority.NORMAL < MessagePriority.HIGH
        assert MessagePriority.HIGH < MessagePriority.CRITICAL

    def test_is_int(self):
        assert isinstance(MessagePriority.NORMAL, int)

    def test_members_count(self):
        assert len(MessagePriority) == 4


# ===========================================================================
# 2. MessageStatus enum
# ===========================================================================

class TestMessageStatus:
    def test_pending_exists(self):
        assert MessageStatus.PENDING.value == "PENDING"

    def test_processing_exists(self):
        assert MessageStatus.PROCESSING.value == "PROCESSING"

    def test_completed_exists(self):
        assert MessageStatus.COMPLETED.value == "COMPLETED"

    def test_failed_exists(self):
        assert MessageStatus.FAILED.value == "FAILED"

    def test_dead_letter_exists(self):
        assert MessageStatus.DEAD_LETTER.value == "DEAD_LETTER"

    def test_members_count(self):
        assert len(MessageStatus) == 5


# ===========================================================================
# 3. Message dataclass
# ===========================================================================

class TestMessage:
    def test_topic_required(self):
        m = Message(topic="hello")
        assert m.topic == "hello"

    def test_default_payload_empty_dict(self):
        m = Message(topic="t")
        assert m.payload == {}

    def test_payload_not_shared(self):
        m1 = Message(topic="t")
        m2 = Message(topic="t")
        m1.payload["x"] = 1
        assert "x" not in m2.payload

    def test_default_priority(self):
        m = Message(topic="t")
        assert m.priority == MessagePriority.NORMAL

    def test_default_status(self):
        m = Message(topic="t")
        assert m.status == MessageStatus.PENDING

    def test_created_at_set(self):
        before = time.time()
        m = Message(topic="t")
        after = time.time()
        assert before <= m.created_at <= after

    def test_default_attempts(self):
        m = Message(topic="t")
        assert m.attempts == 0

    def test_default_max_retries(self):
        m = Message(topic="t")
        assert m.max_retries == 3

    def test_default_scheduled_at(self):
        m = Message(topic="t")
        assert m.scheduled_at == 0.0

    def test_message_id_hex_string(self):
        m = Message(topic="t")
        assert isinstance(m.message_id, str)
        assert len(m.message_id) == 32  # uuid4().hex

    def test_message_ids_unique(self):
        ids = {Message(topic="t").message_id for _ in range(100)}
        assert len(ids) == 100

    def test_can_retry_fresh(self):
        m = Message(topic="t", max_retries=3)
        assert m.can_retry() is True

    def test_can_retry_at_limit(self):
        m = Message(topic="t", max_retries=3)
        m.attempts = 3
        assert m.can_retry() is False

    def test_can_retry_beyond_limit(self):
        m = Message(topic="t", max_retries=3)
        m.attempts = 10
        assert m.can_retry() is False

    def test_can_retry_zero_retries(self):
        m = Message(topic="t", max_retries=0)
        assert m.can_retry() is False

    def test_can_retry_one_retry_remaining(self):
        m = Message(topic="t", max_retries=3)
        m.attempts = 2
        assert m.can_retry() is True

    def test_custom_priority(self):
        m = Message(topic="t", priority=MessagePriority.CRITICAL)
        assert m.priority == MessagePriority.CRITICAL

    def test_custom_payload(self):
        m = Message(topic="t", payload={"key": "value"})
        assert m.payload["key"] == "value"

    def test_custom_message_id(self):
        m = Message(topic="t", message_id="abc123")
        assert m.message_id == "abc123"


# ===========================================================================
# 4. QueueConfig
# ===========================================================================

class TestQueueConfig:
    def test_defaults(self):
        cfg = QueueConfig()
        assert cfg.max_size == 0
        assert cfg.default_priority == MessagePriority.NORMAL

    def test_custom_max_size(self):
        cfg = QueueConfig(max_size=10)
        assert cfg.max_size == 10

    def test_custom_default_priority(self):
        cfg = QueueConfig(default_priority=MessagePriority.HIGH)
        assert cfg.default_priority == MessagePriority.HIGH


# ===========================================================================
# 5. MessageQueue — basic operations
# ===========================================================================

class TestMessageQueuePublishConsume:
    def test_consume_empty_returns_none(self):
        q = make_queue()
        assert q.consume() is None

    def test_publish_then_consume(self):
        q = make_queue()
        m = make_message()
        q.publish(m)
        result = q.consume()
        assert result is m

    def test_consume_sets_processing(self):
        q = make_queue()
        m = make_message()
        q.publish(m)
        result = q.consume()
        assert result.status == MessageStatus.PROCESSING

    def test_consume_removes_from_pending(self):
        q = make_queue()
        q.publish(make_message())
        q.consume()
        assert q.size() == 0

    def test_priority_ordering_high_before_low(self):
        q = make_queue()
        low = make_message(priority=MessagePriority.LOW)
        high = make_message(priority=MessagePriority.HIGH)
        q.publish(low)
        q.publish(high)
        first = q.consume()
        assert first.priority == MessagePriority.HIGH

    def test_priority_ordering_critical_first(self):
        q = make_queue()
        for p in [MessagePriority.LOW, MessagePriority.NORMAL,
                  MessagePriority.HIGH, MessagePriority.CRITICAL]:
            q.publish(make_message(priority=p))
        assert q.consume().priority == MessagePriority.CRITICAL

    def test_priority_all_levels_in_order(self):
        q = make_queue()
        expected = [
            MessagePriority.CRITICAL,
            MessagePriority.HIGH,
            MessagePriority.NORMAL,
            MessagePriority.LOW,
        ]
        for p in expected:
            q.publish(make_message(priority=p))
        results = [q.consume().priority for _ in range(4)]
        assert results == expected

    def test_consume_topic_filter(self):
        q = make_queue()
        q.publish(make_message(topic="a"))
        q.publish(make_message(topic="b"))
        result = q.consume(topic="b")
        assert result.topic == "b"

    def test_consume_topic_filter_no_match_returns_none(self):
        q = make_queue()
        q.publish(make_message(topic="a"))
        assert q.consume(topic="z") is None

    def test_consume_leaves_other_topics(self):
        q = make_queue()
        q.publish(make_message(topic="a"))
        q.publish(make_message(topic="b"))
        q.consume(topic="a")
        assert q.size(topic="b") == 1


# ===========================================================================
# 6. MessageQueue — ack / nack
# ===========================================================================

class TestMessageQueueAckNack:
    def test_ack_sets_completed(self):
        q = make_queue()
        m = make_message()
        q.publish(m)
        q.consume()
        assert q.ack(m.message_id) is True
        assert m.status == MessageStatus.COMPLETED

    def test_ack_unknown_id_returns_false(self):
        q = make_queue()
        assert q.ack("nonexistent") is False

    def test_nack_increments_attempts(self):
        q = make_queue()
        m = make_message(max_retries=3)
        q.publish(m)
        q.consume()
        q.nack(m.message_id)
        assert m.attempts == 1

    def test_nack_retries_sets_pending(self):
        q = make_queue()
        m = make_message(max_retries=3)
        q.publish(m)
        q.consume()
        q.nack(m.message_id)
        assert m.status == MessageStatus.PENDING

    def test_nack_exhausted_sets_dead_letter(self):
        q = make_queue()
        m = make_message(max_retries=1)
        q.publish(m)
        q.consume()
        q.nack(m.message_id)  # attempts=1, can_retry False → DEAD_LETTER
        assert m.status == MessageStatus.DEAD_LETTER

    def test_nack_retry_cycle(self):
        q = make_queue()
        m = make_message(max_retries=2)
        q.publish(m)
        # Round 1
        q.consume()
        q.nack(m.message_id)
        assert m.status == MessageStatus.PENDING
        # Round 2
        q.consume()
        q.nack(m.message_id)
        assert m.status == MessageStatus.DEAD_LETTER

    def test_nack_unknown_id_returns_false(self):
        q = make_queue()
        assert q.nack("nonexistent") is False

    def test_dead_letters_empty_initially(self):
        q = make_queue()
        assert q.dead_letters() == []

    def test_dead_letters_after_exhaustion(self):
        q = make_queue()
        m = make_message(max_retries=0)
        q.publish(m)
        q.consume()
        q.nack(m.message_id)
        dl = q.dead_letters()
        assert len(dl) == 1
        assert dl[0] is m

    def test_dead_letters_multiple(self):
        q = make_queue()
        for _ in range(3):
            m = make_message(max_retries=0)
            q.publish(m)
            q.consume()
            q.nack(m.message_id)
        assert len(q.dead_letters()) == 3


# ===========================================================================
# 7. MessageQueue — size / purge
# ===========================================================================

class TestMessageQueueSizePurge:
    def test_size_empty(self):
        q = make_queue()
        assert q.size() == 0

    def test_size_after_publish(self):
        q = make_queue()
        for _ in range(5):
            q.publish(make_message())
        assert q.size() == 5

    def test_size_topic_filter(self):
        q = make_queue()
        for _ in range(3):
            q.publish(make_message(topic="a"))
        for _ in range(2):
            q.publish(make_message(topic="b"))
        assert q.size(topic="a") == 3
        assert q.size(topic="b") == 2

    def test_size_decreases_after_consume(self):
        q = make_queue()
        q.publish(make_message())
        q.consume()
        assert q.size() == 0

    def test_purge_all(self):
        q = make_queue()
        for _ in range(4):
            q.publish(make_message())
        removed = q.purge()
        assert removed == 4
        assert q.size() == 0

    def test_purge_topic(self):
        q = make_queue()
        for _ in range(3):
            q.publish(make_message(topic="a"))
        for _ in range(2):
            q.publish(make_message(topic="b"))
        removed = q.purge(topic="a")
        assert removed == 3
        assert q.size(topic="a") == 0
        assert q.size(topic="b") == 2

    def test_purge_empty_returns_zero(self):
        q = make_queue()
        assert q.purge() == 0

    def test_purge_does_not_remove_processing(self):
        q = make_queue()
        m = make_message()
        q.publish(m)
        q.consume()          # status → PROCESSING
        q.purge()
        # message still present internally (as PROCESSING)
        assert m.status == MessageStatus.PROCESSING

    def test_purge_does_not_remove_dead_letters(self):
        q = make_queue()
        m = make_message(max_retries=0)
        q.publish(m)
        q.consume()
        q.nack(m.message_id)
        q.purge()
        assert len(q.dead_letters()) == 1


# ===========================================================================
# 8. QueueFullError
# ===========================================================================

class TestQueueFullError:
    def test_full_error_raised(self):
        q = make_queue(max_size=2)
        q.publish(make_message())
        q.publish(make_message())
        with pytest.raises(QueueFullError):
            q.publish(make_message())

    def test_full_error_is_exception(self):
        assert issubclass(QueueFullError, Exception)

    def test_no_error_when_unlimited(self):
        q = make_queue(max_size=0)
        for _ in range(50):
            q.publish(make_message())
        assert q.size() == 50

    def test_full_error_after_consume_allows_publish(self):
        q = make_queue(max_size=1)
        m = make_message()
        q.publish(m)
        with pytest.raises(QueueFullError):
            q.publish(make_message())
        q.consume()
        q.ack(m.message_id)
        # Now one slot is free (PENDING count == 0)
        q.publish(make_message())
        assert q.size() == 1

    def test_full_error_message_contains_queue_name(self):
        q = MessageQueue(name="myqueue", config=QueueConfig(max_size=1))
        q.publish(make_message())
        with pytest.raises(QueueFullError, match="myqueue"):
            q.publish(make_message())


# ===========================================================================
# 9. Scheduled messages
# ===========================================================================

class TestScheduledMessages:
    def test_future_message_not_returned(self):
        q = make_queue()
        future = time.time() + 9999
        m = make_message(scheduled_at=future)
        q.publish(m)
        assert q.consume(now=time.time()) is None

    def test_immediate_zero_always_returned(self):
        q = make_queue()
        m = make_message(scheduled_at=0.0)
        q.publish(m)
        assert q.consume() is m

    def test_past_scheduled_returned(self):
        q = make_queue()
        past = time.time() - 100
        m = make_message(scheduled_at=past)
        q.publish(m)
        assert q.consume() is m

    def test_exactly_now_scheduled_returned(self):
        now = time.time()
        q = make_queue()
        m = make_message(scheduled_at=now)
        q.publish(m)
        assert q.consume(now=now) is m

    def test_future_not_returned_but_immediate_is(self):
        q = make_queue()
        future = time.time() + 9999
        delayed = make_message(topic="delayed", scheduled_at=future)
        immediate = make_message(topic="immediate", scheduled_at=0.0)
        q.publish(delayed)
        q.publish(immediate)
        result = q.consume(now=time.time())
        assert result.topic == "immediate"

    def test_scheduled_becomes_available(self):
        now = 1000.0
        q = make_queue()
        m = make_message(scheduled_at=1001.0)
        q.publish(m)
        assert q.consume(now=now) is None
        assert q.consume(now=1001.0) is m


# ===========================================================================
# 10. MessageBroker
# ===========================================================================

class TestMessageBroker:
    def test_create_queue_returns_queue(self):
        broker = MessageBroker()
        q = broker.create_queue("orders")
        assert isinstance(q, MessageQueue)

    def test_create_queue_name(self):
        broker = MessageBroker()
        q = broker.create_queue("events")
        assert q.name == "events"

    def test_get_queue_existing(self):
        broker = MessageBroker()
        q = broker.create_queue("q1")
        assert broker.get_queue("q1") is q

    def test_get_queue_missing_returns_none(self):
        broker = MessageBroker()
        assert broker.get_queue("missing") is None

    def test_delete_queue_returns_true(self):
        broker = MessageBroker()
        broker.create_queue("q")
        assert broker.delete_queue("q") is True

    def test_delete_queue_missing_returns_false(self):
        broker = MessageBroker()
        assert broker.delete_queue("nope") is False

    def test_delete_queue_removes_it(self):
        broker = MessageBroker()
        broker.create_queue("q")
        broker.delete_queue("q")
        assert broker.get_queue("q") is None

    def test_queues_list(self):
        broker = MessageBroker()
        broker.create_queue("b")
        broker.create_queue("a")
        broker.create_queue("c")
        assert broker.queues() == ["a", "b", "c"]

    def test_queues_empty_initially(self):
        broker = MessageBroker()
        assert broker.queues() == []

    def test_publish_returns_message(self):
        broker = MessageBroker()
        broker.create_queue("q")
        msg = broker.publish("q", topic="t", payload={"x": 1})
        assert isinstance(msg, Message)

    def test_publish_message_in_queue(self):
        broker = MessageBroker()
        broker.create_queue("q")
        broker.publish("q", topic="t")
        q = broker.get_queue("q")
        assert q.size() == 1

    def test_publish_missing_queue_raises_key_error(self):
        broker = MessageBroker()
        with pytest.raises(KeyError):
            broker.publish("nonexistent", topic="t")

    def test_publish_with_priority(self):
        broker = MessageBroker()
        broker.create_queue("q")
        msg = broker.publish("q", topic="t", priority=MessagePriority.CRITICAL)
        assert msg.priority == MessagePriority.CRITICAL

    def test_publish_uses_default_priority(self):
        broker = MessageBroker()
        cfg = QueueConfig(default_priority=MessagePriority.HIGH)
        broker.create_queue("q", config=cfg)
        msg = broker.publish("q", topic="t")
        assert msg.priority == MessagePriority.HIGH

    def test_stats_empty(self):
        broker = MessageBroker()
        broker.create_queue("q")
        s = broker.stats()
        assert s["q"]["size"] == 0
        assert s["q"]["dead_letters"] == 0

    def test_stats_with_messages(self):
        broker = MessageBroker()
        broker.create_queue("q")
        broker.publish("q", topic="t")
        broker.publish("q", topic="t")
        s = broker.stats()
        assert s["q"]["size"] == 2

    def test_stats_dead_letters(self):
        broker = MessageBroker()
        broker.create_queue("q")
        msg = broker.publish("q", topic="t", max_retries=0)
        q = broker.get_queue("q")
        q.consume()
        q.nack(msg.message_id)
        s = broker.stats()
        assert s["q"]["dead_letters"] == 1

    def test_stats_multiple_queues(self):
        broker = MessageBroker()
        broker.create_queue("a")
        broker.create_queue("b")
        broker.publish("a", topic="t")
        broker.publish("b", topic="t")
        broker.publish("b", topic="t")
        s = broker.stats()
        assert s["a"]["size"] == 1
        assert s["b"]["size"] == 2


# ===========================================================================
# 11. Threading — concurrent publish + consume
# ===========================================================================

class TestThreading:
    def test_concurrent_publish(self):
        q = make_queue()
        errors = []

        def publisher():
            try:
                for _ in range(20):
                    q.publish(make_message())
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=publisher) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors
        assert q.size() == 100

    def test_concurrent_consume(self):
        q = make_queue()
        for _ in range(50):
            q.publish(make_message())

        consumed = []
        lock = threading.Lock()
        errors = []

        def consumer():
            try:
                while True:
                    m = q.consume()
                    if m is None:
                        break
                    with lock:
                        consumed.append(m.message_id)
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=consumer) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors
        # No duplicates: each message consumed exactly once
        assert len(consumed) == len(set(consumed))

    def test_concurrent_publish_consume(self):
        q = make_queue()
        produced = []
        consumed = []
        p_lock = threading.Lock()
        c_lock = threading.Lock()
        errors = []

        def publisher():
            try:
                for _ in range(30):
                    m = make_message()
                    q.publish(m)
                    with p_lock:
                        produced.append(m.message_id)
            except Exception as exc:
                errors.append(exc)

        def consumer():
            try:
                for _ in range(30):
                    m = q.consume()
                    if m:
                        with c_lock:
                            consumed.append(m.message_id)
            except Exception as exc:
                errors.append(exc)

        threads = (
            [threading.Thread(target=publisher) for _ in range(3)]
            + [threading.Thread(target=consumer) for _ in range(3)]
        )
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors
        # No message was consumed more than once
        assert len(consumed) == len(set(consumed))

    def test_concurrent_broker_publish(self):
        broker = MessageBroker()
        broker.create_queue("shared")
        errors = []

        def worker():
            try:
                for _ in range(10):
                    broker.publish("shared", topic="t")
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=worker) for _ in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors
        assert broker.get_queue("shared").size() == 80
