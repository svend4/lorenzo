from dataclasses import dataclass, field
from docstoolkit.config_profiles.profile import ConfigProfile


@dataclass
class ProfileMergeResult:
    """Result of merging multiple config profiles."""
    merged: dict
    sources: dict = field(default_factory=dict)
    layers_applied: list = field(default_factory=list)
    _all_setters: dict = field(default_factory=dict, repr=False)

    def get(self, key: str, default=None):
        return self.merged.get(key, default)

    def who_set(self, key: str) -> str:
        """Return name of profile that last set this key."""
        return self.sources.get(key, "")

    def conflicts(self) -> list:
        """Keys set by more than one profile."""
        return [k for k, v in self._all_setters.items() if len(v) > 1]


def merge_profiles(profiles: list) -> ProfileMergeResult:
    """Merge list[ConfigProfile] in order (later profiles override earlier).

    profiles should be ordered: base first, runtime last.

    For each profile in order:
      for each key in profile.values:
        merged[key] = value
        sources[key] = profile.name

    Track which profiles set each key (for conflict detection).
    layers_applied = [p.name for p in profiles]
    """
    merged: dict = {}
    sources: dict = {}
    all_setters: dict = {}
    layers_applied = []

    for profile in profiles:
        layers_applied.append(profile.name)
        for key, value in profile.values.items():
            merged[key] = value
            sources[key] = profile.name
            if key not in all_setters:
                all_setters[key] = []
            if profile.name not in all_setters[key]:
                all_setters[key].append(profile.name)

    return ProfileMergeResult(
        merged=merged,
        sources=sources,
        layers_applied=layers_applied,
        _all_setters=all_setters,
    )
