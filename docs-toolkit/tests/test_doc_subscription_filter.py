"""Tests for E422 DocSubscriptionFilter."""
from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_subscription_filter import (
    DocSubscriptionFilter,
    FilterMatchResult,
    SubFilter,
    SubFilterStats,
)


# ----------------------------------------------------------- SubFilter dataclass


def test_subfilter_defaults():
    f = SubFilter(filter_id="f1", subscriber_id="s1")
    assert f.doc_pattern == "*"
    assert f.event_types == []
    assert f.priority == 0
    assert f.enabled is True


def test_subfilter_event_types_independent_instances():
    a = SubFilter(filter_id="a", subscriber_id="s")
    b = SubFilter(filter_id="b", subscriber_id="s")
    a.event_types.append("created")
    assert b.event_types == []


def test_subfilter_custom_fields():
    f = SubFilter(
        filter_id="x",
        subscriber_id="u",
        doc_pattern="docs/*.md",
        event_types=["created", "updated"],
        priority=5,
        enabled=False,
    )
    assert f.doc_pattern == "docs/*.md"
    assert f.event_types == ["created", "updated"]
    assert f.priority == 5
    assert f.enabled is False


# ----------------------------------------------------------- FilterMatchResult


def test_match_result_defaults():
    r = FilterMatchResult(matched=False)
    assert r.matched is False
    assert r.matching_filters == []


def test_match_result_with_filters():
    r = FilterMatchResult(matched=True, matching_filters=["f1", "f2"])
    assert r.matched is True
    assert r.matching_filters == ["f1", "f2"]


# ----------------------------------------------------------- SubFilterStats


def test_stats_dataclass_fields():
    s = SubFilterStats(
        total_filters=2, enabled_filters=1, total_evaluations=5, total_matches=3
    )
    assert s.total_filters == 2
    assert s.enabled_filters == 1
    assert s.total_evaluations == 5
    assert s.total_matches == 3


# ----------------------------------------------------------- add_filter


def test_add_filter_basic():
    reg = DocSubscriptionFilter()
    reg.add_filter(SubFilter(filter_id="f1", subscriber_id="s1"))
    assert reg.get_filter("f1") is not None


def test_add_filter_duplicate_raises():
    reg = DocSubscriptionFilter()
    reg.add_filter(SubFilter(filter_id="f1", subscriber_id="s1"))
    with pytest.raises(ValueError):
        reg.add_filter(SubFilter(filter_id="f1", subscriber_id="s2"))


def test_add_filter_wrong_type():
    reg = DocSubscriptionFilter()
    with pytest.raises(TypeError):
        reg.add_filter({"filter_id": "f1"})  # type: ignore[arg-type]


def test_add_filter_empty_filter_id():
    reg = DocSubscriptionFilter()
    with pytest.raises(ValueError):
        reg.add_filter(SubFilter(filter_id="", subscriber_id="s1"))


def test_add_filter_empty_subscriber_id():
    reg = DocSubscriptionFilter()
    with pytest.raises(ValueError):
        reg.add_filter(SubFilter(filter_id="f1", subscriber_id=""))


def test_add_filter_tracked_by_subscriber():
    reg = DocSubscriptionFilter()
    reg.add_filter(SubFilter(filter_id="f1", subscriber_id="s1"))
    reg.add_filter(SubFilter(filter_id="f2", subscriber_id="s1"))
    assert {f.filter_id for f in reg.filters_for_subscriber("s1")} == {"f1", "f2"}


# ----------------------------------------------------------- remove_filter


def test_remove_filter_existing():
    reg = DocSubscriptionFilter()
    reg.add_filter(SubFilter(filter_id="f1", subscriber_id="s1"))
    assert reg.remove_filter("f1") is True
    assert reg.get_filter("f1") is None


def test_remove_filter_missing():
    reg = DocSubscriptionFilter()
    assert reg.remove_filter("nope") is False


def test_remove_filter_cleans_subscriber_index():
    reg = DocSubscriptionFilter()
    reg.add_filter(SubFilter(filter_id="f1", subscriber_id="s1"))
    reg.remove_filter("f1")
    assert reg.filters_for_subscriber("s1") == []


def test_remove_filter_keeps_other_subscriber_filters():
    reg = DocSubscriptionFilter()
    reg.add_filter(SubFilter(filter_id="f1", subscriber_id="s1"))
    reg.add_filter(SubFilter(filter_id="f2", subscriber_id="s1"))
    reg.remove_filter("f1")
    remaining = reg.filters_for_subscriber("s1")
    assert [f.filter_id for f in remaining] == ["f2"]


