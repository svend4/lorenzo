"""Tests for E331 DocWorkspaceManager."""
from __future__ import annotations

import threading
import uuid

import pytest

from docstoolkit.doc_workspace_manager import (
    DocWorkspaceManager,
    Workspace,
    WorkspaceMember,
    WorkspaceStats,
)


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


class TestWorkspaceDataclass:
    def test_basic_fields(self):
        ws = Workspace(workspace_id="w1", name="Alpha", owner="u1")
        assert ws.workspace_id == "w1"
        assert ws.name == "Alpha"
        assert ws.owner == "u1"

    def test_defaults(self):
        ws = Workspace(workspace_id="w1", name="Alpha", owner="u1")
        assert ws.created_at == 0.0
        assert ws.description == ""
        assert ws.archived is False

    def test_custom_values(self):
        ws = Workspace(
            workspace_id="w1",
            name="Alpha",
            owner="u1",
            created_at=10.0,
            description="desc",
            archived=True,
        )
        assert ws.created_at == 10.0
        assert ws.description == "desc"
        assert ws.archived is True


class TestWorkspaceMemberDataclass:
    def test_basic_fields(self):
        m = WorkspaceMember(workspace_id="w1", user_id="u1")
        assert m.workspace_id == "w1"
        assert m.user_id == "u1"

    def test_default_role(self):
        m = WorkspaceMember(workspace_id="w1", user_id="u1")
        assert m.role == "member"
        assert m.joined_at == 0.0

    def test_custom_role(self):
        m = WorkspaceMember(workspace_id="w1", user_id="u1", role="admin", joined_at=42.0)
        assert m.role == "admin"
        assert m.joined_at == 42.0


class TestWorkspaceStatsDataclass:
    def test_fields(self):
        s = WorkspaceStats(total_workspaces=1, archived_count=2, total_members=3, total_docs=4)
        assert s.total_workspaces == 1
        assert s.archived_count == 2
        assert s.total_members == 3
        assert s.total_docs == 4


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------


class TestConstruction:
    def test_empty_manager(self):
        m = DocWorkspaceManager()
        assert m.list_workspaces() == []

    def test_initial_stats(self):
        m = DocWorkspaceManager()
        s = m.stats()
        assert s.total_workspaces == 0
        assert s.archived_count == 0
        assert s.total_members == 0
        assert s.total_docs == 0

    def test_independent_instances(self):
        m1 = DocWorkspaceManager()
        m2 = DocWorkspaceManager()
        m1.create_workspace("A", "u1")
        assert m2.list_workspaces() == []


# ---------------------------------------------------------------------------
# create_workspace
# ---------------------------------------------------------------------------


class TestCreateWorkspace:
    def test_returns_workspace(self):
        m = DocWorkspaceManager()
        ws = m.create_workspace("Alpha", "u1")
        assert isinstance(ws, Workspace)
        assert ws.name == "Alpha"
        assert ws.owner == "u1"

    def test_id_is_uuid(self):
        m = DocWorkspaceManager()
        ws = m.create_workspace("Alpha", "u1")
        # parse should succeed
        uuid.UUID(ws.workspace_id)

    def test_ids_unique(self):
        m = DocWorkspaceManager()
        a = m.create_workspace("A", "u1")
        b = m.create_workspace("B", "u1")
        assert a.workspace_id != b.workspace_id

    def test_owner_becomes_member(self):
        m = DocWorkspaceManager()
        ws = m.create_workspace("Alpha", "u1")
        member = m.get_member(ws.workspace_id, "u1")
        assert member is not None
        assert member.role == "owner"

    def test_timestamp_set(self):
        m = DocWorkspaceManager()
        ws = m.create_workspace("Alpha", "u1", now=12345.0)
        assert ws.created_at == 12345.0

    def test_owner_joined_at_matches(self):
        m = DocWorkspaceManager()
        ws = m.create_workspace("Alpha", "u1", now=999.0)
        member = m.get_member(ws.workspace_id, "u1")
        assert member.joined_at == 999.0

    def test_description(self):
        m = DocWorkspaceManager()
        ws = m.create_workspace("Alpha", "u1", description="My ws")
        assert ws.description == "My ws"

    def test_default_now_is_current(self):
        m = DocWorkspaceManager()
        ws = m.create_workspace("Alpha", "u1")
        assert ws.created_at > 0


# ---------------------------------------------------------------------------
# delete_workspace
# ---------------------------------------------------------------------------


