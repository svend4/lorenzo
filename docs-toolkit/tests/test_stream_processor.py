"""Tests for ``docstoolkit.stream_processor`` (E173)."""

from __future__ import annotations

import pytest

from docstoolkit.stream_processor import Stream


# ---------------------------------------------------------------------------
# Basic construction
# ---------------------------------------------------------------------------
class TestStreamBasic:
    def test_from_list(self):
        assert Stream([1, 2, 3]).to_list() == [1, 2, 3]

    def test_from_generator(self):
        def gen():
            yield 1
            yield 2
            yield 3

        assert Stream(gen()).to_list() == [1, 2, 3]

    def test_from_empty_list(self):
        assert Stream([]).to_list() == []

    def test_from_range(self):
        assert Stream(range(5)).to_list() == [0, 1, 2, 3, 4]

    def test_from_none_raises(self):
        with pytest.raises(TypeError):
            Stream(None)

    def test_iter_protocol(self):
        s = Stream([10, 20, 30])
        result = [x for x in s]
        assert result == [10, 20, 30]


# ---------------------------------------------------------------------------
# map
# ---------------------------------------------------------------------------
class TestMap:
    def test_map_double(self):
        assert Stream([1, 2, 3]).map(lambda x: x * 2).to_list() == [2, 4, 6]

    def test_map_empty(self):
        assert Stream([]).map(lambda x: x + 1).to_list() == []

    def test_map_chain(self):
        assert (
            Stream([1, 2, 3])
            .map(lambda x: x + 1)
            .map(lambda x: x * 10)
            .to_list()
        ) == [20, 30, 40]


# ---------------------------------------------------------------------------
# filter
# ---------------------------------------------------------------------------
class TestFilter:
    def test_filter_even(self):
        assert Stream(range(6)).filter(lambda x: x % 2 == 0).to_list() == [0, 2, 4]

    def test_filter_none_match(self):
        assert Stream([1, 3, 5]).filter(lambda x: x % 2 == 0).to_list() == []

    def test_filter_all_match(self):
        assert Stream([2, 4, 6]).filter(lambda x: x % 2 == 0).to_list() == [2, 4, 6]


# ---------------------------------------------------------------------------
# flat_map
# ---------------------------------------------------------------------------
class TestFlatMap:
    def test_flat_map_lists(self):
        result = Stream([1, 2, 3]).flat_map(lambda x: [x, x * 10]).to_list()
        assert result == [1, 10, 2, 20, 3, 30]

    def test_flat_map_strings(self):
        assert Stream(["ab", "cd"]).flat_map(iter).to_list() == ["a", "b", "c", "d"]

    def test_flat_map_empty_inner(self):
        assert Stream([1, 2, 3]).flat_map(lambda x: []).to_list() == []


# ---------------------------------------------------------------------------
# take / skip
# ---------------------------------------------------------------------------
class TestTakeSkip:
    def test_take(self):
        assert Stream(range(10)).take(3).to_list() == [0, 1, 2]

    def test_take_more_than_available(self):
        assert Stream([1, 2]).take(5).to_list() == [1, 2]

    def test_take_zero(self):
        assert Stream(range(5)).take(0).to_list() == []

    def test_take_negative_raises(self):
        with pytest.raises(ValueError):
            Stream(range(5)).take(-1)

    def test_skip(self):
        assert Stream(range(5)).skip(2).to_list() == [2, 3, 4]

    def test_skip_more_than_available(self):
        assert Stream([1, 2]).skip(5).to_list() == []

    def test_skip_zero(self):
        assert Stream([1, 2, 3]).skip(0).to_list() == [1, 2, 3]

    def test_skip_negative_raises(self):
        with pytest.raises(ValueError):
            Stream([1, 2]).skip(-1)


# ---------------------------------------------------------------------------
# distinct
# ---------------------------------------------------------------------------
class TestDistinct:
    def test_distinct_ints(self):
        assert Stream([1, 2, 2, 3, 1, 4]).distinct().to_list() == [1, 2, 3, 4]

    def test_distinct_preserves_order(self):
        assert Stream([3, 1, 2, 1, 3]).distinct().to_list() == [3, 1, 2]

    def test_distinct_with_key(self):
        items = [{"id": 1, "v": "a"}, {"id": 2, "v": "b"}, {"id": 1, "v": "c"}]
        result = Stream(items).distinct(key=lambda d: d["id"]).to_list()
        assert result == [{"id": 1, "v": "a"}, {"id": 2, "v": "b"}]

    def test_distinct_empty(self):
        assert Stream([]).distinct().to_list() == []