# ----------------------------------------------------------- enable / disable


def test_disable_filter():
    reg = DocSubscriptionFilter()
    reg.add_filter(SubFilter(filter_id="f1", subscriber_id="s1"))
    assert reg.disable_filter("f1") is True
    assert reg.get_filter("f1").enabled is False


def test_disable_filter_already_disabled():
    reg = DocSubscriptionFilter()
    reg.add_filter(SubFilter(filter_id="f1", subscriber_id="s1", enabled=False))
    assert reg.disable_filter("f1") is False


def test_disable_filter_missing():
    reg = DocSubscriptionFilter()
    assert reg.disable_filter("nope") is False


def test_enable_filter():
    reg = DocSubscriptionFilter()
    reg.add_filter(SubFilter(filter_id="f1", subscriber_id="s1", enabled=False))
    assert reg.enable_filter("f1") is True
    assert reg.get_filter("f1").enabled is True


def test_enable_filter_already_enabled():
    reg = DocSubscriptionFilter()
    reg.add_filter(SubFilter(filter_id="f1", subscriber_id="s1"))
    assert reg.enable_filter("f1") is False


def test_enable_filter_missing():
    reg = DocSubscriptionFilter()
    assert reg.enable_filter("nope") is False


# ----------------------------------------------------------- get_filter


def test_get_filter_present():
    reg = DocSubscriptionFilter()
    f = SubFilter(filter_id="f1", subscriber_id="s1")
    reg.add_filter(f)
    assert reg.get_filter("f1") is f


def test_get_filter_absent():
    reg = DocSubscriptionFilter()
    assert reg.get_filter("ghost") is None


# ----------------------------------------------------------- list_filters


def test_list_filters_empty():
    reg = DocSubscriptionFilter()
    assert reg.list_filters() == []


def test_list_filters_sorted_by_priority_desc():
    reg = DocSubscriptionFilter()
    reg.add_filter(SubFilter(filter_id="a", subscriber_id="s", priority=1))
    reg.add_filter(SubFilter(filter_id="b", subscriber_id="s", priority=10))
    reg.add_filter(SubFilter(filter_id="c", subscriber_id="s", priority=5))
    assert [f.filter_id for f in reg.list_filters()] == ["b", "c", "a"]


def test_list_filters_tiebreak_by_id():
    reg = DocSubscriptionFilter()
    reg.add_filter(SubFilter(filter_id="z", subscriber_id="s", priority=1))
    reg.add_filter(SubFilter(filter_id="a", subscriber_id="s", priority=1))
    reg.add_filter(SubFilter(filter_id="m", subscriber_id="s", priority=1))
    assert [f.filter_id for f in reg.list_filters()] == ["a", "m", "z"]


def test_list_filters_includes_disabled():
    reg = DocSubscriptionFilter()
    reg.add_filter(SubFilter(filter_id="f1", subscriber_id="s1", enabled=False))
    assert len(reg.list_filters()) == 1


# ----------------------------------------------------------- filters_for_subscriber


def test_filters_for_subscriber_empty():
    reg = DocSubscriptionFilter()
    assert reg.filters_for_subscriber("nobody") == []


def test_filters_for_subscriber_active_only_default():
    reg = DocSubscriptionFilter()
    reg.add_filter(SubFilter(filter_id="on", subscriber_id="s", enabled=True))
    reg.add_filter(SubFilter(filter_id="off", subscriber_id="s", enabled=False))
    ids = [f.filter_id for f in reg.filters_for_subscriber("s")]
    assert ids == ["on"]


def test_filters_for_subscriber_include_disabled():
    reg = DocSubscriptionFilter()
    reg.add_filter(SubFilter(filter_id="on", subscriber_id="s", enabled=True))
    reg.add_filter(SubFilter(filter_id="off", subscriber_id="s", enabled=False))
    ids = {f.filter_id for f in reg.filters_for_subscriber("s", active_only=False)}
    assert ids == {"on", "off"}


def test_filters_for_subscriber_sorted():
    reg = DocSubscriptionFilter()
    reg.add_filter(SubFilter(filter_id="a", subscriber_id="s", priority=1))
    reg.add_filter(SubFilter(filter_id="b", subscriber_id="s", priority=3))
    assert [f.filter_id for f in reg.filters_for_subscriber("s")] == ["b", "a"]


def test_filters_for_subscriber_isolated():
    reg = DocSubscriptionFilter()
    reg.add_filter(SubFilter(filter_id="f1", subscriber_id="alice"))
    reg.add_filter(SubFilter(filter_id="f2", subscriber_id="bob"))
    alice = [f.filter_id for f in reg.filters_for_subscriber("alice")]
    bob = [f.filter_id for f in reg.filters_for_subscriber("bob")]
    assert alice == ["f1"]
    assert bob == ["f2"]


