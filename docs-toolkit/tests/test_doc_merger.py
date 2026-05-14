"""Tests for ``docstoolkit.doc_merger``."""
from __future__ import annotations

import pytest

from docstoolkit.doc_merger import (
    DocMerger,
    MergeConflict,
    MergeResult,
    MergeStrategy,
)


# ---------------------------------------------------------------------------
# MergeStrategy
# ---------------------------------------------------------------------------


class TestMergeStrategy:
    def test_has_all_strategies(self):
        names = {s.name for s in MergeStrategy}
        assert {
            "CONCAT",
            "DEDUP_LINES",
            "BY_SECTION",
            "THREE_WAY",
            "INTERLEAVE",
        } <= names

    def test_strategy_values_are_strings(self):
        for s in MergeStrategy:
            assert isinstance(s.value, str)

    def test_strategies_distinct(self):
        values = [s.value for s in MergeStrategy]
        assert len(values) == len(set(values))


# ---------------------------------------------------------------------------
# MergeConflict
# ---------------------------------------------------------------------------


class TestMergeConflict:
    def test_construct(self):
        c = MergeConflict(section="## Intro", version_a="a", version_b="b", line_num=3)
        assert c.section == "## Intro"
        assert c.version_a == "a"
        assert c.version_b == "b"
        assert c.line_num == 3

    def test_equality(self):
        c1 = MergeConflict("s", "a", "b", 1)
        c2 = MergeConflict("s", "a", "b", 1)
        assert c1 == c2

    def test_inequality(self):
        c1 = MergeConflict("s", "a", "b", 1)
        c2 = MergeConflict("s", "a", "b", 2)
        assert c1 != c2


# ---------------------------------------------------------------------------
# MergeResult
# ---------------------------------------------------------------------------


class TestMergeResult:
    def test_default(self):
        r = MergeResult(output="x")
        assert r.output == "x"
        assert r.conflicts == []
        assert r.strategy == MergeStrategy.CONCAT
        assert r.source_count == 0

    def test_had_conflicts_false_when_empty(self):
        r = MergeResult(output="x")
        assert r.had_conflicts is False

    def test_had_conflicts_true(self):
        r = MergeResult(
            output="x",
            conflicts=[MergeConflict("s", "a", "b", 1)],
        )
        assert r.had_conflicts is True

    def test_carries_strategy_and_source_count(self):
        r = MergeResult(
            output="x",
            strategy=MergeStrategy.DEDUP_LINES,
            source_count=4,
        )
        assert r.strategy == MergeStrategy.DEDUP_LINES
        assert r.source_count == 4


# ---------------------------------------------------------------------------
# Concat
# ---------------------------------------------------------------------------


class TestMergeConcat:
    def setup_method(self):
        self.m = DocMerger()

    def test_basic(self):
        out = self.m.merge_concat(["a", "b", "c"])
        assert out == "a\n\nb\n\nc"

    def test_custom_separator(self):
        out = self.m.merge_concat(["a", "b"], separator=" | ")
        assert out == "a | b"

    def test_empty_list(self):
        assert self.m.merge_concat([]) == ""

    def test_single_doc(self):
        assert self.m.merge_concat(["only"]) == "only"

    def test_preserves_internal_newlines(self):
        out = self.m.merge_concat(["a\nb", "c"])
        assert "a\nb" in out
        assert "c" in out


# ---------------------------------------------------------------------------
# Dedup lines
# ---------------------------------------------------------------------------


class TestMergeDedupLines:
    def setup_method(self):
        self.m = DocMerger()

    def test_unique_preserved(self):
        out = self.m.merge_dedup_lines(["a\nb", "b\nc"])
        lines = out.split("\n")
        assert lines == ["a", "b", "c"]

    def test_order_first_seen(self):
        out = self.m.merge_dedup_lines(["x\ny\nz", "y\na\nx"])
        assert out.split("\n") == ["x", "y", "z", "a"]

    def test_all_duplicates(self):
        out = self.m.merge_dedup_lines(["a\nb", "a\nb", "a\nb"])
        assert out.split("\n") == ["a", "b"]

    def test_empty(self):
        assert self.m.merge_dedup_lines([]) == ""

    def test_single_doc_unchanged_when_unique(self):
        out = self.m.merge_dedup_lines(["a\nb\nc"])
        assert out == "a\nb\nc"


