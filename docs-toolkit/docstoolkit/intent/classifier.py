"""Rule-based query intent classifier (RU + EN, no ML)."""
import re
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Intent labels
# ---------------------------------------------------------------------------

FACTOID = "factoid"
EXPLANATION = "explanation"
COMPARISON = "comparison"
SYNTHESIS = "synthesis"
OPINION = "opinion"
INSTRUCTION = "instruction"
UNKNOWN = "unknown"


# ---------------------------------------------------------------------------
# Dataclass
# ---------------------------------------------------------------------------

@dataclass
class Intent:
    """Classified query intent."""
    label: str
    confidence: float
    extracted: dict = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Pattern rules
# ---------------------------------------------------------------------------

# Each rule: (pattern_re, confidence, label)
# Patterns are matched case-insensitively against the full query.
_RULES: list[tuple[re.Pattern, float, str]] = []


def _add(pattern: str, confidence: float, label: str) -> None:
    _RULES.append((re.compile(pattern, re.IGNORECASE | re.UNICODE), confidence, label))


# INSTRUCTION  (check before explanation — "как сделать" is more specific than "как")
_add(r"\bкак\s+(сделать|установить|настроить|запустить|создать|написать|использовать)\b", 0.92, INSTRUCTION)
_add(r"\bинструкция\b", 0.92, INSTRUCTION)
_add(r"\bшаги\b", 0.88, INSTRUCTION)
_add(r"\bhow\s+to\b", 0.92, INSTRUCTION)
_add(r"\bsteps?\s+to\b", 0.88, INSTRUCTION)
_add(r"\bguide\b", 0.82, INSTRUCTION)
_add(r"\binstall\b", 0.80, INSTRUCTION)

# COMPARISON
_add(r"\bсравни\b", 0.92, COMPARISON)
_add(r"\bчем\s+отличается\b", 0.92, COMPARISON)
_add(r"\bотличие\b", 0.85, COMPARISON)
_add(r"\bvs\.?\b", 0.90, COMPARISON)
_add(r"\bversus\b", 0.90, COMPARISON)
_add(r"\bcompare\b", 0.90, COMPARISON)
_add(r"\bdifference\s+between\b", 0.92, COMPARISON)
_add(r"\bvsравни\b", 0.90, COMPARISON)

# SYNTHESIS
_add(r"\bобобщи\b", 0.92, SYNTHESIS)
_add(r"\bсуммаризуй\b", 0.92, SYNTHESIS)
_add(r"\bчто\s+известно\b", 0.88, SYNTHESIS)
_add(r"\bsummariz\b", 0.92, SYNTHESIS)
_add(r"\boverview\s+of\b", 0.90, SYNTHESIS)
_add(r"\beverything\s+about\b", 0.90, SYNTHESIS)
_add(r"\bдайте\s+обзор\b", 0.88, SYNTHESIS)
_add(r"\bобзор\b", 0.82, SYNTHESIS)

# OPINION
_add(r"\bоцени\b", 0.90, OPINION)
_add(r"\bтвоё\s+мнение\b", 0.90, OPINION)
_add(r"\bлучший\b", 0.85, OPINION)
_add(r"\bрекоменд\w+\b", 0.88, OPINION)
_add(r"\bbest\b", 0.80, OPINION)
_add(r"\brecommend\b", 0.88, OPINION)
_add(r"\bopinion\s+on\b", 0.90, OPINION)
_add(r"\bстоит\s+ли\b", 0.82, OPINION)

# EXPLANATION
_add(r"\bкак\s+работает\b", 0.92, EXPLANATION)
_add(r"\bпочему\b", 0.88, EXPLANATION)
_add(r"\bобъясни\b", 0.90, EXPLANATION)
_add(r"\bрасскажи\b", 0.85, EXPLANATION)
_add(r"\bhow\s+does\b", 0.92, EXPLANATION)
_add(r"\bwhy\b", 0.85, EXPLANATION)
_add(r"\bexplain\b", 0.90, EXPLANATION)
_add(r"\bwhat\s+makes\b", 0.82, EXPLANATION)
_add(r"\bкак\b", 0.70, EXPLANATION)  # fallback "как" without specific trigger