# ---------------------------------------------------------------------------
# sort
# ---------------------------------------------------------------------------
class TestSort:
    def test_sort_default(self):
        assert Stream([3, 1, 2]).sort().to_list() == [1, 2, 3]

    def test_sort_reverse(self):
        assert Stream([1, 3, 2]).sort(reverse=True).to_list() == [3, 2, 1]

    def test_sort_with_key(self):
        items = [("a", 3), ("b", 1), ("c", 2)]
        result = Stream(items).sort(key=lambda t: t[1]).to_list()
        assert result == [("b", 1), ("c", 2), ("a", 3)]


# ---------------------------------------------------------------------------
# reverse
# ---------------------------------------------------------------------------
class TestReverse:
    def test_reverse(self):
        assert Stream([1, 2, 3]).reverse().to_list() == [3, 2, 1]

    def test_reverse_empty(self):
        assert Stream([]).reverse().to_list() == []


# ---------------------------------------------------------------------------
# group_by
# ---------------------------------------------------------------------------
class TestGroupBy:
    def test_group_by_parity(self):
        result = Stream(range(6)).group_by(lambda x: x % 2).to_list()
        assert result == [(0, [0, 2, 4]), (1, [1, 3, 5])]

    def test_group_by_unsorted_input(self):
        result = Stream([5, 1, 4, 2, 3]).group_by(lambda x: x % 2).to_list()
        # Sorted globally by key before grouping
        keys = [k for k, _ in result]
        assert keys == [0, 1]
        groups = {k: v for k, v in result}
        assert sorted(groups[0]) == [2, 4]
        assert sorted(groups[1]) == [1, 3, 5]


# ---------------------------------------------------------------------------
# window
# ---------------------------------------------------------------------------
class TestWindow:
    def test_window_size_2(self):
        assert Stream([1, 2, 3, 4]).window(2).to_list() == [
            (1, 2),
            (2, 3),
            (3, 4),
        ]

    def test_window_size_3(self):
        assert Stream([1, 2, 3, 4, 5]).window(3).to_list() == [
            (1, 2, 3),
            (2, 3, 4),
            (3, 4, 5),
        ]

    def test_window_step_2(self):
        assert Stream(range(6)).window(2, step=2).to_list() == [(0, 1), (2, 3), (4, 5)]

    def test_window_too_small(self):
        assert Stream([1, 2]).window(3).to_list() == []

    def test_window_invalid_size(self):
        with pytest.raises(ValueError):
            Stream([1]).window(0)

    def test_window_invalid_step(self):
        with pytest.raises(ValueError):
            Stream([1, 2, 3]).window(2, step=0)


# ---------------------------------------------------------------------------
# chunked
# ---------------------------------------------------------------------------
class TestChunked:
    def test_chunked_even(self):
        assert Stream([1, 2, 3, 4]).chunked(2).to_list() == [(1, 2), (3, 4)]

    def test_chunked_uneven(self):
        assert Stream([1, 2, 3, 4, 5]).chunked(2).to_list() == [(1, 2), (3, 4), (5,)]

    def test_chunked_empty(self):
        assert Stream([]).chunked(3).to_list() == []

    def test_chunked_invalid_size(self):
        with pytest.raises(ValueError):
            Stream([1]).chunked(0)


# ---------------------------------------------------------------------------
# peek / tap
# ---------------------------------------------------------------------------
class TestPeek:
    def test_peek_side_effect(self):
        seen = []
        result = Stream([1, 2, 3]).peek(seen.append).to_list()
        assert result == [1, 2, 3]
        assert seen == [1, 2, 3]

    def test_peek_does_not_modify(self):
        result = Stream([1, 2]).peek(lambda x: x * 100).to_list()
        assert result == [1, 2]

    def test_tap_alias(self):
        seen = []
        result = Stream([10, 20]).tap(seen.append).to_list()
        assert result == [10, 20]
        assert seen == [10, 20]


# ---------------------------------------------------------------------------
# concat
# ---------------------------------------------------------------------------
class TestConcat:
    def test_concat_list(self):
        assert Stream([1, 2]).concat([3, 4]).to_list() == [1, 2, 3, 4]

    def test_concat_generator(self):
        def gen():
            yield 10
            yield 20

        assert Stream([1]).concat(gen()).to_list() == [1, 10, 20]

    def test_concat_empty(self):
        assert Stream([]).concat([1, 2]).to_list() == [1, 2]


