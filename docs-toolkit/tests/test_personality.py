"""Tests for docstoolkit.personality (N9 — Personality-shaped retrieval)."""
import pytest
from dataclasses import dataclass

from docstoolkit.personality import (
    CognitiveProfile,
    ProfileSurvey,
    infer_profile,
    PersonalRetriever,
    StyleModifier,
    explain_personalization,
    PersonalizationExplanation,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

@dataclass
class FakePassage:
    """Minimal Passage-like object for testing."""
    text: str
    doc_id: str
    title: str = ""
    score: float = 0.5


# ---------------------------------------------------------------------------
# CognitiveProfile
# ---------------------------------------------------------------------------

class TestCognitiveProfileFields:
    def test_default_skepticism(self):
        p = CognitiveProfile()
        assert p.skepticism == 0.5

    def test_default_synthesis(self):
        p = CognitiveProfile()
        assert p.synthesis == 0.5

    def test_default_exploration(self):
        p = CognitiveProfile()
        assert p.exploration == 0.5

    def test_default_verification(self):
        p = CognitiveProfile()
        assert p.verification == 0.5

    def test_default_pragmatism(self):
        p = CognitiveProfile()
        assert p.pragmatism == 0.5

    def test_default_confidence(self):
        p = CognitiveProfile()
        assert p.confidence == 0.5

    def test_custom_values(self):
        p = CognitiveProfile(skepticism=0.8, pragmatism=0.2)
        assert p.skepticism == 0.8
        assert p.pragmatism == 0.2


class TestDominantStyle:
    def test_returns_highest_dim_skepticism(self):
        p = CognitiveProfile(skepticism=0.9, synthesis=0.1)
        assert p.dominant_style() == "skepticism"

    def test_returns_highest_dim_pragmatism(self):
        p = CognitiveProfile(pragmatism=0.95)
        assert p.dominant_style() == "pragmatism"

    def test_returns_highest_dim_synthesis(self):
        p = CognitiveProfile(synthesis=0.8, skepticism=0.3)
        assert p.dominant_style() == "synthesis"

    def test_returns_highest_dim_verification(self):
        p = CognitiveProfile(verification=0.7, synthesis=0.3)
        assert p.dominant_style() == "verification"

    def test_returns_highest_dim_exploration(self):
        p = CognitiveProfile(exploration=0.75)
        assert p.dominant_style() == "exploration"

    def test_equal_dims_no_crash(self):
        # All equal — should return some valid dim name without raising
        p = CognitiveProfile(
            skepticism=0.5, synthesis=0.5, exploration=0.5,
            verification=0.5, pragmatism=0.5
        )
        valid = {"skepticism", "synthesis", "exploration", "verification", "pragmatism"}
        assert p.dominant_style() in valid


class TestToFromDict:
    def test_to_dict_keys(self):
        p = CognitiveProfile(skepticism=0.7)
        d = p.to_dict()
        assert set(d.keys()) == {
            "skepticism", "synthesis", "exploration",
            "verification", "pragmatism", "confidence",
        }

    def test_to_dict_values(self):
        p = CognitiveProfile(skepticism=0.7, pragmatism=0.3)
        d = p.to_dict()
        assert d["skepticism"] == 0.7
        assert d["pragmatism"] == 0.3

    def test_round_trip(self):
        p = CognitiveProfile(skepticism=0.7, synthesis=0.2, exploration=0.9,
                             verification=0.1, pragmatism=0.6, confidence=0.8)
        assert CognitiveProfile.from_dict(p.to_dict()) == p

    def test_from_dict_defaults_missing_keys(self):
        p = CognitiveProfile.from_dict({})
        assert p.skepticism == 0.5
        assert p.confidence == 0.5


class TestBlend:
    def test_blend_50_50(self):
        a = CognitiveProfile(skepticism=0.0)
        b = CognitiveProfile(skepticism=1.0)
        result = a.blend(b, weight=0.5)
        assert abs(result.skepticism - 0.5) < 1e-9

    def test_blend_weight_0(self):
        a = CognitiveProfile(pragmatism=0.2)
        b = CognitiveProfile(pragmatism=0.8)
        result = a.blend(b, weight=0.0)
        assert abs(result.pragmatism - 0.2) < 1e-9

    def test_blend_weight_1(self):
        a = CognitiveProfile(pragmatism=0.2)
        b = CognitiveProfile(pragmatism=0.8)
        result = a.blend(b, weight=1.0)
        assert abs(result.pragmatism - 0.8) < 1e-9

    def test_blend_all_dims(self):
        a = CognitiveProfile(skepticism=0.0, synthesis=0.0, exploration=0.0,
                             verification=0.0, pragmatism=0.0)
        b = CognitiveProfile(skepticism=1.0, synthesis=1.0, exploration=1.0,
                             verification=1.0, pragmatism=1.0)
        result = a.blend(b, weight=0.3)
        assert abs(result.skepticism - 0.3) < 1e-9
        assert abs(result.synthesis - 0.3) < 1e-9


# ---------------------------------------------------------------------------
# ProfileSurvey
# ---------------------------------------------------------------------------

class TestProfileSurvey:
    def setup_method(self):
        self.survey = ProfileSurvey()

    def test_questions_initialized(self):
        assert len(self.survey.QUESTIONS) == 5

    def test_score_answer_q0_chose_b_skepticism(self):
        delta = self.survey.score_answer(0, True)
        assert "skepticism" in delta
        assert delta["skepticism"] == pytest.approx(0.2)

    def test_score_answer_q0_chose_a_no_boost(self):
        delta = self.survey.score_answer(0, False)
        assert delta == {}

    def test_score_answer_q2_chose_b_exploration(self):
        delta = self.survey.score_answer(2, True)
        assert "exploration" in delta
        assert delta["exploration"] == pytest.approx(0.2)

    def test_score_answer_q1_chose_a_synthesis(self):
        delta = self.survey.score_answer(1, False)
        assert "synthesis" in delta
        assert delta["synthesis"] == pytest.approx(0.2)

    def test_score_answer_q3_chose_a_verification(self):
        delta = self.survey.score_answer(3, False)
        assert "verification" in delta
        assert delta["verification"] == pytest.approx(0.2)

    def test_score_answer_q4_chose_b_pragmatism(self):
        delta = self.survey.score_answer(4, True)
        assert "pragmatism" in delta
        assert delta["pragmatism"] == pytest.approx(0.2)

    def test_build_profile_all_b(self):
        profile = self.survey.build_profile([True, True, True, True, True])
        # Q0 chose_b → skepticism boosted
        assert profile.skepticism > 0.3
        # Q2 chose_b → exploration boosted
        assert profile.exploration > 0.3
        # Q4 chose_b → pragmatism boosted
        assert profile.pragmatism > 0.3

    def test_build_profile_empty(self):
        profile = self.survey.build_profile([])
        assert profile.skepticism == pytest.approx(0.3)
        assert profile.synthesis == pytest.approx(0.3)
        assert profile.confidence == pytest.approx(0.0)

    def test_confidence_partial(self):
        profile = self.survey.build_profile([True, False, True])
        assert profile.confidence == pytest.approx(3 / 5)

    def test_confidence_full(self):
        profile = self.survey.build_profile([True, True, True, True, True])
        assert profile.confidence == pytest.approx(1.0)

    def test_build_profile_all_a(self):
        # Q1 chose_a(False=chose_a) → synthesis boosted; Q3 chose_a → verification boosted
        profile = self.survey.build_profile([False, False, False, False, False])
        assert profile.synthesis > 0.3
        assert profile.verification > 0.3


# ---------------------------------------------------------------------------
# infer_profile
# ---------------------------------------------------------------------------

class TestInferProfile:
    def test_skepticism_from_however(self):
        queries = ["but why", "however this is wrong"] * 5
        p = infer_profile(queries)
        assert p.skepticism > 0.5

    def test_pragmatism_from_how_to(self):
        queries = ["how to install", "how to use it"] * 5
        p = infer_profile(queries)
        assert p.pragmatism > 0.5

    def test_synthesis_from_compare(self):
        queries = ["compare A vs B", "what is the difference"] * 5
        p = infer_profile(queries)
        assert p.synthesis > 0.5

    def test_verification_from_source(self):
        queries = ["find evidence", "cite source", "proof required"] * 5
        p = infer_profile(queries)
        assert p.verification > 0.5

    def test_exploration_from_short_queries(self):
        queries = ["AI", "RAG", "LLM", "NLP"] * 5
        p = infer_profile(queries)
        assert p.exploration > 0.5

    def test_empty_queries_confidence_zero(self):
        p = infer_profile([])
        assert p.confidence == 0.0

    def test_confidence_scales_with_count(self):
        p = infer_profile(["test"] * 10)
        assert p.confidence == pytest.approx(10 / 20)

    def test_confidence_capped_at_one(self):
        p = infer_profile(["test"] * 100)
        assert p.confidence == pytest.approx(1.0)

    def test_values_in_range(self):
        queries = ["however", "how to", "compare", "source", "AI"] * 3
        p = infer_profile(queries)
        for dim in [p.skepticism, p.synthesis, p.exploration, p.verification, p.pragmatism]:
            assert 0.0 <= dim <= 1.0


# ---------------------------------------------------------------------------
# StyleModifier
# ---------------------------------------------------------------------------

class TestStyleModifier:
    def test_default_skepticism_boost(self):
        m = StyleModifier()
        assert m.skepticism_boost == pytest.approx(0.2)

    def test_default_synthesis_boost(self):
        m = StyleModifier()
        assert m.synthesis_boost == pytest.approx(0.2)

    def test_default_exploration_penalty(self):
        m = StyleModifier()
        assert m.exploration_penalty == pytest.approx(0.05)

    def test_default_verification_boost(self):
        m = StyleModifier()
        assert m.verification_boost == pytest.approx(0.15)

    def test_default_pragmatism_boost(self):
        m = StyleModifier()
        assert m.pragmatism_boost == pytest.approx(0.2)

    def test_custom_values(self):
        m = StyleModifier(skepticism_boost=0.5, verification_boost=0.1)
        assert m.skepticism_boost == pytest.approx(0.5)
        assert m.verification_boost == pytest.approx(0.1)


# ---------------------------------------------------------------------------
# PersonalRetriever
# ---------------------------------------------------------------------------

class TestPersonalRetriever:
    def _make_retriever(self, **profile_kwargs) -> PersonalRetriever:
        return PersonalRetriever(CognitiveProfile(**profile_kwargs))

    def test_rerank_returns_same_count(self):
        retriever = self._make_retriever()
        passages = [FakePassage("text", f"doc{i}") for i in range(5)]
        result = retriever.rerank(passages)
        assert len(result) == 5

    def test_rerank_empty_returns_empty(self):
        retriever = self._make_retriever()
        assert retriever.rerank([]) == []

    def test_high_skepticism_boosts_skeptic_passage(self):
        retriever = self._make_retriever(skepticism=0.9)
        skeptic = FakePassage("However, this contradicts prior work", "skeptic", score=0.5)
        neutral = FakePassage("This is a plain statement", "neutral", score=0.5)
        result = retriever.rerank([neutral, skeptic])
        # skeptic passage should come first (higher score)
        assert result[0].doc_id == "skeptic"

    def test_high_verification_boosts_cited_passage(self):
        retriever = self._make_retriever(verification=0.9)
        cited = FakePassage("According to [source], this is true", "cited", score=0.5)
        plain = FakePassage("This is just a claim", "plain", score=0.5)
        result = retriever.rerank([plain, cited])
        assert result[0].doc_id == "cited"

    def test_high_pragmatism_boosts_howto_passage(self):
        retriever = self._make_retriever(pragmatism=0.9)
        howto = FakePassage("How to install and run this example step by step", "howto", score=0.5)
        theory = FakePassage("The theoretical basis of the system", "theory", score=0.5)
        result = retriever.rerank([theory, howto])
        assert result[0].doc_id == "howto"

    def test_high_synthesis_boosts_overview_passage(self):
        retriever = self._make_retriever(synthesis=0.9)
        overview = FakePassage("In general, the overview shows a broad pattern", "overview", score=0.5)
        detail = FakePassage("A single narrow implementation detail", "detail", score=0.5)
        result = retriever.rerank([detail, overview])
        assert result[0].doc_id == "overview"

    def test_exploration_penalty_for_seen_docs(self):
        retriever = self._make_retriever(exploration=0.9)
        seen = FakePassage("Some text", "doc_seen", score=0.5)
        fresh = FakePassage("Some text", "doc_fresh", score=0.5)
        result = retriever.rerank([seen, fresh], seen_doc_ids={"doc_seen"})
        # fresh passage should rank higher because seen is penalized
        assert result[0].doc_id == "doc_fresh"

    def test_no_boost_when_profile_below_threshold(self):
        # All dims = 0.5, below 0.6 threshold — scores should be unchanged, order stable by score
        retriever = self._make_retriever()  # all 0.5
        p1 = FakePassage("However contradicts challenges", "p1", score=0.8)
        p2 = FakePassage("However contradicts challenges", "p2", score=0.6)
        result = retriever.rerank([p1, p2])
        # No boosts applied; order by original score
        assert result[0].doc_id == "p1"

    def test_rerank_preserves_doc_ids(self):
        retriever = self._make_retriever()
        passages = [FakePassage("text", f"doc{i}", score=float(i)) for i in range(4)]
        result = retriever.rerank(passages)
        ids = {p.doc_id for p in result}
        assert ids == {"doc0", "doc1", "doc2", "doc3"}

    def test_top_style_matches_profile(self):
        profile = CognitiveProfile(pragmatism=0.9)
        retriever = PersonalRetriever(profile)
        assert retriever.top_style() == "pragmatism"

    def test_top_style_returns_string(self):
        retriever = self._make_retriever(verification=0.95)
        assert retriever.top_style() == "verification"


# ---------------------------------------------------------------------------
# PersonalizationExplanation
# ---------------------------------------------------------------------------

class TestPersonalizationExplanation:
    def test_fields_exist(self):
        exp = PersonalizationExplanation(
            dominant_style="skepticism",
            applied_boosts=["skepticism +0.80"],
            default_ranking=["a", "b"],
            personal_ranking=["b", "a"],
            rank_changes={"a": 1, "b": -1},
        )
        assert exp.dominant_style == "skepticism"
        assert exp.applied_boosts == ["skepticism +0.80"]
        assert exp.default_ranking == ["a", "b"]
        assert exp.personal_ranking == ["b", "a"]
        assert exp.rank_changes == {"a": 1, "b": -1}


# ---------------------------------------------------------------------------
# explain_personalization
# ---------------------------------------------------------------------------

class TestExplainPersonalization:
    def _make_passages(self, doc_ids: list, scores: list | None = None) -> list:
        if scores is None:
            scores = [float(i) for i in range(len(doc_ids), 0, -1)]
        return [FakePassage("text", did, score=s) for did, s in zip(doc_ids, scores)]

    def test_returns_explanation_object(self):
        profile = CognitiveProfile(skepticism=0.8)
        default_p = self._make_passages(["a", "b", "c"])
        personal_p = self._make_passages(["b", "a", "c"])
        result = explain_personalization(profile, default_p, personal_p)
        assert isinstance(result, PersonalizationExplanation)

    def test_dominant_style_matches_profile(self):
        profile = CognitiveProfile(verification=0.9)
        p = self._make_passages(["a"])
        result = explain_personalization(profile, p, p)
        assert result.dominant_style == "verification"

    def test_default_ranking_is_list_of_doc_ids(self):
        profile = CognitiveProfile()
        default_p = self._make_passages(["x", "y", "z"])
        result = explain_personalization(profile, default_p, default_p)
        assert result.default_ranking == ["x", "y", "z"]

    def test_personal_ranking_is_list_of_doc_ids(self):
        profile = CognitiveProfile()
        default_p = self._make_passages(["x", "y", "z"])
        personal_p = self._make_passages(["z", "x", "y"])
        result = explain_personalization(profile, default_p, personal_p)
        assert result.personal_ranking == ["z", "x", "y"]

    def test_rank_changes_moved_up_negative(self):
        profile = CognitiveProfile()
        default_p = self._make_passages(["a", "b", "c"])
        personal_p = self._make_passages(["b", "a", "c"])
        result = explain_personalization(profile, default_p, personal_p)
        # "b" moved from pos 1 to pos 0 → change = -1
        assert result.rank_changes["b"] == -1
        # "a" moved from pos 0 to pos 1 → change = +1
        assert result.rank_changes["a"] == 1

    def test_rank_changes_no_change(self):
        profile = CognitiveProfile()
        passages = self._make_passages(["a", "b", "c"])
        result = explain_personalization(profile, passages, passages)
        assert all(v == 0 for v in result.rank_changes.values())

    def test_applied_boosts_high_dim(self):
        profile = CognitiveProfile(skepticism=0.8, verification=0.7)
        p = self._make_passages(["a"])
        result = explain_personalization(profile, p, p)
        boost_names = [b.split()[0] for b in result.applied_boosts]
        assert "skepticism" in boost_names
        assert "verification" in boost_names

    def test_applied_boosts_empty_when_all_low(self):
        profile = CognitiveProfile(
            skepticism=0.3, synthesis=0.3, exploration=0.3,
            verification=0.3, pragmatism=0.3
        )
        p = self._make_passages(["a"])
        result = explain_personalization(profile, p, p)
        assert result.applied_boosts == []

    def test_applied_boosts_format(self):
        profile = CognitiveProfile(pragmatism=0.75)
        p = self._make_passages(["a"])
        result = explain_personalization(profile, p, p)
        assert any("pragmatism" in b for b in result.applied_boosts)
        # Should contain "+0.75"
        assert any("+0.75" in b for b in result.applied_boosts)
