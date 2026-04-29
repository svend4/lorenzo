"""SQLite-based budget tracker с per-scope usage records и limit rules."""
import sqlite3
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path

from docstoolkit.config import load_config


SCHEMA = """
CREATE TABLE IF NOT EXISTS usage (
    id TEXT PRIMARY KEY,
    scope TEXT NOT NULL,           -- user:X | skill:Y | model:Z | global
    model TEXT,
    tokens_in INTEGER DEFAULT 0,
    tokens_out INTEGER DEFAULT 0,
    cost REAL DEFAULT 0.0,
    ts TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_usage_scope ON usage(scope);
CREATE INDEX IF NOT EXISTS idx_usage_ts ON usage(ts);

CREATE TABLE IF NOT EXISTS rules (
    scope TEXT NOT NULL,
    period TEXT NOT NULL,           -- day | week | month | total
    limit_usd REAL NOT NULL,
    warn_at REAL DEFAULT 0.8,       -- предупреждение при 80%
    PRIMARY KEY (scope, period)
);
"""


class BudgetExceeded(Exception):
    """Бюджет превышен — вызов должен быть заблокирован."""


@dataclass
class UsageRecord:
    """Один LLM-вызов: scope/model/tokens/cost."""
    id: str = ""
    scope: str = ""                # "user:alice" | "skill:rag" | "model:claude-haiku-4-5"
    model: str = ""
    tokens_in: int = 0
    tokens_out: int = 0
    cost: float = 0.0
    ts: str = ""

    def __post_init__(self):
        if not self.id:
            self.id = uuid.uuid4().hex[:12]
        if not self.ts:
            self.ts = datetime.now().isoformat(timespec='seconds')


@dataclass
class BudgetRule:
    """Лимит на trace по scope + период."""
    scope: str                      # "user:alice" | "*" (global)
    period: str = "day"             # day | week | month | total
    limit_usd: float = 1.0
    warn_at: float = 0.8            # доля от limit для warning


@dataclass
class BudgetStatus:
    """Текущий статус scope: ok / warning / blocked."""
    scope: str
    state: str = "ok"               # ok | warning | blocked
    used_usd: float = 0.0
    limit_usd: float = 0.0
    percent: float = 0.0
    period: str = "day"
    reason: str = ""

    @property
    def ok(self) -> bool:
        return self.state != "blocked"


