"""Dead letter queue: failed jobs, retry, and poison pill detection."""
from docstoolkit.dlq.item import DeadLetterItem, FailureReason
from docstoolkit.dlq.queue import DeadLetterQueue
from docstoolkit.dlq.retry import RetryPolicy, RetryResult, execute_with_retry
from docstoolkit.dlq.poison import PoisonPillDetector, PoisonReport

__all__ = [
    "DeadLetterItem", "FailureReason",
    "DeadLetterQueue",
    "RetryPolicy", "RetryResult", "execute_with_retry",
    "PoisonPillDetector", "PoisonReport",
]
