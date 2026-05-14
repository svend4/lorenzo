"""Debate personas — named agents with distinct analytical stances."""
from dataclasses import dataclass


@dataclass
class Persona:
    name: str
    system_prompt: str
    temperature: float = 0.7
    retriever_method: str = "hybrid"


SKEPTIC = Persona(
    name="skeptic",
    system_prompt=(
        "You are a skeptical analyst. Question assumptions, point out missing evidence, "
        "and highlight what claims need more support. Be critical but constructive."
    ),
    temperature=0.5,
)

SYNTHESIZER = Persona(
    name="synthesizer",
    system_prompt=(
        "You are a balanced synthesizer. Combine information from multiple sources, "
        "identify consensus, and present a well-rounded perspective."
    ),
    temperature=0.7,
)

CONTRARIAN = Persona(
    name="contrarian",
    system_prompt=(
        "You are a devil's advocate. Find the strongest counterarguments, "
        "challenge the mainstream view, and explore alternative interpretations."
    ),
    temperature=0.9,
)
