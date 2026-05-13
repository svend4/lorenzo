"""BanditExperiment — high-level A/B testing harness for RAG configurations."""
from dataclasses import dataclass, field

from docstoolkit.bandit.bandit import ThompsonBandit, BanditState


@dataclass
class BanditResult:
    """Snapshot of a bandit experiment's outcome."""

    experiment_name: str
    total_pulls: int
    arm_states: list[BanditState]
    winner: str | None
    winner_confidence: float = 0.95

    def summary(self) -> str:
        """Return a Markdown summary of the experiment."""
        lines = [
            f"# Bandit Experiment: {self.experiment_name}",
            "",
            f"**Total pulls:** {self.total_pulls}",
            f"**Winner:** {self.winner or 'undecided'} "
            f"(confidence={self.winner_confidence:.0%})",
            "",
            "## Arm Statistics",
            "",
            "| Arm | Mean | CI Low | CI High | Pulls |",
            "|-----|------|--------|---------|-------|",
        ]
        for s in self.arm_states:
            lines.append(
                f"| {s.arm_name} | {s.mean:.4f} | {s.ci_low:.4f} | "
                f"{s.ci_high:.4f} | {s.total_pulls} |"
            )
        return "\n".join(lines)


class BanditExperiment:
    """High-level bandit experiment for comparing RAG variants.

    Usage
    -----
    >>> exp = BanditExperiment("rag-config-test", ["bm25", "hybrid", "semantic"])
    >>> variant = exp.choose()
    >>> # … run retrieval with `variant` …
    >>> exp.record(variant, success=True)
    >>> print(exp.auto_promote_winner())
    """

    def __init__(
        self,
        name: str,
        variants: list[str],
        db_path: str = ":memory:",
        exploration_floor: float = 0.05,
    ):
        self._name = name
        self._bandit = ThompsonBandit(
            arms=variants,
            db_path=db_path,
            exploration_floor=exploration_floor,
        )

    def choose(self) -> str:
        """Select which variant to use for the next query."""
        return self._bandit.select()

    def record(self, variant: str, success: bool) -> None:
        """Record feedback for a variant (True = success, False = failure)."""
        self._bandit.update(arm=variant, reward=1.0 if success else 0.0)

    def result(self) -> BanditResult:
        """Return the current state of the experiment."""
        states = self._bandit.state()
        total_pulls = sum(s.total_pulls for s in states)
        winner = self._bandit.winner()
        return BanditResult(
            experiment_name=self._name,
            total_pulls=total_pulls,
            arm_states=states,
            winner=winner,
        )

    def auto_promote_winner(self, confidence: float = 0.95) -> str | None:
        """Return winning variant name if a clear winner exists, else None."""
        return self._bandit.winner(confidence=confidence)
