"""Tests for docstoolkit.adversarial (N10: Adversarial co-evolution)."""
import sys
from dataclasses import dataclass
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.adversarial import (
    QuestionPattern, HardQuestion, AdversarialGenerator,
    DifficultyScore, validate_difficulty, DifficultyReport,
    CoEvolutionConfig, EvolutionRound, CoEvolutionLoop,
)


# ---------------------------------------------------------------------------
# Passage helper
# ---------------------------------------------------------------------------

@dataclass
class P:
    text: str
    doc_id: str
    title: str = ""
    score: float = 0.5


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def simple_passages():
    return [
        P("AgentFS is a filesystem layer. Yodoca handles memory.", "doc1"),
        P("NGT Memory was created in 2022 for hot-path retrieval.", "doc2"),
        P("CardIndex is the ingestion layer of Svyazi 2.0 architecture.", "doc3"),
    ]


def retriever_hard(question: str) -> float:
    """Returns 0.1 — low retrieval score → high difficulty (0.9)."""
    return 0.1


def retriever_easy(question: str) -> float:
    """Returns 0.9 — high retrieval score → low difficulty (0.1)."""
    return 0.9


def retriever_medium(question: str) -> float:
    """Returns 0.5 — medium difficulty (0.5)."""
    return 0.5


# ---------------------------------------------------------------------------
# QuestionPattern enum
# ---------------------------------------------------------------------------

class TestQuestionPattern:
    def test_has_five_values(self):
        assert len(QuestionPattern) == 5

    def test_multi_hop_value(self):
        assert QuestionPattern.MULTI_HOP.value == "multi_hop"

    def test_entity_confusion_value(self):
        assert QuestionPattern.ENTITY_CONFUSION.value == "entity_confusion"

    def test_time_sensitive_value(self):
        assert QuestionPattern.TIME_SENSITIVE.value == "time_sensitive"

    def test_contradictory_value(self):
        assert QuestionPattern.CONTRADICTORY.value == "contradictory"

    def test_gap_value(self):
        assert QuestionPattern.GAP.value == "gap"

    def test_is_string_enum(self):
        # str, Enum
        assert isinstance(QuestionPattern.MULTI_HOP, str)


# ---------------------------------------------------------------------------
# HardQuestion
# ---------------------------------------------------------------------------

class TestHardQuestion:
    def test_default_fields(self):
        hq = HardQuestion(question="q?", pattern=QuestionPattern.GAP)
        assert hq.source_doc_ids == []
        assert hq.predicted_difficulty == 0.5
        assert hq.target_weakness == ""

    def test_is_hard_above_threshold(self):
        hq = HardQuestion(question="q?", pattern=QuestionPattern.GAP, predicted_difficulty=0.8)
        assert hq.is_hard() is True

    def test_is_hard_at_threshold(self):
        hq = HardQuestion(question="q?", pattern=QuestionPattern.GAP, predicted_difficulty=0.6)
        assert hq.is_hard(threshold=0.6) is True

    def test_is_hard_below_threshold(self):
        hq = HardQuestion(question="q?", pattern=QuestionPattern.GAP, predicted_difficulty=0.4)
        assert hq.is_hard() is False

    def test_is_hard_custom_threshold(self):
        hq = HardQuestion(question="q?", pattern=QuestionPattern.GAP, predicted_difficulty=0.7)
        assert hq.is_hard(threshold=0.8) is False

    def test_source_doc_ids_populated(self):
        hq = HardQuestion(question="q?", pattern=QuestionPattern.MULTI_HOP, source_doc_ids=["a", "b"])
        assert hq.source_doc_ids == ["a", "b"]

    def test_question_string(self):
        hq = HardQuestion(question="What connects X and Y?", pattern=QuestionPattern.MULTI_HOP)
        assert "What connects" in hq.question


# ---------------------------------------------------------------------------
# AdversarialGenerator — generate()
# ---------------------------------------------------------------------------

