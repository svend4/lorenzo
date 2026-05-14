"""Tests for E428 DocLabelAlias."""
from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_label_alias import (
    AliasStats,
    DocLabelAlias,
    LabelAliasEntry,
)


# ---------------------------------------------------------------------------
# LabelAliasEntry dataclass
# ---------------------------------------------------------------------------


def test_entry_default_values():
    entry = LabelAliasEntry(alias="py", canonical="python")
    assert entry.alias == "py"
    assert entry.canonical == "python"
    assert entry.created_at == 0.0
    assert entry.description == ""


def test_entry_all_fields():
    entry = LabelAliasEntry(
        alias="js", canonical="javascript", created_at=123.0, description="lang"
    )
    assert entry.created_at == 123.0
    assert entry.description == "lang"


def test_entry_equality():
    a = LabelAliasEntry(alias="py", canonical="python")
    b = LabelAliasEntry(alias="py", canonical="python")
    assert a == b


def test_entry_inequality():
    a = LabelAliasEntry(alias="py", canonical="python")
    b = LabelAliasEntry(alias="py", canonical="python3")
    assert a != b


# ---------------------------------------------------------------------------
# AliasStats dataclass
# ---------------------------------------------------------------------------


def test_stats_fields():
    s = AliasStats(total_aliases=5, unique_canonicals=3)
    assert s.total_aliases == 5
    assert s.unique_canonicals == 3


def test_stats_equality():
    assert AliasStats(2, 1) == AliasStats(2, 1)


# ---------------------------------------------------------------------------
# Construction / state
# ---------------------------------------------------------------------------


def test_init_empty():
    a = DocLabelAlias()
    assert len(a) == 0


def test_init_stats_empty():
    a = DocLabelAlias()
    s = a.stats()
    assert s.total_aliases == 0
    assert s.unique_canonicals == 0


# ---------------------------------------------------------------------------
# register
# ---------------------------------------------------------------------------


def test_register_basic():
    a = DocLabelAlias()
    entry = a.register("py", "python")
    assert entry.alias == "py"
    assert entry.canonical == "python"
    assert entry.description == ""
    assert entry.created_at > 0


def test_register_with_description():
    a = DocLabelAlias()
    entry = a.register("py", "python", description="programming language")
    assert entry.description == "programming language"


def test_register_with_now():
    a = DocLabelAlias()
    entry = a.register("py", "python", now=42.0)
    assert entry.created_at == 42.0


def test_register_now_zero():
    a = DocLabelAlias()
    entry = a.register("py", "python", now=0)
    assert entry.created_at == 0.0


def test_register_updates_existing():
    a = DocLabelAlias()
    a.register("py", "python", now=10.0)
    entry = a.register("py", "python3", description="v3", now=99.0)
    # created_at preserved
    assert entry.created_at == 10.0
    assert entry.canonical == "python3"
    assert entry.description == "v3"


def test_register_does_not_create_duplicate():
    a = DocLabelAlias()
    a.register("py", "python")
    a.register("py", "python3")
    assert len(a) == 1


def test_register_empty_alias_raises():
    a = DocLabelAlias()
    with pytest.raises(ValueError):
        a.register("", "python")


def test_register_non_string_alias_raises():
    a = DocLabelAlias()
    with pytest.raises(ValueError):
        a.register(123, "python")  # type: ignore[arg-type]


def test_register_empty_canonical_raises():
    a = DocLabelAlias()
    with pytest.raises(ValueError):
        a.register("py", "")


def test_register_non_string_canonical_raises():
    a = DocLabelAlias()
    with pytest.raises(ValueError):
        a.register("py", None)  # type: ignore[arg-type]


def test_register_increases_len():
    a = DocLabelAlias()
    a.register("py", "python")
    a.register("js", "javascript")
    assert len(a) == 2


# ---------------------------------------------------------------------------
# unregister
# ---------------------------------------------------------------------------


def test_unregister_existing():
    a = DocLabelAlias()
    a.register("py", "python")
    assert a.unregister("py") is True
    assert len(a) == 0


def test_unregister_missing():
    a = DocLabelAlias()
    assert a.unregister("missing") is False


def test_unregister_twice():
    a = DocLabelAlias()
    a.register("py", "python")
    assert a.unregister("py") is True
    assert a.unregister("py") is False


# ---------------------------------------------------------------------------
# resolve
# ---------------------------------------------------------------------------


def test_resolve_known_alias():
    a = DocLabelAlias()
    a.register("py", "python")
    assert a.resolve("py") == "python"


