"""Tests for docstoolkit.reads (read-receipt + reading time tracking)."""
import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.reads import (
    ReadRecord,
    ReadStore,
    estimate_reading_time,
    recommendations_for,
)
from docstoolkit.reads.store import READ, SAVED, SKIPPED, UNREAD


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def store(tmp_path):
    """ReadStore backed by a temp SQLite file."""
    db = tmp_path / ".docstoolkit" / "reads.sqlite"
    s = ReadStore(db_path=db)
    yield s
    s.close()


# ---------------------------------------------------------------------------
# S7-1  Imports
# ---------------------------------------------------------------------------

def test_imports():
    assert ReadStore is not None
    assert ReadRecord is not None
    assert estimate_reading_time is not None
    assert recommendations_for is not None


# ---------------------------------------------------------------------------
# S7-2  ReadRecord dataclass
# ---------------------------------------------------------------------------

def test_read_record_fields():
    r = ReadRecord(
        user="alice",
        doc_id="docs/intro.md",
        status="read",
        ts="2026-01-01T10:00:00",
        reading_time_sec=120,
    )
    assert r.user == "alice"
    assert r.doc_id == "docs/intro.md"
    assert r.status == "read"
    assert r.reading_time_sec == 120


def test_read_record_default_reading_time():
    r = ReadRecord(user="bob", doc_id="x.md", status="unread", ts="2026-01-01T00:00:00")
    assert r.reading_time_sec == 0


# ---------------------------------------------------------------------------
# S7-3  mark / get_status
# ---------------------------------------------------------------------------

def test_mark_and_get_status(store):
    store.mark("alice", "docs/a.md", "read")
    assert store.get_status("alice", "docs/a.md") == "read"


def test_get_status_unread_default(store):
    assert store.get_status("alice", "docs/nonexistent.md") == "unread"


def test_mark_upsert(store):
    store.mark("alice", "docs/a.md", "read")
    store.mark("alice", "docs/a.md", "saved")
    assert store.get_status("alice", "docs/a.md") == "saved"


def test_mark_with_reading_time(store):
    store.mark("alice", "docs/a.md", "read", reading_time_sec=300)
    records = store.list_by_status("alice", "read")
    assert records[0].reading_time_sec == 300


def test_mark_different_users(store):
    store.mark("alice", "docs/a.md", "read")
    store.mark("bob", "docs/a.md", "skipped")
    assert store.get_status("alice", "docs/a.md") == "read"
    assert store.get_status("bob", "docs/a.md") == "skipped"


# ---------------------------------------------------------------------------
# S7-4  list_by_status
# ---------------------------------------------------------------------------

def test_list_by_status_empty(store):
    result = store.list_by_status("alice", "read")
    assert result == []


def test_list_by_status_filters_correctly(store):
    store.mark("alice", "docs/a.md", "read")
    store.mark("alice", "docs/b.md", "saved")
    store.mark("alice", "docs/c.md", "read")
    read_records = store.list_by_status("alice", "read")
    assert len(read_records) == 2
    doc_ids = {r.doc_id for r in read_records}
    assert "docs/a.md" in doc_ids
    assert "docs/c.md" in doc_ids
    assert "docs/b.md" not in doc_ids


def test_list_by_status_returns_read_records(store):
    store.mark("alice", "docs/x.md", "skipped")
    records = store.list_by_status("alice", "skipped")
    assert len(records) == 1
    assert isinstance(records[0], ReadRecord)
    assert records[0].status == "skipped"


def test_list_by_status_user_isolation(store):
    store.mark("alice", "docs/a.md", "read")
    store.mark("bob", "docs/b.md", "read")
    alice_reads = store.list_by_status("alice", "read")
    assert len(alice_reads) == 1
    assert alice_reads[0].user == "alice"


# ---------------------------------------------------------------------------
# S7-5  reading_history
# ---------------------------------------------------------------------------

def test_reading_history_ordering(store):
    # Insert records with explicit timestamps to guarantee ordering
    store.conn.execute(
        "INSERT INTO reads (user, doc_id, status, ts, reading_time_sec) VALUES (?,?,?,?,?)",
        ("alice", "docs/first.md", "read", "2026-01-01T10:00:00", 0),
    )
    store.conn.execute(
        "INSERT INTO reads (user, doc_id, status, ts, reading_time_sec) VALUES (?,?,?,?,?)",
        ("alice", "docs/second.md", "read", "2026-01-01T10:00:01", 0),
    )
    store.conn.execute(
        "INSERT INTO reads (user, doc_id, status, ts, reading_time_sec) VALUES (?,?,?,?,?)",
        ("alice", "docs/third.md", "read", "2026-01-01T10:00:02", 0),
    )
    store.conn.commit()
    history = store.reading_history("alice")
    # Newest first — third should be before first
    doc_ids = [r.doc_id for r in history]
    assert doc_ids.index("docs/third.md") < doc_ids.index("docs/first.md")


def test_reading_history_limit(store):
    for i in range(10):
        store.mark("alice", f"docs/doc{i}.md", "read")
    history = store.reading_history("alice", limit=3)
    assert len(history) == 3


def test_reading_history_empty_for_new_user(store):
    assert store.reading_history("newuser") == []