class TestAdversarialGeneratorGenerate:
    def test_returns_list(self):
        gen = AdversarialGenerator(seed=0)
        result = gen.generate(simple_passages(), n=3)
        assert isinstance(result, list)

    def test_returns_hard_questions(self):
        gen = AdversarialGenerator(seed=0)
        result = gen.generate(simple_passages(), n=3)
        assert all(isinstance(hq, HardQuestion) for hq in result)

    def test_length_equals_n(self):
        gen = AdversarialGenerator(seed=42)
        result = gen.generate(simple_passages(), n=7)
        assert len(result) == 7

    def test_n_zero_returns_empty(self):
        gen = AdversarialGenerator(seed=0)
        result = gen.generate(simple_passages(), n=0)
        assert result == []

    def test_all_patterns_covered_with_large_n(self):
        gen = AdversarialGenerator(seed=1)
        result = gen.generate(simple_passages(), n=20)
        used_patterns = {hq.pattern for hq in result}
        # With n=20 and 5 patterns, all should appear
        assert len(used_patterns) == 5

    def test_each_question_has_nonempty_text(self):
        gen = AdversarialGenerator(seed=0)
        result = gen.generate(simple_passages(), n=10)
        for hq in result:
            assert hq.question.strip() != ""

    def test_multi_hop_difficulty(self):
        gen = AdversarialGenerator(seed=0)
        result = gen.generate(simple_passages(), n=20, patterns=[QuestionPattern.MULTI_HOP])
        for hq in result:
            assert hq.predicted_difficulty == 0.8

    def test_entity_confusion_difficulty(self):
        gen = AdversarialGenerator(seed=0)
        result = gen.generate(simple_passages(), n=10, patterns=[QuestionPattern.ENTITY_CONFUSION])
        for hq in result:
            assert hq.predicted_difficulty == 0.7

    def test_time_sensitive_difficulty(self):
        gen = AdversarialGenerator(seed=0)
        result = gen.generate(simple_passages(), n=10, patterns=[QuestionPattern.TIME_SENSITIVE])
        for hq in result:
            assert hq.predicted_difficulty == 0.75

    def test_contradictory_difficulty(self):
        gen = AdversarialGenerator(seed=0)
        result = gen.generate(simple_passages(), n=10, patterns=[QuestionPattern.CONTRADICTORY])
        for hq in result:
            assert hq.predicted_difficulty == 0.9

    def test_gap_difficulty(self):
        gen = AdversarialGenerator(seed=0)
        result = gen.generate(simple_passages(), n=10, patterns=[QuestionPattern.GAP])
        for hq in result:
            assert hq.predicted_difficulty == 0.65

    def test_source_doc_ids_populated(self):
        gen = AdversarialGenerator(seed=0)
        result = gen.generate(simple_passages(), n=5)
        for hq in result:
            assert isinstance(hq.source_doc_ids, list)
            assert len(hq.source_doc_ids) >= 1

    def test_deterministic_with_same_seed(self):
        gen1 = AdversarialGenerator(seed=99)
        gen2 = AdversarialGenerator(seed=99)
        r1 = gen1.generate(simple_passages(), n=5)
        r2 = gen2.generate(simple_passages(), n=5)
        assert [hq.question for hq in r1] == [hq.question for hq in r2]

    def test_different_seeds_may_differ(self):
        gen1 = AdversarialGenerator(seed=1)
        gen2 = AdversarialGenerator(seed=2)
        r1 = gen1.generate(simple_passages(), n=10)
        r2 = gen2.generate(simple_passages(), n=10)
        # Not guaranteed but with n=10 very likely to differ
        questions1 = [hq.question for hq in r1]
        questions2 = [hq.question for hq in r2]
        assert questions1 != questions2

    def test_empty_passages_no_crash(self):
        gen = AdversarialGenerator(seed=0)
        result = gen.generate([], n=3)
        assert len(result) == 3
        for hq in result:
            assert hq.question.strip() != ""

    def test_single_passage(self):
        gen = AdversarialGenerator(seed=0)
        result = gen.generate([P("Hello World test passage.", "only_doc")], n=5)
        assert len(result) == 5

    def test_patterns_filter(self):
        gen = AdversarialGenerator(seed=0)
        result = gen.generate(
            simple_passages(), n=10,
            patterns=[QuestionPattern.GAP, QuestionPattern.CONTRADICTORY],
        )
        for hq in result:
            assert hq.pattern in (QuestionPattern.GAP, QuestionPattern.CONTRADICTORY)

    def test_target_weakness_set(self):
        gen = AdversarialGenerator(seed=0)
        result = gen.generate(simple_passages(), n=10)
        for hq in result:
            assert hq.target_weakness != ""


