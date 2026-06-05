"""Per-user profiles, preferences, and personalized retrieval."""
import json
import re
import sqlite3
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from docstoolkit.config import load_config
from docstoolkit.rag.types import Passage


SCHEMA = """
CREATE TABLE IF NOT EXISTS profiles (
    user_id TEXT PRIMARY KEY,
    interests_json TEXT NOT NULL DEFAULT '[]',
    read_docs_json TEXT NOT NULL DEFAULT '[]',
    preferred_sections_json TEXT NOT NULL DEFAULT '[]',
    preferred_retriever TEXT NOT NULL DEFAULT 'hybrid',
    created_ts TEXT NOT NULL,
    updated_ts TEXT NOT NULL
);
"""

# Stopwords for interest extraction (RU + EN)
_STOPWORDS = {
    # Russian
    "и", "в", "на", "не", "с", "по", "для", "что", "как", "это", "из",
    "от", "до", "за", "при", "или", "но", "а", "же", "бы", "так", "все",
    "уже", "было", "есть", "быть", "его", "ее", "их", "они", "мы", "вы",
    "он", "она", "оно", "я", "мне", "нас", "вас", "им", "об", "со",
    # English
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
    "it", "this", "that", "which", "who", "what", "how", "when", "where",
    "not", "no", "as", "if", "then", "so", "also", "have", "has", "had",
}


@dataclass
class UserProfile:
    """Per-user preferences and read history."""
    user_id: str
    interests: list[str] = field(default_factory=list)
    read_docs: set[str] = field(default_factory=set)
    preferred_sections: list[str] = field(default_factory=list)
    preferred_retriever: str = "hybrid"
    created_ts: str = ""
    updated_ts: str = ""

    def __post_init__(self):
        if not self.created_ts:
            self.created_ts = datetime.now().isoformat(timespec='seconds')
        if not self.updated_ts:
            self.updated_ts = self.created_ts


class ProfileStore:
    """SQLite-backed store for user profiles."""

    def __init__(self, db_path: Path | None = None):
        if db_path is None:
            cfg = load_config()
            db_path = cfg.root / ".docstoolkit" / "profiles.sqlite"
        self.path = Path(db_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.path))
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)
        self.conn.commit()

    def close(self):
        self.conn.close()

    def save(self, profile: UserProfile) -> None:
        """Upsert a profile."""
        profile.updated_ts = datetime.now().isoformat(timespec='seconds')
        self.conn.execute(
            "INSERT OR REPLACE INTO profiles "
            "(user_id, interests_json, read_docs_json, preferred_sections_json, "
            " preferred_retriever, created_ts, updated_ts) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                profile.user_id,
                json.dumps(profile.interests, ensure_ascii=False),
                json.dumps(sorted(profile.read_docs), ensure_ascii=False),
                json.dumps(profile.preferred_sections, ensure_ascii=False),
                profile.preferred_retriever,
                profile.created_ts,
                profile.updated_ts,
            ),
        )
        self.conn.commit()

    def load(self, user_id: str) -> UserProfile | None:
        """Load a profile by user_id, or None if not found."""
        row = self.conn.execute(
            "SELECT * FROM profiles WHERE user_id = ?", (user_id,)
        ).fetchone()
        if not row:
            return None
        return self._row_to_profile(row)

    def mark_read(self, user_id: str, doc_id: str) -> None:
        """Add doc_id to user's read_docs set."""
        profile = self.load(user_id)
        if profile is None:
            profile = UserProfile(user_id=user_id)
        profile.read_docs.add(doc_id)
        self.save(profile)

    def update_interests(self, user_id: str, new_terms: list[str]) -> None:
        """Merge new_terms with existing interests, keep top-50 unique terms."""
        profile = self.load(user_id)
        if profile is None:
            profile = UserProfile(user_id=user_id)
        # Merge and deduplicate, preserving existing order first
        combined: list[str] = list(profile.interests)
        existing_set = set(combined)
        for term in new_terms:
            if term not in existing_set:
                combined.append(term)
                existing_set.add(term)
        profile.interests = combined[:50]
        self.save(profile)

    def list_users(self) -> list[str]:
        """Return all user_ids."""
        rows = self.conn.execute(
            "SELECT user_id FROM profiles ORDER BY updated_ts DESC"
        ).fetchall()
        return [r["user_id"] for r in rows]

    def _row_to_profile(self, row) -> UserProfile:
        return UserProfile(
            user_id=row["user_id"],
            interests=json.loads(row["interests_json"] or "[]"),
            read_docs=set(json.loads(row["read_docs_json"] or "[]")),
            preferred_sections=json.loads(row["preferred_sections_json"] or "[]"),
            preferred_retriever=row["preferred_retriever"] or "hybrid",
            created_ts=row["created_ts"],
            updated_ts=row["updated_ts"],
        )


