"""Tests for docstoolkit.doc_versioning_v2."""
from __future__ import annotations

import os
import tempfile

import pytest

from docstoolkit.doc_versioning_v2 import (
    Branch,
    DocVersion,
    Tag,
    VersionStore,
)


# ---------------------------------------------------------------- dataclasses
class TestDocVersion:
    def test_create_minimal(self):
        v = DocVersion(version_id=1, doc_id="d", content="c", created_at=0.0)
        assert v.version_id == 1
        assert v.doc_id == "d"
        assert v.content == "c"
        assert v.created_at == 0.0
        assert v.author is None
        assert v.message is None
        assert v.parent_id is None

    def test_create_full(self):
        v = DocVersion(
            version_id=2,
            doc_id="doc",
            content="hello",
            created_at=10.5,
            author="alice",
            message="initial",
            parent_id=1,
        )
        assert v.author == "alice"
        assert v.message == "initial"
        assert v.parent_id == 1

    def test_equality(self):
        a = DocVersion(1, "d", "c", 0.0)
        b = DocVersion(1, "d", "c", 0.0)
        assert a == b

    def test_inequality(self):
        a = DocVersion(1, "d", "c", 0.0)
        b = DocVersion(2, "d", "c", 0.0)
        assert a != b


class TestBranch:
    def test_create(self):
        b = Branch(name="main", head_version=1, created_at=0.0)
        assert b.name == "main"
        assert b.head_version == 1
        assert b.created_at == 0.0

    def test_equality(self):
        a = Branch("dev", 1, 0.0)
        b = Branch("dev", 1, 0.0)
        assert a == b


class TestTag:
    def test_create(self):
        t = Tag(name="v1.0", version_id=3, created_at=1.0)
        assert t.name == "v1.0"
        assert t.version_id == 3
        assert t.created_at == 1.0

    def test_equality(self):
        a = Tag("v1.0", 3, 1.0)
        b = Tag("v1.0", 3, 1.0)
        assert a == b


# ---------------------------------------------------------------- commit
class TestCommit:
    def test_basic_commit_returns_docversion(self):
        store = VersionStore()
        v = store.commit("doc1", "hello", message="init", now=1.0)
        assert isinstance(v, DocVersion)
        assert v.doc_id == "doc1"
        assert v.content == "hello"
        assert v.message == "init"
        assert v.created_at == 1.0
        store.close()

    def test_commit_assigns_increasing_ids(self):
        store = VersionStore()
        a = store.commit("d", "1", now=1.0)
        b = store.commit("d", "2", now=2.0)
        c = store.commit("d", "3", now=3.0)
        assert a.version_id < b.version_id < c.version_id
        store.close()

    def test_commit_auto_links_parent(self):
        store = VersionStore()
        a = store.commit("d", "1", now=1.0)
        b = store.commit("d", "2", now=2.0)
        assert b.parent_id == a.version_id
        store.close()

    def test_first_commit_has_no_parent(self):
        store = VersionStore()
        a = store.commit("d", "1", now=1.0)
        assert a.parent_id is None
        store.close()

    def test_commit_with_explicit_parent(self):
        store = VersionStore()
        a = store.commit("d", "1", now=1.0)
        store.commit("d", "2", now=2.0)
        c = store.commit("d", "3", parent_id=a.version_id, now=3.0)
        assert c.parent_id == a.version_id
        store.close()

    def test_commit_with_author(self):
        store = VersionStore()
        v = store.commit("d", "x", author="bob", now=1.0)
        assert v.author == "bob"
        store.close()

    def test_commit_creates_main_branch(self):
        store = VersionStore()
        store.commit("d", "x", now=1.0)
        branches = store.list_branches()
        assert any(b.name == "main" for b in branches)
        store.close()

    def test_commit_updates_main_head(self):
        store = VersionStore()
        a = store.commit("d", "1", now=1.0)
        b = store.commit("d", "2", now=2.0)
        branches = {br.name: br for br in store.list_branches()}
        assert branches["main"].head_version == b.version_id
        assert branches["main"].head_version != a.version_id
        store.close()

    def test_different_docs_have_separate_parents(self):
        store = VersionStore()
        store.commit("doc_a", "x", now=1.0)
        b = store.commit("doc_b", "y", now=2.0)
        # b is first commit on doc_b, parent should be None
        assert b.parent_id is None
        store.close()


