import json
from dataclasses import dataclass, field
from datetime import datetime
from docstoolkit.federated_eval.privacy import PrivacyBudget, privatize_metrics

@dataclass
class NodeMetrics:
    """Metrics from one federated node."""
    node_id: str
    query_count: int
    precision_at_5: float      # 0-1
    recall_at_5: float         # 0-1
    mrr: float                 # mean reciprocal rank, 0-1
    avg_latency_ms: float
    golden_queries: int        # number of golden dataset entries
    ts: str = ""

    def __post_init__(self):
        if not self.ts:
            self.ts = datetime.now().isoformat(timespec='seconds')

    def to_dict(self) -> dict:
        return {
            "node_id": self.node_id,
            "query_count": self.query_count,
            "precision_at_5": self.precision_at_5,
            "recall_at_5": self.recall_at_5,
            "mrr": self.mrr,
            "avg_latency_ms": self.avg_latency_ms,
            "golden_queries": self.golden_queries,
            "ts": self.ts,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "NodeMetrics":
        return cls(
            node_id=d["node_id"],
            query_count=int(d.get("query_count", 0)),
            precision_at_5=float(d.get("precision_at_5", 0.0)),
            recall_at_5=float(d.get("recall_at_5", 0.0)),
            mrr=float(d.get("mrr", 0.0)),
            avg_latency_ms=float(d.get("avg_latency_ms", 0.0)),
            golden_queries=int(d.get("golden_queries", 0)),
            ts=d.get("ts", ""),
        )


@dataclass
class FederatedNode:
    """A node that contributes to federated evaluation."""
    node_id: str
    privacy_budget: PrivacyBudget = None
    _metrics_history: list = field(default_factory=list, repr=False)  # list[NodeMetrics]

    def __post_init__(self):
        if self.privacy_budget is None:
            self.privacy_budget = PrivacyBudget()

    def submit_metrics(self, metrics: NodeMetrics, seed: int | None = None) -> dict:
        """Privatize metrics and return as dict ready to share.

        1. Convert metrics to dict
        2. Apply privatize_metrics with node's privacy_budget
        3. Append original to _metrics_history
        4. Return privatized dict
        """
        self._metrics_history.append(metrics)
        raw = metrics.to_dict()
        return privatize_metrics(raw, self.privacy_budget, seed=seed)

    def history(self) -> list:
        return list(self._metrics_history)
