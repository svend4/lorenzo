"""Tests for IndexCoordinator (M7).

Uses only stdlib — no pytest fixtures that require extra deps.
A simple DictIndex stub is used to simulate real indexes.
"""
from __future__ import annotations

import os
import tempfile
import threading
import time
from pathlib import Path

import pytest

from docstoolkit.embeddings.coordinator import (
    Index,
    IndexCoordinator,
    IndexHit,
    _md5,
    _normalize_doc_id,
)


# ---------------------------------------------------------------------------
# Helpers / stubs
# ---------------------------------------------------------------------------


class DictIndex:
    """Minimal in-memory index backed by a dict. Supports optional list_all()."""

    def __init__(self):
        self.docs: dict[str, str] = {}
        self.add_calls: list[tuple[str, str]] = []
        self.update_calls: list[tuple[str, str]] = []
        self.remove_calls: list[str] = []

    def add(self, doc_id: str, content: str) -> None:
        self.docs[doc_id] = content
        self.add_calls.append((doc_id, content))

    def remove(self, doc_id: str) -> None:
        self.docs.pop(doc_id, None)
        self.remove_calls.append(doc_id)

    def update(self, doc_id: str, content: str) -> None:
        self.docs[doc_id] = content
        self.update_calls.append((doc_id, content))

    def query(self, q: str, top_k: int = 10) -> list[dict]:
        results = []
        for doc_id, content in self.docs.items():
            if q.lower() in content.lower():
                results.append({"doc_id": doc_id, "score": 1.0})
        return results[:top_k]

    def list_all(self) -> list[str]:
        return list(self.docs.keys())


class NoListAllIndex(DictIndex):
    """DictIndex without list_all — to test verify() fallback."""

    def __getattribute__(self, name):
        if name == "list_all":
            raise AttributeError("no list_all")
        return super().__getattribute__(name)


class BrokenQueryIndex(DictIndex):
    """Index whose query() always raises — to test error resilience."""

    def query(self, q: str, top_k: int = 10) -> list[dict]:
        raise RuntimeError("simulated query failure")


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def tmp_file(tmp_path):
    """Return a Path to a temp file with initial content."""
    f = tmp_path / "doc.md"
    f.write_text("Hello world", encoding="utf-8")
    return f


@pytest.fixture()
def coordinator():
    """Fresh in-memory coordinator."""
    return IndexCoordinator()


@pytest.fixture()
def coordinator_with_index(coordinator):
    idx = DictIndex()
    coordinator.register("main", idx)
    return coordinator, idx


# ---------------------------------------------------------------------------
# IndexHit dataclass tests (3 tests)
# ---------------------------------------------------------------------------


def test_indexhit_basic_fields():
    hit = IndexHit(doc_id="a/b.md", score=0.9)
    assert hit.doc_id == "a/b.md"
    assert hit.score == 0.9


def test_indexhit_default_index_name():
    hit = IndexHit(doc_id="x", score=0.5)
    assert hit.index_name == ""


def test_indexhit_custom_index_name():
    hit = IndexHit(doc_id="x", score=0.5, index_name="bm25")
    assert hit.index_name == "bm25"


# ---------------------------------------------------------------------------
# Index Protocol tests (2 tests)
# ---------------------------------------------------------------------------


def test_dict_index_satisfies_protocol():
    idx = DictIndex()
    assert isinstance(idx, Index)


def test_plain_object_does_not_satisfy_protocol():
    class Bad:
        pass
    assert not isinstance(Bad(), Index)


# ---------------------------------------------------------------------------
# IndexCoordinator init tests (3 tests)
# ---------------------------------------------------------------------------


def test_coordinator_init_memory(coordinator):
    s = coordinator.stats()
    assert s["docs_tracked"] == 0
    assert s["indexes"] == []
    assert s["db_path"] == ":memory:"


def test_coordinator_init_file_db(tmp_path):
    db = str(tmp_path / "manifest.sqlite")
    coord = IndexCoordinator(db_path=db)
    assert coord.stats()["db_path"] == db
    assert os.path.exists(db)
    coord.close()


def test_coordinator_init_creates_schema(coordinator):
    # Should not raise — schema was created during __init__
    row = coordinator._conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='doc_manifest'"
    ).fetchone()
    assert row is not None


