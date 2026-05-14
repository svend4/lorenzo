from dataclasses import dataclass, field
from docstoolkit.snapshot.capture import CapturedState


@dataclass
class SnapshotDiff:
    """Diff between two corpus snapshots."""
    snapshot_id_before: str
    snapshot_id_after: str
    added_docs: list = field(default_factory=list)     # list[str] doc_ids added
    removed_docs: list = field(default_factory=list)   # list[str] doc_ids removed
    modified_docs: list = field(default_factory=list)  # list[str] doc_ids changed
    unchanged_docs: list = field(default_factory=list) # list[str] unchanged

    def total_changes(self) -> int:
        return len(self.added_docs) + len(self.removed_docs) + len(self.modified_docs)

    def change_rate(self) -> float:
        """Fraction of docs that changed vs total docs in 'after' snapshot.
        Returns 0.0 if no docs.
        """
        total = (len(self.added_docs) + len(self.removed_docs)
                 + len(self.modified_docs) + len(self.unchanged_docs))
        if total == 0:
            return 0.0
        return (len(self.added_docs) + len(self.removed_docs) + len(self.modified_docs)) / total

    def summary(self) -> str:
        return (f"+{len(self.added_docs)} -{len(self.removed_docs)} "
                f"~{len(self.modified_docs)} ={len(self.unchanged_docs)}")


def diff_snapshots(before: CapturedState, after: CapturedState) -> SnapshotDiff:
    """Compute diff between two snapshots.

    Algorithm:
    - added: doc_ids in after.doc_hashes but not in before.doc_hashes
    - removed: doc_ids in before.doc_hashes but not in after.doc_hashes
    - modified: doc_ids in both but with different hash values
    - unchanged: doc_ids in both with same hash
    """
    before_ids = set(before.doc_hashes)
    after_ids = set(after.doc_hashes)

    added = sorted(after_ids - before_ids)
    removed = sorted(before_ids - after_ids)
    shared = before_ids & after_ids
    modified = sorted(
        doc_id for doc_id in shared
        if before.doc_hashes[doc_id] != after.doc_hashes[doc_id]
    )
    unchanged = sorted(
        doc_id for doc_id in shared
        if before.doc_hashes[doc_id] == after.doc_hashes[doc_id]
    )

    return SnapshotDiff(
        snapshot_id_before=before.snapshot_id,
        snapshot_id_after=after.snapshot_id,
        added_docs=added,
        removed_docs=removed,
        modified_docs=modified,
        unchanged_docs=unchanged,
    )
