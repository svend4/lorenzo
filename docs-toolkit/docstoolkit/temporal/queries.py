"""Temporal queries: differential / time-aware knowledge queries."""
import re
import statistics
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from docstoolkit.temporal.snapshot import CorpusSnapshot, snapshot_index


@dataclass
class TemporalAnswer:
    answer: str              # "Found N docs matching query at <commit>"
    passages: list[dict]     # from snapshot.search()
    timestamp: str
    commit: str
    doc_count: int


@dataclass
class TimelineEvent:
    timestamp: str
    commit: str
    event_type: str          # "introduced" | "spike" | "decline" | "stable"
    mentions: int
    context_snippet: str = ""


@dataclass
class ConceptEvolution:
    concept: str
    timeline: list[TimelineEvent]
    stability_score: float   # 0-1: 1=stable, 0=wildly varying
    notable_changes: list[str]  # human-readable descriptions of changes

    def to_markdown(self) -> str:
        """Format as markdown timeline."""
        lines = [f"# Concept Evolution: {self.concept}", ""]
        lines.append(f"**Stability score:** {self.stability_score:.2f}")
        lines.append("")
        if self.notable_changes:
            lines.append("## Notable changes")
            for change in self.notable_changes:
                lines.append(f"- {change}")
            lines.append("")
        if self.timeline:
            lines.append("## Timeline")
            lines.append("")
            lines.append("| Timestamp | Commit | Event | Mentions |")
            lines.append("|-----------|--------|-------|----------|")
            for ev in self.timeline:
                short_commit = ev.commit[:7] if ev.commit else ""
                lines.append(
                    f"| {ev.timestamp} | {short_commit} | {ev.event_type} | {ev.mentions} |"
                )
        else:
            lines.append("*No timeline data available.*")
        return "\n".join(lines)


@dataclass
class StaleDoc:
    path: str
    last_modified: str       # ISO timestamp
    age_days: float
    staleness_score: float   # 0-1
    reason: str              # "old" | "contradicted" | "unreferenced"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _run_git(args: list[str], cwd: Path, timeout: int = 30) -> tuple[int, str]:
    """Run git command, return (returncode, stdout). Never raises."""
    try:
        result = subprocess.run(
            ["git", "-C", str(cwd)] + args,
            capture_output=True, text=True, timeout=timeout,
        )
        return result.returncode, result.stdout
    except Exception:
        return 1, ""


def _resolve_commit(commit_or_ts: str, repo_path: Path) -> str:
    """If commit_or_ts looks like a date, find closest commit. Else return as-is."""
    # Heuristic: contains '-' and digits → treat as date/timestamp
    if re.search(r"\d{4}-\d{2}", commit_or_ts):
        rc, out = _run_git(
            ["log", f"--before={commit_or_ts}", "-1", "--format=%H", "--", "docs/"],
            repo_path,
        )
        if rc == 0 and out.strip():
            return out.strip()
        # Try without path restriction
        rc, out = _run_git(
            ["log", f"--before={commit_or_ts}", "-1", "--format=%H"],
            repo_path,
        )
        if rc == 0 and out.strip():
            return out.strip()
        return ""
    return commit_or_ts


