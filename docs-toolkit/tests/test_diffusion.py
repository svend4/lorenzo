"""Tests for docstoolkit.diffusion — 60+ tests covering all components."""
import pytest

from docstoolkit.diffusion.alignment import (
    ConceptAlignment,
    AlignmentResult,
    align_corpora,
    _token_set,
    _jaccard,
)
from docstoolkit.diffusion.transfer import (
    TransferRecord,
    TransferReport,
    DiffusionTransfer,
)
from docstoolkit.diffusion.provenance import (
    DiffusionProvenance,
    trace_origin,
)


# ---------------------------------------------------------------------------
# ConceptAlignment fields and defaults
# ---------------------------------------------------------------------------

class TestConceptAlignment:
    def test_fields_set_correctly(self):
        ca = ConceptAlignment(
            concept="memory",
            doc_id_a="doc1",
            doc_id_b="doc2",
            similarity=0.5,
            aligned=True,
        )
        assert ca.concept == "memory"
        assert ca.doc_id_a == "doc1"
        assert ca.doc_id_b == "doc2"
        assert ca.similarity == 0.5
        assert ca.aligned is True

    def test_aligned_false(self):
        ca = ConceptAlignment(
            concept="agent",
            doc_id_a="a",
            doc_id_b="b",
            similarity=0.05,
            aligned=False,
        )
        assert ca.aligned is False

    def test_similarity_zero(self):
        ca = ConceptAlignment("word", "a", "b", 0.0, False)
        assert ca.similarity == 0.0

    def test_similarity_one(self):
        ca = ConceptAlignment("word", "a", "b", 1.0, True)
        assert ca.similarity == 1.0


# ---------------------------------------------------------------------------
# AlignmentResult
# ---------------------------------------------------------------------------

class TestAlignmentResult:
    def test_defaults(self):
        ar = AlignmentResult()
        assert ar.alignments == []
        assert ar.corpus_a_size == 0
        assert ar.corpus_b_size == 0
        assert ar.aligned_count == 0

    def test_alignment_rate_empty(self):
        ar = AlignmentResult()
        assert ar.alignment_rate() == 0.0

    def test_alignment_rate_all_aligned(self):
        ca = ConceptAlignment("x", "a", "b", 0.5, True)
        ar = AlignmentResult(alignments=[ca, ca], aligned_count=2)
        assert ar.alignment_rate() == 1.0

    def test_alignment_rate_half_aligned(self):
        ca1 = ConceptAlignment("x", "a", "b", 0.5, True)
        ca2 = ConceptAlignment("y", "a", "b", 0.1, False)
        ar = AlignmentResult(alignments=[ca1, ca2], aligned_count=1)
        assert ar.alignment_rate() == 0.5

    def test_alignment_rate_none_aligned(self):
        ca = ConceptAlignment("x", "a", "b", 0.05, False)
        ar = AlignmentResult(alignments=[ca], aligned_count=0)
        assert ar.alignment_rate() == 0.0

    def test_best_alignments_sorted_desc(self):
        ca1 = ConceptAlignment("x", "a", "b", 0.3, True)
        ca2 = ConceptAlignment("y", "a", "b", 0.8, True)
        ca3 = ConceptAlignment("z", "a", "b", 0.5, True)
        ar = AlignmentResult(alignments=[ca1, ca2, ca3], aligned_count=3)
        best = ar.best_alignments(top_n=3)
        assert best[0].similarity == 0.8
        assert best[1].similarity == 0.5
        assert best[2].similarity == 0.3

    def test_best_alignments_respects_top_n(self):
        alignments = [
            ConceptAlignment(f"c{i}", "a", "b", float(i) / 10, True)
            for i in range(10)
        ]
        ar = AlignmentResult(alignments=alignments, aligned_count=10)
        best = ar.best_alignments(top_n=3)
        assert len(best) == 3

    def test_best_alignments_default_top_n(self):
        alignments = [
            ConceptAlignment(f"c{i}", "a", "b", float(i) / 10, True)
            for i in range(10)
        ]
        ar = AlignmentResult(alignments=alignments, aligned_count=10)
        best = ar.best_alignments()
        assert len(best) == 5

    def test_best_alignments_fewer_than_top_n(self):
        ca = ConceptAlignment("x", "a", "b", 0.5, True)
        ar = AlignmentResult(alignments=[ca], aligned_count=1)
        best = ar.best_alignments(top_n=10)
        assert len(best) == 1


