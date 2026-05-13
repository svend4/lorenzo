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


def test_cmd_find_no_match(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "CUSTOM_RECIPES_FILE", tmp_path / "recipes.json")
    mod.cmd_find("xyzxyzxyz_no_match_abc")
    out = capsys.readouterr().out
    assert "Нет" in out or "нет" in out or "no" in out.lower()


def test_cmd_find_with_match(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "CUSTOM_RECIPES_FILE", tmp_path / "recipes.json")
    mod.cmd_find("качество проверка")
    out = capsys.readouterr().out
    assert "quality" in out.lower() or "качество" in out.lower() or "Рецепт" in out


def test_cmd_info_existing_recipe(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "CUSTOM_RECIPES_FILE", tmp_path / "recipes.json")
    mod.cmd_info("quality-check")
    out = capsys.readouterr().out
    assert "quality-check" in out


def test_cmd_list_with_group_filter(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "CUSTOM_RECIPES_FILE", tmp_path / "recipes.json")
    mod.cmd_list(group_filter="quality")
    out = capsys.readouterr().out
    assert isinstance(out, str)


def test_load_history_missing_file(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "HISTORY_FILE", tmp_path / "nonexistent.json")
    result = mod._load_history()
    assert result == []


def test_save_and_load_history(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "HISTORY_FILE", tmp_path / "history.json")
    entry = {"recipe": "test", "started_at": "2026-01-01T10:00:00", "ok_count": 1, "total_count": 1, "total_sec": 5.0}
    mod._save_history(entry)
    result = mod._load_history()
    assert len(result) >= 1
    assert result[-1]["recipe"] == "test"


def test_parse_since_days():
    result = mod._parse_since("7d")
    assert result is not None
    assert isinstance(result, str)


def test_parse_since_date():
    result = mod._parse_since("2026-01-01")
    assert result is not None
    assert "2026-01-01" in result


def test_parse_since_invalid():
    result = mod._parse_since("invalid")
    assert result is None


def test_cmd_stats_empty_history(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "HISTORY_FILE", tmp_path / "empty.json")
    mod.cmd_stats()
    out = capsys.readouterr().out
    assert "пуст" in out.lower() or "empty" in out.lower() or "история" in out.lower()


def test_cmd_stats_with_history(tmp_path, monkeypatch, capsys):
    import json
    hist_file = tmp_path / "history.json"
    hist_file.write_text(json.dumps([
        {"recipe": "quality-check", "started_at": "2026-01-01T10:00:00", "dry_run": False,
         "ok_count": 3, "total_count": 3, "total_sec": 5.0},
    ]), encoding="utf-8")
    monkeypatch.setattr(mod, "HISTORY_FILE", hist_file)
    mod.cmd_stats()
    out = capsys.readouterr().out
    assert "quality-check" in out


def test_cmd_stats_with_name_filter(tmp_path, monkeypatch, capsys):
    import json
    hist_file = tmp_path / "history.json"
    hist_file.write_text(json.dumps([
        {"recipe": "quality-check", "started_at": "2026-01-01T10:00:00",
         "ok_count": 1, "total_count": 1, "total_sec": 2.0},
    ]), encoding="utf-8")
    monkeypatch.setattr(mod, "HISTORY_FILE", hist_file)
    mod.cmd_stats(name="quality-check")
    out = capsys.readouterr().out
    assert "quality-check" in out


def test_cmd_stats_name_no_history(tmp_path, monkeypatch, capsys):
    import json
    hist_file = tmp_path / "history.json"
    hist_file.write_text(json.dumps([
        {"recipe": "other-recipe", "started_at": "2026-01-01T10:00:00",
         "ok_count": 1, "total_count": 1, "total_sec": 2.0},
    ]), encoding="utf-8")
    monkeypatch.setattr(mod, "HISTORY_FILE", hist_file)
    mod.cmd_stats(name="nonexistent-recipe")
    out = capsys.readouterr().out
    assert "Нет" in out or "нет" in out


def test_cmd_run_not_found(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "CUSTOM_RECIPES_FILE", tmp_path / "recipes.json")
    monkeypatch.setattr(mod, "HISTORY_FILE", tmp_path / "history.json")
    mod.cmd_run("nonexistent-recipe-xyz", dry_run=False)
    out = capsys.readouterr().out
    assert "не найден" in out or "not found" in out.lower()


