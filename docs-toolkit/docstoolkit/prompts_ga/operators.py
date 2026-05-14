"""Mutation and crossover operators for GA-based prompt evolution."""
import random
import re
from enum import Enum


class MutationOp(Enum):
    REPHRASE = "rephrase"   # paraphrase a random sentence (rule-based, no LLM)
    INJECT = "inject"       # add a random instruction phrase
    REMOVE = "remove"       # remove a random sentence
    REORDER = "reorder"     # swap two sentences


# Pool of instruction phrases to inject
_INJECT_PHRASES = [
    "Be concise.",
    "Use bullet points.",
    "Cite your sources.",
    "Think step by step.",
    "Be specific and precise.",
    "Focus on the most relevant information.",
    "Avoid unnecessary repetition.",
    "Use simple language.",
]

# Rule-based synonym pairs (substring replacement, RU+EN)
_REPHRASE_RULES = [
    ("использ", "примен"),
    ("получ", "выдел"),
    ("return", "provide"),
    ("use", "apply"),
    ("generate", "produce"),
    ("create", "build"),
    ("show", "display"),
    ("list", "enumerate"),
]


def _split_sentences(text: str) -> list[str]:
    """Split text into sentences on '. ', '.\\n', '! ', '? ' boundaries."""
    # Split on sentence-ending punctuation followed by space or newline
    parts = re.split(r'(?<=[.!?])[\s]+', text.strip())
    # Filter out empty strings
    return [p.strip() for p in parts if p.strip()]


def _join_sentences(sentences: list[str]) -> str:
    """Re-join sentences with ' ' separator, strip trailing whitespace.

    Sentences that already end with punctuation (.!?) are joined with a space;
    sentences that do not are given a period before the space.
    """
    if not sentences:
        return ""
    parts = []
    for i, s in enumerate(sentences):
        s = s.strip()
        if not s:
            continue
        if i < len(sentences) - 1:
            # Ensure sentence ends with punctuation before the next one
            if s and s[-1] not in ".!?":
                s = s + "."
        parts.append(s)
    return " ".join(parts).strip()


def mutate(
    template: str,
    op: MutationOp | None = None,   # None → random op
    rng: random.Random | None = None,
) -> str:
    """Apply one mutation operator to the template string.

    REPHRASE: pick a random sentence, replace common words with synonyms
      (simple rule-based: "использ" → "примен", "получ" → "выдел",
       "return" → "provide", "use" → "apply", etc.)
    INJECT: add a random phrase from _INJECT_PHRASES at a random position
    REMOVE: remove a random sentence (if >1 sentence remains)
    REORDER: swap two random sentences (if >1 sentence)

    If template has only 1 sentence, REMOVE and REORDER fall back to INJECT.
    Always return a non-empty string.
    """
    if rng is None:
        rng = random.Random()
    if op is None:
        op = rng.choice(list(MutationOp))

    sentences = _split_sentences(template)

    if op == MutationOp.INJECT or (op in (MutationOp.REMOVE, MutationOp.REORDER) and len(sentences) <= 1):
        phrase = rng.choice(_INJECT_PHRASES)
        if not sentences:
            return phrase
        pos = rng.randint(0, len(sentences))
        sentences.insert(pos, phrase)
        return _join_sentences(sentences)

    if op == MutationOp.REMOVE:
        # len(sentences) > 1 guaranteed here
        idx = rng.randrange(len(sentences))
        sentences.pop(idx)
        result = _join_sentences(sentences)
        return result if result.strip() else template

    if op == MutationOp.REORDER:
        # len(sentences) > 1 guaranteed here
        if len(sentences) == 2:
            sentences = [sentences[1], sentences[0]]
        else:
            i, j = rng.sample(range(len(sentences)), 2)
            sentences[i], sentences[j] = sentences[j], sentences[i]
        return _join_sentences(sentences)

    if op == MutationOp.REPHRASE:
        if not sentences:
            return template
        idx = rng.randrange(len(sentences))
        sentence = sentences[idx]
        # Apply rule-based substitutions
        for old, new in _REPHRASE_RULES:
            if old in sentence:
                sentence = sentence.replace(old, new, 1)
                break  # one substitution per rephrase
        sentences[idx] = sentence
        return _join_sentences(sentences)

    return template


def crossover(
    parent_a: str,
    parent_b: str,
    rng: random.Random | None = None,
) -> tuple[str, str]:
    """Sentence-level crossover between two prompt templates.

    Algorithm:
    1. Split each parent into sentences
    2. If either has <2 sentences: return (parent_a, parent_b) unchanged
    3. Pick crossover point randomly: cross_a in [1, len(a)-1], cross_b in [1, len(b)-1]
    4. child_1 = a[:cross_a] + b[cross_b:]
    5. child_2 = b[:cross_b] + a[cross_a:]
    6. Return (_join_sentences(child_1), _join_sentences(child_2))
    """
    if rng is None:
        rng = random.Random()

    sents_a = _split_sentences(parent_a)
    sents_b = _split_sentences(parent_b)

    if len(sents_a) < 2 or len(sents_b) < 2:
        return (parent_a, parent_b)

    cross_a = rng.randint(1, len(sents_a) - 1)
    cross_b = rng.randint(1, len(sents_b) - 1)

    child_1 = sents_a[:cross_a] + sents_b[cross_b:]
    child_2 = sents_b[:cross_b] + sents_a[cross_a:]

    return (_join_sentences(child_1), _join_sentences(child_2))
