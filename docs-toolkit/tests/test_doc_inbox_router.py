"""Tests for E423 DocInboxRouter."""
from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_inbox_router import (
    DocInboxRouter,
    RoutedMessage,
    RouterStats,
    RoutingRule,
)


# ---------------------------------------------------------------------------
# Dataclass tests
# ---------------------------------------------------------------------------


def test_routing_rule_defaults():
    rule = RoutingRule(rule_id="r1", pattern="*.md", inbox="default")
    assert rule.priority == 0
    assert rule.stop_on_match is False
    assert rule.enabled is True


def test_routing_rule_custom_values():
    rule = RoutingRule(
        rule_id="r1",
        pattern="foo/*",
        inbox="inbox",
        priority=5,
        stop_on_match=True,
        enabled=False,
    )
    assert rule.priority == 5
    assert rule.stop_on_match is True
    assert rule.enabled is False


def test_routed_message_defaults():
    msg = RoutedMessage(message_id=1, doc_id="d", inbox="i", rule_id="r")
    assert msg.delivered_at == 0.0
    assert msg.payload == {}


def test_routed_message_payload_is_separate_per_instance():
    a = RoutedMessage(message_id=1, doc_id="d", inbox="i", rule_id="r")
    b = RoutedMessage(message_id=2, doc_id="d", inbox="i", rule_id="r")
    a.payload["x"] = 1
    assert b.payload == {}


def test_router_stats_fields():
    s = RouterStats(
        total_rules=1,
        enabled_rules=1,
        total_routings=2,
        total_deliveries=3,
        unique_inboxes=4,
    )
    assert s.total_rules == 1
    assert s.enabled_rules == 1
    assert s.total_routings == 2
    assert s.total_deliveries == 3
    assert s.unique_inboxes == 4


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------


def test_router_initial_state():
    r = DocInboxRouter()
    assert r.list_rules() == []
    assert r.inbox_count() == 0
    stats = r.stats()
    assert stats.total_rules == 0
    assert stats.enabled_rules == 0
    assert stats.total_routings == 0
    assert stats.total_deliveries == 0
    assert stats.unique_inboxes == 0


# ---------------------------------------------------------------------------
# add_rule / get_rule / remove_rule
# ---------------------------------------------------------------------------


def test_add_rule_stores_rule():
    r = DocInboxRouter()
    rule = RoutingRule(rule_id="r1", pattern="*", inbox="all")
    r.add_rule(rule)
    assert r.get_rule("r1") is rule


def test_add_rule_replaces_existing():
    r = DocInboxRouter()
    r.add_rule(RoutingRule(rule_id="r1", pattern="*", inbox="a"))
    r.add_rule(RoutingRule(rule_id="r1", pattern="*", inbox="b"))
    assert r.get_rule("r1").inbox == "b"


def test_add_rule_rejects_non_rule():
    r = DocInboxRouter()
    with pytest.raises(TypeError):
        r.add_rule("not-a-rule")  # type: ignore[arg-type]


def test_get_rule_missing_returns_none():
    r = DocInboxRouter()
    assert r.get_rule("missing") is None


def test_remove_rule_existing_returns_true():
    r = DocInboxRouter()
    r.add_rule(RoutingRule(rule_id="r1", pattern="*", inbox="i"))
    assert r.remove_rule("r1") is True
    assert r.get_rule("r1") is None


def test_remove_rule_missing_returns_false():
    r = DocInboxRouter()
    assert r.remove_rule("absent") is False


# ---------------------------------------------------------------------------
# enable_rule / disable_rule
# ---------------------------------------------------------------------------


def test_enable_rule_returns_true_on_existing():
    r = DocInboxRouter()
    r.add_rule(RoutingRule(rule_id="r1", pattern="*", inbox="i", enabled=False))
    assert r.enable_rule("r1") is True
    assert r.get_rule("r1").enabled is True


def test_enable_rule_returns_false_for_missing():
    r = DocInboxRouter()
    assert r.enable_rule("absent") is False