# ---------------------------------------------------------------- get
class TestGet:
    def test_get_existing(self):
        store = VersionStore()
        v = store.commit("d", "x", now=1.0)
        fetched = store.get(v.version_id)
        assert fetched is not None
        assert fetched.version_id == v.version_id
        assert fetched.content == "x"
        store.close()

    def test_get_missing_returns_none(self):
        store = VersionStore()
        assert store.get(9999) is None
        store.close()

    def test_get_preserves_fields(self):
        store = VersionStore()
        v = store.commit(
            "d", "data", author="a", message="m", now=5.0
        )
        fetched = store.get(v.version_id)
        assert fetched.author == "a"
        assert fetched.message == "m"
        assert fetched.created_at == 5.0
        store.close()


# ---------------------------------------------------------------- get_current
class TestGetCurrent:
    def test_returns_latest(self):
        store = VersionStore()
        store.commit("d", "1", now=1.0)
        b = store.commit("d", "2", now=2.0)
        current = store.get_current("d")
        assert current.version_id == b.version_id
        assert current.content == "2"
        store.close()

    def test_none_when_no_commits(self):
        store = VersionStore()
        assert store.get_current("nope") is None
        store.close()

    def test_isolates_doc_ids(self):
        store = VersionStore()
        store.commit("a", "alpha", now=1.0)
        b = store.commit("b", "beta", now=2.0)
        assert store.get_current("b").version_id == b.version_id
        store.close()


# ---------------------------------------------------------------- history
class TestHistory:
    def test_history_newest_first(self):
        store = VersionStore()
        a = store.commit("d", "1", now=1.0)
        b = store.commit("d", "2", now=2.0)
        c = store.commit("d", "3", now=3.0)
        hist = store.history("d")
        assert [v.version_id for v in hist] == [
            c.version_id,
            b.version_id,
            a.version_id,
        ]
        store.close()

    def test_history_empty_for_unknown_doc(self):
        store = VersionStore()
        assert store.history("ghost") == []
        store.close()

    def test_history_returns_only_branch_versions(self):
        store = VersionStore()
        a = store.commit("d", "main1", now=1.0)
        store.create_branch("dev", from_version=a.version_id, now=2.0)
        store.commit("d", "dev1", branch="dev", now=3.0)
        main_hist = store.history("d", branch="main")
        assert [v.content for v in main_hist] == ["main1"]
        dev_hist = store.history("d", branch="dev")
        assert [v.content for v in dev_hist] == ["dev1"]
        store.close()


# ---------------------------------------------------------------- rollback
class TestRollback:
    def test_rollback_creates_new_commit(self):
        store = VersionStore()
        a = store.commit("d", "v1", now=1.0)
        store.commit("d", "v2", now=2.0)
        r = store.rollback("d", a.version_id, now=3.0)
        assert r.version_id != a.version_id
        assert r.content == "v1"
        store.close()

    def test_rollback_advances_head(self):
        store = VersionStore()
        a = store.commit("d", "v1", now=1.0)
        store.commit("d", "v2", now=2.0)
        r = store.rollback("d", a.version_id, now=3.0)
        cur = store.get_current("d")
        assert cur.version_id == r.version_id
        assert cur.content == "v1"
        store.close()

    def test_rollback_increments_version_count(self):
        store = VersionStore()
        a = store.commit("d", "v1", now=1.0)
        store.commit("d", "v2", now=2.0)
        before = store.version_count("d")
        store.rollback("d", a.version_id, now=3.0)
        assert store.version_count("d") == before + 1
        store.close()

    def test_rollback_unknown_version(self):
        store = VersionStore()
        with pytest.raises(KeyError):
            store.rollback("d", 9999, now=1.0)
        store.close()

    def test_rollback_wrong_doc_id(self):
        store = VersionStore()
        a = store.commit("doc_a", "x", now=1.0)
        with pytest.raises(ValueError):
            store.rollback("doc_b", a.version_id, now=2.0)
        store.close()

    def test_rollback_message_mentions_version(self):
        store = VersionStore()
        a = store.commit("d", "x", now=1.0)
        store.commit("d", "y", now=2.0)
        r = store.rollback("d", a.version_id, now=3.0)
        assert str(a.version_id) in (r.message or "")
        store.close()


