"""Document collaboration invitation system.

Public API
----------
- ``InviteStatus``  — enum of invitation lifecycle states
- ``InviteRole``    — enum of collaboration roles
- ``Invitation``    — dataclass representing an invite
- ``InviteStats``   — aggregate statistics
- ``DocInvitation`` — manager class with create/accept/decline/revoke/expire
"""

from docstoolkit.doc_invitation.invitation import (
    InviteStatus,
    InviteRole,
    Invitation,
    InviteStats,
    DocInvitation,
)

__all__ = [
    "InviteStatus",
    "InviteRole",
    "Invitation",
    "InviteStats",
    "DocInvitation",
]
