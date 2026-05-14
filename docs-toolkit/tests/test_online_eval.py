"""Тесты для docstoolkit.online_eval — continuous online evaluation."""
import sys
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.online_eval import (
    OnlineEvalSampler,
    OnlineEvalStore,
    OnlineEvalRunner,
    OnlineEvalRun,
    DriftReport,
)
from docstoolkit.rag.types import AnswerResult, Passage


# ---- helpers ----

def make_run(
    query: str = "test query",
    precision: float = 0.8,
    recall: float = 0.7,
    f1: float = 0.75,
    citation_precision: float = 0.8,
    answer_score: float = 0.9,
    ts: str | None = None,
    retriever: str = "hybrid",
    answerer: str = "echo",
    duration_ms: int = 100,
) -> OnlineEvalRun:
    if ts is None:
        ts = datetime.now(tz=timezone.utc).isoformat(timespec="seconds")
    return OnlineEvalRun(
        id=uuid.uuid4().hex[:16],
        query=query,
        ts=ts,
        precision=precision,
        recall=recall,
        f1=f1,
        citation_precision=citation_precision,
        answer_score=answer_score,
        retriever=retriever,
        answerer=answerer,
        duration_ms=duration_ms,
    )


def make_answer_result(
    answer: str = "test answer",
    citations: list[dict] | None = None,
    method: str = "hybrid",
    answerer: str = "echo",
    duration_ms: int = 50,
) -> AnswerResult:
    return AnswerResult(
        answer=answer,
        citations=citations or [],
        retrieved_passages=[],
        query="",
        method=method,
        answerer=answerer,
        duration_ms=duration_ms,
    )


@pytest.fixture
def store(tmp_path):
    db = tmp_path / "online_eval.sqlite"
    s = OnlineEvalStore(db_path=db)
    yield s
    s.close()


# ======================================================================
# OnlineEvalSampler
# ======================================================================

class TestOnlineEvalSampler:
    def test_default_rate(self):
        s = OnlineEvalSampler()
        assert s.sample_rate == 0.01

    def test_maybe_sample_determinism(self):
        """Same query always produces same result (no seed)."""
        s = OnlineEvalSampler(sample_rate=0.5)
        query = "what is machine learning"
        results = [s.maybe_sample(query) for _ in range(10)]
        assert len(set(results)) == 1  # all identical

    def test_maybe_sample_different_queries_differ(self):
        """Different queries can produce different sampling decisions."""
        s = OnlineEvalSampler(sample_rate=0.5)
        results = set()
        for i in range(50):
            results.add(s.maybe_sample(f"unique query number {i} text"))
        # With rate=0.5 over 50 queries we should see both True and False
        assert True in results
        assert False in results

    def test_zero_rate_never_samples(self):
        s = OnlineEvalSampler(sample_rate=0.0)
        for i in range(100):
            assert s.maybe_sample(f"query {i}") is False

    def test_full_rate_always_samples(self):
        s = OnlineEvalSampler(sample_rate=1.0)
        for i in range(20):
            assert s.maybe_sample(f"query {i}") is True

    def test_rate_approximately_correct_over_1000_queries(self):
        """Sample rate should be within 10% of target over 1000 queries."""
        s = OnlineEvalSampler(sample_rate=0.1)
        # Use diverse queries to spread across hash buckets
        sampled = sum(
            1 for i in range(1000) if s.maybe_sample(f"query unique text number {i} hello world")
        )
        # 10% of 1000 = 100, allow ±5% absolute tolerance
        assert 50 <= sampled <= 150, f"Expected ~100 sampled, got {sampled}"

    def test_stats_total_seen(self):
        s = OnlineEvalSampler(sample_rate=0.5)
        for i in range(20):
            s.maybe_sample(f"query {i}")
        stats = s.stats()
        assert stats["total_seen"] == 20

    def test_stats_total_sampled_consistent(self):
        s = OnlineEvalSampler(sample_rate=1.0)
        for i in range(10):
            s.maybe_sample(f"query {i}")
        stats = s.stats()
        assert stats["total_sampled"] == 10
        assert stats["effective_rate"] == pytest.approx(1.0)

    def test_stats_zero_seen(self):
        s = OnlineEvalSampler()
        stats = s.stats()
        assert stats["total_seen"] == 0
        assert stats["total_sampled"] == 0
        assert stats["effective_rate"] == 0.0

    def test_with_seed_is_random_but_reproducible(self):
        """Two samplers with the same seed produce identical sequences."""
        s1 = OnlineEvalSampler(sample_rate=0.3, seed=42)
        s2 = OnlineEvalSampler(sample_rate=0.3, seed=42)
        queries = [f"query {i}" for i in range(30)]
        r1 = [s1.maybe_sample(q) for q in queries]
        r2 = [s2.maybe_sample(q) for q in queries]
        assert r1 == r2

    def test_with_seed_differs_from_no_seed(self):
        """Seeded sampler may differ from hash-based for some queries."""
        # At rate=0.5 the hash-based and seeded should sometimes differ
        # This is a smoke test — just ensure no crash
        s_hash = OnlineEvalSampler(sample_rate=0.5, seed=None)
        s_seed = OnlineEvalSampler(sample_rate=0.5, seed=123)
        results_hash = [s_hash.maybe_sample(f"q{i}") for i in range(50)]
        results_seed = [s_seed.maybe_sample(f"q{i}") for i in range(50)]
        # Both should return booleans
        assert all(isinstance(r, bool) for r in results_hash)
        assert all(isinstance(r, bool) for r in results_seed)


