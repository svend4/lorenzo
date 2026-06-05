"""Тесты IncrementalIndex + WatchResult/watch_once."""
import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.embeddings.incremental import IncrementalIndex, _hash_file
from docstoolkit.embeddings.watcher import WatchResult, watch_once


# ------------------------------------------------------------------ #
# Fixtures                                                            #
# ------------------------------------------------------------------ #

@pytest.fixture
def root(tmp_path):
    """Временная корневая директория."""
    return tmp_path


@pytest.fixture
def idx(root):
    """IncrementalIndex с tmp root."""
    index = IncrementalIndex(root)
    yield index
    index.close()


@pytest.fixture
def docs(tmp_path):
    """Директория с несколькими .md файлами."""
    d = tmp_path / "docs"
    d.mkdir()
    (d / "a.md").write_text("# A\nHello")
    (d / "b.md").write_text("# B\nWorld")
    return d


# ------------------------------------------------------------------ #
# needs_update                                                         #
# ------------------------------------------------------------------ #

def test_needs_update_new_file(idx, tmp_path):
    """Файл отсутствующий в манифесте всегда требует индексации."""
    p = tmp_path / "test.md"
    p.write_text("content")
    stat = p.stat()
    assert idx.needs_update(p, stat.st_mtime, stat.st_size) is True


def test_needs_update_after_mark_indexed(idx, tmp_path):
    """После mark_indexed needs_update должен вернуть False."""
    p = tmp_path / "test.md"
    p.write_text("content")
    stat = p.stat()
    idx.mark_indexed(p, stat.st_mtime, stat.st_size, "hash123")
    assert idx.needs_update(p, stat.st_mtime, stat.st_size) is False


def test_needs_update_mtime_changed(idx, tmp_path):
    """Изменение mtime должно потребовать переиндексации."""
    p = tmp_path / "test.md"
    p.write_text("content")
    stat = p.stat()
    idx.mark_indexed(p, stat.st_mtime, stat.st_size, "hash123")
    # Симулируем изменение mtime
    assert idx.needs_update(p, stat.st_mtime + 1.0, stat.st_size) is True


def test_needs_update_size_changed(idx, tmp_path):
    """Изменение размера должно потребовать переиндексации."""
    p = tmp_path / "test.md"
    p.write_text("content")
    stat = p.stat()
    idx.mark_indexed(p, stat.st_mtime, stat.st_size, "hash123")
    assert idx.needs_update(p, stat.st_mtime, stat.st_size + 10) is True


# ------------------------------------------------------------------ #
# mark_indexed                                                         #
# ------------------------------------------------------------------ #

def test_mark_indexed_stores_all_fields(idx, tmp_path):
    """mark_indexed должен сохранить все поля в манифесте."""
    p = tmp_path / "doc.md"
    p.write_text("hello")
    mtime = 1700000000.0
    size = 5
    content_hash = "abcdef123456"
    idx.mark_indexed(p, mtime, size, content_hash)

    row = idx.conn.execute(
        "SELECT * FROM manifest WHERE path = ?", (str(p),)
    ).fetchone()
    assert row is not None
    assert row["mtime"] == mtime
    assert row["size"] == size
    assert row["content_hash"] == content_hash
    assert row["indexed_ts"] > 0


def test_mark_indexed_update_replaces_existing(idx, tmp_path):
    """Повторный mark_indexed должен обновить запись."""
    p = tmp_path / "doc.md"
    p.write_text("hello")
    idx.mark_indexed(p, 1000.0, 5, "hash_v1")
    idx.mark_indexed(p, 2000.0, 10, "hash_v2")

    row = idx.conn.execute(
        "SELECT mtime, size, content_hash FROM manifest WHERE path = ?",
        (str(p),)
    ).fetchone()
    assert row["mtime"] == 2000.0
    assert row["size"] == 10
    assert row["content_hash"] == "hash_v2"


# ------------------------------------------------------------------ #
# get_stale_docs                                                        #
# ------------------------------------------------------------------ #

def test_get_stale_docs_all_new(idx, docs):
    """Пустой манифест → все файлы считаются устаревшими."""
    stale = idx.get_stale_docs(docs)
    assert len(stale) == 2
    names = {p.name for p in stale}
    assert "a.md" in names
    assert "b.md" in names


def test_get_stale_docs_none_after_indexing(idx, docs):
    """После индексации всех файлов get_stale_docs возвращает пустой список."""
    for path in docs.rglob("*.md"):
        stat = path.stat()
        idx.mark_indexed(path, stat.st_mtime, stat.st_size, "h")
    stale = idx.get_stale_docs(docs)
    assert stale == []


def test_get_stale_docs_detects_modification(idx, docs):
    """Изменение файла должно сделать его устаревшим."""
    a = docs / "a.md"
    stat = a.stat()
    idx.mark_indexed(a, stat.st_mtime, stat.st_size, "h")
    b = docs / "b.md"
    stat_b = b.stat()
    idx.mark_indexed(b, stat_b.st_mtime, stat_b.st_size, "h")

    # Симулируем изменение a.md (обновляем запись вручную с другим mtime)
    idx.conn.execute(
        "UPDATE manifest SET mtime = mtime - 100 WHERE path = ?", (str(a),)
    )
    idx.conn.commit()

    stale = idx.get_stale_docs(docs)
    assert any(p.name == "a.md" for p in stale)
    assert not any(p.name == "b.md" for p in stale)


def test_get_stale_docs_ignores_non_md(idx, docs):
    """Файлы не .md не включаются в stale."""
    (docs / "readme.txt").write_text("ignore me")
    stale = idx.get_stale_docs(docs)
    assert all(p.suffix == ".md" for p in stale)


