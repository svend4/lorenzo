"""Layered configuration profiles: base → env → user → runtime."""
from docstoolkit.config_profiles.profile import ConfigProfile, ProfileLayer
from docstoolkit.config_profiles.loader import ProfileLoader, load_profile
from docstoolkit.config_profiles.merger import merge_profiles, ProfileMergeResult

__all__ = [
    "ConfigProfile", "ProfileLayer",
    "ProfileLoader", "load_profile",
    "merge_profiles", "ProfileMergeResult",
]
