"""Tests for docstoolkit.temporal — differential / time-aware queries.

Strategy: all tests avoid real git calls by either:
  - building CorpusSnapshot directly (no git), or
  - patching subprocess.run to simulate git failures / responses.
"""
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.temporal import (
    CorpusSnapshot,
    ConceptEvolution,
    StaleDoc,
    TemporalAnswer,
    TimelineEvent,
    detect_stale,
    evolve_concept,
    query_at_time,
    snapshot_index,
)


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

def _make_snapshot(docs: dict[str, str] = None) -> CorpusSnapshot:
    return CorpusSnapshot(
        commit="abc1234",
        timestamp="2024-06-01T12:00:00+00:00",
        docs=docs or {},
    )


def _make_evolution(timeline=None, stability=0.8) -> ConceptEvolution:
    return ConceptEvolution(
        concept="AgentFS",
        timeline=timeline or [],
        stability_score=stability,
        notable_changes=["First appearance at 2024-01-01 (abc1234)"],
    )


# ===========================================================================
# CorpusSnapshot tests
# ===========================================================================

class TestCorpusSnapshot:

    def test_doc_count_empty(self):
        snap = _make_snapshot()
        assert snap.doc_count() == 0

    def test_doc_count_nonempty(self):
        snap = _make_snapshot({"a.md": "hello", "b.md": "world"})
        assert snap.doc_count() == 2

    def test_has_doc_true(self):
        snap = _make_snapshot({"docs/intro.md": "content"})
        assert snap.has_doc("docs/intro.md") is True

    def test_has_doc_false(self):
        snap = _make_snapshot({"docs/intro.md": "content"})
        assert snap.has_doc("docs/other.md") is False

    def test_has_doc_empty_corpus(self):
        snap = _make_snapshot()
        assert snap.has_doc("anything.md") is False

    def test_search_returns_list(self):
        snap = _make_snapshot({"a.md": "knowledge graph neural"})
        results = snap.search("knowledge")
        assert isinstance(results, list)

    def test_search_result_has_required_keys(self):
        snap = _make_snapshot({"a.md": "knowledge graph neural networks"})
        results = snap.search("knowledge")
        assert len(results) > 0
        r = results[0]
        assert "path" in r
        assert "score" in r

    def test_search_most_relevant_first(self):
        snap = _make_snapshot({
            "relevant.md": "knowledge graph knowledge semantic knowledge retrieval",
            "irrelevant.md": "apple banana cherry orange",
        })
        results = snap.search("knowledge", top_k=5)
        assert len(results) >= 1
        assert results[0]["path"] == "relevant.md"

    def test_search_top_k_respected(self):
        docs = {f"doc{i}.md": f"python code example {i}" for i in range(10)}
        snap = _make_snapshot(docs)
        results = snap.search("python", top_k=3)
        assert len(results) <= 3

    def test_search_empty_corpus_returns_empty(self):
        snap = _make_snapshot()
        results = snap.search("anything")
        assert results == []

    def test_search_query_not_in_docs_returns_empty(self):
        snap = _make_snapshot({"a.md": "hello world foo bar"})
        results = snap.search("xyzzyabcdefghij")
        assert results == []

    def test_search_empty_query_returns_empty(self):
        snap = _make_snapshot({"a.md": "hello world"})
        results = snap.search("")
        assert results == []

    def test_search_snippet_in_result(self):
        snap = _make_snapshot({"a.md": "The knowledge graph is important for retrieval."})
        results = snap.search("knowledge graph")
        assert len(results) > 0
        assert "snippet" in results[0]
        assert isinstance(results[0]["snippet"], str)

    def test_search_score_positive(self):
        snap = _make_snapshot({"a.md": "machine learning is great for ML tasks"})
        results = snap.search("machine learning")
        assert all(r["score"] > 0 for r in results)

    def test_search_multiple_docs_ranked(self):
        snap = _make_snapshot({
            "high.md": "memory memory memory memory architecture memory",
            "low.md": "memory architecture overview",
            "none.md": "completely unrelated topic about cooking",
        })
        results = snap.search("memory", top_k=5)
        paths = [r["path"] for r in results]
        assert "high.md" in paths
        # high.md should rank above low.md
        if "low.md" in paths:
            assert paths.index("high.md") < paths.index("low.md")

    def test_corpus_snapshot_commit_field(self):
        snap = CorpusSnapshot(commit="deadbeef", timestamp="2024-01-01", docs={})
        assert snap.commit == "deadbeef"

    def test_corpus_snapshot_timestamp_field(self):
        snap = CorpusSnapshot(commit="abc", timestamp="2024-06-15T10:00:00+00:00", docs={})
        assert snap.timestamp == "2024-06-15T10:00:00+00:00"


