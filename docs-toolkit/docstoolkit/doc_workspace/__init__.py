"""E205 Document workspace — group documents, members, settings, and shared resources.

Public API
----------
:class:`WorkspaceRole`  — role enum (OWNER, ADMIN, EDITOR, VIEWER, GUEST)
:class:`Member`         — workspace member record
:class:`Workspace`      — workspace data container
:class:`WorkspaceStats` — aggregate statistics over workspaces
:class:`DocWorkspace`   — main manager class
"""
from docstoolkit.doc_workspace.workspace import (
    DocWorkspace,
    Member,
    Workspace,
    WorkspaceRole,
    WorkspaceStats,
)

__all__ = [
    "DocWorkspace",
    "Member",
    "Workspace",
    "WorkspaceRole",
    "WorkspaceStats",
]
