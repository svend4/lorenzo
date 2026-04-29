"""Benchmark runner: тайминг ключевых операций + history."""
import argparse
import json
import statistics
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).parent.parent
HISTORY_PATH = ROOT / "bench" / "history.jsonl"


class Bench:
    """Один benchmark: выполняется N раз, статистика по таймингам."""

    def __init__(self, name: str, fn: Callable, *,
                 setup: Callable | None = None,
                 iterations: int = 5,
                 warmup: int = 1,
                 suite: str = "default"):
        self.name = name
        self.fn = fn
        self.setup = setup
        self.iterations = iterations
        self.warmup = warmup
        self.suite = suite

    def run(self) -> dict:
        """Запускает benchmark и возвращает статистику."""
        ctx = self.setup() if self.setup else None

        # Warmup
        for _ in range(self.warmup):
            self._call(ctx)

        # Измерения
        times: list[float] = []
        for _ in range(self.iterations):
            t0 = time.perf_counter()
            self._call(ctx)
            times.append((time.perf_counter() - t0) * 1000)  # ms

        return {
            "name": self.name,
            "suite": self.suite,
            "iterations": self.iterations,
            "min_ms": round(min(times), 3),
            "max_ms": round(max(times), 3),
            "mean_ms": round(statistics.mean(times), 3),
            "median_ms": round(statistics.median(times), 3),
            "stdev_ms": round(statistics.stdev(times), 3) if len(times) > 1 else 0.0,
        }

    def _call(self, ctx):
        if ctx is None:
            self.fn()
        else:
            self.fn(ctx)


# ---------------------------------------------------------------------------
# Suites
# ---------------------------------------------------------------------------

def _suite_frontmatter() -> list[Bench]:
    from docstoolkit.frontmatter import parse_yaml, extract_frontmatter

    sample_yaml = "\n".join([
        "title: Test",
        "version: \"1.0\"",
        "tags: [a, b, c]",
        "status: draft",
    ] * 10)
    sample_doc = f"---\n{sample_yaml}\n---\n\n# Body\n\ncontent " * 100

    return [
        Bench("parse_yaml", lambda: parse_yaml(sample_yaml), suite="frontmatter"),
        Bench("extract_frontmatter", lambda: extract_frontmatter(sample_doc),
              suite="frontmatter"),
    ]


def _suite_embeddings() -> list[Bench]:
    from docstoolkit.embeddings.tfidf import TFIDFProvider, _tokenize, _cosine_sparse

    docs = ["hello world memory agent " * 20, "rag retrieval search " * 20] * 50
    long_text = "memory agent rag retrieval search " * 100

    def setup_fitted():
        prov = TFIDFProvider()
        prov.fit(docs)
        return prov

    return [
        Bench("tokenize_long", lambda: _tokenize(long_text), suite="embeddings"),
        Bench("tfidf_fit_100docs", lambda: TFIDFProvider().fit(docs),
              suite="embeddings", iterations=3),
        Bench("tfidf_encode", lambda p: p.encode(["query memory"]),
              setup=setup_fitted, suite="embeddings"),
        Bench("cosine_sparse",
              lambda: _cosine_sparse({"a": 0.5, "b": 0.3}, {"a": 0.4, "c": 0.2}),
              suite="embeddings", iterations=1000),
    ]


def _suite_search() -> list[Bench]:
    from docstoolkit.embeddings.tfidf import TFIDFProvider

    docs = [
        {"id": f"d{i}", "title": f"Doc {i}",
         "content": f"document {i} contains memory rag search agent"}
        for i in range(200)
    ]

    def setup_search():
        prov = TFIDFProvider()
        prov.fit([d["content"] for d in docs])
        return (prov, docs)

    return [
        Bench("search_top10",
              lambda ctx: ctx[0].search("memory agent", ctx[1], top_k=10),
              setup=setup_search, suite="search", iterations=3),
    ]


def _suite_graph() -> list[Bench]:
    from docstoolkit.graph.ner import extract_entities
    from docstoolkit.graph.builder import build_graph

    long_text = ("AgentFS works with @kksudo and Yodoca. "
                 "knowledge-space integrates NgtMemory perfectly. " * 20)
    docs = [
        {"path": f"d{i}", "content": long_text}
        for i in range(50)
    ]

    return [
        Bench("ner_extract", lambda: extract_entities(long_text), suite="graph"),
        Bench("build_graph_50docs", lambda: build_graph(docs),
              suite="graph", iterations=3),
    ]


def _suite_jobs() -> list[Bench]:
    from docstoolkit.jobs.queue import JobQueue
    import tempfile

    def setup_queue():
        tmp = Path(tempfile.mkdtemp())
        q = JobQueue(tmp / "bench.sqlite")
        return (q, tmp)

    def submit_then_claim(ctx):
        q, _ = ctx
        for _ in range(10):
            q.submit("test_handler", {"x": 1})
        for _ in range(10):
            q.claim_next()

    return [
        Bench("submit_claim_10",
              submit_then_claim,
              setup=setup_queue, suite="jobs", iterations=3),
    ]


