"""Experiment runner."""
import time
from datetime import datetime

from docstoolkit.experiments.types import (
    Experiment, ExperimentResult, VariantResult, QueryRun,
)


def run_variant(variant_config: dict, questions: list[str]) -> VariantResult:
    """Прогон одного variant'а на всех questions."""
    from docstoolkit.rag import ask

    name = variant_config.get("name", "unknown")
    runs = []
    for q in questions:
        try:
            result = ask(
                q,
                top_k=variant_config.get("top_k", 5),
                method=variant_config.get("method", "hybrid"),
                answerer=variant_config.get("answerer", "echo"),
                model=variant_config.get("model", "claude-haiku-4-5-20251001"),
            )
            runs.append(QueryRun(
                question=q,
                answer=result.answer,
                citations=result.citations,
                duration_ms=result.duration_ms,
                tokens=result.tokens_used,
                cost=result.cost_estimate,
                error=result.error,
            ))
        except Exception as e:
            runs.append(QueryRun(question=q, answer="", error=str(e)[:200]))

    return VariantResult(name=name, config=variant_config, runs=runs)


def run_experiment(exp: Experiment) -> ExperimentResult:
    """Прогон всех variant'ов на всех questions."""
    t0 = time.time()
    variant_results = [
        run_variant(v, exp.questions)
        for v in exp.variants
    ]
    return ExperimentResult(
        experiment=exp,
        variant_results=variant_results,
        duration_ms=int((time.time() - t0) * 1000),
    )


def load_experiment_from_yaml(path: str) -> Experiment:
    """Загружает эксперимент из YAML файла.

    Формат:
        name: my-test
        description: ...
        variants:
          - name: control
            method: keyword
          - name: treatment
            method: hybrid
        questions:
          - "вопрос 1"
          - "вопрос 2"
    """
    from docstoolkit.frontmatter import parse_yaml
    from pathlib import Path
    text = Path(path).read_text(encoding="utf-8")
    data = parse_yaml(text)

    return Experiment(
        name=data.get("name", "unnamed"),
        description=data.get("description", ""),
        variants=data.get("variants", []),
        questions=data.get("questions", []),
        metric=data.get("metric", "duration_ms"),
    )