# ---------------------------------------------------------------------------
# By-section merge
# ---------------------------------------------------------------------------


class TestMergeBySection:
    def setup_method(self):
        self.m = DocMerger()

    def test_groups_same_heading(self):
        d1 = "# Title\n\nBody1"
        d2 = "# Title\n\nBody2"
        out = self.m.merge_by_section([d1, d2])
        assert out.count("# Title") == 1
        assert "Body1" in out
        assert "Body2" in out

    def test_case_insensitive(self):
        d1 = "## Intro\n\nA"
        d2 = "## INTRO\n\nB"
        out = self.m.merge_by_section([d1, d2])
        assert out.count("## Intro") == 1 or out.count("## INTRO") == 1
        assert "A" in out and "B" in out

    def test_preserves_first_heading_text(self):
        d1 = "## Intro\n\nA"
        d2 = "## intro\n\nB"
        out = self.m.merge_by_section([d1, d2])
        assert "## Intro" in out
        assert "## intro" not in out

    def test_unique_sections_preserved(self):
        d1 = "## A\nA-body"
        d2 = "## B\nB-body"
        out = self.m.merge_by_section([d1, d2])
        assert "## A" in out and "## B" in out
        assert "A-body" in out and "B-body" in out

    def test_preamble_handled(self):
        d1 = "Preamble1\n## H\nbody1"
        d2 = "Preamble2\n## H\nbody2"
        out = self.m.merge_by_section([d1, d2])
        assert "Preamble1" in out
        assert "Preamble2" in out
        assert "## H" in out

    def test_single_doc(self):
        d = "# T\nBody"
        out = self.m.merge_by_section([d])
        assert "# T" in out and "Body" in out


# ---------------------------------------------------------------------------
# Three-way merge — no conflict
# ---------------------------------------------------------------------------


class TestMergeThreeWay:
    def setup_method(self):
        self.m = DocMerger()

    def test_identical_inputs(self):
        result = self.m.merge_three_way("a\nb\nc", "a\nb\nc", "a\nb\nc")
        assert result.output == "a\nb\nc"
        assert result.had_conflicts is False
        assert result.strategy == MergeStrategy.THREE_WAY
        assert result.source_count == 3

    def test_only_a_modified(self):
        base = "x\ny\nz"
        a = "x\nY\nz"
        b = "x\ny\nz"
        result = self.m.merge_three_way(base, a, b)
        assert result.output == "x\nY\nz"
        assert not result.had_conflicts

    def test_only_b_modified(self):
        base = "x\ny\nz"
        a = "x\ny\nz"
        b = "x\nyy\nz"
        result = self.m.merge_three_way(base, a, b)
        assert result.output == "x\nyy\nz"
        assert not result.had_conflicts

    def test_both_modified_same_way(self):
        base = "x\ny\nz"
        a = "x\nY\nz"
        b = "x\nY\nz"
        result = self.m.merge_three_way(base, a, b)
        assert result.output == "x\nY\nz"
        assert not result.had_conflicts

    def test_non_overlapping_modifications(self):
        base = "1\n2\n3\n4\n5"
        a = "1\n2-mod\n3\n4\n5"
        b = "1\n2\n3\n4-mod\n5"
        result = self.m.merge_three_way(base, a, b)
        assert "2-mod" in result.output
        assert "4-mod" in result.output
        assert not result.had_conflicts

    def test_returns_merge_result(self):
        result = self.m.merge_three_way("a", "a", "a")
        assert isinstance(result, MergeResult)


# ---------------------------------------------------------------------------
# Three-way merge — conflict
# ---------------------------------------------------------------------------