def _suite_cluster() -> list[Bench]:
    from docstoolkit.embeddings.cluster import kmeans, detect_duplicates

    items = [
        (f"d{i}", {f"tok{i % 10}": 1.0, f"common{i % 3}": 0.5})
        for i in range(50)
    ]

    return [
        Bench("kmeans_5x50", lambda: kmeans(items, k=5, seed=42),
              suite="cluster", iterations=3),
        Bench("dedup_50",
              lambda: detect_duplicates(items, threshold=0.7),
              suite="cluster", iterations=3),
    ]


SUITES: dict[str, Callable[[], list[Bench]]] = {
    "frontmatter": _suite_frontmatter,
    "embeddings": _suite_embeddings,
    "search": _suite_search,
    "graph": _suite_graph,
    "jobs": _suite_jobs,
    "cluster": _suite_cluster,
}


# ---------------------------------------------------------------------------
# Run + history + compare
# ---------------------------------------------------------------------------

def run_suites(suites: list[str]) -> list[dict]:
    results = []
    for suite_name in suites:
        if suite_name not in SUITES:
            print(f"⚠️ Unknown suite: {suite_name}")
            continue
        for bench in SUITES[suite_name]():
            print(f"  running {bench.suite}/{bench.name}...")
            results.append(bench.run())
    return results


def save_history(results: list[dict], extra: dict = None):
    HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "ts": datetime.now().isoformat(timespec='seconds'),
        "results": results,
        **(extra or {}),
    }
    with HISTORY_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def load_history(limit: int = 100) -> list[dict]:
    if not HISTORY_PATH.exists():
        return []
    records = []
    for line in HISTORY_PATH.read_text(encoding="utf-8").splitlines():
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return records[-limit:]


def compare_with_baseline(current: list[dict],
                           baseline: list[dict],
                           threshold_pct: float = 30) -> dict:
    """Сравнивает current с baseline; возвращает регрессии (>threshold % медленнее)."""
    baseline_map = {(r["suite"], r["name"]): r for r in baseline}
    regressions = []
    for r in current:
        key = (r["suite"], r["name"])
        if key not in baseline_map:
            continue
        old_mean = baseline_map[key]["mean_ms"]
        new_mean = r["mean_ms"]
        if old_mean <= 0:
            continue
        delta_pct = (new_mean - old_mean) / old_mean * 100
        if delta_pct >= threshold_pct:
            regressions.append({
                "name": f"{r['suite']}/{r['name']}",
                "old_ms": old_mean,
                "new_ms": new_mean,
                "delta_pct": round(delta_pct, 1),
            })
    return {
        "regressions": regressions,
        "total_compared": len(current),
        "threshold_pct": threshold_pct,
    }


def render_text(results: list[dict]) -> str:
    lines = [f"# Benchmark results ({len(results)} benches)\n"]
    by_suite = {}
    for r in results:
        by_suite.setdefault(r["suite"], []).append(r)

    for suite_name in sorted(by_suite):
        items = by_suite[suite_name]
        lines.append(f"\n## {suite_name} ({len(items)})")
        lines.append("| Bench | Iter | Min | Mean | Max | Stdev |")
        lines.append("|-------|-----:|----:|-----:|----:|------:|")
        for r in items:
            lines.append(
                f"| `{r['name']}` | {r['iterations']} | "
                f"{r['min_ms']}ms | **{r['mean_ms']}ms** | "
                f"{r['max_ms']}ms | ±{r['stdev_ms']}ms |"
            )
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--suite", nargs="*", help="Какие suites (default: все)")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--save", action="store_true", help="Save to history")
    parser.add_argument("--compare", help="Compare с предыдущим запуском (n назад)")
    parser.add_argument("--threshold", type=float, default=30.0,
                        help="Regression % (default 30)")
    args = parser.parse_args()

    suites = args.suite or list(SUITES)
    print(f"# docs-toolkit bench (suites: {', '.join(suites)})\n")

    results = run_suites(suites)

    if args.save:
        save_history(results)
        print(f"\n→ Saved to {HISTORY_PATH.relative_to(ROOT)}")

    if args.compare:
        history = load_history()
        if len(history) < int(args.compare) + 1:
            print(f"⚠️ Недостаточно истории для compare ({len(history)} runs)")
        else:
            baseline = history[-int(args.compare) - 1]["results"]
            cmp = compare_with_baseline(results, baseline, args.threshold)
            if cmp["regressions"]:
                print(f"\n## ⚠️ Регрессии ({len(cmp['regressions'])}):")
                for reg in cmp["regressions"]:
                    print(f"  {reg['name']}: {reg['old_ms']}ms → {reg['new_ms']}ms "
                          f"({reg['delta_pct']:+.1f}%)")
                return 1
            else:
                print(f"\n✓ Без регрессий (threshold {args.threshold}%)")

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print()
        print(render_text(results))

    return 0


if __name__ == "__main__":
    sys.exit(main())