def test_resolve_unknown_returns_input():
    a = DocLabelAlias()
    assert a.resolve("rust") == "rust"


def test_resolve_after_update():
    a = DocLabelAlias()
    a.register("py", "python")
    a.register("py", "python3")
    assert a.resolve("py") == "python3"


def test_resolve_empty_string_unchanged():
    a = DocLabelAlias()
    assert a.resolve("") == ""


# ---------------------------------------------------------------------------
# resolve_list
# ---------------------------------------------------------------------------


def test_resolve_list_basic():
    a = DocLabelAlias()
    a.register("py", "python")
    a.register("js", "javascript")
    out = a.resolve_list(["py", "js"])
    assert out == ["javascript", "python"]


def test_resolve_list_mixed():
    a = DocLabelAlias()
    a.register("py", "python")
    out = a.resolve_list(["py", "rust", "python"])
    # py->python, rust->rust, python->python ; dedupe + sort
    assert out == ["python", "rust"]


def test_resolve_list_empty():
    a = DocLabelAlias()
    assert a.resolve_list([]) == []


def test_resolve_list_all_unknown():
    a = DocLabelAlias()
    assert a.resolve_list(["x", "y", "x"]) == ["x", "y"]


def test_resolve_list_collapses_to_canonical():
    a = DocLabelAlias()
    a.register("py", "python")
    a.register("py3", "python")
    a.register("python3", "python")
    assert a.resolve_list(["py", "py3", "python3"]) == ["python"]


# ---------------------------------------------------------------------------
# get_alias
# ---------------------------------------------------------------------------


def test_get_alias_existing():
    a = DocLabelAlias()
    a.register("py", "python", description="lang")
    entry = a.get_alias("py")
    assert entry is not None
    assert entry.canonical == "python"
    assert entry.description == "lang"


def test_get_alias_missing():
    a = DocLabelAlias()
    assert a.get_alias("missing") is None


# ---------------------------------------------------------------------------
# aliases_for_canonical
# ---------------------------------------------------------------------------


def test_aliases_for_canonical_multiple():
    a = DocLabelAlias()
    a.register("py", "python")
    a.register("py3", "python")
    a.register("js", "javascript")
    assert a.aliases_for_canonical("python") == ["py", "py3"]


def test_aliases_for_canonical_none():
    a = DocLabelAlias()
    assert a.aliases_for_canonical("python") == []


def test_aliases_for_canonical_sorted():
    a = DocLabelAlias()
    a.register("zzz", "python")
    a.register("aaa", "python")
    a.register("mmm", "python")
    assert a.aliases_for_canonical("python") == ["aaa", "mmm", "zzz"]


# ---------------------------------------------------------------------------
# list_aliases
# ---------------------------------------------------------------------------


def test_list_aliases_empty():
    a = DocLabelAlias()
    assert a.list_aliases() == []


def test_list_aliases_sorted():
    a = DocLabelAlias()
    a.register("zz", "Z")
    a.register("aa", "A")
    a.register("mm", "M")
    out = a.list_aliases()
    assert [e.alias for e in out] == ["aa", "mm", "zz"]


def test_list_aliases_returns_entries():
    a = DocLabelAlias()
    a.register("py", "python")
    out = a.list_aliases()
    assert isinstance(out[0], LabelAliasEntry)


# ---------------------------------------------------------------------------
# canonicals
# ---------------------------------------------------------------------------


def test_canonicals_empty():
    a = DocLabelAlias()
    assert a.canonicals() == []


def test_canonicals_unique_sorted():
    a = DocLabelAlias()
    a.register("py", "python")
    a.register("py3", "python")
    a.register("js", "javascript")
    a.register("rb", "ruby")
    assert a.canonicals() == ["javascript", "python", "ruby"]


# ---------------------------------------------------------------------------
# merge_labels
# ---------------------------------------------------------------------------


def test_merge_labels_basic():
    a = DocLabelAlias()
    a.register("py", "python")
    a.register("js", "javascript")
    out = a.merge_labels(["py", "js", "rust"])
    assert out == ["javascript", "python", "rust"]


def test_merge_labels_dedupe():
    a = DocLabelAlias()
    a.register("py", "python")
    a.register("py3", "python")
    out = a.merge_labels(["py", "py3", "python", "rust", "rust"])
    assert out == ["python", "rust"]


def test_merge_labels_empty():
    a = DocLabelAlias()
    assert a.merge_labels([]) == []


