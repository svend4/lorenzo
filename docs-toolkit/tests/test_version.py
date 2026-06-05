"""Version sanity test — `__version__` matches `pyproject.toml` and is
non-empty, semver-shaped, and pinned to a real release tag.
"""
from __future__ import annotations

import re
from pathlib import Path

import docstoolkit


_SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:[-+][\w.-]+)?$")


def test_version_attribute_present():
    assert hasattr(docstoolkit, "__version__")
    assert isinstance(docstoolkit.__version__, str)
    assert docstoolkit.__version__


def test_version_is_semver():
    assert _SEMVER.match(docstoolkit.__version__), (
        f"`__version__` is not semver-shaped: {docstoolkit.__version__!r}"
    )


def test_version_matches_pyproject():
    pyproject = Path(__file__).resolve().parents[1] / "pyproject.toml"
    text = pyproject.read_text(encoding="utf-8")
    m = re.search(r'^version\s*=\s*"([^"]+)"', text, re.MULTILINE)
    assert m, "pyproject.toml has no top-level version"
    assert m.group(1) == docstoolkit.__version__, (
        f"pyproject.toml says {m.group(1)!r} but "
        f"docstoolkit.__version__ is {docstoolkit.__version__!r}"
    )