# ----------------------------------------------------------- matches


def test_matches_no_filters_returns_unmatched():
    reg = DocSubscriptionFilter()
    r = reg.matches("s1", "doc1", "created")
    assert r.matched is False
    assert r.matching_filters == []


def test_matches_wildcard_pattern_default():
    reg = DocSubscriptionFilter()
    reg.add_filter(SubFilter(filter_id="f1", subscriber_id="s1"))
    r = reg.matches("s1", "anything", "any-event")
    assert r.matched is True
    assert r.matching_filters == ["f1"]


def test_matches_pattern_specific():
    reg = DocSubscriptionFilter()
    reg.add_filter(
        SubFilter(filter_id="f1", subscriber_id="s1", doc_pattern="docs/*.md")
    )
    assert reg.matches("s1", "docs/readme.md", "x").matched is True
    assert reg.matches("s1", "src/main.py", "x").matched is False


def test_matches_event_type_whitelist():
    reg = DocSubscriptionFilter()
    reg.add_filter(
        SubFilter(filter_id="f1", subscriber_id="s1", event_types=["created"])
    )
    assert reg.matches("s1", "d", "created").matched is True
    assert reg.matches("s1", "d", "deleted").matched is False


def test_matches_event_type_empty_allows_all():
    reg = DocSubscriptionFilter()
    reg.add_filter(SubFilter(filter_id="f1", subscriber_id="s1", event_types=[]))
    assert reg.matches("s1", "d", "anything").matched is True


def test_matches_disabled_filter_excluded():
    reg = DocSubscriptionFilter()
    reg.add_filter(SubFilter(filter_id="f1", subscriber_id="s1", enabled=False))
    assert reg.matches("s1", "d", "x").matched is False


def test_matches_other_subscriber_excluded():
    reg = DocSubscriptionFilter()
    reg.add_filter(SubFilter(filter_id="f1", subscriber_id="alice"))
    assert reg.matches("bob", "d", "x").matched is False


def test_matches_multiple_filters_ordered_by_priority():
    reg = DocSubscriptionFilter()
    reg.add_filter(SubFilter(filter_id="low", subscriber_id="s", priority=1))
    reg.add_filter(SubFilter(filter_id="high", subscriber_id="s", priority=10))
    reg.add_filter(SubFilter(filter_id="mid", subscriber_id="s", priority=5))
    r = reg.matches("s", "d", "x")
    assert r.matching_filters == ["high", "mid", "low"]


def test_matches_tie_priority_ordered_by_id():
    reg = DocSubscriptionFilter()
    reg.add_filter(SubFilter(filter_id="b", subscriber_id="s", priority=1))
    reg.add_filter(SubFilter(filter_id="a", subscriber_id="s", priority=1))
    r = reg.matches("s", "d", "x")
    assert r.matching_filters == ["a", "b"]


def test_matches_increments_evaluation_counter_when_no_filters():
    reg = DocSubscriptionFilter()
    reg.matches("s", "d", "x")
    reg.matches("s", "d", "x")
    assert reg.stats().total_evaluations == 2
    assert reg.stats().total_matches == 0


def test_matches_increments_match_counter_only_when_matched():
    reg = DocSubscriptionFilter()
    reg.add_filter(SubFilter(filter_id="f1", subscriber_id="s1"))
    reg.matches("s1", "d", "x")  # match
    reg.matches("s2", "d", "x")  # no match
    s = reg.stats()
    assert s.total_evaluations == 2
    assert s.total_matches == 1


def test_matches_pattern_question_mark():
    reg = DocSubscriptionFilter()
    reg.add_filter(SubFilter(filter_id="f1", subscriber_id="s", doc_pattern="doc?"))
    assert reg.matches("s", "doc1", "x").matched is True
    assert reg.matches("s", "doc12", "x").matched is False


def test_matches_pattern_is_case_sensitive():
    reg = DocSubscriptionFilter()
    reg.add_filter(SubFilter(filter_id="f1", subscriber_id="s", doc_pattern="DOC*"))
    assert reg.matches("s", "doc1", "x").matched is False
    assert reg.matches("s", "DOC1", "x").matched is True


# ----------------------------------------------------------- would_match


def test_would_match_basic_true():
    reg = DocSubscriptionFilter()
    f = SubFilter(filter_id="f1", subscriber_id="s")
    assert reg.would_match(f, "anything", "ev") is True