class BudgetTracker:
    def __init__(self, db_path: Path | None = None):
        if db_path is None:
            cfg = load_config()
            db_path = cfg.root / ".docstoolkit" / "budget.sqlite"
        self.path = Path(db_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.path))
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)

    def close(self):
        self.conn.close()

    # ---- rules ----
    def set_rule(self, rule: BudgetRule) -> None:
        self.conn.execute(
            "INSERT OR REPLACE INTO rules (scope, period, limit_usd, warn_at) "
            "VALUES (?, ?, ?, ?)",
            (rule.scope, rule.period, rule.limit_usd, rule.warn_at),
        )
        self.conn.commit()

    def get_rules(self, scope: str = "") -> list[BudgetRule]:
        if scope:
            rows = self.conn.execute(
                "SELECT * FROM rules WHERE scope = ? OR scope = '*'", (scope,)
            ).fetchall()
        else:
            rows = self.conn.execute("SELECT * FROM rules").fetchall()
        return [
            BudgetRule(scope=r["scope"], period=r["period"],
                       limit_usd=r["limit_usd"], warn_at=r["warn_at"])
            for r in rows
        ]

    def remove_rule(self, scope: str, period: str) -> None:
        self.conn.execute(
            "DELETE FROM rules WHERE scope = ? AND period = ?", (scope, period)
        )
        self.conn.commit()

    # ---- usage ----
    def record(self, *, scope: str, model: str = "",
               tokens_in: int = 0, tokens_out: int = 0,
               cost: float = 0.0) -> str:
        rec = UsageRecord(scope=scope, model=model, tokens_in=tokens_in,
                          tokens_out=tokens_out, cost=cost)
        self.conn.execute(
            "INSERT INTO usage (id, scope, model, tokens_in, tokens_out, cost, ts) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (rec.id, rec.scope, rec.model, rec.tokens_in,
             rec.tokens_out, rec.cost, rec.ts),
        )
        self.conn.commit()
        return rec.id

    def used_in_period(self, scope: str, period: str) -> float:
        """Сумма расходов scope за период."""
        since = self._period_start(period)
        if since is None:
            row = self.conn.execute(
                "SELECT SUM(cost) AS s FROM usage WHERE scope = ?", (scope,)
            ).fetchone()
        else:
            row = self.conn.execute(
                "SELECT SUM(cost) AS s FROM usage WHERE scope = ? AND ts >= ?",
                (scope, since),
            ).fetchone()
        return float(row["s"] or 0.0)

    # ---- guards ----
    def check(self, scope: str) -> BudgetStatus:
        """Проверяет все применимые правила. Возвращает worst-case status."""
        rules = self.get_rules(scope)
        if not rules:
            return BudgetStatus(scope=scope, state="ok",
                                limit_usd=0.0, used_usd=0.0)

        worst: BudgetStatus | None = None
        for rule in rules:
            check_scope = scope if rule.scope != "*" else scope
            used = self.used_in_period(check_scope, rule.period)
            pct = (used / rule.limit_usd * 100) if rule.limit_usd > 0 else 0
            state = "ok"
            reason = ""
            if used >= rule.limit_usd:
                state = "blocked"
                reason = (f"{rule.scope}/{rule.period}: "
                          f"${used:.4f} >= ${rule.limit_usd:.2f} (100%)")
            elif used >= rule.limit_usd * rule.warn_at:
                state = "warning"
                reason = (f"{rule.scope}/{rule.period}: "
                          f"${used:.4f} ({pct:.0f}% of ${rule.limit_usd:.2f})")
            status = BudgetStatus(scope=scope, state=state,
                                  used_usd=used, limit_usd=rule.limit_usd,
                                  percent=pct, period=rule.period, reason=reason)
            if worst is None or self._worse(status.state, worst.state):
                worst = status
        return worst or BudgetStatus(scope=scope)

    def enforce(self, scope: str) -> BudgetStatus:
        """check + raise BudgetExceeded если blocked."""
        s = self.check(scope)
        if s.state == "blocked":
            raise BudgetExceeded(s.reason or f"Budget exceeded for {scope}")
        return s

    # ---- analytics ----
    def top_spenders(self, period: str = "day", limit: int = 10) -> list[tuple[str, float]]:
        since = self._period_start(period)
        if since is None:
            rows = self.conn.execute(
                "SELECT scope, SUM(cost) AS s FROM usage "
                "GROUP BY scope ORDER BY s DESC LIMIT ?",
                (limit,),
            ).fetchall()
        else:
            rows = self.conn.execute(
                "SELECT scope, SUM(cost) AS s FROM usage WHERE ts >= ? "
                "GROUP BY scope ORDER BY s DESC LIMIT ?",
                (since, limit),
            ).fetchall()
        return [(r["scope"], float(r["s"] or 0.0)) for r in rows]

    def per_model_breakdown(self, period: str = "day") -> dict[str, dict]:
        since = self._period_start(period)
        if since is None:
            rows = self.conn.execute(
                "SELECT model, COUNT(*) AS n, SUM(cost) AS s, "
                "SUM(tokens_in) AS ti, SUM(tokens_out) AS to_ "
                "FROM usage GROUP BY model"
            ).fetchall()
        else:
            rows = self.conn.execute(
                "SELECT model, COUNT(*) AS n, SUM(cost) AS s, "
                "SUM(tokens_in) AS ti, SUM(tokens_out) AS to_ "
                "FROM usage WHERE ts >= ? GROUP BY model",
                (since,),
            ).fetchall()
        return {
            (r["model"] or "unknown"): {
                "calls": int(r["n"] or 0),
                "cost": float(r["s"] or 0.0),
                "tokens_in": int(r["ti"] or 0),
                "tokens_out": int(r["to_"] or 0),
            }
            for r in rows
        }

    def report_markdown(self, period: str = "day") -> str:
        """Markdown сводка: top spenders + per-model breakdown."""
        lines = [f"# Budget report ({period})\n"]

        # Top spenders
        top = self.top_spenders(period=period, limit=10)
        if top:
            total = sum(c for _, c in top)
            lines.append("## Top scopes\n")
            lines.append("| Scope | Cost | Share |")
            lines.append("|-------|-----:|------:|")
            for scope, cost in top:
                share = (cost / total * 100) if total else 0
                lines.append(f"| `{scope}` | ${cost:.4f} | {share:.1f}% |")
            lines.append("")

        # Per-model
        per_model = self.per_model_breakdown(period=period)
        if per_model:
            lines.append("## Per-model breakdown\n")
            lines.append("| Model | Calls | Tokens in | Tokens out | Cost |")
            lines.append("|-------|------:|----------:|-----------:|-----:|")
            for model, m in sorted(per_model.items(),
                                    key=lambda kv: -kv[1]["cost"]):
                lines.append(
                    f"| `{model}` | {m['calls']} | {m['tokens_in']} | "
                    f"{m['tokens_out']} | ${m['cost']:.4f} |"
                )
            lines.append("")

        # Active rules
        rules = self.get_rules()
        if rules:
            lines.append("## Active rules\n")
            lines.append("| Scope | Period | Limit | Warn at |")
            lines.append("|-------|--------|------:|--------:|")
            for r in rules:
                lines.append(f"| `{r.scope}` | {r.period} | "
                             f"${r.limit_usd:.2f} | {r.warn_at*100:.0f}% |")

        return "\n".join(lines) if len(lines) > 1 else "_(пусто)_"

    # ---- internals ----
    @staticmethod
    def _period_start(period: str) -> str | None:
        now = datetime.now()
        if period == "day":
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == "week":
            start = now - timedelta(days=now.weekday())
            start = start.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == "month":
            start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        elif period == "total":
            return None
        else:
            return None
        return start.isoformat(timespec='seconds')

    @staticmethod
    def _worse(a: str, b: str) -> bool:
        order = {"ok": 0, "warning": 1, "blocked": 2}
        return order.get(a, 0) > order.get(b, 0)
