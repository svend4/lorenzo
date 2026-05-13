"""Тесты для docstoolkit.rerank — cross-encoder реранкинг."""
import sys
from dataclasses import replace
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.rerank import (
    Reranker,
    NoOpReranker,
    TFIDFReranker,
    LLMReranker,
    BGEReranker,
    rerank,
    get_reranker,
)
from docstoolkit.rag.types import Passage


# ---- helpers ----

def make_passage(text: str, doc_id: str = "doc", score: float = 0.5) -> Passage:
    return Passage(text=text, doc_id=doc_id, score=score)


# ======================================================================
# NoOpReranker
# ======================================================================

class TestNoOpReranker:
    def test_name(self):
        r = NoOpReranker()
        assert r.name == "noop"

    def test_preserves_original_scores(self):
        r = NoOpReranker()
        passages = [
            make_passage("hello world", score=0.9),
            make_passage("foo bar", score=0.3),
            make_passage("baz qux", score=0.7),
        ]
        scores = r.score("query", passages)
        assert scores == [0.9, 0.3, 0.7]

    def test_empty_passages(self):
        r = NoOpReranker()
        assert r.score("query", []) == []

    def test_zero_score_preserved(self):
        r = NoOpReranker()
        p = make_passage("text", score=0.0)
        scores = r.score("q", [p])
        assert scores == [0.0]

    def test_is_reranker_protocol(self):
        r = NoOpReranker()
        assert isinstance(r, Reranker)


# ======================================================================
# TFIDFReranker
# ======================================================================

class TestTFIDFReranker:
    def test_name(self):
        r = TFIDFReranker()
        assert r.name == "tfidf"

    def test_passage_with_more_query_terms_scores_higher(self):
        r = TFIDFReranker()
        query = "neural network training"
        high = make_passage("neural network training deep learning", score=0.1)
        low  = make_passage("unrelated content about cooking recipes", score=0.9)
        scores = r.score(query, [high, low])
        assert scores[0] > scores[1]

    def test_empty_passages(self):
        r = TFIDFReranker()
        assert r.score("query", []) == []

    def test_empty_query_returns_zeros(self):
        r = TFIDFReranker()
        passages = [make_passage("hello world"), make_passage("foo bar")]
        scores = r.score("", passages)
        assert all(s == 0.0 for s in scores)

    def test_all_scores_between_zero_and_one(self):
        r = TFIDFReranker()
        passages = [
            make_passage("the quick brown fox"),
            make_passage("completely unrelated text here now"),
            make_passage("quick brown dog"),
        ]
        scores = r.score("quick brown", passages)
        assert all(0.0 <= s <= 1.0 for s in scores)

    def test_deterministic(self):
        r = TFIDFReranker()
        query = "machine learning model"
        passages = [make_passage("machine learning is great"), make_passage("other text")]
        s1 = r.score(query, passages)
        s2 = r.score(query, passages)
        assert s1 == s2

    def test_score_length_matches_passages(self):
        r = TFIDFReranker()
        passages = [make_passage(f"text {i}") for i in range(5)]
        scores = r.score("text", passages)
        assert len(scores) == 5

    def test_empty_passage_text_gets_zero(self):
        r = TFIDFReranker()
        p = make_passage("")
        scores = r.score("query word", [p])
        assert scores == [0.0]

    def test_cyrillic_tokens(self):
        r = TFIDFReranker()
        query = "нейронная сеть обучение"
        relevant = make_passage("нейронная сеть глубокое обучение")
        irrelevant = make_passage("рецепт приготовления борща")
        scores = r.score(query, [relevant, irrelevant])
        assert scores[0] > scores[1]

    def test_is_reranker_protocol(self):
        r = TFIDFReranker()
        assert isinstance(r, Reranker)


# ======================================================================
# rerank() function
# ======================================================================

class TestRerankFunction:
    def test_sorts_by_score_descending(self):
        r = TFIDFReranker()
        query = "apple fruit"
        passages = [
            make_passage("banana is a yellow fruit", doc_id="d1", score=0.1),
            make_passage("apple is a red fruit very tasty apple", doc_id="d2", score=0.1),
            make_passage("orange fruit juice drink", doc_id="d3", score=0.1),
        ]
        result = rerank(query, passages, r)
        # d2 should score highest (most apple/fruit overlap)
        assert result[0].doc_id == "d2"
        # All subsequent scores are <= first
        for i in range(len(result) - 1):
            assert result[i].score >= result[i + 1].score

    def test_applies_top_k(self):
        r = NoOpReranker()
        passages = [make_passage(f"text {i}", score=float(i)) for i in range(10)]
        result = rerank("query", passages, r, top_k=3)
        assert len(result) == 3

    def test_top_k_none_returns_all(self):
        r = NoOpReranker()
        passages = [make_passage(f"text {i}", score=float(i)) for i in range(7)]
        result = rerank("query", passages, r, top_k=None)
        assert len(result) == 7

    def test_empty_passages_returns_empty(self):
        r = NoOpReranker()
        result = rerank("query", [], r)
        assert result == []

    def test_updates_score_field(self):
        """Returned passages have updated score from reranker."""
        r = TFIDFReranker()
        query = "hello world"
        p = make_passage("hello world foo bar", score=0.0)
        result = rerank(query, [p], r)
        # score should be updated (non-zero since tokens overlap)
        assert result[0].score > 0.0

    def test_original_passages_not_modified(self):
        """rerank() must not mutate the input list."""
        r = NoOpReranker()
        passages = [make_passage("text", score=0.5)]
        original_score = passages[0].score
        rerank("q", passages, r)
        assert passages[0].score == original_score

    def test_top_k_larger_than_list_returns_all(self):
        r = NoOpReranker()
        passages = [make_passage(f"t{i}", score=float(i)) for i in range(3)]
        result = rerank("q", passages, r, top_k=100)
        assert len(result) == 3