def test_cmd_run_dry_run(tmp_path, monkeypatch, capsys):
    from unittest.mock import MagicMock, patch
    # Create a fake script file
    fake_script = tmp_path / "fake_script.py"
    fake_script.write_text('# fake\nprint("ok")\n', encoding="utf-8")
    custom_file = tmp_path / "recipes.json"
    monkeypatch.setattr(mod, "CUSTOM_RECIPES_FILE", custom_file)
    monkeypatch.setattr(mod, "HISTORY_FILE", tmp_path / "history.json")
    monkeypatch.setattr(mod, "SCRIPTS", tmp_path)
    # Add a test recipe pointing to the fake script
    import json
    custom_file.write_text(json.dumps({
        "test-recipe": {
            "description": "Test recipe",
            "tags": ["test"],
            "scripts": [["fake_script.py", []]],
        }
    }), encoding="utf-8")
    fake_result = MagicMock()
    fake_result.returncode = 0
    fake_result.stdout = "Success output\n"
    fake_result.stderr = ""
    with patch("subprocess.run", return_value=fake_result):
        mod.cmd_run("test-recipe", dry_run=True)
    out = capsys.readouterr().out
    assert "test-recipe" in out


def test_cmd_add_builtin_name_rejected(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "CUSTOM_RECIPES_FILE", tmp_path / "recipes.json")
    mod.cmd_add("quality-check", "desc", ["script.py"])
    out = capsys.readouterr().out
    assert "зарезервировано" in out or "reserved" in out.lower()


def test_cmd_add_custom_recipe(tmp_path, monkeypatch, capsys):
    custom_file = tmp_path / "recipes.json"
    monkeypatch.setattr(mod, "CUSTOM_RECIPES_FILE", custom_file)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.cmd_add("my-test-recipe", "My test recipe", ["script.py"])
    out = capsys.readouterr().out
    assert "my-test-recipe" in out or "добавлен" in out


def test_cmd_delete_builtin_rejected(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "CUSTOM_RECIPES_FILE", tmp_path / "recipes.json")
    mod.cmd_delete("quality-check")
    out = capsys.readouterr().out
    assert "Нельзя" in out or "cannot" in out.lower()


def test_cmd_delete_not_found(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "CUSTOM_RECIPES_FILE", tmp_path / "recipes.json")
    mod.cmd_delete("nonexistent-custom-recipe")
    out = capsys.readouterr().out
    assert "не найден" in out or "not found" in out.lower()


def test_cmd_delete_custom_recipe(tmp_path, monkeypatch, capsys):
    import json
    custom_file = tmp_path / "recipes.json"
    custom_file.write_text(json.dumps({
        "my-recipe": {"description": "test", "tags": [], "scripts": []}
    }), encoding="utf-8")
    monkeypatch.setattr(mod, "CUSTOM_RECIPES_FILE", custom_file)
    mod.cmd_delete("my-recipe")
    out = capsys.readouterr().out
    assert "удалён" in out or "deleted" in out.lower()


def test_main_stats_no_crash(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "HISTORY_FILE", tmp_path / "history.json")
    monkeypatch.setattr("sys.argv", ["prog", "--stats"])
    mod.main()


def test_main_run_not_found(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "CUSTOM_RECIPES_FILE", tmp_path / "recipes.json")
    monkeypatch.setattr(mod, "HISTORY_FILE", tmp_path / "history.json")
    monkeypatch.setattr("sys.argv", ["prog", "--run", "nonexistent-xyz"])
    mod.main()


def test_main_add_missing_desc_exits(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "CUSTOM_RECIPES_FILE", tmp_path / "recipes.json")
    monkeypatch.setattr("sys.argv", ["prog", "--add", "my-recipe"])
    with pytest.raises(SystemExit):
        mod.main()


def test_main_add_recipe(tmp_path, monkeypatch, capsys):
    custom_file = tmp_path / "recipes.json"
    monkeypatch.setattr(mod, "CUSTOM_RECIPES_FILE", custom_file)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog", "--add", "my-recipe", "--desc", "My recipe", "--scripts", "script.py"])
    mod.main()


def test_main_delete_recipe(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "CUSTOM_RECIPES_FILE", tmp_path / "recipes.json")
    monkeypatch.setattr("sys.argv", ["prog", "--delete", "nonexistent-xyz"])
    mod.main()


def test_main_no_args_calls_list(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["prog"])
    mod.main()
    out = capsys.readouterr().out
    assert isinstance(out, str)
