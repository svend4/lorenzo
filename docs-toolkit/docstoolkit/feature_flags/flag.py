import json
from dataclasses import dataclass, field
from enum import Enum

class FlagStatus(str, Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"
    ROLLOUT = "rollout"     # percentage-based

class RolloutStrategy(str, Enum):
    ALL = "all"             # 100% of users
    NONE = "none"           # 0% of users
    PERCENTAGE = "percentage"  # based on user_id hash
    ALLOWLIST = "allowlist"    # explicit user list

@dataclass
class FeatureFlag:
    name: str
    status: FlagStatus = FlagStatus.DISABLED
    rollout_pct: float = 0.0        # 0-100
    strategy: RolloutStrategy = RolloutStrategy.NONE
    allowlist: list = field(default_factory=list)  # list[str] user_ids
    description: str = ""
    tags: list = field(default_factory=list)

    def is_globally_enabled(self) -> bool:
        return self.status == FlagStatus.ENABLED

    def is_disabled(self) -> bool:
        return self.status == FlagStatus.DISABLED

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "status": self.status.value,
            "rollout_pct": self.rollout_pct,
            "strategy": self.strategy.value,
            "allowlist": self.allowlist,
            "description": self.description,
            "tags": self.tags,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "FeatureFlag":
        return cls(
            name=d["name"],
            status=FlagStatus(d.get("status", "disabled")),
            rollout_pct=float(d.get("rollout_pct", 0.0)),
            strategy=RolloutStrategy(d.get("strategy", "none")),
            allowlist=d.get("allowlist", []),
            description=d.get("description", ""),
            tags=d.get("tags", []),
        )
