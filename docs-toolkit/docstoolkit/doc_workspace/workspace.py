"""E205 Document workspace — workspace container grouping docs, members, settings.

The :class:`DocWorkspace` class manages multiple :class:`Workspace` containers,
each with its own members (users with roles), document IDs, and arbitrary
key/value settings. Access control is enforced via :class:`WorkspaceRole`
hierarchy: OWNER > ADMIN > EDITOR > VIEWER > GUEST.

Only Python's standard library is used (``threading``).
"""
from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set


# ---------------------------------------------------------------------------
# Enums and dataclasses
# ---------------------------------------------------------------------------


class WorkspaceRole(Enum):
    """Role within a workspace, ordered most-to-least permissive."""

    OWNER = "owner"
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"
    GUEST = "guest"


# Numeric rank: lower value = more permissive.
_ROLE_RANK: Dict[WorkspaceRole, int] = {
    WorkspaceRole.OWNER: 0,
    WorkspaceRole.ADMIN: 1,
    WorkspaceRole.EDITOR: 2,
    WorkspaceRole.VIEWER: 3,
    WorkspaceRole.GUEST: 4,
}


def _role_meets(actual: WorkspaceRole, required: WorkspaceRole) -> bool:
    """Return True if ``actual`` is at least as permissive as ``required``."""
    return _ROLE_RANK[actual] <= _ROLE_RANK[required]


@dataclass
class Member:
    """A single member of a workspace."""

    user_id: str
    role: WorkspaceRole
    joined_at: float


@dataclass
class Workspace:
    """Container for a workspace: members, documents, and settings."""

    workspace_id: str
    name: str
    owner_id: str
    created_at: float
    members: Dict[str, Member] = field(default_factory=dict)
    doc_ids: Set[str] = field(default_factory=set)
    settings: Dict[str, Any] = field(default_factory=dict)
    archived: bool = False


@dataclass
class WorkspaceStats:
    """Aggregate statistics across all workspaces."""

    total: int
    archived: int
    active: int
    by_role_distribution: Dict[str, int]
    total_docs: int
    total_members: int


# ---------------------------------------------------------------------------
# DocWorkspace
# ---------------------------------------------------------------------------


