"""Deduplication key computation: strategies and hashing."""
import hashlib
import uuid
from dataclasses import dataclass, field
from enum import Enum
import time


class DeduplicationStrategy(Enum):
    """Strategy used to compute a deduplication key from a payload."""
    EXACT = "exact"           # hash the full payload as-is
    NORMALIZED = "normalized" # strip whitespace and lowercase, then hash
    SEMANTIC = "semantic"     # first 100 chars of normalized payload, then hash


@dataclass
class DeduplicationKey:
    """Immutable deduplication key for a single request."""
    request_id: str
    key_hash: str                   # SHA-256[:16] hex of transformed payload
    strategy: DeduplicationStrategy
    created_ts: float               # time.time() at creation


def _transform(payload: str, strategy: DeduplicationStrategy) -> str:
    """Apply strategy-specific transformation to payload before hashing."""
    if strategy == DeduplicationStrategy.EXACT:
        return payload
    normalized = " ".join(payload.split()).lower()
    if strategy == DeduplicationStrategy.NORMALIZED:
        return normalized
    # SEMANTIC: first 100 chars of normalized text
    return normalized[:100]


def compute_key(
    payload: str,
    strategy: DeduplicationStrategy,
    request_id: str = None,
) -> DeduplicationKey:
    """Compute a DeduplicationKey for *payload* using *strategy*.

    Parameters
    ----------
    payload:    Raw request payload string.
    strategy:   Which transformation to apply before hashing.
    request_id: Optional caller-supplied ID; defaults to a new UUID4 string.

    Returns
    -------
    DeduplicationKey with SHA-256[:16] hex digest of the transformed payload.
    """
    if request_id is None:
        request_id = str(uuid.uuid4())
    transformed = _transform(payload, strategy)
    digest = hashlib.sha256(transformed.encode("utf-8")).hexdigest()[:16]
    return DeduplicationKey(
        request_id=request_id,
        key_hash=digest,
        strategy=strategy,
        created_ts=time.time(),
    )
