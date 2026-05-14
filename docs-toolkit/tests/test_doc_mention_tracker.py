"""Tests for E292 DocMentionTracker.

Run with:
    python -m pytest tests/test_doc_mention_tracker.py -q
"""

from __future__ import annotations

import threading
import time

import pytest

from docstoolkit.doc_mention_tracker import (
    DocMentionTracker,
    Mention,
    MentionStats,
)


# ===========================================================================
# Fixtures
# ===========================================================================


@pytest.fixture
def tracker() -> DocMentionTracker:
    return DocMentionTracker()


# ===========================================================================
# add — basic recording
# ===========================================================================


class TestAdd:
    def test_add_returns_mention(self, tracker):
        m = tracker.add("doc1", "alice", "user")
        assert isinstance(m, Mention)

    def test_add_auto_increments_id(self, tracker):
        m1 = tracker.add("doc1", "alice", "user")
        m2 = tracker.add("doc1", "bob", "user")
        assert m2.mention_id == m1.mention_id + 1

    def test_add_id_starts_at_one(self, tracker):
        m = tracker.add("doc1", "alice", "user")
        assert m.mention_id == 1

    def test_add_stores_source_doc(self, tracker):
        m = tracker.add("readme.md", "alice", "user")
        assert m.source_doc == "readme.md"

    def test_add_stores_target(self, tracker):
        m = tracker.add("doc1", "alice", "user")
        assert m.target == "alice"

    def test_add_stores_mention_type(self, tracker):
        m = tracker.add("doc1", "alice", "user")
        assert m.mention_type == "user"

    def test_add_stores_context(self, tracker):
        m = tracker.add("doc1", "alice", "user", context="Hello @alice there")
        assert m.context == "Hello @alice there"

    def test_add_stores_position(self, tracker):
        m = tracker.add("doc1", "alice", "user", position=42)
        assert m.position == 42

    def test_add_default_context_empty(self, tracker):
        m = tracker.add("doc1", "x", "user")
        assert m.context == ""

    def test_add_default_position_zero(self, tracker):
        m = tracker.add("doc1", "x", "user")
        assert m.position == 0

    def test_add_custom_timestamp(self, tracker):
        ts = 1_700_000_000.0
        m = tracker.add("doc1", "x", "user", now=ts)
        assert m.timestamp == ts

    def test_add_default_timestamp_is_recent(self, tracker):
        before = time.time()
        m = tracker.add("doc1", "x", "user")
        after = time.time()
        assert before <= m.timestamp <= after

    def test_add_increments_total_mentions(self, tracker):
        tracker.add("doc1", "alice", "user")
        tracker.add("doc1", "bob", "user")
        assert tracker.total_mentions == 2

    def test_add_doc_type(self, tracker):
        m = tracker.add("doc1", "Architecture", "doc")
        assert m.mention_type == "doc"

    def test_add_tag_type(self, tracker):
        m = tracker.add("doc1", "python", "tag")
        assert m.mention_type == "tag"


# ===========================================================================
# extract_and_add — pattern parsing
# ===========================================================================