class TestMergeThreeWayConflict:
    def setup_method(self):
        self.m = DocMerger()

    def test_conflict_detected(self):
        base = "a\nb\nc"
        a = "a\nB-a\nc"
        b = "a\nB-b\nc"
        result = self.m.merge_three_way(base, a, b)
        assert result.had_conflicts
        assert len(result.conflicts) == 1

    def test_conflict_markers_in_output(self):
        base = "a\nb\nc"
        a = "a\nB-a\nc"
        b = "a\nB-b\nc"
        result = self.m.merge_three_way(base, a, b)
        assert "<<<<<<< A" in result.output
        assert "=======" in result.output
        assert ">>>>>>> B" in result.output
        assert "B-a" in result.output
        assert "B-b" in result.output

    def test_conflict_records_versions(self):
        base = "x\nold\ny"
        a = "x\nnewA\ny"
        b = "x\nnewB\ny"
        result = self.m.merge_three_way(base, a, b)
        c = result.conflicts[0]
        assert "newA" in c.version_a
        assert "newB" in c.version_b

    def test_conflict_line_num_is_int(self):
        base = "a\nb\nc"
        a = "a\nX\nc"
        b = "a\nY\nc"
        result = self.m.merge_three_way(base, a, b)
        assert isinstance(result.conflicts[0].line_num, int)
        assert result.conflicts[0].line_num >= 0

    def test_multiple_conflicts(self):
        base = "a\nb\nc\nd\ne"
        a = "a\nB-a\nc\nD-a\ne"
        b = "a\nB-b\nc\nD-b\ne"
        result = self.m.merge_three_way(base, a, b)
        assert len(result.conflicts) >= 2

    def test_source_count_three(self):
        result = self.m.merge_three_way("a", "b", "c")
        assert result.source_count == 3

    def test_strategy_is_three_way(self):
        result = self.m.merge_three_way("a", "a", "a")
        assert result.strategy == MergeStrategy.THREE_WAY


# ---------------------------------------------------------------------------
# Interleave
# ---------------------------------------------------------------------------


class TestMergeInterleave:
    def setup_method(self):
        self.m = DocMerger()

    def test_basic_round_robin(self):
        out = self.m.merge_interleave(["1\n2\n3", "a\nb\nc"])
        assert out.split("\n") == ["1", "a", "2", "b", "3", "c"]

    def test_unequal_length(self):
        out = self.m.merge_interleave(["1\n2\n3", "a"])
        assert out.split("\n") == ["1", "a", "2", "3"]

    def test_three_sources(self):
        out = self.m.merge_interleave(["x\ny", "1\n2", "a\nb"])
        assert out.split("\n") == ["x", "1", "a", "y", "2", "b"]

    def test_empty_list(self):
        assert self.m.merge_interleave([]) == ""

    def test_single_doc(self):
        out = self.m.merge_interleave(["a\nb\nc"])
        assert out == "a\nb\nc"


# ---------------------------------------------------------------------------
# find_common_sections
# ---------------------------------------------------------------------------


class TestFindCommonSections:
    def setup_method(self):
        self.m = DocMerger()

    def test_basic(self):
        d1 = "## A\nx\n## B\ny"
        d2 = "## A\nq\n## C\nr"
        common = self.m.find_common_sections([d1, d2])
        assert "## A" in common
        assert "## B" not in common
        assert "## C" not in common

    def test_no_common(self):
        d1 = "## A\nx"
        d2 = "## B\ny"
        assert self.m.find_common_sections([d1, d2]) == []

    def test_case_insensitive_match(self):
        d1 = "## Intro\n"
        d2 = "## INTRO\n"
        common = self.m.find_common_sections([d1, d2])
        assert len(common) == 1

    def test_preamble_excluded(self):
        d1 = "before\n## H\n"
        d2 = "preamble2\n## H\n"
        common = self.m.find_common_sections([d1, d2])
        assert "preamble" not in [c.lower() for c in common]

    def test_empty_docs_list(self):
        assert self.m.find_common_sections([]) == []


# ---------------------------------------------------------------------------
# find_unique_sections
# ---------------------------------------------------------------------------


