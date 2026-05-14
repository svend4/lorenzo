"""TieredMemory: unified interface to all three memory tiers."""
import uuid
from datetime import datetime, timezone

from docstoolkit.memory.tiers import (
    WorkingMemory,
    RecallMemory,
    ArchivalMemory,
    RecallItem,
    ArchivalFact,
)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class TieredMemory:
    """Unified interface to all three memory tiers."""

    def __init__(
        self,
        db_path: str = ":memory:",
        user_id: str = "default",
        working_max: int = 20,
    ):
        self.working = WorkingMemory(max_messages=working_max)
        self.recall = RecallMemory(db_path=db_path, user_id=user_id)
        self.archival = ArchivalMemory(db_path=db_path, user_id=user_id)
        self._user_id = user_id

    def add_interaction(self, role: str, content: str) -> None:
        """Add to working memory AND persist to recall."""
        self.working.add(role, content)
        item = RecallItem(
            id=uuid.uuid4().hex[:16],
            content=content,
            role=role,
            ts=_now_iso(),
        )
        self.recall.store(item)

    def archive(self, text: str, tags: list = None, importance: float = 0.5) -> str:
        """Archive a compressed fact. Returns fact_id."""
        return self.archival.archive(text, tags=tags, importance=importance)

    def recall_search(self, query: str, top_k: int = 5) -> list:
        """Search recall memory."""
        return self.recall.search(query, top_k=top_k)

    def archival_search(self, query: str, top_k: int = 5) -> list:
        """Search archival memory."""
        return self.archival.search(query, top_k=top_k)

    def forget(self, fact_id: str) -> bool:
        """Remove from archival memory."""
        return self.archival.forget(fact_id)

    def stats(self) -> dict:
        """Return {working_messages, recall_count, archival_count, user_id}."""
        return {
            "working_messages": len(self.working.messages),
            "recall_count": self.recall.count(),
            "archival_count": self.archival.count(),
            "user_id": self._user_id,
        }

    def squash_working_to_recall(self) -> int:
        """Move all working memory messages to recall. Clear working. Returns count moved."""
        messages = list(self.working.messages)
        count = len(messages)
        for m in messages:
            item = RecallItem(
                id=uuid.uuid4().hex[:16],
                content=m.get("content", ""),
                role=m.get("role", "user"),
                ts=m.get("ts", _now_iso()),
            )
            self.recall.store(item)
        self.working.clear()
        return count

    def context_for_llm(self, query: str = "", top_k_recall: int = 3) -> str:
        """Build LLM context string combining all tiers."""
        parts = []

        # Working memory section
        parts.append("[Working Memory]")
        working_ctx = self.working.to_context()
        parts.append(working_ctx if working_ctx else "(empty)")

        # Relevant recall section
        parts.append("")
        parts.append("[Relevant Recall]")
        if query:
            recall_items = self.recall.search(query, top_k=top_k_recall)
        else:
            recall_items = self.recall.list_recent(limit=top_k_recall)
        if recall_items:
            for item in recall_items:
                parts.append(f"{item.role} [{item.ts}]: {item.content}")
        else:
            parts.append("(none)")

        # Key facts section
        parts.append("")
        parts.append("[Key Facts]")
        arch_items = self.archival.search(query, top_k=3) if query else []
        if not arch_items:
            # fall back to most recent facts
            arch_items = self.archival.search("", top_k=3)
        if arch_items:
            for fact in arch_items:
                parts.append(f"- {fact.text}")
        else:
            parts.append("(none)")

        return "\n".join(parts)