def test_disable_rule_returns_true_on_existing():
    r = DocInboxRouter()
    r.add_rule(RoutingRule(rule_id="r1", pattern="*", inbox="i"))
    assert r.disable_rule("r1") is True
    assert r.get_rule("r1").enabled is False


def test_disable_rule_returns_false_for_missing():
    r = DocInboxRouter()
    assert r.disable_rule("absent") is False


# ---------------------------------------------------------------------------
# list_rules ordering
# ---------------------------------------------------------------------------


def test_list_rules_sorted_by_priority_desc():
    r = DocInboxRouter()
    r.add_rule(RoutingRule(rule_id="a", pattern="*", inbox="x", priority=1))
    r.add_rule(RoutingRule(rule_id="b", pattern="*", inbox="x", priority=5))
    r.add_rule(RoutingRule(rule_id="c", pattern="*", inbox="x", priority=3))
    order = [rule.rule_id for rule in r.list_rules()]
    assert order == ["b", "c", "a"]


def test_list_rules_ties_broken_by_rule_id_asc():
    r = DocInboxRouter()
    r.add_rule(RoutingRule(rule_id="z", pattern="*", inbox="x", priority=2))
    r.add_rule(RoutingRule(rule_id="a", pattern="*", inbox="x", priority=2))
    r.add_rule(RoutingRule(rule_id="m", pattern="*", inbox="x", priority=2))
    order = [rule.rule_id for rule in r.list_rules()]
    assert order == ["a", "m", "z"]


def test_list_rules_empty():
    assert DocInboxRouter().list_rules() == []


# ---------------------------------------------------------------------------
# route — basic delivery
# ---------------------------------------------------------------------------


def test_route_no_rules_yields_no_messages():
    r = DocInboxRouter()
    assert r.route("doc-1") == []


def test_route_matches_single_rule():
    r = DocInboxRouter()
    r.add_rule(RoutingRule(rule_id="r1", pattern="*.md", inbox="markdown"))
    delivered = r.route("notes.md")
    assert len(delivered) == 1
    msg = delivered[0]
    assert msg.doc_id == "notes.md"
    assert msg.inbox == "markdown"
    assert msg.rule_id == "r1"
    assert msg.message_id == 1


def test_route_no_match_returns_empty():
    r = DocInboxRouter()
    r.add_rule(RoutingRule(rule_id="r1", pattern="*.md", inbox="markdown"))
    assert r.route("notes.txt") == []


def test_route_message_ids_auto_increment():
    r = DocInboxRouter()
    r.add_rule(RoutingRule(rule_id="r1", pattern="*", inbox="all"))
    a = r.route("a")
    b = r.route("b")
    c = r.route("c")
    assert a[0].message_id == 1
    assert b[0].message_id == 2
    assert c[0].message_id == 3


def test_route_multiple_matches_returns_all():
    r = DocInboxRouter()
    r.add_rule(RoutingRule(rule_id="r1", pattern="*", inbox="all", priority=1))
    r.add_rule(RoutingRule(rule_id="r2", pattern="*.md", inbox="markdown", priority=2))
    delivered = r.route("x.md")
    assert len(delivered) == 2
    # Higher priority first.
    assert delivered[0].rule_id == "r2"
    assert delivered[1].rule_id == "r1"


def test_route_stop_on_match_short_circuits():
    r = DocInboxRouter()
    r.add_rule(
        RoutingRule(
            rule_id="r1",
            pattern="*.md",
            inbox="markdown",
            priority=10,
            stop_on_match=True,
        )
    )
    r.add_rule(RoutingRule(rule_id="r2", pattern="*", inbox="all", priority=1))
    delivered = r.route("readme.md")
    assert len(delivered) == 1
    assert delivered[0].rule_id == "r1"


