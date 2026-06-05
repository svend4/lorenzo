"""Document HMAC-based signing/verification (E165).

Public API:
    SignatureAlgo, Signature, SignedDocument, VerifyResult,
    DocSigner, MultiKeyDocSigner
"""
from docstoolkit.doc_signature.signer import (
    DocSigner,
    MultiKeyDocSigner,
    Signature,
    SignatureAlgo,
    SignedDocument,
    VerifyResult,
)

__all__ = [
    "DocSigner",
    "MultiKeyDocSigner",
    "Signature",
    "SignatureAlgo",
    "SignedDocument",
    "VerifyResult",
]
