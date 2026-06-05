"""Phase VII — verify plugin groups are registered & discoverable."""
from __future__ import annotations

from docstoolkit.plugins import (
    SUPPORTED_GROUPS, discover, list_plugin_groups,
)


def test_retrievers_group_registered():
    """Phase VII contract: retrievers can be plugged in via entry_points."""
    assert "docstoolkit.retrievers" in SUPPORTED_GROUPS


def test_answerers_group_registered():
    assert "docstoolkit.answerers" in SUPPORTED_GROUPS


def test_discover_empty_group_returns_empty_list():
    """A group with no entry_points returns an empty list, not an error."""
    # docstoolkit.retrievers has no third-party entries in CI;
    # discover() should still return without raising.
    assert discover("docstoolkit.retrievers") == []


def test_list_plugin_groups_shape():
    groups = list_plugin_groups()
    assert isinstance(groups, dict)
    for g in SUPPORTED_GROUPS:
        assert g in groups
        assert isinstance(groups[g], list)
