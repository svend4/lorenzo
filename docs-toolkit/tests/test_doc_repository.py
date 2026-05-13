"""Tests for docstoolkit.doc_repository (E157)."""

from __future__ import annotations

import os
import tempfile
import time

import pytest

from docstoolkit.doc_repository import (
    DocRepository,
    RepoConfig,
    RepoDocument,
    RepoStats,
)


@pytest.fixture
def repo():
    r = DocRepository(RepoConfig(db_path=":memory:", auto_timestamps=False))
    yield r
    r.close()


@pytest.fixture
def repo_auto():
    r = DocRepository(RepoConfig(db_path=":memory:", auto_timestamps=True))
    yield r
    r.close()


class TestRepoDocument:
    def test_create_minimal(self):
        d = RepoDocument(doc_id="a", title="T", content="C")
        assert d.doc_id == "a"
        assert d.title == "T"
        assert d.content == "C"
        assert d.tags == []
        assert d.metadata == {}
        assert d.created_at == 0.0
        assert d.updated_at == 0.0

    def test_create_full(self):
        d = RepoDocument(
            doc_id="a",
            title="T",
            content="C",
            tags=["x", "y"],
            created_at=10.0,
            updated_at=20.0,
            metadata={"k": "v"},
        )
        assert d.tags == ["x", "y"]
        assert d.metadata == {"k": "v"}
        assert d.created_at == 10.0

    def test_independent_defaults(self):
        a = RepoDocument(doc_id="a", title="T", content="C")
        b = RepoDocument(doc_id="b", title="T", content="C")
        a.tags.append("x")
        assert b.tags == []


class TestRepoStats:
    def test_create(self):
        s = RepoStats(
            total_docs=2,
            total_tags=3,
            avg_doc_length=10.5,
            most_used_tags=[("x", 2)],
            oldest_doc_id="a",
            newest_doc_id="b",
        )
        assert s.total_docs == 2
        assert s.total_tags == 3
        assert s.avg_doc_length == 10.5
        assert s.most_used_tags == [("x", 2)]
        assert s.oldest_doc_id == "a"
        assert s.newest_doc_id == "b"


class TestRepoConfig:
    def test_defaults(self):
        c = RepoConfig()
        assert c.db_path == ":memory:"
        assert c.auto_timestamps is True

    def test_custom(self):
        c = RepoConfig(db_path="/tmp/x.db", auto_timestamps=False)
        assert c.db_path == "/tmp/x.db"
        assert c.auto_timestamps is False


class TestCreate:
    def test_create_basic(self, repo):
        d = repo.create("a", "Title", "Content", now=100.0)
        assert d.doc_id == "a"
        assert d.title == "Title"
        assert d.content == "Content"
        assert d.tags == []
        assert d.created_at == 100.0
        assert d.updated_at == 100.0

    def test_create_with_tags(self, repo):
        d = repo.create("a", "T", "C", tags=["x", "y"], now=1.0)
        assert d.tags == ["x", "y"]

    def test_create_with_metadata(self, repo):
        d = repo.create("a", "T", "C", metadata={"author": "me"}, now=1.0)
        assert d.metadata == {"author": "me"}

    def test_create_full(self, repo):
        d = repo.create(
            "a", "T", "C", tags=["x"], metadata={"v": 1}, now=5.0
        )
        assert d.doc_id == "a"
        assert d.tags == ["x"]
        assert d.metadata == {"v": 1}
        assert d.created_at == 5.0

    def test_create_dedups_tags(self, repo):
        d = repo.create("a", "T", "C", tags=["x", "x", "y"], now=1.0)
        assert d.tags == ["x", "y"]

    def test_create_persists(self, repo):
        repo.create("a", "T", "C", now=1.0)
        fetched = repo.get("a")
        assert fetched is not None
        assert fetched.title == "T"

    def test_create_auto_timestamp(self, repo_auto):
        before = time.time()
        d = repo_auto.create("a", "T", "C")
        after = time.time()
        assert before <= d.created_at <= after

    def test_create_uses_explicit_now(self, repo_auto):
        d = repo_auto.create("a", "T", "C", now=42.0)
        assert d.created_at == 42.0


class TestGet:
    def test_get_existing(self, repo):
        repo.create("a", "T", "C", tags=["x"], now=1.0)
        d = repo.get("a")
        assert d is not None
        assert d.doc_id == "a"
        assert d.tags == ["x"]

    def test_get_missing(self, repo):
        assert repo.get("missing") is None

    def test_get_preserves_metadata(self, repo):
        repo.create("a", "T", "C", metadata={"k": [1, 2, 3]}, now=1.0)
        d = repo.get("a")
        assert d.metadata == {"k": [1, 2, 3]}

    def test_get_empty_metadata(self, repo):
        repo.create("a", "T", "C", now=1.0)
        d = repo.get("a")
        assert d.metadata == {}


