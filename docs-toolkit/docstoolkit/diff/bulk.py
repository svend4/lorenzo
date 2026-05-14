"""Bulk diff — compare collections of documentation files.

All computation is stdlib-only: difflib for line diffs, re/Counter for TF-IDF
cosine similarity, subprocess for git commands.
"""
from __future__ import annotations

import math
import re
import subprocess
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path


# ---------------------------------------------------------------------------
# Helpers: headings + semantic similarity
# ---------------------------------------------------------------------------

def extract_headings(text: str) -> list[str]:
    """Return heading text (without leading ``#`` characters) for every heading line."""
    headings: list[str] = []
    for line in text.splitlines():
        m = re.match(r"^(#{1,6})\s+(.+)", line)
        if m:
            headings.append(m.group(2).strip())
    return headings


def _tokenize_simple(text: str) -> list[str]:
    """Unigram tokenizer for similarity (3+ char words, lowercase)."""
    return re.findall(r"[a-zа-яё][a-zа-яё]{2,}", text.lower())


def semantic_similarity(text_a: str, text_b: str) -> float:
    """TF-IDF cosine similarity between two texts (simple unigram, no external deps)."""
    toks_a = _tokenize_simple(text_a)
    toks_b = _tokenize_simple(text_b)
    if not toks_a or not toks_b:
        return 0.0

    # Build IDF from both documents
    all_docs = [toks_a, toks_b]
    n_docs = 2
    df: Counter = Counter()
    for toks in all_docs:
        for t in set(toks):
            df[t] += 1
    idf = {t: math.log((n_docs + 1) / (c + 1)) + 1.0 for t, c in df.items()}

    def tfidf_vec(toks: list[str]) -> dict[str, float]:
        tf = Counter(toks)
        total = sum(tf.values())
        return {t: (cnt / total) * idf.get(t, 1.0) for t, cnt in tf.items()}

    va = tfidf_vec(toks_a)
    vb = tfidf_vec(toks_b)

    common = set(va) & set(vb)
    if not common:
        return 0.0
    dot = sum(va[t] * vb[t] for t in common)
    norm_a = math.sqrt(sum(v * v for v in va.values()))
    norm_b = math.sqrt(sum(v * v for v in vb.values()))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return min(1.0, dot / (norm_a * norm_b))


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class DocDiff:
    """Diff result for a single document."""
    path: str
    change: str                          # added | removed | modified | renamed
    headings_added: list[str] = field(default_factory=list)
    headings_removed: list[str] = field(default_factory=list)
    semantic_similarity: float = 0.0
    line_changes: tuple[int, int] = (0, 0)   # (added, removed)


@dataclass
class BulkDiffResult:
    """Aggregated diff result for a collection of docs."""
    added: list[DocDiff] = field(default_factory=list)
    removed: list[DocDiff] = field(default_factory=list)
    modified: list[DocDiff] = field(default_factory=list)
    summary: str = ""
    total_added: int = 0
    total_removed: int = 0
    total_modified: int = 0


# ---------------------------------------------------------------------------
# diff_docs helper
# ---------------------------------------------------------------------------

def diff_docs(
    path_a: str,
    content_a: str,
    path_b: str,
    content_b: str,
) -> DocDiff:
    """Compare two versions of the same doc (or different paths for renames)."""
    change = "renamed" if path_a != path_b else "modified"

    headings_a = set(extract_headings(content_a))
    headings_b = set(extract_headings(content_b))
    headings_added = sorted(headings_b - headings_a)
    headings_removed = sorted(headings_a - headings_b)

    sim = semantic_similarity(content_a, content_b)

    # Line-level diff counts
    lines_a = set(content_a.splitlines())
    lines_b = set(content_b.splitlines())
    added_lines = sum(1 for l in content_b.splitlines() if l not in lines_a)
    removed_lines = sum(1 for l in content_a.splitlines() if l not in lines_b)

    return DocDiff(
        path=path_b,
        change=change,
        headings_added=headings_added,
        headings_removed=headings_removed,
        semantic_similarity=sim,
        line_changes=(added_lines, removed_lines),
    )


# ---------------------------------------------------------------------------
# BulkDiffer
# ---------------------------------------------------------------------------

