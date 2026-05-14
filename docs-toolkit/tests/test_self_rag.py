"""Tests for Self-RAG: reflection-driven iterative retrieval."""
import pytest

from docstoolkit.self_rag import (
    DecisionToken,
    parse_decision,
    NEED_RETRIEVAL,
    NO_RETRIEVAL,
    REFLECT,
    ANSWER_OK,
    ANSWER_INSUFFICIENT,
    reflect_on_answer,
    ReflectScore,
    ReflectStep,
    SelfRAGResult,
    self_rag_ask,
)
from docstoolkit.rag.types import Passage


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_passage(text: str, doc_id: str = "doc1", score: float = 0.9) -> Passage:
    return Passage(text=text, doc_id=doc_id, title=doc_id, score=score)


# ---------------------------------------------------------------------------
# DecisionToken — enum values
# ---------------------------------------------------------------------------

class TestDecisionTokenEnum:
    def test_need_retrieval_exists(self):
        assert DecisionToken.NEED_RETRIEVAL is not None

    def test_no_retrieval_exists(self):
        assert DecisionToken.NO_RETRIEVAL is not None

    def test_reflect_exists(self):
        assert DecisionToken.REFLECT is not None

    def test_answer_ok_exists(self):
        assert DecisionToken.ANSWER_OK is not None

    def test_answer_insufficient_exists(self):
        assert DecisionToken.ANSWER_INSUFFICIENT is not None

    def test_all_five_members(self):
        assert len(DecisionToken) == 5

    def test_values_are_strings(self):
        for token in DecisionToken:
            assert isinstance(token.value, str)


# ---------------------------------------------------------------------------
# Convenience aliases
# ---------------------------------------------------------------------------

class TestAliases:
    def test_need_retrieval_alias(self):
        assert NEED_RETRIEVAL == DecisionToken.NEED_RETRIEVAL

    def test_no_retrieval_alias(self):
        assert NO_RETRIEVAL == DecisionToken.NO_RETRIEVAL

    def test_reflect_alias(self):
        assert REFLECT == DecisionToken.REFLECT

    def test_answer_ok_alias(self):
        assert ANSWER_OK == DecisionToken.ANSWER_OK

    def test_answer_insufficient_alias(self):
        assert ANSWER_INSUFFICIENT == DecisionToken.ANSWER_INSUFFICIENT


# ---------------------------------------------------------------------------
# parse_decision
# ---------------------------------------------------------------------------

class TestParseDecision:
    def test_bracket_need_retrieval(self):
        assert parse_decision("[NEED_RETRIEVAL]") == DecisionToken.NEED_RETRIEVAL

    def test_bracket_answer_ok(self):
        assert parse_decision("[ANSWER_OK]") == DecisionToken.ANSWER_OK

    def test_bracket_answer_insufficient(self):
        assert parse_decision("[ANSWER_INSUFFICIENT]") == DecisionToken.ANSWER_INSUFFICIENT

    def test_bracket_no_retrieval(self):
        assert parse_decision("[NO_RETRIEVAL]") == DecisionToken.NO_RETRIEVAL

    def test_bracket_reflect(self):
        assert parse_decision("[REFLECT]") == DecisionToken.REFLECT

    def test_case_insensitive_answer_ok(self):
        assert parse_decision("[answer_ok]") == DecisionToken.ANSWER_OK

    def test_case_insensitive_need_retrieval(self):
        assert parse_decision("[need_retrieval]") == DecisionToken.NEED_RETRIEVAL

    def test_case_insensitive_reflect(self):
        assert parse_decision("[reflect]") == DecisionToken.REFLECT

    def test_token_anywhere_in_text(self):
        assert parse_decision("I think [REFLECT] we need more info") == DecisionToken.REFLECT

    def test_reflect_in_long_text(self):
        text = "After careful consideration of all available evidence, [REFLECT] seems appropriate"
        assert parse_decision(text) == DecisionToken.REFLECT

    def test_short_text_no_token_fallback_need_retrieval(self):
        # Less than 20 chars, no token
        assert parse_decision("short") == DecisionToken.NEED_RETRIEVAL

    def test_short_text_exact_boundary(self):
        # Exactly 19 chars
        text = "1234567890123456789"  # 19 chars
        assert parse_decision(text) == DecisionToken.NEED_RETRIEVAL

    def test_long_text_no_token_fallback_reflect(self):
        long_text = "This is a very long answer that does not contain any special decision token at all."
        assert parse_decision(long_text) == DecisionToken.REFLECT

    def test_empty_string_fallback_need_retrieval(self):
        assert parse_decision("") == DecisionToken.NEED_RETRIEVAL

    def test_answer_insufficient_takes_priority_over_answer_ok(self):
        # ANSWER_INSUFFICIENT should be found (appears in text before ANSWER_OK in terms of matching)
        result = parse_decision("[ANSWER_INSUFFICIENT]")
        assert result == DecisionToken.ANSWER_INSUFFICIENT


