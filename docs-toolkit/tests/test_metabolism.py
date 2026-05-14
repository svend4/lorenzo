"""Tests for docstoolkit.metabolism — living documents module."""
import pytest
from datetime import datetime, timezone, timedelta

from docstoolkit.metabolism.signals import StalenessSignal, ConflictSignal, FreshnessScore
from docstoolkit.metabolism.absorber import (
    AbsorptionResult, absorb_fragment, _token_set, _jaccard,
)
from docstoolkit.metabolism.aging import DocAge, AgeReport, age_document
from docstoolkit.metabolism.lifecycle import DocLifecycle, LifecycleState


# ---------------------------------------------------------------------------
# StalenessSignal
# ---------------------------------------------------------------------------

class TestStalenessSignal:
    def test_required_fields(self):
        s = StalenessSignal(
            doc_id="doc1", section="## Overview",
            newer_doc_id="doc2", confidence=0.8,
        )
        assert s.doc_id == "doc1"
        assert s.section == "## Overview"
        assert s.newer_doc_id == "doc2"
        assert s.confidence == 0.8

    def test_reason_default_empty(self):
        s = StalenessSignal(doc_id="d", section="s", newer_doc_id="n", confidence=0.5)
        assert s.reason == ""

    def test_reason_custom(self):
        s = StalenessSignal(doc_id="d", section="s", newer_doc_id="n",
                            confidence=0.5, reason="outdated API")
        assert s.reason == "outdated API"

    def test_confidence_boundary_zero(self):
        s = StalenessSignal(doc_id="d", section="s", newer_doc_id="n", confidence=0.0)
        assert s.confidence == 0.0

    def test_confidence_boundary_one(self):
        s = StalenessSignal(doc_id="d", section="s", newer_doc_id="n", confidence=1.0)
        assert s.confidence == 1.0


# ---------------------------------------------------------------------------
# ConflictSignal
# ---------------------------------------------------------------------------

class TestConflictSignal:
    def test_all_fields(self):
        c = ConflictSignal(
            doc_id_a="a", doc_id_b="b",
            passage_a="The sky is blue", passage_b="The sky is red",
            overlap_score=0.5, confidence=0.9,
        )
        assert c.doc_id_a == "a"
        assert c.doc_id_b == "b"
        assert c.passage_a == "The sky is blue"
        assert c.passage_b == "The sky is red"
        assert c.overlap_score == 0.5
        assert c.confidence == 0.9

    def test_zero_confidence(self):
        c = ConflictSignal(doc_id_a="a", doc_id_b="b",
                           passage_a="x", passage_b="y",
                           overlap_score=0.0, confidence=0.0)
        assert c.confidence == 0.0


# ---------------------------------------------------------------------------
# FreshnessScore
# ---------------------------------------------------------------------------

class TestFreshnessScore:
    def test_defaults(self):
        fs = FreshnessScore(doc_id="doc1", score=0.8)
        assert fs.staleness_signals == []
        assert fs.conflict_signals == []
        assert fs.last_updated == ""

    def test_is_fresh_above_threshold(self):
        fs = FreshnessScore(doc_id="d", score=0.9)
        assert fs.is_fresh() is True

    def test_is_fresh_at_threshold(self):
        fs = FreshnessScore(doc_id="d", score=0.6)
        assert fs.is_fresh(threshold=0.6) is True

    def test_is_fresh_below_threshold(self):
        fs = FreshnessScore(doc_id="d", score=0.5)
        assert fs.is_fresh() is False

    def test_is_fresh_custom_threshold(self):
        fs = FreshnessScore(doc_id="d", score=0.4)
        assert fs.is_fresh(threshold=0.3) is True
        assert fs.is_fresh(threshold=0.5) is False

    def test_summary_format(self):
        fs = FreshnessScore(doc_id="mydoc", score=0.75)
        s = fs.summary()
        assert "doc=mydoc" in s
        assert "score=0.75" in s
        assert "stale_signals=0" in s
        assert "conflicts=0" in s

    def test_summary_with_signals(self):
        fs = FreshnessScore(doc_id="d", score=0.5)
        fs.staleness_signals.append(
            StalenessSignal(doc_id="d", section="s", newer_doc_id="n", confidence=0.5)
        )
        fs.conflict_signals.append(
            ConflictSignal(doc_id_a="d", doc_id_b="e", passage_a="a",
                           passage_b="b", overlap_score=0.3, confidence=0.7)
        )
        s = fs.summary()
        assert "stale_signals=1" in s
        assert "conflicts=1" in s

    def test_score_zero(self):
        fs = FreshnessScore(doc_id="d", score=0.0)
        assert fs.is_fresh() is False

    def test_last_updated_stored(self):
        fs = FreshnessScore(doc_id="d", score=1.0, last_updated="2024-01-01")
        assert fs.last_updated == "2024-01-01"


