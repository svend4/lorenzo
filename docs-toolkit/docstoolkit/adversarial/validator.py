"""Difficulty validation: test generated questions against a retriever."""
import re
from dataclasses import dataclass, field
from docstoolkit.adversarial.generator import HardQuestion


@dataclass
class DifficultyScore:
    """Validated difficulty of a question against actual system performance."""
    question: str
    predicted: float      # from generator
    actual: float         # measured by testing system
    confirmed_hard: bool  # actual >= threshold

    def calibration_error(self) -> float:
        """abs(predicted - actual)"""
        return abs(self.predicted - self.actual)


@dataclass
class DifficultyReport:
    """Batch difficulty validation report."""
    scores: list = field(default_factory=list)   # list[DifficultyScore]
    confirmed_hard_count: int = 0
    avg_calibration_error: float = 0.0

    def hard_questions(self) -> list:
        """Return DifficultyScore entries where confirmed_hard=True."""
        return [s for s in self.scores if s.confirmed_hard]

    def precision(self) -> float:
        """Fraction of predicted-hard that are actually hard."""
        predicted_hard = [s for s in self.scores if s.predicted >= 0.6]
        if not predicted_hard:
            return 0.0
        confirmed = sum(1 for s in predicted_hard if s.confirmed_hard)
        return confirmed / len(predicted_hard)


def validate_difficulty(
    questions: list,           # list[HardQuestion]
    retriever_fn,              # callable(question: str) -> float (0-1 score, lower = harder)
    threshold: float = 0.6,
) -> DifficultyReport:
    """Validate question difficulty by testing against retriever.

    For each question:
    1. Call retriever_fn(question.question) to get retrieval score
    2. actual_difficulty = 1.0 - retrieval_score  (high retrieval = easy question)
    3. confirmed_hard = actual_difficulty >= threshold
    4. Create DifficultyScore

    Compute avg_calibration_error = mean of all calibration errors.
    Return DifficultyReport.
    """
    if not questions:
        return DifficultyReport(scores=[], confirmed_hard_count=0, avg_calibration_error=0.0)

    scores = []
    for hq in questions:
        retrieval_score = retriever_fn(hq.question)
        actual = 1.0 - retrieval_score
        confirmed = actual >= threshold
        ds = DifficultyScore(
            question=hq.question,
            predicted=hq.predicted_difficulty,
            actual=actual,
            confirmed_hard=confirmed,
        )
        scores.append(ds)

    confirmed_hard_count = sum(1 for s in scores if s.confirmed_hard)
    avg_cal_error = sum(s.calibration_error() for s in scores) / len(scores)

    return DifficultyReport(
        scores=scores,
        confirmed_hard_count=confirmed_hard_count,
        avg_calibration_error=avg_cal_error,
    )
