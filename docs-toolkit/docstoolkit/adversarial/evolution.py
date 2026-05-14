"""Co-evolution loop: adversarial generation + validation across rounds."""
from dataclasses import dataclass, field
from docstoolkit.adversarial.generator import AdversarialGenerator, HardQuestion
from docstoolkit.adversarial.validator import validate_difficulty, DifficultyReport


@dataclass
class CoEvolutionConfig:
    questions_per_round: int = 5
    hard_threshold: float = 0.6
    max_rounds: int = 3
    seed: int | None = None


@dataclass
class EvolutionRound:
    """One round of adversarial co-evolution."""
    round_num: int
    generated: list = field(default_factory=list)    # list[HardQuestion]
    report: DifficultyReport = None
    confirmed_hard: int = 0

    def improvement_potential(self) -> float:
        """Fraction of confirmed hard questions in this round."""
        if not self.generated:
            return 0.0
        return self.confirmed_hard / len(self.generated)


class CoEvolutionLoop:
    """Runs multiple rounds of adversarial generation + validation."""

    def __init__(self, config: CoEvolutionConfig | None = None):
        self._config = config or CoEvolutionConfig()

    def run(
        self,
        passages: list,          # corpus passages
        retriever_fn,            # callable(question: str) -> float
        golden_queue: list | None = None,  # append confirmed-hard questions here
    ) -> list:
        """Run max_rounds of co-evolution.

        Each round:
        1. Generate questions_per_round questions
        2. Validate with retriever_fn
        3. Add confirmed-hard to golden_queue (if provided)
        4. Create EvolutionRound

        Return list[EvolutionRound].
        """
        cfg = self._config
        # Use a different seed per round so rounds aren't identical,
        # but keep overall determinism if seed is set.
        rounds = []

        for round_num in range(cfg.max_rounds):
            # Derive per-round seed
            if cfg.seed is not None:
                round_seed = cfg.seed + round_num
            else:
                round_seed = None

            generator = AdversarialGenerator(seed=round_seed)
            generated = generator.generate(passages, n=cfg.questions_per_round)

            report = validate_difficulty(
                generated, retriever_fn, threshold=cfg.hard_threshold
            )

            # Collect confirmed-hard HardQuestion objects
            confirmed_hard_qs = [
                hq for hq, ds in zip(generated, report.scores)
                if ds.confirmed_hard
            ]

            if golden_queue is not None:
                golden_queue.extend(confirmed_hard_qs)

            ev_round = EvolutionRound(
                round_num=round_num,
                generated=generated,
                report=report,
                confirmed_hard=len(confirmed_hard_qs),
            )
            rounds.append(ev_round)

        return rounds
