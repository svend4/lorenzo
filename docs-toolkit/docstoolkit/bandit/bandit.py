"""ThompsonBandit — multi-armed bandit with Thompson sampling.

State is persisted in SQLite so experiments survive process restarts.
"""
import random
import sqlite3
from dataclasses import dataclass
from pathlib import Path

from docstoolkit.bandit.arms import BetaBernoulliArm, ArmStats


_SCHEMA = """
CREATE TABLE IF NOT EXISTS bandit_arms (
    name      TEXT PRIMARY KEY,
    alpha     REAL NOT NULL,
    beta      REAL NOT NULL,
    pulls     INTEGER NOT NULL DEFAULT 0,
    successes INTEGER NOT NULL DEFAULT 0
);
"""


@dataclass
class BanditState:
    """Snapshot of one arm's state."""

    arm_name: str
    mean: float
    ci_low: float
    ci_high: float
    total_pulls: int


class ThompsonBandit:
    """Multi-armed bandit with Thompson sampling.

    Parameters
    ----------
    arms:
        List of arm names (variant identifiers).
    db_path:
        SQLite file path.  Use ``":memory:"`` for ephemeral experiments.
    prior_alpha / prior_beta:
        Beta prior hyper-parameters (default 1.0 → uniform prior).
    exploration_floor:
        Minimum fraction of pulls each arm must receive.  When an arm is
        below this floor it is selected regardless of sampling.
    seed:
        Optional RNG seed for reproducibility.
    """

    def __init__(
        self,
        arms: list[str],
        db_path: str = ":memory:",
        prior_alpha: float = 1.0,
        prior_beta: float = 1.0,
        exploration_floor: float = 0.05,
        seed: int | None = None,
    ):
        if not arms:
            raise ValueError("arms list must not be empty")
        self._arm_names: list[str] = list(arms)
        self._prior_alpha = prior_alpha
        self._prior_beta = prior_beta
        self._exploration_floor = exploration_floor
        self._rng = random.Random(seed)

        # Connect (or create) SQLite database
        self._conn = sqlite3.connect(db_path)
        self._conn.row_factory = sqlite3.Row
        self._conn.executescript(_SCHEMA)
        self._conn.commit()

        # Ensure all arms exist in DB (insert missing ones with prior)
        for name in self._arm_names:
            self._conn.execute(
                "INSERT OR IGNORE INTO bandit_arms (name, alpha, beta, pulls, successes) "
                "VALUES (?, ?, ?, 0, 0)",
                (name, prior_alpha, prior_beta),
            )
        self._conn.commit()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _load_arms(self) -> dict[str, BetaBernoulliArm]:
        """Load all arms from DB and return a {name: BetaBernoulliArm} dict."""
        arms: dict[str, BetaBernoulliArm] = {}
        rows = self._conn.execute(
            "SELECT name, alpha, beta, pulls, successes FROM bandit_arms WHERE name IN ({})".format(
                ",".join("?" * len(self._arm_names))
            ),
            self._arm_names,
        ).fetchall()
        for row in rows:
            arm = BetaBernoulliArm(
                name=row["name"],
                prior_alpha=row["alpha"],
                prior_beta=row["beta"],
            )
            # Restore pull / success counts into the stats object directly
            arm._stats.total_pulls = row["pulls"]
            arm._stats.total_successes = row["successes"]
            arms[row["name"]] = arm
        return arms

    def _save_arm(self, arm: BetaBernoulliArm) -> None:
        """Persist a single arm's statistics to DB."""
        s = arm.stats
        self._conn.execute(
            "UPDATE bandit_arms SET alpha=?, beta=?, pulls=?, successes=? WHERE name=?",
            (s.alpha, s.beta, s.total_pulls, s.total_successes, s.name),
        )
        self._conn.commit()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def select(self) -> str:
        """Select an arm using Thompson sampling.

        If any arm is below its ``exploration_floor`` fraction of total pulls
        it is chosen first (round-robin among under-explored arms).
        """
        arms = self._load_arms()

        total_pulls = sum(a.stats.total_pulls for a in arms.values())

        # Exploration floor check: find arms that haven't met their floor
        if total_pulls > 0 and self._exploration_floor > 0.0:
            under_floor = [
                name
                for name in self._arm_names
                if (arms[name].stats.total_pulls / total_pulls) < self._exploration_floor
            ]
            if under_floor:
                # Choose the least-pulled arm among under-floor arms
                return min(under_floor, key=lambda n: arms[n].stats.total_pulls)

        # Thompson sampling: sample each arm's Beta posterior, pick the max
        samples = {name: arms[name].sample(rng=self._rng) for name in self._arm_names}
        return max(samples, key=lambda n: samples[n])

    def update(self, arm: str, reward: float) -> None:
        """Record an observation for an arm and persist to DB.

        Parameters
        ----------
        arm:
            Arm name (must be one of the arms passed to ``__init__``).
        reward:
            1.0 = success, 0.0 = failure.  Values in-between are treated
            as fractional successes via weighted update.
        """
        if arm not in self._arm_names:
            raise KeyError(f"Unknown arm: {arm!r}.  Known arms: {self._arm_names}")

        row = self._conn.execute(
            "SELECT alpha, beta, pulls, successes FROM bandit_arms WHERE name=?",
            (arm,),
        ).fetchone()
        alpha, beta_val, pulls, successes = row["alpha"], row["beta"], row["pulls"], row["successes"]
        if reward >= 0.5:
            alpha += 1.0
            successes += 1
        else:
            beta_val += 1.0
        pulls += 1
        self._conn.execute(
            "UPDATE bandit_arms SET alpha=?, beta=?, pulls=?, successes=? WHERE name=?",
            (alpha, beta_val, pulls, successes, arm),
        )
        self._conn.commit()

    def winner(self, confidence: float = 0.95) -> str | None:
        """Return the winning arm if one arm's lower CI > all others' upper CIs.

        Returns ``None`` if no clear winner has emerged yet.
        """
        arms = self._load_arms()
        states = {
            name: arm.posterior_ci(confidence=confidence) for name, arm in arms.items()
        }
        for candidate in self._arm_names:
            low_c, _ = states[candidate]
            others_upper = [states[n][1] for n in self._arm_names if n != candidate]
            if others_upper and low_c > max(others_upper):
                return candidate
        return None

    def state(self) -> list[BanditState]:
        """Return current snapshot of all arms."""
        arms = self._load_arms()
        result = []
        for name in self._arm_names:
            arm = arms[name]
            low, high = arm.posterior_ci()
            result.append(
                BanditState(
                    arm_name=name,
                    mean=arm.mean(),
                    ci_low=low,
                    ci_high=high,
                    total_pulls=arm.stats.total_pulls,
                )
            )
        return result

    def reset(self) -> None:
        """Reset all arms to their prior Beta(prior_alpha, prior_beta)."""
        for name in self._arm_names:
            self._conn.execute(
                "UPDATE bandit_arms SET alpha=?, beta=?, pulls=0, successes=0 WHERE name=?",
                (self._prior_alpha, self._prior_beta, name),
            )
        self._conn.commit()