class TestFindUniqueSections:
    def setup_method(self):
        self.m = DocMerger()

    def test_basic(self):
        d1 = "## A\nx\n## B\ny"
        d2 = "## A\nq\n## C\nr"
        unique = self.m.find_unique_sections([d1, d2])
        assert "## B" in unique[0]
        assert "## A" not in unique[0]
        assert "## C" in unique[1]
        assert "## A" not in unique[1]

    def test_all_shared(self):
        d1 = "## A\n"
        d2 = "## A\n"
        unique = self.m.find_unique_sections([d1, d2])
        assert unique[0] == []
        assert unique[1] == []

    def test_returns_dict_indexed_by_doc(self):
        d1 = "## A\n"
        d2 = "## B\n"
        d3 = "## C\n"
        unique = self.m.find_unique_sections([d1, d2, d3])
        assert set(unique.keys()) == {0, 1, 2}
        assert unique[0] == ["## A"]
        assert unique[1] == ["## B"]
        assert unique[2] == ["## C"]

    def test_empty_list(self):
        assert self.m.find_unique_sections([]) == {}


# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------


class TestMergeDispatcher:
    def setup_method(self):
        self.m = DocMerger()

    def test_concat_dispatch(self):
        r = self.m.merge(["a", "b"], MergeStrategy.CONCAT)
        assert r.output == "a\n\nb"
        assert r.strategy == MergeStrategy.CONCAT
        assert r.source_count == 2
        assert not r.had_conflicts

    def test_dedup_dispatch(self):
        r = self.m.merge(["a\nb", "b\nc"], MergeStrategy.DEDUP_LINES)
        assert r.output.split("\n") == ["a", "b", "c"]
        assert r.strategy == MergeStrategy.DEDUP_LINES

    def test_by_section_dispatch(self):
        r = self.m.merge(["## A\n1", "## A\n2"], MergeStrategy.BY_SECTION)
        assert "## A" in r.output
        assert r.strategy == MergeStrategy.BY_SECTION

    def test_three_way_dispatch(self):
        r = self.m.merge(["x", "x", "x"], MergeStrategy.THREE_WAY)
        assert r.strategy == MergeStrategy.THREE_WAY
        assert r.source_count == 3

    def test_three_way_dispatch_wrong_arity(self):
        with pytest.raises(ValueError):
            self.m.merge(["a", "b"], MergeStrategy.THREE_WAY)

    def test_interleave_dispatch(self):
        r = self.m.merge(["a\nb", "1\n2"], MergeStrategy.INTERLEAVE)
        assert r.output.split("\n") == ["a", "1", "b", "2"]
        assert r.strategy == MergeStrategy.INTERLEAVE

    def test_default_strategy_is_concat(self):
        r = self.m.merge(["a", "b"])
        assert r.strategy == MergeStrategy.CONCAT
        assert r.output == "a\n\nb"


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def setup_method(self):
        self.m = DocMerger()

    def test_empty_list_concat(self):
        r = self.m.merge([], MergeStrategy.CONCAT)
        assert r.output == ""
        assert r.source_count == 0

    def test_empty_list_dedup(self):
        r = self.m.merge([], MergeStrategy.DEDUP_LINES)
        assert r.output == ""

    def test_empty_list_by_section(self):
        r = self.m.merge([], MergeStrategy.BY_SECTION)
        assert r.output == ""

    def test_empty_list_interleave(self):
        r = self.m.merge([], MergeStrategy.INTERLEAVE)
        assert r.output == ""

    def test_single_doc_all_strategies(self):
        d = "## Title\nBody"
        for strat in (
            MergeStrategy.CONCAT,
            MergeStrategy.DEDUP_LINES,
            MergeStrategy.BY_SECTION,
            MergeStrategy.INTERLEAVE,
        ):
            r = self.m.merge([d], strat)
            assert "Body" in r.output
            assert r.source_count == 1

    def test_identical_docs_concat(self):
        r = self.m.merge(["abc", "abc"], MergeStrategy.CONCAT)
        assert r.output == "abc\n\nabc"

    def test_identical_docs_dedup_collapses(self):
        r = self.m.merge(["a\nb", "a\nb"], MergeStrategy.DEDUP_LINES)
        assert r.output.split("\n") == ["a", "b"]

    def test_blank_doc_concat(self):
        r = self.m.merge(["", "x"], MergeStrategy.CONCAT)
        assert r.output == "\n\nx"

    def test_three_way_all_empty(self):
        r = self.m.merge_three_way("", "", "")
        assert r.output == ""
        assert not r.had_conflicts