# ---------------------------------------------------------------------------
# register() tests (2 tests)
# ---------------------------------------------------------------------------


def test_register_stores_index(coordinator):
    idx = DictIndex()
    coordinator.register("alpha", idx)
    assert "alpha" in coordinator.stats()["indexes"]


def test_register_multiple_indexes(coordinator):
    coordinator.register("a", DictIndex())
    coordinator.register("b", DictIndex())
    names = coordinator.stats()["indexes"]
    assert set(names) == {"a", "b"}


# ---------------------------------------------------------------------------
# on_doc_change() tests (8 tests)
# ---------------------------------------------------------------------------


def test_on_doc_change_calls_add(coordinator_with_index, tmp_file):
    coord, idx = coordinator_with_index
    updated = coord.on_doc_change(tmp_file)
    assert "main" in updated
    assert len(idx.add_calls) == 1
    doc_id, content = idx.add_calls[0]
    assert content == "Hello world"


def test_on_doc_change_updates_manifest(coordinator_with_index, tmp_file):
    coord, idx = coordinator_with_index
    coord.on_doc_change(tmp_file)
    s = coord.stats()
    assert s["docs_tracked"] == 1


def test_on_doc_change_same_content_no_reindex(coordinator_with_index, tmp_file):
    coord, idx = coordinator_with_index
    coord.on_doc_change(tmp_file)
    # Second call — same content
    updated = coord.on_doc_change(tmp_file)
    assert updated == []
    assert len(idx.add_calls) == 1  # still only one add
    assert len(idx.update_calls) == 0


def test_on_doc_change_changed_content_calls_update(coordinator_with_index, tmp_file):
    coord, idx = coordinator_with_index
    coord.on_doc_change(tmp_file)
    tmp_file.write_text("Updated content", encoding="utf-8")
    updated = coord.on_doc_change(tmp_file)
    assert "main" in updated
    assert len(idx.update_calls) == 1
    assert idx.update_calls[0][1] == "Updated content"


def test_on_doc_change_no_indexes_returns_empty(coordinator, tmp_file):
    # No indexes registered, but file is new — still updates manifest
    updated = coordinator.on_doc_change(tmp_file)
    assert updated == []
    assert coordinator.stats()["docs_tracked"] == 1


def test_on_doc_change_missing_file_raises(coordinator):
    with pytest.raises(FileNotFoundError):
        coordinator.on_doc_change(Path("/nonexistent/path/file.md"))


def test_on_doc_change_multiple_indexes_all_updated(coordinator, tmp_file):
    idx1 = DictIndex()
    idx2 = DictIndex()
    coordinator.register("x", idx1)
    coordinator.register("y", idx2)
    updated = coordinator.on_doc_change(tmp_file)
    assert set(updated) == {"x", "y"}
    assert len(idx1.add_calls) == 1
    assert len(idx2.add_calls) == 1


def test_on_doc_change_doc_id_is_normalized_path(coordinator_with_index, tmp_file):
    coord, idx = coordinator_with_index
    coord.on_doc_change(tmp_file)
    expected_doc_id = str(tmp_file)
    assert idx.add_calls[0][0] == expected_doc_id


# ---------------------------------------------------------------------------
# on_doc_remove() tests (4 tests)
# ---------------------------------------------------------------------------


def test_on_doc_remove_calls_remove(coordinator_with_index, tmp_file):
    coord, idx = coordinator_with_index
    coord.on_doc_change(tmp_file)
    coord.on_doc_remove(tmp_file)
    assert str(tmp_file) in idx.remove_calls


def test_on_doc_remove_clears_manifest(coordinator_with_index, tmp_file):
    coord, idx = coordinator_with_index
    coord.on_doc_change(tmp_file)
    assert coord.stats()["docs_tracked"] == 1
    coord.on_doc_remove(tmp_file)
    assert coord.stats()["docs_tracked"] == 0


def test_on_doc_remove_idempotent_when_not_indexed(coordinator_with_index, tmp_file):
    coord, idx = coordinator_with_index
    # Remove without ever adding — should not raise
    coord.on_doc_remove(tmp_file)
    assert str(tmp_file) in idx.remove_calls