class TestExtractAndAdd:
    def test_extract_user_mention(self, tracker):
        mentions = tracker.extract_and_add("doc1", "Hello @alice how are you")
        assert len(mentions) == 1
        assert mentions[0].target == "alice"
        assert mentions[0].mention_type == "user"

    def test_extract_doc_mention(self, tracker):
        mentions = tracker.extract_and_add("doc1", "See [[Architecture]] for details")
        assert len(mentions) == 1
        assert mentions[0].target == "Architecture"
        assert mentions[0].mention_type == "doc"

    def test_extract_doc_multi_word(self, tracker):
        mentions = tracker.extract_and_add("doc1", "Read [[Getting Started Guide]]")
        assert len(mentions) == 1
        assert mentions[0].target == "Getting Started Guide"
        assert mentions[0].mention_type == "doc"

    def test_extract_tag_mention(self, tracker):
        mentions = tracker.extract_and_add("doc1", "This is #python code")
        assert len(mentions) == 1
        assert mentions[0].target == "python"
        assert mentions[0].mention_type == "tag"

    def test_extract_mixed_content(self, tracker):
        content = "@alice look at [[RFC 42]] and tag it #important"
        mentions = tracker.extract_and_add("doc1", content)
        types = {m.mention_type for m in mentions}
        assert types == {"user", "doc", "tag"}

    def test_extract_returns_in_position_order(self, tracker):
        content = "@alice [[Doc]] #tag"
        mentions = tracker.extract_and_add("doc1", content)
        positions = [m.position for m in mentions]
        assert positions == sorted(positions)

    def test_extract_position_is_match_start(self, tracker):
        content = "Hello @alice"
        mentions = tracker.extract_and_add("doc1", content)
        assert mentions[0].position == content.index("@alice")

    def test_extract_context_includes_surrounding(self, tracker):
        content = "Some text before @alice and text after"
        mentions = tracker.extract_and_add("doc1", content)
        assert "before" in mentions[0].context
        assert "after" in mentions[0].context

    def test_extract_context_at_start_of_content(self, tracker):
        content = "@bob is here"
        mentions = tracker.extract_and_add("doc1", content)
        # context should start from position 0, not go negative
        assert mentions[0].context.startswith("@bob")

    def test_extract_context_at_end_of_content(self, tracker):
        content = "Here is @carol"
        mentions = tracker.extract_and_add("doc1", content)
        assert mentions[0].context.endswith("@carol")

    def test_extract_context_max_100_chars(self, tracker):
        prefix = "x" * 80
        suffix = "y" * 80
        content = prefix + "@alice" + suffix
        mentions = tracker.extract_and_add("doc1", content)
        assert len(mentions[0].context) <= 100

    def test_extract_multiple_users(self, tracker):
        content = "@alice and @bob are friends"
        mentions = tracker.extract_and_add("doc1", content)
        targets = {m.target for m in mentions}
        assert targets == {"alice", "bob"}

    def test_extract_empty_content(self, tracker):
        mentions = tracker.extract_and_add("doc1", "")
        assert mentions == []

    def test_extract_no_patterns(self, tracker):
        mentions = tracker.extract_and_add("doc1", "plain text no patterns here")
        assert mentions == []

    def test_extract_assigns_sequential_ids(self, tracker):
        content = "@alice [[Doc]] #tag"
        mentions = tracker.extract_and_add("doc1", content)
        ids = [m.mention_id for m in mentions]
        assert ids == list(range(ids[0], ids[0] + len(ids)))

    def test_extract_stores_source_doc(self, tracker):
        mentions = tracker.extract_and_add("readme.md", "@alice")
        assert all(m.source_doc == "readme.md" for m in mentions)

    def test_extract_custom_timestamp(self, tracker):
        ts = 1_600_000_000.0
        mentions = tracker.extract_and_add("doc1", "@alice", now=ts)
        assert mentions[0].timestamp == ts

    def test_extract_increments_total_mentions(self, tracker):
        tracker.extract_and_add("doc1", "@alice [[Doc]] #tag")
        assert tracker.total_mentions == 3

    def test_extract_doc_with_spaces_in_brackets(self, tracker):
        mentions = tracker.extract_and_add("d", "[[  spaced  ]]")
        # The captured group is everything between [[ and ]], including spaces
        assert mentions[0].target == "  spaced  "


# ===========================================================================
# mentions_of
# ===========================================================================


