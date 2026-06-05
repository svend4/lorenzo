import json
from pathlib import Path
from docstoolkit.config_profiles.profile import ConfigProfile, ProfileLayer


class ProfileLoader:
    """Loads ConfigProfiles from files and a registry."""

    def __init__(self):
        self._registry: dict = {}   # {name: ConfigProfile}

    def register(self, profile: ConfigProfile) -> None:
        """Add profile to in-memory registry."""
        self._registry[profile.name] = profile

    def get(self, name: str) -> ConfigProfile | None:
        return self._registry.get(name)

    def list_names(self) -> list:
        return sorted(self._registry.keys())

    def load_from_dict(self, d: dict) -> ConfigProfile:
        """Parse dict → ConfigProfile and register it."""
        profile = ConfigProfile.from_dict(d)
        self.register(profile)
        return profile

    def load_from_json(self, json_str: str) -> ConfigProfile:
        """Parse JSON string → ConfigProfile and register it."""
        return self.load_from_dict(json.loads(json_str))

    def load_from_file(self, path: Path) -> ConfigProfile:
        """Load from .json file."""
        content = Path(path).read_text(encoding='utf-8')
        return self.load_from_json(content)

    def resolve_chain(self, name: str) -> list:
        """Return inheritance chain from root to named profile.

        If profile.extends is set and that parent exists in registry:
          chain = resolve_chain(parent) + [profile]
        Else: [profile]
        Handles circular extends by stopping at max_depth=10.
        """
        chain = []
        visited = set()
        current = name
        while current and len(chain) < 10:
            if current in visited:
                break
            profile = self._registry.get(current)
            if not profile:
                break
            visited.add(current)
            chain.append(profile)
            current = profile.extends
        return list(reversed(chain))


def load_profile(
    name: str,
    values: dict | None = None,
    layer: ProfileLayer = ProfileLayer.RUNTIME,
) -> ConfigProfile:
    """Convenience: create a one-off ConfigProfile with given values."""
    return ConfigProfile(
        name=name,
        layer=layer,
        values=values or {},
    )
