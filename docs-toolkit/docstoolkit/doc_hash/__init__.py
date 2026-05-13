"""Document hashing utilities (E149).

Public API:
    HashAlgo, HashResult, SimHashResult, DocHash
"""
from docstoolkit.doc_hash.hasher import (
    DocHash,
    HashAlgo,
    HashResult,
    SimHashResult,
)

__all__ = [
    "DocHash",
    "HashAlgo",
    "HashResult",
    "SimHashResult",
]