# ---------------------------------------------------------------- diff
class TestDiff:
    def test_diff_format(self):
        store = VersionStore()
        a = store.commit("d", "alpha\nbeta\n", now=1.0)
        b = store.commit("d", "alpha\ngamma\n", now=2.0)
        out = store.diff(a.version_id, b.version_id)
        assert "---" in out
        assert "+++" in out
        assert "-beta" in out
        assert "+gamma" in out
        store.close()

    def test_diff_identical_versions_empty(self):
        store = VersionStore()
        a = store.commit("d", "same", now=1.0)
        b = store.commit("d", "same", now=2.0)
        out = store.diff(a.version_id, b.version_id)
        assert out == ""
        store.close()

    def test_diff_unknown_a(self):
        store = VersionStore()
        b = store.commit("d", "x", now=1.0)
        with pytest.raises(KeyError):
            store.diff(9999, b.version_id)
        store.close()

    def test_diff_unknown_b(self):
        store = VersionStore()
        a = store.commit("d", "x", now=1.0)
        with pytest.raises(KeyError):
            store.diff(a.version_id, 9999)
        store.close()

    def test_diff_mentions_version_ids(self):
        store = VersionStore()
        a = store.commit("d", "x\n", now=1.0)
        b = store.commit("d", "y\n", now=2.0)
        out = store.diff(a.version_id, b.version_id)
        assert f"version_{a.version_id}" in out
        assert f"version_{b.version_id}" in out
        store.close()


# ---------------------------------------------------------------- create_branch
class TestCreateBranch:
    def test_create_branch_returns_branch(self):
        store = VersionStore()
        a = store.commit("d", "x", now=1.0)
        br = store.create_branch("dev", from_version=a.version_id, now=2.0)
        assert isinstance(br, Branch)
        assert br.name == "dev"
        assert br.head_version == a.version_id
        assert br.created_at == 2.0
        store.close()

    def test_create_branch_appears_in_list(self):
        store = VersionStore()
        a = store.commit("d", "x", now=1.0)
        store.create_branch("dev", from_version=a.version_id, now=2.0)
        names = {b.name for b in store.list_branches()}
        assert "dev" in names
        store.close()

    def test_create_duplicate_branch(self):
        store = VersionStore()
        a = store.commit("d", "x", now=1.0)
        store.create_branch("dev", from_version=a.version_id, now=2.0)
        with pytest.raises(ValueError):
            store.create_branch("dev", from_version=a.version_id, now=3.0)
        store.close()

    def test_create_branch_unknown_version(self):
        store = VersionStore()
        with pytest.raises(KeyError):
            store.create_branch("dev", from_version=999, now=1.0)
        store.close()

    def test_create_branch_empty_name(self):
        store = VersionStore()
        a = store.commit("d", "x", now=1.0)
        with pytest.raises(ValueError):
            store.create_branch("", from_version=a.version_id, now=2.0)
        store.close()


# ---------------------------------------------------------------- list_branches
class TestListBranches:
    def test_empty_initially(self):
        store = VersionStore()
        assert store.list_branches() == []
        store.close()

    def test_main_after_first_commit(self):
        store = VersionStore()
        store.commit("d", "x", now=1.0)
        branches = store.list_branches()
        assert len(branches) == 1
        assert branches[0].name == "main"
        store.close()

    def test_multiple_branches(self):
        store = VersionStore()
        a = store.commit("d", "x", now=1.0)
        store.create_branch("dev", from_version=a.version_id, now=2.0)
        store.create_branch("feature", from_version=a.version_id, now=3.0)
        names = {b.name for b in store.list_branches()}
        assert names == {"main", "dev", "feature"}
        store.close()


