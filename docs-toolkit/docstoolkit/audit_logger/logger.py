"""High-level AuditLogger facade."""
import json
from pathlib import Path
from typing import Optional

from docstoolkit.audit_logger.event import AuditAction, AuditEvent
from docstoolkit.audit_logger.store import AuditStore


class AuditLogger:
    """Convenience wrapper around AuditStore."""

    def __init__(self, store: Optional[AuditStore] = None) -> None:
        self._store = store if store is not None else AuditStore()

    # ------------------------------------------------------------------
    # Write
    # ------------------------------------------------------------------

    def log(
        self,
        action: AuditAction,
        actor: str,
        resource: str,
        **kwargs,
    ) -> AuditEvent:
        """Create, persist, and return an AuditEvent.

        *kwargs* may contain: resource_id, details, outcome,
        ip_address, session_id.
        """
        event = AuditEvent(action=action, actor=actor, resource=resource, **kwargs)
        self._store.record(event)
        return event

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------

    def query(self, **kwargs) -> "list[AuditEvent]":
        """Delegate to AuditStore.query with the same keyword arguments."""
        return self._store.query(**kwargs)

    def recent(self, n: int = 20) -> "list[AuditEvent]":
        """Return the *n* most recent events."""
        return self._store.recent(n)

    # ------------------------------------------------------------------
    # Analytics
    # ------------------------------------------------------------------

    def actor_summary(self, actor: str) -> dict:
        """Return {action_name: count} for every action taken by *actor*."""
        events = self._store.query(actor=actor, limit=10_000)
        summary: dict[str, int] = {}
        for ev in events:
            key = ev.action.value
            summary[key] = summary.get(key, 0) + 1
        return summary

    # ------------------------------------------------------------------
    # Export
    # ------------------------------------------------------------------

    def export_jsonl(self, path: "str | Path") -> int:
        """Write all events as JSONL to *path*; return count written."""
        all_events = self._store.query(limit=10_000_000)
        path = Path(path)
        written = 0
        with path.open("w", encoding="utf-8") as fh:
            for ev in all_events:
                fh.write(json.dumps(ev.to_dict(), ensure_ascii=False) + "\n")
                written += 1
        return written