# ---------------------------------------------------------------------------
# AdversarialGenerator — _extract_entities()
# ---------------------------------------------------------------------------

class TestExtractEntities:
    def setup_method(self):
        self.gen = AdversarialGenerator()

    def test_extracts_capitalized_words(self):
        result = self.gen._extract_entities("The AgentFS system uses Yodoca internally")
        assert "AgentFS" in result
        assert "Yodoca" in result

    def test_skips_sentence_start(self):
        # Index 0 word is at sentence start → skipped
        result = self.gen._extract_entities("AgentFS is great")
        assert "AgentFS" not in result

    def test_empty_string(self):
        assert self.gen._extract_entities("") == []

    def test_no_capitals_mid_sentence(self):
        result = self.gen._extract_entities("just lowercase words here")
        assert result == []

    def test_strips_punctuation(self):
        result = self.gen._extract_entities("The AgentFS, is used by Yodoca.")
        assert "AgentFS" in result

    def test_multiple_occurrences(self):
        result = self.gen._extract_entities("The Alpha and Alpha system works")
        assert result.count("Alpha") == 2

    def test_returns_list(self):
        result = self.gen._extract_entities("Hello World")
        assert isinstance(result, list)


# ---------------------------------------------------------------------------
# AdversarialGenerator — _extract_keywords()
# ---------------------------------------------------------------------------

class TestExtractKeywords:
    def setup_method(self):
        self.gen = AdversarialGenerator()

    def test_extracts_long_words(self):
        result = self.gen._extract_keywords("memory retrieval architecture system")
        assert "memory" in result
        assert "retrieval" in result
        assert "architecture" in result
        assert "system" in result

    def test_filters_short_words(self):
        result = self.gen._extract_keywords("is a to the")
        assert result == []

    def test_lowercase(self):
        result = self.gen._extract_keywords("AgentFS Memory System")
        assert "agentfs" in result or "memory" in result

    def test_unique(self):
        result = self.gen._extract_keywords("memory memory memory")
        assert len([w for w in result if w == "memory"]) == 1

    def test_min_len_parameter(self):
        result = self.gen._extract_keywords("cat fetch big small", min_len=4)
        assert "fetch" in result
        assert "small" in result
        assert "big" not in result
        assert "cat" not in result

    def test_empty_string(self):
        assert self.gen._extract_keywords("") == []

    def test_returns_list(self):
        result = self.gen._extract_keywords("hello world today")
        assert isinstance(result, list)


# ---------------------------------------------------------------------------
# AdversarialGenerator — _apply_pattern()
# ---------------------------------------------------------------------------

class TestApplyPattern:
    def setup_method(self):
        self.gen = AdversarialGenerator(seed=0)
        self.passages = simple_passages()

    def _call(self, pattern):
        return self.gen._apply_pattern(pattern, self.passages[:2])

    def test_returns_tuple_multi_hop(self):
        result = self._call(QuestionPattern.MULTI_HOP)
        assert isinstance(result, tuple) and len(result) == 3

    def test_question_is_str_multi_hop(self):
        q, ids, w = self._call(QuestionPattern.MULTI_HOP)
        assert isinstance(q, str) and q.strip() != ""

    def test_doc_ids_list_multi_hop(self):
        q, ids, w = self._call(QuestionPattern.MULTI_HOP)
        assert isinstance(ids, list)

    def test_multi_hop_question_format(self):
        q, _, _ = self.gen._apply_pattern(QuestionPattern.MULTI_HOP, self.passages[:2])
        assert "What connects" in q and " and " in q

    def test_entity_confusion_format(self):
        q, _, _ = self._call(QuestionPattern.ENTITY_CONFUSION)
        assert "How is" in q and "different from" in q

    def test_time_sensitive_format(self):
        q, _, _ = self._call(QuestionPattern.TIME_SENSITIVE)
        assert "What changed about" in q and "after" in q

    def test_contradictory_format(self):
        q, _, _ = self._call(QuestionPattern.CONTRADICTORY)
        assert q.startswith("Is it true that")

    def test_gap_format(self):
        q, _, _ = self._call(QuestionPattern.GAP)
        assert "What is the relationship between" in q and "_unknown_" in q

    def test_weakness_nonempty_for_all_patterns(self):
        for pattern in QuestionPattern:
            _, _, w = self.gen._apply_pattern(pattern, self.passages[:1])
            assert w != ""

    def test_time_sensitive_uses_year_from_passage(self):
        p = P("The project started in 2022 with major improvements.", "doc_time")
        q, _, _ = self.gen._apply_pattern(QuestionPattern.TIME_SENSITIVE, [p])
        assert "2022" in q

    def test_time_sensitive_fallback_year(self):
        p = P("No year mentioned here at all.", "doc_noyear")
        q, _, _ = self.gen._apply_pattern(QuestionPattern.TIME_SENSITIVE, [p])
        assert "2020" in q

    def test_apply_pattern_empty_passages(self):
        for pattern in QuestionPattern:
            q, ids, w = self.gen._apply_pattern(pattern, [])
            assert isinstance(q, str) and q.strip() != ""
            assert isinstance(ids, list)