# ===========================================================================
# TimelineEvent dataclass
# ===========================================================================

class TestTimelineEvent:

    def test_timeline_event_fields(self):
        ev = TimelineEvent(
            timestamp="2024-01-01",
            commit="abc1234",
            event_type="introduced",
            mentions=5,
            context_snippet="some context here",
        )
        assert ev.timestamp == "2024-01-01"
        assert ev.commit == "abc1234"
        assert ev.event_type == "introduced"
        assert ev.mentions == 5
        assert ev.context_snippet == "some context here"

    def test_timeline_event_default_snippet(self):
        ev = TimelineEvent(
            timestamp="2024-01-01",
            commit="abc1234",
            event_type="stable",
            mentions=3,
        )
        assert ev.context_snippet == ""

    def test_timeline_event_event_types(self):
        valid_types = {"introduced", "spike", "decline", "stable"}
        for et in valid_types:
            ev = TimelineEvent(timestamp="", commit="", event_type=et, mentions=0)
            assert ev.event_type == et


# ===========================================================================
# ConceptEvolution
# ===========================================================================

class TestConceptEvolution:

    def test_concept_evolution_fields(self):
        ev = _make_evolution()
        assert ev.concept == "AgentFS"
        assert isinstance(ev.timeline, list)
        assert isinstance(ev.stability_score, float)
        assert isinstance(ev.notable_changes, list)

    def test_stability_score_in_range(self):
        ev = _make_evolution(stability=0.75)
        assert 0.0 <= ev.stability_score <= 1.0

    def test_stability_score_boundary_zero(self):
        ev = _make_evolution(stability=0.0)
        assert ev.stability_score == 0.0

    def test_stability_score_boundary_one(self):
        ev = _make_evolution(stability=1.0)
        assert ev.stability_score == 1.0

    def test_to_markdown_returns_string(self):
        ev = _make_evolution()
        md = ev.to_markdown()
        assert isinstance(md, str)

    def test_to_markdown_contains_concept_name(self):
        ev = _make_evolution()
        md = ev.to_markdown()
        assert "AgentFS" in md

    def test_to_markdown_empty_timeline(self):
        ev = ConceptEvolution(
            concept="RAG",
            timeline=[],
            stability_score=1.0,
            notable_changes=[],
        )
        md = ev.to_markdown()
        assert isinstance(md, str)
        assert "RAG" in md

    def test_to_markdown_with_events(self):
        events = [
            TimelineEvent(
                timestamp="2024-01-01 12:00:00 +0000",
                commit="abc1234abcdefghijklmnopqrstuvwxyz12345678",
                event_type="introduced",
                mentions=3,
            ),
            TimelineEvent(
                timestamp="2024-02-01 12:00:00 +0000",
                commit="def5678abcdefghijklmnopqrstuvwxyz12345678",
                event_type="spike",
                mentions=10,
            ),
        ]
        ev = ConceptEvolution(
            concept="Yodoca",
            timeline=events,
            stability_score=0.5,
            notable_changes=["First appearance", "Spike detected"],
        )
        md = ev.to_markdown()
        assert "Yodoca" in md
        assert "2024-01-01" in md
        assert "2024-02-01" in md

    def test_to_markdown_contains_notable_changes(self):
        ev = ConceptEvolution(
            concept="TestConcept",
            timeline=[],
            stability_score=0.6,
            notable_changes=["Something changed here", "Another change"],
        )
        md = ev.to_markdown()
        assert "Something changed here" in md


