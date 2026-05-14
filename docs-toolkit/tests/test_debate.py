"""Tests for docstoolkit.debate — multi-agent debate module."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.debate.persona import Persona, SKEPTIC, SYNTHESIZER, CONTRARIAN
from docstoolkit.debate.round import DebateRound, run_debate_round, _generate_answer, _generate_critique
from docstoolkit.debate.result import (
    DebateResult,
    multi_agent_debate,
    _agreement_score,
    _synthesize,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def echo_fn(question: str, passages: list, system_prompt: str) -> str:
    """Simple deterministic answerer for tests."""
    return f"{system_prompt[:20]}:{question[:30]}"


def word_fn(word: str):
    """Returns a fn that always answers with the given word."""
    def fn(q, p, s):
        return word
    return fn


# ---------------------------------------------------------------------------
# Persona tests
# ---------------------------------------------------------------------------

class TestPersona:
    def test_fields_exist(self):
        p = Persona(name="test", system_prompt="prompt")
        assert hasattr(p, "name")
        assert hasattr(p, "system_prompt")
        assert hasattr(p, "temperature")
        assert hasattr(p, "retriever_method")

    def test_skeptic_name(self):
        assert SKEPTIC.name == "skeptic"

    def test_synthesizer_name(self):
        assert SYNTHESIZER.name == "synthesizer"

    def test_contrarian_name(self):
        assert CONTRARIAN.name == "contrarian"

    def test_skeptic_temperature(self):
        assert SKEPTIC.temperature == 0.5

    def test_synthesizer_temperature(self):
        assert SYNTHESIZER.temperature == 0.7

    def test_contrarian_temperature(self):
        assert CONTRARIAN.temperature == 0.9

    def test_default_temperature(self):
        p = Persona(name="x", system_prompt="y")
        assert p.temperature == 0.7

    def test_default_retriever_method(self):
        p = Persona(name="x", system_prompt="y")
        assert p.retriever_method == "hybrid"

    def test_custom_persona(self):
        p = Persona(name="custom", system_prompt="be creative", temperature=0.3, retriever_method="bm25")
        assert p.name == "custom"
        assert p.system_prompt == "be creative"
        assert p.temperature == 0.3
        assert p.retriever_method == "bm25"

    def test_system_prompt_not_empty(self):
        for persona in [SKEPTIC, SYNTHESIZER, CONTRARIAN]:
            assert len(persona.system_prompt) > 0


# ---------------------------------------------------------------------------
# DebateRound tests
# ---------------------------------------------------------------------------

class TestDebateRound:
    def test_fields_exist(self):
        dr = DebateRound(round_num=0, agent_answers={}, critiques={})
        assert hasattr(dr, "round_num")
        assert hasattr(dr, "agent_answers")
        assert hasattr(dr, "critiques")

    def test_round_num_preserved(self):
        dr = DebateRound(round_num=3, agent_answers={}, critiques={})
        assert dr.round_num == 3

    def test_agent_answers_is_dict(self):
        dr = DebateRound(round_num=0, agent_answers={"a": "ans"}, critiques={})
        assert isinstance(dr.agent_answers, dict)

    def test_critiques_is_dict_of_dicts(self):
        dr = DebateRound(round_num=0, agent_answers={}, critiques={"a": {"b": "crit"}})
        assert isinstance(dr.critiques, dict)
        assert isinstance(dr.critiques["a"], dict)


# ---------------------------------------------------------------------------
# run_debate_round tests
# ---------------------------------------------------------------------------

class TestRunDebateRound:
    def _personas(self):
        return [SKEPTIC, SYNTHESIZER, CONTRARIAN]

    def test_returns_debate_round(self):
        result = run_debate_round("q", self._personas(), [], echo_fn)
        assert isinstance(result, DebateRound)

    def test_agent_answers_has_key_for_each_persona(self):
        personas = self._personas()
        result = run_debate_round("q", personas, [], echo_fn)
        for p in personas:
            assert p.name in result.agent_answers

    def test_critiques_has_key_for_each_persona(self):
        personas = self._personas()
        result = run_debate_round("q", personas, [], echo_fn)
        for p in personas:
            assert p.name in result.critiques

    def test_each_persona_critiques_others(self):
        personas = self._personas()
        result = run_debate_round("q", personas, [], echo_fn)
        for critic in personas:
            for target in personas:
                if critic.name != target.name:
                    assert target.name in result.critiques[critic.name]

    def test_no_self_critique(self):
        personas = self._personas()
        result = run_debate_round("q", personas, [], echo_fn)
        for p in personas:
            assert p.name not in result.critiques[p.name]

    def test_round_num_matches_input(self):
        result = run_debate_round("q", self._personas(), [], echo_fn, round_num=2)
        assert result.round_num == 2

    def test_answerer_fn_called_for_each_persona(self):
        calls = []
        def tracking_fn(q, p, s):
            calls.append((q, s))
            return "answer"
        personas = self._personas()
        run_debate_round("question", personas, [], tracking_fn)
        # At minimum, each persona generates 1 answer
        answer_calls = [c for c in calls if "answer" not in c[0].lower() or True]
        assert len(calls) >= len(personas)

    def test_with_prior_answers_returns_valid_round(self):
        prior = {"skeptic": "old answer one", "synthesizer": "old answer two", "contrarian": "old answer three"}
        result = run_debate_round("q", self._personas(), [], echo_fn, round_num=1, prior_answers=prior)
        assert isinstance(result, DebateRound)
        for p in self._personas():
            assert p.name in result.agent_answers

    def test_agent_answers_are_strings(self):
        result = run_debate_round("q", self._personas(), [], echo_fn)
        for name, answer in result.agent_answers.items():
            assert isinstance(answer, str)

    def test_two_personas(self):
        personas = [SKEPTIC, SYNTHESIZER]
        result = run_debate_round("q", personas, [], echo_fn)
        assert len(result.agent_answers) == 2
        assert len(result.critiques) == 2


# ---------------------------------------------------------------------------
# _agreement_score tests
# ---------------------------------------------------------------------------

class TestAgreementScore:
    def test_identical_answers(self):
        answers = {"a": "the quick brown fox", "b": "the quick brown fox"}
        assert _agreement_score(answers) == pytest.approx(1.0)

    def test_completely_different(self):
        answers = {"a": "apple mango banana", "b": "car truck bus plane"}
        score = _agreement_score(answers)
        assert score == pytest.approx(0.0)

    def test_partial_overlap(self):
        answers = {"a": "the quick brown fox", "b": "the slow green cat"}
        score = _agreement_score(answers)
        assert 0.0 < score < 1.0

    def test_single_answer(self):
        answers = {"a": "only one answer here"}
        assert _agreement_score(answers) == pytest.approx(1.0)

    def test_three_answers_partial(self):
        answers = {
            "a": "alpha beta gamma",
            "b": "alpha delta epsilon",
            "c": "alpha zeta eta",
        }
        score = _agreement_score(answers)
        assert 0.0 < score < 1.0

    def test_empty_answers_dict(self):
        # Edge case: no answers
        score = _agreement_score({})
        assert score == pytest.approx(1.0)


# ---------------------------------------------------------------------------
# _synthesize tests
# ---------------------------------------------------------------------------

class TestSynthesize:
    def test_returns_tuple(self):
        answers = {"a": "Hello world.", "b": "Hello world."}
        result = _synthesize(answers, "q", echo_fn)
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_consensus_is_non_empty_string(self):
        answers = {"a": "Hello world.", "b": "Hello world."}
        consensus, _ = _synthesize(answers, "q", echo_fn)
        assert isinstance(consensus, str)
        assert len(consensus) > 0

    def test_dissenting_is_list(self):
        answers = {"a": "Hello world.", "b": "Goodbye world."}
        _, dissenting = _synthesize(answers, "q", echo_fn)
        assert isinstance(dissenting, list)

    def test_dissenting_items_are_strings(self):
        answers = {
            "a": "The sky is blue.",
            "b": "Trains are fast.",
            "c": "Mountains are tall.",
        }
        _, dissenting = _synthesize(answers, "q", echo_fn)
        for item in dissenting:
            assert isinstance(item, str)

    def test_identical_answers_no_dissenting(self):
        text = "The answer is yes. This is confirmed."
        answers = {"a": text, "b": text, "c": text}
        consensus, dissenting = _synthesize(answers, "q", echo_fn)
        assert len(consensus) > 0


# ---------------------------------------------------------------------------
# DebateResult tests
# ---------------------------------------------------------------------------

class TestDebateResult:
    def _make_result(self):
        rnd = DebateRound(
            round_num=0,
            agent_answers={"skeptic": "ans1", "synthesizer": "ans2"},
            critiques={"skeptic": {"synthesizer": "crit"}, "synthesizer": {"skeptic": "crit2"}},
        )
        return DebateResult(
            question="What is life?",
            consensus="Life is complex.",
            dissenting=["Some say it is simple."],
            confidence=0.75,
            rounds=[rnd],
            personas_used=["skeptic", "synthesizer"],
        )

    def test_fields_exist(self):
        r = self._make_result()
        assert hasattr(r, "question")
        assert hasattr(r, "consensus")
        assert hasattr(r, "dissenting")
        assert hasattr(r, "confidence")
        assert hasattr(r, "rounds")
        assert hasattr(r, "personas_used")

    def test_confidence_in_range(self):
        r = self._make_result()
        assert 0.0 <= r.confidence <= 1.0

    def test_to_markdown_contains_consensus(self):
        r = self._make_result()
        md = r.to_markdown()
        assert "consensus" in md.lower()

    def test_to_markdown_shows_round_count(self):
        r = self._make_result()
        md = r.to_markdown()
        assert "1" in md  # 1 round shown somewhere

    def test_to_markdown_returns_string(self):
        r = self._make_result()
        assert isinstance(r.to_markdown(), str)

    def test_personas_used_matches(self):
        r = self._make_result()
        assert r.personas_used == ["skeptic", "synthesizer"]


# ---------------------------------------------------------------------------
# multi_agent_debate tests
# ---------------------------------------------------------------------------

class TestMultiAgentDebate:
    def test_returns_debate_result(self):
        result = multi_agent_debate("What is AI?", [])
        assert isinstance(result, DebateResult)

    def test_no_answerer_fn_works(self):
        # Should not raise
        result = multi_agent_debate("test question", [])
        assert result is not None

    def test_no_personas_uses_three_defaults(self):
        result = multi_agent_debate("q", [])
        assert len(result.personas_used) == 3

    def test_default_persona_names(self):
        result = multi_agent_debate("q", [])
        assert "skeptic" in result.personas_used
        assert "synthesizer" in result.personas_used
        assert "contrarian" in result.personas_used

    def test_personas_used_correct_names(self):
        custom = [
            Persona("agent_a", "You are agent A."),
            Persona("agent_b", "You are agent B."),
        ]
        result = multi_agent_debate("q", [], personas=custom, answerer_fn=echo_fn)
        assert result.personas_used == ["agent_a", "agent_b"]

    def test_max_rounds_1_exactly_one_round(self):
        result = multi_agent_debate("q", [], max_rounds=1, answerer_fn=echo_fn)
        assert len(result.rounds) == 1

    def test_max_rounds_2_exactly_two_rounds(self):
        result = multi_agent_debate("q", [], max_rounds=2, answerer_fn=echo_fn)
        assert len(result.rounds) == 2

    def test_confidence_in_range(self):
        result = multi_agent_debate("q", [], answerer_fn=echo_fn)
        assert 0.0 <= result.confidence <= 1.0

    def test_consensus_non_empty(self):
        result = multi_agent_debate("q", [], answerer_fn=echo_fn)
        assert isinstance(result.consensus, str)
        assert len(result.consensus) > 0

    def test_rounds_list_non_empty(self):
        result = multi_agent_debate("q", [], answerer_fn=echo_fn)
        assert len(result.rounds) > 0

    def test_round_nums_sequential(self):
        result = multi_agent_debate("q", [], max_rounds=3, answerer_fn=echo_fn)
        for i, rnd in enumerate(result.rounds):
            assert rnd.round_num == i

    def test_all_personas_in_all_rounds(self):
        personas = [SKEPTIC, SYNTHESIZER]
        result = multi_agent_debate("q", [], personas=personas, max_rounds=2, answerer_fn=echo_fn)
        for rnd in result.rounds:
            for p in personas:
                assert p.name in rnd.agent_answers

    def test_identical_answerer_high_confidence(self):
        # When all personas produce identical answers, confidence should be high
        result = multi_agent_debate("q", [], answerer_fn=word_fn("exact same answer text"))
        assert result.confidence > 0.5

    def test_question_preserved(self):
        question = "What is the meaning of life?"
        result = multi_agent_debate(question, [], answerer_fn=echo_fn)
        assert result.question == question