def test_reading_history_all_statuses(store):
    store.mark("alice", "docs/a.md", "read")
    store.mark("alice", "docs/b.md", "skipped")
    store.mark("alice", "docs/c.md", "saved")
    history = store.reading_history("alice")
    assert len(history) == 3


# ---------------------------------------------------------------------------
# S7-6  stats
# ---------------------------------------------------------------------------

def test_stats_empty(store):
    result = store.stats("alice")
    assert result == {}


def test_stats_breakdown(store):
    store.mark("alice", "docs/a.md", "read")
    store.mark("alice", "docs/b.md", "read")
    store.mark("alice", "docs/c.md", "skipped")
    store.mark("alice", "docs/d.md", "saved")
    stats = store.stats("alice")
    assert stats["read"] == 2
    assert stats["skipped"] == 1
    assert stats["saved"] == 1


def test_stats_user_isolation(store):
    store.mark("alice", "docs/a.md", "read")
    store.mark("bob", "docs/b.md", "read")
    store.mark("bob", "docs/c.md", "read")
    alice_stats = store.stats("alice")
    assert alice_stats.get("read", 0) == 1


# ---------------------------------------------------------------------------
# S7-7  estimate_reading_time
# ---------------------------------------------------------------------------

PURE_RU_TEXT = " ".join(["слово"] * 200)   # 200 Russian words
PURE_EN_TEXT = " ".join(["word"] * 250)     # 250 English words


def test_estimate_pure_russian():
    secs = estimate_reading_time(PURE_RU_TEXT, wpm_ru=200, wpm_en=250)
    # 200 words / 200 wpm * 60 = 60 seconds
    assert secs == pytest.approx(60, abs=2)


def test_estimate_pure_english():
    secs = estimate_reading_time(PURE_EN_TEXT, wpm_ru=200, wpm_en=250)
    # 250 words / 250 wpm * 60 = 60 seconds
    assert secs == pytest.approx(60, abs=2)


def test_estimate_ru_slower_than_en():
    ru_text = " ".join(["слово"] * 300)
    en_text = " ".join(["word"] * 300)
    ru_secs = estimate_reading_time(ru_text, wpm_ru=200, wpm_en=250)
    en_secs = estimate_reading_time(en_text, wpm_ru=200, wpm_en=250)
    # Russian is slower (wpm_ru < wpm_en), so takes longer
    assert ru_secs > en_secs


def test_estimate_empty_text():
    assert estimate_reading_time("") == 0


def test_estimate_returns_int():
    secs = estimate_reading_time("hello world this is a test")
    assert isinstance(secs, int)


def test_estimate_ceil():
    # 1 word at 200 wpm = 0.005 min = 0.3 sec → ceil = 1
    text = "слово"
    secs = estimate_reading_time(text, wpm_ru=200, wpm_en=250)
    assert secs >= 1


# ---------------------------------------------------------------------------
# S7-8  recommendations_for
# ---------------------------------------------------------------------------

def test_recommendations_empty_history(store):
    graph = {"docs/a.md": ["docs/b.md"]}
    recs = recommendations_for("alice", store, graph)
    assert recs == []


def test_recommendations_basic(store):
    store.mark("alice", "docs/a.md", "read")
    # docs/a.md cites docs/b.md and docs/c.md
    graph = {
        "docs/a.md": ["docs/b.md", "docs/c.md"],
    }
    recs = recommendations_for("alice", store, graph)
    rec_ids = [r[0] for r in recs]
    assert "docs/b.md" in rec_ids
    assert "docs/c.md" in rec_ids


def test_recommendations_skips_already_read(store):
    store.mark("alice", "docs/a.md", "read")
    store.mark("alice", "docs/b.md", "read")
    graph = {"docs/a.md": ["docs/b.md", "docs/c.md"]}
    recs = recommendations_for("alice", store, graph)
    rec_ids = [r[0] for r in recs]
    assert "docs/b.md" not in rec_ids
    assert "docs/c.md" in rec_ids


def test_recommendations_reason_format(store):
    store.mark("alice", "docs/a.md", "read")
    graph = {"docs/a.md": ["docs/b.md"]}
    recs = recommendations_for("alice", store, graph)
    assert len(recs) == 1
    doc_id, score, reason = recs[0]
    assert "docs/a.md" in reason


def test_recommendations_top_k(store):
    store.mark("alice", "docs/a.md", "read")
    graph = {"docs/a.md": [f"docs/doc{i}.md" for i in range(20)]}
    recs = recommendations_for("alice", store, graph, top_k=5)
    assert len(recs) <= 5


def test_recommendations_with_pagerank(store):
    store.mark("alice", "docs/a.md", "read")
    graph = {
        "docs/a.md": ["docs/high.md", "docs/low.md"],
        "pagerank": {"docs/high.md": 0.9, "docs/low.md": 0.1},
    }
    recs = recommendations_for("alice", store, graph)
    # high-pagerank doc should come first
    assert recs[0][0] == "docs/high.md"


def test_recommendations_deduplication(store):
    store.mark("alice", "docs/a.md", "read")
    store.mark("alice", "docs/b.md", "read")
    # Both a and b cite docs/c.md
    graph = {
        "docs/a.md": ["docs/c.md"],
        "docs/b.md": ["docs/c.md"],
    }
    recs = recommendations_for("alice", store, graph)
    rec_ids = [r[0] for r in recs]
    # docs/c.md should appear only once
    assert rec_ids.count("docs/c.md") == 1
