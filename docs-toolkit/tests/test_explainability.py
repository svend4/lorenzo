"""Tests for docstoolkit.explainability module (E30)."""
import pytest
from docstoolkit.explainability import (
    AttributionMethod,
    TokenAttribution,
    PassageAttribution,
    AttributionExplainer,
    TraceStep,
    ReasoningTrace,
    TraceBuilder,
    ExplainabilityReport,
    ExplainabilityEngine,
)


# ---------------------------------------------------------------------------
# TokenAttribution
# ---------------------------------------------------------------------------

class TestTokenAttribution:
    def test_fields(self):
        ta = TokenAttribution(token="neural", score=0.7, method=AttributionMethod.TOKEN_OVERLAP)
        assert ta.token == "neural"
        assert ta.score == 0.7
        assert ta.method == AttributionMethod.TOKEN_OVERLAP

    def test_all_methods_accessible(self):
        for method in AttributionMethod:
            ta = TokenAttribution(token="x", score=0.0, method=method)
            assert ta.method == method

    def test_zero_score(self):
        ta = TokenAttribution(token="foo", score=0.0, method=AttributionMethod.POSITION)
        assert ta.score == 0.0

    def test_score_one(self):
        ta = TokenAttribution(token="bar", score=1.0, method=AttributionMethod.KEYWORD_FREQUENCY)
        assert ta.score == 1.0


# ---------------------------------------------------------------------------
# AttributionMethod enum
# ---------------------------------------------------------------------------

class TestAttributionMethod:
    def test_enum_members(self):
        members = {m.name for m in AttributionMethod}
        assert "TOKEN_OVERLAP" in members
        assert "PASSAGE_SCORE" in members
        assert "KEYWORD_FREQUENCY" in members
        assert "POSITION" in members

    def test_values(self):
        assert AttributionMethod.TOKEN_OVERLAP.value == "token_overlap"
        assert AttributionMethod.PASSAGE_SCORE.value == "passage_score"
        assert AttributionMethod.KEYWORD_FREQUENCY.value == "keyword_frequency"
        assert AttributionMethod.POSITION.value == "position"


# ---------------------------------------------------------------------------
# PassageAttribution
# ---------------------------------------------------------------------------

class TestPassageAttribution:
    def _make_passage(self, n_tokens=6):
        tokens = [
            TokenAttribution(token=f"tok{i}", score=float(i) / n_tokens, method=AttributionMethod.TOKEN_OVERLAP)
            for i in range(n_tokens)
        ]
        return PassageAttribution(
            passage_id="p1",
            passage_text="some text here",
            attribution_score=0.5,
            token_attributions=tokens,
            rank=1,
        )

    def test_fields(self):
        pa = self._make_passage()
        assert pa.passage_id == "p1"
        assert pa.passage_text == "some text here"
        assert pa.attribution_score == 0.5
        assert pa.rank == 1
        assert len(pa.token_attributions) == 6

    def test_top_tokens_default(self):
        pa = self._make_passage(10)
        top = pa.top_tokens()
        assert len(top) == 5
        # Ensure descending order
        for a, b in zip(top, top[1:]):
            assert a.score >= b.score

    def test_top_tokens_n(self):
        pa = self._make_passage(10)
        top = pa.top_tokens(3)
        assert len(top) == 3

    def test_top_tokens_fewer_than_n(self):
        pa = self._make_passage(2)
        top = pa.top_tokens(5)
        assert len(top) == 2

    def test_top_tokens_empty(self):
        pa = PassageAttribution(
            passage_id="p0", passage_text="", attribution_score=0.0,
            token_attributions=[], rank=1,
        )
        assert pa.top_tokens() == []

    def test_top_tokens_sorted_desc(self):
        tokens = [
            TokenAttribution("a", 0.1, AttributionMethod.TOKEN_OVERLAP),
            TokenAttribution("b", 0.9, AttributionMethod.TOKEN_OVERLAP),
            TokenAttribution("c", 0.5, AttributionMethod.TOKEN_OVERLAP),
        ]
        pa = PassageAttribution("id", "text", 0.5, tokens, 1)
        top = pa.top_tokens(3)
        assert top[0].token == "b"
        assert top[1].token == "c"
        assert top[2].token == "a"


# ---------------------------------------------------------------------------
# AttributionExplainer.explain_passage
# ---------------------------------------------------------------------------

