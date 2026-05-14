"""E153 Document transformer — applies named transformations pipeline-style.

Public API
----------
:class:`TransformOp`       — enum of transform operations
:class:`Transform`         — single transform spec (op + params + optional condition)
:class:`TransformResult`   — result of a pipeline application
:class:`DocTransformer`    — main transform engine
"""
from .transformer import (
    DocTransformer,
    Transform,
    TransformOp,
    TransformResult,
)

__all__ = [
    "DocTransformer",
    "Transform",
    "TransformOp",
    "TransformResult",
]