class TestUpdate:
    def test_update_title(self, repo):
        repo.create("a", "Old", "C", now=1.0)
        d = repo.update("a", title="New", now=2.0)
        assert d.title == "New"
        assert d.content == "C"
        assert d.updated_at == 2.0

    def test_update_content(self, repo):
        repo.create("a", "T", "Old", now=1.0)
        d = repo.update("a", content="New", now=2.0)
        assert d.content == "New"
        assert d.title == "T"

    def test_update_tags_replaces(self, repo):
        repo.create("a", "T", "C", tags=["x", "y"], now=1.0)
        d = repo.update("a", tags=["z"], now=2.0)
        assert d.tags == ["z"]

    def test_update_metadata_replaces(self, repo):
        repo.create("a", "T", "C", metadata={"a": 1}, now=1.0)
        d = repo.update("a", metadata={"b": 2}, now=2.0)
        assert d.metadata == {"b": 2}

    def test_update_partial(self, repo):
        repo.create("a", "T", "C", tags=["x"], metadata={"k": 1}, now=1.0)
        d = repo.update("a", title="NewT", now=2.0)
        assert d.title == "NewT"
        assert d.content == "C"
        assert d.tags == ["x"]
        assert d.metadata == {"k": 1}

    def test_update_missing_returns_none(self, repo):
        assert repo.update("missing", title="X", now=1.0) is None

    def test_update_preserves_created_at(self, repo):
        repo.create("a", "T", "C", now=1.0)
        d = repo.update("a", title="X", now=5.0)
        assert d.created_at == 1.0
        assert d.updated_at == 5.0

    def test_update_empty_tags(self, repo):
        repo.create("a", "T", "C", tags=["x"], now=1.0)
        d = repo.update("a", tags=[], now=2.0)
        assert d.tags == []


class TestDelete:
    def test_delete_existing(self, repo):
        repo.create("a", "T", "C", now=1.0)
        assert repo.delete("a") is True
        assert repo.get("a") is None

    def test_delete_missing(self, repo):
        assert repo.delete("missing") is False

    def test_delete_removes_tags(self, repo):
        repo.create("a", "T", "C", tags=["only-on-a"], now=1.0)
        repo.delete("a")
        assert "only-on-a" not in repo.all_tags()


class TestExists:
    def test_exists_true(self, repo):
        repo.create("a", "T", "C", now=1.0)
        assert repo.exists("a") is True

    def test_exists_false(self, repo):
        assert repo.exists("missing") is False

    def test_exists_after_delete(self, repo):
        repo.create("a", "T", "C", now=1.0)
        repo.delete("a")
        assert repo.exists("a") is False


class TestListAll:
    def test_list_empty(self, repo):
        assert repo.list_all() == []

    def test_list_all_orders_by_created(self, repo):
        repo.create("b", "T", "C", now=2.0)
        repo.create("a", "T", "C", now=1.0)
        repo.create("c", "T", "C", now=3.0)
        ids = [d.doc_id for d in repo.list_all()]
        assert ids == ["a", "b", "c"]

    def test_list_with_limit(self, repo):
        for i in range(5):
            repo.create(f"d{i}", "T", "C", now=float(i))
        result = repo.list_all(limit=2)
        assert len(result) == 2
        assert [d.doc_id for d in result] == ["d0", "d1"]

    def test_list_with_offset(self, repo):
        for i in range(5):
            repo.create(f"d{i}", "T", "C", now=float(i))
        result = repo.list_all(offset=2)
        assert [d.doc_id for d in result] == ["d2", "d3", "d4"]

    def test_list_limit_offset(self, repo):
        for i in range(5):
            repo.create(f"d{i}", "T", "C", now=float(i))
        result = repo.list_all(limit=2, offset=1)
        assert [d.doc_id for d in result] == ["d1", "d2"]


class TestFindByTag:
    def test_find_by_tag(self, repo):
        repo.create("a", "T", "C", tags=["x"], now=1.0)
        repo.create("b", "T", "C", tags=["y"], now=2.0)
        repo.create("c", "T", "C", tags=["x", "y"], now=3.0)
        result = repo.find_by_tag("x")
        ids = sorted(d.doc_id for d in result)
        assert ids == ["a", "c"]

    def test_find_by_tag_empty(self, repo):
        assert repo.find_by_tag("missing") == []

    def test_find_by_tag_returns_full_docs(self, repo):
        repo.create("a", "Title", "Content", tags=["x"], now=1.0)
        result = repo.find_by_tag("x")
        assert len(result) == 1
        assert result[0].title == "Title"
        assert result[0].tags == ["x"]


