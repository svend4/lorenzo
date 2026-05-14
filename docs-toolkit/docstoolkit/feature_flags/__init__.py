"""Feature flags: runtime toggles with rollout control."""
from docstoolkit.feature_flags.flag import FeatureFlag, FlagStatus, RolloutStrategy
from docstoolkit.feature_flags.evaluator import FlagEvaluator, EvaluationContext, EvalResult
from docstoolkit.feature_flags.store import FlagStore

__all__ = [
    "FeatureFlag", "FlagStatus", "RolloutStrategy",
    "FlagEvaluator", "EvaluationContext", "EvalResult",
    "FlagStore",
]