def test_merge_labels_no_aliases():
    a = DocLabelAlias()
    assert a.merge_labels(["c", "a", "b"]) == ["a", "b", "c"]


# ---------------------------------------------------------------------------
# bulk_register
# ---------------------------------------------------------------------------


def test_bulk_register_count():
    a = DocLabelAlias()
    count = a.bulk_register({"py": "python", "js": "javascript", "rb": "ruby"})
    assert count == 3
    assert len(a) == 3


def test_bulk_register_resolves():
    a = DocLabelAlias()
    a.bulk_register({"py": "python", "js": "javascript"})
    assert a.resolve("py") == "python"
    assert a.resolve("js") == "javascript"


def test_bulk_register_empty():
    a = DocLabelAlias()
    assert a.bulk_register({}) == 0


def test_bulk_register_overwrites():
    a = DocLabelAlias()
    a.register("py", "python")
    count = a.bulk_register({"py": "python3"})
    assert count == 1
    assert a.resolve("py") == "python3"


def test_bulk_register_non_dict_raises():
    a = DocLabelAlias()
    with pytest.raises(TypeError):
        a.bulk_register([("py", "python")])  # type: ignore[arg-type]


def test_bulk_register_invalid_alias():
    a = DocLabelAlias()
    with pytest.raises(ValueError):
        a.bulk_register({"": "python"})


def test_bulk_register_invalid_canonical():
    a = DocLabelAlias()
    with pytest.raises(ValueError):
        a.bulk_register({"py": ""})


# ---------------------------------------------------------------------------
# clear
# ---------------------------------------------------------------------------


def test_clear_empty():
    a = DocLabelAlias()
    assert a.clear() == 0


def test_clear_returns_count():
    a = DocLabelAlias()
    a.register("py", "python")
    a.register("js", "javascript")
    assert a.clear() == 2
    assert len(a) == 0


def test_clear_actually_clears():
    a = DocLabelAlias()
    a.register("py", "python")
    a.clear()
    assert a.resolve("py") == "py"


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------


def test_stats_after_register():
    a = DocLabelAlias()
    a.register("py", "python")
    a.register("py3", "python")
    a.register("js", "javascript")
    s = a.stats()
    assert s.total_aliases == 3
    assert s.unique_canonicals == 2


def test_stats_type():
    a = DocLabelAlias()
    assert isinstance(a.stats(), AliasStats)


# ---------------------------------------------------------------------------
# dunder
# ---------------------------------------------------------------------------


def test_len_empty():
    assert len(DocLabelAlias()) == 0


def test_len_after_register():
    a = DocLabelAlias()
    a.register("py", "python")
    a.register("js", "javascript")
    assert len(a) == 2


def test_contains_true():
    a = DocLabelAlias()
    a.register("py", "python")
    assert "py" in a


def test_contains_false():
    a = DocLabelAlias()
    a.register("py", "python")
    assert "rust" not in a


def test_contains_non_string():
    a = DocLabelAlias()
    assert (123 in a) is False


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------


def test_thread_safe_register():
    a = DocLabelAlias()

    def worker(start: int) -> None:
        for i in range(start, start + 50):
            a.register(f"a{i}", f"canon{i % 5}")

    threads = [threading.Thread(target=worker, args=(i * 50,)) for i in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert len(a) == 200


def test_thread_safe_mixed_ops():
    a = DocLabelAlias()
    for i in range(100):
        a.register(f"a{i}", f"c{i}")

    errors: list[BaseException] = []

    def reader() -> None:
        try:
            for _ in range(200):
                a.resolve("a1")
                a.list_aliases()
                a.stats()
                a.canonicals()
        except BaseException as exc:  # pragma: no cover - safety
            errors.append(exc)

    def writer() -> None:
        try:
            for i in range(200):
                a.register(f"w{i}", "wc")
                a.unregister(f"w{i}")
        except BaseException as exc:  # pragma: no cover - safety
            errors.append(exc)

    threads = [
        threading.Thread(target=reader),
        threading.Thread(target=reader),
        threading.Thread(target=writer),
        threading.Thread(target=writer),
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert errors == []
    assert len(a) == 100


def test_thread_safe_bulk_register():
    a = DocLabelAlias()

    def worker(offset: int) -> None:
        a.bulk_register({f"b{offset + i}": "canon" for i in range(50)})

    threads = [threading.Thread(target=worker, args=(i * 50,)) for i in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert len(a) == 200
    assert a.canonicals() == ["canon"]
