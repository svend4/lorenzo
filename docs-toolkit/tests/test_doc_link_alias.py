"""Tests for E425 DocLinkAlias."""
from __future__ import annotations

import threading
import time

import pytest

from docstoolkit.doc_link_alias import (
    AliasStats,
    DocLinkAlias,
    LinkAliasEntry,
)


# ---------------------------------------------------------------------------
# Dataclass smoke tests
# ---------------------------------------------------------------------------


def test_link_alias_entry_defaults():
    e = LinkAliasEntry(alias="a", target_url="http://x")
    assert e.alias == "a"
    assert e.target_url == "http://x"
    assert e.description == ""
    assert e.created_at == 0.0
    assert e.hit_count == 0


def test_link_alias_entry_full():
    e = LinkAliasEntry(
        alias="a",
        target_url="http://x",
        description="d",
        created_at=1.0,
        hit_count=3,
    )
    assert e.description == "d"
    assert e.created_at == 1.0
    assert e.hit_count == 3


def test_alias_stats_dataclass():
    s = AliasStats(total_aliases=2, unique_targets=1, total_hits=5)
    assert s.total_aliases == 2
    assert s.unique_targets == 1
    assert s.total_hits == 5


# ---------------------------------------------------------------------------
# register / unregister
# ---------------------------------------------------------------------------


def test_register_returns_entry():
    m = DocLinkAlias()
    e = m.register("docs", "http://docs", "desc", now=10.0)
    assert isinstance(e, LinkAliasEntry)
    assert e.alias == "docs"
    assert e.target_url == "http://docs"
    assert e.description == "desc"
    assert e.created_at == 10.0
    assert e.hit_count == 0


def test_register_default_timestamp_uses_time(monkeypatch):
    m = DocLinkAlias()
    monkeypatch.setattr("docstoolkit.doc_link_alias.alias.time.time", lambda: 42.5)
    e = m.register("a", "http://a")
    assert e.created_at == 42.5


def test_register_existing_updates_target_keeps_metadata():
    m = DocLinkAlias()
    e1 = m.register("a", "http://a", "old", now=1.0)
    # bump hit count
    m.resolve("a")
    e2 = m.register("a", "http://b", "new", now=99.0)
    assert e2 is e1  # same object
    assert e2.target_url == "http://b"
    assert e2.description == "new"
    assert e2.created_at == 1.0  # preserved
    assert e2.hit_count == 1  # preserved


def test_register_empty_alias_raises():
    m = DocLinkAlias()
    with pytest.raises(ValueError):
        m.register("", "http://x")


def test_register_non_string_alias_raises():
    m = DocLinkAlias()
    with pytest.raises(ValueError):
        m.register(None, "http://x")  # type: ignore[arg-type]


def test_register_empty_target_raises():
    m = DocLinkAlias()
    with pytest.raises(ValueError):
        m.register("a", "")


def test_register_non_string_target_raises():
    m = DocLinkAlias()
    with pytest.raises(ValueError):
        m.register("a", None)  # type: ignore[arg-type]


def test_unregister_existing_returns_true():
    m = DocLinkAlias()
    m.register("a", "http://a")
    assert m.unregister("a") is True
    assert "a" not in m


def test_unregister_missing_returns_false():
    m = DocLinkAlias()
    assert m.unregister("missing") is False


def test_unregister_twice():
    m = DocLinkAlias()
    m.register("a", "http://a")
    assert m.unregister("a") is True
    assert m.unregister("a") is False


# ---------------------------------------------------------------------------
# resolve / peek
# ---------------------------------------------------------------------------


def test_resolve_returns_target():
    m = DocLinkAlias()
    m.register("a", "http://a")
    assert m.resolve("a") == "http://a"


def test_resolve_increments_hit_count():
    m = DocLinkAlias()
    m.register("a", "http://a")
    m.resolve("a")
    m.resolve("a")
    m.resolve("a")
    assert m.peek("a").hit_count == 3


def test_resolve_missing_returns_none():
    m = DocLinkAlias()
    assert m.resolve("missing") is None


def test_resolve_missing_does_not_create():
    m = DocLinkAlias()
    m.resolve("missing")
    assert len(m) == 0