# ---------------------------------------------------------------------------
# align_corpora
# ---------------------------------------------------------------------------

CORPUS_A = {
    "doc1": (
        "Memory systems store information persistently across sessions. "
        "Knowledge retrieval helps agents find relevant data quickly."
    ),
    "doc2": (
        "Agent frameworks coordinate multiple workers. "
        "Planning modules decompose complex tasks into smaller steps."
    ),
}

CORPUS_B = {
    "docX": (
        "Memory storage allows persistent information retrieval for agents. "
        "Sessions benefit from retained knowledge."
    ),
    "docY": (
        "Coordination of worker agents is essential for distributed planning. "
        "Complex task decomposition requires frameworks."
    ),
}


class TestAlignCorpora:
    def test_returns_alignment_result(self):
        result = align_corpora(CORPUS_A, CORPUS_B)
        assert isinstance(result, AlignmentResult)

    def test_corpus_sizes_set(self):
        result = align_corpora(CORPUS_A, CORPUS_B)
        assert result.corpus_a_size == 2
        assert result.corpus_b_size == 2

    def test_empty_corpus_a(self):
        result = align_corpora({}, CORPUS_B)
        assert result.alignments == []
        assert result.aligned_count == 0

    def test_empty_corpus_b(self):
        result = align_corpora(CORPUS_A, {})
        assert result.alignments == []
        assert result.aligned_count == 0

    def test_both_empty(self):
        result = align_corpora({}, {})
        assert result.alignments == []

    def test_overlapping_text_produces_aligned(self):
        ca = {"doc1": "memory knowledge retrieval system agent persistent data"}
        cb = {"docX": "memory knowledge retrieval system agent persistent data"}
        result = align_corpora(ca, cb, threshold=0.15)
        assert result.aligned_count > 0

    def test_threshold_1_no_alignments(self):
        result = align_corpora(CORPUS_A, CORPUS_B, threshold=1.0)
        assert result.aligned_count == 0

    def test_threshold_0_all_aligned(self):
        result = align_corpora(CORPUS_A, CORPUS_B, threshold=0.0)
        assert result.aligned_count == len(result.alignments)

    def test_alignments_similarity_in_range(self):
        result = align_corpora(CORPUS_A, CORPUS_B)
        for a in result.alignments:
            assert 0.0 <= a.similarity <= 1.0

    def test_alignment_rate_le_1(self):
        result = align_corpora(CORPUS_A, CORPUS_B)
        assert result.alignment_rate() <= 1.0

    def test_no_duplicate_alignments(self):
        result = align_corpora(CORPUS_A, CORPUS_B)
        keys = [(a.concept, a.doc_id_a, a.doc_id_b) for a in result.alignments]
        assert len(keys) == len(set(keys))

    def test_aligned_flag_matches_threshold(self):
        result = align_corpora(CORPUS_A, CORPUS_B, threshold=0.15)
        for a in result.alignments:
            if a.similarity >= 0.15:
                assert a.aligned is True
            else:
                assert a.aligned is False

    def test_single_doc_corpora(self):
        ca = {"a": "retrieval system stores documents efficiently"}
        cb = {"b": "retrieval system stores documents efficiently"}
        result = align_corpora(ca, cb, threshold=0.1)
        assert result.corpus_a_size == 1
        assert result.corpus_b_size == 1
        assert result.aligned_count > 0


# ---------------------------------------------------------------------------
# _token_set
# ---------------------------------------------------------------------------

