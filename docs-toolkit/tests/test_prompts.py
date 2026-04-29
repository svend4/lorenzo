"""Тесты prompt library."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.prompts import Prompt, PromptLibrary, PromptRenderError


def test_prompt_auto_extract_variables():
    p = Prompt(id="x", template="hello {name}, today is {day}")
    assert set(p.variables) == {"name", "day"}


def test_prompt_render_basic():
    p = Prompt(id="x", template="Hi {name}!", variables=["name"])
    assert p.render({"name": "Alice"}) == "Hi Alice!"


def test_prompt_render_strict_missing_var():
    p = Prompt(id="x", template="Hi {name}!", variables=["name"])
    with pytest.raises(PromptRenderError):
        p.render({}, strict=True)


def test_prompt_render_non_strict_leaves_placeholder():
    p = Prompt(id="x", template="Hi {name}!", variables=["name"])
    out = p.render({}, strict=False)
    assert "{name}" in out


def test_prompt_render_strict_unknown_placeholder():
    p = Prompt(id="x", template="Hi {name} {typo}", variables=["name"])
    with pytest.raises(PromptRenderError):
        p.render({"name": "x"}, strict=True)


def test_prompt_fingerprint_stable():
    p1 = Prompt(id="x", version=1, template="hi")
    p2 = Prompt(id="x", version=1, template="hi")
    assert p1.fingerprint() == p2.fingerprint()


def test_prompt_fingerprint_changes_with_template():
    p1 = Prompt(id="x", version=1, template="hi")
    p2 = Prompt(id="x", version=1, template="hello")
    assert p1.fingerprint() != p2.fingerprint()


# ---- registry ----

def test_register_and_get():
    lib = PromptLibrary()
    lib.register(Prompt(id="a", template="x"))
    assert lib.get("a").template == "x"


def test_get_returns_latest_version():
    lib = PromptLibrary()
    lib.register(Prompt(id="a", version=1, template="v1"))
    lib.register(Prompt(id="a", version=2, template="v2"))
    assert lib.get("a").version == 2


def test_get_specific_version():
    lib = PromptLibrary()
    lib.register(Prompt(id="a", version=1, template="v1"))
    lib.register(Prompt(id="a", version=2, template="v2"))
    assert lib.get("a", version=1).template == "v1"


def test_list_ids_and_versions():
    lib = PromptLibrary()
    lib.register(Prompt(id="a", version=1, template="x"))
    lib.register(Prompt(id="a", version=2, template="x"))
    lib.register(Prompt(id="b", version=1, template="y"))
    assert lib.list_ids() == ["a", "b"]
    assert lib.list_versions("a") == [1, 2]


def test_remove_version():
    lib = PromptLibrary()
    lib.register(Prompt(id="a", version=1, template="x"))
    lib.register(Prompt(id="a", version=2, template="y"))
    lib.remove("a", version=1)
    assert lib.list_versions("a") == [2]


def test_remove_all_versions():
    lib = PromptLibrary()
    lib.register(Prompt(id="a", template="x"))
    lib.remove("a")
    assert lib.get("a") is None


# ---- A/B variants ----

def test_set_active_variant_unknown_id_raises():
    lib = PromptLibrary()
    with pytest.raises(KeyError):
        lib.set_active_variant("nope", version=1)


def test_set_active_variant_unknown_version_raises():
    lib = PromptLibrary()
    lib.register(Prompt(id="a", template="x"))
    with pytest.raises(KeyError):
        lib.set_active_variant("a", version=99)


def test_get_active_variants_default():
    lib = PromptLibrary()
    lib.register(Prompt(id="a", version=3, template="x"))
    # default: latest version weight 1
    assert lib.get_active_variants("a") == [(3, 1.0)]


def test_ab_split_50_50_with_seed():
    """С детерминированным seed должно дать ~50/50."""
    lib = PromptLibrary(rng_seed=42)
    lib.register(Prompt(id="a", version=1, template="v1"))
    lib.register(Prompt(id="a", version=2, template="v2"))
    lib.set_active_variant("a", version=1, weight=0.5,
                            additional=[(2, 0.5)])
    counts = {1: 0, 2: 0}
    for _ in range(200):
        _, p = lib.render("a", {})
        counts[p.version] += 1
    # tolerance ±25 from 100 each
    assert abs(counts[1] - 100) < 30
    assert abs(counts[2] - 100) < 30


def test_render_returns_text_and_used_prompt():
    lib = PromptLibrary()
    lib.register(Prompt(id="a", template="hi {x}"))
    text, used = lib.render("a", {"x": "world"})
    assert text == "hi world"
    assert used.id == "a"


def test_render_unknown_id_raises():
    lib = PromptLibrary()
    with pytest.raises(PromptRenderError):
        lib.render("nope", {})


# ---- save/load ----

def test_save_and_load_roundtrip(tmp_path):
    p = tmp_path / "lib.json"
    lib = PromptLibrary(path=p)
    lib.register(Prompt(id="a", version=1, template="t1",
                         description="d"))
    lib.register(Prompt(id="a", version=2, template="t2"))
    lib.set_active_variant("a", version=1, weight=0.7,
                            additional=[(2, 0.3)])
    lib.save()

    lib2 = PromptLibrary(path=p)
    assert lib2.list_versions("a") == [1, 2]
    variants = lib2.get_active_variants("a")
    weights = {v: w for v, w in variants}
    assert weights[1] == 0.7
    assert weights[2] == 0.3


def test_stats():
    lib = PromptLibrary()
    lib.register(Prompt(id="a", version=1, template="x"))
    lib.register(Prompt(id="a", version=2, template="y"))
    lib.register(Prompt(id="b", template="z"))
    lib.set_active_variant("a", version=1, weight=0.5,
                            additional=[(2, 0.5)])
    s = lib.stats()
    assert s["ids"] == 2
    assert s["total_versions"] == 3
    assert s["active_ab_tests"] == 1