# ---------------------------------------------------------------- delete_branch
class TestDeleteBranch:
    def test_delete_existing(self):
        store = VersionStore()
        a = store.commit("d", "x", now=1.0)
        store.create_branch("dev", from_version=a.version_id, now=2.0)
        assert store.delete_branch("dev") is True
        names = {b.name for b in store.list_branches()}
        assert "dev" not in names
        store.close()

    def test_delete_missing_returns_false(self):
        store = VersionStore()
        store.commit("d", "x", now=1.0)
        assert store.delete_branch("nope") is False
        store.close()

    def test_cannot_delete_main(self):
        store = VersionStore()
        store.commit("d", "x", now=1.0)
        with pytest.raises(ValueError):
            store.delete_branch("main")
        store.close()


# ---------------------------------------------------------------- tags
class TestTagOps:
    def test_tag_returns_tag(self):
        store = VersionStore()
        a = store.commit("d", "x", now=1.0)
        t = store.tag("v1.0", a.version_id, now=2.0)
        assert isinstance(t, Tag)
        assert t.name == "v1.0"
        assert t.version_id == a.version_id
        store.close()

    def test_tag_appears_in_list(self):
        store = VersionStore()
        a = store.commit("d", "x", now=1.0)
        store.tag("v1.0", a.version_id, now=2.0)
        names = {t.name for t in store.list_tags()}
        assert "v1.0" in names
        store.close()

    def test_duplicate_tag_rejected(self):
        store = VersionStore()
        a = store.commit("d", "x", now=1.0)
        store.tag("v1.0", a.version_id, now=2.0)
        with pytest.raises(ValueError):
            store.tag("v1.0", a.version_id, now=3.0)
        store.close()

    def test_tag_unknown_version(self):
        store = VersionStore()
        with pytest.raises(KeyError):
            store.tag("v1.0", 9999, now=1.0)
        store.close()

    def test_tag_empty_name(self):
        store = VersionStore()
        a = store.commit("d", "x", now=1.0)
        with pytest.raises(ValueError):
            store.tag("", a.version_id, now=2.0)
        store.close()

    def test_list_tags_empty_initially(self):
        store = VersionStore()
        assert store.list_tags() == []
        store.close()

    def test_multiple_tags(self):
        store = VersionStore()
        a = store.commit("d", "x", now=1.0)
        b = store.commit("d", "y", now=2.0)
        store.tag("v1.0", a.version_id, now=3.0)
        store.tag("v1.1", b.version_id, now=4.0)
        names = {t.name for t in store.list_tags()}
        assert names == {"v1.0", "v1.1"}
        store.close()


# ---------------------------------------------------------------- get_by_tag
class TestGetByTag:
    def test_get_by_tag_returns_version(self):
        store = VersionStore()
        a = store.commit("d", "x", now=1.0)
        store.tag("v1", a.version_id, now=2.0)
        v = store.get_by_tag("v1")
        assert v is not None
        assert v.version_id == a.version_id
        assert v.content == "x"
        store.close()

    def test_get_by_tag_missing(self):
        store = VersionStore()
        assert store.get_by_tag("ghost") is None
        store.close()


# ---------------------------------------------------------------- version_count
class TestVersionCount:
    def test_zero_initially(self):
        store = VersionStore()
        assert store.version_count("d") == 0
        store.close()

    def test_increments(self):
        store = VersionStore()
        store.commit("d", "1", now=1.0)
        assert store.version_count("d") == 1
        store.commit("d", "2", now=2.0)
        assert store.version_count("d") == 2
        store.close()

    def test_count_per_doc(self):
        store = VersionStore()
        store.commit("a", "x", now=1.0)
        store.commit("b", "x", now=2.0)
        store.commit("b", "y", now=3.0)
        assert store.version_count("a") == 1
        assert store.version_count("b") == 2
        store.close()


