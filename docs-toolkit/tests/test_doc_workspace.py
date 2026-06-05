"""Tests for E205 doc_workspace module."""
from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_workspace import (
    DocWorkspace,
    Member,
    Workspace,
    WorkspaceRole,
    WorkspaceStats,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def make_ws(dw: DocWorkspace, name: str = "ws", owner: str = "alice", now: float = 1.0):
    return dw.create(name=name, owner_id=owner, now=now)


# ---------------------------------------------------------------------------
# Enum / dataclass tests
# ---------------------------------------------------------------------------


class TestWorkspaceRole:
    def test_owner_value(self):
        assert WorkspaceRole.OWNER.value == "owner"

    def test_all_roles_distinct(self):
        names = {r.name for r in WorkspaceRole}
        assert names == {"OWNER", "ADMIN", "EDITOR", "VIEWER", "GUEST"}

    def test_five_roles(self):
        assert len(list(WorkspaceRole)) == 5


class TestMember:
    def test_create_member(self):
        m = Member(user_id="u1", role=WorkspaceRole.EDITOR, joined_at=10.0)
        assert m.user_id == "u1"
        assert m.role is WorkspaceRole.EDITOR
        assert m.joined_at == 10.0

    def test_member_equality(self):
        a = Member(user_id="u", role=WorkspaceRole.VIEWER, joined_at=1.0)
        b = Member(user_id="u", role=WorkspaceRole.VIEWER, joined_at=1.0)
        assert a == b


class TestWorkspace:
    def test_create_workspace_defaults(self):
        ws = Workspace(workspace_id="w1", name="N", owner_id="o", created_at=0.0)
        assert ws.members == {}
        assert ws.doc_ids == set()
        assert ws.settings == {}
        assert ws.archived is False

    def test_workspace_fields(self):
        ws = Workspace(workspace_id="w1", name="N", owner_id="o", created_at=5.0)
        assert ws.workspace_id == "w1"
        assert ws.name == "N"
        assert ws.owner_id == "o"
        assert ws.created_at == 5.0


class TestWorkspaceStats:
    def test_construct(self):
        s = WorkspaceStats(
            total=2,
            archived=1,
            active=1,
            by_role_distribution={"OWNER": 2},
            total_docs=3,
            total_members=4,
        )
        assert s.total == 2
        assert s.archived == 1
        assert s.active == 1
        assert s.total_docs == 3
        assert s.total_members == 4
        assert s.by_role_distribution == {"OWNER": 2}


# ---------------------------------------------------------------------------
# Method tests
# ---------------------------------------------------------------------------


class TestCreate:
    def test_create_returns_workspace(self):
        dw = DocWorkspace()
        ws = dw.create(name="proj", owner_id="alice", now=10.0)
        assert isinstance(ws, Workspace)
        assert ws.name == "proj"
        assert ws.owner_id == "alice"
        assert ws.created_at == 10.0

    def test_create_assigns_unique_ids(self):
        dw = DocWorkspace()
        a = dw.create("a", "u1")
        b = dw.create("b", "u1")
        assert a.workspace_id != b.workspace_id

    def test_owner_auto_added(self):
        dw = DocWorkspace()
        ws = dw.create("proj", "alice", now=3.0)
        assert "alice" in ws.members
        m = ws.members["alice"]
        assert m.role is WorkspaceRole.OWNER
        assert m.joined_at == 3.0

    def test_archived_initially_false(self):
        dw = DocWorkspace()
        ws = dw.create("p", "u")
        assert ws.archived is False


class TestGet:
    def test_get_existing(self):
        dw = DocWorkspace()
        ws = make_ws(dw)
        assert dw.get(ws.workspace_id) is ws

    def test_get_missing_returns_none(self):
        dw = DocWorkspace()
        assert dw.get("nope") is None


class TestArchive:
    def test_archive_success(self):
        dw = DocWorkspace()
        ws = make_ws(dw)
        assert dw.archive(ws.workspace_id) is True
        assert ws.archived is True

    def test_archive_unknown(self):
        dw = DocWorkspace()
        assert dw.archive("nope") is False

    def test_archive_already_archived(self):
        dw = DocWorkspace()
        ws = make_ws(dw)
        dw.archive(ws.workspace_id)
        assert dw.archive(ws.workspace_id) is False


class TestRestore:
    def test_restore_success(self):
        dw = DocWorkspace()
        ws = make_ws(dw)
        dw.archive(ws.workspace_id)
        assert dw.restore(ws.workspace_id) is True
        assert ws.archived is False

    def test_restore_unknown(self):
        dw = DocWorkspace()
        assert dw.restore("nope") is False

    def test_restore_not_archived(self):
        dw = DocWorkspace()
        ws = make_ws(dw)
        assert dw.restore(ws.workspace_id) is False


class TestDelete:
    def test_delete_success(self):
        dw = DocWorkspace()
        ws = make_ws(dw)
        assert dw.delete(ws.workspace_id) is True
        assert dw.get(ws.workspace_id) is None

    def test_delete_unknown(self):
        dw = DocWorkspace()
        assert dw.delete("nope") is False


class TestAddMember:
    def test_add_member_default_role(self):
        dw = DocWorkspace()
        ws = make_ws(dw)
        m = dw.add_member(ws.workspace_id, "bob", now=2.0)
        assert m is not None
        assert m.user_id == "bob"
        assert m.role is WorkspaceRole.EDITOR
        assert m.joined_at == 2.0
        assert "bob" in ws.members

    def test_add_member_custom_role(self):
        dw = DocWorkspace()
        ws = make_ws(dw)
        m = dw.add_member(ws.workspace_id, "bob", role=WorkspaceRole.ADMIN, now=1.0)
        assert m.role is WorkspaceRole.ADMIN

    def test_add_member_unknown_workspace(self):
        dw = DocWorkspace()
        assert dw.add_member("nope", "bob") is None

    def test_add_member_overrides_existing(self):
        dw = DocWorkspace()
        ws = make_ws(dw)
        dw.add_member(ws.workspace_id, "bob", role=WorkspaceRole.VIEWER)
        dw.add_member(ws.workspace_id, "bob", role=WorkspaceRole.ADMIN)
        assert ws.members["bob"].role is WorkspaceRole.ADMIN


class TestRemoveMember:
    def test_remove_member_success(self):
        dw = DocWorkspace()
        ws = make_ws(dw)
        dw.add_member(ws.workspace_id, "bob")
        assert dw.remove_member(ws.workspace_id, "bob") is True
        assert "bob" not in ws.members

    def test_remove_member_unknown_user(self):
        dw = DocWorkspace()
        ws = make_ws(dw)
        assert dw.remove_member(ws.workspace_id, "ghost") is False

    def test_remove_member_unknown_ws(self):
        dw = DocWorkspace()
        assert dw.remove_member("nope", "bob") is False

    def test_cannot_remove_owner(self):
        dw = DocWorkspace()
        ws = make_ws(dw, owner="alice")
        assert dw.remove_member(ws.workspace_id, "alice") is False
        assert "alice" in ws.members


class TestChangeRole:
    def test_change_role_success(self):
        dw = DocWorkspace()
        ws = make_ws(dw)
        dw.add_member(ws.workspace_id, "bob", role=WorkspaceRole.VIEWER)
        assert dw.change_role(ws.workspace_id, "bob", WorkspaceRole.ADMIN) is True
        assert ws.members["bob"].role is WorkspaceRole.ADMIN

    def test_change_role_unknown_user(self):
        dw = DocWorkspace()
        ws = make_ws(dw)
        assert dw.change_role(ws.workspace_id, "ghost", WorkspaceRole.ADMIN) is False

    def test_change_role_unknown_ws(self):
        dw = DocWorkspace()
        assert dw.change_role("nope", "bob", WorkspaceRole.ADMIN) is False

    def test_cannot_demote_owner(self):
        dw = DocWorkspace()
        ws = make_ws(dw, owner="alice")
        assert dw.change_role(ws.workspace_id, "alice", WorkspaceRole.EDITOR) is False
        assert ws.members["alice"].role is WorkspaceRole.OWNER


class TestTransferOwnership:
    def test_transfer_success(self):
        dw = DocWorkspace()
        ws = make_ws(dw, owner="alice")
        dw.add_member(ws.workspace_id, "bob", role=WorkspaceRole.EDITOR)
        assert dw.transfer_ownership(ws.workspace_id, "bob") is True
        assert ws.owner_id == "bob"
        assert ws.members["bob"].role is WorkspaceRole.OWNER
        assert ws.members["alice"].role is WorkspaceRole.ADMIN

    def test_transfer_unknown_ws(self):
        dw = DocWorkspace()
        assert dw.transfer_ownership("nope", "bob") is False

    def test_transfer_not_a_member(self):
        dw = DocWorkspace()
        ws = make_ws(dw)
        assert dw.transfer_ownership(ws.workspace_id, "ghost") is False

    def test_transfer_to_self_noop(self):
        dw = DocWorkspace()
        ws = make_ws(dw, owner="alice")
        assert dw.transfer_ownership(ws.workspace_id, "alice") is False


class TestAddDoc:
    def test_add_doc_success(self):
        dw = DocWorkspace()
        ws = make_ws(dw)
        assert dw.add_doc(ws.workspace_id, "d1") is True
        assert "d1" in ws.doc_ids

    def test_add_doc_unknown_ws(self):
        dw = DocWorkspace()
        assert dw.add_doc("nope", "d1") is False

    def test_add_doc_idempotent(self):
        dw = DocWorkspace()
        ws = make_ws(dw)
        dw.add_doc(ws.workspace_id, "d1")
        dw.add_doc(ws.workspace_id, "d1")
        assert len(ws.doc_ids) == 1


class TestRemoveDoc:
    def test_remove_doc_success(self):
        dw = DocWorkspace()
        ws = make_ws(dw)
        dw.add_doc(ws.workspace_id, "d1")
        assert dw.remove_doc(ws.workspace_id, "d1") is True
        assert "d1" not in ws.doc_ids

    def test_remove_doc_missing(self):
        dw = DocWorkspace()
        ws = make_ws(dw)
        assert dw.remove_doc(ws.workspace_id, "missing") is False

    def test_remove_doc_unknown_ws(self):
        dw = DocWorkspace()
        assert dw.remove_doc("nope", "d1") is False


class TestSetGetSetting:
    def test_set_and_get(self):
        dw = DocWorkspace()
        ws = make_ws(dw)
        assert dw.set_setting(ws.workspace_id, "color", "red") is True
        assert dw.get_setting(ws.workspace_id, "color") == "red"

    def test_get_missing_returns_default(self):
        dw = DocWorkspace()
        ws = make_ws(dw)
        assert dw.get_setting(ws.workspace_id, "missing", default=42) == 42

    def test_set_unknown_ws(self):
        dw = DocWorkspace()
        assert dw.set_setting("nope", "k", "v") is False

    def test_get_unknown_ws_returns_default(self):
        dw = DocWorkspace()
        assert dw.get_setting("nope", "k", default="dflt") == "dflt"

    def test_set_overwrites(self):
        dw = DocWorkspace()
        ws = make_ws(dw)
        dw.set_setting(ws.workspace_id, "k", 1)
        dw.set_setting(ws.workspace_id, "k", 2)
        assert dw.get_setting(ws.workspace_id, "k") == 2


class TestWorkspacesForUser:
    def test_lists_membership(self):
        dw = DocWorkspace()
        a = dw.create("a", "alice")
        b = dw.create("b", "alice")
        c = dw.create("c", "carol")
        dw.add_member(c.workspace_id, "alice")
        result = {ws.workspace_id for ws in dw.workspaces_for_user("alice")}
        assert result == {a.workspace_id, b.workspace_id, c.workspace_id}

    def test_no_membership_empty(self):
        dw = DocWorkspace()
        dw.create("a", "alice")
        assert dw.workspaces_for_user("ghost") == []


class TestWorkspacesForDoc:
    def test_lists_workspaces_with_doc(self):
        dw = DocWorkspace()
        a = dw.create("a", "u")
        b = dw.create("b", "u")
        c = dw.create("c", "u")
        dw.add_doc(a.workspace_id, "d1")
        dw.add_doc(b.workspace_id, "d1")
        dw.add_doc(c.workspace_id, "d2")
        result = {ws.workspace_id for ws in dw.workspaces_for_doc("d1")}
        assert result == {a.workspace_id, b.workspace_id}

    def test_missing_doc_empty(self):
        dw = DocWorkspace()
        dw.create("a", "u")
        assert dw.workspaces_for_doc("nope") == []


class TestMemberOf:
    def test_owner_is_member(self):
        dw = DocWorkspace()
        ws = make_ws(dw, owner="alice")
        m = dw.member_of(ws.workspace_id, "alice")
        assert m is not None
        assert m.role is WorkspaceRole.OWNER

    def test_unknown_user(self):
        dw = DocWorkspace()
        ws = make_ws(dw)
        assert dw.member_of(ws.workspace_id, "ghost") is None

    def test_unknown_ws(self):
        dw = DocWorkspace()
        assert dw.member_of("nope", "u") is None


class TestCanAccess:
    def test_owner_can_access_everything(self):
        dw = DocWorkspace()
        ws = make_ws(dw, owner="alice")
        for r in WorkspaceRole:
            assert dw.can_access(ws.workspace_id, "alice", required_role=r) is True

    def test_viewer_cannot_admin(self):
        dw = DocWorkspace()
        ws = make_ws(dw)
        dw.add_member(ws.workspace_id, "bob", role=WorkspaceRole.VIEWER)
        assert dw.can_access(ws.workspace_id, "bob", WorkspaceRole.ADMIN) is False
        assert dw.can_access(ws.workspace_id, "bob", WorkspaceRole.VIEWER) is True

    def test_guest_only_guest(self):
        dw = DocWorkspace()
        ws = make_ws(dw)
        dw.add_member(ws.workspace_id, "g", role=WorkspaceRole.GUEST)
        assert dw.can_access(ws.workspace_id, "g", WorkspaceRole.GUEST) is True
        assert dw.can_access(ws.workspace_id, "g", WorkspaceRole.VIEWER) is False

    def test_unknown_user_no_access(self):
        dw = DocWorkspace()
        ws = make_ws(dw)
        assert dw.can_access(ws.workspace_id, "ghost") is False

    def test_unknown_ws_no_access(self):
        dw = DocWorkspace()
        assert dw.can_access("nope", "u") is False

    def test_default_required_role_viewer(self):
        dw = DocWorkspace()
        ws = make_ws(dw)
        dw.add_member(ws.workspace_id, "v", role=WorkspaceRole.VIEWER)
        assert dw.can_access(ws.workspace_id, "v") is True


class TestListActive:
    def test_lists_only_unarchived(self):
        dw = DocWorkspace()
        a = dw.create("a", "u")
        b = dw.create("b", "u")
        dw.archive(b.workspace_id)
        ids = {ws.workspace_id for ws in dw.list_active()}
        assert ids == {a.workspace_id}

    def test_empty(self):
        dw = DocWorkspace()
        assert dw.list_active() == []


class TestListArchived:
    def test_lists_only_archived(self):
        dw = DocWorkspace()
        a = dw.create("a", "u")
        b = dw.create("b", "u")
        dw.archive(b.workspace_id)
        ids = {ws.workspace_id for ws in dw.list_archived()}
        assert ids == {b.workspace_id}

    def test_empty(self):
        dw = DocWorkspace()
        assert dw.list_archived() == []


class TestRename:
    def test_rename_success(self):
        dw = DocWorkspace()
        ws = make_ws(dw, name="old")
        assert dw.rename(ws.workspace_id, "new") is True
        assert ws.name == "new"

    def test_rename_unknown(self):
        dw = DocWorkspace()
        assert dw.rename("nope", "x") is False


class TestStats:
    def test_empty_stats(self):
        dw = DocWorkspace()
        s = dw.stats()
        assert s.total == 0
        assert s.archived == 0
        assert s.active == 0
        assert s.total_docs == 0
        assert s.total_members == 0
        assert all(v == 0 for v in s.by_role_distribution.values())
        assert set(s.by_role_distribution.keys()) == {
            "OWNER",
            "ADMIN",
            "EDITOR",
            "VIEWER",
            "GUEST",
        }

    def test_stats_with_data(self):
        dw = DocWorkspace()
        a = dw.create("a", "alice")
        b = dw.create("b", "bob")
        dw.archive(b.workspace_id)
        dw.add_member(a.workspace_id, "x", role=WorkspaceRole.EDITOR)
        dw.add_member(a.workspace_id, "y", role=WorkspaceRole.VIEWER)
        dw.add_doc(a.workspace_id, "d1")
        dw.add_doc(a.workspace_id, "d2")
        dw.add_doc(b.workspace_id, "d3")

        s = dw.stats()
        assert s.total == 2
        assert s.archived == 1
        assert s.active == 1
        assert s.total_docs == 3
        # alice, x, y in a; bob in b → 4 total members
        assert s.total_members == 4
        # 2 owners (alice, bob), 1 editor, 1 viewer
        assert s.by_role_distribution["OWNER"] == 2
        assert s.by_role_distribution["EDITOR"] == 1
        assert s.by_role_distribution["VIEWER"] == 1
        assert s.by_role_distribution["ADMIN"] == 0
        assert s.by_role_distribution["GUEST"] == 0


class TestWorkspaceCount:
    def test_count_zero(self):
        dw = DocWorkspace()
        assert dw.workspace_count == 0

    def test_count_increments(self):
        dw = DocWorkspace()
        dw.create("a", "u")
        dw.create("b", "u")
        assert dw.workspace_count == 2

    def test_count_after_delete(self):
        dw = DocWorkspace()
        a = dw.create("a", "u")
        dw.create("b", "u")
        dw.delete(a.workspace_id)
        assert dw.workspace_count == 1


class TestClear:
    def test_clear_empties(self):
        dw = DocWorkspace()
        dw.create("a", "u")
        dw.create("b", "u")
        dw.clear()
        assert dw.workspace_count == 0
        assert dw.list_active() == []
        assert dw.list_archived() == []

    def test_clear_on_empty(self):
        dw = DocWorkspace()
        dw.clear()
        assert dw.workspace_count == 0


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_threadsafe_create_many(self):
        dw = DocWorkspace()

        def worker():
            for _ in range(20):
                dw.create("w", "u")

        threads = [threading.Thread(target=worker) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert dw.workspace_count == 80

    def test_threadsafe_member_ops(self):
        dw = DocWorkspace()
        ws = dw.create("w", "alice")

        def worker(start: int):
            for i in range(20):
                dw.add_member(ws.workspace_id, f"u{start}_{i}")

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # 80 added + alice owner = 81
        assert len(ws.members) == 81

    def test_setting_value_can_be_any_type(self):
        dw = DocWorkspace()
        ws = make_ws(dw)
        dw.set_setting(ws.workspace_id, "list", [1, 2, 3])
        dw.set_setting(ws.workspace_id, "dict", {"a": 1})
        dw.set_setting(ws.workspace_id, "none", None)
        assert dw.get_setting(ws.workspace_id, "list") == [1, 2, 3]
        assert dw.get_setting(ws.workspace_id, "dict") == {"a": 1}
        assert dw.get_setting(ws.workspace_id, "none", default="X") is None

    def test_member_of_after_remove(self):
        dw = DocWorkspace()
        ws = make_ws(dw)
        dw.add_member(ws.workspace_id, "bob")
        dw.remove_member(ws.workspace_id, "bob")
        assert dw.member_of(ws.workspace_id, "bob") is None

    def test_transfer_ownership_to_owner_member_only(self):
        # New owner must be an existing member - non-member returns False.
        dw = DocWorkspace()
        ws = make_ws(dw, owner="alice")
        assert dw.transfer_ownership(ws.workspace_id, "stranger") is False
        assert ws.owner_id == "alice"

    def test_archive_then_delete(self):
        dw = DocWorkspace()
        ws = make_ws(dw)
        dw.archive(ws.workspace_id)
        assert dw.delete(ws.workspace_id) is True
        assert dw.get(ws.workspace_id) is None

    def test_can_access_owner_above_admin(self):
        dw = DocWorkspace()
        ws = make_ws(dw, owner="alice")
        assert dw.can_access(ws.workspace_id, "alice", WorkspaceRole.ADMIN) is True

    def test_workspaces_for_user_after_remove(self):
        dw = DocWorkspace()
        a = dw.create("a", "u")
        dw.add_member(a.workspace_id, "bob")
        assert len(dw.workspaces_for_user("bob")) == 1
        dw.remove_member(a.workspace_id, "bob")
        assert dw.workspaces_for_user("bob") == []

    def test_doc_ids_are_a_set(self):
        dw = DocWorkspace()
        ws = make_ws(dw)
        dw.add_doc(ws.workspace_id, "d1")
        dw.add_doc(ws.workspace_id, "d1")
        dw.add_doc(ws.workspace_id, "d2")
        assert ws.doc_ids == {"d1", "d2"}
