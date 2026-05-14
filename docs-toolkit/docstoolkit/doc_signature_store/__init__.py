"""E330 DocSignatureStore — digital signature tracking for documents.

Public API
----------
:class:`Signature`         — a single signature on a document
:class:`SignatureStats`    — aggregate statistics
:class:`DocSignatureStore` — main interface for signature management
"""

from .store import Signature, SignatureStats, DocSignatureStore

__all__ = ["Signature", "SignatureStats", "DocSignatureStore"]
