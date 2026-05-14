"""E344 DocReplicationLog — replication log for cross-region document sync.

Public API
----------
:class:`ReplicationEntry`  — a single replicated document operation
:class:`ReplicaStatus`     — sync status of a single replica
:class:`ReplicationStats`  — aggregate statistics
:class:`DocReplicationLog` — main interface for replication log management
"""

from .log import ReplicationEntry, ReplicaStatus, ReplicationStats, DocReplicationLog

__all__ = ["ReplicationEntry", "ReplicaStatus", "ReplicationStats", "DocReplicationLog"]
