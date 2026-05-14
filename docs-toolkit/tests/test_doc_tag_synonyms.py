"""Tests for E438 DocTagSynonyms."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_tag_synonyms import (
    DocTagSynonyms,
    SynonymGroup,
    SynonymStats,
)


# ---------------------------------------------------------------------------
# Dataclass tests
# ---------------------------------------------------------------------------


class TestSynonymGroupDataclass:
    def test_minimal_construction(self):
        g = SynonymGroup(group_id="g1", canonical="python")
        assert g.group_id == "g1"
        assert g.canonical == "python"
        assert g.synonyms == []
        assert g.created_at == 0.0

    def test_full_construction(self):
        g = SynonymGroup(
            group_id="g1",
            canonical="python",
            synonyms=["py", "python3"],
            created_at=123.5,
        )
        assert g.synonyms == ["py", "python3"]
        assert g.created_at == 123.5

    def test_default_synonyms_independent_between_instances(self):
        a = SynonymGroup(group_id="a", canonical="a")
        b = SynonymGroup(group_id="b", canonical="b")
        a.synonyms.append("alpha")
        assert b.synonyms == []


class TestSynonymStatsDataclass:
    def test_construction(self):
        s = SynonymStats(total_groups=2, total_synonyms=5, unique_canonicals=2)
        assert s.total_groups == 2
        assert s.total_synonyms == 5
        assert s.unique_canonicals == 2


# ---------------------------------------------------------------------------
# create_group / delete_group
# ---------------------------------------------------------------------------


class TestCreateGroup:
    def test_create_minimal(self):
        s = DocTagSynonyms()
        g = s.create_group("python")
        assert g.canonical == "python"
        assert g.synonyms == []
        assert g.group_id
        assert g.created_at > 0

    def test_create_with_synonyms(self):
        s = DocTagSynonyms()
        g = s.create_group("python", ["py", "python3"])
        assert g.synonyms == ["py", "python3"]

    def test_create_with_now_override(self):
        s = DocTagSynonyms()
        g = s.create_group("python", now=42.0)
        assert g.created_at == 42.0

    def test_create_duplicates_synonyms_collapsed(self):
        s = DocTagSynonyms()
        g = s.create_group("python", ["py", "py", "python3"])
        assert g.synonyms == ["py", "python3"]

    def test_create_synonym_equal_to_canonical_skipped(self):
        s = DocTagSynonyms()
        g = s.create_group("python", ["python", "py"])
        assert g.synonyms == ["py"]

    def test_create_empty_synonym_skipped(self):
        s = DocTagSynonyms()
        g = s.create_group("python", ["", "py"])
        assert g.synonyms == ["py"]

    def test_create_empty_canonical_raises(self):
        s = DocTagSynonyms()
        with pytest.raises(ValueError):
            s.create_group("")

    def test_create_duplicate_canonical_raises(self):
        s = DocTagSynonyms()
        s.create_group("python")
        with pytest.raises(ValueError):
            s.create_group("python")

    def test_create_canonical_clashes_with_existing_synonym(self):
        s = DocTagSynonyms()
        s.create_group("python", ["py"])
        with pytest.raises(ValueError):
            s.create_group("py")

    def test_create_synonym_clashes_with_other_group(self):
        s = DocTagSynonyms()
        s.create_group("python", ["py"])
        with pytest.raises(ValueError):
            s.create_group("snake", ["py"])

    def test_create_synonym_clashes_with_other_canonical(self):
        s = DocTagSynonyms()
        s.create_group("python")
        with pytest.raises(ValueError):
            s.create_group("snake", ["python"])

    def test_unique_group_ids(self):
        s = DocTagSynonyms()
        g1 = s.create_group("a")
        g2 = s.create_group("b")
        assert g1.group_id != g2.group_id


class TestDeleteGroup:
    def test_delete_existing(self):
        s = DocTagSynonyms()
        g = s.create_group("python", ["py"])
        assert s.delete_group(g.group_id) is True
        assert s.get_group(g.group_id) is None

    def test_delete_unknown(self):
        s = DocTagSynonyms()
        assert s.delete_group("nope") is False

    def test_delete_clears_tag_mappings(self):
        s = DocTagSynonyms()
        g = s.create_group("python", ["py", "python3"])
        s.delete_group(g.group_id)
        assert s.canonical_of("python") is None
        assert s.canonical_of("py") is None
        assert s.canonical_of("python3") is None

    def test_delete_allows_recreate(self):
        s = DocTagSynonyms()
        g = s.create_group("python", ["py"])
        s.delete_group(g.group_id)
        s.create_group("python", ["py"])
        assert s.canonical_of("py") == "python"


# ---------------------------------------------------------------------------
# add_synonym / remove_synonym
# ---------------------------------------------------------------------------


class TestAddSynonym:
    def test_add_new(self):
        s = DocTagSynonyms()
        g = s.create_group("python")
        assert s.add_synonym(g.group_id, "py") is True
        assert "py" in s.get_group(g.group_id).synonyms

    def test_add_existing_returns_false(self):
        s = DocTagSynonyms()
        g = s.create_group("python", ["py"])
        assert s.add_synonym(g.group_id, "py") is False

    def test_add_canonical_returns_false(self):
        s = DocTagSynonyms()
        g = s.create_group("python")
        assert s.add_synonym(g.group_id, "python") is False

    def test_add_empty_raises(self):
        s = DocTagSynonyms()
        g = s.create_group("python")
        with pytest.raises(ValueError):
            s.add_synonym(g.group_id, "")

    def test_add_unknown_group_raises(self):
        s = DocTagSynonyms()
        with pytest.raises(KeyError):
            s.add_synonym("missing", "py")

    def test_add_clashes_with_other_group(self):
        s = DocTagSynonyms()
        g1 = s.create_group("python")
        s.create_group("snake", ["py"])
        with pytest.raises(ValueError):
            s.add_synonym(g1.group_id, "py")

    def test_add_updates_tag_mapping(self):
        s = DocTagSynonyms()
        g = s.create_group("python")
        s.add_synonym(g.group_id, "py")
        assert s.canonical_of("py") == "python"


class TestRemoveSynonym:
    def test_remove_existing(self):
        s = DocTagSynonyms()
        g = s.create_group("python", ["py"])
        assert s.remove_synonym(g.group_id, "py") is True
        assert "py" not in s.get_group(g.group_id).synonyms

    def test_remove_clears_mapping(self):
        s = DocTagSynonyms()
        g = s.create_group("python", ["py"])
        s.remove_synonym(g.group_id, "py")
        assert s.canonical_of("py") is None

    def test_remove_canonical_returns_false(self):
        s = DocTagSynonyms()
        g = s.create_group("python", ["py"])
        assert s.remove_synonym(g.group_id, "python") is False
        assert s.canonical_of("python") == "python"

    def test_remove_unknown_group(self):
        s = DocTagSynonyms()
        assert s.remove_synonym("nope", "py") is False

    def test_remove_unknown_synonym(self):
        s = DocTagSynonyms()
        g = s.create_group("python")
        assert s.remove_synonym(g.group_id, "py") is False


# ---------------------------------------------------------------------------
# move_synonym
# ---------------------------------------------------------------------------


class TestMoveSynonym:
    def test_move_basic(self):
        s = DocTagSynonyms()
        g1 = s.create_group("python", ["py"])
        g2 = s.create_group("snake")
        assert s.move_synonym("py", g2.group_id) is True
        assert "py" not in s.get_group(g1.group_id).synonyms
        assert "py" in s.get_group(g2.group_id).synonyms

    def test_move_updates_canonical_lookup(self):
        s = DocTagSynonyms()
        s.create_group("python", ["py"])
        g2 = s.create_group("snake")
        s.move_synonym("py", g2.group_id)
        assert s.canonical_of("py") == "snake"

    def test_move_unknown_synonym(self):
        s = DocTagSynonyms()
        g = s.create_group("python")
        assert s.move_synonym("nope", g.group_id) is False

    def test_move_unknown_destination(self):
        s = DocTagSynonyms()
        s.create_group("python", ["py"])
        assert s.move_synonym("py", "missing") is False

    def test_move_canonical_rejected(self):
        s = DocTagSynonyms()
        s.create_group("python", ["py"])
        g2 = s.create_group("snake")
        assert s.move_synonym("python", g2.group_id) is False

    def test_move_same_group(self):
        s = DocTagSynonyms()
        g = s.create_group("python", ["py"])
        assert s.move_synonym("py", g.group_id) is False


# ---------------------------------------------------------------------------
# Lookups
# ---------------------------------------------------------------------------


class TestLookups:
    def test_get_group_existing(self):
        s = DocTagSynonyms()
        g = s.create_group("python")
        assert s.get_group(g.group_id) is g or s.get_group(g.group_id).group_id == g.group_id

    def test_get_group_unknown(self):
        s = DocTagSynonyms()
        assert s.get_group("nope") is None

    def test_find_group_by_canonical(self):
        s = DocTagSynonyms()
        g = s.create_group("python", ["py"])
        found = s.find_group("python")
        assert found is not None and found.group_id == g.group_id

    def test_find_group_by_synonym(self):
        s = DocTagSynonyms()
        g = s.create_group("python", ["py"])
        found = s.find_group("py")
        assert found is not None and found.group_id == g.group_id

    def test_find_group_unknown(self):
        s = DocTagSynonyms()
        assert s.find_group("missing") is None

    def test_canonical_of_canonical(self):
        s = DocTagSynonyms()
        s.create_group("python", ["py"])
        assert s.canonical_of("python") == "python"

    def test_canonical_of_synonym(self):
        s = DocTagSynonyms()
        s.create_group("python", ["py"])
        assert s.canonical_of("py") == "python"

    def test_canonical_of_unknown(self):
        s = DocTagSynonyms()
        assert s.canonical_of("nope") is None

    def test_synonyms_of_canonical(self):
        s = DocTagSynonyms()
        s.create_group("python", ["py", "python3"])
        assert s.synonyms_of("python") == ["py", "python3"]

    def test_synonyms_of_synonym_excludes_self(self):
        s = DocTagSynonyms()
        s.create_group("python", ["py", "python3"])
        assert s.synonyms_of("py") == ["python", "python3"]

    def test_synonyms_of_unknown(self):
        s = DocTagSynonyms()
        assert s.synonyms_of("nope") == []

    def test_synonyms_sorted(self):
        s = DocTagSynonyms()
        s.create_group("python", ["zeta", "alpha", "py"])
        assert s.synonyms_of("python") == ["alpha", "py", "zeta"]

    def test_is_synonym_same_group(self):
        s = DocTagSynonyms()
        s.create_group("python", ["py", "python3"])
        assert s.is_synonym("py", "python3") is True
        assert s.is_synonym("py", "python") is True

    def test_is_synonym_different_groups(self):
        s = DocTagSynonyms()
        s.create_group("python", ["py"])
        s.create_group("snake", ["serpent"])
        assert s.is_synonym("py", "serpent") is False

    def test_is_synonym_unknown(self):
        s = DocTagSynonyms()
        s.create_group("python")
        assert s.is_synonym("python", "missing") is False
        assert s.is_synonym("missing", "missing") is False


# ---------------------------------------------------------------------------
# expand / expand_query
# ---------------------------------------------------------------------------


class TestExpand:
    def test_expand_canonical(self):
        s = DocTagSynonyms()
        s.create_group("python", ["py", "python3"])
        assert s.expand("python") == ["py", "python", "python3"]

    def test_expand_synonym(self):
        s = DocTagSynonyms()
        s.create_group("python", ["py", "python3"])
        assert s.expand("py") == ["py", "python", "python3"]

    def test_expand_unknown(self):
        s = DocTagSynonyms()
        assert s.expand("alone") == ["alone"]

    def test_expand_dedup(self):
        s = DocTagSynonyms()
        s.create_group("alpha", ["a"])
        result = s.expand("alpha")
        assert result == sorted(set(result))


class TestExpandQuery:
    def test_expand_query_all_known(self):
        s = DocTagSynonyms()
        s.create_group("python", ["py"])
        s.create_group("snake", ["serpent"])
        assert s.expand_query(["py", "snake"]) == ["py", "python", "serpent", "snake"]

    def test_expand_query_with_unknown(self):
        s = DocTagSynonyms()
        s.create_group("python", ["py"])
        assert s.expand_query(["py", "unknown"]) == ["py", "python", "unknown"]

    def test_expand_query_empty(self):
        s = DocTagSynonyms()
        assert s.expand_query([]) == []

    def test_expand_query_dedup(self):
        s = DocTagSynonyms()
        s.create_group("python", ["py"])
        assert s.expand_query(["py", "py", "python"]) == ["py", "python"]


# ---------------------------------------------------------------------------
# list_groups / all_tags / clear / stats
# ---------------------------------------------------------------------------


class TestListGroups:
    def test_empty(self):
        s = DocTagSynonyms()
        assert s.list_groups() == []

    def test_sorted_by_canonical(self):
        s = DocTagSynonyms()
        s.create_group("zeta")
        s.create_group("alpha")
        s.create_group("mu")
        names = [g.canonical for g in s.list_groups()]
        assert names == ["alpha", "mu", "zeta"]


class TestAllTags:
    def test_empty(self):
        s = DocTagSynonyms()
        assert s.all_tags() == []

    def test_union_sorted(self):
        s = DocTagSynonyms()
        s.create_group("python", ["py"])
        s.create_group("snake", ["serpent"])
        assert s.all_tags() == ["py", "python", "serpent", "snake"]


class TestClear:
    def test_clear_empty(self):
        s = DocTagSynonyms()
        assert s.clear() == 0

    def test_clear_with_data(self):
        s = DocTagSynonyms()
        s.create_group("python", ["py"])
        s.create_group("snake")
        assert s.clear() == 2
        assert s.list_groups() == []
        assert s.all_tags() == []

    def test_clear_allows_reuse(self):
        s = DocTagSynonyms()
        s.create_group("python", ["py"])
        s.clear()
        s.create_group("python", ["py"])
        assert s.canonical_of("py") == "python"


class TestStats:
    def test_empty(self):
        s = DocTagSynonyms()
        st = s.stats()
        assert st.total_groups == 0
        assert st.total_synonyms == 0
        assert st.unique_canonicals == 0

    def test_with_data(self):
        s = DocTagSynonyms()
        s.create_group("python", ["py", "python3"])
        s.create_group("snake", ["serpent"])
        st = s.stats()
        assert st.total_groups == 2
        assert st.total_synonyms == 3
        assert st.unique_canonicals == 2

    def test_stats_after_modifications(self):
        s = DocTagSynonyms()
        g = s.create_group("python", ["py"])
        s.add_synonym(g.group_id, "python3")
        s.remove_synonym(g.group_id, "py")
        st = s.stats()
        assert st.total_groups == 1
        assert st.total_synonyms == 1


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------


class TestThreadSafety:
    def test_concurrent_create(self):
        s = DocTagSynonyms()

        def worker(prefix: str, count: int):
            for i in range(count):
                s.create_group(f"{prefix}_{i}")

        threads = [
            threading.Thread(target=worker, args=(f"t{i}", 20)) for i in range(5)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert s.stats().total_groups == 100

    def test_concurrent_add_synonyms(self):
        s = DocTagSynonyms()
        g = s.create_group("python")

        def worker(start: int, count: int):
            for i in range(start, start + count):
                try:
                    s.add_synonym(g.group_id, f"syn_{i}")
                except ValueError:
                    pass

        threads = [
            threading.Thread(target=worker, args=(i * 20, 20)) for i in range(5)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        group = s.get_group(g.group_id)
        assert len(group.synonyms) == 100

    def test_concurrent_mixed_ops(self):
        s = DocTagSynonyms()
        for i in range(20):
            s.create_group(f"canon_{i}", [f"syn_{i}"])

        results = []

        def lookup_worker():
            for i in range(50):
                results.append(s.canonical_of(f"syn_{i % 20}"))

        def stats_worker():
            for _ in range(50):
                results.append(s.stats().total_groups)

        threads = [threading.Thread(target=lookup_worker) for _ in range(3)]
        threads += [threading.Thread(target=stats_worker) for _ in range(3)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # All canonical lookups should return matching values.
        # No exceptions and stats remain consistent.
        assert all(r is not None for r in results)


# ---------------------------------------------------------------------------
# Integration / scenario tests
# ---------------------------------------------------------------------------


class TestScenarios:
    def test_full_lifecycle(self):
        s = DocTagSynonyms()
        g1 = s.create_group("python", ["py"])
        g2 = s.create_group("snake", ["serpent"])
        assert s.stats().total_groups == 2
        s.add_synonym(g1.group_id, "python3")
        assert "python3" in s.synonyms_of("python")
        s.move_synonym("python3", g2.group_id)
        assert s.canonical_of("python3") == "snake"
        s.remove_synonym(g2.group_id, "python3")
        assert s.canonical_of("python3") is None
        s.delete_group(g1.group_id)
        assert s.stats().total_groups == 1

    def test_query_expansion_workflow(self):
        s = DocTagSynonyms()
        s.create_group("python", ["py", "python3"])
        s.create_group("javascript", ["js", "ecmascript"])
        expanded = s.expand_query(["py", "js"])
        assert "python" in expanded
        assert "python3" in expanded
        assert "javascript" in expanded
        assert "ecmascript" in expanded
