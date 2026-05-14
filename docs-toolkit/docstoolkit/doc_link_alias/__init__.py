"""E425 DocLinkAlias — alias mapping for document hyperlinks.

Public API
----------
:class:`LinkAliasEntry`  — a single link alias entry
:class:`AliasStats`      — aggregate statistics
:class:`DocLinkAlias`    — main interface for link alias management
"""

from .alias import LinkAliasEntry, AliasStats, DocLinkAlias

__all__ = ["LinkAliasEntry", "AliasStats", "DocLinkAlias"]