def test_on_doc_remove_all_indexes_called(coordinator, tmp_file):
    idx1 = DictIndex()
    idx2 = DictIndex()
    coordinator.register("p", idx1)
    coordinator.register("q", idx2)
    coordinator.on_doc_change(tmp_file)
    coordinator.on_doc_remove(tmp_file)
    assert str(tmp_file) in idx1.remove_calls
    assert str(tmp_file) in idx2.remove_calls


# ---------------------------------------------------------------------------
# query_all() tests (3 tests)
# ---------------------------------------------------------------------------


def test_query_all_returns_hits(coordinator_with_index, tmp_file):
    coord, idx = coordinator_with_index
    coord.on_doc_change(tmp_file)
    results = coord.query_all("Hello")
    assert "main" in results
    hits = results["main"]
    assert len(hits) >= 1
    assert all(isinstance(h, IndexHit) for h in hits)
    assert hits[0].index_name == "main"


def test_query_all_returns_empty_for_no_match(coordinator_with_index, tmp_file):
    coord, idx = coordinator_with_index
    coord.on_doc_change(tmp_file)
    results = coord.query_all("zzznomatch")
    assert results["main"] == []


def test_query_all_broken_index_returns_empty(coordinator, tmp_file):
    broken = BrokenQueryIndex()
    coordinator.register("broken", broken)
    coordinator.on_doc_change(tmp_file)
    results = coordinator.query_all("Hello")
    assert results["broken"] == []


# ---------------------------------------------------------------------------
# verify() tests (3 tests)
# ---------------------------------------------------------------------------


def test_verify_empty_when_all_present(coordinator_with_index, tmp_file):
    coord, idx = coordinator_with_index
    coord.on_doc_change(tmp_file)
    missing = coord.verify()
    assert missing["main"] == []


def test_verify_detects_missing_doc(coordinator, tmp_file):
    """Simulate an index that missed a doc: add to manifest but not to index."""
    idx = DictIndex()
    coordinator.register("sparse", idx)
    coordinator.on_doc_change(tmp_file)
    # Manually remove from index without touching manifest
    idx.docs.pop(str(tmp_file), None)
    missing = coordinator.verify()
    assert str(tmp_file) in missing["sparse"]


def test_verify_skips_index_without_list_all(coordinator, tmp_file):
    idx = NoListAllIndex()
    coordinator.register("nola", idx)
    coordinator.on_doc_change(tmp_file)
    missing = coordinator.verify()
    assert missing["nola"] == []


# ---------------------------------------------------------------------------
# stats() tests (3 tests)
# ---------------------------------------------------------------------------


def test_stats_initial(coordinator):
    s = coordinator.stats()
    assert s["docs_tracked"] == 0
    assert s["indexes"] == []


def test_stats_after_changes(coordinator, tmp_file, tmp_path):
    idx = DictIndex()
    coordinator.register("z", idx)
    coordinator.on_doc_change(tmp_file)
    second = tmp_path / "second.md"
    second.write_text("Another doc")
    coordinator.on_doc_change(second)
    s = coordinator.stats()
    assert s["docs_tracked"] == 2
    assert "z" in s["indexes"]


def test_stats_after_remove(coordinator_with_index, tmp_file):
    coord, idx = coordinator_with_index
    coord.on_doc_change(tmp_file)
    coord.on_doc_remove(tmp_file)
    assert coord.stats()["docs_tracked"] == 0


# ---------------------------------------------------------------------------
# Thread-safety smoke test (1 test)
# ---------------------------------------------------------------------------


def test_thread_safety(tmp_path):
    """Multiple threads updating different docs concurrently should not corrupt state."""
    coord = IndexCoordinator()
    idx = DictIndex()
    coord.register("shared", idx)

    errors: list[Exception] = []

    def worker(n: int):
        p = tmp_path / f"doc_{n}.md"
        p.write_text(f"Content {n}")
        try:
            coord.on_doc_change(p)
        except Exception as exc:
            errors.append(exc)

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert errors == [], f"Thread errors: {errors}"
    assert coord.stats()["docs_tracked"] == 10


# ---------------------------------------------------------------------------
# Import from package __init__ (1 test)
# ---------------------------------------------------------------------------


def test_exports_from_package():
    from docstoolkit.embeddings import Index, IndexHit, IndexCoordinator  # noqa: F401
    assert True