# ---------------------------------------------------------------------------
# zip
# ---------------------------------------------------------------------------
class TestZip:
    def test_zip_equal_length(self):
        assert Stream([1, 2, 3]).zip(["a", "b", "c"]).to_list() == [
            (1, "a"),
            (2, "b"),
            (3, "c"),
        ]

    def test_zip_shorter_other(self):
        assert Stream([1, 2, 3]).zip(["a"]).to_list() == [(1, "a")]

    def test_zip_empty(self):
        assert Stream([]).zip([1, 2]).to_list() == []


# ---------------------------------------------------------------------------
# count
# ---------------------------------------------------------------------------
class TestCount:
    def test_count_basic(self):
        assert Stream([1, 2, 3, 4]).count() == 4

    def test_count_empty(self):
        assert Stream([]).count() == 0

    def test_count_after_filter(self):
        assert Stream(range(10)).filter(lambda x: x % 2 == 0).count() == 5


# ---------------------------------------------------------------------------
# first / first_or_none
# ---------------------------------------------------------------------------
class TestFirst:
    def test_first(self):
        assert Stream([10, 20, 30]).first() == 10

    def test_first_empty_raises(self):
        with pytest.raises(StopIteration):
            Stream([]).first()

    def test_first_or_none(self):
        assert Stream([1, 2]).first_or_none() == 1

    def test_first_or_none_empty(self):
        assert Stream([]).first_or_none() is None


# ---------------------------------------------------------------------------
# last
# ---------------------------------------------------------------------------
class TestLast:
    def test_last(self):
        assert Stream([1, 2, 3]).last() == 3

    def test_last_single(self):
        assert Stream(["x"]).last() == "x"

    def test_last_empty_raises(self):
        with pytest.raises(StopIteration):
            Stream([]).last()


# ---------------------------------------------------------------------------
# any / all
# ---------------------------------------------------------------------------
class TestAnyAll:
    def test_any_no_predicate_true(self):
        assert Stream([0, 0, 1]).any() is True

    def test_any_no_predicate_false(self):
        assert Stream([0, 0, 0]).any() is False

    def test_any_with_predicate(self):
        assert Stream([1, 2, 3]).any(lambda x: x > 2) is True
        assert Stream([1, 2, 3]).any(lambda x: x > 10) is False

    def test_all_true(self):
        assert Stream([2, 4, 6]).all(lambda x: x % 2 == 0) is True

    def test_all_false(self):
        assert Stream([2, 3, 4]).all(lambda x: x % 2 == 0) is False

    def test_all_empty(self):
        assert Stream([]).all(lambda x: False) is True


# ---------------------------------------------------------------------------
# reduce
# ---------------------------------------------------------------------------
class TestReduce:
    def test_reduce_sum(self):
        assert Stream([1, 2, 3, 4]).reduce(lambda a, b: a + b) == 10

    def test_reduce_with_initial(self):
        assert Stream([1, 2, 3]).reduce(lambda a, b: a + b, initial=100) == 106

    def test_reduce_empty_raises(self):
        with pytest.raises(TypeError):
            Stream([]).reduce(lambda a, b: a + b)

    def test_reduce_empty_with_initial(self):
        assert Stream([]).reduce(lambda a, b: a + b, initial=0) == 0


# ---------------------------------------------------------------------------
# min / max
# ---------------------------------------------------------------------------
class TestMinMax:
    def test_min(self):
        assert Stream([3, 1, 4, 1, 5]).min() == 1

    def test_max(self):
        assert Stream([3, 1, 4, 1, 5]).max() == 5

    def test_min_with_key(self):
        items = [("a", 3), ("b", 1), ("c", 2)]
        assert Stream(items).min(key=lambda t: t[1]) == ("b", 1)

    def test_max_with_key(self):
        items = [("a", 3), ("b", 1), ("c", 2)]
        assert Stream(items).max(key=lambda t: t[1]) == ("a", 3)

    def test_min_empty_raises(self):
        with pytest.raises(ValueError):
            Stream([]).min()


# ---------------------------------------------------------------------------
# sum
# ---------------------------------------------------------------------------
class TestSum:
    def test_sum_ints(self):
        assert Stream([1, 2, 3]).sum() == 6

    def test_sum_empty(self):
        assert Stream([]).sum() == 0

    def test_sum_floats(self):
        assert Stream([0.5, 1.5, 2.0]).sum() == 4.0


# ---------------------------------------------------------------------------
# to_list / to_set / to_dict
# ---------------------------------------------------------------------------
class TestToList:
    def test_to_list_basic(self):
        assert Stream([1, 2, 3]).to_list() == [1, 2, 3]

    def test_to_list_empty(self):
        assert Stream([]).to_list() == []


class TestToSet:
    def test_to_set_basic(self):
        assert Stream([1, 2, 2, 3]).to_set() == {1, 2, 3}

    def test_to_set_empty(self):
        assert Stream([]).to_set() == set()