class TestFindByTagsAny:
    def test_or_match(self, repo):
        repo.create("a", "T", "C", tags=["x"], now=1.0)
        repo.create("b", "T", "C", tags=["y"], now=2.0)
        repo.create("c", "T", "C", tags=["z"], now=3.0)
        result = repo.find_by_tags(["x", "y"], match_all=False)
        ids = sorted(d.doc_id for d in result)
        assert ids == ["a", "b"]

    def test_or_match_dedup(self, repo):
        repo.create("a", "T", "C", tags=["x", "y"], now=1.0)
        result = repo.find_by_tags(["x", "y"], match_all=False)
        assert len(result) == 1
        assert result[0].doc_id == "a"

    def test_or_match_empty_tags(self, repo):
        repo.create("a", "T", "C", tags=["x"], now=1.0)
        assert repo.find_by_tags([], match_all=False) == []


class TestFindByTagsAll:
    def test_and_match(self, repo):
        repo.create("a", "T", "C", tags=["x", "y"], now=1.0)
        repo.create("b", "T", "C", tags=["x"], now=2.0)
        repo.create("c", "T", "C", tags=["x", "y", "z"], now=3.0)
        result = repo.find_by_tags(["x", "y"], match_all=True)
        ids = sorted(d.doc_id for d in result)
        assert ids == ["a", "c"]

    def test_and_match_strict(self, repo):
        repo.create("a", "T", "C", tags=["x"], now=1.0)
        repo.create("b", "T", "C", tags=["y"], now=2.0)
        result = repo.find_by_tags(["x", "y"], match_all=True)
        assert result == []

    def test_and_match_empty(self, repo):
        assert repo.find_by_tags([], match_all=True) == []


class TestFindByTitle:
    def test_substring(self, repo):
        repo.create("a", "Hello World", "C", now=1.0)
        repo.create("b", "Goodbye", "C", now=2.0)
        result = repo.find_by_title("Hello")
        assert len(result) == 1
        assert result[0].doc_id == "a"

    def test_case_insensitive(self, repo):
        repo.create("a", "Hello World", "C", now=1.0)
        result = repo.find_by_title("hello")
        assert len(result) == 1

    def test_no_match(self, repo):
        repo.create("a", "Hi", "C", now=1.0)
        assert repo.find_by_title("missing") == []

    def test_multi_match(self, repo):
        repo.create("a", "Cat report", "C", now=1.0)
        repo.create("b", "Dog Report", "C", now=2.0)
        result = repo.find_by_title("report")
        assert len(result) == 2


class TestFindByContent:
    def test_substring(self, repo):
        repo.create("a", "T", "hello world content", now=1.0)
        repo.create("b", "T", "goodbye content", now=2.0)
        result = repo.find_by_content("hello")
        assert len(result) == 1
        assert result[0].doc_id == "a"

    def test_case_insensitive(self, repo):
        repo.create("a", "T", "Hello World", now=1.0)
        result = repo.find_by_content("HELLO")
        assert len(result) == 1

    def test_no_match(self, repo):
        repo.create("a", "T", "C", now=1.0)
        assert repo.find_by_content("missing") == []


class TestAddRemoveTag:
    def test_add_tag(self, repo):
        repo.create("a", "T", "C", now=1.0)
        assert repo.add_tag("a", "new") is True
        d = repo.get("a")
        assert "new" in d.tags

    def test_add_tag_duplicate(self, repo):
        repo.create("a", "T", "C", tags=["x"], now=1.0)
        assert repo.add_tag("a", "x") is False

    def test_add_tag_missing_doc(self, repo):
        assert repo.add_tag("missing", "tag") is False

    def test_remove_tag(self, repo):
        repo.create("a", "T", "C", tags=["x", "y"], now=1.0)
        assert repo.remove_tag("a", "x") is True
        d = repo.get("a")
        assert d.tags == ["y"]

    def test_remove_tag_missing(self, repo):
        repo.create("a", "T", "C", now=1.0)
        assert repo.remove_tag("a", "missing") is False

    def test_remove_tag_missing_doc(self, repo):
        assert repo.remove_tag("missing", "x") is False


class TestAllTags:
    def test_empty(self, repo):
        assert repo.all_tags() == []

    def test_lists_all_distinct(self, repo):
        repo.create("a", "T", "C", tags=["x", "y"], now=1.0)
        repo.create("b", "T", "C", tags=["y", "z"], now=2.0)
        assert repo.all_tags() == ["x", "y", "z"]

    def test_sorted(self, repo):
        repo.create("a", "T", "C", tags=["zeta", "alpha", "mid"], now=1.0)
        assert repo.all_tags() == ["alpha", "mid", "zeta"]


