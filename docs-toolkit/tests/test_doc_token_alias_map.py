"""Tests for ``docstoolkit.doc_token_alias_map``."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_token_alias_map import (
    AliasMapStats,
    DocTokenAliasMap,
    TokenAlias,
)


# ---------------------------------------------------------------------------
# TestTokenAliasDataclass
# ---------------------------------------------------------------------------
class TestTokenAliasDataclass:
    def test_construct_with_defaults(self):
        t = TokenAlias(alias="ml", canonical="machine learning")
        assert t.alias == "ml"
        assert t.canonical == "machine learning"
        assert t.case_sensitive is False
        assert t.created_at == 0.0

    def test_construct_case_sensitive(self):
        t = TokenAlias(alias="ML", canonical="machine learning", case_sensitive=True)
        assert t.case_sensitive is True

    def test_construct_with_timestamp(self):
        t = TokenAlias(alias="x", canonical="y", created_at=123.5)
        assert t.created_at == 123.5

    def test_equality(self):
        a = TokenAlias(alias="x", canonical="y", created_at=1.0)
        b = TokenAlias(alias="x", canonical="y", created_at=1.0)
        assert a == b

    def test_inequality_on_canonical(self):
        a = TokenAlias(alias="x", canonical="y")
        b = TokenAlias(alias="x", canonical="z")
        assert a != b

    def test_inequality_on_case_sensitive(self):
        a = TokenAlias(alias="x", canonical="y", case_sensitive=True)
        b = TokenAlias(alias="x", canonical="y", case_sensitive=False)
        assert a != b


# ---------------------------------------------------------------------------
# TestAliasMapStatsDataclass
# ---------------------------------------------------------------------------
class TestAliasMapStatsDataclass:
    def test_construct(self):
        s = AliasMapStats(total_aliases=2, unique_canonicals=1, total_replacements=5)
        assert s.total_aliases == 2
        assert s.unique_canonicals == 1
        assert s.total_replacements == 5

    def test_equality(self):
        a = AliasMapStats(total_aliases=1, unique_canonicals=1, total_replacements=1)
        b = AliasMapStats(total_aliases=1, unique_canonicals=1, total_replacements=1)
        assert a == b

    def test_inequality(self):
        a = AliasMapStats(total_aliases=1, unique_canonicals=1, total_replacements=1)
        b = AliasMapStats(total_aliases=2, unique_canonicals=1, total_replacements=1)
        assert a != b


# ---------------------------------------------------------------------------
# TestConstruction
# ---------------------------------------------------------------------------
class TestConstruction:
    def test_empty(self):
        m = DocTokenAliasMap()
        assert m.list_aliases() == []

    def test_stats_empty(self):
        m = DocTokenAliasMap()
        s = m.stats()
        assert s.total_aliases == 0
        assert s.unique_canonicals == 0
        assert s.total_replacements == 0

    def test_canonicals_empty(self):
        assert DocTokenAliasMap().canonicals() == []


# ---------------------------------------------------------------------------
# TestAddAlias
# ---------------------------------------------------------------------------
class TestAddAlias:
    def test_add_new(self):
        m = DocTokenAliasMap()
        e = m.add_alias("ml", "machine learning")
        assert isinstance(e, TokenAlias)
        assert e.alias == "ml"
        assert e.canonical == "machine learning"
        assert e.case_sensitive is False

    def test_add_case_sensitive(self):
        m = DocTokenAliasMap()
        e = m.add_alias("ML", "machine learning", case_sensitive=True)
        assert e.case_sensitive is True

    def test_add_uses_provided_timestamp(self):
        m = DocTokenAliasMap()
        e = m.add_alias("a", "b", now=42.0)
        assert e.created_at == 42.0

    def test_add_default_timestamp_nonzero(self):
        m = DocTokenAliasMap()
        e = m.add_alias("a", "b")
        assert e.created_at > 0.0

    def test_add_replaces_existing(self):
        m = DocTokenAliasMap()
        m.add_alias("ml", "machine learning")
        m.add_alias("ml", "meta learning")
        assert m.get_alias("ml").canonical == "meta learning"

    def test_add_increases_total_count(self):
        m = DocTokenAliasMap()
        m.add_alias("a", "X")
        m.add_alias("b", "X")
        assert m.stats().total_aliases == 2

    def test_replace_does_not_double_count(self):
        m = DocTokenAliasMap()
        m.add_alias("a", "X")
        m.add_alias("a", "Y")
        assert m.stats().total_aliases == 1


# ---------------------------------------------------------------------------
# TestRemoveAlias
# ---------------------------------------------------------------------------
class TestRemoveAlias:
    def test_remove_existing_returns_true(self):
        m = DocTokenAliasMap()
        m.add_alias("a", "X")
        assert m.remove_alias("a") is True

    def test_remove_missing_returns_false(self):
        m = DocTokenAliasMap()
        assert m.remove_alias("nope") is False

    def test_remove_actually_removes(self):
        m = DocTokenAliasMap()
        m.add_alias("a", "X")
        m.remove_alias("a")
        assert m.get_alias("a") is None

    def test_remove_then_add_again(self):
        m = DocTokenAliasMap()
        m.add_alias("a", "X")
        m.remove_alias("a")
        m.add_alias("a", "Y")
        assert m.get_alias("a").canonical == "Y"


# ---------------------------------------------------------------------------
# TestGetAlias
# ---------------------------------------------------------------------------
class TestGetAlias:
    def test_get_existing(self):
        m = DocTokenAliasMap()
        m.add_alias("a", "X")
        assert m.get_alias("a").canonical == "X"

    def test_get_missing_returns_none(self):
        m = DocTokenAliasMap()
        assert m.get_alias("missing") is None

    def test_get_returns_token_alias_instance(self):
        m = DocTokenAliasMap()
        m.add_alias("a", "X")
        assert isinstance(m.get_alias("a"), TokenAlias)


# ---------------------------------------------------------------------------
# TestResolve
# ---------------------------------------------------------------------------
class TestResolve:
    def test_resolve_exact_match(self):
        m = DocTokenAliasMap()
        m.add_alias("ml", "machine learning")
        assert m.resolve("ml") == "machine learning"

    def test_resolve_unaliased_passthrough(self):
        m = DocTokenAliasMap()
        m.add_alias("ml", "machine learning")
        assert m.resolve("foo") == "foo"

    def test_resolve_empty_map_returns_token(self):
        m = DocTokenAliasMap()
        assert m.resolve("anything") == "anything"

    def test_resolve_case_insensitive_default(self):
        m = DocTokenAliasMap()
        m.add_alias("ml", "machine learning")
        assert m.resolve("ML") == "machine learning"
        assert m.resolve("Ml") == "machine learning"

    def test_resolve_case_sensitive_only_exact(self):
        m = DocTokenAliasMap()
        m.add_alias("ML", "machine learning", case_sensitive=True)
        assert m.resolve("ML") == "machine learning"
        # Different casing does not match a case-sensitive entry.
        assert m.resolve("ml") == "ml"

    def test_resolve_exact_wins_over_case_insensitive(self):
        m = DocTokenAliasMap()
        m.add_alias("ml", "lowercase-canonical")
        m.add_alias("ML", "exact-canonical", case_sensitive=True)
        assert m.resolve("ML") == "exact-canonical"

    def test_resolve_empty_string(self):
        m = DocTokenAliasMap()
        assert m.resolve("") == ""


# ---------------------------------------------------------------------------
# TestReplaceTokens
# ---------------------------------------------------------------------------
class TestReplaceTokens:
    def test_replace_single_token(self):
        m = DocTokenAliasMap()
        m.add_alias("ml", "machine learning")
        assert m.replace_tokens("ml") == "machine learning"

    def test_replace_preserves_whitespace(self):
        m = DocTokenAliasMap()
        m.add_alias("ml", "machine learning")
        out = m.replace_tokens("hello   ml   world")
        assert out == "hello   machine learning   world"

    def test_replace_preserves_newlines(self):
        m = DocTokenAliasMap()
        m.add_alias("ml", "machine learning")
        out = m.replace_tokens("ml\nis\nfun")
        assert out == "machine learning\nis\nfun"

    def test_replace_preserves_tabs(self):
        m = DocTokenAliasMap()
        m.add_alias("ml", "machine learning")
        out = m.replace_tokens("a\tml\tb")
        assert out == "a\tmachine learning\tb"

    def test_replace_unaliased_unchanged(self):
        m = DocTokenAliasMap()
        m.add_alias("ml", "machine learning")
        assert m.replace_tokens("hello world") == "hello world"

    def test_replace_multiple_occurrences(self):
        m = DocTokenAliasMap()
        m.add_alias("ml", "ML.")
        assert m.replace_tokens("ml ml ml") == "ML. ML. ML."

    def test_replace_empty_text(self):
        m = DocTokenAliasMap()
        m.add_alias("ml", "machine learning")
        assert m.replace_tokens("") == ""

    def test_replace_case_insensitive_replaces(self):
        m = DocTokenAliasMap()
        m.add_alias("ml", "machine learning")
        assert m.replace_tokens("ML and Ml") == "machine learning and machine learning"

    def test_replace_case_sensitive_only_exact(self):
        m = DocTokenAliasMap()
        m.add_alias("ML", "machine learning", case_sensitive=True)
        out = m.replace_tokens("ML ml")
        assert out == "machine learning ml"

    def test_replace_increments_total_replacements(self):
        m = DocTokenAliasMap()
        m.add_alias("ml", "machine learning")
        m.replace_tokens("ml and ml")
        assert m.stats().total_replacements == 2

    def test_replace_no_change_no_increment(self):
        m = DocTokenAliasMap()
        m.add_alias("ml", "machine learning")
        m.replace_tokens("nothing here")
        assert m.stats().total_replacements == 0

    def test_replace_with_custom_splitter(self):
        m = DocTokenAliasMap()
        m.add_alias("ml", "machine learning")
        # Splitter that keeps separator pieces.
        def split(text):
            out = []
            for i, part in enumerate(text.split("|")):
                if i > 0:
                    out.append("|")
                out.append(part)
            return out
        assert m.replace_tokens("ml|foo|ml", splitter=split) == "machine learning|foo|machine learning"

    def test_replace_canonical_equals_alias_no_increment(self):
        m = DocTokenAliasMap()
        m.add_alias("ml", "ml")
        m.replace_tokens("ml ml")
        assert m.stats().total_replacements == 0


# ---------------------------------------------------------------------------
# TestAliasesFor
# ---------------------------------------------------------------------------
class TestAliasesFor:
    def test_aliases_for_returns_sorted(self):
        m = DocTokenAliasMap()
        m.add_alias("c", "X")
        m.add_alias("a", "X")
        m.add_alias("b", "X")
        assert m.aliases_for("X") == ["a", "b", "c"]

    def test_aliases_for_missing(self):
        m = DocTokenAliasMap()
        m.add_alias("a", "X")
        assert m.aliases_for("Y") == []

    def test_aliases_for_only_matching_canonical(self):
        m = DocTokenAliasMap()
        m.add_alias("a", "X")
        m.add_alias("b", "Y")
        m.add_alias("c", "X")
        assert m.aliases_for("X") == ["a", "c"]

    def test_aliases_for_empty_map(self):
        assert DocTokenAliasMap().aliases_for("anything") == []


# ---------------------------------------------------------------------------
# TestListAliases
# ---------------------------------------------------------------------------
class TestListAliases:
    def test_list_aliases_sorted(self):
        m = DocTokenAliasMap()
        m.add_alias("c", "X")
        m.add_alias("a", "Y")
        m.add_alias("b", "Z")
        names = [t.alias for t in m.list_aliases()]
        assert names == ["a", "b", "c"]

    def test_list_aliases_returns_token_alias(self):
        m = DocTokenAliasMap()
        m.add_alias("a", "X")
        items = m.list_aliases()
        assert all(isinstance(i, TokenAlias) for i in items)

    def test_list_aliases_empty(self):
        assert DocTokenAliasMap().list_aliases() == []


# ---------------------------------------------------------------------------
# TestCanonicals
# ---------------------------------------------------------------------------
class TestCanonicals:
    def test_canonicals_unique(self):
        m = DocTokenAliasMap()
        m.add_alias("a", "X")
        m.add_alias("b", "X")
        m.add_alias("c", "Y")
        assert m.canonicals() == ["X", "Y"]

    def test_canonicals_sorted(self):
        m = DocTokenAliasMap()
        m.add_alias("a", "Z")
        m.add_alias("b", "A")
        m.add_alias("c", "M")
        assert m.canonicals() == ["A", "M", "Z"]

    def test_canonicals_empty(self):
        assert DocTokenAliasMap().canonicals() == []


# ---------------------------------------------------------------------------
# TestClear
# ---------------------------------------------------------------------------
class TestClear:
    def test_clear_returns_count(self):
        m = DocTokenAliasMap()
        m.add_alias("a", "X")
        m.add_alias("b", "Y")
        assert m.clear() == 2

    def test_clear_empties_map(self):
        m = DocTokenAliasMap()
        m.add_alias("a", "X")
        m.clear()
        assert m.list_aliases() == []

    def test_clear_empty_returns_zero(self):
        assert DocTokenAliasMap().clear() == 0

    def test_clear_does_not_reset_total_replacements(self):
        m = DocTokenAliasMap()
        m.add_alias("a", "X")
        m.replace_tokens("a a a")
        assert m.stats().total_replacements == 3
        m.clear()
        # Replacement counter is independent of the alias registry.
        assert m.stats().total_replacements == 3


# ---------------------------------------------------------------------------
# TestStats
# ---------------------------------------------------------------------------
class TestStats:
    def test_stats_totals(self):
        m = DocTokenAliasMap()
        m.add_alias("a", "X")
        m.add_alias("b", "X")
        m.add_alias("c", "Y")
        s = m.stats()
        assert s.total_aliases == 3
        assert s.unique_canonicals == 2

    def test_stats_replacements_zero_initially(self):
        m = DocTokenAliasMap()
        assert m.stats().total_replacements == 0

    def test_stats_replacements_increment(self):
        m = DocTokenAliasMap()
        m.add_alias("a", "X")
        m.replace_tokens("a a a")
        assert m.stats().total_replacements == 3

    def test_stats_replacements_accumulate(self):
        m = DocTokenAliasMap()
        m.add_alias("a", "X")
        m.replace_tokens("a")
        m.replace_tokens("a a")
        assert m.stats().total_replacements == 3

    def test_stats_returns_dataclass(self):
        m = DocTokenAliasMap()
        assert isinstance(m.stats(), AliasMapStats)

    def test_stats_after_remove(self):
        m = DocTokenAliasMap()
        m.add_alias("a", "X")
        m.add_alias("b", "X")
        m.remove_alias("a")
        assert m.stats().total_aliases == 1
        assert m.stats().unique_canonicals == 1


# ---------------------------------------------------------------------------
# TestThreadSafety
# ---------------------------------------------------------------------------
class TestThreadSafety:
    def test_concurrent_add_alias(self):
        m = DocTokenAliasMap()
        n_threads = 8
        per_thread = 50

        def worker(tid: int) -> None:
            for i in range(per_thread):
                m.add_alias(f"t{tid}-{i}", f"canon-{tid}")

        threads = [threading.Thread(target=worker, args=(t,)) for t in range(n_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert m.stats().total_aliases == n_threads * per_thread
        assert m.stats().unique_canonicals == n_threads

    def test_concurrent_add_and_resolve(self):
        m = DocTokenAliasMap()
        m.add_alias("ml", "machine learning")

        results: list[str] = []
        results_lock = threading.Lock()

        def adder() -> None:
            for i in range(100):
                m.add_alias(f"x{i}", f"X{i}")

        def resolver() -> None:
            for _ in range(100):
                r = m.resolve("ml")
                with results_lock:
                    results.append(r)

        threads = [
            threading.Thread(target=adder),
            threading.Thread(target=adder),
            threading.Thread(target=resolver),
            threading.Thread(target=resolver),
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert all(r == "machine learning" for r in results)
        assert m.stats().total_aliases == 1 + 100  # ml + x0..x99 (deduped)

    def test_concurrent_replace_tokens(self):
        m = DocTokenAliasMap()
        m.add_alias("ml", "machine learning")

        def worker() -> None:
            for _ in range(50):
                m.replace_tokens("ml ml ml")

        threads = [threading.Thread(target=worker) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # 4 threads * 50 iters * 3 replacements = 600
        assert m.stats().total_replacements == 600