# ---------------------------------------------------------------------------
# DifficultyScore
# ---------------------------------------------------------------------------

class TestDifficultyScore:
    def test_calibration_error_positive(self):
        ds = DifficultyScore(question="q?", predicted=0.8, actual=0.6, confirmed_hard=True)
        assert abs(ds.calibration_error() - 0.2) < 1e-9

    def test_calibration_error_zero(self):
        ds = DifficultyScore(question="q?", predicted=0.7, actual=0.7, confirmed_hard=True)
        assert ds.calibration_error() == 0.0

    def test_calibration_error_abs_value(self):
        ds = DifficultyScore(question="q?", predicted=0.4, actual=0.9, confirmed_hard=True)
        assert abs(ds.calibration_error() - 0.5) < 1e-9

    def test_fields_accessible(self):
        ds = DifficultyScore(question="test", predicted=0.5, actual=0.3, confirmed_hard=False)
        assert ds.question == "test"
        assert ds.predicted == 0.5
        assert ds.actual == 0.3
        assert ds.confirmed_hard is False


# ---------------------------------------------------------------------------
# DifficultyReport
# ---------------------------------------------------------------------------

class TestDifficultyReport:
    def _make_report(self):
        scores = [
            DifficultyScore("q1", 0.8, 0.9, True),
            DifficultyScore("q2", 0.7, 0.4, False),
            DifficultyScore("q3", 0.9, 0.8, True),
        ]
        return DifficultyReport(scores=scores, confirmed_hard_count=2, avg_calibration_error=0.1)

    def test_hard_questions_filters_confirmed(self):
        report = self._make_report()
        hard = report.hard_questions()
        assert len(hard) == 2
        assert all(s.confirmed_hard for s in hard)

    def test_hard_questions_empty(self):
        report = DifficultyReport(scores=[], confirmed_hard_count=0, avg_calibration_error=0.0)
        assert report.hard_questions() == []

    def test_precision_all_confirmed(self):
        scores = [
            DifficultyScore("q1", 0.8, 0.9, True),
            DifficultyScore("q2", 0.7, 0.8, True),
        ]
        report = DifficultyReport(scores=scores)
        assert report.precision() == 1.0

    def test_precision_none_confirmed(self):
        scores = [
            DifficultyScore("q1", 0.8, 0.3, False),
            DifficultyScore("q2", 0.7, 0.2, False),
        ]
        report = DifficultyReport(scores=scores)
        assert report.precision() == 0.0

    def test_precision_partial(self):
        scores = [
            DifficultyScore("q1", 0.8, 0.9, True),
            DifficultyScore("q2", 0.8, 0.3, False),
        ]
        report = DifficultyReport(scores=scores)
        assert report.precision() == 0.5

    def test_precision_no_predicted_hard(self):
        # All predicted < 0.6 → precision = 0.0
        scores = [
            DifficultyScore("q1", 0.3, 0.9, True),
            DifficultyScore("q2", 0.4, 0.8, True),
        ]
        report = DifficultyReport(scores=scores)
        assert report.precision() == 0.0

    def test_default_scores_empty(self):
        report = DifficultyReport()
        assert report.scores == []
        assert report.confirmed_hard_count == 0


# ---------------------------------------------------------------------------
# validate_difficulty()
# ---------------------------------------------------------------------------