class TestAttributionExplainerPassage:
    def setup_method(self):
        self.ex = AttributionExplainer()

    def test_returns_passage_attribution(self):
        result = self.ex.explain_passage("memory agent", "memory is key for agents", "p0", 1)
        assert isinstance(result, PassageAttribution)

    def test_passage_id_set(self):
        result = self.ex.explain_passage("query", "passage text", passage_id="abc")
        assert result.passage_id == "abc"

    def test_rank_set(self):
        result = self.ex.explain_passage("query", "passage text", rank=3)
        assert result.rank == 3

    def test_no_overlap_score_zero(self):
        result = self.ex.explain_passage("xyz rare word", "completely unrelated banana cake")
        assert result.attribution_score == 0.0

    def test_full_overlap_nonzero(self):
        query = "memory agent"
        passage = "memory agent memory agent memory agent"
        result = self.ex.explain_passage(query, passage)
        assert result.attribution_score > 0.0

    def test_token_attributions_present(self):
        result = self.ex.explain_passage("memory agent", "memory is used by agent")
        assert len(result.token_attributions) > 0

    def test_token_attribution_method(self):
        result = self.ex.explain_passage("memory", "memory memory memory")
        for ta in result.token_attributions:
            assert ta.method == AttributionMethod.TOKEN_OVERLAP

    def test_token_scores_normalized(self):
        # Token scores should sum to ~1.0 when there is overlap
        result = self.ex.explain_passage("memory agent", "memory agent knowledge")
        total = sum(ta.score for ta in result.token_attributions)
        assert abs(total - 1.0) < 1e-9

    def test_no_query_tokens_score_zero(self):
        result = self.ex.explain_passage("", "some passage text")
        assert result.attribution_score == 0.0

    def test_empty_passage_score_zero(self):
        result = self.ex.explain_passage("memory agent", "")
        assert result.attribution_score == 0.0

    def test_higher_frequency_higher_score(self):
        # Passage with more query token occurrences should score higher
        p_high = "memory memory memory agent agent"
        p_low = "memory nothing here at all"
        r_high = self.ex.explain_passage("memory agent", p_high)
        r_low = self.ex.explain_passage("memory agent", p_low)
        assert r_high.attribution_score >= r_low.attribution_score

    def test_passage_text_preserved(self):
        text = "exact passage text preserved"
        result = self.ex.explain_passage("passage", text)
        assert result.passage_text == text

    def test_default_passage_id(self):
        result = self.ex.explain_passage("query", "text")
        assert result.passage_id == ""

    def test_default_rank(self):
        result = self.ex.explain_passage("query", "text")
        assert result.rank == 1


# ---------------------------------------------------------------------------
# AttributionExplainer.explain_all
# ---------------------------------------------------------------------------

class TestAttributionExplainerAll:
    def setup_method(self):
        self.ex = AttributionExplainer()

    def test_returns_list(self):
        result = self.ex.explain_all("memory", ["passage one", "passage two"])
        assert isinstance(result, list)

    def test_count_matches_passages(self):
        passages = ["p1", "p2", "p3"]
        result = self.ex.explain_all("query", passages)
        assert len(result) == 3

    def test_empty_passages(self):
        result = self.ex.explain_all("query", [])
        assert result == []

    def test_sorted_by_score_desc(self):
        query = "memory agent"
        passages = [
            "banana apple orange",          # no overlap
            "memory agent memory agent",    # high overlap
            "memory is good",               # some overlap
        ]
        result = self.ex.explain_all(query, passages)
        for a, b in zip(result, result[1:]):
            assert a.attribution_score >= b.attribution_score

    def test_ranks_reassigned(self):
        passages = ["no overlap at all", "memory agent knowledge"]
        result = self.ex.explain_all("memory agent", passages)
        ranks = [r.rank for r in result]
        assert ranks == list(range(1, len(result) + 1))

    def test_passage_ids_are_strings(self):
        result = self.ex.explain_all("query", ["a", "b", "c"])
        for pa in result:
            assert isinstance(pa.passage_id, str)

    def test_single_passage(self):
        result = self.ex.explain_all("memory", ["memory is great"])
        assert len(result) == 1
        assert result[0].rank == 1


# ---------------------------------------------------------------------------
# TraceStep
# ---------------------------------------------------------------------------