def _count_mentions_in_commit(
    concept: str, commit: str, repo_path: Path
) -> tuple[int, str]:
    """Count case-insensitive occurrences of concept in files changed at commit."""
    # Get files changed in this commit
    rc, stat_out = _run_git(
        ["show", "--stat", "--name-only", "--format=", commit],
        repo_path,
    )
    if rc != 0:
        return 0, ""

    changed_files = [
        line.strip() for line in stat_out.splitlines()
        if line.strip() and not line.strip().startswith("{") and "|" not in line
    ]

    total_mentions = 0
    snippet = ""
    pattern = re.compile(re.escape(concept), re.IGNORECASE)

    for filepath in changed_files:
        rc2, content = _run_git(["show", f"{commit}:{filepath}"], repo_path)
        if rc2 == 0 and content:
            matches = pattern.findall(content)
            total_mentions += len(matches)
            if not snippet and matches:
                # extract a small snippet
                idx = content.lower().find(concept.lower())
                if idx != -1:
                    start = max(0, idx - 30)
                    snippet = content[start : start + 100]

    return total_mentions, snippet


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def query_at_time(
    query: str,
    commit_or_ts: str,
    *,
    repo_path: str | Path = ".",
    file_glob: str = "docs/**/*.md",
    top_k: int = 5,
) -> TemporalAnswer:
    """Query the corpus at a specific git commit or timestamp.

    If commit_or_ts looks like a date (contains '-' and digits),
    find the closest commit before that date using:
      git log --before=<ts> -1 --format="%H" -- docs/
    Otherwise treat as commit hash.

    Returns TemporalAnswer. On any git failure, returns empty TemporalAnswer.
    """
    repo_path = Path(repo_path)
    empty = TemporalAnswer(answer="", passages=[], timestamp="", commit="", doc_count=0)

    try:
        commit = _resolve_commit(commit_or_ts, repo_path)
        if not commit:
            return empty

        snapshot = snapshot_index(repo_path, commit, file_glob)
        passages = snapshot.search(query, top_k=top_k)
        n = snapshot.doc_count()
        answer = f"Found {len(passages)} docs matching query at {commit[:7]}"

        return TemporalAnswer(
            answer=answer,
            passages=passages,
            timestamp=snapshot.timestamp,
            commit=commit,
            doc_count=n,
        )
    except Exception:
        return empty


def evolve_concept(
    concept: str,
    *,
    repo_path: str | Path = ".",
    file_glob: str = "docs/**/*.md",
    since: str = "",
    until: str = "",
    max_commits: int = 20,
) -> ConceptEvolution:
    """Trace how a concept's presence changes across git history.

    Algorithm:
    1. git log --format="%H %ai" [--since] [--until] -n max_commits -- docs/
    2. For each commit count mentions of concept in changed files
    3. Build TimelineEvent per commit
    4. Compute stability_score = 1 - (stdev/max) if max>0 else 1.0
    5. Detect notable changes: first appearance, >2x spike, disappearance

    On git failure: return ConceptEvolution with empty timeline.
    """
    repo_path = Path(repo_path)
    empty = ConceptEvolution(
        concept=concept,
        timeline=[],
        stability_score=1.0,
        notable_changes=[],
    )

    try:
        log_args = ["log", f"--format=%H %ai", f"-{max_commits}"]
        if since:
            log_args.append(f"--since={since}")
        if until:
            log_args.append(f"--until={until}")
        log_args.extend(["--", "docs/"])

        rc, log_out = _run_git(log_args, repo_path)
        if rc != 0 or not log_out.strip():
            return empty

        timeline: list[TimelineEvent] = []
        for line in log_out.splitlines():
            line = line.strip()
            if not line:
                continue
            # Format: "<40-char-hash> <ISO timestamp with timezone>"
            parts = line.split(" ", 2)
            if len(parts) < 2:
                continue
            commit_hash = parts[0]
            timestamp = parts[1] if len(parts) >= 2 else ""
            # The rest could be timezone offset — combine timestamp + tz
            if len(parts) == 3:
                timestamp = f"{parts[1]} {parts[2]}"

            mentions, snippet = _count_mentions_in_commit(concept, commit_hash, repo_path)
            timeline.append(TimelineEvent(
                timestamp=timestamp,
                commit=commit_hash,
                event_type="stable",   # will update below
                mentions=mentions,
                context_snippet=snippet,
            ))

        if not timeline:
            return empty

        # Compute stability_score
        mention_counts = [ev.mentions for ev in timeline]
        max_m = max(mention_counts) if mention_counts else 0
        if max_m == 0:
            stability = 1.0
        elif len(mention_counts) < 2:
            stability = 1.0
        else:
            std = statistics.stdev(mention_counts)
            stability = max(0.0, min(1.0, 1.0 - (std / max_m)))

        # Detect event types and notable changes
        notable: list[str] = []
        prev_mentions = 0
        first_introduced = False

        for i, ev in enumerate(timeline):
            if ev.mentions > 0 and not first_introduced:
                ev.event_type = "introduced"
                first_introduced = True
                notable.append(
                    f"Concept '{concept}' first appeared at {ev.timestamp[:10]} "
                    f"({ev.commit[:7]}) with {ev.mentions} mention(s)"
                )
            elif ev.mentions == 0 and prev_mentions > 0:
                ev.event_type = "decline"
                notable.append(
                    f"Concept '{concept}' disappeared at {ev.timestamp[:10]} "
                    f"({ev.commit[:7]})"
                )
            elif prev_mentions > 0 and ev.mentions >= prev_mentions * 2:
                ev.event_type = "spike"
                notable.append(
                    f"Spike: '{concept}' went from {prev_mentions} to {ev.mentions} "
                    f"mentions at {ev.timestamp[:10]} ({ev.commit[:7]})"
                )
            elif ev.mentions > 0:
                ev.event_type = "stable"

            prev_mentions = ev.mentions

        return ConceptEvolution(
            concept=concept,
            timeline=timeline,
            stability_score=stability,
            notable_changes=notable,
        )

    except Exception:
        return empty