class TestDeleteWorkspace:
    def test_returns_true_if_existed(self):
        m = DocWorkspaceManager()
        ws = m.create_workspace("A", "u1")
        assert m.delete_workspace(ws.workspace_id) is True

    def test_returns_false_if_missing(self):
        m = DocWorkspaceManager()
        assert m.delete_workspace("nope") is False

    def test_workspace_removed(self):
        m = DocWorkspaceManager()
        ws = m.create_workspace("A", "u1")
        m.delete_workspace(ws.workspace_id)
        assert m.get_workspace(ws.workspace_id) is None

    def test_members_removed(self):
        m = DocWorkspaceManager()
        ws = m.create_workspace("A", "u1")
        m.add_member(ws.workspace_id, "u2")
        m.delete_workspace(ws.workspace_id)
        assert m.get_member(ws.workspace_id, "u1") is None
        assert m.get_member(ws.workspace_id, "u2") is None

    def test_docs_removed(self):
        m = DocWorkspaceManager()
        ws = m.create_workspace("A", "u1")
        m.add_doc(ws.workspace_id, "d1")
        m.delete_workspace(ws.workspace_id)
        assert m.docs_in_workspace(ws.workspace_id) == []


# ---------------------------------------------------------------------------
# archive / unarchive
# ---------------------------------------------------------------------------


class TestArchive:
    def test_archive_true(self):
        m = DocWorkspaceManager()
        ws = m.create_workspace("A", "u1")
        assert m.archive_workspace(ws.workspace_id) is True

    def test_archive_false_for_missing(self):
        m = DocWorkspaceManager()
        assert m.archive_workspace("nope") is False

    def test_archived_flag_set(self):
        m = DocWorkspaceManager()
        ws = m.create_workspace("A", "u1")
        m.archive_workspace(ws.workspace_id)
        assert m.get_workspace(ws.workspace_id).archived is True


class TestUnarchive:
    def test_unarchive_true(self):
        m = DocWorkspaceManager()
        ws = m.create_workspace("A", "u1")
        m.archive_workspace(ws.workspace_id)
        assert m.unarchive_workspace(ws.workspace_id) is True

    def test_unarchive_false_for_missing(self):
        m = DocWorkspaceManager()
        assert m.unarchive_workspace("nope") is False

    def test_archived_flag_cleared(self):
        m = DocWorkspaceManager()
        ws = m.create_workspace("A", "u1")
        m.archive_workspace(ws.workspace_id)
        m.unarchive_workspace(ws.workspace_id)
        assert m.get_workspace(ws.workspace_id).archived is False


# ---------------------------------------------------------------------------
# get_workspace
# ---------------------------------------------------------------------------


class TestGetWorkspace:
    def test_found(self):
        m = DocWorkspaceManager()
        ws = m.create_workspace("A", "u1")
        got = m.get_workspace(ws.workspace_id)
        assert got is not None
        assert got.name == "A"

    def test_not_found(self):
        m = DocWorkspaceManager()
        assert m.get_workspace("nope") is None


# ---------------------------------------------------------------------------
# list_workspaces
# ---------------------------------------------------------------------------


class TestListWorkspaces:
    def test_sorted_by_created_at(self):
        m = DocWorkspaceManager()
        a = m.create_workspace("A", "u1", now=300.0)
        b = m.create_workspace("B", "u1", now=100.0)
        c = m.create_workspace("C", "u1", now=200.0)
        ws_list = m.list_workspaces()
        assert [w.workspace_id for w in ws_list] == [b.workspace_id, c.workspace_id, a.workspace_id]

    def test_excludes_archived_by_default(self):
        m = DocWorkspaceManager()
        a = m.create_workspace("A", "u1")
        b = m.create_workspace("B", "u1")
        m.archive_workspace(a.workspace_id)
        ws_list = m.list_workspaces()
        assert [w.workspace_id for w in ws_list] == [b.workspace_id]

    def test_include_archived(self):
        m = DocWorkspaceManager()
        a = m.create_workspace("A", "u1", now=1.0)
        b = m.create_workspace("B", "u1", now=2.0)
        m.archive_workspace(a.workspace_id)
        ws_list = m.list_workspaces(include_archived=True)
        assert len(ws_list) == 2

    def test_empty(self):
        m = DocWorkspaceManager()
        assert m.list_workspaces() == []


# ---------------------------------------------------------------------------
# add_member
# ---------------------------------------------------------------------------


class TestAddMember:
    def test_returns_member(self):
        m = DocWorkspaceManager()
        ws = m.create_workspace("A", "u1")
        member = m.add_member(ws.workspace_id, "u2")
        assert isinstance(member, WorkspaceMember)
        assert member.user_id == "u2"
        assert member.role == "member"

    def test_replace_existing(self):
        m = DocWorkspaceManager()
        ws = m.create_workspace("A", "u1")
        m.add_member(ws.workspace_id, "u2", role="member")
        m.add_member(ws.workspace_id, "u2", role="admin")
        got = m.get_member(ws.workspace_id, "u2")
        assert got.role == "admin"

    def test_missing_workspace_returns_none(self):
        m = DocWorkspaceManager()
        assert m.add_member("nope", "u1") is None

    def test_joined_at_set(self):
        m = DocWorkspaceManager()
        ws = m.create_workspace("A", "u1")
        member = m.add_member(ws.workspace_id, "u2", now=500.0)
        assert member.joined_at == 500.0