class TestValidateDifficulty:
    def _make_questions(self, n=3):
        gen = AdversarialGenerator(seed=0)
        return gen.generate(simple_passages(), n=n)

    def test_returns_difficulty_report(self):
        qs = self._make_questions()
        report = validate_difficulty(qs, retriever_hard)
        assert isinstance(report, DifficultyReport)

    def test_confirmed_hard_with_hard_retriever(self):
        qs = self._make_questions(n=5)
        report = validate_difficulty(qs, retriever_hard)
        # retriever returns 0.1 → actual = 0.9 >= 0.6 → all confirmed hard
        assert report.confirmed_hard_count == 5
        assert all(s.confirmed_hard for s in report.scores)

    def test_not_confirmed_with_easy_retriever(self):
        qs = self._make_questions(n=5)
        report = validate_difficulty(qs, retriever_easy)
        # retriever returns 0.9 → actual = 0.1 < 0.6 → none confirmed hard
        assert report.confirmed_hard_count == 0
        assert all(not s.confirmed_hard for s in report.scores)

    def test_actual_is_one_minus_retrieval(self):
        qs = self._make_questions(n=2)
        report = validate_difficulty(qs, retriever_medium)
        for s in report.scores:
            assert abs(s.actual - 0.5) < 1e-9

    def test_avg_calibration_error_computed(self):
        qs = self._make_questions(n=3)
        report = validate_difficulty(qs, retriever_easy)
        # actual = 0.1 for all; predicted varies by pattern
        expected = sum(abs(hq.predicted_difficulty - 0.1) for hq in qs) / len(qs)
        assert abs(report.avg_calibration_error - expected) < 1e-9

    def test_empty_questions_returns_empty_report(self):
        report = validate_difficulty([], retriever_hard)
        assert report.scores == []
        assert report.confirmed_hard_count == 0
        assert report.avg_calibration_error == 0.0

    def test_custom_threshold(self):
        qs = self._make_questions(n=3)
        # retriever_medium → actual = 0.5; threshold 0.4 → confirmed
        report = validate_difficulty(qs, retriever_medium, threshold=0.4)
        assert report.confirmed_hard_count == 3

    def test_scores_count_matches_questions(self):
        qs = self._make_questions(n=7)
        report = validate_difficulty(qs, retriever_medium)
        assert len(report.scores) == 7

    def test_question_text_preserved(self):
        qs = self._make_questions(n=2)
        report = validate_difficulty(qs, retriever_easy)
        for hq, ds in zip(qs, report.scores):
            assert ds.question == hq.question


# ---------------------------------------------------------------------------
# CoEvolutionConfig defaults
# ---------------------------------------------------------------------------

class TestCoEvolutionConfig:
    def test_default_questions_per_round(self):
        cfg = CoEvolutionConfig()
        assert cfg.questions_per_round == 5

    def test_default_hard_threshold(self):
        cfg = CoEvolutionConfig()
        assert cfg.hard_threshold == 0.6

    def test_default_max_rounds(self):
        cfg = CoEvolutionConfig()
        assert cfg.max_rounds == 3

    def test_default_seed_none(self):
        cfg = CoEvolutionConfig()
        assert cfg.seed is None

    def test_custom_config(self):
        cfg = CoEvolutionConfig(questions_per_round=10, max_rounds=5, hard_threshold=0.7, seed=42)
        assert cfg.questions_per_round == 10
        assert cfg.max_rounds == 5
        assert cfg.hard_threshold == 0.7
        assert cfg.seed == 42


# ---------------------------------------------------------------------------
# EvolutionRound
# ---------------------------------------------------------------------------

class TestEvolutionRound:
    def test_improvement_potential_normal(self):
        gen = AdversarialGenerator(seed=0)
        generated = gen.generate(simple_passages(), n=4)
        er = EvolutionRound(round_num=0, generated=generated, confirmed_hard=2)
        assert er.improvement_potential() == 0.5

    def test_improvement_potential_all_hard(self):
        gen = AdversarialGenerator(seed=0)
        generated = gen.generate(simple_passages(), n=4)
        er = EvolutionRound(round_num=0, generated=generated, confirmed_hard=4)
        assert er.improvement_potential() == 1.0

    def test_improvement_potential_none_hard(self):
        gen = AdversarialGenerator(seed=0)
        generated = gen.generate(simple_passages(), n=4)
        er = EvolutionRound(round_num=0, generated=generated, confirmed_hard=0)
        assert er.improvement_potential() == 0.0

    def test_improvement_potential_empty_generated(self):
        er = EvolutionRound(round_num=0, generated=[], confirmed_hard=0)
        assert er.improvement_potential() == 0.0

    def test_round_num_stored(self):
        er = EvolutionRound(round_num=2)
        assert er.round_num == 2

    def test_default_report_none(self):
        er = EvolutionRound(round_num=0)
        assert er.report is None

    def test_default_generated_empty(self):
        er = EvolutionRound(round_num=0)
        assert er.generated == []


