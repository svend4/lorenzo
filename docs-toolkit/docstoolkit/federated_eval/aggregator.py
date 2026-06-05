from dataclasses import dataclass, field
from docstoolkit.federated_eval.node import NodeMetrics

@dataclass
class AggregatedReport:
    """Aggregated metrics across all federated nodes."""
    node_count: int
    total_queries: int
    avg_precision_at_5: float
    avg_recall_at_5: float
    avg_mrr: float
    avg_latency_ms: float
    total_golden_queries: int
    node_ids: list = field(default_factory=list)

    def f1(self) -> float:
        """Harmonic mean of precision and recall."""
        p = self.avg_precision_at_5
        r = self.avg_recall_at_5
        if p + r == 0:
            return 0.0
        return 2 * p * r / (p + r)

    def summary(self) -> str:
        return (
            f"nodes={self.node_count} queries={self.total_queries} "
            f"P@5={self.avg_precision_at_5:.3f} R@5={self.avg_recall_at_5:.3f} "
            f"MRR={self.avg_mrr:.3f} F1={self.f1():.3f}"
        )


class SecureAggregator:
    """Aggregates privatized metrics from multiple nodes."""

    def aggregate(self, privatized_reports: list) -> AggregatedReport:
        """Aggregate list of privatized metric dicts (from FederatedNode.submit_metrics).

        Computes weighted averages for float metrics (weighted by query_count).
        Sums integer metrics.
        Returns AggregatedReport.

        If empty list: return AggregatedReport with all zeros.
        """
        if not privatized_reports:
            return AggregatedReport(
                node_count=0, total_queries=0,
                avg_precision_at_5=0.0, avg_recall_at_5=0.0,
                avg_mrr=0.0, avg_latency_ms=0.0,
                total_golden_queries=0,
            )

        node_ids = [r.get("node_id", "") for r in privatized_reports]
        total_queries = sum(r.get("query_count", 0) for r in privatized_reports)
        total_golden = sum(r.get("golden_queries", 0) for r in privatized_reports)

        # Weighted averages by query_count
        def wavg(field: str) -> float:
            if total_queries == 0:
                vals = [r.get(field, 0.0) for r in privatized_reports]
                return sum(vals) / len(vals) if vals else 0.0
            total = sum(r.get(field, 0.0) * r.get("query_count", 0)
                       for r in privatized_reports)
            return total / total_queries

        return AggregatedReport(
            node_count=len(privatized_reports),
            total_queries=total_queries,
            avg_precision_at_5=wavg("precision_at_5"),
            avg_recall_at_5=wavg("recall_at_5"),
            avg_mrr=wavg("mrr"),
            avg_latency_ms=wavg("avg_latency_ms"),
            total_golden_queries=total_golden,
            node_ids=node_ids,
        )