class PersonalizedRetriever:
    """Wraps a base retriever with per-user re-ranking."""

    def __init__(self, base_retriever, profile: UserProfile):
        self.base = base_retriever
        self.profile = profile

    def search(self, query: str, top_k: int = 5) -> list[Passage]:
        """Search with personalization: section boost, read-penalty, interest injection."""
        # Augment query with top-2 interests if they add context
        augmented_query = query
        if self.profile.interests:
            top_interests = self.profile.interests[:2]
            # Only add if not already in query
            extras = [t for t in top_interests if t.lower() not in query.lower()]
            if extras:
                augmented_query = query + " " + " ".join(extras)

        # Retrieve 2x candidates
        candidates: list[Passage] = self.base.search(augmented_query, top_k * 2)

        # Re-rank
        scored: list[tuple[float, Passage]] = []
        for passage in candidates:
            score = passage.score

            # Boost for preferred sections
            for section in self.profile.preferred_sections:
                if section in passage.doc_id or section in passage.title:
                    score += 0.2
                    break

            # Penalize already-read docs
            if passage.doc_id in self.profile.read_docs:
                score -= 0.1

            scored.append((score, passage))

        # Sort descending by adjusted score
        scored.sort(key=lambda x: -x[0])

        result: list[Passage] = []
        for adjusted_score, passage in scored[:top_k]:
            from dataclasses import replace
            try:
                p = replace(passage, score=adjusted_score)
            except TypeError:
                # Fallback if Passage doesn't support replace
                p = Passage(
                    text=passage.text,
                    doc_id=passage.doc_id,
                    title=passage.title,
                    score=adjusted_score,
                )
            result.append(p)
        return result


def apply_profile(
    user_id: str,
    kwargs: dict,
    store: "ProfileStore | None" = None,
) -> dict:
    """Middleware: inject per-user defaults into kwargs for rag.ask / agent.run.

    Loads UserProfile by user_id and overrides kwargs fields:
      - `method` ← profile.preferred_retriever (only if caller did not override)
      - kwargs is mutated and also returned for chaining

    Caller-provided values always win. Unknown user → no-op (returns kwargs unchanged).
    `_profile` is stashed in kwargs so downstream RAGPipeline can wrap the retriever.
    """
    own_store = False
    if store is None:
        store = ProfileStore()
        own_store = True
    try:
        profile = store.load(user_id)
        if profile is None:
            return kwargs
        # Honour caller-provided overrides; only fill what's absent.
        kwargs.setdefault("method", profile.preferred_retriever)
        kwargs["_profile"] = profile
        return kwargs
    finally:
        if own_store:
            store.close()


def infer_interests(passages: list[Passage], top_n: int = 10) -> list[str]:
    """Extract most frequent meaningful words from passage titles/texts.

    Filters stopwords, returns top_n terms as interest candidates.
    """
    counter: Counter = Counter()
    for p in passages:
        combined = (p.title + " " + p.text).lower()
        tokens = re.findall(r'\b[a-zA-Zа-яА-ЯёЁ][\w\-]{2,}\b', combined)
        for tok in tokens:
            if tok.lower() not in _STOPWORDS and len(tok) >= 3:
                counter[tok] += 1

    return [term for term, _ in counter.most_common(top_n)]
