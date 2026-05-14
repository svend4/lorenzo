"""Document access matrix module (E284) — role-based permission matrix.

Public API
----------
- ``Permission``      — single action + allowed flag
- ``RolePolicy``      — named role with its action→bool permission map
- ``AccessDecision``  — result of a ``DocAccessMatrix.check`` call
- ``MatrixStats``     — aggregate counts for the current matrix state
- ``DocAccessMatrix`` — thread-safe RBAC matrix with explicit doc-level overrides
"""

from docstoolkit.doc_access_matrix.matrix import (
    AccessDecision,
    DocAccessMatrix,
    MatrixStats,
    Permission,
    RolePolicy,
)

__all__ = [
    "Permission",
    "RolePolicy",
    "AccessDecision",
    "MatrixStats",
    "DocAccessMatrix",
]