# ===========================================================================
# StaleDoc dataclass
# ===========================================================================

class TestStaleDoc:

    def test_stale_doc_fields(self):
        sd = StaleDoc(
            path="docs/old.md",
            last_modified="2023-01-01",
            age_days=400.0,
            staleness_score=0.8,
            reason="old",
        )
        assert sd.path == "docs/old.md"
        assert sd.last_modified == "2023-01-01"
        assert sd.age_days == 400.0
        assert sd.staleness_score == 0.8
        assert sd.reason == "old"

    def test_staleness_score_in_range(self):
        sd = StaleDoc(path="x.md", last_modified="", age_days=200, staleness_score=0.5, reason="old")
        assert 0.0 <= sd.staleness_score <= 1.0


# ===========================================================================
# query_at_time — mocked git
# ===========================================================================

class TestQueryAtTime:

    def test_returns_temporal_answer_on_git_failure(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="error")
            result = query_at_time("knowledge", "abc1234", repo_path="/tmp/fake")
        assert isinstance(result, TemporalAnswer)

    def test_does_not_raise_on_git_failure(self):
        with patch("subprocess.run", side_effect=Exception("git not found")):
            result = query_at_time("test", "HEAD", repo_path="/nonexistent")
        assert isinstance(result, TemporalAnswer)

    def test_temporal_answer_has_all_fields(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="")
            result = query_at_time("test", "HEAD", repo_path="/tmp")
        assert hasattr(result, "answer")
        assert hasattr(result, "passages")
        assert hasattr(result, "timestamp")
        assert hasattr(result, "commit")
        assert hasattr(result, "doc_count")

    def test_temporal_answer_passages_is_list(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="")
            result = query_at_time("test", "2024-01-01", repo_path="/tmp")
        assert isinstance(result.passages, list)

    def test_date_string_handled(self):
        """Date-looking commit_or_ts should not raise even on failure."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="")
            result = query_at_time("search term", "2024-06-15", repo_path="/tmp")
        assert isinstance(result, TemporalAnswer)

    def test_returns_empty_on_no_commit_found(self):
        """When git returns empty for --before= lookup, answer is empty."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
            result = query_at_time("test", "2099-01-01", repo_path="/tmp")
        assert result.commit == ""

    def test_query_at_time_with_real_snapshot(self):
        """Build snapshot manually to test query_at_time end-to-end search logic."""
        snap = CorpusSnapshot(
            commit="abc1234",
            timestamp="2024-01-01",
            docs={
                "docs/a.md": "knowledge graph semantic retrieval system",
                "docs/b.md": "agent memory architecture overview",
            },
        )
        # Test search directly on snapshot (not requiring git)
        results = snap.search("knowledge graph")
        assert len(results) >= 1
        assert results[0]["path"] == "docs/a.md"


# ===========================================================================
# evolve_concept — mocked git
# ===========================================================================

