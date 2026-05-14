"""Adversarial question generator: rule-based, no LLM required."""
import re
import random
from dataclasses import dataclass, field
from enum import Enum


class QuestionPattern(str, Enum):
    MULTI_HOP = "multi_hop"               # requires reasoning across multiple docs
    ENTITY_CONFUSION = "entity_confusion"  # similar entities that could be confused
    TIME_SENSITIVE = "time_sensitive"      # depends on temporal ordering
    CONTRADICTORY = "contradictory"        # premise contradicts corpus
    GAP = "gap"                           # topic not covered in corpus


_PATTERN_DIFFICULTY = {
    QuestionPattern.MULTI_HOP: 0.8,
    QuestionPattern.ENTITY_CONFUSION: 0.7,
    QuestionPattern.TIME_SENSITIVE: 0.75,
    QuestionPattern.CONTRADICTORY: 0.9,
    QuestionPattern.GAP: 0.65,
}

_PATTERN_WEAKNESS = {
    QuestionPattern.MULTI_HOP: "multi-document reasoning",
    QuestionPattern.ENTITY_CONFUSION: "entity disambiguation",
    QuestionPattern.TIME_SENSITIVE: "temporal reasoning",
    QuestionPattern.CONTRADICTORY: "premise validation",
    QuestionPattern.GAP: "corpus coverage",
}


@dataclass
class HardQuestion:
    """An adversarially generated hard question."""
    question: str
    pattern: QuestionPattern
    source_doc_ids: list = field(default_factory=list)  # docs used to generate it
    predicted_difficulty: float = 0.5   # 0=easy, 1=very hard
    target_weakness: str = ""           # what weakness this exploits

    def is_hard(self, threshold: float = 0.6) -> bool:
        return self.predicted_difficulty >= threshold