# FACTOID  (lower priority — check short queries separately)
_add(r"\bчто\s+такое\b", 0.92, FACTOID)
_add(r"\bкто\s+такой\b", 0.92, FACTOID)
_add(r"\bкогда\b", 0.85, FACTOID)
_add(r"\bгде\b", 0.80, FACTOID)
_add(r"\bwhat\s+is\b", 0.92, FACTOID)
_add(r"\bwho\s+is\b", 0.92, FACTOID)
_add(r"\bwhen\b", 0.82, FACTOID)
_add(r"\bwhere\b", 0.80, FACTOID)


def _word_count(query: str) -> int:
    return len(query.split())


def _has_two_named_entities(query: str) -> bool:
    """Detect if query contains at least 2 capitalised tokens or quoted strings."""
    quoted = re.findall(r'"[^"]+"', query)
    caps = re.findall(r'\b[А-ЯA-Z][а-яёa-z]{1,}\b', query)
    return len(quoted) + len(caps) >= 2


class IntentClassifier:
    """Rule-based intent classifier supporting Russian and English queries."""

    def classify(self, query: str) -> Intent:
        """Classify query, returning highest-confidence Intent."""
        # Collect all matching rules
        matches: list[tuple[float, str]] = []
        for pattern, conf, label in _RULES:
            if pattern.search(query):
                matches.append((conf, label))

        # Special boost: comparison when 2+ named entities are present
        if _has_two_named_entities(query):
            # check if comparison pattern fired or boost it
            comparison_present = any(lbl == COMPARISON for _, lbl in matches)
            if not comparison_present:
                # Check for "и / and" connecting two entities
                conj_pattern = re.compile(
                    r'\b[А-ЯA-Z][а-яёa-z]+\s+(?:и|and)\s+[А-ЯA-Z][а-яёa-z]+\b',
                    re.UNICODE,
                )
                if conj_pattern.search(query):
                    matches.append((0.85, COMPARISON))
            else:
                # Boost existing comparison match
                matches = [
                    (max(c, 0.92), lbl) if lbl == COMPARISON else (c, lbl)
                    for c, lbl in matches
                ]

        # Short query boost for factoid
        if _word_count(query) < 5:
            factoid_present = any(lbl == FACTOID for _, lbl in matches)
            if factoid_present:
                matches = [
                    (min(c + 0.05, 1.0), lbl) if lbl == FACTOID else (c, lbl)
                    for c, lbl in matches
                ]

        if not matches:
            return Intent(label=UNKNOWN, confidence=0.0)

        # Pick highest confidence match
        matches.sort(key=lambda x: -x[0])
        best_conf, best_label = matches[0]

        if best_conf < 0.5:
            return Intent(label=UNKNOWN, confidence=best_conf)

        extracted = self._extract_for_label(query, best_label)
        return Intent(label=best_label, confidence=round(best_conf, 3), extracted=extracted)

    def _extract_for_label(self, query: str, label: str) -> dict:
        if label == COMPARISON:
            entities = self.extract_entities(query)
            return {"entities": entities}
        return {}

    def extract_entities(self, query: str) -> list[str]:
        """Extract capitalised words and quoted strings as entities."""
        entities: list[str] = []
        # Quoted strings first
        for m in re.finditer(r'"([^"]+)"', query):
            entities.append(m.group(1))
        # Capitalised words (not at sentence start — but we include all here)
        for m in re.finditer(r'\b([А-ЯA-Z][а-яёa-z]{1,})\b', query):
            word = m.group(1)
            if word not in entities:
                entities.append(word)
        return entities
