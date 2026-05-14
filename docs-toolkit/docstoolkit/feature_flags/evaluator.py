import hashlib
from dataclasses import dataclass
from docstoolkit.feature_flags.flag import FeatureFlag, FlagStatus, RolloutStrategy

@dataclass
class EvaluationContext:
    user_id: str = ""
    attributes: dict = None

    def __post_init__(self):
        if self.attributes is None:
            self.attributes = {}

@dataclass
class EvalResult:
    flag_name: str
    enabled: bool
    reason: str      # "globally_enabled", "disabled", "allowlist", "rollout_pct", "no_flag"

    def __bool__(self) -> bool:
        return self.enabled


class FlagEvaluator:
    """Evaluates feature flags for a given context."""

    def evaluate(self, flag: FeatureFlag, ctx: EvaluationContext) -> EvalResult:
        """Evaluate whether flag is enabled for this context.

        Rules (in order):
        1. status=DISABLED -> disabled, reason="disabled"
        2. status=ENABLED -> enabled, reason="globally_enabled"
        3. status=ROLLOUT:
           a. strategy=ALL -> enabled, reason="rollout_all"
           b. strategy=NONE -> disabled, reason="rollout_none"
           c. strategy=ALLOWLIST:
              - if ctx.user_id in flag.allowlist -> enabled, reason="allowlist"
              - else -> disabled, reason="not_in_allowlist"
           d. strategy=PERCENTAGE:
              - hash(flag.name + ":" + ctx.user_id) mod 100 < rollout_pct -> enabled
              - reason="rollout_pct" or "rollout_excluded"
        """
        if flag.status == FlagStatus.DISABLED:
            return EvalResult(flag.name, False, "disabled")
        if flag.status == FlagStatus.ENABLED:
            return EvalResult(flag.name, True, "globally_enabled")
        # ROLLOUT
        strategy = flag.strategy
        if strategy == RolloutStrategy.ALL:
            return EvalResult(flag.name, True, "rollout_all")
        if strategy == RolloutStrategy.NONE:
            return EvalResult(flag.name, False, "rollout_none")
        if strategy == RolloutStrategy.ALLOWLIST:
            if ctx.user_id in flag.allowlist:
                return EvalResult(flag.name, True, "allowlist")
            return EvalResult(flag.name, False, "not_in_allowlist")
        if strategy == RolloutStrategy.PERCENTAGE:
            key = f"{flag.name}:{ctx.user_id}"
            bucket = int(hashlib.md5(key.encode()).hexdigest(), 16) % 100
            if bucket < flag.rollout_pct:
                return EvalResult(flag.name, True, "rollout_pct")
            return EvalResult(flag.name, False, "rollout_excluded")
        return EvalResult(flag.name, False, "disabled")

    def evaluate_all(self, flags: list, ctx: EvaluationContext) -> dict:
        """Evaluate all flags, return {flag_name: EvalResult}."""
        return {f.name: self.evaluate(f, ctx) for f in flags}