def test_peek_returns_entry_without_hit():
    m = DocLinkAlias()
    m.register("a", "http://a")
    e = m.peek("a")
    assert e is not None
    assert e.hit_count == 0
    # peek again
    m.peek("a")
    assert m.peek("a").hit_count == 0


def test_peek_missing_returns_none():
    m = DocLinkAlias()
    assert m.peek("missing") is None


# ---------------------------------------------------------------------------
# expand_text
# ---------------------------------------------------------------------------


def test_expand_text_basic():
    m = DocLinkAlias()
    m.register("docs", "http://docs")
    out = m.expand_text("see @docs for more")
    assert out == "see http://docs for more"


def test_expand_text_multiple():
    m = DocLinkAlias()
    m.register("a", "http://a")
    m.register("b", "http://b")
    out = m.expand_text("@a and @b")
    assert out == "http://a and http://b"


def test_expand_text_unknown_alias_left_unchanged():
    m = DocLinkAlias()
    m.register("docs", "http://docs")
    out = m.expand_text("@docs and @unknown")
    assert out == "http://docs and @unknown"


def test_expand_text_increments_hit_count():
    m = DocLinkAlias()
    m.register("docs", "http://docs")
    m.expand_text("@docs @docs @docs")
    assert m.peek("docs").hit_count == 3


def test_expand_text_no_increment_for_missing():
    m = DocLinkAlias()
    m.register("docs", "http://docs")
    m.expand_text("@unknown @docs")
    assert m.peek("docs").hit_count == 1


def test_expand_text_custom_marker():
    m = DocLinkAlias()
    m.register("docs", "http://docs")
    out = m.expand_text("see #docs", marker="#")
    assert out == "see http://docs"


def test_expand_text_multichar_marker():
    m = DocLinkAlias()
    m.register("docs", "http://docs")
    out = m.expand_text("see %%docs end", marker="%%")
    assert out == "see http://docs end"


def test_expand_text_marker_special_regex_chars():
    m = DocLinkAlias()
    m.register("docs", "http://docs")
    out = m.expand_text("see .docs", marker=".")
    assert out == "see http://docs"


def test_expand_text_with_underscore_in_alias():
    m = DocLinkAlias()
    m.register("my_alias", "http://x")
    out = m.expand_text("@my_alias")
    assert out == "http://x"


def test_expand_text_with_digits_in_alias():
    m = DocLinkAlias()
    m.register("v2", "http://v2")
    out = m.expand_text("@v2")
    assert out == "http://v2"


def test_expand_text_stops_at_non_word():
    m = DocLinkAlias()
    m.register("a", "http://a")
    out = m.expand_text("@a!")
    assert out == "http://a!"


def test_expand_text_empty_input():
    m = DocLinkAlias()
    m.register("a", "http://a")
    assert m.expand_text("") == ""


def test_expand_text_no_marker_in_input():
    m = DocLinkAlias()
    m.register("a", "http://a")
    assert m.expand_text("plain text") == "plain text"


def test_expand_text_rejects_empty_marker():
    m = DocLinkAlias()
    with pytest.raises(ValueError):
        m.expand_text("hi", marker="")


def test_expand_text_rejects_non_string():
    m = DocLinkAlias()
    with pytest.raises(TypeError):
        m.expand_text(123)  # type: ignore[arg-type]


def test_expand_text_lone_marker_unchanged():
    m = DocLinkAlias()
    out = m.expand_text("just @ alone")
    assert out == "just @ alone"


# ---------------------------------------------------------------------------
# update_target
# ---------------------------------------------------------------------------


def test_update_target_existing():
    m = DocLinkAlias()
    m.register("a", "http://a")
    assert m.update_target("a", "http://b") is True
    assert m.resolve("a") == "http://b"


def test_update_target_preserves_hit_count():
    m = DocLinkAlias()
    m.register("a", "http://a")
    m.resolve("a")
    m.resolve("a")
    m.update_target("a", "http://b")
    assert m.peek("a").hit_count == 2


def test_update_target_missing_returns_false():
    m = DocLinkAlias()
    assert m.update_target("missing", "http://x") is False


def test_update_target_empty_raises():
    m = DocLinkAlias()
    m.register("a", "http://a")
    with pytest.raises(ValueError):
        m.update_target("a", "")