class TestMentionsOf:
    def test_mentions_of_returns_matching(self, tracker):
        tracker.add("doc1", "alice", "user")
        tracker.add("doc2", "alice", "user")
        result = tracker.mentions_of("alice")
        assert len(result) == 2

    def test_mentions_of_empty_when_unknown(self, tracker):
        assert tracker.mentions_of("ghost") == []

    def test_mentions_of_filtered_by_type(self, tracker):
        tracker.add("doc1", "alice", "user")
        tracker.add("doc2", "alice", "doc")
        result = tracker.mentions_of("alice", mention_type="user")
        assert all(m.mention_type == "user" for m in result)
        assert len(result) == 1

    def test_mentions_of_newest_first(self, tracker):
        tracker.add("doc1", "alice", "user", now=1000.0)
        tracker.add("doc2", "alice", "user", now=2000.0)
        result = tracker.mentions_of("alice")
        assert result[0].timestamp == 2000.0

    def test_mentions_of_does_not_include_other_targets(self, tracker):
        tracker.add("doc1", "alice", "user")
        tracker.add("doc1", "bob", "user")
        result = tracker.mentions_of("alice")
        assert all(m.target == "alice" for m in result)


# ===========================================================================
# mentions_from
# ===========================================================================


class TestMentionsFrom:
    def test_mentions_from_returns_matching(self, tracker):
        tracker.add("doc1", "alice", "user")
        tracker.add("doc1", "bob", "user")
        result = tracker.mentions_from("doc1")
        assert len(result) == 2

    def test_mentions_from_empty_when_unknown_source(self, tracker):
        assert tracker.mentions_from("nonexistent.md") == []

    def test_mentions_from_filtered_by_type(self, tracker):
        tracker.add("doc1", "alice", "user")
        tracker.add("doc1", "Architecture", "doc")
        result = tracker.mentions_from("doc1", mention_type="doc")
        assert len(result) == 1
        assert result[0].mention_type == "doc"

    def test_mentions_from_newest_first(self, tracker):
        tracker.add("doc1", "a", "user", now=500.0)
        tracker.add("doc1", "b", "user", now=600.0)
        result = tracker.mentions_from("doc1")
        assert result[0].timestamp == 600.0

    def test_mentions_from_does_not_include_other_sources(self, tracker):
        tracker.add("doc1", "alice", "user")
        tracker.add("doc2", "alice", "user")
        result = tracker.mentions_from("doc1")
        assert all(m.source_doc == "doc1" for m in result)


# ===========================================================================
# targets_mentioned_by
# ===========================================================================


class TestTargetsMentionedBy:
    def test_targets_mentioned_by_returns_sorted(self, tracker):
        tracker.add("doc1", "charlie", "user")
        tracker.add("doc1", "alice", "user")
        tracker.add("doc1", "bob", "user")
        assert tracker.targets_mentioned_by("doc1") == ["alice", "bob", "charlie"]

    def test_targets_mentioned_by_unique(self, tracker):
        tracker.add("doc1", "alice", "user")
        tracker.add("doc1", "alice", "doc")  # same target, different type
        result = tracker.targets_mentioned_by("doc1")
        assert result.count("alice") == 1

    def test_targets_mentioned_by_empty_for_unknown(self, tracker):
        assert tracker.targets_mentioned_by("unknown.md") == []


# ===========================================================================
# sources_mentioning
# ===========================================================================


class TestSourcesMentioning:
    def test_sources_mentioning_returns_sorted(self, tracker):
        tracker.add("c.md", "alice", "user")
        tracker.add("a.md", "alice", "user")
        tracker.add("b.md", "alice", "user")
        assert tracker.sources_mentioning("alice") == ["a.md", "b.md", "c.md"]

    def test_sources_mentioning_unique(self, tracker):
        tracker.add("doc1", "alice", "user")
        tracker.add("doc1", "alice", "doc")
        result = tracker.sources_mentioning("alice")
        assert result.count("doc1") == 1

    def test_sources_mentioning_empty_for_unknown(self, tracker):
        assert tracker.sources_mentioning("nobody") == []


# ===========================================================================
# top_mentioned
# ===========================================================================