def test_route_stop_on_match_after_lower_priority_match():
    # The stop_on_match rule has lower priority and is reached after another match.
    r = DocInboxRouter()
    r.add_rule(RoutingRule(rule_id="r1", pattern="*", inbox="all", priority=10))
    r.add_rule(
        RoutingRule(
            rule_id="r2",
            pattern="*.md",
            inbox="markdown",
            priority=1,
            stop_on_match=True,
        )
    )
    delivered = r.route("x.md")
    assert [m.rule_id for m in delivered] == ["r1", "r2"]


def test_route_disabled_rule_skipped():
    r = DocInboxRouter()
    r.add_rule(
        RoutingRule(rule_id="r1", pattern="*", inbox="i", enabled=False)
    )
    assert r.route("anything") == []


def test_route_after_enable_works():
    r = DocInboxRouter()
    r.add_rule(RoutingRule(rule_id="r1", pattern="*", inbox="i", enabled=False))
    assert r.route("a") == []
    r.enable_rule("r1")
    assert len(r.route("a")) == 1


def test_route_after_disable_skipped():
    r = DocInboxRouter()
    r.add_rule(RoutingRule(rule_id="r1", pattern="*", inbox="i"))
    r.disable_rule("r1")
    assert r.route("a") == []


def test_route_priority_order_higher_first():
    r = DocInboxRouter()
    r.add_rule(RoutingRule(rule_id="low", pattern="*", inbox="x", priority=1))
    r.add_rule(RoutingRule(rule_id="high", pattern="*", inbox="x", priority=99))
    delivered = r.route("doc")
    assert [m.rule_id for m in delivered] == ["high", "low"]


def test_route_uses_supplied_now():
    r = DocInboxRouter()
    r.add_rule(RoutingRule(rule_id="r1", pattern="*", inbox="i"))
    delivered = r.route("a", now=1234.5)
    assert delivered[0].delivered_at == 1234.5


def test_route_default_now_is_set():
    r = DocInboxRouter()
    r.add_rule(RoutingRule(rule_id="r1", pattern="*", inbox="i"))
    delivered = r.route("a")
    assert delivered[0].delivered_at > 0.0


def test_route_payload_default_empty():
    r = DocInboxRouter()
    r.add_rule(RoutingRule(rule_id="r1", pattern="*", inbox="i"))
    delivered = r.route("a")
    assert delivered[0].payload == {}


def test_route_payload_is_copied():
    r = DocInboxRouter()
    r.add_rule(RoutingRule(rule_id="r1", pattern="*", inbox="i"))
    payload = {"k": 1}
    delivered = r.route("a", payload=payload)
    payload["k"] = 999
    assert delivered[0].payload == {"k": 1}


# ---------------------------------------------------------------------------
# fnmatch pattern coverage
# ---------------------------------------------------------------------------


def test_pattern_star_matches_all():
    r = DocInboxRouter()
    r.add_rule(RoutingRule(rule_id="r1", pattern="*", inbox="i"))
    assert len(r.route("anything")) == 1


def test_pattern_question_mark():
    r = DocInboxRouter()
    r.add_rule(RoutingRule(rule_id="r1", pattern="a?c", inbox="i"))
    assert len(r.route("abc")) == 1
    assert r.route("abbc") == []


def test_pattern_bracket_charset():
    r = DocInboxRouter()
    r.add_rule(RoutingRule(rule_id="r1", pattern="doc[12]", inbox="i"))
    assert len(r.route("doc1")) == 1
    assert len(r.route("doc2")) == 1
    assert r.route("doc3") == []


def test_pattern_case_sensitive():
    r = DocInboxRouter()
    r.add_rule(RoutingRule(rule_id="r1", pattern="ABC", inbox="i"))
    assert len(r.route("ABC")) == 1
    assert r.route("abc") == []


def test_pattern_prefix_match():
    r = DocInboxRouter()
    r.add_rule(RoutingRule(rule_id="r1", pattern="proj/*", inbox="i"))
    assert len(r.route("proj/x")) == 1
    assert r.route("other/x") == []


# ---------------------------------------------------------------------------
# messages_for_inbox
# ---------------------------------------------------------------------------


def test_messages_for_inbox_empty():
    r = DocInboxRouter()
    assert r.messages_for_inbox("any") == []