# ======================================================================
# OnlineEvalStore
# ======================================================================

class TestOnlineEvalStore:
    def test_save_and_retrieve_run(self, store):
        run = make_run(query="hello world")
        store.save_run(run)
        recent = store.recent_runs(days=7)
        assert len(recent) == 1
        assert recent[0].query == "hello world"

    def test_save_preserves_all_fields(self, store):
        run = make_run(
            query="test",
            precision=0.9,
            recall=0.8,
            f1=0.85,
            citation_precision=0.9,
            answer_score=0.95,
            retriever="bm25",
            answerer="anthropic",
            duration_ms=250,
        )
        store.save_run(run)
        retrieved = store.recent_runs(days=1)[0]
        assert retrieved.precision == pytest.approx(0.9)
        assert retrieved.recall == pytest.approx(0.8)
        assert retrieved.f1 == pytest.approx(0.85)
        assert retrieved.citation_precision == pytest.approx(0.9)
        assert retrieved.answer_score == pytest.approx(0.95)
        assert retrieved.retriever == "bm25"
        assert retrieved.answerer == "anthropic"
        assert retrieved.duration_ms == 250

    def test_recent_runs_filters_by_days(self, store):
        now = datetime.now(tz=timezone.utc)
        old_ts = (now - timedelta(days=10)).isoformat(timespec="seconds")
        new_ts = now.isoformat(timespec="seconds")
        store.save_run(make_run(query="old", ts=old_ts))
        store.save_run(make_run(query="new", ts=new_ts))
        recent = store.recent_runs(days=3)
        queries = {r.query for r in recent}
        assert "new" in queries
        assert "old" not in queries

    def test_recent_runs_empty(self, store):
        assert store.recent_runs(days=7) == []

    def test_current_stats_empty_returns_zeros(self, store):
        stats = store.current_stats(days=7)
        assert stats["precision"] == 0.0
        assert stats["recall"] == 0.0
        assert stats["f1"] == 0.0
        assert stats["citation_precision"] == 0.0
        assert stats["answer_score"] == 0.0

    def test_current_stats_computes_mean(self, store):
        now = datetime.now(tz=timezone.utc).isoformat(timespec="seconds")
        store.save_run(make_run(ts=now, f1=0.6))
        store.save_run(make_run(ts=now, f1=0.8))
        stats = store.current_stats(days=1)
        assert stats["f1"] == pytest.approx(0.7)

    def test_baseline_stats_window(self, store):
        now = datetime.now(tz=timezone.utc)
        # Baseline: 8-14 days ago
        baseline_ts = (now - timedelta(days=10)).isoformat(timespec="seconds")
        # Current: last 7 days
        current_ts = (now - timedelta(days=1)).isoformat(timespec="seconds")
        store.save_run(make_run(ts=baseline_ts, f1=0.5, query="baseline"))
        store.save_run(make_run(ts=current_ts, f1=0.9, query="current"))
        baseline = store.baseline_stats(days_ago_start=14, days_ago_end=7)
        current = store.current_stats(days=7)
        assert baseline["f1"] == pytest.approx(0.5)
        assert current["f1"] == pytest.approx(0.9)

    def test_save_run_idempotent_replace(self, store):
        run = make_run()
        store.save_run(run)
        # Update same ID
        updated = OnlineEvalRun(
            id=run.id, query=run.query, ts=run.ts,
            precision=0.99, recall=0.99, f1=0.99,
            citation_precision=0.99, answer_score=0.99,
            retriever=run.retriever, answerer=run.answerer,
            duration_ms=run.duration_ms,
        )
        store.save_run(updated)  # should not raise
        recent = store.recent_runs(days=7)
        # Only one run (replaced)
        ids = [r.id for r in recent]
        assert ids.count(run.id) == 1


