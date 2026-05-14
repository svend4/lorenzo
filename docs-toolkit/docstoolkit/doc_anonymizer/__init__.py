"""E203 Document Anonymizer module for docs-toolkit.

Pattern-based PII detection and masking for unstructured document text.

Unlike :mod:`docstoolkit.data_masking` (E105) which operates on structured
dicts via field-name rules, ``doc_anonymizer`` scans free text for emails,
phone numbers, SSNs, IPs, credit cards, URLs and custom regex patterns.

Usage::

    from docstoolkit.doc_anonymizer import (
        DocAnonymizer, AnonymizerConfig, MaskingMode, PiiType,
    )

    cfg = AnonymizerConfig(
        enabled_types={PiiType.EMAIL, PiiType.PHONE},
        mode=MaskingMode.PARTIAL,
        partial_keep=4,
    )
    anon = DocAnonymizer(cfg)
    result = anon.anonymize("Reach me at alice@example.com")
    print(result.anonymized)
"""
from docstoolkit.doc_anonymizer.anonymizer import (
    AnonymizeResult,
    AnonymizerConfig,
    DocAnonymizer,
    MaskingMode,
    PiiMatch,
    PiiType,
)

__all__ = [
    "AnonymizeResult",
    "AnonymizerConfig",
    "DocAnonymizer",
    "MaskingMode",
    "PiiMatch",
    "PiiType",
]