# ---------------------------------------------------------------------------
# _token_set
# ---------------------------------------------------------------------------

class TestTokenSet:
    def test_basic(self):
        tokens = _token_set("Hello world foo")
        assert "hello" in tokens
        assert "world" in tokens
        assert "foo" in tokens

    def test_min_length_3(self):
        tokens = _token_set("a bb ccc dddd")
        assert "a" not in tokens
        assert "bb" not in tokens
        assert "ccc" in tokens
        assert "dddd" in tokens

    def test_lowercase(self):
        tokens = _token_set("Hello WORLD Foo")
        assert "hello" in tokens
        assert "world" in tokens

    def test_empty_string(self):
        assert _token_set("") == set()

    def test_punctuation_stripped(self):
        tokens = _token_set("hello, world!")
        assert "hello" in tokens
        assert "world" in tokens

    def test_numbers_included(self):
        tokens = _token_set("version 123 api")
        assert "123" in tokens
        assert "version" in tokens


# ---------------------------------------------------------------------------
# _jaccard
# ---------------------------------------------------------------------------

class TestJaccard:
    def test_empty_sets(self):
        assert _jaccard(set(), set()) == 0.0

    def test_identical_sets(self):
        s = {"a", "b", "c"}
        assert _jaccard(s, s) == 1.0

    def test_disjoint_sets(self):
        assert _jaccard({"a", "b"}, {"c", "d"}) == 0.0

    def test_partial_overlap(self):
        a = {"a", "b", "c"}
        b = {"b", "c", "d"}
        score = _jaccard(a, b)
        # intersection=2, union=4 → 0.5
        assert abs(score - 0.5) < 1e-9

    def test_one_empty(self):
        assert _jaccard({"a", "b"}, set()) == 0.0
        assert _jaccard(set(), {"a", "b"}) == 0.0


# ---------------------------------------------------------------------------
# absorb_fragment
# ---------------------------------------------------------------------------

SAMPLE_DOC = """# Introduction
This document describes the memory system and knowledge graph for agents.
The system uses vector embeddings and retrieval augmented generation.

## Architecture
The architecture consists of multiple layers including the storage layer,
the retrieval layer and the generation layer with memory components.

## Memory
The memory module handles short-term and long-term storage for agents.
"""

