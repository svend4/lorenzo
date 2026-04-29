"""A/B testing framework для retrievers / answerers / RAG configs.

Использование:
    from docstoolkit.experiments import Experiment, run_experiment

    exp = Experiment(
        name="hybrid-vs-keyword",
        variants=[
            {"name": "control", "method": "keyword"},
            {"name": "treatment", "method": "hybrid"},
        ],
        questions=["вопрос 1", "вопрос 2", ...],
    )
    result = run_experiment(exp)
    print(result.compare())  # → markdown отчёт
"""
from docstoolkit.experiments.types import Experiment, ExperimentResult, VariantResult
from docstoolkit.experiments.runner import run_experiment, run_variant

__all__ = [
    "Experiment", "ExperimentResult", "VariantResult",
    "run_experiment", "run_variant",
]
