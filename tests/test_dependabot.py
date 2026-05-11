"""Tests for scripts/improve_dependabot.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_dependabot")


def test_version_tuple_returns_tuple():
    result = mod._version_tuple("1.2.3")
    assert isinstance(result, tuple)


def test_version_tuple_parses_major_minor_patch():
    result = mod._version_tuple("3.11.5")
    assert result == (3, 11, 5)


def test_version_tuple_handles_short_version():
    result = mod._version_tuple("1.2")
    assert result == (1, 2)


def test_version_tuple_handles_invalid():
    result = mod._version_tuple("not-a-version")
    assert result == (0,)


def test_version_tuple_comparison():
    old = mod._version_tuple("1.0.0")
    new = mod._version_tuple("2.0.0")
    assert new > old


def test_extract_version_mentions_returns_list():
    result = mod._extract_version_mentions("anthropic==0.25.0 fastapi>=0.100.0")
    assert isinstance(result, list)


def test_extract_version_mentions_finds_pinned():
    result = mod._extract_version_mentions("anthropic==0.25.0")
    assert len(result) >= 1
    packages = [r[0] for r in result]
    assert "anthropic" in packages


def test_extract_version_mentions_finds_gte():
    result = mod._extract_version_mentions("fastapi>=0.100.0")
    assert len(result) >= 1


def test_extract_version_mentions_captures_version():
    result = mod._extract_version_mentions("anthropic==0.25.0")
    versions = [r[1] for r in result]
    assert any("0.25" in v for v in versions)


def test_extract_version_mentions_empty_text():
    result = mod._extract_version_mentions("no version mentions here")
    assert result == []


def test_extract_version_mentions_multiple():
    text = "anthropic==0.25.0 fastapi>=0.100.0 pydantic==2.0.0"
    result = mod._extract_version_mentions(text)
    assert len(result) >= 2