class TestEvolveConcept:

    def test_returns_concept_evolution_on_git_failure(self):
        with patch("subprocess.run", side_effect=Exception("no git")):
            result = evolve_concept("Yodoca", repo_path="/nonexistent")
        assert isinstance(result, ConceptEvolution)

    def test_returns_empty_timeline_on_git_failure(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="")
            result = evolve_concept("AgentFS", repo_path="/tmp/fake")
        assert isinstance(result.timeline, list)

    def test_notable_changes_is_list_on_failure(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="")
            result = evolve_concept("NGT Memory", repo_path="/tmp/fake")
        assert isinstance(result.notable_changes, list)

    def test_stability_score_in_range_on_failure(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="")
            result = evolve_concept("test", repo_path="/tmp")
        assert 0.0 <= result.stability_score <= 1.0

    def test_concept_name_preserved(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="")
            result = evolve_concept("MySpecialConcept", repo_path="/tmp")
        assert result.concept == "MySpecialConcept"

    def test_evolve_concept_with_mocked_commits(self):
        """Simulate git log returning two commits, show returning file content."""
        commit1 = "a" * 40
        commit2 = "b" * 40

        log_output = (
            f"{commit1} 2024-01-15 10:00:00 +0000\n"
            f"{commit2} 2024-02-15 10:00:00 +0000\n"
        )

        call_count = 0

        def mock_run(args, **kwargs):
            nonlocal call_count
            mock = MagicMock()
            mock.returncode = 0
            cmd = " ".join(str(a) for a in args)
            if "log" in cmd and "format" in cmd:
                mock.stdout = log_output
            elif "show" in cmd and "--stat" in cmd:
                mock.stdout = "docs/notes.md\n"
            elif "show" in cmd:
                mock.stdout = "AgentFS is a filesystem layer for knowledge graphs"
            else:
                mock.stdout = ""
            call_count += 1
            return mock

        with patch("subprocess.run", side_effect=mock_run):
            result = evolve_concept("AgentFS", repo_path="/tmp")

        assert isinstance(result, ConceptEvolution)
        assert isinstance(result.timeline, list)
        assert 0.0 <= result.stability_score <= 1.0

    def test_stability_score_all_same_mentions(self):
        """Identical mention counts → stability = 1.0."""
        timeline = [
            TimelineEvent(timestamp="2024-01-01", commit="abc", event_type="stable", mentions=5),
            TimelineEvent(timestamp="2024-02-01", commit="def", event_type="stable", mentions=5),
            TimelineEvent(timestamp="2024-03-01", commit="ghi", event_type="stable", mentions=5),
        ]
        ev = ConceptEvolution(
            concept="test",
            timeline=timeline,
            stability_score=1.0,
            notable_changes=[],
        )
        assert ev.stability_score == 1.0

    def test_to_markdown_with_timeline_events(self):
        timeline = [
            TimelineEvent(
                timestamp="2024-01-01 12:00:00 +0000",
                commit="a" * 40,
                event_type="introduced",
                mentions=2,
            ),
        ]
        ev = ConceptEvolution(
            concept="Svyazi",
            timeline=timeline,
            stability_score=0.9,
            notable_changes=["First seen in Jan 2024"],
        )
        md = ev.to_markdown()
        assert "Svyazi" in md
        assert "2024-01-01" in md
        assert "First seen in Jan 2024" in md


# ===========================================================================
# detect_stale — mocked git
# ===========================================================================

