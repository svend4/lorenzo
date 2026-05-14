"""E366 DocInvitationStore — manage invitations to access documents.

Public API
----------
:class:`Invitation`         — a single invitation
:class:`InvitationStats`    — aggregate statistics
:class:`DocInvitationStore` — main interface for invitation management
"""

from .store import Invitation, InvitationStats, DocInvitationStore

__all__ = ["Invitation", "InvitationStats", "DocInvitationStore"]
