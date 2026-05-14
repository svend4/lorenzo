"""text_normalizer — pure-stdlib text normalization for docs-toolkit."""
from docstoolkit.text_normalizer.rules import (
    NormRule,
    case_rules,
    number_rules,
    punctuation_rules,
    whitespace_rules,
)
from docstoolkit.text_normalizer.normalizer import NormalizerConfig, TextNormalizer
from docstoolkit.text_normalizer.pipeline import NormPipeline, NormStep

__all__ = [
    # rules
    "NormRule",
    "whitespace_rules",
    "punctuation_rules",
    "case_rules",
    "number_rules",
    # normalizer
    "NormalizerConfig",
    "TextNormalizer",
    # pipeline
    "NormPipeline",
    "NormStep",
]
