"""Intent-based pipeline router."""
import json
from dataclasses import dataclass, field
from pathlib import Path

from docstoolkit.intent.classifier import (
    Intent, IntentClassifier,
    FACTOID, EXPLANATION, COMPARISON, SYNTHESIS, OPINION, INSTRUCTION, UNKNOWN,
)


@dataclass
class PipelineConfig:
    """Configuration for a RAG pipeline, chosen based on query intent."""
    retriever: str = "hybrid"
    top_k: int = 5
    prompt_id: str = ""
    post_processor: str = ""
    use_mapreduce: bool = False
    use_hierarchical: bool = False


# Default config per intent label
_DEFAULTS: dict[str, PipelineConfig] = {
    FACTOID:     PipelineConfig(retriever="keyword", top_k=3),
    EXPLANATION: PipelineConfig(retriever="hybrid", top_k=5),
    COMPARISON:  PipelineConfig(retriever="hybrid", top_k=10, post_processor="compare"),
    SYNTHESIS:   PipelineConfig(retriever="hybrid", top_k=20, use_mapreduce=True),
    INSTRUCTION: PipelineConfig(retriever="hybrid", top_k=5, post_processor="steps"),
    OPINION:     PipelineConfig(retriever="semantic", top_k=7),
    UNKNOWN:     PipelineConfig(),
}


class IntentRouter:
    """Route queries to PipelineConfig based on classified intent."""

    def __init__(self, classifier: IntentClassifier | None = None) -> None:
        self._classifier = classifier or IntentClassifier()
        self._configs: dict[str, PipelineConfig] = dict(_DEFAULTS)

    def configure(self, label: str, config: PipelineConfig) -> None:
        """Override default PipelineConfig for a given intent label."""
        self._configs[label] = config

    def route(self, query: str) -> tuple[Intent, PipelineConfig]:
        """Classify query and return (Intent, PipelineConfig)."""
        intent = self._classifier.classify(query)
        cfg = self._configs.get(intent.label, self._configs[UNKNOWN])
        return intent, cfg

    def route_and_log(
        self,
        query: str,
        log_path: Path | None = None,
    ) -> tuple[Intent, PipelineConfig]:
        """Classify query, return (Intent, PipelineConfig), and append JSON log line."""
        intent, cfg = self.route(query)
        if log_path is not None:
            entry = {
                "query": query,
                "intent": intent.label,
                "confidence": intent.confidence,
                "extracted": intent.extracted,
                "pipeline": {
                    "retriever": cfg.retriever,
                    "top_k": cfg.top_k,
                    "prompt_id": cfg.prompt_id,
                    "post_processor": cfg.post_processor,
                    "use_mapreduce": cfg.use_mapreduce,
                    "use_hierarchical": cfg.use_hierarchical,
                },
            }
            log_path.parent.mkdir(parents=True, exist_ok=True)
            with log_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        return intent, cfg