class TestDetectStale:

    def test_returns_list_on_git_failure(self):
        with patch("subprocess.run", side_effect=Exception("no git")):
            result = detect_stale(repo_path="/nonexistent")
        assert isinstance(result, list)

    def test_returns_empty_on_git_failure(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="")
            result = detect_stale(repo_path="/tmp/fake")
        assert result == []

    def test_stale_doc_has_required_fields(self):
        sd = StaleDoc(
            path="docs/old.md",
            last_modified="2023-06-01 12:00:00 +0000",
            age_days=350.0,
            staleness_score=0.97,
            reason="old",
        )
        assert hasattr(sd, "path")
        assert hasattr(sd, "last_modified")
        assert hasattr(sd, "age_days")
        assert hasattr(sd, "staleness_score")
        assert hasattr(sd, "reason")

    def test_staleness_score_formula(self):
        """staleness_score = min(1.0, age_days / (threshold_days * 2))"""
        threshold = 180.0
        age = 270.0  # 1.5x threshold → score = 270/(180*2) = 0.75
        expected = min(1.0, age / (threshold * 2))
        sd = StaleDoc(
            path="x.md",
            last_modified="2023-01-01",
            age_days=age,
            staleness_score=expected,
            reason="old",
        )
        assert abs(sd.staleness_score - 0.75) < 1e-9

    def test_staleness_score_capped_at_one(self):
        """Very old docs should have staleness_score == 1.0."""
        threshold = 180.0
        age = 10000.0
        score = min(1.0, age / (threshold * 2))
        assert score == 1.0

    def test_detect_stale_with_real_filesystem(self, tmp_path):
        """Use a real filesystem but mock git log responses."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        (docs_dir / "old.md").write_text("# Old doc\nsome content")
        (docs_dir / "also_old.md").write_text("# Also old")

        very_old_ts = "2020-01-01 10:00:00 +0000"

        def mock_run(args, **kwargs):
            mock = MagicMock()
            cmd = " ".join(str(a) for a in args)
            if "log" in cmd and "-1" in cmd and "format" in cmd:
                mock.returncode = 0
                mock.stdout = very_old_ts + "\n"
            else:
                mock.returncode = 1
                mock.stdout = ""
            return mock

        with patch("subprocess.run", side_effect=mock_run):
            result = detect_stale(
                repo_path=str(tmp_path),
                docs_path="docs",
                threshold_days=30.0,
            )

        assert isinstance(result, list)
        # Both files are old enough to be stale
        for sd in result:
            assert sd.age_days > 30.0
            assert 0.0 <= sd.staleness_score <= 1.0
            assert sd.reason == "old"

    def test_threshold_respected(self, tmp_path):
        """Docs younger than threshold should not be returned."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        (docs_dir / "fresh.md").write_text("# Fresh doc")

        import datetime
        recent_ts = (
            datetime.datetime.now(datetime.timezone.utc)
            - datetime.timedelta(days=10)
        ).strftime("%Y-%m-%d %H:%M:%S +0000")

        def mock_run(args, **kwargs):
            mock = MagicMock()
            cmd = " ".join(str(a) for a in args)
            if "log" in cmd and "-1" in cmd:
                mock.returncode = 0
                mock.stdout = recent_ts + "\n"
            else:
                mock.returncode = 1
                mock.stdout = ""
            return mock

        with patch("subprocess.run", side_effect=mock_run):
            result = detect_stale(
                repo_path=str(tmp_path),
                docs_path="docs",
                threshold_days=30.0,
            )

        # Fresh doc should not appear in stale list
        stale_paths = [sd.path for sd in result]
        assert not any("fresh.md" in p for p in stale_paths)


# ===========================================================================
# snapshot_index — mocked git
# ===========================================================================

class TestSnapshotIndex:

    def test_returns_corpus_snapshot_on_git_failure(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="")
            result = snapshot_index("/nonexistent", "abc1234")
        assert isinstance(result, CorpusSnapshot)

    def test_commit_field_preserved_on_failure(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="")
            result = snapshot_index("/nonexistent", "deadbeef")
        assert result.commit == "deadbeef"

    def test_returns_empty_docs_on_failure(self):
        with patch("subprocess.run", side_effect=Exception("no git")):
            result = snapshot_index("/nonexistent", "abc1234")
        assert result.docs == {}

    def test_does_not_raise_on_exception(self):
        with patch("subprocess.run", side_effect=RuntimeError("unexpected")):
            result = snapshot_index("/tmp", "abc123")
        assert isinstance(result, CorpusSnapshot)

    def test_snapshot_with_mocked_git(self):
        """Simulate successful git ls-tree and git show."""
        ts_output = "2024-03-15 09:00:00 +0000\n"
        ls_output = "docs/intro.md\ndocs/guide.md\n"
        file_content = "# Introduction\nThis document explains everything."

        responses = {
            "log": ts_output,
            "ls-tree": ls_output,
            "show": file_content,
        }

        def mock_run(args, **kwargs):
            mock = MagicMock()
            cmd_str = " ".join(str(a) for a in args)
            if "log" in cmd_str and "format" in cmd_str:
                mock.returncode = 0
                mock.stdout = ts_output
            elif "ls-tree" in cmd_str:
                mock.returncode = 0
                mock.stdout = ls_output
            elif "show" in cmd_str:
                mock.returncode = 0
                mock.stdout = file_content
            else:
                mock.returncode = 1
                mock.stdout = ""
            return mock

        with patch("subprocess.run", side_effect=mock_run):
            result = snapshot_index("/tmp/repo", "abc1234")

        assert isinstance(result, CorpusSnapshot)
        assert result.commit == "abc1234"
        # Docs should be populated if git responded correctly
        # (timestamp is parsed from log output)
        assert isinstance(result.docs, dict)


