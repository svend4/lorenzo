"""Tests for scripts/improve_tech_radar.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_tech_radar")


def test_radar_is_dict():
    assert hasattr(mod, "RADAR")
    assert isinstance(mod.RADAR, dict)


def test_radar_has_four_quadrants():
    assert "ADOPT" in mod.RADAR
    assert "TRIAL" in mod.RADAR
    assert "ASSESS" in mod.RADAR
    assert "HOLD" in mod.RADAR


def test_radar_quadrant_has_description():
    for quadrant, data in mod.RADAR.items():
        assert "description" in data, f"Quadrant {quadrant} missing description"


def test_radar_quadrant_has_items():
    for quadrant, data in mod.RADAR.items():
        assert "items" in data, f"Quadrant {quadrant} missing items"
        assert len(data["items"]) > 0


def test_radar_items_have_3_elements():
    for quadrant, data in mod.RADAR.items():
        for item in data["items"]:
            assert len(item) == 3, f"Item {item} in {quadrant} must have 3 elements"


def test_quadrant_icons_is_dict():
    assert hasattr(mod, "QUADRANT_ICONS")
    assert isinstance(mod.QUADRANT_ICONS, dict)


def test_quadrant_icons_has_all_quadrants():
    for q in ["ADOPT", "TRIAL", "ASSESS", "HOLD"]:
        assert q in mod.QUADRANT_ICONS


def test_adopt_contains_mcp():
    items = [i[0] for i in mod.RADAR["ADOPT"]["items"]]
    assert any("MCP" in item for item in items)


def test_hold_contains_bsl():
    items = [i[0] for i in mod.RADAR["HOLD"]["items"]]
    assert any("BSL" in item for item in items)


def test_make_ascii_radar_returns_list():
    result = mod.make_ascii_radar(mod.RADAR)
    assert isinstance(result, list)


def test_make_ascii_radar_nonempty():
    result = mod.make_ascii_radar(mod.RADAR)
    assert len(result) > 0


def test_make_ascii_radar_has_adopt_section():
    result = mod.make_ascii_radar(mod.RADAR)
    text = "\n".join(result)
    assert "ADOPT" in text


def test_make_ascii_radar_has_hold_section():
    result = mod.make_ascii_radar(mod.RADAR)
    text = "\n".join(result)
    assert "HOLD" in text