class TestTopMentioned:
    def test_top_mentioned_sorted_by_count_desc(self, tracker):
        for _ in range(3):
            tracker.add("doc1", "alice", "user")
        tracker.add("doc1", "bob", "user")
        result = tracker.top_mentioned()
        assert result[0] == ("alice", 3)
        assert result[1] == ("bob", 1)

    def test_top_mentioned_respects_limit(self, tracker):
        for name in ["a", "b", "c", "d", "e"]:
            tracker.add("doc1", name, "user")
        result = tracker.top_mentioned(limit=3)
        assert len(result) == 3

    def test_top_mentioned_filtered_by_type(self, tracker):
        tracker.add("doc1", "alice", "user")
        tracker.add("doc1", "alice", "user")
        tracker.add("doc1", "alice", "doc")
        result = tracker.top_mentioned(mention_type="user")
        assert result[0] == ("alice", 2)

    def test_top_mentioned_empty_when_no_mentions(self, tracker):
        assert tracker.top_mentioned() == []

    def test_top_mentioned_type_filter_excludes_others(self, tracker):
        tracker.add("doc1", "alpha", "tag")
        tracker.add("doc1", "beta", "user")
        result = tracker.top_mentioned(mention_type="tag")
        targets = [t for t, _ in result]
        assert "beta" not in targets


# ===========================================================================
# delete
# ===========================================================================


class TestDelete:
    def test_delete_returns_true_when_exists(self, tracker):
        m = tracker.add("doc1", "alice", "user")
        assert tracker.delete(m.mention_id) is True

    def test_delete_returns_false_when_not_exists(self, tracker):
        assert tracker.delete(999) is False

    def test_delete_removes_from_total(self, tracker):
        m = tracker.add("doc1", "alice", "user")
        tracker.delete(m.mention_id)
        assert tracker.total_mentions == 0

    def test_delete_removes_from_mentions_of(self, tracker):
        m = tracker.add("doc1", "alice", "user")
        tracker.delete(m.mention_id)
        assert tracker.mentions_of("alice") == []

    def test_delete_removes_from_mentions_from(self, tracker):
        m = tracker.add("doc1", "alice", "user")
        tracker.delete(m.mention_id)
        assert tracker.mentions_from("doc1") == []

    def test_delete_idempotent_second_call(self, tracker):
        m = tracker.add("doc1", "alice", "user")
        tracker.delete(m.mention_id)
        assert tracker.delete(m.mention_id) is False

    def test_delete_does_not_affect_other_mentions(self, tracker):
        m1 = tracker.add("doc1", "alice", "user")
        tracker.add("doc1", "bob", "user")
        tracker.delete(m1.mention_id)
        assert tracker.total_mentions == 1


# ===========================================================================
# clear_source
# ===========================================================================


class TestClearSource:
    def test_clear_source_returns_count(self, tracker):
        tracker.add("doc1", "alice", "user")
        tracker.add("doc1", "bob", "user")
        assert tracker.clear_source("doc1") == 2

    def test_clear_source_returns_zero_for_unknown(self, tracker):
        assert tracker.clear_source("ghost.md") == 0

    def test_clear_source_removes_all_from_source(self, tracker):
        tracker.add("doc1", "alice", "user")
        tracker.add("doc1", "bob", "user")
        tracker.clear_source("doc1")
        assert tracker.mentions_from("doc1") == []

    def test_clear_source_updates_total(self, tracker):
        tracker.add("doc1", "alice", "user")
        tracker.add("doc1", "bob", "user")
        tracker.add("doc2", "carol", "user")
        tracker.clear_source("doc1")
        assert tracker.total_mentions == 1

    def test_clear_source_removes_from_mentions_of(self, tracker):
        tracker.add("doc1", "alice", "user")
        tracker.add("doc2", "alice", "user")
        tracker.clear_source("doc1")
        result = tracker.mentions_of("alice")
        assert all(m.source_doc == "doc2" for m in result)

    def test_clear_source_does_not_affect_other_sources(self, tracker):
        tracker.add("doc1", "alice", "user")
        tracker.add("doc2", "alice", "user")
        tracker.clear_source("doc1")
        assert len(tracker.mentions_from("doc2")) == 1


# ===========================================================================
# stats
# ===========================================================================