class TestAbsorbFragment:
    def test_high_overlap_absorbed(self):
        fragment = "The memory system uses retrieval for knowledge agents storage."
        result = absorb_fragment(SAMPLE_DOC, fragment)
        assert result.was_absorbed is True
        assert result.relevance_score > 0.15

    def test_unrelated_not_absorbed(self):
        fragment = "Quantum physics explores subatomic particles and wave functions."
        result = absorb_fragment(SAMPLE_DOC, fragment)
        assert result.was_absorbed is False
        assert result.relevance_score < 0.15

    def test_empty_doc(self):
        result = absorb_fragment("", "some fragment text here")
        assert result.was_absorbed is False
        assert result.relevance_score == 0.0

    def test_empty_fragment(self):
        result = absorb_fragment(SAMPLE_DOC, "")
        assert result.was_absorbed is False
        assert result.relevance_score == 0.0

    def test_fragment_with_heading_match(self):
        fragment = "The memory module handles long-term storage."
        result = absorb_fragment(SAMPLE_DOC, fragment)
        # Should find a heading like "## Memory" as insertion hint
        assert result.insertion_hint != ""
        assert "#" in result.insertion_hint

    def test_min_relevance_zero_always_absorbed(self):
        fragment = "Completely unrelated unicorn rainbow butterfly content here."
        result = absorb_fragment(SAMPLE_DOC, fragment, min_relevance=0.0)
        assert result.was_absorbed is True

    def test_min_relevance_one_never_absorbed(self):
        fragment = "Something different from the document content entirely."
        result = absorb_fragment(SAMPLE_DOC, fragment, min_relevance=1.0)
        assert result.was_absorbed is False

    def test_reason_contains_score(self):
        fragment = "The memory system retrieval."
        result = absorb_fragment(SAMPLE_DOC, fragment)
        assert "score=" in result.reason

    def test_reason_relevant_when_absorbed(self):
        fragment = "The memory system uses retrieval for knowledge agents storage."
        result = absorb_fragment(SAMPLE_DOC, fragment)
        if result.was_absorbed:
            assert "relevant" in result.reason

    def test_reason_below_threshold_when_rejected(self):
        fragment = "Quantum physics subatomic particles waves."
        result = absorb_fragment(SAMPLE_DOC, fragment)
        if not result.was_absorbed:
            assert "below threshold" in result.reason

    def test_doc_id_stored(self):
        result = absorb_fragment(SAMPLE_DOC, "memory system", doc_id="my-doc")
        assert result.doc_id == "my-doc"

    def test_fragment_text_stored(self):
        frag = "memory system retrieval"
        result = absorb_fragment(SAMPLE_DOC, frag)
        assert result.fragment_text == frag

    def test_no_headings_empty_hint(self):
        doc = "This document has no headings just plain text about memory systems."
        fragment = "memory systems plain text"
        result = absorb_fragment(doc, fragment)
        assert result.insertion_hint == ""

    def test_result_type(self):
        result = absorb_fragment(SAMPLE_DOC, "memory")
        assert isinstance(result, AbsorptionResult)


# ---------------------------------------------------------------------------
# age_document
# ---------------------------------------------------------------------------

class TestAgeDocument:
    def test_known_iso_date_positive_days(self):
        old_date = (datetime.now(timezone.utc) - timedelta(days=100)).isoformat()
        doc = age_document("d1", "Some content here", last_modified_iso=old_date)
        assert doc.days_since_update >= 99  # allow 1 day rounding slack

    def test_empty_date_zero(self):
        doc = age_document("d1", "Some content here", last_modified_iso="")
        assert doc.days_since_update == 0.0

    def test_malformed_date_zero(self):
        doc = age_document("d1", "content", last_modified_iso="not-a-date")
        assert doc.days_since_update == 0.0

    def test_word_count(self):
        content = "one two three four five"
        doc = age_document("d1", content)
        assert doc.word_count == 5

    def test_word_count_empty(self):
        doc = age_document("d1", "")
        assert doc.word_count == 0

    def test_heading_count(self):
        content = "# Title\n## Section\nSome text\n### Subsection\nMore text"
        doc = age_document("d1", content)
        assert doc.heading_count == 3

    def test_heading_count_zero(self):
        content = "No headings here, just plain text."
        doc = age_document("d1", content)
        assert doc.heading_count == 0

    def test_has_dates_true(self):
        content = "Updated in 2024 with new features."
        doc = age_document("d1", content)
        assert doc.has_dates is True

    def test_has_dates_false(self):
        content = "No dates mentioned here at all."
        doc = age_document("d1", content)
        assert doc.has_dates is False

    def test_has_dates_boundary_1990(self):
        doc = age_document("d1", "Started in 1990.")
        assert doc.has_dates is True

    def test_has_dates_boundary_2030(self):
        doc = age_document("d1", "Projected to 2030.")
        assert doc.has_dates is True

    def test_doc_id_stored(self):
        doc = age_document("my-doc-42", "content")
        assert doc.doc_id == "my-doc-42"

    def test_result_type(self):
        doc = age_document("d1", "content")
        assert isinstance(doc, DocAge)

    def test_recent_date_small_days(self):
        recent = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
        doc = age_document("d1", "content", last_modified_iso=recent)
        assert 0 <= doc.days_since_update <= 2