class DocWorkspace:
    """Thread-safe registry of :class:`Workspace` instances."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._workspaces: Dict[str, Workspace] = {}

    # -- Lifecycle ----------------------------------------------------------

    def create(self, name: str, owner_id: str, now: float = 0.0) -> Workspace:
        """Create a new workspace; owner is auto-added with OWNER role."""
        workspace_id = uuid.uuid4().hex
        owner_member = Member(user_id=owner_id, role=WorkspaceRole.OWNER, joined_at=now)
        ws = Workspace(
            workspace_id=workspace_id,
            name=name,
            owner_id=owner_id,
            created_at=now,
            members={owner_id: owner_member},
        )
        with self._lock:
            self._workspaces[workspace_id] = ws
        return ws

    def get(self, workspace_id: str) -> Optional[Workspace]:
        """Return the workspace by id, or None."""
        with self._lock:
            return self._workspaces.get(workspace_id)

    def archive(self, workspace_id: str) -> bool:
        """Mark a workspace as archived. Returns False if unknown or already archived."""
        with self._lock:
            ws = self._workspaces.get(workspace_id)
            if ws is None or ws.archived:
                return False
            ws.archived = True
            return True

    def restore(self, workspace_id: str) -> bool:
        """Restore (un-archive) a workspace. Returns False if unknown or not archived."""
        with self._lock:
            ws = self._workspaces.get(workspace_id)
            if ws is None or not ws.archived:
                return False
            ws.archived = False
            return True

    def delete(self, workspace_id: str) -> bool:
        """Remove a workspace entirely. Returns False if unknown."""
        with self._lock:
            if workspace_id not in self._workspaces:
                return False
            del self._workspaces[workspace_id]
            return True

    def rename(self, workspace_id: str, new_name: str) -> bool:
        """Change a workspace name. Returns False if unknown."""
        with self._lock:
            ws = self._workspaces.get(workspace_id)
            if ws is None:
                return False
            ws.name = new_name
            return True

    # -- Members ------------------------------------------------------------

    def add_member(
        self,
        workspace_id: str,
        user_id: str,
        role: WorkspaceRole = WorkspaceRole.EDITOR,
        now: float = 0.0,
    ) -> Optional[Member]:
        """Add (or replace) a member; returns the resulting Member, or None if unknown ws."""
        with self._lock:
            ws = self._workspaces.get(workspace_id)
            if ws is None:
                return None
            member = Member(user_id=user_id, role=role, joined_at=now)
            ws.members[user_id] = member
            return member

    def remove_member(self, workspace_id: str, user_id: str) -> bool:
        """Remove a member; refuses to remove the current owner."""
        with self._lock:
            ws = self._workspaces.get(workspace_id)
            if ws is None or user_id not in ws.members:
                return False
            if user_id == ws.owner_id:
                return False
            del ws.members[user_id]
            return True

    def change_role(
        self, workspace_id: str, user_id: str, new_role: WorkspaceRole
    ) -> bool:
        """Change a member's role. Refuses to demote the current owner via this call."""
        with self._lock:
            ws = self._workspaces.get(workspace_id)
            if ws is None or user_id not in ws.members:
                return False
            if user_id == ws.owner_id and new_role != WorkspaceRole.OWNER:
                return False
            ws.members[user_id].role = new_role
            return True

    def transfer_ownership(self, workspace_id: str, new_owner_id: str) -> bool:
        """Transfer ownership; new owner must already be a member. Old owner becomes ADMIN."""
        with self._lock:
            ws = self._workspaces.get(workspace_id)
            if ws is None or new_owner_id not in ws.members:
                return False
            if new_owner_id == ws.owner_id:
                return False
            old_owner_id = ws.owner_id
            ws.owner_id = new_owner_id
            ws.members[new_owner_id].role = WorkspaceRole.OWNER
            if old_owner_id in ws.members:
                ws.members[old_owner_id].role = WorkspaceRole.ADMIN
            return True

    def member_of(self, workspace_id: str, user_id: str) -> Optional[Member]:
        """Return the :class:`Member` record for user_id in this workspace, or None."""
        with self._lock:
            ws = self._workspaces.get(workspace_id)
            if ws is None:
                return None
            return ws.members.get(user_id)

    def can_access(
        self,
        workspace_id: str,
        user_id: str,
        required_role: WorkspaceRole = WorkspaceRole.VIEWER,
    ) -> bool:
        """Return True if user has at least ``required_role`` in the workspace."""
        with self._lock:
            ws = self._workspaces.get(workspace_id)
            if ws is None:
                return False
            member = ws.members.get(user_id)
            if member is None:
                return False
            return _role_meets(member.role, required_role)

    # -- Documents ----------------------------------------------------------

    def add_doc(self, workspace_id: str, doc_id: str) -> bool:
        """Add a doc id to the workspace. False if unknown ws."""
        with self._lock:
            ws = self._workspaces.get(workspace_id)
            if ws is None:
                return False
            ws.doc_ids.add(doc_id)
            return True

    def remove_doc(self, workspace_id: str, doc_id: str) -> bool:
        """Remove a doc id from the workspace. False if unknown ws or doc not present."""
        with self._lock:
            ws = self._workspaces.get(workspace_id)
            if ws is None or doc_id not in ws.doc_ids:
                return False
            ws.doc_ids.discard(doc_id)
            return True

    # -- Settings -----------------------------------------------------------

    def set_setting(self, workspace_id: str, key: str, value: Any) -> bool:
        """Set a settings key=value. False if unknown ws."""
        with self._lock:
            ws = self._workspaces.get(workspace_id)
            if ws is None:
                return False
            ws.settings[key] = value
            return True

    def get_setting(self, workspace_id: str, key: str, default: Any = None) -> Any:
        """Get a settings value; returns ``default`` if unknown ws or missing key."""
        with self._lock:
            ws = self._workspaces.get(workspace_id)
            if ws is None:
                return default
            return ws.settings.get(key, default)

    # -- Queries ------------------------------------------------------------

    def workspaces_for_user(self, user_id: str) -> List[Workspace]:
        """List workspaces where user_id is a member."""
        with self._lock:
            return [ws for ws in self._workspaces.values() if user_id in ws.members]

    def workspaces_for_doc(self, doc_id: str) -> List[Workspace]:
        """List workspaces that contain the given doc_id."""
        with self._lock:
            return [ws for ws in self._workspaces.values() if doc_id in ws.doc_ids]

    def list_active(self) -> List[Workspace]:
        """List workspaces that are not archived."""
        with self._lock:
            return [ws for ws in self._workspaces.values() if not ws.archived]

    def list_archived(self) -> List[Workspace]:
        """List workspaces that are archived."""
        with self._lock:
            return [ws for ws in self._workspaces.values() if ws.archived]

    # -- Stats --------------------------------------------------------------

    def stats(self) -> WorkspaceStats:
        """Return aggregated stats over all workspaces."""
        with self._lock:
            total = len(self._workspaces)
            archived = sum(1 for ws in self._workspaces.values() if ws.archived)
            active = total - archived
            role_dist: Dict[str, int] = {r.name: 0 for r in WorkspaceRole}
            total_docs = 0
            total_members = 0
            for ws in self._workspaces.values():
                total_docs += len(ws.doc_ids)
                total_members += len(ws.members)
                for m in ws.members.values():
                    role_dist[m.role.name] = role_dist.get(m.role.name, 0) + 1
            return WorkspaceStats(
                total=total,
                archived=archived,
                active=active,
                by_role_distribution=role_dist,
                total_docs=total_docs,
                total_members=total_members,
            )

    @property
    def workspace_count(self) -> int:
        """Total number of workspaces (active + archived)."""
        with self._lock:
            return len(self._workspaces)

    def clear(self) -> None:
        """Drop all workspaces."""
        with self._lock:
            self._workspaces.clear()
