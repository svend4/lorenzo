"""Opaque access token issuance and validation.

Public API
----------
- ``TokenStatus``      — enum of validation outcomes (VALID, EXPIRED, REVOKED, INVALID)
- ``Token``            — server-side record of an issued token
- ``ValidationResult`` — outcome of validating a token string
- ``TokenManager``     — issuance, validation, revocation, cleanup

The wire format is a base64url-encoded ``token_id.signature`` pair where
``signature = hmac_sha256(secret, token_id)``. No JWT, no third-party
crypto libraries — only stdlib.
"""

from docstoolkit.access_token.manager import (
    TokenStatus,
    Token,
    ValidationResult,
    TokenManager,
)

__all__ = [
    "TokenStatus",
    "Token",
    "ValidationResult",
    "TokenManager",
]