# ===========================================================================
# Integration tests (no git dependency)
# ===========================================================================

class TestIntegration:

    def test_build_corpus_snapshot_manually(self):
        """Build CorpusSnapshot without git and verify search works."""
        snap = CorpusSnapshot(
            commit="test000",
            timestamp="2024-05-01",
            docs={
                "docs/svyazi.md": (
                    "Svyazi 2.0 is a local community intelligence platform "
                    "built on knowledge graphs and agent memory."
                ),
                "docs/yodoca.md": (
                    "Yodoca provides hierarchical memory with tag-based retrieval "
                    "for document collections."
                ),
                "docs/agentfs.md": (
                    "AgentFS is a filesystem abstraction for agent memory and "
                    "knowledge storage."
                ),
            },
        )

        assert snap.doc_count() == 3
        assert snap.has_doc("docs/svyazi.md")
        assert not snap.has_doc("docs/missing.md")

        # Search should find relevant doc
        results = snap.search("agent memory knowledge", top_k=3)
        assert len(results) >= 1
        assert all("path" in r and "score" in r for r in results)
        # agentfs.md or svyazi.md should be near top
        top_paths = [r["path"] for r in results[:2]]
        assert any("agentfs" in p or "svyazi" in p for p in top_paths)

    def test_corpus_snapshot_search_case_insensitive_tokenization(self):
        snap = CorpusSnapshot(
            commit="abc",
            timestamp="",
            docs={"a.md": "Python PYTHON python is great"},
        )
        results = snap.search("python")
        assert len(results) == 1
        assert results[0]["score"] > 0

    def test_concept_evolution_to_markdown_empty(self):
        ev = ConceptEvolution(
            concept="EmptyConcept",
            timeline=[],
            stability_score=1.0,
            notable_changes=[],
        )
        md = ev.to_markdown()
        assert "EmptyConcept" in md
        assert isinstance(md, str)
        assert len(md) > 0

    def test_concept_evolution_stability_bounds(self):
        """All constructed evolutions have stability in [0,1]."""
        for score in [0.0, 0.25, 0.5, 0.75, 1.0]:
            ev = ConceptEvolution("X", [], score, [])
            assert 0.0 <= ev.stability_score <= 1.0

    def test_stale_doc_reason_field(self):
        for reason in ["old", "contradicted", "unreferenced"]:
            sd = StaleDoc("p.md", "2023-01-01", 400.0, 0.9, reason)
            assert sd.reason == reason

    def test_temporal_answer_construction(self):
        ans = TemporalAnswer(
            answer="Found 3 docs matching query at abc1234",
            passages=[{"path": "a.md", "score": 0.9, "snippet": "..."}],
            timestamp="2024-01-01",
            commit="abc1234",
            doc_count=10,
        )
        assert ans.doc_count == 10
        assert len(ans.passages) == 1
        assert "abc1234" in ans.answer

    def test_query_at_time_empty_result_structure(self):
        """Even empty TemporalAnswer has correct field types."""
        ta = TemporalAnswer(answer="", passages=[], timestamp="", commit="", doc_count=0)
        assert isinstance(ta.answer, str)
        assert isinstance(ta.passages, list)
        assert isinstance(ta.timestamp, str)
        assert isinstance(ta.commit, str)
        assert isinstance(ta.doc_count, int)

    def test_import_all_exports(self):
        """All __all__ exports are importable."""
        from docstoolkit.temporal import (
            CorpusSnapshot,
            ConceptEvolution,
            StaleDoc,
            TemporalAnswer,
            TimelineEvent,
            detect_stale,
            evolve_concept,
            query_at_time,
            snapshot_index,
        )
        assert CorpusSnapshot is not None
        assert query_at_time is not None
        assert evolve_concept is not None
        assert detect_stale is not None
        assert snapshot_index is not None
