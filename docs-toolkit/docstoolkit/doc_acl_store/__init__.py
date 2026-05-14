"""E356 DocAclStore — access control list (ACL) store for documents.

Public API
----------
:class:`AclEntry`     — a single ACL entry
:class:`AclStats`     — aggregate statistics
:class:`DocAclStore`  — main interface for ACL management
"""

from .store import AclEntry, AclStats, DocAclStore

__all__ = ["AclEntry", "AclStats", "DocAclStore"]