def test_messages_for_inbox_returns_recent_first():
    r = DocInboxRouter()
    r.add_rule(RoutingRule(rule_id="r1", pattern="*", inbox="i"))
    r.route("a")
    r.route("b")
    r.route("c")
    msgs = r.messages_for_inbox("i")
    assert [m.doc_id for m in msgs] == ["c", "b", "a"]


def test_messages_for_inbox_respects_limit():
    r = DocInboxRouter()
    r.add_rule(RoutingRule(rule_id="r1", pattern="*", inbox="i"))
    for x in "abcd":
        r.route(x)
    msgs = r.messages_for_inbox("i", limit=2)
    assert [m.doc_id for m in msgs] == ["d", "c"]


def test_messages_for_inbox_limit_zero():
    r = DocInboxRouter()
    r.add_rule(RoutingRule(rule_id="r1", pattern="*", inbox="i"))
    r.route("a")
    assert r.messages_for_inbox("i", limit=0) == []


def test_messages_for_inbox_limit_larger_than_count():
    r = DocInboxRouter()
    r.add_rule(RoutingRule(rule_id="r1", pattern="*", inbox="i"))
    r.route("a")
    r.route("b")
    msgs = r.messages_for_inbox("i", limit=99)
    assert len(msgs) == 2


def test_messages_for_inbox_negative_limit_returns_empty():
    r = DocInboxRouter()
    r.add_rule(RoutingRule(rule_id="r1", pattern="*", inbox="i"))
    r.route("a")
    assert r.messages_for_inbox("i", limit=-1) == []


def test_messages_for_inbox_isolated_across_inboxes():
    r = DocInboxRouter()
    r.add_rule(RoutingRule(rule_id="ra", pattern="a*", inbox="A"))
    r.add_rule(RoutingRule(rule_id="rb", pattern="b*", inbox="B"))
    r.route("a1")
    r.route("b1")
    r.route("a2")
    assert [m.doc_id for m in r.messages_for_inbox("A")] == ["a2", "a1"]
    assert [m.doc_id for m in r.messages_for_inbox("B")] == ["b1"]


# ---------------------------------------------------------------------------
# messages_for_doc
# ---------------------------------------------------------------------------


def test_messages_for_doc_returns_recent_first():
    r = DocInboxRouter()
    r.add_rule(RoutingRule(rule_id="r1", pattern="*", inbox="A", priority=1))
    r.add_rule(RoutingRule(rule_id="r2", pattern="*", inbox="B", priority=2))
    r.route("doc")
    msgs = r.messages_for_doc("doc")
    # message ids issued in priority order — r2 first (id=1) then r1 (id=2);
    # recent-first means highest id first: r1 then r2.
    assert [m.rule_id for m in msgs] == ["r1", "r2"]


def test_messages_for_doc_empty():
    r = DocInboxRouter()
    assert r.messages_for_doc("missing") == []


def test_messages_for_doc_filters_by_doc_id():
    r = DocInboxRouter()
    r.add_rule(RoutingRule(rule_id="r1", pattern="*", inbox="i"))
    r.route("a")
    r.route("b")
    assert [m.doc_id for m in r.messages_for_doc("a")] == ["a"]
    assert [m.doc_id for m in r.messages_for_doc("b")] == ["b"]


# ---------------------------------------------------------------------------
# clear_inbox / clear_all_messages
# ---------------------------------------------------------------------------


def test_clear_inbox_returns_count():
    r = DocInboxRouter()
    r.add_rule(RoutingRule(rule_id="r1", pattern="*", inbox="i"))
    r.route("a")
    r.route("b")
    assert r.clear_inbox("i") == 2
    assert r.messages_for_inbox("i") == []


def test_clear_inbox_unknown_returns_zero():
    r = DocInboxRouter()
    assert r.clear_inbox("missing") == 0


