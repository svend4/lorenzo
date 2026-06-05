"""E331 DocWorkspaceManager — multi-workspace document organization.

Pure stdlib implementation. Thread-safe via :class:`threading.Lock`.
"""
from __future__ import annotations

import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass
class Workspace:
    """A workspace with metadata."""

    workspace_id: str
    name: str
    owner: str
    created_at: float = 0.0
    description: str = ""
    archived: bool = False


@dataclass
class WorkspaceMember:
    """A user's membership in a workspace."""

    workspace_id: str
    user_id: str
    role: str = "member"  # "owner", "admin", "member", "viewer"
    joined_at: float = 0.0


@dataclass
class WorkspaceStats:
    """Aggregate statistics about workspaces."""

    total_workspaces: int  # non-archived
    archived_count: int
    total_members: int  # sum of memberships
    total_docs: int  # sum of docs across workspaces


# ---------------------------------------------------------------------------
# DocWorkspaceManager
# ---------------------------------------------------------------------------


class DocWorkspaceManager:
    """Thread-safe manager for workspaces, members, and document assignments."""

    def __init__(self) -> None:
        self._workspaces: Dict[str, Workspace] = {}
        self._members: Dict[Tuple[str, str], WorkspaceMember] = {}
        self._docs: Dict[str, Set[str]] = {}
        self._lock = threading.Lock()

    # -- Workspaces ---------------------------------------------------------

    def create_workspace(
        self,
        name: str,
        owner: str,
        description: str = "",
        now: Optional[float] = None,
    ) -> Workspace:
        """Create a new workspace; the owner also becomes a member with role "owner"."""
        ts = time.time() if now is None else now
        with self._lock:
            workspace_id = str(uuid.uuid4())
            ws = Workspace(
                workspace_id=workspace_id,
                name=name,
                owner=owner,
                created_at=ts,
                description=description,
                archived=False,
            )
            self._workspaces[workspace_id] = ws
            self._members[(workspace_id, owner)] = WorkspaceMember(
                workspace_id=workspace_id,
                user_id=owner,
                role="owner",
                joined_at=ts,
            )
            self._docs[workspace_id] = set()
            return ws

    def delete_workspace(self, workspace_id: str) -> bool:
        """Remove workspace and all of its members and doc assignments."""
        with self._lock:
            if workspace_id not in self._workspaces:
                return False
            del self._workspaces[workspace_id]
            keys = [k for k in self._members if k[0] == workspace_id]
            for k in keys:
                del self._members[k]
            self._docs.pop(workspace_id, None)
            return True

    def archive_workspace(self, workspace_id: str) -> bool:
        """Mark workspace as archived."""
        with self._lock:
            ws = self._workspaces.get(workspace_id)
            if ws is None:
                return False
            ws.archived = True
            return True

    def unarchive_workspace(self, workspace_id: str) -> bool:
        """Mark workspace as not archived."""
        with self._lock:
            ws = self._workspaces.get(workspace_id)
            if ws is None:
                return False
            ws.archived = False
            return True

    def get_workspace(self, workspace_id: str) -> Optional[Workspace]:
        """Return a workspace by id, or None."""
        with self._lock:
            return self._workspaces.get(workspace_id)

    def list_workspaces(self, include_archived: bool = False) -> List[Workspace]:
        """Return all workspaces sorted by ``created_at``."""
        with self._lock:
            items = list(self._workspaces.values())
            if not include_archived:
                items = [w for w in items if not w.archived]
            return sorted(items, key=lambda w: w.created_at)

    # -- Members ------------------------------------------------------------

    def add_member(
        self,
        workspace_id: str,
        user_id: str,
        role: str = "member",
        now: Optional[float] = None,
    ) -> Optional[WorkspaceMember]:
        """Add or replace a member; returns None if workspace not found."""
        ts = time.time() if now is None else now
        with self._lock:
            if workspace_id not in self._workspaces:
                return None
            member = WorkspaceMember(
                workspace_id=workspace_id,
                user_id=user_id,
                role=role,
                joined_at=ts,
            )
            self._members[(workspace_id, user_id)] = member
            return member

    def remove_member(self, workspace_id: str, user_id: str) -> bool:
        """Remove a member; True if existed."""
        with self._lock:
            key = (workspace_id, user_id)
            if key not in self._members:
                return False
            del self._members[key]
            return True

    def get_member(self, workspace_id: str, user_id: str) -> Optional[WorkspaceMember]:
        """Return a member or None."""
        with self._lock:
            return self._members.get((workspace_id, user_id))

    def members_of(self, workspace_id: str) -> List[WorkspaceMember]:
        """Return all members of a workspace, sorted by ``user_id``."""
        with self._lock:
            members = [m for k, m in self._members.items() if k[0] == workspace_id]
            return sorted(members, key=lambda m: m.user_id)

    def workspaces_for_user(self, user_id: str) -> List[Workspace]:
        """Return all workspaces a user is a member of, sorted by ``name``."""
        with self._lock:
            ws_ids = [k[0] for k in self._members if k[1] == user_id]
            workspaces = [self._workspaces[wid] for wid in ws_ids if wid in self._workspaces]
            return sorted(workspaces, key=lambda w: w.name)

    # -- Documents ----------------------------------------------------------

    def add_doc(self, workspace_id: str, doc_id: str) -> bool:
        """Attach a doc to a workspace; True if newly added."""
        with self._lock:
            if workspace_id not in self._workspaces:
                return False
            bucket = self._docs.setdefault(workspace_id, set())
            if doc_id in bucket:
                return False
            bucket.add(doc_id)
            return True

    def remove_doc(self, workspace_id: str, doc_id: str) -> bool:
        """Detach a doc from a workspace; True if existed."""
        with self._lock:
            bucket = self._docs.get(workspace_id)
            if bucket is None or doc_id not in bucket:
                return False
            bucket.remove(doc_id)
            return True

    def docs_in_workspace(self, workspace_id: str) -> List[str]:
        """Return sorted list of doc ids in a workspace."""
        with self._lock:
            bucket = self._docs.get(workspace_id, set())
            return sorted(bucket)

    def workspaces_for_doc(self, doc_id: str) -> List[str]:
        """Return sorted list of workspace ids that contain this doc."""
        with self._lock:
            return sorted(wid for wid, docs in self._docs.items() if doc_id in docs)

    # -- Stats --------------------------------------------------------------

    def stats(self) -> WorkspaceStats:
        """Return aggregate statistics."""
        with self._lock:
            total_workspaces = sum(1 for w in self._workspaces.values() if not w.archived)
            archived_count = sum(1 for w in self._workspaces.values() if w.archived)
            total_members = len(self._members)
            total_docs = sum(len(d) for d in self._docs.values())
            return WorkspaceStats(
                total_workspaces=total_workspaces,
                archived_count=archived_count,
                total_members=total_members,
                total_docs=total_docs,
            )
