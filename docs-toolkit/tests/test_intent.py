"""Tests for query intent classification and routing (M4)."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.intent import (
    Intent,
    IntentClassifier,
    IntentRouter,
    PipelineConfig,
    FACTOID,
    EXPLANATION,
    COMPARISON,
    SYNTHESIS,
    OPINION,
    INSTRUCTION,
    UNKNOWN,
)
from docstoolkit.intent.classifier import _has_two_named_entities, _word_count


# ---------------------------------------------------------------------------
# Label constants
# ---------------------------------------------------------------------------

def test_label_constants_are_strings():
    assert FACTOID == "factoid"
    assert EXPLANATION == "explanation"
    assert COMPARISON == "comparison"
    assert SYNTHESIS == "synthesis"
    assert OPINION == "opinion"
    assert INSTRUCTION == "instruction"
    assert UNKNOWN == "unknown"


# ---------------------------------------------------------------------------
# Intent dataclass
# ---------------------------------------------------------------------------

def test_intent_dataclass():
    intent = Intent(label=FACTOID, confidence=0.9)
    assert intent.label == FACTOID
    assert intent.confidence == 0.9
    assert intent.extracted == {}


def test_intent_dataclass_extracted():
    intent = Intent(label=COMPARISON, confidence=0.85, extracted={"entities": ["A", "B"]})
    assert intent.extracted == {"entities": ["A", "B"]}


# ---------------------------------------------------------------------------
# IntentClassifier — Russian patterns
# ---------------------------------------------------------------------------

def test_factoid_ru_chto_takoe():
    clf = IntentClassifier()
    intent = clf.classify("что такое RAG?")
    assert intent.label == FACTOID
    assert intent.confidence >= 0.5


def test_factoid_ru_kto_takoy():
    clf = IntentClassifier()
    intent = clf.classify("кто такой инженер по данным?")
    assert intent.label == FACTOID


def test_factoid_ru_kogda():
    clf = IntentClassifier()
    intent = clf.classify("когда появился RAG?")
    assert intent.label == FACTOID


def test_explanation_ru_kak_rabotaet():
    clf = IntentClassifier()
    intent = clf.classify("как работает BM25?")
    assert intent.label == EXPLANATION
    assert intent.confidence >= 0.5


def test_explanation_ru_pochemu():
    clf = IntentClassifier()
    intent = clf.classify("почему агент не запоминает контекст?")
    assert intent.label == EXPLANATION


def test_explanation_ru_obyasni():
    clf = IntentClassifier()
    intent = clf.classify("объясни принцип работы векторного поиска")
    assert intent.label == EXPLANATION


def test_comparison_ru_sravni():
    clf = IntentClassifier()
    intent = clf.classify("сравни Yodoca и NGT Memory")
    assert intent.label == COMPARISON


def test_comparison_ru_sravni_entities():
    clf = IntentClassifier()
    # Use "Memory" (mixed-case) instead of "NGT" (all-caps) since entity extraction
    # requires at least one lowercase letter after the initial capital.
    intent = clf.classify("сравни Yodoca и Memory Engine")
    assert intent.label == COMPARISON
    assert "entities" in intent.extracted
    entities = intent.extracted["entities"]
    assert any("Yodoca" in e for e in entities)
    assert any("Memory" in e or "Engine" in e for e in entities)


def test_comparison_ru_chem_otlichaetsya():
    clf = IntentClassifier()
    intent = clf.classify("чем отличается BM25 от TF-IDF?")
    assert intent.label == COMPARISON


def test_synthesis_ru_obobshchi():
    clf = IntentClassifier()
    intent = clf.classify("обобщи всё про memory")
    assert intent.label == SYNTHESIS


def test_synthesis_ru_summarize():
    clf = IntentClassifier()
    intent = clf.classify("суммаризуй статью про AgentFS")
    assert intent.label == SYNTHESIS


def test_instruction_ru_kak_sdelat():
    clf = IntentClassifier()
    intent = clf.classify("как установить docs-toolkit?")
    assert intent.label == INSTRUCTION


def test_instruction_ru_instruktsiya():
    clf = IntentClassifier()
    intent = clf.classify("инструкция по настройке MCP сервера")
    assert intent.label == INSTRUCTION


def test_instruction_ru_shagi():
    clf = IntentClassifier()
    intent = clf.classify("шаги для деплоя")
    assert intent.label == INSTRUCTION


def test_opinion_ru_otsenki():
    clf = IntentClassifier()
    intent = clf.classify("оцени архитектуру Yodoca")
    assert intent.label == OPINION


def test_opinion_ru_luchshiy():
    clf = IntentClassifier()
    intent = clf.classify("лучший инструмент для RAG?")
    assert intent.label == OPINION


# ---------------------------------------------------------------------------
# IntentClassifier — English patterns
# ---------------------------------------------------------------------------

def test_factoid_en_what_is():
    clf = IntentClassifier()
    intent = clf.classify("what is RAG?")
    assert intent.label == FACTOID
    assert intent.confidence >= 0.5


def test_factoid_en_who_is():
    clf = IntentClassifier()
    intent = clf.classify("who is the author?")
    assert intent.label == FACTOID


def test_explanation_en_how_does():
    clf = IntentClassifier()
    intent = clf.classify("how does BM25 work?")
    assert intent.label == EXPLANATION


def test_explanation_en_why():
    clf = IntentClassifier()
    intent = clf.classify("why does the agent fail to remember?")
    assert intent.label == EXPLANATION


def test_explanation_en_explain():
    clf = IntentClassifier()
    intent = clf.classify("explain the concept of RAG retrieval")
    assert intent.label == EXPLANATION


def test_comparison_en_vs():
    clf = IntentClassifier()
    intent = clf.classify("BM25 vs TF-IDF performance")
    assert intent.label == COMPARISON


def test_comparison_en_compare():
    clf = IntentClassifier()
    intent = clf.classify("compare Yodoca and NGT Memory approaches")
    assert intent.label == COMPARISON


def test_comparison_en_difference_between():
    clf = IntentClassifier()
    intent = clf.classify("what is the difference between BM25 and TF-IDF?")
    assert intent.label == COMPARISON


def test_synthesis_en_summarize():
    clf = IntentClassifier()
    intent = clf.classify("summarize everything about the memory layer")
    assert intent.label == SYNTHESIS


def test_synthesis_en_overview_of():
    clf = IntentClassifier()
    intent = clf.classify("give an overview of the RAG pipeline")
    assert intent.label == SYNTHESIS


def test_instruction_en_how_to():
    clf = IntentClassifier()
    intent = clf.classify("how to install docs-toolkit?")
    assert intent.label == INSTRUCTION


def test_instruction_en_steps_to():
    clf = IntentClassifier()
    intent = clf.classify("steps to deploy the service")
    assert intent.label == INSTRUCTION


def test_opinion_en_best():
    clf = IntentClassifier()
    # "what is" (factoid, 0.92) beats "best" (opinion, 0.80) when combined.
    # Use a query without factoid trigger words.
    intent = clf.classify("which is the best retrieval method?")
    assert intent.label == OPINION


def test_opinion_en_recommend():
    clf = IntentClassifier()
    intent = clf.classify("recommend a memory framework")
    assert intent.label == OPINION


def test_opinion_en_opinion_on():
    clf = IntentClassifier()
    intent = clf.classify("give your opinion on Yodoca")
    assert intent.label == OPINION


# ---------------------------------------------------------------------------
# Unknown / low confidence
# ---------------------------------------------------------------------------

def test_unknown_gibberish():
    clf = IntentClassifier()
    intent = clf.classify("xyz abc def ghi jkl")
    assert intent.label == UNKNOWN


def test_unknown_low_confidence_is_unknown():
    clf = IntentClassifier()
    intent = clf.classify("xyz abc")
    # Either UNKNOWN or confidence < 0.5
    assert intent.label == UNKNOWN or intent.confidence < 0.5


def test_classify_returns_intent_dataclass():
    clf = IntentClassifier()
    result = clf.classify("что такое RAG?")
    assert isinstance(result, Intent)
    assert isinstance(result.label, str)
    assert isinstance(result.confidence, float)
    assert isinstance(result.extracted, dict)


# ---------------------------------------------------------------------------
# extract_entities
# ---------------------------------------------------------------------------

def test_extract_entities_capitalized():
    clf = IntentClassifier()
    # Entity extraction matches [A-ZА-Я][a-zа-яё]{1,} — requires at least 1 lowercase.
    # "NGT" is all-caps so won't match; use "Memory" (mixed case) instead.
    entities = clf.extract_entities("сравни Yodoca и Memory Engine")
    assert "Yodoca" in entities
    assert "Memory" in entities or "Engine" in entities


def test_extract_entities_quoted():
    clf = IntentClassifier()
    entities = clf.extract_entities('compare "BM25 algorithm" and "TF-IDF"')
    assert any("BM25 algorithm" in e for e in entities)


def test_extract_entities_empty():
    clf = IntentClassifier()
    entities = clf.extract_entities("how does this work")
    assert isinstance(entities, list)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def test_word_count():
    assert _word_count("one two three") == 3
    assert _word_count("one") == 1
    # "".split() returns [] in Python, so empty string → 0 words
    assert _word_count("") == 0


def test_has_two_named_entities_true():
    # Pattern requires [A-ZА-Я][a-zа-яё]{1,} — "NGT" (all caps) won't match.
    # Use "Yodoca" and "Memory" which are mixed-case.
    assert _has_two_named_entities("Yodoca and Memory")


def test_has_two_named_entities_false():
    assert not _has_two_named_entities("simple lowercase query")


# ---------------------------------------------------------------------------
# PipelineConfig
# ---------------------------------------------------------------------------

def test_pipeline_config_defaults():
    cfg = PipelineConfig()
    assert cfg.retriever == "hybrid"
    assert cfg.top_k == 5
    assert cfg.prompt_id == ""
    assert cfg.post_processor == ""
    assert cfg.use_mapreduce is False
    assert cfg.use_hierarchical is False


def test_pipeline_config_custom():
    cfg = PipelineConfig(retriever="keyword", top_k=3, post_processor="compare")
    assert cfg.retriever == "keyword"
    assert cfg.top_k == 3
    assert cfg.post_processor == "compare"


# ---------------------------------------------------------------------------
# IntentRouter
# ---------------------------------------------------------------------------

def test_router_route_factoid():
    router = IntentRouter()
    intent, cfg = router.route("что такое RAG?")
    assert intent.label == FACTOID
    assert cfg.retriever == "keyword"
    assert cfg.top_k == 3


def test_router_route_explanation():
    router = IntentRouter()
    intent, cfg = router.route("как работает BM25?")
    assert intent.label == EXPLANATION
    assert cfg.retriever == "hybrid"
    assert cfg.top_k == 5


def test_router_route_comparison():
    router = IntentRouter()
    intent, cfg = router.route("сравни Yodoca и NGT Memory")
    assert intent.label == COMPARISON
    assert cfg.top_k == 10
    assert cfg.post_processor == "compare"


def test_router_route_synthesis():
    router = IntentRouter()
    intent, cfg = router.route("обобщи всё про memory")
    assert intent.label == SYNTHESIS
    assert cfg.top_k == 20
    assert cfg.use_mapreduce is True


def test_router_route_instruction():
    router = IntentRouter()
    intent, cfg = router.route("как установить docs-toolkit?")
    assert intent.label == INSTRUCTION
    assert cfg.post_processor == "steps"


def test_router_route_opinion():
    router = IntentRouter()
    intent, cfg = router.route("оцени архитектуру Yodoca")
    assert intent.label == OPINION
    assert cfg.retriever == "semantic"
    assert cfg.top_k == 7


def test_router_route_unknown():
    router = IntentRouter()
    intent, cfg = router.route("xyz abc def")
    assert intent.label == UNKNOWN
    assert isinstance(cfg, PipelineConfig)


def test_router_configure_overrides_default():
    router = IntentRouter()
    custom = PipelineConfig(retriever="semantic", top_k=15)
    router.configure(FACTOID, custom)
    _, cfg = router.route("что такое RAG?")
    assert cfg.retriever == "semantic"
    assert cfg.top_k == 15


def test_router_configure_does_not_affect_other_intents():
    router = IntentRouter()
    router.configure(FACTOID, PipelineConfig(top_k=99))
    _, cfg_explain = router.route("как работает BM25?")
    assert cfg_explain.top_k != 99


def test_router_route_returns_tuple():
    router = IntentRouter()
    result = router.route("что такое RAG?")
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert isinstance(result[0], Intent)
    assert isinstance(result[1], PipelineConfig)


def test_router_custom_classifier():
    class AlwaysFactoid:
        def classify(self, query: str) -> Intent:
            return Intent(label=FACTOID, confidence=1.0)

    router = IntentRouter(classifier=AlwaysFactoid())
    intent, _ = router.route("anything at all")
    assert intent.label == FACTOID


# ---------------------------------------------------------------------------
# route_and_log
# ---------------------------------------------------------------------------

def test_route_and_log_writes_json(tmp_path):
    log_path = tmp_path / "intent_log.jsonl"
    router = IntentRouter()
    router.route_and_log("что такое RAG?", log_path=log_path)
    assert log_path.exists()
    lines = log_path.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1
    entry = json.loads(lines[0])
    assert entry["query"] == "что такое RAG?"
    assert entry["intent"] == FACTOID
    assert "confidence" in entry
    assert "pipeline" in entry


def test_route_and_log_appends(tmp_path):
    log_path = tmp_path / "intent_log.jsonl"
    router = IntentRouter()
    router.route_and_log("что такое RAG?", log_path=log_path)
    router.route_and_log("как работает BM25?", log_path=log_path)
    lines = log_path.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 2


def test_route_and_log_no_path_no_crash():
    router = IntentRouter()
    intent, cfg = router.route_and_log("что такое RAG?", log_path=None)
    assert intent.label == FACTOID


def test_route_and_log_creates_parent_dirs(tmp_path):
    log_path = tmp_path / "subdir" / "deeper" / "log.jsonl"
    router = IntentRouter()
    router.route_and_log("test query", log_path=log_path)
    assert log_path.exists()


def test_route_and_log_json_contains_pipeline(tmp_path):
    log_path = tmp_path / "log.jsonl"
    router = IntentRouter()
    router.route_and_log("обобщи всё про memory", log_path=log_path)
    entry = json.loads(log_path.read_text(encoding="utf-8").strip())
    pipeline = entry["pipeline"]
    assert "retriever" in pipeline
    assert "top_k" in pipeline
    assert "use_mapreduce" in pipeline


def test_route_and_log_returns_same_as_route():
    router = IntentRouter()
    query = "что такое RAG?"
    intent1, cfg1 = router.route(query)
    intent2, cfg2 = router.route_and_log(query, log_path=None)
    assert intent1.label == intent2.label
    assert cfg1.top_k == cfg2.top_k