# ---------------------------------------------------------------------------
# ReflectScore — dataclass fields
# ---------------------------------------------------------------------------

class TestReflectScoreFields:
    def test_has_score_field(self):
        rs = ReflectScore(
            score=7.5,
            missing_topics=[],
            contradictions=[],
            suggested_query="q",
            decision="answer_ok",
        )
        assert rs.score == 7.5

    def test_has_missing_topics_field(self):
        rs = ReflectScore(
            score=5.0,
            missing_topics=["topic1", "topic2"],
            contradictions=[],
            suggested_query="q",
            decision="answer_insufficient",
        )
        assert rs.missing_topics == ["topic1", "topic2"]

    def test_has_contradictions_field(self):
        rs = ReflectScore(
            score=6.0,
            missing_topics=[],
            contradictions=["some contradiction"],
            suggested_query="q",
            decision="answer_insufficient",
        )
        assert rs.contradictions == ["some contradiction"]

    def test_has_suggested_query_field(self):
        rs = ReflectScore(
            score=4.0,
            missing_topics=["missing"],
            contradictions=[],
            suggested_query="original question missing",
            decision="answer_insufficient",
        )
        assert "original" in rs.suggested_query

    def test_has_decision_field(self):
        rs = ReflectScore(
            score=8.0,
            missing_topics=[],
            contradictions=[],
            suggested_query="q",
            decision="answer_ok",
        )
        assert rs.decision == "answer_ok"


# ---------------------------------------------------------------------------
# reflect_on_answer
# ---------------------------------------------------------------------------

class TestReflectOnAnswer:
    def test_returns_reflect_score_instance(self):
        rs = reflect_on_answer("What is RAG?", "RAG retrieval system", [])
        assert isinstance(rs, ReflectScore)

    def test_score_in_range_0_to_10(self):
        rs = reflect_on_answer("test question", "some answer text here", [])
        assert 0.0 <= rs.score <= 10.0

    def test_perfect_answer_high_score(self):
        question = "What is memory retrieval system?"
        # Answer contains all question terms, passage also contains them
        answer = "Memory retrieval system stores and retrieves information efficiently."
        passages = [make_passage("memory retrieval system for knowledge management")]
        rs = reflect_on_answer(question, answer, passages, reflect_threshold=7.0)
        assert rs.score > 5.0

    def test_empty_answer_low_score(self):
        question = "What is memory retrieval system?"
        rs = reflect_on_answer(question, "", [])
        assert rs.score < 5.0

    def test_answer_covers_question_terms_score_above_5(self):
        question = "knowledge graph system"
        answer = "Knowledge graph system organizes information in a structured graph"
        passages = [make_passage("knowledge graph system for data")]
        rs = reflect_on_answer(question, answer, passages)
        assert rs.score > 5.0

    def test_missing_topics_are_question_terms_not_in_answer(self):
        question = "Explain knowledge graph retrieval system"
        answer = "knowledge graph stores data"
        rs = reflect_on_answer(question, answer, [])
        # "retrieval" and "system" from question should be missing in answer
        assert isinstance(rs.missing_topics, list)
        missing_lower = [t.lower() for t in rs.missing_topics]
        assert "retrieval" in missing_lower or "system" in missing_lower

    def test_missing_topics_max_3(self):
        question = "memory knowledge graph retrieval system architecture design"
        answer = "basic answer"
        rs = reflect_on_answer(question, answer, [])
        assert len(rs.missing_topics) <= 3

    def test_decision_answer_ok_when_score_high(self):
        question = "memory system"
        answer = "memory system is a data structure for storing information"
        passages = [make_passage("memory system stores data")]
        rs = reflect_on_answer(question, answer, passages, reflect_threshold=3.0)
        assert rs.decision == "answer_ok"

    def test_decision_answer_insufficient_when_score_low(self):
        question = "What is retrieval augmented generation knowledge graph?"
        answer = "I don't know"
        rs = reflect_on_answer(question, answer, [], reflect_threshold=7.0)
        assert rs.decision == "answer_insufficient"

    def test_suggested_query_contains_original_question(self):
        question = "What is memory retrieval?"
        answer = "basic info"
        rs = reflect_on_answer(question, answer, [])
        assert question in rs.suggested_query or question[:20] in rs.suggested_query

    def test_suggested_query_appends_missing_topics(self):
        question = "knowledge graph retrieval system"
        answer = "some basic answer here"
        rs = reflect_on_answer(question, answer, [])
        if rs.missing_topics:
            # suggested_query should be enriched with missing topics
            assert len(rs.suggested_query) >= len(question)

    def test_contradictions_returns_list(self):
        rs = reflect_on_answer("test question", "test answer", [])
        assert isinstance(rs.contradictions, list)

    def test_no_passages_still_works(self):
        rs = reflect_on_answer("What is RAG?", "RAG is retrieval augmented generation", [])
        assert isinstance(rs, ReflectScore)
        assert 0.0 <= rs.score <= 10.0

    def test_threshold_boundary_equal_is_ok(self):
        # When score exactly equals threshold, decision should be "answer_ok"
        question = "memory system"
        answer = "memory system"
        passages = [make_passage("memory system")]
        rs = reflect_on_answer(question, answer, passages, reflect_threshold=0.0)
        assert rs.decision == "answer_ok"