# ------------------------------------------------------------------ #
# purge_deleted                                                         #
# ------------------------------------------------------------------ #

def test_purge_deleted_removes_missing_files(idx, docs):
    """purge_deleted должен удалить записи для файлов, которых больше нет."""
    a = docs / "a.md"
    b = docs / "b.md"
    for p in [a, b]:
        stat = p.stat()
        idx.mark_indexed(p, stat.st_mtime, stat.st_size, "h")

    # Удаляем a.md с диска
    a.unlink()
    deleted = idx.purge_deleted(docs)
    assert deleted == 1

    # Запись для a.md должна быть удалена
    row = idx.conn.execute(
        "SELECT * FROM manifest WHERE path = ?", (str(a),)
    ).fetchone()
    assert row is None

    # Запись для b.md должна остаться
    row_b = idx.conn.execute(
        "SELECT * FROM manifest WHERE path = ?", (str(b),)
    ).fetchone()
    assert row_b is not None


def test_purge_deleted_returns_zero_when_nothing_to_purge(idx, docs):
    """Если все файлы на месте — purge_deleted возвращает 0."""
    for path in docs.rglob("*.md"):
        stat = path.stat()
        idx.mark_indexed(path, stat.st_mtime, stat.st_size, "h")
    assert idx.purge_deleted(docs) == 0


def test_purge_deleted_ignores_other_docs_dir(idx, tmp_path):
    """purge_deleted не должен трогать записи из другого docs_dir."""
    other_docs = tmp_path / "other_docs"
    other_docs.mkdir()
    ghost = other_docs / "ghost.md"
    ghost.write_text("x")
    stat = ghost.stat()
    idx.mark_indexed(ghost, stat.st_mtime, stat.st_size, "h")
    # Удаляем файл с диска
    ghost.unlink()

    main_docs = tmp_path / "docs"
    main_docs.mkdir()
    # purge_deleted для main_docs не должен трогать записи из other_docs
    deleted = idx.purge_deleted(main_docs)
    assert deleted == 0

    # Запись ghost всё ещё должна быть
    row = idx.conn.execute(
        "SELECT * FROM manifest WHERE path = ?", (str(ghost),)
    ).fetchone()
    assert row is not None


# ------------------------------------------------------------------ #
# stats                                                                 #
# ------------------------------------------------------------------ #

def test_stats_empty(idx):
    s = idx.stats()
    assert s["total_tracked"] == 0
    assert s["last_update"] is None


def test_stats_after_indexing(idx, tmp_path):
    p = tmp_path / "x.md"
    p.write_text("hi")
    stat = p.stat()
    idx.mark_indexed(p, stat.st_mtime, stat.st_size, "h")
    s = idx.stats()
    assert s["total_tracked"] == 1
    assert s["last_update"] is not None
    assert ".docstoolkit" in s["db_path"]


# ------------------------------------------------------------------ #
# WatchResult and watch_once                                           #
# ------------------------------------------------------------------ #

def test_watch_result_has_changes_false_when_empty():
    wr = WatchResult()
    assert wr.has_changes is False
    assert wr.total == 0


def test_watch_result_has_changes_true_when_added():
    wr = WatchResult(added=[Path("x.md")])
    assert wr.has_changes is True
    assert wr.total == 1


def test_watch_once_all_added(idx, docs):
    """Пустой манифест → все файлы в added."""
    result = watch_once(docs, idx)
    assert len(result.added) == 2
    assert result.changed == []
    assert result.deleted == []


def test_watch_once_no_changes_after_mark(idx, docs):
    """После mark_indexed всех файлов → нет изменений."""
    for path in docs.rglob("*.md"):
        stat = path.stat()
        idx.mark_indexed(path, stat.st_mtime, stat.st_size, "h")
    result = watch_once(docs, idx)
    assert not result.has_changes


def test_watch_once_detects_deleted(idx, docs):
    """Файл удалён с диска → попадает в deleted."""
    a = docs / "a.md"
    b = docs / "b.md"
    for p in [a, b]:
        stat = p.stat()
        idx.mark_indexed(p, stat.st_mtime, stat.st_size, "h")
    a.unlink()
    result = watch_once(docs, idx)
    assert a in result.deleted
    assert b not in result.deleted


def test_watch_once_detects_changed(idx, docs):
    """Файл с изменённым mtime → попадает в changed."""
    a = docs / "a.md"
    b = docs / "b.md"
    stat_a = a.stat()
    stat_b = b.stat()
    idx.mark_indexed(a, stat_a.st_mtime, stat_a.st_size, "h")
    idx.mark_indexed(b, stat_b.st_mtime, stat_b.st_size, "h")

    # Симулируем изменение mtime в манифесте (уменьшаем, чтобы не совпадало)
    idx.conn.execute(
        "UPDATE manifest SET mtime = mtime - 100 WHERE path = ?", (str(a),)
    )
    idx.conn.commit()

    result = watch_once(docs, idx)
    assert a in result.changed
    assert b not in result.changed


# ------------------------------------------------------------------ #
# _hash_file                                                            #
# ------------------------------------------------------------------ #

def test_hash_file_consistent(tmp_path):
    p = tmp_path / "f.md"
    p.write_text("hello world")
    h1 = _hash_file(p)
    h2 = _hash_file(p)
    assert h1 == h2
    assert len(h1) == 16


def test_hash_file_missing_returns_empty(tmp_path):
    p = tmp_path / "nonexistent.md"
    assert _hash_file(p) == ""
