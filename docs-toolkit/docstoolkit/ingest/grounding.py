"""Cross-modal grounding: link images to surrounding text spans."""
import json
import math
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from docstoolkit.rag.types import Passage


# Markdown image pattern: ![alt](path)
_IMG_RE = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')

# Stopwords for keyword extraction
_STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
    "it", "this", "that", "which", "who", "what", "how",
    "и", "в", "на", "не", "с", "по", "для", "что", "как", "это", "из",
    "от", "до", "за", "при", "или", "но", "а", "же", "бы", "так",
}


@dataclass
class ImageRef:
    """Reference to an image with surrounding text context."""
    path: str
    alt_text: str
    caption: str
    context_before: str   # 100 chars before the image tag
    context_after: str    # 100 chars after the image tag
    doc_id: str


@dataclass
class GroundedImage:
    """Image enriched with synthetic text for retrieval indexing."""
    ref: ImageRef
    synthetic_text: str
    keywords: list[str] = field(default_factory=list)


def extract_image_refs(markdown_text: str, doc_id: str) -> list[ImageRef]:
    """Parse all ![alt](path) patterns with 100-char context windows."""
    refs: list[ImageRef] = []
    for m in _IMG_RE.finditer(markdown_text):
        alt_text = m.group(1).strip()
        path = m.group(2).strip()
        start = m.start()
        end = m.end()

        # Context: 100 chars before/after the image tag
        context_before = markdown_text[max(0, start - 100):start]
        context_after = markdown_text[end:end + 100]

        # Caption heuristic: look for an italics or text line immediately after
        caption = ""
        after_stripped = context_after.strip()
        cap_match = re.match(r'^_([^_]+)_|^\*([^*]+)\*|^([^\n]{3,80})\n', after_stripped)
        if cap_match:
            caption = next(g for g in cap_match.groups() if g) or ""

        refs.append(ImageRef(
            path=path,
            alt_text=alt_text,
            caption=caption,
            context_before=context_before,
            context_after=context_after,
            doc_id=doc_id,
        ))
    return refs


def ground_image(ref: ImageRef) -> GroundedImage:
    """Create a GroundedImage with synthetic text and keywords."""
    synthetic_text = " ".join(filter(None, [
        ref.alt_text,
        ref.caption,
        ref.context_before,
        ref.context_after,
    ]))

    # Simple tokenization + stopword filtering
    tokens = re.findall(r'\b[a-zA-Zа-яА-ЯёЁ][\w\-]{1,}\b', synthetic_text.lower())
    counter: Counter = Counter()
    for tok in tokens:
        if tok not in _STOPWORDS and len(tok) >= 3:
            counter[tok] += 1

    keywords = [word for word, _ in counter.most_common(15)]

    return GroundedImage(
        ref=ref,
        synthetic_text=synthetic_text,
        keywords=keywords,
    )


def ground_document(markdown_text: str, doc_id: str) -> list[GroundedImage]:
    """Extract and ground all images from a markdown document."""
    refs = extract_image_refs(markdown_text, doc_id)
    return [ground_image(r) for r in refs]


def _tfidf_score(query_tokens: set[str], doc_tokens: list[str],
                 idf: dict[str, float]) -> float:
    """Simplified TF-IDF scoring for a document given query tokens."""
    if not doc_tokens:
        return 0.0
    tf: Counter = Counter(doc_tokens)
    total = len(doc_tokens)
    score = 0.0
    for tok in query_tokens:
        if tok in tf:
            term_tf = tf[tok] / total
            term_idf = idf.get(tok, 1.0)
            score += term_tf * term_idf
    return score


class ImageIndex:
    """In-memory image index with optional JSON persistence."""

    def __init__(self):
        self._images: list[GroundedImage] = []
        self._tokens_cache: list[list[str]] = []  # tokenized synthetic_text per image

    def add(self, grounded: GroundedImage) -> None:
        """Add a grounded image to the index."""
        self._images.append(grounded)
        tokens = re.findall(
            r'\b[a-zA-Zа-яА-ЯёЁ][\w\-]{1,}\b',
            grounded.synthetic_text.lower()
        )
        self._tokens_cache.append(tokens)

    def _build_idf(self) -> dict[str, float]:
        """Compute IDF over all indexed documents."""
        n = len(self._images)
        if n == 0:
            return {}
        df: Counter = Counter()
        for tokens in self._tokens_cache:
            for tok in set(tokens):
                df[tok] += 1
        idf: dict[str, float] = {}
        for tok, freq in df.items():
            idf[tok] = math.log((n + 1) / (freq + 1)) + 1.0
        return idf

    def search(self, query: str, top_k: int = 5) -> list[GroundedImage]:
        """TF-IDF-like search over synthetic_text of all indexed images."""
        if not self._images:
            return []
        query_tokens = set(re.findall(
            r'\b[a-zA-Zа-яА-ЯёЁ][\w\-]{1,}\b',
            query.lower()
        ))
        if not query_tokens:
            return []

        idf = self._build_idf()
        scored: list[tuple[float, int]] = []
        for idx, tokens in enumerate(self._tokens_cache):
            score = _tfidf_score(query_tokens, tokens, idf)
            if score > 0:
                scored.append((score, idx))

        scored.sort(key=lambda x: -x[0])
        return [self._images[idx] for _, idx in scored[:top_k]]

    def save(self, path: Path) -> None:
        """Serialize index to JSON."""
        data = []
        for gi in self._images:
            data.append({
                "ref": {
                    "path": gi.ref.path,
                    "alt_text": gi.ref.alt_text,
                    "caption": gi.ref.caption,
                    "context_before": gi.ref.context_before,
                    "context_after": gi.ref.context_after,
                    "doc_id": gi.ref.doc_id,
                },
                "synthetic_text": gi.synthetic_text,
                "keywords": gi.keywords,
            })
        Path(path).write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def load(self, path: Path) -> None:
        """Deserialize index from JSON (appends to existing)."""
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
        for item in raw:
            ref_data = item["ref"]
            ref = ImageRef(
                path=ref_data["path"],
                alt_text=ref_data["alt_text"],
                caption=ref_data["caption"],
                context_before=ref_data["context_before"],
                context_after=ref_data["context_after"],
                doc_id=ref_data["doc_id"],
            )
            gi = GroundedImage(
                ref=ref,
                synthetic_text=item["synthetic_text"],
                keywords=item["keywords"],
            )
            self.add(gi)

    def to_passages(self) -> list[Passage]:
        """Convert grounded images to Passage objects for inclusion in retrieval."""
        passages: list[Passage] = []
        for gi in self._images:
            title = gi.ref.alt_text or gi.ref.path
            passages.append(Passage(
                text=gi.synthetic_text,
                doc_id=gi.ref.doc_id,
                title=f"[image] {title}",
                score=0.0,
            ))
        return passages