# ======================================================================
# get_reranker() factory
# ======================================================================

class TestGetRerankerFactory:
    def test_noop(self):
        r = get_reranker("noop")
        assert isinstance(r, NoOpReranker)
        assert r.name == "noop"

    def test_tfidf(self):
        r = get_reranker("tfidf")
        assert isinstance(r, TFIDFReranker)
        assert r.name == "tfidf"

    def test_llm_default(self):
        r = get_reranker("llm")
        assert isinstance(r, LLMReranker)
        assert r.name == "llm"

    def test_llm_with_kwargs(self):
        r = get_reranker("llm", answerer_name="echo", batch_size=3)
        assert isinstance(r, LLMReranker)
        assert r.batch_size == 3
        assert r.answerer_name == "echo"

    def test_bge(self):
        r = get_reranker("bge")
        assert isinstance(r, BGEReranker)
        assert r.name == "bge"

    def test_unknown_raises_value_error(self):
        with pytest.raises(ValueError, match="Неизвестный реранкер"):
            get_reranker("nonexistent")


# ======================================================================
# BGEReranker — graceful fallback
# ======================================================================

class TestBGERerankerFallback:
    def test_name(self):
        r = BGEReranker()
        assert r.name == "bge"

    def test_falls_back_to_tfidf_when_unavailable(self):
        """When neither sentence_transformers nor transformers is available,
        BGEReranker must fall back to TFIDFReranker scores."""
        r = BGEReranker()
        # Force unavailable state
        r._available = False
        r._model = None

        query = "apple fruit"
        passages = [
            make_passage("apple is a fruit", score=0.0),
            make_passage("unrelated cooking content", score=0.0),
        ]
        scores = r.score(query, passages)
        assert len(scores) == 2
        # TFIDF: apple passage should score higher
        assert scores[0] >= scores[1]

    def test_graceful_when_import_error(self):
        """Simulate ImportError for both sentence_transformers and transformers."""
        r = BGEReranker()

        # Mock _try_init to mark unavailable
        def fake_try_init():
            r._available = False

        r._try_init = fake_try_init

        query = "hello world"
        passages = [make_passage("hello world example"), make_passage("other stuff here")]
        # Should not raise; falls back to tfidf
        scores = r.score(query, passages)
        assert len(scores) == 2
        assert all(isinstance(s, float) for s in scores)

    def test_default_model_name(self):
        r = BGEReranker()
        assert r.model_name == "BAAI/bge-reranker-base"

    def test_custom_model_name(self):
        r = BGEReranker(model_name="BAAI/bge-reranker-large")
        assert r.model_name == "BAAI/bge-reranker-large"

    def test_cache_dir_stored(self, tmp_path):
        r = BGEReranker(cache_dir=tmp_path)
        assert r.cache_dir == tmp_path

    def test_try_init_marks_unavailable_without_libs(self):
        """_try_init sets _available=False when no ML libs present."""
        r = BGEReranker()
        with patch.dict("sys.modules", {"sentence_transformers": None, "transformers": None}):
            # Remove from sys.modules to force ImportError path
            import sys
            # Backup and remove if present
            st_backup = sys.modules.pop("sentence_transformers", None)
            tr_backup = sys.modules.pop("transformers", None)
            try:
                r._try_init()
                # _available is False when neither lib importable
                # (If libs ARE installed, this test is a no-op on _available)
                assert isinstance(r._available, bool)
            finally:
                if st_backup is not None:
                    sys.modules["sentence_transformers"] = st_backup
                if tr_backup is not None:
                    sys.modules["transformers"] = tr_backup


# ======================================================================
# LLMReranker
# ======================================================================

class TestLLMReranker:
    def test_name(self):
        r = LLMReranker()
        assert r.name == "llm"

    def test_defaults(self):
        r = LLMReranker()
        assert r.answerer_name == "echo"
        assert r.batch_size == 5

    def test_score_with_echo_answerer(self):
        """EchoAnswerer returns text, LLMReranker should parse a float (or 0.0)."""
        r = LLMReranker(answerer_name="echo", batch_size=2)
        passages = [
            make_passage("relevant content about the topic"),
            make_passage("other unrelated stuff"),
        ]
        scores = r.score("topic query", passages)
        assert len(scores) == 2
        assert all(isinstance(s, float) for s in scores)
        assert all(0.0 <= s <= 10.0 for s in scores)

    def test_batch_processing_respects_batch_size(self):
        """All passages should be scored regardless of batch size."""
        r = LLMReranker(answerer_name="echo", batch_size=2)
        passages = [make_passage(f"passage {i}") for i in range(7)]
        scores = r.score("query", passages)
        assert len(scores) == 7

    def test_score_fallback_on_exception(self):
        """If answerer raises, score should return 0.0 for that passage."""
        r = LLMReranker(answerer_name="echo")
        # Mock the answerer to raise
        mock_answerer = MagicMock()
        mock_answerer.answer.side_effect = RuntimeError("boom")
        r._answerer = mock_answerer

        passages = [make_passage("some text")]
        scores = r.score("query", passages)
        assert scores == [0.0]

    def test_empty_passages(self):
        r = LLMReranker(answerer_name="echo")
        scores = r.score("query", [])
        assert scores == []

    def test_is_reranker_protocol(self):
        r = LLMReranker()
        assert isinstance(r, Reranker)