class TestStats:
    def test_stats_empty(self, tracker):
        s = tracker.stats()
        assert isinstance(s, MentionStats)
        assert s.total_mentions == 0
        assert s.unique_targets == 0
        assert s.unique_sources == 0
        assert s.type_counts == {}

    def test_stats_total_mentions(self, tracker):
        tracker.add("doc1", "alice", "user")
        tracker.add("doc1", "bob", "user")
        assert tracker.stats().total_mentions == 2

    def test_stats_unique_targets(self, tracker):
        tracker.add("doc1", "alice", "user")
        tracker.add("doc2", "alice", "user")
        tracker.add("doc1", "bob", "user")
        assert tracker.stats().unique_targets == 2

    def test_stats_unique_sources(self, tracker):
        tracker.add("doc1", "alice", "user")
        tracker.add("doc2", "bob", "user")
        tracker.add("doc2", "carol", "user")
        assert tracker.stats().unique_sources == 2

    def test_stats_type_counts(self, tracker):
        tracker.add("doc1", "alice", "user")
        tracker.add("doc1", "bob", "user")
        tracker.add("doc1", "Arch", "doc")
        tracker.add("doc1", "python", "tag")
        s = tracker.stats()
        assert s.type_counts["user"] == 2
        assert s.type_counts["doc"] == 1
        assert s.type_counts["tag"] == 1

    def test_stats_updates_after_delete(self, tracker):
        m = tracker.add("doc1", "alice", "user")
        tracker.delete(m.mention_id)
        assert tracker.stats().total_mentions == 0

    def test_stats_updates_after_clear_source(self, tracker):
        tracker.add("doc1", "alice", "user")
        tracker.add("doc1", "bob", "user")
        tracker.clear_source("doc1")
        s = tracker.stats()
        assert s.total_mentions == 0
        assert s.unique_sources == 0


# ===========================================================================
# total_mentions property
# ===========================================================================


class TestTotalMentions:
    def test_total_mentions_zero_initially(self, tracker):
        assert tracker.total_mentions == 0

    def test_total_mentions_increases_on_add(self, tracker):
        tracker.add("doc1", "x", "user")
        assert tracker.total_mentions == 1

    def test_total_mentions_decreases_on_delete(self, tracker):
        m = tracker.add("doc1", "x", "user")
        tracker.delete(m.mention_id)
        assert tracker.total_mentions == 0


# ===========================================================================
# Thread safety
# ===========================================================================


class TestThreadSafety:
    def test_concurrent_add_no_errors(self, tracker):
        errors: list[Exception] = []

        def worker(doc_id: str) -> None:
            try:
                for i in range(10):
                    tracker.add(doc_id, f"target_{i}", "user")
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=worker, args=(f"doc{n}",)) for n in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors
        assert tracker.total_mentions == 100

    def test_concurrent_extract_and_add_no_errors(self, tracker):
        errors: list[Exception] = []
        content = "@alice [[Doc]] #python"

        def worker(doc_id: str) -> None:
            try:
                tracker.extract_and_add(doc_id, content)
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=worker, args=(f"d{n}",)) for n in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors
        assert tracker.total_mentions == 60  # 3 mentions × 20 docs

    def test_concurrent_reads_and_writes(self, tracker):
        tracker.add("shared", "alice", "user")
        results: list[list] = []

        def reader() -> None:
            for _ in range(50):
                results.append(tracker.mentions_of("alice"))

        def writer() -> None:
            for i in range(10):
                tracker.add(f"doc_{i}", "alice", "user")

        r = threading.Thread(target=reader)
        w = threading.Thread(target=writer)
        r.start()
        w.start()
        r.join()
        w.join()

        assert len(results) == 50

    def test_concurrent_delete_no_errors(self, tracker):
        mention_ids = [tracker.add("doc1", f"t{i}", "user").mention_id for i in range(50)]
        errors: list[Exception] = []

        def deleter(mid: int) -> None:
            try:
                tracker.delete(mid)
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=deleter, args=(mid,)) for mid in mention_ids]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors
        assert tracker.total_mentions == 0
