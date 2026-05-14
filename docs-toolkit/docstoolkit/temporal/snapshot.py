"""CorpusSnapshot: corpus state at a specific git commit, with TF-IDF search."""
import math
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class CorpusSnapshot:
    """A corpus state at a specific git commit."""
    commit: str
    timestamp: str                  # ISO 8601
    docs: dict[str, str]            # path → content (relative paths)

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        """Simple TF-IDF search over docs. Returns [{path, score, snippet}]."""
        if not self.docs or not query.strip():
            return []

        query_tokens = _tokenize(query)
        if not query_tokens:
            return []

        # Build IDF over all docs
        doc_list = list(self.docs.items())
        num_docs = len(doc_list)

        # df: how many docs contain each term
        df: dict[str, int] = {}
        for _, content in doc_list:
            tokens = set(_tokenize(content))
            for t in tokens:
                df[t] = df.get(t, 0) + 1

        def idf(term: str) -> float:
            return math.log((num_docs + 1) / (df.get(term, 0) + 1)) + 1.0

        # Score each doc: sum of tf*idf for query terms
        results = []
        for path, content in doc_list:
            tokens = _tokenize(content)
            if not tokens:
                continue
            tf_map: dict[str, float] = {}
            for t in tokens:
                tf_map[t] = tf_map.get(t, 0) + 1
            total = len(tokens)

            score = 0.0
            for qt in query_tokens:
                tf = tf_map.get(qt, 0) / total if total > 0 else 0.0
                score += tf * idf(qt)

            if score > 0:
                snippet = _snippet(content, query_tokens)
                results.append({"path": path, "score": score, "snippet": snippet})

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

    def doc_count(self) -> int:
        return len(self.docs)

    def has_doc(self, path: str) -> bool:
        return path in self.docs


def _tokenize(text: str) -> list[str]:
    """Lowercase word tokenization, no external deps."""
    return re.findall(r"[a-zA-Zа-яёА-ЯЁ0-9]+", text.lower())


def _snippet(content: str, query_tokens: list[str], window: int = 120) -> str:
    """Extract a snippet around the first query token match."""
    lower = content.lower()
    best_pos = len(content)
    for qt in query_tokens:
        idx = lower.find(qt)
        if idx != -1 and idx < best_pos:
            best_pos = idx
    if best_pos == len(content):
        return content[:window]
    start = max(0, best_pos - 30)
    end = min(len(content), start + window)
    return content[start:end]


def snapshot_index(
    repo_path: str | Path,
    commit: str,
    file_glob: str = "docs/**/*.md",
) -> "CorpusSnapshot":
    """Build CorpusSnapshot for a git commit.

    Uses: git ls-tree -r --name-only <commit> -- <path>
    Then: git show <commit>:<path> for each file

    IMPORTANT: If git operations fail (not a git repo, commit not found),
    return empty CorpusSnapshot with commit=commit, timestamp="", docs={}.
    Never raise exceptions from git failures.
    """
    repo_path = Path(repo_path)

    # Derive a path prefix from the glob (e.g. "docs/**/*.md" → "docs/")
    glob_parts = file_glob.split("/")
    # Use the first segment as the tree prefix
    tree_prefix = glob_parts[0] if glob_parts else "docs"

    try:
        # Get commit timestamp
        ts_result = subprocess.run(
            ["git", "-C", str(repo_path), "log", "-1", "--format=%ai", commit],
            capture_output=True, text=True, timeout=15,
        )
        timestamp = ts_result.stdout.strip() if ts_result.returncode == 0 else ""

        # List files at that commit under the prefix
        ls_result = subprocess.run(
            ["git", "-C", str(repo_path), "ls-tree", "-r", "--name-only",
             commit, "--", tree_prefix],
            capture_output=True, text=True, timeout=15,
        )
        if ls_result.returncode != 0:
            return CorpusSnapshot(commit=commit, timestamp="", docs={})

        # Filter by extension from glob (e.g. "*.md")
        ext = ""
        if "." in file_glob:
            ext = "." + file_glob.rsplit(".", 1)[-1]

        docs: dict[str, str] = {}
        for filepath in ls_result.stdout.splitlines():
            filepath = filepath.strip()
            if not filepath:
                continue
            if ext and not filepath.endswith(ext):
                continue
            # Fetch content
            show_result = subprocess.run(
                ["git", "-C", str(repo_path), "show", f"{commit}:{filepath}"],
                capture_output=True, text=True, timeout=15,
            )
            if show_result.returncode == 0:
                docs[filepath] = show_result.stdout

        return CorpusSnapshot(commit=commit, timestamp=timestamp, docs=docs)

    except Exception:
        return CorpusSnapshot(commit=commit, timestamp="", docs={})