class TestToDict:
    def test_to_dict_key_only(self):
        items = [{"id": 1}, {"id": 2}]
        result = Stream(items).to_dict(key_func=lambda d: d["id"])
        assert result == {1: {"id": 1}, 2: {"id": 2}}

    def test_to_dict_key_and_value(self):
        items = [{"id": 1, "v": "a"}, {"id": 2, "v": "b"}]
        result = Stream(items).to_dict(
            key_func=lambda d: d["id"], value_func=lambda d: d["v"]
        )
        assert result == {1: "a", 2: "b"}


# ---------------------------------------------------------------------------
# for_each
# ---------------------------------------------------------------------------
class TestForEach:
    def test_for_each_collects(self):
        seen = []
        Stream([1, 2, 3]).for_each(seen.append)
        assert seen == [1, 2, 3]

    def test_for_each_returns_none(self):
        result = Stream([1]).for_each(lambda x: None)
        assert result is None

    def test_for_each_empty(self):
        seen = []
        Stream([]).for_each(seen.append)
        assert seen == []


# ---------------------------------------------------------------------------
# Chaining (full pipeline)
# ---------------------------------------------------------------------------
class TestChaining:
    def test_full_pipeline(self):
        result = (
            Stream(range(20))
            .filter(lambda x: x % 2 == 0)
            .map(lambda x: x * x)
            .take(3)
            .to_list()
        )
        assert result == [0, 4, 16]

    def test_complex_pipeline_with_distinct_sort(self):
        result = (
            Stream([3, 1, 2, 2, 4, 1, 5])
            .distinct()
            .filter(lambda x: x > 1)
            .sort(reverse=True)
            .to_list()
        )
        assert result == [5, 4, 3, 2]

    def test_pipeline_with_flat_map_and_sum(self):
        total = (
            Stream([[1, 2], [3, 4], [5]])
            .flat_map(lambda x: x)
            .sum()
        )
        assert total == 15

    def test_pipeline_count_after_transform(self):
        n = (
            Stream(range(100))
            .filter(lambda x: x % 3 == 0)
            .map(lambda x: x + 1)
            .count()
        )
        # 0,3,6,...,99 => 34 items
        assert n == 34


# ---------------------------------------------------------------------------
# Laziness
# ---------------------------------------------------------------------------
class TestLaziness:
    def test_map_is_lazy(self):
        calls = []

        def f(x):
            calls.append(x)
            return x

        s = Stream(range(5)).map(f)
        # Nothing consumed yet
        assert calls == []
        # take just 2
        assert s.take(2).to_list() == [0, 1]
        # f only called for the items we consumed
        assert calls == [0, 1]

    def test_filter_is_lazy(self):
        calls = []

        def is_even(x):
            calls.append(x)
            return x % 2 == 0

        # Consume only first two evens
        result = Stream(range(100)).filter(is_even).take(2).to_list()
        assert result == [0, 2]
        # We should not have evaluated all 100 items
        assert len(calls) < 100

    def test_infinite_source_with_take(self):
        import itertools as _it

        result = Stream(_it.count(0)).map(lambda x: x * 2).take(5).to_list()
        assert result == [0, 2, 4, 6, 8]

    def test_generator_yields_one_at_a_time(self):
        produced = []

        def src():
            for i in range(10):
                produced.append(i)
                yield i

        s = Stream(src()).map(lambda x: x + 100)
        it = iter(s)
        assert next(it) == 100
        # Only one item should have been produced so far
        assert produced == [0]
        assert next(it) == 101
        assert produced == [0, 1]


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------
class TestEdgeCases:
    def test_single_item(self):
        assert Stream([42]).map(lambda x: x + 1).to_list() == [43]

    def test_single_item_first_last(self):
        assert Stream([7]).first() == 7

    def test_single_item_first_or_none(self):
        s = Stream([])
        assert s.first_or_none() is None

    def test_empty_chained_ops(self):
        result = (
            Stream([])
            .map(lambda x: x * 2)
            .filter(lambda x: True)
            .take(10)
            .to_list()
        )
        assert result == []

    def test_stream_is_single_use(self):
        s = Stream([1, 2, 3])
        assert s.to_list() == [1, 2, 3]
        # Source exhausted
        assert s.to_list() == []

    def test_window_exact_size(self):
        assert Stream([1, 2, 3]).window(3).to_list() == [(1, 2, 3)]

    def test_chunked_single_full_chunk(self):
        assert Stream([1, 2]).chunked(2).to_list() == [(1, 2)]