# ======================================================================
# OnlineEvalRunner
# ======================================================================

class TestOnlineEvalRunner:
    def test_maybe_run_returns_none_when_not_sampled(self, store):
        sampler = OnlineEvalSampler(sample_rate=0.0)  # never sample
        runner = OnlineEvalRunner(store=store, sampler=sampler)
        result = make_answer_result()
        run = runner.maybe_run("any query", result)
        assert run is None

    def test_maybe_run_returns_run_when_sampled(self, store):
        sampler = OnlineEvalSampler(sample_rate=1.0)  # always sample
        runner = OnlineEvalRunner(store=store, sampler=sampler)
        result = make_answer_result(answer="some answer")
        run = runner.maybe_run("test query", result)
        assert run is not None
        assert isinstance(run, OnlineEvalRun)
        assert run.query == "test query"

    def test_maybe_run_saves_to_store(self, store):
        sampler = OnlineEvalSampler(sample_rate=1.0)
        runner = OnlineEvalRunner(store=store, sampler=sampler)
        result = make_answer_result()
        runner.maybe_run("saved query", result)
        recent = store.recent_runs(days=1)
        assert any(r.query == "saved query" for r in recent)

    def test_maybe_run_no_golden_match_gives_100_answer_score(self, store):
        """Without golden, expected_answer_contains=[] → score_answer=100 → answer_score=1.0."""
        sampler = OnlineEvalSampler(sample_rate=1.0)
        runner = OnlineEvalRunner(store=store, sampler=sampler, golden_dataset_path=None)
        result = make_answer_result(answer="any answer text")
        run = runner.maybe_run("unmatched unique query xyz", result)
        assert run is not None
        # No expected_answer_contains → answer_score normalized = 1.0
        assert run.answer_score == pytest.approx(1.0)

    def test_maybe_run_with_golden_json(self, store, tmp_path):
        """Loads golden from JSON, matches query, computes real scores."""
        import json
        golden_path = tmp_path / "golden.json"
        golden_data = {
            "items": [
                {
                    "question": "what is machine learning",
                    "expected_answer_contains": ["machine", "learning"],
                    "expected_doc_ids": ["ml_intro.md"],
                }
            ]
        }
        golden_path.write_text(json.dumps(golden_data))

        sampler = OnlineEvalSampler(sample_rate=1.0)
        runner = OnlineEvalRunner(
            store=store,
            golden_dataset_path=golden_path,
            sampler=sampler,
        )
        result = make_answer_result(
            answer="machine learning is a branch of AI",
            citations=[{"doc_id": "ml_intro.md", "title": "ML Intro", "score": 0.9}],
        )
        run = runner.maybe_run("what is machine learning", result)
        assert run is not None
        assert run.answer_score > 0.0  # found "machine" and "learning"
        assert run.precision > 0.0     # cited ml_intro.md

    def test_maybe_run_retriever_and_answerer_captured(self, store):
        sampler = OnlineEvalSampler(sample_rate=1.0)
        runner = OnlineEvalRunner(store=store, sampler=sampler)
        result = make_answer_result(method="bm25", answerer="anthropic")
        run = runner.maybe_run("test", result)
        assert run.retriever == "bm25"
        assert run.answerer == "anthropic"

    def test_load_golden_empty_when_no_path(self, store):
        runner = OnlineEvalRunner(store=store, golden_dataset_path=None)
        golden = runner._load_golden()
        assert golden == []

    def test_load_golden_empty_when_missing_file(self, store, tmp_path):
        runner = OnlineEvalRunner(
            store=store,
            golden_dataset_path=tmp_path / "nonexistent.json",
        )
        golden = runner._load_golden()
        assert golden == []


