"""Тесты vector DB backends."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.embeddings.vectordb import (
    SQLiteBackend, get_backend, list_backends, VectorMatch,
)


def test_list_backends_includes_sqlite():
    backends = list_backends()
    sqlite_b = next(b for b in backends if b["name"] == "sqlite")
    assert sqlite_b["available"] is True


def test_get_backend_default():
    """Unknown backend → fallback на sqlite."""
    import tempfile
    import os
    with tempfile.TemporaryDirectory() as tmp:
        b = get_backend("nonexistent", db_path=os.path.join(tmp, "x.sqlite"))
        assert b.name == "sqlite"
        b.close()


def test_sqlite_upsert_search(tmp_path):
    db = SQLiteBackend(tmp_path / "v.sqlite", dim=3)
    db.upsert("d1", [1.0, 0.0, 0.0], {"title": "X"})
    db.upsert("d2", [0.0, 1.0, 0.0], {"title": "Y"})

    results = db.search([1.0, 0.0, 0.0], top_k=2)
    assert len(results) == 2
    assert results[0].doc_id == "d1"
    assert results[0].score > 0.99
    assert results[1].doc_id == "d2"
    db.close()


def test_sqlite_upsert_replaces(tmp_path):
    db = SQLiteBackend(tmp_path / "v.sqlite", dim=3)
    db.upsert("d1", [1.0, 0.0, 0.0], {"v": 1})
    db.upsert("d1", [0.0, 1.0, 0.0], {"v": 2})  # replace
    assert db.count() == 1
    db.close()


def test_sqlite_batch(tmp_path):
    db = SQLiteBackend(tmp_path / "v.sqlite", dim=2)
    db.upsert_batch([
        ("a", [1.0, 0.0], {}),
        ("b", [0.0, 1.0], {}),
        ("c", [0.5, 0.5], {}),
    ])
    assert db.count() == 3
    db.close()


def test_sqlite_delete(tmp_path):
    db = SQLiteBackend(tmp_path / "v.sqlite", dim=2)
    db.upsert("d1", [1.0, 0.0])
    db.upsert("d2", [0.0, 1.0])
    db.delete("d1")
    assert db.count() == 1
    db.close()


def test_sqlite_metadata_returned(tmp_path):
    db = SQLiteBackend(tmp_path / "v.sqlite", dim=2)
    db.upsert("d1", [1.0, 0.0], {"author": "alice", "year": 2024})
    results = db.search([1.0, 0.0], top_k=1)
    assert results[0].metadata["author"] == "alice"
    assert results[0].metadata["year"] == 2024
    db.close()


def test_sqlite_dimension_mismatch_skips(tmp_path):
    """Векторы разных размерностей пропускаются при поиске."""
    db = SQLiteBackend(tmp_path / "v.sqlite", dim=3)
    db.upsert("d1", [1.0, 0.0, 0.0])
    # Search с другой размерностью
    results = db.search([1.0, 0.0], top_k=5)
    # Не падает, но не возвращает d1 (mismatch)
    assert len(results) == 0
    db.close()


def test_vector_match_dataclass():
    m = VectorMatch(doc_id="x", score=0.9, metadata={"k": "v"})
    assert m.doc_id == "x"
    assert m.metadata["k"] == "v"
