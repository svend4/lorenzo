"""Dead letter queue: failed jobs, retry, poison pill detection, and replay."""
from docstoolkit.dlq.item import DeadLetterItem, FailureReason
from docstoolkit.dlq.queue import DeadLetterQueue
from docstoolkit.dlq.retry import RetryPolicy, RetryResult, execute_with_retry
from docstoolkit.dlq.poison import PoisonPillDetector, PoisonReport
from docstoolkit.dlq.replay import ReplayFilter, ReplayResult, ReplayEngine, replay_dlq

__all__ = [
    "DeadLetterItem", "FailureReason",
    "DeadLetterQueue",
    "RetryPolicy", "RetryResult", "execute_with_retry",
    "PoisonPillDetector", "PoisonReport",
    "ReplayFilter", "ReplayResult", "ReplayEngine", "replay_dlq",
]