# ---------------------------------------------------------------------------
# remove_member
# ---------------------------------------------------------------------------


class TestRemoveMember:
    def test_returns_true_if_existed(self):
        m = DocWorkspaceManager()
        ws = m.create_workspace("A", "u1")
        m.add_member(ws.workspace_id, "u2")
        assert m.remove_member(ws.workspace_id, "u2") is True

    def test_returns_false_if_missing(self):
        m = DocWorkspaceManager()
        ws = m.create_workspace("A", "u1")
        assert m.remove_member(ws.workspace_id, "ghost") is False

    def test_actually_removed(self):
        m = DocWorkspaceManager()
        ws = m.create_workspace("A", "u1")
        m.add_member(ws.workspace_id, "u2")
        m.remove_member(ws.workspace_id, "u2")
        assert m.get_member(ws.workspace_id, "u2") is None


# ---------------------------------------------------------------------------
# get_member
# ---------------------------------------------------------------------------


class TestGetMember:
    def test_found(self):
        m = DocWorkspaceManager()
        ws = m.create_workspace("A", "u1")
        got = m.get_member(ws.workspace_id, "u1")
        assert got is not None
        assert got.role == "owner"

    def test_not_found(self):
        m = DocWorkspaceManager()
        ws = m.create_workspace("A", "u1")
        assert m.get_member(ws.workspace_id, "ghost") is None


# ---------------------------------------------------------------------------
# members_of
# ---------------------------------------------------------------------------


class TestMembersOf:
    def test_sorted_by_user_id(self):
        m = DocWorkspaceManager()
        ws = m.create_workspace("A", "alpha")
        m.add_member(ws.workspace_id, "charlie")
        m.add_member(ws.workspace_id, "bravo")
        ids = [mem.user_id for mem in m.members_of(ws.workspace_id)]
        assert ids == ["alpha", "bravo", "charlie"]

    def test_empty_for_missing_workspace(self):
        m = DocWorkspaceManager()
        assert m.members_of("nope") == []

    def test_only_members_of_target_workspace(self):
        m = DocWorkspaceManager()
        a = m.create_workspace("A", "u1")
        b = m.create_workspace("B", "u2")
        m.add_member(a.workspace_id, "u3")
        ids = [mem.user_id for mem in m.members_of(b.workspace_id)]
        assert ids == ["u2"]


# ---------------------------------------------------------------------------
# workspaces_for_user
# ---------------------------------------------------------------------------


class TestWorkspacesForUser:
    def test_sorted_by_name(self):
        m = DocWorkspaceManager()
        c = m.create_workspace("Charlie", "u1")
        a = m.create_workspace("Alpha", "u2")
        b = m.create_workspace("Bravo", "u2")
        m.add_member(c.workspace_id, "u2")
        names = [w.name for w in m.workspaces_for_user("u2")]
        assert names == ["Alpha", "Bravo", "Charlie"]

    def test_empty_for_unknown(self):
        m = DocWorkspaceManager()
        m.create_workspace("A", "u1")
        assert m.workspaces_for_user("ghost") == []

    def test_owner_included(self):
        m = DocWorkspaceManager()
        ws = m.create_workspace("A", "u1")
        result = m.workspaces_for_user("u1")
        assert [w.workspace_id for w in result] == [ws.workspace_id]


# ---------------------------------------------------------------------------
# add_doc
# ---------------------------------------------------------------------------


class TestAddDoc:
    def test_true_if_new(self):
        m = DocWorkspaceManager()
        ws = m.create_workspace("A", "u1")
        assert m.add_doc(ws.workspace_id, "d1") is True

    def test_false_if_duplicate(self):
        m = DocWorkspaceManager()
        ws = m.create_workspace("A", "u1")
        m.add_doc(ws.workspace_id, "d1")
        assert m.add_doc(ws.workspace_id, "d1") is False

    def test_false_if_missing_workspace(self):
        m = DocWorkspaceManager()
        assert m.add_doc("nope", "d1") is False


# ---------------------------------------------------------------------------
# remove_doc
# ---------------------------------------------------------------------------