def detect_stale(
    *,
    repo_path: str | Path = ".",
    docs_path: str = "docs",
    threshold_days: float = 180.0,
) -> list[StaleDoc]:
    """Find docs that haven't been updated in threshold_days.

    Algorithm:
    1. For each .md file in docs_path, run:
         git log -1 --format="%ai" -- <file>
    2. Compute age in days
    3. staleness_score = min(1.0, age_days / (threshold_days * 2))
    4. reason = "old" if age > threshold else "recent"

    Return only docs where age_days > threshold_days.
    On git failure, return empty list.
    """
    import datetime

    repo_path = Path(repo_path)
    docs_dir = repo_path / docs_path

    try:
        # Find all .md files
        if not docs_dir.exists():
            # Try listing from git
            rc, out = _run_git(
                ["ls-files", "--", f"{docs_path}/**/*.md", f"{docs_path}/*.md"],
                repo_path,
            )
            if rc != 0:
                return []
            md_files = [f.strip() for f in out.splitlines() if f.strip()]
        else:
            md_files = []
            for p in docs_dir.rglob("*.md"):
                try:
                    md_files.append(str(p.relative_to(repo_path)))
                except ValueError:
                    md_files.append(str(p))

        if not md_files:
            # Fall back to git ls-files
            rc, out = _run_git(
                ["ls-files", "--", docs_path],
                repo_path,
            )
            if rc != 0:
                return []
            md_files = [
                f.strip() for f in out.splitlines()
                if f.strip().endswith(".md")
            ]

        stale: list[StaleDoc] = []
        now = datetime.datetime.now(datetime.timezone.utc)

        for filepath in md_files:
            rc, ts_out = _run_git(
                ["log", "-1", "--format=%ai", "--", filepath],
                repo_path,
            )
            if rc != 0 or not ts_out.strip():
                continue

            ts_str = ts_out.strip()
            try:
                # Parse ISO 8601 with timezone offset, e.g. "2024-01-15 12:30:00 +0300"
                # or "2024-01-15T12:30:00+03:00"
                ts_str_clean = ts_str.replace("T", " ")
                # Handle "+HHMM" vs "+HH:MM"
                # datetime.fromisoformat handles "+HH:MM" in Python 3.7+
                # but git outputs "+HHMM" without colon
                import re as _re
                ts_normalized = _re.sub(
                    r"([+-])(\d{2})(\d{2})$",
                    r"\1\2:\3",
                    ts_str_clean,
                )
                last_mod = datetime.datetime.fromisoformat(ts_normalized)
                if last_mod.tzinfo is None:
                    last_mod = last_mod.replace(tzinfo=datetime.timezone.utc)
            except Exception:
                continue

            age = (now - last_mod).total_seconds() / 86400.0
            if age > threshold_days:
                staleness = min(1.0, age / (threshold_days * 2))
                stale.append(StaleDoc(
                    path=filepath,
                    last_modified=ts_str,
                    age_days=age,
                    staleness_score=staleness,
                    reason="old",
                ))

        return stale

    except Exception:
        return []
