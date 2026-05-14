from dataclasses import dataclass, field
from docstoolkit.audit.log import AuditLog


@dataclass
class VerificationReport:
    """Result of audit log chain verification."""
    total_events: int
    valid_count: int
    tampered_ids: list = field(default_factory=list)   # event_ids with bad hash
    broken_chain_ids: list = field(default_factory=list)  # where prev_hash mismatch

    def is_intact(self) -> bool:
        return not self.tampered_ids and not self.broken_chain_ids

    def summary(self) -> str:
        status = "INTACT" if self.is_intact() else "COMPROMISED"
        return (
            f"{status}: {self.valid_count}/{self.total_events} valid, "
            f"{len(self.tampered_ids)} tampered, "
            f"{len(self.broken_chain_ids)} chain breaks"
        )


class AuditVerifier:
    """Verifies integrity of an AuditLog."""

    def verify(self, log: AuditLog) -> VerificationReport:
        """Walk all events in seq order; verify each hash and chain.

        For each event:
        1. event.verify() → checks event_hash == recomputed
        2. Check event.prev_hash == previous event's event_hash
           (first event: prev_hash should be "")

        Collect tampered_ids and broken_chain_ids.
        """
        events = log.list_events(limit=100_000)
        tampered: list[str] = []
        broken_chain: list[str] = []
        prev_hash = ""

        for event in events:
            if not event.verify():
                tampered.append(event.event_id)
            if event.prev_hash != prev_hash:
                broken_chain.append(event.event_id)
            prev_hash = event.event_hash

        valid_count = len(events) - len(set(tampered) | set(broken_chain))

        return VerificationReport(
            total_events=len(events),
            valid_count=max(0, valid_count),
            tampered_ids=tampered,
            broken_chain_ids=broken_chain,
        )