class AdversarialGenerator:
    """Generates hard questions from corpus passages.

    Rule-based (no LLM): pattern matching and template filling.
    """

    def __init__(self, seed: int | None = None):
        self._rng = random.Random(seed)

    def generate(
        self,
        passages: list,       # list of Passage-like with .text, .doc_id
        n: int = 5,
        patterns: list | None = None,  # list[QuestionPattern] to use; None = all
    ) -> list:
        """Generate n HardQuestion objects from passages.

        For each question:
        1. Pick a random pattern (from patterns or all if None)
        2. Pick 1-2 random passages
        3. Generate question using _apply_pattern()
        4. Set predicted_difficulty based on pattern:
           MULTI_HOP=0.8, ENTITY_CONFUSION=0.7, TIME_SENSITIVE=0.75,
           CONTRADICTORY=0.9, GAP=0.65

        Return list of n HardQuestions.
        """
        available_patterns = list(patterns) if patterns else list(QuestionPattern)
        results = []

        for _ in range(n):
            pattern = self._rng.choice(available_patterns)

            # Pick 1-2 passages
            if not passages:
                selected = []
            elif len(passages) == 1:
                selected = passages[:]
            else:
                count = 2 if pattern == QuestionPattern.MULTI_HOP else 1
                count = min(count, len(passages))
                selected = self._rng.sample(passages, count)

            question_text, doc_ids, weakness = self._apply_pattern(pattern, selected)

            hq = HardQuestion(
                question=question_text,
                pattern=pattern,
                source_doc_ids=doc_ids,
                predicted_difficulty=_PATTERN_DIFFICULTY[pattern],
                target_weakness=weakness,
            )
            results.append(hq)

        return results

    def _apply_pattern(
        self,
        pattern: QuestionPattern,
        passages: list,
    ) -> tuple:
        """Generate (question_text, source_doc_ids, target_weakness).

        MULTI_HOP: "What connects {entity_from_p1} and {entity_from_p2}?"
          - extract first capitalized word from each passage
          - target_weakness = "multi-document reasoning"

        ENTITY_CONFUSION: "How is {entity_A} different from {entity_B}?"
          - extract two capitalized words from one passage
          - if only one found: use passage title or doc_id
          - target_weakness = "entity disambiguation"

        TIME_SENSITIVE: "What changed about {topic} after {year}?"
          - find a 4-digit year in passage (1990-2030), else use "2020"
          - extract first keyword (>= 5 chars) from passage
          - target_weakness = "temporal reasoning"

        CONTRADICTORY: "Is it true that {claim}?"
          - take first sentence of passage (up to first period)
          - target_weakness = "premise validation"

        GAP: "What is the relationship between {topic} and {missing_concept}?"
          - extract a keyword from passage
          - missing_concept = "_unknown_" (represents a gap)
          - target_weakness = "corpus coverage"

        Returns (question: str, doc_ids: list[str], weakness: str)
        """
        doc_ids = [getattr(p, "doc_id", "unknown") for p in passages]
        weakness = _PATTERN_WEAKNESS[pattern]

        if pattern == QuestionPattern.MULTI_HOP:
            entities = []
            for p in passages:
                ents = self._extract_entities(getattr(p, "text", ""))
                entities.append(ents[0] if ents else getattr(p, "doc_id", "unknown"))
            while len(entities) < 2:
                entities.append("unknown")
            question = f"What connects {entities[0]} and {entities[1]}?"
            return question, doc_ids, weakness

        if pattern == QuestionPattern.ENTITY_CONFUSION:
            text = getattr(passages[0], "text", "") if passages else ""
            ents = self._extract_entities(text)
            if len(ents) >= 2:
                entity_a, entity_b = ents[0], ents[1]
            elif len(ents) == 1:
                entity_a = ents[0]
                entity_b = getattr(passages[0], "doc_id", "unknown") if passages else "unknown"
            else:
                entity_a = getattr(passages[0], "doc_id", "unknown") if passages else "unknown"
                entity_b = "unknown"
            question = f"How is {entity_a} different from {entity_b}?"
            return question, doc_ids, weakness

        if pattern == QuestionPattern.TIME_SENSITIVE:
            text = getattr(passages[0], "text", "") if passages else ""
            # Find a 4-digit year in range 1990-2030
            years = re.findall(r'\b((?:199\d|20[012]\d|2030))\b', text)
            year = years[0] if years else "2020"
            keywords = self._extract_keywords(text, min_len=5)
            topic = keywords[0] if keywords else "topic"
            question = f"What changed about {topic} after {year}?"
            return question, doc_ids, weakness

        if pattern == QuestionPattern.CONTRADICTORY:
            text = getattr(passages[0], "text", "") if passages else ""
            # First sentence: up to first period
            first_sentence = text.split(".")[0].strip() if text else ""
            if not first_sentence:
                first_sentence = "this claim is correct"
            question = f"Is it true that {first_sentence}?"
            return question, doc_ids, weakness

        if pattern == QuestionPattern.GAP:
            text = getattr(passages[0], "text", "") if passages else ""
            keywords = self._extract_keywords(text, min_len=5)
            topic = keywords[0] if keywords else "topic"
            missing_concept = "_unknown_"
            question = f"What is the relationship between {topic} and {missing_concept}?"
            return question, doc_ids, weakness

        # Fallback (should not reach here)
        return "Unknown question?", doc_ids, weakness

    def _extract_entities(self, text: str) -> list:
        """Extract capitalized words (not at sentence start) from text."""
        words = text.split()
        entities = []
        for i, w in enumerate(words):
            clean = re.sub(r'[^\w]', '', w)
            if clean and clean[0].isupper() and i > 0:
                entities.append(clean)
        return entities

    def _extract_keywords(self, text: str, min_len: int = 5) -> list:
        """Extract unique lowercase words >= min_len chars."""
        return list(set(
            w.lower() for w in re.findall(r'\b\w{' + str(min_len) + r',}\b', text)
        ))