# ======================================================================
# compute_drift
# ======================================================================

class TestComputeDrift:
    def test_compute_drift_returns_5_reports(self, store):
        runner = OnlineEvalRunner(store=store)
        reports = runner.compute_drift(window_days=7)
        assert len(reports) == 5
        metrics = {r.metric for r in reports}
        assert metrics == {"precision", "recall", "f1", "citation_precision", "answer_score"}

    def test_compute_drift_significant_when_large_delta(self, store):
        now = datetime.now(tz=timezone.utc)
        # Baseline: f1 = 0.3 (2 weeks ago)
        baseline_ts = (now - timedelta(days=10)).isoformat(timespec="seconds")
        # Current: f1 = 0.8 (now)
        current_ts = now.isoformat(timespec="seconds")

        for _ in range(3):
            store.save_run(make_run(ts=baseline_ts, f1=0.3))
        for _ in range(3):
            store.save_run(make_run(ts=current_ts, f1=0.8))

        runner = OnlineEvalRunner(store=store)
        reports = runner.compute_drift(window_days=7)
        f1_report = next(r for r in reports if r.metric == "f1")
        assert f1_report.significant is True
        assert f1_report.delta == pytest.approx(0.5, abs=0.05)

    def test_compute_drift_not_significant_when_small_delta(self, store):
        now = datetime.now(tz=timezone.utc)
        # Both baseline and current have similar f1
        baseline_ts = (now - timedelta(days=10)).isoformat(timespec="seconds")
        current_ts = now.isoformat(timespec="seconds")

        for _ in range(3):
            store.save_run(make_run(ts=baseline_ts, f1=0.75))
        for _ in range(3):
            store.save_run(make_run(ts=current_ts, f1=0.78))

        runner = OnlineEvalRunner(store=store)
        reports = runner.compute_drift(window_days=7)
        f1_report = next(r for r in reports if r.metric == "f1")
        assert f1_report.significant is False

    def test_drift_report_fields(self, store):
        now = datetime.now(tz=timezone.utc).isoformat(timespec="seconds")
        store.save_run(make_run(ts=now, f1=0.6))
        runner = OnlineEvalRunner(store=store)
        reports = runner.compute_drift(window_days=7)
        for report in reports:
            assert isinstance(report.metric, str)
            assert isinstance(report.baseline_value, float)
            assert isinstance(report.current_value, float)
            assert isinstance(report.delta, float)
            assert isinstance(report.significant, bool)
            assert report.window_days == 7

    def test_drift_empty_store_all_zeros(self, store):
        runner = OnlineEvalRunner(store=store)
        reports = runner.compute_drift(window_days=7)
        for r in reports:
            assert r.baseline_value == 0.0
            assert r.current_value == 0.0
            assert r.delta == 0.0
            assert r.significant is False
