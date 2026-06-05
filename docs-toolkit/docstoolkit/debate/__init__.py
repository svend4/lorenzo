"""Multi-agent debate for robust, bias-resistant answers."""
from docstoolkit.debate.persona import Persona, SKEPTIC, SYNTHESIZER, CONTRARIAN
from docstoolkit.debate.round import DebateRound, run_debate_round
from docstoolkit.debate.result import DebateResult, multi_agent_debate

__all__ = [
    "Persona", "SKEPTIC", "SYNTHESIZER", "CONTRARIAN",
    "DebateRound", "run_debate_round",
    "DebateResult", "multi_agent_debate",
]