class TestCount:
    def test_count_empty(self, repo):
        assert repo.count == 0

    def test_count_after_create(self, repo):
        repo.create("a", "T", "C", now=1.0)
        repo.create("b", "T", "C", now=2.0)
        assert repo.count == 2

    def test_count_after_delete(self, repo):
        repo.create("a", "T", "C", now=1.0)
        repo.delete("a")
        assert repo.count == 0


class TestStats:
    def test_empty_stats(self, repo):
        s = repo.stats()
        assert s.total_docs == 0
        assert s.total_tags == 0
        assert s.avg_doc_length == 0.0
        assert s.most_used_tags == []
        assert s.oldest_doc_id is None
        assert s.newest_doc_id is None

    def test_total_docs(self, repo):
        repo.create("a", "T", "Hello", now=1.0)
        repo.create("b", "T", "World!", now=2.0)
        s = repo.stats()
        assert s.total_docs == 2

    def test_total_tags(self, repo):
        repo.create("a", "T", "C", tags=["x", "y"], now=1.0)
        repo.create("b", "T", "C", tags=["y", "z"], now=2.0)
        s = repo.stats()
        assert s.total_tags == 3

    def test_avg_doc_length(self, repo):
        repo.create("a", "T", "abc", now=1.0)  # len 3
        repo.create("b", "T", "abcdefg", now=2.0)  # len 7
        s = repo.stats()
        assert s.avg_doc_length == 5.0

    def test_most_used_tags(self, repo):
        repo.create("a", "T", "C", tags=["x", "y"], now=1.0)
        repo.create("b", "T", "C", tags=["x"], now=2.0)
        repo.create("c", "T", "C", tags=["x", "z"], now=3.0)
        s = repo.stats()
        assert s.most_used_tags[0] == ("x", 3)

    def test_oldest_newest(self, repo):
        repo.create("a", "T", "C", now=10.0)
        repo.create("b", "T", "C", now=5.0)
        repo.create("c", "T", "C", now=20.0)
        s = repo.stats()
        assert s.oldest_doc_id == "b"
        assert s.newest_doc_id == "c"

    def test_most_used_top_10(self, repo):
        for i in range(15):
            repo.create(f"d{i}", "T", "C", tags=[f"t{i}"], now=float(i))
        s = repo.stats()
        assert len(s.most_used_tags) <= 10


class TestPersistence:
    def test_file_db_persists(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "test.db")
            r1 = DocRepository(RepoConfig(db_path=path, auto_timestamps=False))
            r1.create("a", "Title", "Content", tags=["x"], now=1.0)
            r1.close()

            r2 = DocRepository(RepoConfig(db_path=path, auto_timestamps=False))
            d = r2.get("a")
            assert d is not None
            assert d.title == "Title"
            assert d.tags == ["x"]
            r2.close()

    def test_file_db_persists_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "test.db")
            r1 = DocRepository(RepoConfig(db_path=path, auto_timestamps=False))
            r1.create("a", "T", "C", metadata={"k": "v"}, now=1.0)
            r1.close()

            r2 = DocRepository(RepoConfig(db_path=path, auto_timestamps=False))
            d = r2.get("a")
            assert d.metadata == {"k": "v"}
            r2.close()


class TestEdgeCases:
    def test_duplicate_create_raises(self, repo):
        repo.create("a", "T", "C", now=1.0)
        with pytest.raises(Exception):
            repo.create("a", "T2", "C2", now=2.0)

    def test_get_missing(self, repo):
        assert repo.get("nope") is None

    def test_delete_missing(self, repo):
        assert repo.delete("nope") is False

    def test_update_missing(self, repo):
        assert repo.update("nope", title="x", now=1.0) is None

    def test_empty_repo_list(self, repo):
        assert repo.list_all() == []

    def test_empty_repo_find_by_tag(self, repo):
        assert repo.find_by_tag("any") == []

    def test_empty_repo_stats(self, repo):
        s = repo.stats()
        assert s.total_docs == 0

    def test_close_idempotent_via_new_repo(self, repo):
        repo.create("a", "T", "C", now=1.0)
        # close inside fixture, just ensure no error
        assert repo.count == 1

    def test_unicode_content(self, repo):
        repo.create("a", "Привет", "Мир", tags=["рус"], now=1.0)
        d = repo.get("a")
        assert d.title == "Привет"
        assert d.content == "Мир"
        assert d.tags == ["рус"]

    def test_complex_metadata(self, repo):
        meta = {"list": [1, 2, 3], "nested": {"k": "v"}, "n": 1.5}
        repo.create("a", "T", "C", metadata=meta, now=1.0)
        d = repo.get("a")
        assert d.metadata == meta
