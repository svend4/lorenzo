"""Template-based abstractive summarization — pure stdlib."""
import re
from collections import Counter
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Stopwords (must match extractor so topics make sense)
# ---------------------------------------------------------------------------
_STOPWORDS: frozenset[str] = frozenset({
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
    "being", "have", "has", "had", "do", "does", "did", "will", "would",
    "could", "should", "may", "might", "shall", "can", "this", "that",
    "these", "those", "it", "its", "as", "if", "into", "up", "out",
    "not", "no", "nor", "so", "yet", "both", "either", "neither",
    "each", "every", "all", "any", "more", "most", "other", "such",
    "same", "than", "then", "there", "their", "they", "them", "we",
    "our", "you", "your", "he", "she", "his", "her", "my", "me",
    "who", "which", "what", "when", "where", "how", "just", "also",
    "about", "after", "before", "while", "during", "through", "over",
    "under", "between", "among", "against", "within", "without",
})


@dataclass
class TemplateConfig:
    """Templates used by AbstractiveSummarizer."""
    intro_template: str = "This document covers {topics}."
    body_template: str = "Key points: {key_points}."
    conclusion_template: str = "In summary: {conclusion}."


class AbstractiveSummarizer:
    """Template-driven summarizer: extract topics and key points, then fill templates."""

    def _tokenize_words(self, text: str) -> list[str]:
        """Return lowercase word tokens."""
        return re.findall(r"[a-zA-Zа-яёА-ЯЁ]+", text.lower())

    def extract_topics(self, text: str, n: int = 5) -> list[str]:
        """Return the top-n high-frequency content words as topic strings.

        Filters: token length >= 4, not a stopword.
        Sorted by frequency descending.
        """
        tokens = self._tokenize_words(text)
        counter: Counter = Counter(
            w for w in tokens if len(w) >= 4 and w not in _STOPWORDS
        )
        return [word for word, _ in counter.most_common(n)]

    def extract_key_points(self, text: str, n: int = 3) -> list[str]:
        """Return the top-n scoring sentences using extractive scoring."""
        from docstoolkit.summarization.extractor import ExtractiveSummarizer
        extractor = ExtractiveSummarizer()
        scored = extractor.key_sentences(text, n=n)
        # Return sentences in *score* order (key_sentences already sorts desc)
        return [ss.sentence for ss in scored]

    def summarize(self, text: str, config: TemplateConfig = None) -> str:
        """Build a three-part abstractive summary using templates.

        - Intro  : top-5 topics joined by ", "
        - Body   : top-3 key-point sentences joined by "; "
        - Conclusion: first key-point sentence (or first topic as fallback)
        """
        if config is None:
            config = TemplateConfig()

        if not text or not text.strip():
            return ""

        topics = self.extract_topics(text, n=5)
        key_points = self.extract_key_points(text, n=3)

        # Intro
        topics_str = ", ".join(topics) if topics else "various topics"
        intro = config.intro_template.format(topics=topics_str)

        # Body
        body_str = "; ".join(key_points) if key_points else text.strip()[:200]
        body = config.body_template.format(key_points=body_str)

        # Conclusion — first key-point sentence or first topic
        if key_points:
            conclusion_str = key_points[0]
        elif topics:
            conclusion_str = topics[0]
        else:
            conclusion_str = text.strip()[:100]
        conclusion = config.conclusion_template.format(conclusion=conclusion_str)

        return f"{intro} {body} {conclusion}"