def test_clear_inbox_does_not_affect_others():
    r = DocInboxRouter()
    r.add_rule(RoutingRule(rule_id="ra", pattern="a*", inbox="A"))
    r.add_rule(RoutingRule(rule_id="rb", pattern="b*", inbox="B"))
    r.route("a1")
    r.route("b1")
    assert r.clear_inbox("A") == 1
    assert len(r.messages_for_inbox("B")) == 1


def test_clear_all_messages_returns_count():
    r = DocInboxRouter()
    r.add_rule(RoutingRule(rule_id="r1", pattern="*", inbox="i"))
    r.route("a")
    r.route("b")
    assert r.clear_all_messages() == 2
    assert r.messages_for_inbox("i") == []
    assert r.inbox_count() == 0


def test_clear_all_messages_on_empty_returns_zero():
    r = DocInboxRouter()
    assert r.clear_all_messages() == 0


def test_clear_inbox_then_route_again():
    r = DocInboxRouter()
    r.add_rule(RoutingRule(rule_id="r1", pattern="*", inbox="i"))
    r.route("a")
    r.clear_inbox("i")
    r.route("b")
    msgs = r.messages_for_inbox("i")
    assert len(msgs) == 1
    assert msgs[0].doc_id == "b"


# ---------------------------------------------------------------------------
# inbox_count
# ---------------------------------------------------------------------------


def test_inbox_count_initial_zero():
    assert DocInboxRouter().inbox_count() == 0


def test_inbox_count_grows_with_deliveries():
    r = DocInboxRouter()
    r.add_rule(RoutingRule(rule_id="ra", pattern="a*", inbox="A"))
    r.add_rule(RoutingRule(rule_id="rb", pattern="b*", inbox="B"))
    r.add_rule(RoutingRule(rule_id="rc", pattern="c*", inbox="C"))
    r.route("a1")
    assert r.inbox_count() == 1
    r.route("b1")
    assert r.inbox_count() == 2
    r.route("c1")
    assert r.inbox_count() == 3


def test_inbox_count_after_clear_inbox():
    r = DocInboxRouter()
    r.add_rule(RoutingRule(rule_id="ra", pattern="a*", inbox="A"))
    r.add_rule(RoutingRule(rule_id="rb", pattern="b*", inbox="B"))
    r.route("a1")
    r.route("b1")
    assert r.inbox_count() == 2
    r.clear_inbox("A")
    assert r.inbox_count() == 1


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------


def test_stats_total_rules_and_enabled():
    r = DocInboxRouter()
    r.add_rule(RoutingRule(rule_id="r1", pattern="*", inbox="i", enabled=True))
    r.add_rule(RoutingRule(rule_id="r2", pattern="*", inbox="i", enabled=False))
    s = r.stats()
    assert s.total_rules == 2
    assert s.enabled_rules == 1


def test_stats_total_routings_increments():
    r = DocInboxRouter()
    s0 = r.stats()
    assert s0.total_routings == 0
    r.route("a")
    r.route("b")
    s = r.stats()
    assert s.total_routings == 2


def test_stats_total_deliveries_counts_messages():
    r = DocInboxRouter()
    r.add_rule(RoutingRule(rule_id="r1", pattern="*", inbox="A", priority=1))
    r.add_rule(RoutingRule(rule_id="r2", pattern="*", inbox="B", priority=2))
    r.route("doc")  # delivers to both inboxes
    s = r.stats()
    assert s.total_deliveries == 2
    assert s.total_routings == 1


def test_stats_unique_inboxes():
    r = DocInboxRouter()
    r.add_rule(RoutingRule(rule_id="ra", pattern="a*", inbox="A"))
    r.add_rule(RoutingRule(rule_id="rb", pattern="b*", inbox="B"))
    r.route("a1")
    r.route("a2")
    r.route("b1")
    s = r.stats()
    assert s.unique_inboxes == 2


def test_stats_returns_router_stats_instance():
    assert isinstance(DocInboxRouter().stats(), RouterStats)


# ---------------------------------------------------------------------------
# Integration scenarios
# ---------------------------------------------------------------------------