class TestTraceStep:
    def test_fields(self):
        step = TraceStep(
            step_name="retrieve",
            input_summary="query: memory",
            output_summary="found 5 passages",
            duration_ms=12.5,
            metadata={"top_k": 5},
        )
        assert step.step_name == "retrieve"
        assert step.input_summary == "query: memory"
        assert step.output_summary == "found 5 passages"
        assert step.duration_ms == 12.5
        assert step.metadata == {"top_k": 5}

    def test_defaults(self):
        step = TraceStep(step_name="s", input_summary="in", output_summary="out")
        assert step.duration_ms == 0.0
        assert step.metadata == {}

    def test_metadata_default_independent(self):
        s1 = TraceStep("a", "in", "out")
        s2 = TraceStep("b", "in", "out")
        s1.metadata["key"] = "val"
        assert "key" not in s2.metadata


# ---------------------------------------------------------------------------
# ReasoningTrace
# ---------------------------------------------------------------------------

class TestReasoningTrace:
    def _make_trace(self, n=3):
        steps = [
            TraceStep(f"step{i}", f"input {i}", f"output {i}", duration_ms=float(i * 10))
            for i in range(n)
        ]
        return ReasoningTrace(query="what is memory?", steps=steps, final_answer="Memory is X.")

    def test_step_count(self):
        trace = self._make_trace(3)
        assert trace.step_count() == 3

    def test_step_count_empty(self):
        trace = ReasoningTrace(query="q", steps=[])
        assert trace.step_count() == 0

    def test_add_step(self):
        trace = ReasoningTrace(query="q", steps=[])
        step = TraceStep("new", "in", "out")
        trace.add_step(step)
        assert trace.step_count() == 1
        assert trace.steps[0] is step

    def test_add_step_increments(self):
        trace = self._make_trace(2)
        trace.add_step(TraceStep("extra", "x", "y"))
        assert trace.step_count() == 3

    def test_to_markdown_contains_query(self):
        trace = self._make_trace(2)
        md = trace.to_markdown()
        assert "what is memory?" in md

    def test_to_markdown_contains_answer(self):
        trace = self._make_trace(1)
        md = trace.to_markdown()
        assert "Memory is X." in md

    def test_to_markdown_numbered_steps(self):
        trace = self._make_trace(3)
        md = trace.to_markdown()
        assert "1." in md
        assert "2." in md
        assert "3." in md

    def test_to_markdown_step_names(self):
        trace = self._make_trace(2)
        md = trace.to_markdown()
        assert "step0" in md
        assert "step1" in md

    def test_to_markdown_input_output(self):
        trace = self._make_trace(1)
        md = trace.to_markdown()
        assert "input 0" in md
        assert "output 0" in md

    def test_to_markdown_empty_steps(self):
        trace = ReasoningTrace(query="q", steps=[], final_answer="ans")
        md = trace.to_markdown()
        assert "q" in md

    def test_to_markdown_returns_string(self):
        trace = self._make_trace(2)
        assert isinstance(trace.to_markdown(), str)

    def test_total_ms_default(self):
        trace = ReasoningTrace(query="q", steps=[])
        assert trace.total_ms == 0.0

    def test_final_answer_default(self):
        trace = ReasoningTrace(query="q", steps=[])
        assert trace.final_answer == ""


# ---------------------------------------------------------------------------
# TraceBuilder
# ---------------------------------------------------------------------------

class TestTraceBuilder:
    def test_build_empty(self):
        tb = TraceBuilder("my query")
        trace = tb.build()
        assert trace.query == "my query"
        assert trace.step_count() == 0
        assert trace.final_answer == ""

    def test_build_with_answer(self):
        tb = TraceBuilder("q")
        trace = tb.build("The answer")
        assert trace.final_answer == "The answer"

    def test_record_adds_steps(self):
        tb = TraceBuilder("q")
        tb.record("retrieve", "query q", "5 passages", duration_ms=10.0)
        tb.record("rank", "5 passages", "top 3", duration_ms=5.0)
        trace = tb.build()
        assert trace.step_count() == 2

    def test_record_step_fields(self):
        tb = TraceBuilder("q")
        tb.record("step1", "in", "out", duration_ms=7.5)
        trace = tb.build()
        step = trace.steps[0]
        assert step.step_name == "step1"
        assert step.input_summary == "in"
        assert step.output_summary == "out"
        assert step.duration_ms == 7.5

    def test_record_metadata(self):
        tb = TraceBuilder("q")
        tb.record("step", "in", "out", top_k=5, model="bm25")
        trace = tb.build()
        assert trace.steps[0].metadata == {"top_k": 5, "model": "bm25"}

    def test_total_ms_sum(self):
        tb = TraceBuilder("q")
        tb.record("a", "in", "out", duration_ms=10.0)
        tb.record("b", "in", "out", duration_ms=20.0)
        trace = tb.build()
        assert trace.total_ms == 30.0

    def test_total_ms_zero_when_no_steps(self):
        tb = TraceBuilder("q")
        trace = tb.build()
        assert trace.total_ms == 0.0

    def test_build_does_not_mutate_builder(self):
        tb = TraceBuilder("q")
        tb.record("step", "in", "out")
        t1 = tb.build()
        t2 = tb.build()
        assert t1.step_count() == t2.step_count()

    def test_multiple_builds_independent(self):
        tb = TraceBuilder("q")
        tb.record("step1", "in", "out")
        t1 = tb.build("ans1")
        tb.record("step2", "in2", "out2")
        t2 = tb.build("ans2")
        assert t1.step_count() == 1
        assert t2.step_count() == 2

    def test_record_default_duration(self):
        tb = TraceBuilder("q")
        tb.record("step", "in", "out")
        trace = tb.build()
        assert trace.steps[0].duration_ms == 0.0