class TestRemoveDoc:
    def test_true_if_existed(self):
        m = DocWorkspaceManager()
        ws = m.create_workspace("A", "u1")
        m.add_doc(ws.workspace_id, "d1")
        assert m.remove_doc(ws.workspace_id, "d1") is True

    def test_false_if_missing(self):
        m = DocWorkspaceManager()
        ws = m.create_workspace("A", "u1")
        assert m.remove_doc(ws.workspace_id, "d1") is False

    def test_actually_removed(self):
        m = DocWorkspaceManager()
        ws = m.create_workspace("A", "u1")
        m.add_doc(ws.workspace_id, "d1")
        m.remove_doc(ws.workspace_id, "d1")
        assert m.docs_in_workspace(ws.workspace_id) == []


# ---------------------------------------------------------------------------
# docs_in_workspace
# ---------------------------------------------------------------------------


class TestDocsInWorkspace:
    def test_sorted(self):
        m = DocWorkspaceManager()
        ws = m.create_workspace("A", "u1")
        m.add_doc(ws.workspace_id, "c")
        m.add_doc(ws.workspace_id, "a")
        m.add_doc(ws.workspace_id, "b")
        assert m.docs_in_workspace(ws.workspace_id) == ["a", "b", "c"]

    def test_empty(self):
        m = DocWorkspaceManager()
        ws = m.create_workspace("A", "u1")
        assert m.docs_in_workspace(ws.workspace_id) == []

    def test_empty_for_missing_workspace(self):
        m = DocWorkspaceManager()
        assert m.docs_in_workspace("nope") == []


# ---------------------------------------------------------------------------
# workspaces_for_doc
# ---------------------------------------------------------------------------


class TestWorkspacesForDoc:
    def test_sorted_cross_workspace(self):
        m = DocWorkspaceManager()
        a = m.create_workspace("A", "u1")
        b = m.create_workspace("B", "u1")
        m.add_doc(a.workspace_id, "shared")
        m.add_doc(b.workspace_id, "shared")
        result = m.workspaces_for_doc("shared")
        assert result == sorted([a.workspace_id, b.workspace_id])

    def test_empty(self):
        m = DocWorkspaceManager()
        assert m.workspaces_for_doc("d1") == []

    def test_single(self):
        m = DocWorkspaceManager()
        ws = m.create_workspace("A", "u1")
        m.add_doc(ws.workspace_id, "d1")
        assert m.workspaces_for_doc("d1") == [ws.workspace_id]


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------


class TestStats:
    def test_totals(self):
        m = DocWorkspaceManager()
        a = m.create_workspace("A", "u1")
        b = m.create_workspace("B", "u2")
        m.add_member(a.workspace_id, "u3")
        m.add_doc(a.workspace_id, "d1")
        m.add_doc(a.workspace_id, "d2")
        m.add_doc(b.workspace_id, "d3")
        s = m.stats()
        assert s.total_workspaces == 2
        assert s.archived_count == 0
        assert s.total_members == 3
        assert s.total_docs == 3

    def test_archived_count(self):
        m = DocWorkspaceManager()
        a = m.create_workspace("A", "u1")
        m.create_workspace("B", "u2")
        m.archive_workspace(a.workspace_id)
        s = m.stats()
        assert s.total_workspaces == 1
        assert s.archived_count == 1

    def test_empty_stats(self):
        m = DocWorkspaceManager()
        s = m.stats()
        assert s.total_workspaces == 0
        assert s.archived_count == 0
        assert s.total_members == 0
        assert s.total_docs == 0


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------


class TestThreadSafety:
    def test_concurrent_create_workspace(self):
        m = DocWorkspaceManager()
        results = []

        def worker(i):
            ws = m.create_workspace(f"W{i}", f"u{i}")
            results.append(ws.workspace_id)

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert len(results) == 20
        assert len(set(results)) == 20
        assert len(m.list_workspaces()) == 20

    def test_concurrent_add_member(self):
        m = DocWorkspaceManager()
        ws = m.create_workspace("A", "owner")

        def worker(i):
            m.add_member(ws.workspace_id, f"user{i}")

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(30)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        # 30 user members + 1 owner
        assert len(m.members_of(ws.workspace_id)) == 31

    def test_concurrent_mixed(self):
        m = DocWorkspaceManager()
        ws = m.create_workspace("A", "owner")

        def add_workspace(i):
            m.create_workspace(f"W{i}", "u1")

        def add_member(i):
            m.add_member(ws.workspace_id, f"u{i}")

        threads = []
        for i in range(10):
            threads.append(threading.Thread(target=add_workspace, args=(i,)))
            threads.append(threading.Thread(target=add_member, args=(i,)))
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert len(m.list_workspaces()) == 11  # 10 new + initial
        assert len(m.members_of(ws.workspace_id)) == 11  # 10 new + owner
