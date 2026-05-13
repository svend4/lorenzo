"""Active learning triggers — decide when to enqueue a query for labelling.

Each trigger implements LearningTrigger.should_queue() and returns a
(should_add: bool, priority: float, reason: str) tuple.

Usage:
    trigger = CompositeTrigger([
        LowConfidenceTrigger(threshold=0.4),
        DownThumbTrigger(),
    ])
    item_id = auto_enqueue(query, passages, queue, trigger, context)
"""
import json
import uuid
from abc import ABC, abstractmethod
from datetime import datetime

from docstoolkit.rag.types import Passage
from docstoolkit.active_learning.queue import LearningItem, LearningQueue


class LearningTrigger(ABC):
    """Abstract base for active-learning triggers."""

    @abstractmethod
    def should_queue(
        self,
        query: str,
        passages: list[Passage],
        context: dict,
    ) -> tuple[bool, float, str]:
        """Return (should_add, priority 0-1, reason string)."""


# ---------------------------------------------------------------------------
# Concrete triggers
# ---------------------------------------------------------------------------

class LowConfidenceTrigger(LearningTrigger):
    """Fires when the top retrieved passage has a score below *threshold*,
    or when no passages were returned at all.
    """

    def __init__(self, threshold: float = 0.4):
        self.threshold = threshold

    def should_queue(
        self,
        query: str,
        passages: list[Passage],
        context: dict,
    ) -> tuple[bool, float, str]:
        if not passages:
            return True, 1.0, "low_confidence"
        max_score = max(p.score for p in passages)
        if max_score < self.threshold:
            priority = 1.0 - max_score  # closer to 0 → higher priority
            return True, priority, "low_confidence"
        return False, 0.0, "low_confidence"


class DownThumbTrigger(LearningTrigger):
    """Fires when the user gave a thumbs-down signal via context["thumbs"]."""

    PRIORITY = 0.8

    def should_queue(
        self,
        query: str,
        passages: list[Passage],
        context: dict,
    ) -> tuple[bool, float, str]:
        if context.get("thumbs") == "down":
            return True, self.PRIORITY, "down_thumb"
        return False, 0.0, "down_thumb"


class GoldenMismatchTrigger(LearningTrigger):
    """Fires when a query is similar to a known golden query but the
    top-1 passage does NOT match the expected documents.

    Similarity is Jaccard on lowercased tokens > 0.6.
    Expected docs come from *golden_queries* mapping:
        {query_string: [expected_doc_id, ...]}
    """

    PRIORITY = 0.9
    JACCARD_THRESHOLD = 0.6

    def __init__(self, golden_queries: "dict[str, list[str]] | set[str]"):
        # Accept either {query: [doc_ids]} or a plain set of query strings
        # (for backward compat with the spec which says set[str])
        if isinstance(golden_queries, set):
            self._golden: dict[str, list[str]] = {q: [] for q in golden_queries}
        else:
            self._golden = dict(golden_queries)

    # ---- helpers ----

    @staticmethod
    def _tokens(text: str) -> set[str]:
        return set(text.lower().split())

    @classmethod
    def _jaccard(cls, a: str, b: str) -> float:
        ta, tb = cls._tokens(a), cls._tokens(b)
        if not ta and not tb:
            return 1.0
        inter = ta & tb
        union = ta | tb
        return len(inter) / len(union) if union else 0.0

    def should_queue(
        self,
        query: str,
        passages: list[Passage],
        context: dict,
    ) -> tuple[bool, float, str]:
        top_doc_id = passages[0].doc_id if passages else ""

        for golden_q, expected_docs in self._golden.items():
            sim = self._jaccard(query, golden_q)
            if sim <= self.JACCARD_THRESHOLD:
                continue
            # Similar enough — check if top-1 is wrong
            if expected_docs and top_doc_id not in expected_docs:
                return True, self.PRIORITY, "golden_mismatch"
            # If no expected_docs recorded, treat any similar query as a hit
            if not expected_docs:
                return True, self.PRIORITY, "golden_mismatch"

        return False, 0.0, "golden_mismatch"


class CompositeTrigger(LearningTrigger):
    """Fires if ANY of the child triggers fires; priority = max of all."""

    def __init__(self, triggers: list[LearningTrigger]):
        self._triggers = list(triggers)

    def should_queue(
        self,
        query: str,
        passages: list[Passage],
        context: dict,
    ) -> tuple[bool, float, str]:
        best_priority = 0.0
        best_reason = ""
        fired = False

        for trigger in self._triggers:
            should, priority, reason = trigger.should_queue(query, passages, context)
            if should:
                fired = True
                if priority > best_priority:
                    best_priority = priority
                    best_reason = reason

        return fired, best_priority, best_reason


# ---------------------------------------------------------------------------
# auto_enqueue helper
# ---------------------------------------------------------------------------

def auto_enqueue(
    query: str,
    passages: list[Passage],
    queue: LearningQueue,
    trigger: LearningTrigger,
    context: dict | None = None,
) -> "str | None":
    """Check trigger; if fired, build a LearningItem and add it to *queue*.

    Returns the new item's id, or None if the trigger did not fire.
    """
    if context is None:
        context = {}

    should, priority, reason = trigger.should_queue(query, passages, context)
    if not should:
        return None

    passages_data = [
        {"text": p.text, "doc_id": p.doc_id, "score": p.score}
        for p in passages
    ]

    suggested_answer = context.get("suggested_answer", "")

    item = LearningItem(
        id=uuid.uuid4().hex[:16],
        query=query,
        passages_json=json.dumps(passages_data, ensure_ascii=False),
        suggested_answer=suggested_answer,
        priority=priority,
        reason=reason,
        created_ts=datetime.now().isoformat(timespec="seconds"),
    )
    return queue.add(item)