def test_would_match_disabled_filter_false():
    reg = DocSubscriptionFilter()
    f = SubFilter(filter_id="f1", subscriber_id="s", enabled=False)
    assert reg.would_match(f, "d", "x") is False


def test_would_match_pattern():
    reg = DocSubscriptionFilter()
    f = SubFilter(filter_id="f1", subscriber_id="s", doc_pattern="logs/*")
    assert reg.would_match(f, "logs/2026.txt", "x") is True
    assert reg.would_match(f, "data/x", "x") is False


def test_would_match_event_types():
    reg = DocSubscriptionFilter()
    f = SubFilter(filter_id="f1", subscriber_id="s", event_types=["updated"])
    assert reg.would_match(f, "d", "updated") is True
    assert reg.would_match(f, "d", "created") is False


def test_would_match_no_side_effects_on_stats():
    reg = DocSubscriptionFilter()
    f = SubFilter(filter_id="f1", subscriber_id="s")
    reg.would_match(f, "d", "x")
    reg.would_match(f, "d", "x")
    s = reg.stats()
    assert s.total_evaluations == 0
    assert s.total_matches == 0


def test_would_match_does_not_register():
    reg = DocSubscriptionFilter()
    f = SubFilter(filter_id="ephemeral", subscriber_id="s")
    reg.would_match(f, "d", "x")
    assert reg.get_filter("ephemeral") is None


def test_would_match_wrong_type():
    reg = DocSubscriptionFilter()
    with pytest.raises(TypeError):
        reg.would_match("not-a-filter", "d", "x")  # type: ignore[arg-type]


# ----------------------------------------------------------- clear_subscriber


def test_clear_subscriber_removes_all_filters():
    reg = DocSubscriptionFilter()
    reg.add_filter(SubFilter(filter_id="f1", subscriber_id="s"))
    reg.add_filter(SubFilter(filter_id="f2", subscriber_id="s"))
    reg.add_filter(SubFilter(filter_id="other", subscriber_id="other"))
    assert reg.clear_subscriber("s") == 2
    assert reg.get_filter("f1") is None
    assert reg.get_filter("f2") is None
    assert reg.get_filter("other") is not None


def test_clear_subscriber_unknown_returns_zero():
    reg = DocSubscriptionFilter()
    assert reg.clear_subscriber("nobody") == 0


def test_clear_subscriber_cleans_index():
    reg = DocSubscriptionFilter()
    reg.add_filter(SubFilter(filter_id="f1", subscriber_id="s"))
    reg.clear_subscriber("s")
    assert reg.filters_for_subscriber("s") == []


# ----------------------------------------------------------- clear_all


def test_clear_all_empty():
    reg = DocSubscriptionFilter()
    assert reg.clear_all() == 0


def test_clear_all_removes_everything():
    reg = DocSubscriptionFilter()
    reg.add_filter(SubFilter(filter_id="f1", subscriber_id="a"))
    reg.add_filter(SubFilter(filter_id="f2", subscriber_id="b"))
    assert reg.clear_all() == 2
    assert reg.list_filters() == []
    assert reg.filters_for_subscriber("a") == []
    assert reg.filters_for_subscriber("b") == []


def test_clear_all_does_not_reset_counters():
    reg = DocSubscriptionFilter()
    reg.add_filter(SubFilter(filter_id="f1", subscriber_id="s"))
    reg.matches("s", "d", "x")
    reg.clear_all()
    s = reg.stats()
    assert s.total_evaluations == 1
    assert s.total_matches == 1


# ----------------------------------------------------------- stats


def test_stats_empty_registry():
    s = DocSubscriptionFilter().stats()
    assert s == SubFilterStats(0, 0, 0, 0)


def test_stats_counts_enabled_only():
    reg = DocSubscriptionFilter()
    reg.add_filter(SubFilter(filter_id="on1", subscriber_id="s"))
    reg.add_filter(SubFilter(filter_id="on2", subscriber_id="s"))
    reg.add_filter(SubFilter(filter_id="off", subscriber_id="s", enabled=False))
    s = reg.stats()
    assert s.total_filters == 3
    assert s.enabled_filters == 2


def test_stats_tracks_evaluations_and_matches():
    reg = DocSubscriptionFilter()
    reg.add_filter(SubFilter(filter_id="f1", subscriber_id="s"))
    reg.matches("s", "d", "x")
    reg.matches("s", "d", "y")
    reg.matches("ghost", "d", "x")
    s = reg.stats()
    assert s.total_evaluations == 3
    assert s.total_matches == 2


