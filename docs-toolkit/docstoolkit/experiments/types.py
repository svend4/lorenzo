"""Типы для experiments framework."""
import statistics
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Experiment:
    """Описание A/B эксперимента."""
    name: str
    variants: list[dict]              # [{"name": "X", "method": "...", ...}]
    questions: list[str]              # запросы для прогона
    description: str = ""
    metric: str = "duration_ms"       # main metric для сравнения
    seed: int = 42

    @property
    def variant_names(self) -> list[str]:
        return [v["name"] for v in self.variants]


@dataclass
class QueryRun:
    """Один прогон одного запроса в одном variant."""
    question: str
    answer: str
    citations: list[dict] = field(default_factory=list)
    duration_ms: int = 0
    tokens: int = 0
    cost: float = 0.0
    error: str = ""


@dataclass
class VariantResult:
    """Результат одного variant'а на всех запросах."""
    name: str
    config: dict
    runs: list[QueryRun] = field(default_factory=list)

    @property
    def total_duration_ms(self) -> int:
        return sum(r.duration_ms for r in self.runs)

    @property
    def avg_duration_ms(self) -> float:
        if not self.runs:
            return 0
        return self.total_duration_ms / len(self.runs)

    @property
    def median_duration_ms(self) -> float:
        if not self.runs:
            return 0
        return statistics.median(r.duration_ms for r in self.runs)

    @property
    def total_tokens(self) -> int:
        return sum(r.tokens for r in self.runs)

    @property
    def total_cost(self) -> float:
        return sum(r.cost for r in self.runs)

    @property
    def errors(self) -> int:
        return sum(1 for r in self.runs if r.error)

    @property
    def success_rate(self) -> float:
        if not self.runs:
            return 0
        return (len(self.runs) - self.errors) / len(self.runs) * 100


@dataclass
class ExperimentResult:
    """Результат эксперимента: variants + comparison."""
    experiment: Experiment
    variant_results: list[VariantResult] = field(default_factory=list)
    started_ts: str = field(default_factory=lambda: datetime.now().isoformat(timespec='seconds'))
    duration_ms: int = 0

    def compare(self) -> str:
        """Markdown отчёт сравнения variants."""
        if not self.variant_results:
            return "_(нет результатов)_"

        lines = [f"# Experiment: {self.experiment.name}\n"]
        if self.experiment.description:
            lines.append(self.experiment.description + "\n")

        lines.append(f"**Started:** {self.started_ts}")
        lines.append(f"**Duration:** {self.duration_ms}ms")
        lines.append(f"**Questions:** {len(self.experiment.questions)}")
        lines.append(f"**Variants:** {len(self.variant_results)}\n")

        # Summary table
        lines.append("## Summary\n")
        lines.append("| Variant | Runs | Errors | Success% | Avg ms | Median ms | Tokens | Cost |")
        lines.append("|---------|-----:|-------:|---------:|-------:|----------:|-------:|-----:|")
        for vr in self.variant_results:
            lines.append(
                f"| `{vr.name}` | {len(vr.runs)} | {vr.errors} | {vr.success_rate:.0f}% | "
                f"{vr.avg_duration_ms:.0f} | {vr.median_duration_ms:.0f} | "
                f"{vr.total_tokens} | ${vr.total_cost:.4f} |"
            )

        # Winner determination
        if len(self.variant_results) >= 2:
            lines.append("\n## Verdict\n")
            sorted_by_speed = sorted(self.variant_results,
                                      key=lambda v: v.avg_duration_ms)
            sorted_by_cost = sorted(self.variant_results,
                                     key=lambda v: v.total_cost)

            fastest = sorted_by_speed[0]
            cheapest = sorted_by_cost[0]
            lines.append(f"- **Fastest:** `{fastest.name}` "
                         f"({fastest.avg_duration_ms:.0f}ms avg)")
            lines.append(f"- **Cheapest:** `{cheapest.name}` "
                         f"(${cheapest.total_cost:.4f} total)")

            # Speed delta vs control
            if len(self.variant_results) == 2:
                control = self.variant_results[0]
                treat = self.variant_results[1]
                if control.avg_duration_ms > 0:
                    delta = (treat.avg_duration_ms - control.avg_duration_ms) / control.avg_duration_ms * 100
                    lines.append(f"- Treatment vs control: **{delta:+.1f}%** speed change")

        return "\n".join(lines)
