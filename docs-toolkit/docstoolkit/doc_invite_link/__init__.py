"""E436 DocInviteLink — invite link generation and consumption.

Public API
----------
:class:`InviteLink`     — a single invite link
:class:`LinkStats`      — aggregate statistics
:class:`DocInviteLink`  — main interface for invite link management
"""

from .link import InviteLink, LinkStats, DocInviteLink

__all__ = ["InviteLink", "LinkStats", "DocInviteLink"]
