"""Record and replay sequences of document operations."""
from __future__ import annotations

import threading
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Optional, Protocol


class OperationType(Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    TAG = "tag"
    UNTAG = "untag"
    MOVE = "move"
    COPY = "copy"
    OTHER = "other"


@dataclass
class Operation:
    op_id: int
    doc_id: str
    op_type: OperationType
    params: dict = field(default_factory=dict)
    timestamp: float = 0.0
    actor: Optional[str] = None


@dataclass
class ReplaySession:
    session_id: str
    operations: list = field(default_factory=list)
    started_at: float = 0.0
    ended_at: Optional[float] = None
    name: Optional[str] = None


@dataclass
class ReplayResult:
    session_id: str
    total_operations: int
    replayed: int
    skipped: int
    errors: list = field(default_factory=list)
    duration_seconds: float = 0.0


class OperationHandler(Protocol):
    def __call__(self, op: Operation) -> bool:
        ...


class DocReplay:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._sessions: dict[str, ReplaySession] = {}
        self._op_counter = 0

    def _now(self, now: Optional[float]) -> float:
        return now if now is not None else time.time()

    def start_recording(
        self, name: Optional[str] = None, now: Optional[float] = None
    ) -> str:
        with self._lock:
            session_id = str(uuid.uuid4())
            session = ReplaySession(
                session_id=session_id,
                operations=[],
                started_at=self._now(now),
                ended_at=None,
                name=name,
            )
            self._sessions[session_id] = session
            return session_id

    def stop_recording(
        self, session_id: str, now: Optional[float] = None
    ) -> Optional[ReplaySession]:
        with self._lock:
            session = self._sessions.get(session_id)
            if session is None:
                return None
            if session.ended_at is not None:
                return session
            session.ended_at = self._now(now)
            return session

    def record(
        self,
        session_id: str,
        doc_id: str,
        op_type: OperationType,
        params: Optional[dict] = None,
        actor: Optional[str] = None,
        now: Optional[float] = None,
    ) -> Optional[Operation]:
        with self._lock:
            session = self._sessions.get(session_id)
            if session is None:
                return None
            if session.ended_at is not None:
                return None
            self._op_counter += 1
            op = Operation(
                op_id=self._op_counter,
                doc_id=doc_id,
                op_type=op_type,
                params=dict(params) if params else {},
                timestamp=self._now(now),
                actor=actor,
            )
            session.operations.append(op)
            return op

    def get_session(self, session_id: str) -> Optional[ReplaySession]:
        with self._lock:
            return self._sessions.get(session_id)

    def list_sessions(self, active_only: bool = False) -> list:
        with self._lock:
            sessions = list(self._sessions.values())
            if active_only:
                sessions = [s for s in sessions if s.ended_at is None]
            return sessions

    def _run_replay(
        self,
        session: ReplaySession,
        handler: Callable,
        filter_op_types: Optional[list] = None,
        filter_doc_ids: Optional[list] = None,
        start_op: Optional[int] = None,
        end_op: Optional[int] = None,
    ) -> ReplayResult:
        replayed = 0
        skipped = 0
        errors: list = []
        total = len(session.operations)
        start_ts = time.time()

        op_types_set = set(filter_op_types) if filter_op_types else None
        doc_ids_set = set(filter_doc_ids) if filter_doc_ids else None

        for idx, op in enumerate(session.operations):
            if start_op is not None and idx < start_op:
                skipped += 1
                continue
            if end_op is not None and idx >= end_op:
                skipped += 1
                continue
            if op_types_set is not None and op.op_type not in op_types_set:
                skipped += 1
                continue
            if doc_ids_set is not None and op.doc_id not in doc_ids_set:
                skipped += 1
                continue
            try:
                result = handler(op)
                if result:
                    replayed += 1
                else:
                    skipped += 1
            except Exception as exc:
                errors.append(f"op {op.op_id}: {exc}")
                skipped += 1

        duration = time.time() - start_ts
        return ReplayResult(
            session_id=session.session_id,
            total_operations=total,
            replayed=replayed,
            skipped=skipped,
            errors=errors,
            duration_seconds=duration,
        )

    def replay(
        self,
        session_id: str,
        handler: Callable,
        filter_op_types: Optional[list] = None,
        filter_doc_ids: Optional[list] = None,
    ) -> ReplayResult:
        with self._lock:
            session = self._sessions.get(session_id)
            if session is None:
                return ReplayResult(
                    session_id=session_id,
                    total_operations=0,
                    replayed=0,
                    skipped=0,
                    errors=["session not found"],
                    duration_seconds=0.0,
                )
            # snapshot ops to allow handler to be invoked outside lock
            snapshot = ReplaySession(
                session_id=session.session_id,
                operations=list(session.operations),
                started_at=session.started_at,
                ended_at=session.ended_at,
                name=session.name,
            )
        return self._run_replay(
            snapshot,
            handler,
            filter_op_types=filter_op_types,
            filter_doc_ids=filter_doc_ids,
        )

    def replay_partial(
        self,
        session_id: str,
        start_op: int,
        end_op: int,
        handler: Callable,
    ) -> ReplayResult:
        with self._lock:
            session = self._sessions.get(session_id)
            if session is None:
                return ReplayResult(
                    session_id=session_id,
                    total_operations=0,
                    replayed=0,
                    skipped=0,
                    errors=["session not found"],
                    duration_seconds=0.0,
                )
            snapshot = ReplaySession(
                session_id=session.session_id,
                operations=list(session.operations),
                started_at=session.started_at,
                ended_at=session.ended_at,
                name=session.name,
            )
        return self._run_replay(
            snapshot, handler, start_op=start_op, end_op=end_op
        )

    def dry_run(self, session_id: str, handler: Callable) -> ReplayResult:
        return self.replay(session_id, handler)

    def delete_session(self, session_id: str) -> bool:
        with self._lock:
            if session_id in self._sessions:
                del self._sessions[session_id]
                return True
            return False

    def operations_for_doc(
        self, session_id: str, doc_id: str
    ) -> list:
        with self._lock:
            session = self._sessions.get(session_id)
            if session is None:
                return []
            return [op for op in session.operations if op.doc_id == doc_id]

    def operations_by_type(
        self, session_id: str, op_type: OperationType
    ) -> list:
        with self._lock:
            session = self._sessions.get(session_id)
            if session is None:
                return []
            return [op for op in session.operations if op.op_type == op_type]

    def merge_sessions(
        self, session_ids: list, new_name: Optional[str] = None
    ) -> Optional[ReplaySession]:
        with self._lock:
            sessions = []
            for sid in session_ids:
                s = self._sessions.get(sid)
                if s is None:
                    return None
                sessions.append(s)
            if not sessions:
                return None

            all_ops: list = []
            for s in sessions:
                all_ops.extend(s.operations)
            all_ops.sort(key=lambda o: (o.timestamp, o.op_id))

            started = min(s.started_at for s in sessions)
            ended_values = [s.ended_at for s in sessions if s.ended_at is not None]
            ended = max(ended_values) if len(ended_values) == len(sessions) else None

            new_id = str(uuid.uuid4())
            merged = ReplaySession(
                session_id=new_id,
                operations=all_ops,
                started_at=started,
                ended_at=ended,
                name=new_name,
            )
            self._sessions[new_id] = merged
            return merged

    @property
    def total_sessions(self) -> int:
        with self._lock:
            return len(self._sessions)

    @property
    def total_operations(self) -> int:
        with self._lock:
            return sum(len(s.operations) for s in self._sessions.values())

    def clear(self) -> None:
        with self._lock:
            self._sessions.clear()
            self._op_counter = 0