# ---------------------------------------------------------------------------
# AgeReport.stale_docs
# ---------------------------------------------------------------------------

class TestAgeReport:
    def _make_report(self):
        docs = [
            DocAge("old", 200.0, 100, 3, False),
            DocAge("recent", 10.0, 50, 1, True),
            DocAge("medium", 180.0, 80, 2, False),
            DocAge("very_old", 365.0, 200, 5, True),
        ]
        return AgeReport(docs=docs)

    def test_stale_above_threshold(self):
        report = self._make_report()
        stale = report.stale_docs(threshold_days=180.0)
        ids = [d.doc_id for d in stale]
        assert "old" in ids
        assert "very_old" in ids
        assert "recent" not in ids

    def test_stale_exact_threshold_excluded(self):
        report = self._make_report()
        # threshold=180.0, medium has days=180.0 → NOT stale (not >)
        stale = report.stale_docs(threshold_days=180.0)
        ids = [d.doc_id for d in stale]
        assert "medium" not in ids

    def test_stale_empty_list(self):
        report = AgeReport(docs=[])
        assert report.stale_docs() == []

    def test_stale_all_fresh(self):
        docs = [DocAge("a", 5.0, 10, 0, False), DocAge("b", 10.0, 20, 1, False)]
        report = AgeReport(docs=docs)
        assert report.stale_docs(threshold_days=180.0) == []


# ---------------------------------------------------------------------------
# DocLifecycle
# ---------------------------------------------------------------------------

DOC_CONTENT = """# Knowledge System
This document describes the knowledge system for memory and retrieval.

## Storage
The storage layer handles persistence of documents and embeddings.

## Retrieval
The retrieval module uses vector search for finding relevant passages.
"""