class TestTokenSet:
    def test_filters_short_words(self):
        ts = _token_set("the cat sat on the mat")
        # all words are <= 3 chars, so none qualify
        assert ts == set()

    def test_keeps_long_words(self):
        ts = _token_set("memory knowledge system")
        assert "memory" in ts
        assert "knowledge" in ts
        assert "system" in ts

    def test_lowercases(self):
        ts = _token_set("Memory KNOWLEDGE System")
        assert "memory" in ts
        assert "knowledge" in ts
        assert "system" in ts

    def test_mixed(self):
        ts = _token_set("the knowledge system is fast")
        assert "the" not in ts
        assert "is" not in ts
        assert "knowledge" in ts
        assert "system" in ts
        assert "fast" in ts

    def test_empty_string(self):
        assert _token_set("") == set()

    def test_exactly_4_chars(self):
        ts = _token_set("word")
        assert "word" in ts

    def test_3_chars_excluded(self):
        ts = _token_set("cat bat hat")
        assert ts == set()


# ---------------------------------------------------------------------------
# _jaccard
# ---------------------------------------------------------------------------

class TestJaccard:
    def test_identical_sets(self):
        a = {"word", "test", "data"}
        assert _jaccard(a, a) == 1.0

    def test_disjoint_sets(self):
        a = {"alpha", "beta"}
        b = {"gamma", "delta"}
        assert _jaccard(a, b) == 0.0

    def test_partial_overlap(self):
        a = {"word", "test", "data"}
        b = {"word", "test", "other"}
        # inter=2, union=4
        assert abs(_jaccard(a, b) - 0.5) < 1e-9

    def test_both_empty(self):
        assert _jaccard(set(), set()) == 0.0

    def test_one_empty(self):
        assert _jaccard({"word"}, set()) == 0.0
        assert _jaccard(set(), {"word"}) == 0.0

    def test_subset(self):
        a = {"word"}
        b = {"word", "test", "data"}
        # inter=1, union=3
        assert abs(_jaccard(a, b) - 1 / 3) < 1e-9


# ---------------------------------------------------------------------------
# TransferRecord
# ---------------------------------------------------------------------------

class TestTransferRecord:
    def test_ts_auto_set(self):
        r = TransferRecord(
            concept="memory",
            source_doc_id="doc1",
            target_doc_id="docX",
            content_snippet="memory systems store data",
            similarity=0.5,
            accepted=True,
        )
        assert r.ts != ""
        assert "T" in r.ts  # ISO format

    def test_ts_explicit(self):
        r = TransferRecord(
            concept="memory",
            source_doc_id="doc1",
            target_doc_id="docX",
            content_snippet="snippet",
            similarity=0.5,
            accepted=True,
            ts="2025-01-01T00:00:00",
        )
        assert r.ts == "2025-01-01T00:00:00"

    def test_accepted_true(self):
        r = TransferRecord("c", "a", "b", "text", 0.9, True)
        assert r.accepted is True

    def test_accepted_false(self):
        r = TransferRecord("c", "a", "b", "text", 0.05, False)
        assert r.accepted is False

    def test_fields(self):
        r = TransferRecord("concept", "src", "tgt", "snip", 0.3, True)
        assert r.concept == "concept"
        assert r.source_doc_id == "src"
        assert r.target_doc_id == "tgt"
        assert r.content_snippet == "snip"
        assert r.similarity == 0.3


# ---------------------------------------------------------------------------
# TransferReport
# ---------------------------------------------------------------------------

class TestTransferReport:
    def test_defaults(self):
        rpt = TransferReport()
        assert rpt.records == []
        assert rpt.accepted_count == 0
        assert rpt.rejected_count == 0

    def test_acceptance_rate_zero_total(self):
        rpt = TransferReport()
        assert rpt.acceptance_rate() == 0.0

    def test_acceptance_rate_all_accepted(self):
        rpt = TransferReport(accepted_count=5, rejected_count=0)
        assert rpt.acceptance_rate() == 1.0

    def test_acceptance_rate_half(self):
        rpt = TransferReport(accepted_count=3, rejected_count=3)
        assert rpt.acceptance_rate() == 0.5

    def test_acceptance_rate_none_accepted(self):
        rpt = TransferReport(accepted_count=0, rejected_count=4)
        assert rpt.acceptance_rate() == 0.0

    def test_accepted_records_filters(self):
        r1 = TransferRecord("c1", "a", "b", "s", 0.8, True)
        r2 = TransferRecord("c2", "a", "b", "s", 0.05, False)
        r3 = TransferRecord("c3", "a", "b", "s", 0.6, True)
        rpt = TransferReport(records=[r1, r2, r3])
        accepted = rpt.accepted_records()
        assert len(accepted) == 2
        assert all(r.accepted for r in accepted)

    def test_accepted_records_empty(self):
        rpt = TransferReport()
        assert rpt.accepted_records() == []