# ----------------------------------------------------------- thread safety


def test_thread_safety_add_filters_concurrently():
    reg = DocSubscriptionFilter()

    def worker(start: int) -> None:
        for i in range(start, start + 50):
            reg.add_filter(
                SubFilter(filter_id=f"f{i}", subscriber_id=f"s{i % 5}")
            )

    threads = [threading.Thread(target=worker, args=(i * 50,)) for i in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert reg.stats().total_filters == 200


def test_thread_safety_matches_concurrent_with_adds():
    reg = DocSubscriptionFilter()
    for i in range(20):
        reg.add_filter(SubFilter(filter_id=f"f{i}", subscriber_id="s"))

    stop = threading.Event()

    def adder():
        i = 1000
        while not stop.is_set():
            try:
                reg.add_filter(SubFilter(filter_id=f"x{i}", subscriber_id="s"))
            except ValueError:
                pass
            i += 1

    def matcher():
        for _ in range(200):
            reg.matches("s", "doc", "ev")

    a = threading.Thread(target=adder)
    m = threading.Thread(target=matcher)
    a.start()
    m.start()
    m.join()
    stop.set()
    a.join()

    # Should not have raised; matcher saw 200 evaluations.
    assert reg.stats().total_evaluations >= 200


def test_thread_safety_remove_and_match_concurrent():
    reg = DocSubscriptionFilter()
    for i in range(50):
        reg.add_filter(SubFilter(filter_id=f"f{i}", subscriber_id="s"))

    results: list[int] = []

    def remover():
        for i in range(50):
            reg.remove_filter(f"f{i}")

    def matcher():
        for _ in range(100):
            r = reg.matches("s", "d", "x")
            results.append(len(r.matching_filters))

    threads = [
        threading.Thread(target=remover),
        threading.Thread(target=matcher),
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    # No crashes; results are valid lengths.
    assert all(r >= 0 for r in results)


def test_thread_safety_enable_disable_concurrent():
    reg = DocSubscriptionFilter()
    reg.add_filter(SubFilter(filter_id="f1", subscriber_id="s"))

    def toggler():
        for _ in range(100):
            reg.disable_filter("f1")
            reg.enable_filter("f1")

    threads = [threading.Thread(target=toggler) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    # End state should be enabled (last operation in toggler).
    assert reg.get_filter("f1") is not None


# ----------------------------------------------------------- integration


def test_full_lifecycle():
    reg = DocSubscriptionFilter()
    reg.add_filter(
        SubFilter(
            filter_id="alerts",
            subscriber_id="alice",
            doc_pattern="alerts/*",
            event_types=["created"],
            priority=10,
        )
    )
    reg.add_filter(
        SubFilter(
            filter_id="all-alice",
            subscriber_id="alice",
            doc_pattern="*",
            priority=1,
        )
    )
    reg.add_filter(
        SubFilter(filter_id="bob-md", subscriber_id="bob", doc_pattern="*.md")
    )

    r1 = reg.matches("alice", "alerts/server-down", "created")
    assert r1.matched and r1.matching_filters == ["alerts", "all-alice"]

    r2 = reg.matches("alice", "alerts/server-down", "deleted")
    assert r2.matched and r2.matching_filters == ["all-alice"]

    r3 = reg.matches("bob", "notes.md", "any")
    assert r3.matched and r3.matching_filters == ["bob-md"]

    r4 = reg.matches("bob", "notes.txt", "any")
    assert not r4.matched

    s = reg.stats()
    assert s.total_filters == 3
    assert s.enabled_filters == 3
    assert s.total_evaluations == 4
    assert s.total_matches == 3

    reg.disable_filter("all-alice")
    r5 = reg.matches("alice", "random", "x")
    assert not r5.matched

    assert reg.clear_subscriber("alice") == 2
    assert reg.list_filters() == [reg.get_filter("bob-md")]

    assert reg.clear_all() == 1
    assert reg.stats().total_filters == 0


def test_re_add_after_remove():
    reg = DocSubscriptionFilter()
    reg.add_filter(SubFilter(filter_id="f1", subscriber_id="s"))
    reg.remove_filter("f1")
    # Should be possible to re-register the same id.
    reg.add_filter(SubFilter(filter_id="f1", subscriber_id="s", priority=99))
    assert reg.get_filter("f1").priority == 99


def test_filter_object_mutation_visible_via_get():
    reg = DocSubscriptionFilter()
    f = SubFilter(filter_id="f1", subscriber_id="s")
    reg.add_filter(f)
    f.priority = 42
    assert reg.get_filter("f1").priority == 42