def test_full_lifecycle_scenario():
    r = DocInboxRouter()
    r.add_rule(
        RoutingRule(
            rule_id="urgent",
            pattern="urgent/*",
            inbox="urgent",
            priority=100,
            stop_on_match=True,
        )
    )
    r.add_rule(RoutingRule(rule_id="md", pattern="*.md", inbox="md", priority=10))
    r.add_rule(RoutingRule(rule_id="all", pattern="*", inbox="all", priority=0))

    # urgent/x.md → matches "urgent" (stop_on_match), so only one delivery
    delivered = r.route("urgent/x.md")
    assert [m.inbox for m in delivered] == ["urgent"]

    # plain.md → matches "md" and "all"
    delivered = r.route("plain.md")
    assert [m.inbox for m in delivered] == ["md", "all"]

    # plain.txt → matches "all" only
    delivered = r.route("plain.txt")
    assert [m.inbox for m in delivered] == ["all"]

    s = r.stats()
    assert s.total_rules == 3
    assert s.enabled_rules == 3
    assert s.total_routings == 3
    assert s.total_deliveries == 4
    assert s.unique_inboxes == 3


def test_remove_rule_does_not_affect_existing_messages():
    r = DocInboxRouter()
    r.add_rule(RoutingRule(rule_id="r1", pattern="*", inbox="i"))
    r.route("a")
    r.remove_rule("r1")
    msgs = r.messages_for_inbox("i")
    assert len(msgs) == 1
    assert msgs[0].rule_id == "r1"


def test_message_ids_monotonic_even_after_clear():
    r = DocInboxRouter()
    r.add_rule(RoutingRule(rule_id="r1", pattern="*", inbox="i"))
    r.route("a")  # id=1
    r.route("b")  # id=2
    r.clear_all_messages()
    delivered = r.route("c")  # id=3 — never reused
    assert delivered[0].message_id == 3


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------


def test_thread_safety_concurrent_route():
    r = DocInboxRouter()
    r.add_rule(RoutingRule(rule_id="r1", pattern="*", inbox="i"))

    n_threads = 8
    per_thread = 50

    def worker(idx: int) -> None:
        for j in range(per_thread):
            r.route(f"t{idx}-{j}")

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(n_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    s = r.stats()
    assert s.total_routings == n_threads * per_thread
    assert s.total_deliveries == n_threads * per_thread
    # message_ids should be a contiguous set from 1..N
    msgs = r.messages_for_inbox("i")
    ids = sorted(m.message_id for m in msgs)
    assert ids == list(range(1, n_threads * per_thread + 1))


def test_thread_safety_concurrent_add_and_route():
    r = DocInboxRouter()

    def adder() -> None:
        for i in range(50):
            r.add_rule(RoutingRule(rule_id=f"r{i}", pattern="*", inbox=f"box{i % 5}"))

    def router_fn() -> None:
        for _ in range(50):
            r.route("doc")

    threads = [threading.Thread(target=adder) for _ in range(2)] + [
        threading.Thread(target=router_fn) for _ in range(2)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # Should not crash; stats should be consistent.
    s = r.stats()
    assert s.total_rules == 50
    assert s.total_routings == 100
    assert s.total_deliveries >= 0


def test_thread_safety_concurrent_clear_and_route():
    r = DocInboxRouter()
    r.add_rule(RoutingRule(rule_id="r1", pattern="*", inbox="i"))

    stop = threading.Event()

    def router_fn() -> None:
        while not stop.is_set():
            r.route("doc")

    def clearer() -> None:
        for _ in range(20):
            r.clear_inbox("i")

    workers = [threading.Thread(target=router_fn) for _ in range(3)]
    for t in workers:
        t.start()
    clear_t = threading.Thread(target=clearer)
    clear_t.start()
    clear_t.join()
    stop.set()
    for t in workers:
        t.join()

    # Final consistency: messages remaining match by_inbox bookkeeping.
    msgs = r.messages_for_inbox("i")
    # No crashes; sanity: all messages reported are addressed to inbox "i".
    assert all(m.inbox == "i" for m in msgs)