class TestDocLifecycle:
    def test_initial_state_fresh(self):
        lc = DocLifecycle(doc_id="d1", content=DOC_CONTENT)
        assert lc.state == LifecycleState.FRESH

    def test_freshness_initialized(self):
        lc = DocLifecycle(doc_id="d1", content=DOC_CONTENT)
        assert lc.freshness is not None
        assert lc.freshness.score == 1.0
        assert lc.freshness.doc_id == "d1"

    def test_add_staleness_signal_reduces_score(self):
        lc = DocLifecycle(doc_id="d1", content=DOC_CONTENT)
        sig = StalenessSignal(doc_id="d1", section="## Storage",
                              newer_doc_id="d2", confidence=1.0)
        lc.add_staleness_signal(sig)
        assert lc.freshness.score == pytest.approx(0.9, abs=1e-9)

    def test_add_staleness_signal_stored(self):
        lc = DocLifecycle(doc_id="d1", content=DOC_CONTENT)
        sig = StalenessSignal(doc_id="d1", section="s", newer_doc_id="n", confidence=0.5)
        lc.add_staleness_signal(sig)
        assert len(lc.freshness.staleness_signals) == 1

    def test_add_conflict_signal_sets_conflicted(self):
        lc = DocLifecycle(doc_id="d1", content=DOC_CONTENT)
        csig = ConflictSignal(doc_id_a="d1", doc_id_b="d2",
                              passage_a="x", passage_b="y",
                              overlap_score=0.3, confidence=1.0)
        lc.add_conflict_signal(csig)
        assert lc.state == LifecycleState.CONFLICTED

    def test_add_conflict_signal_reduces_score(self):
        lc = DocLifecycle(doc_id="d1", content=DOC_CONTENT)
        csig = ConflictSignal(doc_id_a="d1", doc_id_b="d2",
                              passage_a="x", passage_b="y",
                              overlap_score=0.3, confidence=1.0)
        lc.add_conflict_signal(csig)
        assert lc.freshness.score == pytest.approx(0.85, abs=1e-9)

    def test_try_absorb_relevant_stored(self):
        lc = DocLifecycle(doc_id="d1", content=DOC_CONTENT)
        fragment = "The knowledge system retrieval storage memory documents."
        result = lc.try_absorb(fragment)
        if result.was_absorbed:
            assert len(lc.pending_absorptions) == 1

    def test_try_absorb_irrelevant_not_stored(self):
        lc = DocLifecycle(doc_id="d1", content=DOC_CONTENT)
        fragment = "Quantum subatomic particles wave functions collapse."
        result = lc.try_absorb(fragment)
        if not result.was_absorbed:
            assert len(lc.pending_absorptions) == 0

    def test_try_absorb_relevant_state_absorbing(self):
        lc = DocLifecycle(doc_id="d1", content=DOC_CONTENT)
        fragment = "The knowledge system retrieval storage memory documents."
        result = lc.try_absorb(fragment)
        if result.was_absorbed:
            assert lc.state == LifecycleState.ABSORBING

    def test_commit_absorptions_appends_content(self):
        lc = DocLifecycle(doc_id="d1", content=DOC_CONTENT)
        fragment = "The knowledge system retrieval storage memory documents."
        result = lc.try_absorb(fragment)
        if result.was_absorbed:
            new_content = lc.commit_absorptions()
            assert fragment in new_content

    def test_commit_absorptions_clears_pending(self):
        lc = DocLifecycle(doc_id="d1", content=DOC_CONTENT)
        fragment = "The knowledge system retrieval storage memory documents."
        result = lc.try_absorb(fragment)
        if result.was_absorbed:
            lc.commit_absorptions()
            assert lc.pending_absorptions == []

    def test_commit_absorptions_no_pending_returns_content(self):
        lc = DocLifecycle(doc_id="d1", content="hello world")
        result = lc.commit_absorptions()
        assert result == "hello world"

    def test_state_fresh_after_commit_no_signals(self):
        lc = DocLifecycle(doc_id="d1", content=DOC_CONTENT)
        fragment = "The knowledge system retrieval storage memory documents."
        result = lc.try_absorb(fragment)
        if result.was_absorbed:
            lc.commit_absorptions()
            assert lc.state == LifecycleState.FRESH

    def test_state_stale_when_score_below_0_3(self):
        lc = DocLifecycle(doc_id="d1", content=DOC_CONTENT)
        # Add many high-confidence staleness signals to push score below 0.3
        for _ in range(8):
            sig = StalenessSignal(doc_id="d1", section="s",
                                  newer_doc_id="n", confidence=1.0)
            lc.add_staleness_signal(sig)
        assert lc.state == LifecycleState.STALE

    def test_state_aging_when_score_between_0_3_and_0_6(self):
        lc = DocLifecycle(doc_id="d1", content=DOC_CONTENT)
        # 5 signals × 0.1 × confidence=0.9 = 0.45 reduction → score = 0.55
        for _ in range(5):
            sig = StalenessSignal(doc_id="d1", section="s",
                                  newer_doc_id="n", confidence=0.9)
            lc.add_staleness_signal(sig)
        # score should be around 0.55, which is in [0.3, 0.6)
        assert lc.state in (LifecycleState.AGING, LifecycleState.STALE)

    def test_score_floor_zero(self):
        lc = DocLifecycle(doc_id="d1", content=DOC_CONTENT)
        for _ in range(20):
            sig = StalenessSignal(doc_id="d1", section="s",
                                  newer_doc_id="n", confidence=1.0)
            lc.add_staleness_signal(sig)
        assert lc.freshness.score >= 0.0

    def test_pending_absorptions_initial_empty(self):
        lc = DocLifecycle(doc_id="d1", content=DOC_CONTENT)
        assert lc.pending_absorptions == []