# ---------------------------------------------------------------- persistence
class TestPersistence:
    def test_file_db_reopen(self, tmp_path):
        db = tmp_path / "v.db"
        s1 = VersionStore(str(db))
        v = s1.commit("d", "hello", now=1.0)
        s1.tag("v1.0", v.version_id, now=2.0)
        s1.close()

        s2 = VersionStore(str(db))
        cur = s2.get_current("d")
        assert cur is not None
        assert cur.content == "hello"
        tagged = s2.get_by_tag("v1.0")
        assert tagged is not None
        assert tagged.content == "hello"
        s2.close()

    def test_file_db_branches_persist(self, tmp_path):
        db = tmp_path / "v.db"
        s1 = VersionStore(str(db))
        v = s1.commit("d", "x", now=1.0)
        s1.create_branch("dev", from_version=v.version_id, now=2.0)
        s1.close()

        s2 = VersionStore(str(db))
        names = {b.name for b in s2.list_branches()}
        assert "main" in names and "dev" in names
        s2.close()

    def test_in_memory_isolated(self):
        s1 = VersionStore(":memory:")
        s2 = VersionStore(":memory:")
        s1.commit("d", "in s1", now=1.0)
        assert s2.get_current("d") is None
        s1.close()
        s2.close()


# ---------------------------------------------------------------- edge cases
class TestEdgeCases:
    def test_close_is_idempotent(self):
        store = VersionStore()
        store.close()
        store.close()  # should not raise

    def test_use_after_close_raises(self):
        store = VersionStore()
        store.close()
        with pytest.raises(RuntimeError):
            store.commit("d", "x", now=1.0)

    def test_context_manager(self):
        with VersionStore() as store:
            v = store.commit("d", "x", now=1.0)
            assert v.version_id > 0

    def test_history_no_commits_returns_empty(self):
        store = VersionStore()
        assert store.history("nobody") == []
        store.close()

    def test_get_current_after_delete_branch(self):
        store = VersionStore()
        a = store.commit("d", "x", now=1.0)
        store.create_branch("dev", from_version=a.version_id, now=2.0)
        store.commit("d", "dev1", branch="dev", now=3.0)
        store.delete_branch("dev")
        # versions remain, but branch pointer is gone
        assert store.get_current("d", branch="dev") is not None
        # main is unaffected
        assert store.get_current("d", branch="main").content == "x"
        store.close()

    def test_missing_tag_returns_none(self):
        store = VersionStore()
        store.commit("d", "x", now=1.0)
        assert store.get_by_tag("nope") is None
        store.close()

    def test_diff_with_self(self):
        store = VersionStore()
        a = store.commit("d", "hello\nworld\n", now=1.0)
        assert store.diff(a.version_id, a.version_id) == ""
        store.close()

    def test_commit_on_new_branch_creates_it(self):
        store = VersionStore()
        a = store.commit("d", "main", now=1.0)
        store.create_branch("feature", from_version=a.version_id, now=2.0)
        v = store.commit("d", "feat", branch="feature", now=3.0)
        cur = store.get_current("d", branch="feature")
        assert cur.version_id == v.version_id
        # main head unchanged
        main_cur = store.get_current("d", branch="main")
        assert main_cur.version_id == a.version_id
        store.close()

    def test_large_history(self):
        store = VersionStore()
        for i in range(50):
            store.commit("d", f"v{i}", now=float(i))
        assert store.version_count("d") == 50
        hist = store.history("d")
        assert len(hist) == 50
        assert hist[0].content == "v49"
        assert hist[-1].content == "v0"
        store.close()

    def test_empty_content_allowed(self):
        store = VersionStore()
        v = store.commit("d", "", now=1.0)
        assert store.get(v.version_id).content == ""
        store.close()
