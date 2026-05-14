"""Privacy-preserving search module for docs-toolkit (E38).

Provides PII anonymization, k-anonymity query generalization, and a
BM25-based private searcher that applies these techniques transparently.

Quick start::

    from docstoolkit.private_search import (
        QueryAnonymizer,
        AnonymizationRule,
        QueryGeneralizer,
        KAnonymizer,
        KAnonymityConfig,
        PrivateSearcher,
        PrivateSearchConfig,
        PrivateSearchResult,
    )

    searcher = PrivateSearcher(
        config=PrivateSearchConfig(anonymize_queries=True),
        documents={"doc1": "Machine learning basics", "doc2": "Deep learning"},
    )
    result = searcher.search("how to contact user@example.com about learning?")
    print(result.anonymized_query)   # "how to contact [EMAIL] about learning?"
    print(result.results)            # ["doc1", "doc2"]
"""

from docstoolkit.private_search.anonymizer import (
    AnonymizationRule,
    QueryAnonymizer,
)
from docstoolkit.private_search.k_anonymity import (
    KAnonymityConfig,
    KAnonymizer,
    QueryGeneralizer,
)
from docstoolkit.private_search.searcher import (
    PrivateSearchConfig,
    PrivateSearchResult,
    PrivateSearcher,
)

__all__ = [
    "AnonymizationRule",
    "QueryAnonymizer",
    "KAnonymityConfig",
    "KAnonymizer",
    "QueryGeneralizer",
    "PrivateSearchConfig",
    "PrivateSearchResult",
    "PrivateSearcher",
]
