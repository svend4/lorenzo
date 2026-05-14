"""E331 DocWorkspaceManager — multi-workspace document organization.

Public API
----------
:class:`Workspace`         — a workspace with metadata
:class:`WorkspaceMember`   — a user's membership in a workspace
:class:`WorkspaceStats`    — aggregate statistics
:class:`DocWorkspaceManager` — main interface for workspace management
"""

from .manager import Workspace, WorkspaceMember, WorkspaceStats, DocWorkspaceManager

__all__ = ["Workspace", "WorkspaceMember", "WorkspaceStats", "DocWorkspaceManager"]