# ---------------------------------------------------------------------------
# DiffusionTransfer.transfer
# ---------------------------------------------------------------------------

class TestDiffusionTransfer:
    def _make_alignment(self, concept, doc_id_a, doc_id_b, similarity):
        aligned = similarity >= 0.15
        return ConceptAlignment(concept, doc_id_a, doc_id_b, similarity, aligned)

    def test_returns_transfer_report(self):
        dt = DiffusionTransfer()
        result = dt.transfer([], {})
        assert isinstance(result, TransferReport)

    def test_empty_alignments_empty_report(self):
        dt = DiffusionTransfer()
        report = dt.transfer([], CORPUS_A)
        assert report.records == []
        assert report.accepted_count == 0
        assert report.rejected_count == 0

    def test_total_equals_len_alignments(self):
        dt = DiffusionTransfer(trust_threshold=0.2)
        alignments = [
            self._make_alignment("memory", "doc1", "docX", 0.5),
            self._make_alignment("agent", "doc2", "docY", 0.1),
            self._make_alignment("knowledge", "doc1", "docY", 0.3),
        ]
        report = dt.transfer(alignments, CORPUS_A)
        assert report.accepted_count + report.rejected_count == len(alignments)

    def test_high_similarity_accepted(self):
        dt = DiffusionTransfer(trust_threshold=0.2)
        alignments = [self._make_alignment("memory", "doc1", "docX", 0.8)]
        report = dt.transfer(alignments, CORPUS_A)
        assert report.accepted_count == 1
        assert report.rejected_count == 0

    def test_low_similarity_rejected(self):
        dt = DiffusionTransfer(trust_threshold=0.5)
        alignments = [self._make_alignment("memory", "doc1", "docX", 0.1)]
        report = dt.transfer(alignments, CORPUS_A)
        assert report.accepted_count == 0
        assert report.rejected_count == 1

    def test_content_snippet_non_empty_accepted(self):
        dt = DiffusionTransfer(trust_threshold=0.2)
        alignments = [self._make_alignment("memory", "doc1", "docX", 0.8)]
        report = dt.transfer(alignments, CORPUS_A)
        accepted = report.accepted_records()
        assert len(accepted) == 1
        assert accepted[0].content_snippet != ""

    def test_source_and_target_ids(self):
        dt = DiffusionTransfer()
        report = dt.transfer([], CORPUS_A, source_id="CORP_A", target_id="CORP_B")
        assert report.source_corpus_id == "CORP_A"
        assert report.target_corpus_id == "CORP_B"

    def test_records_length(self):
        dt = DiffusionTransfer(trust_threshold=0.2)
        alignments = [
            self._make_alignment("memory", "doc1", "docX", 0.5),
            self._make_alignment("agent", "doc2", "docY", 0.3),
        ]
        report = dt.transfer(alignments, CORPUS_A)
        assert len(report.records) == 2

    def test_missing_doc_still_produces_snippet(self):
        dt = DiffusionTransfer(trust_threshold=0.0)
        alignments = [self._make_alignment("memory", "missing_doc", "docX", 0.5)]
        # missing_doc not in CORPUS_A, should still work (fallback snippet)
        report = dt.transfer(alignments, CORPUS_A)
        assert len(report.records) == 1


# ---------------------------------------------------------------------------
# DiffusionProvenance
# ---------------------------------------------------------------------------

