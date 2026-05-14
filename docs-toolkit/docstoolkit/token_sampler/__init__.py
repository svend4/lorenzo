"""E93 — Token-bucket sampler.

Public API:
    * :class:`TokenBucket`            — thread-safe token bucket primitive
    * :class:`SamplingDecision`       — KEEP / DROP enum
    * :class:`TokenBucketSampler`     — keep / drop decisions at a fixed rate
    * :class:`AdaptiveSampler`        — sampler that reacts to load feedback
"""
from docstoolkit.token_sampler.bucket import TokenBucket
from docstoolkit.token_sampler.sampler import SamplingDecision, TokenBucketSampler
from docstoolkit.token_sampler.adaptive import AdaptiveSampler

__all__ = [
    "TokenBucket",
    "SamplingDecision",
    "TokenBucketSampler",
    "AdaptiveSampler",
]
