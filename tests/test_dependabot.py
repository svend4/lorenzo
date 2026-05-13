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


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_dependabot_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "DEPENDABOT.md").exists()


def test_main_dependabot_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    text = (tmp_path / "DEPENDABOT.md").read_text(encoding="utf-8")
    assert "# " in text


def test_main_dependabot_starts_with_heading(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    text = (tmp_path / "DEPENDABOT.md").read_text(encoding="utf-8")
    assert text.strip().startswith("#")


def test_check_pypi_version_mock(monkeypatch):
    """Lines 72-79: _check_pypi_version with mock urllib."""
    import urllib.request
    import json as json_mod

    class MockResp:
        def read(self):
            return json_mod.dumps({"info": {"version": "0.99.0"}}).encode()
        def __enter__(self):
            return self
        def __exit__(self, *args):
            pass

    monkeypatch.setattr(urllib.request, "urlopen", lambda req, timeout=8: MockResp())
    result = mod._check_pypi_version("anthropic")
    assert result == "0.99.0"


def test_check_pypi_version_error(monkeypatch):
    """Lines 79: exception → returns None."""
    import urllib.request
    monkeypatch.setattr(urllib.request, "urlopen",
                        lambda req, timeout=8: (_ for _ in ()).throw(Exception("network error")))
    result = mod._check_pypi_version("anthropic")
    assert result is None


def test_main_check_pypi_flag(tmp_path, monkeypatch):
    """Lines 100, 124-128: CHECK_PYPI=True with mock."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "CHECK_PYPI", True)
    monkeypatch.setattr(mod, "_check_pypi_version", lambda pkg: "1.0.0")
    mod.main()
    assert (tmp_path / "DEPENDABOT.md").exists()


def test_main_gen_config_flag(tmp_path, monkeypatch):
    """Lines 103-108: GEN_CONFIG=True → writes .github/dependabot.yml and returns."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "GEN_CONFIG", True)
    monkeypatch.setattr(mod, "CHECK_PYPI", False)
    mod.main()
    assert (tmp_path / ".github" / "dependabot.yml").exists()


def test_main_with_version_mentions_in_docs(tmp_path, monkeypatch):
    """Lines 113-119: doc file with package==version matches KNOWN_DEPS."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "CHECK_PYPI", False)
    monkeypatch.setattr(mod, "GEN_CONFIG", False)
    (tmp_path / "requirements.md").write_text(
        "Use anthropic==0.25.0 and fastapi>=0.100.0\n", encoding="utf-8"
    )
    mod.main()
    assert (tmp_path / "DEPENDABOT.md").exists()


def test_main_check_pypi_with_real_version_status(tmp_path, monkeypatch):
    """Lines 143-144: ok status when pypi version >= min_version."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "CHECK_PYPI", True)
    monkeypatch.setattr(mod, "GEN_CONFIG", False)
    # Mock _check_pypi_version to return valid version
    monkeypatch.setattr(mod, "_check_pypi_version", lambda pkg: "99.0.0")
    mod.main()
    text = (tmp_path / "DEPENDABOT.md").read_text(encoding="utf-8")
    assert "✅" in text


def test_main_docs_read_exception_handled(tmp_path, monkeypatch):
    """Lines 115-116: exception reading docs file → continue."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "CHECK_PYPI", False)
    monkeypatch.setattr(mod, "GEN_CONFIG", False)
    bad = tmp_path / "bad.md"
    bad.write_text("content", encoding="utf-8")

    from pathlib import Path as _Path
    original_read = _Path.read_text

    def mock_read(self, *args, **kwargs):
        if self == bad:
            raise OSError("mocked error")
        return original_read(self, *args, **kwargs)

    monkeypatch.setattr(_Path, "read_text", mock_read)
    mod.main()


def test_main_block_via_runpy(tmp_path, monkeypatch):
    """Line 179: __main__ block."""
    import runpy
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "GEN_CONFIG", False)
    monkeypatch.setattr(mod, "CHECK_PYPI", False)
    script_path = str(ROOT / "scripts" / "improve_dependabot.py")
    runpy.run_path(script_path, run_name="__main__")