# ---------------------------------------------------------------------------
# aliases_for_target
# ---------------------------------------------------------------------------


def test_aliases_for_target_empty():
    m = DocLinkAlias()
    assert m.aliases_for_target("http://x") == []


def test_aliases_for_target_single():
    m = DocLinkAlias()
    m.register("a", "http://x")
    assert m.aliases_for_target("http://x") == ["a"]


def test_aliases_for_target_multiple_sorted():
    m = DocLinkAlias()
    m.register("zeta", "http://x")
    m.register("alpha", "http://x")
    m.register("beta", "http://x")
    m.register("other", "http://y")
    assert m.aliases_for_target("http://x") == ["alpha", "beta", "zeta"]


def test_aliases_for_target_no_match():
    m = DocLinkAlias()
    m.register("a", "http://a")
    assert m.aliases_for_target("http://other") == []


# ---------------------------------------------------------------------------
# list_aliases
# ---------------------------------------------------------------------------


def test_list_aliases_empty():
    m = DocLinkAlias()
    assert m.list_aliases() == []


def test_list_aliases_sorted():
    m = DocLinkAlias()
    m.register("zeta", "http://z")
    m.register("alpha", "http://a")
    m.register("mid", "http://m")
    entries = m.list_aliases()
    assert [e.alias for e in entries] == ["alpha", "mid", "zeta"]


def test_list_aliases_returns_entries():
    m = DocLinkAlias()
    m.register("a", "http://a", "desc")
    entries = m.list_aliases()
    assert len(entries) == 1
    assert isinstance(entries[0], LinkAliasEntry)
    assert entries[0].description == "desc"


# ---------------------------------------------------------------------------
# top_used
# ---------------------------------------------------------------------------


def test_top_used_empty():
    m = DocLinkAlias()
    assert m.top_used() == []


def test_top_used_by_hit_count_desc():
    m = DocLinkAlias()
    m.register("a", "http://a")
    m.register("b", "http://b")
    m.register("c", "http://c")
    for _ in range(3):
        m.resolve("a")
    for _ in range(5):
        m.resolve("b")
    m.resolve("c")
    entries = m.top_used()
    assert [e.alias for e in entries] == ["b", "a", "c"]


def test_top_used_ties_sorted_by_alias_asc():
    m = DocLinkAlias()
    m.register("zeta", "http://z")
    m.register("alpha", "http://a")
    m.register("beta", "http://b")
    # all share hit_count == 0
    entries = m.top_used()
    assert [e.alias for e in entries] == ["alpha", "beta", "zeta"]


def test_top_used_limit():
    m = DocLinkAlias()
    for c in "abcde":
        m.register(c, f"http://{c}")
    assert len(m.top_used(limit=3)) == 3


def test_top_used_limit_zero():
    m = DocLinkAlias()
    m.register("a", "http://a")
    assert m.top_used(limit=0) == []


def test_top_used_limit_larger_than_table():
    m = DocLinkAlias()
    m.register("a", "http://a")
    assert len(m.top_used(limit=100)) == 1


def test_top_used_negative_limit_raises():
    m = DocLinkAlias()
    with pytest.raises(ValueError):
        m.top_used(limit=-1)


# ---------------------------------------------------------------------------
# unused_aliases
# ---------------------------------------------------------------------------


def test_unused_aliases_empty():
    m = DocLinkAlias()
    assert m.unused_aliases() == []


def test_unused_aliases_all_unused():
    m = DocLinkAlias()
    m.register("b", "http://b")
    m.register("a", "http://a")
    assert m.unused_aliases() == ["a", "b"]


def test_unused_aliases_excludes_resolved():
    m = DocLinkAlias()
    m.register("a", "http://a")
    m.register("b", "http://b")
    m.resolve("a")
    assert m.unused_aliases() == ["b"]


def test_unused_aliases_sorted():
    m = DocLinkAlias()
    m.register("zeta", "http://z")
    m.register("alpha", "http://a")
    m.register("mid", "http://m")
    assert m.unused_aliases() == ["alpha", "mid", "zeta"]


# ---------------------------------------------------------------------------
# clear
# ---------------------------------------------------------------------------


def test_clear_empty_returns_zero():
    m = DocLinkAlias()
    assert m.clear() == 0