class BulkDiffer:
    """Compare sets of documentation files by path→content snapshots or via git."""

    def __init__(self, docs_dir: Path) -> None:
        self.docs_dir = Path(docs_dir)

    # ------------------------------------------------------------------
    # diff_snapshots
    # ------------------------------------------------------------------
    def diff_snapshots(
        self,
        snapshot_a: dict[str, str],
        snapshot_b: dict[str, str],
    ) -> BulkDiffResult:
        """Compare two ``{path: content}`` dicts."""
        paths_a = set(snapshot_a)
        paths_b = set(snapshot_b)

        added_paths = paths_b - paths_a
        removed_paths = paths_a - paths_b
        common_paths = paths_a & paths_b

        added: list[DocDiff] = []
        for p in sorted(added_paths):
            headings = extract_headings(snapshot_b[p])
            lines = len(snapshot_b[p].splitlines())
            added.append(DocDiff(
                path=p,
                change="added",
                headings_added=headings,
                semantic_similarity=0.0,
                line_changes=(lines, 0),
            ))

        removed: list[DocDiff] = []
        for p in sorted(removed_paths):
            headings = extract_headings(snapshot_a[p])
            lines = len(snapshot_a[p].splitlines())
            removed.append(DocDiff(
                path=p,
                change="removed",
                headings_removed=headings,
                semantic_similarity=0.0,
                line_changes=(0, lines),
            ))

        modified: list[DocDiff] = []
        for p in sorted(common_paths):
            if snapshot_a[p] != snapshot_b[p]:
                d = diff_docs(p, snapshot_a[p], p, snapshot_b[p])
                modified.append(d)

        return self._build_result(added, removed, modified)

    # ------------------------------------------------------------------
    # diff_git_commits
    # ------------------------------------------------------------------
    def diff_git_commits(
        self,
        commit_a: str,
        commit_b: str,
    ) -> BulkDiffResult:
        """Diff between two git commits using ``git diff --name-status``."""
        name_status = self._git_run(
            ["git", "diff", "--name-status", commit_a, commit_b],
            cwd=self.docs_dir,
        )

        added: list[DocDiff] = []
        removed: list[DocDiff] = []
        modified: list[DocDiff] = []

        for line in name_status.splitlines():
            line = line.strip()
            if not line:
                continue
            parts = line.split("\t", maxsplit=2)
            status = parts[0][0]  # A/D/M/R (rename: R100\told\tnew)

            if status == "A" and len(parts) >= 2:
                path = parts[1]
                content = self._git_show(commit_b, path)
                headings = extract_headings(content)
                added.append(DocDiff(
                    path=path, change="added",
                    headings_added=headings,
                    line_changes=(len(content.splitlines()), 0),
                ))
            elif status == "D" and len(parts) >= 2:
                path = parts[1]
                content = self._git_show(commit_a, path)
                headings = extract_headings(content)
                removed.append(DocDiff(
                    path=path, change="removed",
                    headings_removed=headings,
                    line_changes=(0, len(content.splitlines())),
                ))
            elif status == "M" and len(parts) >= 2:
                path = parts[1]
                content_a = self._git_show(commit_a, path)
                content_b = self._git_show(commit_b, path)
                d = diff_docs(path, content_a, path, content_b)
                modified.append(d)
            elif status == "R" and len(parts) >= 3:
                path_old = parts[1]
                path_new = parts[2]
                content_a = self._git_show(commit_a, path_old)
                content_b = self._git_show(commit_b, path_new)
                d = diff_docs(path_old, content_a, path_new, content_b)
                d.change = "renamed"
                modified.append(d)

        return self._build_result(added, removed, modified)

    # ------------------------------------------------------------------
    # diff_since
    # ------------------------------------------------------------------
    def diff_since(self, days: int) -> BulkDiffResult:
        """Compare HEAD vs the commit approximately *days* ago."""
        # Find commit N days ago
        old_commit_output = self._git_run(
            ["git", "log", f"--since={days} days ago", "--oneline"],
            cwd=self.docs_dir,
        )
        lines = [l.strip() for l in old_commit_output.splitlines() if l.strip()]
        if not lines:
            # No commits in that range — return empty
            return self._build_result([], [], [])
        # The last line is the oldest commit in the range
        oldest_commit = lines[-1].split()[0]
        return self.diff_git_commits(oldest_commit, "HEAD")

    # ------------------------------------------------------------------
    # to_markdown
    # ------------------------------------------------------------------
    def to_markdown(self, result: BulkDiffResult) -> str:
        """Render BulkDiffResult as a Markdown report."""
        lines: list[str] = []
        lines.append("# Bulk Diff Report\n")
        lines.append(f"**Summary:** {result.summary}\n")
        lines.append(
            f"- Added: {result.total_added} | "
            f"Removed: {result.total_removed} | "
            f"Modified: {result.total_modified}\n"
        )

        if result.added:
            lines.append("\n## Added Documents\n")
            for d in result.added:
                lines.append(f"- `{d.path}` (+{d.line_changes[0]} lines)")
                if d.headings_added:
                    lines.append(f"  - Headings: {', '.join(d.headings_added[:5])}")

        if result.removed:
            lines.append("\n## Removed Documents\n")
            for d in result.removed:
                lines.append(f"- `{d.path}` (-{d.line_changes[1]} lines)")

        if result.modified:
            lines.append("\n## Modified Documents\n")
            for d in result.modified:
                add, rem = d.line_changes
                sim_pct = f"{d.semantic_similarity * 100:.0f}%"
                lines.append(
                    f"- `{d.path}` (+{add}/-{rem} lines, similarity {sim_pct})"
                )
                if d.headings_added:
                    lines.append(
                        f"  - Headings added: {', '.join(d.headings_added[:3])}"
                    )
                if d.headings_removed:
                    lines.append(
                        f"  - Headings removed: {', '.join(d.headings_removed[:3])}"
                    )

        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    @staticmethod
    def _build_result(
        added: list[DocDiff],
        removed: list[DocDiff],
        modified: list[DocDiff],
    ) -> BulkDiffResult:
        total_a = sum(d.line_changes[0] for d in added + modified)
        total_r = sum(d.line_changes[1] for d in removed + modified)
        summary = (
            f"{len(added)} doc(s) added, "
            f"{len(removed)} doc(s) removed, "
            f"{len(modified)} doc(s) modified. "
            f"+{total_a}/-{total_r} lines total."
        )
        return BulkDiffResult(
            added=added,
            removed=removed,
            modified=modified,
            summary=summary,
            total_added=len(added),
            total_removed=len(removed),
            total_modified=len(modified),
        )

    @staticmethod
    def _git_run(cmd: list[str], cwd: Path) -> str:
        """Run a git command and return stdout, or empty string on error."""
        try:
            result = subprocess.run(
                cmd,
                cwd=str(cwd),
                capture_output=True,
                text=True,
                timeout=30,
            )
            return result.stdout
        except Exception:
            return ""

    def _git_show(self, commit: str, path: str) -> str:
        """Retrieve file content at a specific commit."""
        try:
            result = subprocess.run(
                ["git", "show", f"{commit}:{path}"],
                cwd=str(self.docs_dir),
                capture_output=True,
                text=True,
                timeout=30,
            )
            return result.stdout
        except Exception:
            return ""
