import json
from dataclasses import dataclass, field
from enum import Enum


class ProfileLayer(str, Enum):
    BASE = "base"
    ENVIRONMENT = "environment"
    USER = "user"
    RUNTIME = "runtime"


@dataclass
class ConfigProfile:
    """A named configuration profile with layered key-value pairs."""
    name: str
    layer: ProfileLayer
    values: dict = field(default_factory=dict)
    extends: str = ""    # name of profile this extends (parent)
    description: str = ""

    def get(self, key: str, default=None):
        """Get value by key, with optional default."""
        return self.values.get(key, default)

    def set(self, key: str, value) -> None:
        self.values[key] = value

    def keys(self) -> list:
        return list(self.values.keys())

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "layer": self.layer.value,
            "values": self.values,
            "extends": self.extends,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "ConfigProfile":
        return cls(
            name=d["name"],
            layer=ProfileLayer(d.get("layer", "base")),
            values=d.get("values", {}),
            extends=d.get("extends", ""),
            description=d.get("description", ""),
        )

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def from_json(cls, s: str) -> "ConfigProfile":
        return cls.from_dict(json.loads(s))
