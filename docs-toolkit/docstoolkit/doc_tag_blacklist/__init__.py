"""E374 DocTagBlacklist — disallowed tag enforcement.

Public API
----------
:class:`BlacklistEntry`   — a single blacklist entry
:class:`BlacklistStats`   — aggregate statistics
:class:`DocTagBlacklist`  — main interface for blacklist management
"""

from .blacklist import BlacklistEntry, BlacklistStats, DocTagBlacklist

__all__ = ["BlacklistEntry", "BlacklistStats", "DocTagBlacklist"]