def test_clear_returns_count():
    m = DocLinkAlias()
    m.register("a", "http://a")
    m.register("b", "http://b")
    m.register("c", "http://c")
    assert m.clear() == 3


def test_clear_actually_clears():
    m = DocLinkAlias()
    m.register("a", "http://a")
    m.clear()
    assert len(m) == 0
    assert m.list_aliases() == []


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------


def test_stats_empty():
    s = DocLinkAlias().stats()
    assert s == AliasStats(total_aliases=0, unique_targets=0, total_hits=0)


def test_stats_basic():
    m = DocLinkAlias()
    m.register("a", "http://x")
    m.register("b", "http://x")  # same target
    m.register("c", "http://y")
    m.resolve("a")
    m.resolve("a")
    m.resolve("c")
    s = m.stats()
    assert s.total_aliases == 3
    assert s.unique_targets == 2
    assert s.total_hits == 3


def test_stats_after_unregister():
    m = DocLinkAlias()
    m.register("a", "http://a")
    m.register("b", "http://b")
    m.resolve("a")
    m.unregister("a")
    s = m.stats()
    assert s.total_aliases == 1
    assert s.unique_targets == 1
    assert s.total_hits == 0


# ---------------------------------------------------------------------------
# Dunder helpers
# ---------------------------------------------------------------------------


def test_len_empty():
    assert len(DocLinkAlias()) == 0


def test_len_after_registers():
    m = DocLinkAlias()
    m.register("a", "http://a")
    m.register("b", "http://b")
    assert len(m) == 2


def test_contains_true():
    m = DocLinkAlias()
    m.register("a", "http://a")
    assert "a" in m


def test_contains_false():
    m = DocLinkAlias()
    assert "missing" not in m


def test_contains_non_string():
    m = DocLinkAlias()
    assert (123 in m) is False  # type: ignore[operator]


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------


def test_thread_safety_register_concurrent():
    m = DocLinkAlias()
    n_threads = 8
    per_thread = 50

    def worker(tid: int) -> None:
        for i in range(per_thread):
            m.register(f"t{tid}_a{i}", f"http://{tid}/{i}")

    threads = [threading.Thread(target=worker, args=(t,)) for t in range(n_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len(m) == n_threads * per_thread


def test_thread_safety_resolve_concurrent():
    m = DocLinkAlias()
    m.register("hot", "http://hot")

    n_threads = 8
    per_thread = 100

    def worker() -> None:
        for _ in range(per_thread):
            m.resolve("hot")

    threads = [threading.Thread(target=worker) for _ in range(n_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert m.peek("hot").hit_count == n_threads * per_thread


def test_thread_safety_mixed_ops():
    m = DocLinkAlias()
    for i in range(20):
        m.register(f"a{i}", f"http://{i}")

    stop = threading.Event()
    errors: list[Exception] = []

    def reader() -> None:
        try:
            while not stop.is_set():
                m.list_aliases()
                m.stats()
                m.top_used(5)
                m.unused_aliases()
        except Exception as exc:  # pragma: no cover - defensive
            errors.append(exc)

    def writer() -> None:
        try:
            for i in range(50):
                m.register(f"w{i}", f"http://w/{i}")
                m.resolve(f"a{i % 20}")
                if i % 5 == 0:
                    m.unregister(f"w{i // 2}")
                m.expand_text(f"see @a{i % 20} done")
        except Exception as exc:  # pragma: no cover - defensive
            errors.append(exc)

    readers = [threading.Thread(target=reader) for _ in range(3)]
    writers = [threading.Thread(target=writer) for _ in range(3)]
    for t in readers + writers:
        t.start()
    for t in writers:
        t.join()
    stop.set()
    for t in readers:
        t.join()

    assert errors == []
    # The store remained healthy: stats should be consistent.
    s = m.stats()
    assert s.total_aliases == len(m)


def test_thread_safety_expand_text_concurrent():
    m = DocLinkAlias()
    m.register("a", "http://a")

    n_threads = 6
    per_thread = 50

    def worker() -> None:
        for _ in range(per_thread):
            out = m.expand_text("hello @a world")
            assert out == "hello http://a world"

    threads = [threading.Thread(target=worker) for _ in range(n_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert m.peek("a").hit_count == n_threads * per_thread