# ---------------------------------------------------------------------------
# ExplainabilityReport
# ---------------------------------------------------------------------------

class TestExplainabilityReport:
    def _make_report(self):
        ex = AttributionExplainer()
        passages = [
            "memory agent knowledge base",
            "banana orange fruit",
            "agent retrieval memory recall",
        ]
        attributions = ex.explain_all("memory agent", passages)
        return ExplainabilityReport(
            query="memory agent",
            answer="Memory helps agents.",
            attributions=attributions,
            confidence=0.42,
        )

    def test_fields(self):
        report = self._make_report()
        assert report.query == "memory agent"
        assert report.answer == "Memory helps agents."
        assert isinstance(report.attributions, list)
        assert report.confidence == 0.42
        assert report.trace is None

    def test_top_passages_default(self):
        report = self._make_report()
        top = report.top_passages()
        assert len(top) == 3

    def test_top_passages_n(self):
        report = self._make_report()
        top = report.top_passages(2)
        assert len(top) == 2

    def test_top_passages_sorted(self):
        report = self._make_report()
        top = report.top_passages(3)
        for a, b in zip(top, top[1:]):
            assert a.attribution_score >= b.attribution_score

    def test_top_passages_fewer_than_n(self):
        ex = AttributionExplainer()
        attributions = ex.explain_all("q", ["one"])
        report = ExplainabilityReport(query="q", answer="a", attributions=attributions)
        assert len(report.top_passages(5)) == 1

    def test_top_passages_empty(self):
        report = ExplainabilityReport(query="q", answer="a", attributions=[])
        assert report.top_passages() == []

    def test_to_dict_keys(self):
        report = self._make_report()
        d = report.to_dict()
        assert "query" in d
        assert "answer" in d
        assert "confidence" in d
        assert "attributions" in d
        assert "trace" in d

    def test_to_dict_values(self):
        report = self._make_report()
        d = report.to_dict()
        assert d["query"] == "memory agent"
        assert d["answer"] == "Memory helps agents."
        assert d["confidence"] == 0.42
        assert d["trace"] is None

    def test_to_dict_attributions_structure(self):
        report = self._make_report()
        d = report.to_dict()
        for a in d["attributions"]:
            assert "passage_id" in a
            assert "passage_text" in a
            assert "attribution_score" in a
            assert "rank" in a
            assert "token_attributions" in a

    def test_to_dict_token_attributions_structure(self):
        report = self._make_report()
        d = report.to_dict()
        # Check first attribution with tokens
        for a in d["attributions"]:
            for ta in a["token_attributions"]:
                assert "token" in ta
                assert "score" in ta
                assert "method" in ta

    def test_to_dict_with_trace(self):
        tb = TraceBuilder("memory agent")
        tb.record("retrieve", "query", "results")
        trace = tb.build("Memory helps agents.")
        ex = AttributionExplainer()
        attributions = ex.explain_all("memory agent", ["memory agent text"])
        report = ExplainabilityReport(
            query="memory agent", answer="ans", attributions=attributions, trace=trace
        )
        d = report.to_dict()
        assert d["trace"] is not None
        assert "steps" in d["trace"]

    def test_to_markdown_contains_query(self):
        report = self._make_report()
        md = report.to_markdown()
        assert "memory agent" in md

    def test_to_markdown_contains_answer(self):
        report = self._make_report()
        md = report.to_markdown()
        assert "Memory helps agents." in md

    def test_to_markdown_contains_confidence(self):
        report = self._make_report()
        md = report.to_markdown()
        assert "0.42" in md or "Confidence" in md

    def test_to_markdown_contains_passages(self):
        report = self._make_report()
        md = report.to_markdown()
        assert "Passage" in md

    def test_to_markdown_returns_string(self):
        report = self._make_report()
        assert isinstance(report.to_markdown(), str)

    def test_to_markdown_with_trace(self):
        tb = TraceBuilder("memory agent")
        tb.record("step", "in", "out")
        trace = tb.build("answer")
        ex = AttributionExplainer()
        attributions = ex.explain_all("memory agent", ["memory"])
        report = ExplainabilityReport(
            query="memory agent", answer="answer", attributions=attributions, trace=trace
        )
        md = report.to_markdown()
        assert "step" in md

    def test_confidence_default_zero(self):
        report = ExplainabilityReport(query="q", answer="a", attributions=[])
        assert report.confidence == 0.0


