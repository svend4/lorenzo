"""Implementation of DocAssistantHistory and supporting types."""
from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# --------------------------------------------------------------------- TurnRole
class TurnRole(str, Enum):
    """Role of a participant in a conversation turn."""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL = "tool"


# --------------------------------------------------------------------- Turn
@dataclass
class Turn:
    """A single turn in a conversation."""

    turn_id: int
    role: TurnRole
    content: str
    created_at: float
    tokens: int = 0
    metadata: dict = field(default_factory=dict)


# --------------------------------------------------------------- Summary
@dataclass
class ConversationSummary:
    """Aggregate summary of a conversation."""

    conversation_id: str
    turn_count: int
    total_tokens: int
    started_at: float
    last_activity_at: float
    roles_used: set


# --------------------------------------------------------------------- helpers
def _estimate_tokens(content: str) -> int:
    """Rough token estimate based on word count."""
    if not content:
        return 0
    return len(content.split())


# -------------------------------------------------------- DocAssistantHistory
class DocAssistantHistory:
    """Thread-safe conversation history manager with context windows."""

    def __init__(self, max_turns: int = 50, max_tokens: int = 16000):
        if max_turns <= 0:
            raise ValueError("max_turns must be positive")
        if max_tokens <= 0:
            raise ValueError("max_tokens must be positive")
        self.max_turns = max_turns
        self.max_tokens = max_tokens
        self._lock = threading.Lock()
        # conversation_id -> list[Turn]
        self._conversations: dict = {}
        # conversation_id -> next turn id
        self._next_turn_ids: dict = {}
        # conversation_id -> started_at
        self._started_at: dict = {}

    # ----------------------------------------------------------- create
    def create_conversation(
        self,
        conversation_id: Optional[str] = None,
        system_prompt: Optional[str] = None,
        now: float = 0.0,
    ) -> str:
        """Create a new conversation, optionally seeded with a system prompt."""
        with self._lock:
            if conversation_id is None:
                conversation_id = uuid.uuid4().hex
            if conversation_id in self._conversations:
                raise ValueError(
                    f"Conversation '{conversation_id}' already exists"
                )
            self._conversations[conversation_id] = []
            self._next_turn_ids[conversation_id] = 1
            self._started_at[conversation_id] = now

            if system_prompt is not None:
                turn = Turn(
                    turn_id=self._next_turn_ids[conversation_id],
                    role=TurnRole.SYSTEM,
                    content=system_prompt,
                    created_at=now,
                    tokens=_estimate_tokens(system_prompt),
                    metadata={},
                )
                self._next_turn_ids[conversation_id] += 1
                self._conversations[conversation_id].append(turn)

            return conversation_id

    # ----------------------------------------------------------- add_turn
    def add_turn(
        self,
        conversation_id: str,
        role: TurnRole,
        content: str,
        tokens: Optional[int] = None,
        metadata: Optional[dict] = None,
        now: float = 0.0,
    ) -> Optional[Turn]:
        """Append a turn. Auto-prunes if limits are exceeded."""
        with self._lock:
            if conversation_id not in self._conversations:
                return None
            if not isinstance(role, TurnRole):
                raise TypeError("role must be a TurnRole instance")

            if tokens is None:
                tokens = _estimate_tokens(content)
            if tokens < 0:
                raise ValueError("tokens must be non-negative")

            turn = Turn(
                turn_id=self._next_turn_ids[conversation_id],
                role=role,
                content=content,
                created_at=now,
                tokens=tokens,
                metadata=dict(metadata) if metadata else {},
            )
            self._next_turn_ids[conversation_id] += 1
            self._conversations[conversation_id].append(turn)

            # Auto-prune
            self._prune_locked(conversation_id)
            return turn

    # ----------------------------------------------------------- get_turn
    def get_turn(self, conversation_id: str, turn_id: int) -> Optional[Turn]:
        with self._lock:
            turns = self._conversations.get(conversation_id)
            if turns is None:
                return None
            for t in turns:
                if t.turn_id == turn_id:
                    return t
            return None

    # ------------------------------------------------------ get_conversation
    def get_conversation(
        self, conversation_id: str, limit: Optional[int] = None
    ) -> list:
        with self._lock:
            turns = self._conversations.get(conversation_id)
            if turns is None:
                return []
            if limit is None:
                return list(turns)
            if limit <= 0:
                return []
            return list(turns[-limit:])

    # ----------------------------------------------------------- recent_turns
    def recent_turns(self, conversation_id: str, n: int = 10) -> list:
        with self._lock:
            turns = self._conversations.get(conversation_id)
            if not turns:
                return []
            if n <= 0:
                return []
            return list(turns[-n:])

    # ----------------------------------------------------------- last_turn
    def last_turn(self, conversation_id: str) -> Optional[Turn]:
        with self._lock:
            turns = self._conversations.get(conversation_id)
            if not turns:
                return None
            return turns[-1]

    # ----------------------------------------------------------- get_context
    def get_context(
        self, conversation_id: str, max_tokens: Optional[int] = None
    ) -> list:
        """Return most-recent turns fitting within token budget, oldest first.

        System prompts are always included.
        """
        with self._lock:
            turns = self._conversations.get(conversation_id)
            if not turns:
                return []
            budget = self.max_tokens if max_tokens is None else max_tokens
            if budget < 0:
                budget = 0

            # Separate system turns (always preserved)
            system_turns = [t for t in turns if t.role == TurnRole.SYSTEM]
            non_system = [t for t in turns if t.role != TurnRole.SYSTEM]

            system_tokens = sum(t.tokens for t in system_turns)
            remaining = budget - system_tokens

            selected_non_system: list = []
            if remaining > 0:
                used = 0
                for t in reversed(non_system):
                    if used + t.tokens > remaining:
                        break
                    selected_non_system.append(t)
                    used += t.tokens
                selected_non_system.reverse()

            # Merge while preserving chronological order (turn_id ascending)
            keep_ids = {t.turn_id for t in system_turns}
            keep_ids.update(t.turn_id for t in selected_non_system)
            return [t for t in turns if t.turn_id in keep_ids]

    # ------------------------------------------------------ clear_conversation
    def clear_conversation(self, conversation_id: str) -> int:
        """Remove all turns from a conversation. Returns number dropped."""
        with self._lock:
            turns = self._conversations.get(conversation_id)
            if turns is None:
                return 0
            count = len(turns)
            self._conversations[conversation_id] = []
            return count

    # ----------------------------------------------------------- prune_to_max
    def prune_to_max(self, conversation_id: str) -> int:
        """Apply max_turns / max_tokens. Returns count of dropped turns."""
        with self._lock:
            if conversation_id not in self._conversations:
                return 0
            return self._prune_locked(conversation_id)

    def _prune_locked(self, conversation_id: str) -> int:
        turns = self._conversations[conversation_id]
        dropped = 0

        def total_tokens() -> int:
            return sum(t.tokens for t in turns)

        # Drop oldest non-system until both limits respected
        i = 0
        # Need at least one pass-through; iterate while exceeding limits
        while (len(turns) > self.max_turns or total_tokens() > self.max_tokens):
            # Find first droppable (non-system) turn
            drop_index = -1
            for idx, t in enumerate(turns):
                if t.role != TurnRole.SYSTEM:
                    drop_index = idx
                    break
            if drop_index == -1:
                # Only system turns remain; cannot prune further
                break
            del turns[drop_index]
            dropped += 1
            i += 1
            if i > 10000:  # safety
                break
        return dropped

    # ----------------------------------------------------------- summary
    def summary(self, conversation_id: str) -> Optional[ConversationSummary]:
        with self._lock:
            turns = self._conversations.get(conversation_id)
            if turns is None:
                return None
            if not turns:
                started = self._started_at.get(conversation_id, 0.0)
                return ConversationSummary(
                    conversation_id=conversation_id,
                    turn_count=0,
                    total_tokens=0,
                    started_at=started,
                    last_activity_at=started,
                    roles_used=set(),
                )
            total_tokens = sum(t.tokens for t in turns)
            started = self._started_at.get(conversation_id, turns[0].created_at)
            last_activity = turns[-1].created_at
            roles = {t.role.value for t in turns}
            return ConversationSummary(
                conversation_id=conversation_id,
                turn_count=len(turns),
                total_tokens=total_tokens,
                started_at=started,
                last_activity_at=last_activity,
                roles_used=roles,
            )

    # ----------------------------------------------------------- properties
    @property
    def conversation_count(self) -> int:
        with self._lock:
            return len(self._conversations)

    @property
    def total_turns(self) -> int:
        with self._lock:
            return sum(len(v) for v in self._conversations.values())

    # ----------------------------------------------------- all_conversation_ids
    def all_conversation_ids(self) -> list:
        with self._lock:
            return list(self._conversations.keys())

    # --------------------------------------------------- delete_conversation
    def delete_conversation(self, conversation_id: str) -> bool:
        with self._lock:
            if conversation_id not in self._conversations:
                return False
            del self._conversations[conversation_id]
            self._next_turn_ids.pop(conversation_id, None)
            self._started_at.pop(conversation_id, None)
            return True

    # ----------------------------------------------------------- clear
    def clear(self) -> None:
        with self._lock:
            self._conversations.clear()
            self._next_turn_ids.clear()
            self._started_at.clear()