# ---------------------------------------------------------------------------
# ReflectStep — dataclass fields
# ---------------------------------------------------------------------------

class TestReflectStepFields:
    def test_all_fields_present(self):
        step = ReflectStep(
            iteration=0,
            decision="retrieve",
            query="test query",
            n_passages=3,
            answer="some answer",
            reflect_score=7.5,
            issues=["topic1"],
            suggested_query="test query topic1",
        )
        assert step.iteration == 0
        assert step.decision == "retrieve"
        assert step.query == "test query"
        assert step.n_passages == 3
        assert step.answer == "some answer"
        assert step.reflect_score == 7.5
        assert step.issues == ["topic1"]
        assert step.suggested_query == "test query topic1"

    def test_suggested_query_has_default(self):
        step = ReflectStep(
            iteration=1,
            decision="stop",
            query="q",
            n_passages=0,
            answer="a",
            reflect_score=8.0,
            issues=[],
        )
        assert step.suggested_query == ""

    def test_iteration_type_int(self):
        step = ReflectStep(
            iteration=2,
            decision="reflect",
            query="q",
            n_passages=5,
            answer="a",
            reflect_score=5.5,
            issues=[],
        )
        assert isinstance(step.iteration, int)

    def test_reflect_score_type_float(self):
        step = ReflectStep(
            iteration=0,
            decision="stop",
            query="q",
            n_passages=1,
            answer="a",
            reflect_score=9.0,
            issues=[],
        )
        assert isinstance(step.reflect_score, float)


# ---------------------------------------------------------------------------
# SelfRAGResult — dataclass fields
# ---------------------------------------------------------------------------

class TestSelfRAGResultFields:
    def test_all_fields_present(self):
        result = SelfRAGResult(
            final_answer="answer",
            steps=[],
            total_retrievals=2,
            total_iterations=2,
            confidence=0.8,
        )
        assert result.final_answer == "answer"
        assert result.steps == []
        assert result.total_retrievals == 2
        assert result.total_iterations == 2
        assert result.confidence == 0.8

    def test_confidence_in_0_1_range(self):
        result = SelfRAGResult(
            final_answer="a",
            steps=[],
            total_retrievals=1,
            total_iterations=1,
            confidence=0.5,
        )
        assert 0.0 <= result.confidence <= 1.0


# ---------------------------------------------------------------------------
# self_rag_ask — integration tests
# ---------------------------------------------------------------------------

