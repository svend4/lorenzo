"""Taxonomy drift detection between two snapshots."""
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone

from docstoolkit.taxonomy.node import TaxonomyTree


@dataclass
class TaxonomySnapshot:
    """Serializable taxonomy state for drift comparison."""
    timestamp: str
    cluster_labels: list[str]        # node labels at this point
    doc_assignments: dict[str, str]  # {doc_id: node_label}

    def to_json(self) -> str:
        return json.dumps({
            "timestamp": self.timestamp,
            "cluster_labels": self.cluster_labels,
            "doc_assignments": self.doc_assignments,
        }, ensure_ascii=False)

    @classmethod
    def from_json(cls, data: str) -> "TaxonomySnapshot":
        obj = json.loads(data)
        return cls(
            timestamp=obj["timestamp"],
            cluster_labels=obj["cluster_labels"],
            doc_assignments=obj["doc_assignments"],
        )

    @classmethod
    def from_tree(cls, tree: TaxonomyTree, timestamp: str = "") -> "TaxonomySnapshot":
        if not timestamp:
            timestamp = datetime.now(timezone.utc).isoformat()
        cluster_labels: list[str] = [n.label for n in tree.all_nodes()]
        doc_assignments: dict[str, str] = {}
        for node in tree.all_nodes():
            for doc_id in node.doc_ids:
                doc_assignments[doc_id] = node.label
        return cls(
            timestamp=timestamp,
            cluster_labels=cluster_labels,
            doc_assignments=doc_assignments,
        )


@dataclass
class DriftReport:
    new_clusters: list[str]          # labels in current but not previous
    removed_clusters: list[str]      # labels in previous but not current
    moved_docs: list[str]            # doc_ids that changed cluster
    stability_score: float           # 0-1: fraction of docs that stayed in same cluster
    summary: str


def detect_drift(
    previous: TaxonomySnapshot,
    current: TaxonomySnapshot,
) -> DriftReport:
    """Compare two snapshots.

    new_clusters     = labels in current not in previous
    removed_clusters = labels in previous not in current
    moved_docs       = doc_ids where assignment changed
    stability_score  = (common docs - moved) / common docs,
                       or 1.0 if no common docs
    summary          = human-readable description
    """
    prev_labels = set(previous.cluster_labels)
    curr_labels = set(current.cluster_labels)

    new_clusters = sorted(curr_labels - prev_labels)
    removed_clusters = sorted(prev_labels - curr_labels)

    common_docs = set(previous.doc_assignments) & set(current.doc_assignments)
    moved_docs = [
        doc_id for doc_id in sorted(common_docs)
        if previous.doc_assignments[doc_id] != current.doc_assignments[doc_id]
    ]

    if common_docs:
        stability_score = (len(common_docs) - len(moved_docs)) / len(common_docs)
    else:
        stability_score = 1.0

    parts: list[str] = []
    if new_clusters:
        parts.append(f"{len(new_clusters)} new cluster(s): {', '.join(new_clusters)}")
    if removed_clusters:
        parts.append(f"{len(removed_clusters)} removed cluster(s): {', '.join(removed_clusters)}")
    if moved_docs:
        parts.append(f"{len(moved_docs)} doc(s) moved to different clusters")
    parts.append(f"stability={stability_score:.2f}")
    summary = "; ".join(parts) if parts else "No changes detected."

    return DriftReport(
        new_clusters=new_clusters,
        removed_clusters=removed_clusters,
        moved_docs=moved_docs,
        stability_score=stability_score,
        summary=summary,
    )
