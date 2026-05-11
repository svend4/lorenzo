"""Tests for scripts/improve_recipe.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_recipe")


def test_builtin_recipes_is_dict():
    assert hasattr(mod, "BUILTIN_RECIPES")
    assert isinstance(mod.BUILTIN_RECIPES, dict)


def test_builtin_recipes_not_empty():
    assert len(mod.BUILTIN_RECIPES) > 0


def test_builtin_recipe_has_description():
    for name, r in mod.BUILTIN_RECIPES.items():
        assert "description" in r, f"Recipe {name} missing description"


def test_builtin_recipe_has_scripts():
    for name, r in mod.BUILTIN_RECIPES.items():
        assert "scripts" in r, f"Recipe {name} missing scripts"
        assert len(r["scripts"]) > 0


def test_quality_check_recipe_exists():
    assert "quality-check" in mod.BUILTIN_RECIPES


def test_all_recipes_returns_dict(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "CUSTOM_RECIPES_FILE", tmp_path / "recipes.json")
    result = mod._all_recipes()
    assert isinstance(result, dict)


def test_all_recipes_includes_builtin(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "CUSTOM_RECIPES_FILE", tmp_path / "recipes.json")
    result = mod._all_recipes()
    assert "quality-check" in result


def test_all_recipes_merges_custom(tmp_path, monkeypatch):
    import json
    custom_file = tmp_path / "recipes.json"
    custom_file.write_text(json.dumps({
        "my-custom": {
            "description": "Custom recipe",
            "tags": ["custom"],
            "scripts": [("improve_health.py", [])],
        }
    }), encoding="utf-8")
    monkeypatch.setattr(mod, "CUSTOM_RECIPES_FILE", custom_file)
    result = mod._all_recipes()
    assert "my-custom" in result
    assert "quality-check" in result


def test_load_custom_missing_file(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "CUSTOM_RECIPES_FILE", tmp_path / "missing.json")
    result = mod._load_custom()
    assert result == {}


def test_load_custom_valid(tmp_path, monkeypatch):
    import json
    f = tmp_path / "recipes.json"
    f.write_text(json.dumps({"my-recipe": {"description": "test", "tags": [], "scripts": []}}))
    monkeypatch.setattr(mod, "CUSTOM_RECIPES_FILE", f)
    result = mod._load_custom()
    assert "my-recipe" in result


def test_score_recipe_returns_int():
    recipe = {"description": "check quality documents", "tags": ["quality", "check"]}
    tokens = ["quality", "check"]
    result = mod._score_recipe(tokens, recipe)
    assert isinstance(result, int)


def test_score_recipe_matches_description_words():
    recipe = {"description": "check quality of documents", "tags": []}
    tokens = ["quality"]
    result = mod._score_recipe(tokens, recipe)
    assert result >= 1


def test_score_recipe_matches_tags():
    recipe = {"description": "does something", "tags": ["quality", "audit"]}
    tokens = ["quality"]
    result = mod._score_recipe(tokens, recipe)
    assert result >= 1


def test_score_recipe_no_match():
    recipe = {"description": "export format conversion", "tags": ["export"]}
    tokens = ["memory", "agent"]
    result = mod._score_recipe(tokens, recipe)
    assert result == 0


def test_score_recipe_multiple_hits():
    recipe = {"description": "quality audit check", "tags": ["quality", "check"]}
    tokens = ["quality", "check", "audit"]
    result = mod._score_recipe(tokens, recipe)
    assert result >= 2


def test_stopwords_is_set():
    assert hasattr(mod, "STOPWORDS")
    assert isinstance(mod.STOPWORDS, set)
    assert "и" in mod.STOPWORDS


def test_save_and_load_custom(tmp_path, monkeypatch):
    custom_file = tmp_path / "recipes.json"
    monkeypatch.setattr(mod, "CUSTOM_RECIPES_FILE", custom_file)
    data = {"my-recipe": {"description": "test", "tags": [], "scripts": []}}
    mod._save_custom(data)
    assert custom_file.exists()
    result = mod._load_custom()
    assert "my-recipe" in result


def test_has_dry_run_flag_no_dry_run(tmp_path):
    f = tmp_path / "script.py"
    f.write_text('import sys\n# no dry-run support\n', encoding="utf-8")
    result = mod._has_dry_run_flag(f)
    assert result is False


def test_has_dry_run_flag_with_dry_run(tmp_path):
    f = tmp_path / "script.py"
    f.write_text('parser.add_argument("--dry-run")\n', encoding="utf-8")
    result = mod._has_dry_run_flag(f)
    assert result is True


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_list_no_crash(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["prog", "--list"])
    mod.main()
    out = capsys.readouterr().out
    assert True  # just verify no exception


def test_main_find_no_crash(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["prog", "--find", "качество"])
    mod.main()


def test_main_info_no_crash(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["prog", "--info", "nonexistent-recipe"])
    mod.main()
