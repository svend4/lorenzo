"""Federated golden datasets with differential privacy."""
from docstoolkit.federated_eval.privacy import (
    add_laplace_noise, add_gaussian_noise, privatize_metrics,
    PrivacyBudget, PrivacyAccountant,
)
from docstoolkit.federated_eval.node import FederatedNode, NodeMetrics
from docstoolkit.federated_eval.aggregator import SecureAggregator, AggregatedReport
from docstoolkit.federated_eval.secure_aggregation import (
    MaskedShare, mask_share, aggregate_shares, secure_average,
)

__all__ = [
    "add_laplace_noise", "add_gaussian_noise", "privatize_metrics",
    "PrivacyBudget", "PrivacyAccountant",
    "FederatedNode", "NodeMetrics",
    "SecureAggregator", "AggregatedReport",
    "MaskedShare", "mask_share", "aggregate_shares", "secure_average",
]