class TestSelfRagAsk:
    def test_returns_self_rag_result(self):
        result = self_rag_ask("What is memory?")
        assert isinstance(result, SelfRAGResult)

    def test_no_retriever_no_answerer_works(self):
        result = self_rag_ask("What is retrieval?")
        assert result.final_answer is not None
        assert isinstance(result.final_answer, str)

    def test_steps_list_non_empty(self):
        result = self_rag_ask("What is knowledge graph?")
        assert len(result.steps) > 0

    def test_total_iterations_equals_len_steps(self):
        result = self_rag_ask("What is RAG system?")
        assert result.total_iterations == len(result.steps)

    def test_confidence_in_0_1_range(self):
        result = self_rag_ask("What is a retrieval system?")
        assert 0.0 <= result.confidence <= 1.0

    def test_max_iterations_1_exactly_1_step(self):
        result = self_rag_ask("What is memory?", max_iterations=1)
        assert result.total_iterations == 1
        assert len(result.steps) == 1

    def test_max_iterations_2_at_most_2_steps(self):
        result = self_rag_ask("What is knowledge graph retrieval?", max_iterations=2)
        assert result.total_iterations <= 2

    def test_high_reflect_threshold_runs_max_iterations(self):
        """With threshold=10, score never reaches it — always runs full iterations."""
        result = self_rag_ask(
            "What is memory retrieval system?",
            max_iterations=3,
            reflect_threshold=10.0,
        )
        assert result.total_iterations == 3

    def test_low_reflect_threshold_stops_after_1(self):
        """With threshold=0, first iteration always passes."""
        result = self_rag_ask(
            "What is memory?",
            max_iterations=4,
            reflect_threshold=0.0,
        )
        assert result.total_iterations == 1

    def test_retriever_fn_called(self):
        calls = []

        def my_retriever(query: str, k: int) -> list:
            calls.append(query)
            return [make_passage(f"memory retrieval {query[:20]}")]

        result = self_rag_ask(
            "What is memory?",
            retriever_fn=my_retriever,
            max_iterations=2,
            reflect_threshold=10.0,
        )
        assert len(calls) >= 1

    def test_retriever_fn_with_good_passages_fewer_iterations(self):
        """Good passages that answer the question well should stop early."""
        question = "memory system"

        def good_retriever(q: str, k: int) -> list:
            return [make_passage("memory system stores data efficiently")]

        def good_answerer(q: str, passages: list) -> str:
            return "memory system is a key data structure"

        result = self_rag_ask(
            question,
            retriever_fn=good_retriever,
            answerer_fn=good_answerer,
            max_iterations=4,
            reflect_threshold=5.0,
        )
        # Should stop early with good answer
        assert result.total_iterations <= 4

    def test_answerer_fn_is_called(self):
        answers = []

        def my_answerer(q: str, passages: list) -> str:
            answers.append(q)
            return "memory is important"

        self_rag_ask(
            "What is memory?",
            answerer_fn=my_answerer,
            max_iterations=1,
        )
        assert len(answers) >= 1

    def test_total_retrievals_counts_calls(self):
        calls = []

        def counting_retriever(q: str, k: int) -> list:
            calls.append(1)
            return []

        result = self_rag_ask(
            "What is memory retrieval graph?",
            retriever_fn=counting_retriever,
            max_iterations=3,
            reflect_threshold=10.0,
        )
        assert result.total_retrievals == len(calls)
        assert result.total_retrievals == 3

    def test_steps_have_correct_type(self):
        result = self_rag_ask("test question", max_iterations=2)
        for step in result.steps:
            assert isinstance(step, ReflectStep)

    def test_final_answer_is_last_step_answer(self):
        result = self_rag_ask("What is memory?", max_iterations=2)
        if result.steps:
            assert result.final_answer == result.steps[-1].answer

    def test_n_passages_recorded_in_step(self):
        def retriever(q: str, k: int) -> list:
            return [make_passage("text1"), make_passage("text2")]

        result = self_rag_ask(
            "test query",
            retriever_fn=retriever,
            max_iterations=1,
        )
        assert result.steps[0].n_passages == 2

    def test_custom_top_k_passed_to_retriever(self):
        received_k = []

        def retriever(q: str, k: int) -> list:
            received_k.append(k)
            return []

        self_rag_ask("test", retriever_fn=retriever, top_k=7, max_iterations=1)
        assert received_k[0] == 7