# ---------------------------------------------------------------------------
# ExplainabilityEngine
# ---------------------------------------------------------------------------

class TestExplainabilityEngine:
    def setup_method(self):
        self.engine = ExplainabilityEngine()

    def test_explain_returns_report(self):
        report = self.engine.explain(
            "memory agent", "Memory helps.", ["memory agent text", "other stuff"]
        )
        assert isinstance(report, ExplainabilityReport)

    def test_explain_query_preserved(self):
        report = self.engine.explain("test query", "answer", ["passage"])
        assert report.query == "test query"

    def test_explain_answer_preserved(self):
        report = self.engine.explain("q", "my answer", ["passage"])
        assert report.answer == "my answer"

    def test_explain_attributions_count(self):
        passages = ["p1", "p2", "p3"]
        report = self.engine.explain("query", "answer", passages)
        assert len(report.attributions) == 3

    def test_explain_no_passages_confidence_zero(self):
        report = self.engine.explain("query", "answer", [])
        assert report.confidence == 0.0
        assert len(report.attributions) == 0

    def test_explain_with_trace(self):
        tb = TraceBuilder("memory")
        tb.record("step", "in", "out")
        trace = tb.build("answer")
        report = self.engine.explain("memory", "answer", ["memory text"], trace=trace)
        assert report.trace is trace

    def test_explain_without_trace(self):
        report = self.engine.explain("memory", "answer", ["memory text"])
        assert report.trace is None

    def test_explain_confidence_positive_with_overlap(self):
        report = self.engine.explain(
            "memory agent",
            "answer",
            ["memory agent memory", "memory agent knowledge", "agent is important"],
        )
        assert report.confidence > 0.0

    def test_explain_confidence_zero_no_overlap(self):
        report = self.engine.explain(
            "memory agent",
            "answer",
            ["banana orange", "apple cake", "fruit salad"],
        )
        assert report.confidence == 0.0

    def test_explain_confidence_avg_top3(self):
        passages = [
            "memory agent knowledge",
            "memory is good for agents",
            "agent recall memory store",
            "completely unrelated content",
        ]
        report = self.engine.explain("memory agent", "answer", passages)
        # confidence should equal average of top-3 scores
        top3 = sorted(report.attributions, key=lambda a: a.attribution_score, reverse=True)[:3]
        expected = sum(a.attribution_score for a in top3) / 3
        assert abs(report.confidence - expected) < 1e-9

    def test_explain_confidence_with_one_passage(self):
        report = self.engine.explain("memory", "answer", ["memory is key"])
        top1 = report.attributions[0].attribution_score
        assert abs(report.confidence - top1) < 1e-9

    def test_explain_attributions_sorted(self):
        passages = [
            "banana",
            "memory agent memory agent",
            "memory",
        ]
        report = self.engine.explain("memory agent", "answer", passages)
        for a, b in zip(report.attributions, report.attributions[1:]):
            assert a.attribution_score >= b.attribution_score

    def test_explain_single_passage(self):
        report = self.engine.explain("memory", "answer", ["memory is important"])
        assert len(report.attributions) == 1

    def test_explain_to_dict_works(self):
        report = self.engine.explain("q", "a", ["passage text"])
        d = report.to_dict()
        assert isinstance(d, dict)

    def test_explain_to_markdown_works(self):
        report = self.engine.explain("q", "a", ["passage text"])
        md = report.to_markdown()
        assert isinstance(md, str)
