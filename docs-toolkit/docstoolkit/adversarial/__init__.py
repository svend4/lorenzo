"""Adversarial co-evolution: system generates hard questions against itself."""
from docstoolkit.adversarial.generator import (
    QuestionPattern, HardQuestion, AdversarialGenerator,
)
from docstoolkit.adversarial.validator import (
    DifficultyScore, validate_difficulty, DifficultyReport,
)
from docstoolkit.adversarial.evolution import (
    CoEvolutionConfig, EvolutionRound, CoEvolutionLoop,
)

__all__ = [
    "QuestionPattern", "HardQuestion", "AdversarialGenerator",
    "DifficultyScore", "validate_difficulty", "DifficultyReport",
    "CoEvolutionConfig", "EvolutionRound", "CoEvolutionLoop",
]