# ---------------------------------------------------------------------------
# CoEvolutionLoop.run()
# ---------------------------------------------------------------------------

class TestCoEvolutionLoop:
    def test_returns_list(self):
        loop = CoEvolutionLoop()
        result = loop.run(simple_passages(), retriever_hard)
        assert isinstance(result, list)

    def test_length_equals_max_rounds(self):
        cfg = CoEvolutionConfig(max_rounds=3)
        loop = CoEvolutionLoop(cfg)
        result = loop.run(simple_passages(), retriever_hard)
        assert len(result) == 3

    def test_custom_max_rounds(self):
        cfg = CoEvolutionConfig(max_rounds=5)
        loop = CoEvolutionLoop(cfg)
        result = loop.run(simple_passages(), retriever_hard)
        assert len(result) == 5

    def test_each_round_has_generated_questions(self):
        cfg = CoEvolutionConfig(questions_per_round=4, max_rounds=2)
        loop = CoEvolutionLoop(cfg)
        result = loop.run(simple_passages(), retriever_hard)
        for er in result:
            assert len(er.generated) == 4

    def test_each_round_is_evolution_round(self):
        loop = CoEvolutionLoop()
        result = loop.run(simple_passages(), retriever_hard)
        assert all(isinstance(er, EvolutionRound) for er in result)

    def test_golden_queue_grows_with_hard_questions(self):
        cfg = CoEvolutionConfig(questions_per_round=5, max_rounds=2)
        loop = CoEvolutionLoop(cfg)
        queue = []
        loop.run(simple_passages(), retriever_hard, golden_queue=queue)
        # retriever_hard → actual=0.9 → all confirmed hard → 5*2=10 items
        assert len(queue) == 10

    def test_golden_queue_empty_with_easy_retriever(self):
        cfg = CoEvolutionConfig(questions_per_round=5, max_rounds=2)
        loop = CoEvolutionLoop(cfg)
        queue = []
        loop.run(simple_passages(), retriever_easy, golden_queue=queue)
        # retriever_easy → actual=0.1 → none confirmed hard
        assert len(queue) == 0

    def test_none_golden_queue_no_crash(self):
        loop = CoEvolutionLoop()
        result = loop.run(simple_passages(), retriever_hard, golden_queue=None)
        assert len(result) == 3

    def test_round_num_is_sequential(self):
        cfg = CoEvolutionConfig(max_rounds=3)
        loop = CoEvolutionLoop(cfg)
        result = loop.run(simple_passages(), retriever_hard)
        assert [er.round_num for er in result] == [0, 1, 2]

    def test_each_round_has_report(self):
        loop = CoEvolutionLoop()
        result = loop.run(simple_passages(), retriever_hard)
        for er in result:
            assert isinstance(er.report, DifficultyReport)

    def test_confirmed_hard_set_on_round(self):
        cfg = CoEvolutionConfig(questions_per_round=5, max_rounds=1)
        loop = CoEvolutionLoop(cfg)
        result = loop.run(simple_passages(), retriever_hard)
        assert result[0].confirmed_hard == 5

    def test_default_config_used_when_none(self):
        loop = CoEvolutionLoop(config=None)
        result = loop.run(simple_passages(), retriever_hard)
        assert len(result) == 3  # default max_rounds=3

    def test_deterministic_with_seed(self):
        cfg1 = CoEvolutionConfig(seed=7, max_rounds=2, questions_per_round=3)
        cfg2 = CoEvolutionConfig(seed=7, max_rounds=2, questions_per_round=3)
        loop1 = CoEvolutionLoop(cfg1)
        loop2 = CoEvolutionLoop(cfg2)
        r1 = loop1.run(simple_passages(), retriever_medium)
        r2 = loop2.run(simple_passages(), retriever_medium)
        q1 = [hq.question for er in r1 for hq in er.generated]
        q2 = [hq.question for er in r2 for hq in er.generated]
        assert q1 == q2