class TestDiffusionProvenance:
    def test_hops_from_chain(self):
        dp = DiffusionProvenance(
            concept="memory",
            origin_corpus="A",
            origin_doc_id="doc1",
            diffused_to_corpus="B",
            diffused_to_doc_id="docX",
            similarity_chain=[0.5, 0.3],
        )
        assert dp.hops() == 2

    def test_hops_zero(self):
        dp = DiffusionProvenance("c", "A", "d1", "B", "d2", similarity_chain=[])
        assert dp.hops() == 0

    def test_min_similarity_correct(self):
        dp = DiffusionProvenance(
            "c", "A", "d1", "B", "d2",
            similarity_chain=[0.8, 0.3, 0.6],
        )
        assert dp.min_similarity() == 0.3

    def test_min_similarity_empty_chain(self):
        dp = DiffusionProvenance("c", "A", "d1", "B", "d2", similarity_chain=[])
        assert dp.min_similarity() == 0.0

    def test_min_similarity_single(self):
        dp = DiffusionProvenance("c", "A", "d1", "B", "d2", similarity_chain=[0.42])
        assert dp.min_similarity() == 0.42

    def test_provenance_string_format(self):
        dp = DiffusionProvenance(
            concept="memory",
            origin_corpus="CorpusA",
            origin_doc_id="doc1",
            diffused_to_corpus="CorpusB",
            diffused_to_doc_id="docX",
            similarity_chain=[0.5],
        )
        s = dp.provenance_string()
        assert "memory" in s
        assert "CorpusA/doc1" in s
        assert "CorpusB/docX" in s
        assert "hops=1" in s
        assert "→" in s

    def test_provenance_string_hops_zero(self):
        dp = DiffusionProvenance("x", "A", "d1", "B", "d2", similarity_chain=[])
        s = dp.provenance_string()
        assert "hops=0" in s

    def test_accepted_default_true(self):
        dp = DiffusionProvenance("c", "A", "d1", "B", "d2")
        assert dp.accepted is True


# ---------------------------------------------------------------------------
# trace_origin
# ---------------------------------------------------------------------------

class TestTraceOrigin:
    def _make_record(self, concept, src, tgt, sim, accepted):
        r = TransferRecord(concept, src, tgt, "snippet", sim, accepted)
        return r

    def test_returns_list(self):
        result = trace_origin([], "A", "B")
        assert isinstance(result, list)

    def test_empty_records(self):
        result = trace_origin([], "CorpusA", "CorpusB")
        assert result == []

    def test_accepted_only(self):
        records = [
            self._make_record("memory", "doc1", "docX", 0.7, True),
            self._make_record("agent", "doc2", "docY", 0.1, False),
            self._make_record("knowledge", "doc1", "docY", 0.5, True),
        ]
        result = trace_origin(records, "A", "B")
        assert len(result) == 2
        assert all(p.accepted for p in result)

    def test_similarity_chain_has_one_hop(self):
        records = [self._make_record("memory", "doc1", "docX", 0.6, True)]
        result = trace_origin(records, "A", "B")
        assert len(result) == 1
        assert result[0].similarity_chain == [0.6]

    def test_origin_corpus_set(self):
        records = [self._make_record("concept", "doc1", "docX", 0.5, True)]
        result = trace_origin(records, "SourceCorpus", "TargetCorpus")
        assert result[0].origin_corpus == "SourceCorpus"

    def test_target_corpus_set(self):
        records = [self._make_record("concept", "doc1", "docX", 0.5, True)]
        result = trace_origin(records, "SourceCorpus", "TargetCorpus")
        assert result[0].diffused_to_corpus == "TargetCorpus"

    def test_doc_ids_set(self):
        records = [self._make_record("concept", "doc1", "docX", 0.5, True)]
        result = trace_origin(records, "A", "B")
        assert result[0].origin_doc_id == "doc1"
        assert result[0].diffused_to_doc_id == "docX"

    def test_all_rejected_returns_empty(self):
        records = [
            self._make_record("c1", "a", "b", 0.1, False),
            self._make_record("c2", "a", "b", 0.05, False),
        ]
        result = trace_origin(records, "A", "B")
        assert result == []

    def test_provenance_is_diffusion_provenance(self):
        records = [self._make_record("memory", "doc1", "docX", 0.6, True)]
        result = trace_origin(records, "A", "B")
        assert isinstance(result[0], DiffusionProvenance)
