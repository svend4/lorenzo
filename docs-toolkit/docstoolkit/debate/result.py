"""Debate result — synthesis and confidence scoring across debate rounds."""
from dataclasses import dataclass, field

from docstoolkit.debate.persona import Persona, SKEPTIC, SYNTHESIZER, CONTRARIAN
from docstoolkit.debate.round import DebateRound, run_debate_round


@dataclass
class DebateResult:
    question: str
    consensus: str                     # synthesized final answer
    dissenting: list[str]              # minority views
    confidence: float                  # 0-1: agreement level across agents
    rounds: list[DebateRound]
    personas_used: list[str]           # names

    def to_markdown(self) -> str:
        """Format debate as markdown with consensus, dissenting views, and round trace."""
        lines = [
            f"# Debate Result",
            f"",
            f"**Question:** {self.question}",
            f"",
            f"**Rounds:** {len(self.rounds)}",
            f"**Confidence:** {self.confidence:.2f}",
            f"**Personas:** {', '.join(self.personas_used)}",
            f"",
            f"## Consensus",
            f"",
            self.consensus,
            f"",
        ]

        if self.dissenting:
            lines += [
                f"## Dissenting Views",
                f"",
            ]
            for view in self.dissenting:
                lines.append(f"- {view}")
            lines.append("")

        lines.append("## Round Trace")
        lines.append("")
        for rnd in self.rounds:
            lines.append(f"### Round {rnd.round_num}")
            lines.append("")
            for persona_name, answer in rnd.agent_answers.items():
                lines.append(f"**{persona_name}:** {answer}")
                lines.append("")
            if rnd.critiques:
                lines.append("*Critiques:*")
                for critic_name, targets in rnd.critiques.items():
                    for target_name, critique in targets.items():
                        lines.append(
                            f"  - {critic_name} → {target_name}: {critique[:100]}"
                        )
                lines.append("")

        return "\n".join(lines)


def _agreement_score(answers: dict[str, str]) -> float:
    """Average pairwise Jaccard similarity between answers.

    0 = all different, 1 = identical.
    """
    from itertools import combinations

    texts = list(answers.values())
    if len(texts) < 2:
        return 1.0

    def _jaccard(a: str, b: str) -> float:
        sa = set(a.lower().split())
        sb = set(b.lower().split())
        if not sa and not sb:
            return 1.0
        if not sa or not sb:
            return 0.0
        return len(sa & sb) / len(sa | sb)

    pairs = list(combinations(texts, 2))
    return sum(_jaccard(a, b) for a, b in pairs) / len(pairs)


def _synthesize(
    answers: dict[str, str],
    question: str,
    answerer_fn,
) -> tuple[str, list[str]]:
    """Synthesize consensus from multiple answers using a simple heuristic.

    Algorithm:
    1. Split each answer into sentences.
    2. consensus = sentences that appear in >= majority of answers
       (token overlap > 0.5 with at least one other answer's sentence).
    3. dissenting = sentences unique to a single agent.
    """
    import re

    def _split_sentences(text: str) -> list[str]:
        # Split on sentence-ending punctuation followed by whitespace or end
        parts = re.split(r'(?<=[.!?])\s+', text.strip())
        return [p.strip() for p in parts if p.strip()]

    def _token_overlap(s1: str, s2: str) -> float:
        t1 = set(s1.lower().split())
        t2 = set(s2.lower().split())
        if not t1 and not t2:
            return 1.0
        if not t1 or not t2:
            return 0.0
        return len(t1 & t2) / len(t1 | t2)

    agent_sentences: dict[str, list[str]] = {
        name: _split_sentences(ans) for name, ans in answers.items()
    }

    n_agents = len(answers)
    majority = max(1, (n_agents + 1) // 2)  # ceil(n/2)

    all_sentences: list[tuple[str, str]] = []  # (agent_name, sentence)
    for agent_name, sents in agent_sentences.items():
        for s in sents:
            all_sentences.append((agent_name, s))

    # For each sentence count how many agents have a similar sentence
    consensus_sentences: list[str] = []
    dissenting_sentences: list[str] = []

    processed: set[int] = set()
    for i, (agent_i, sent_i) in enumerate(all_sentences):
        if i in processed:
            continue
        # Find all sentences across agents that are similar to sent_i
        similar_agents: set[str] = {agent_i}
        similar_indices: list[int] = [i]
        for j, (agent_j, sent_j) in enumerate(all_sentences):
            if j == i or j in processed:
                continue
            if agent_j != agent_i and _token_overlap(sent_i, sent_j) > 0.5:
                similar_agents.add(agent_j)
                similar_indices.append(j)

        if len(similar_agents) >= majority:
            consensus_sentences.append(sent_i)
            for idx in similar_indices:
                processed.add(idx)
        # Don't mark as processed yet for dissenting check

    # Dissenting: sentences not similar to any other agent's sentence
    for i, (agent_i, sent_i) in enumerate(all_sentences):
        is_similar_to_another = False
        for j, (agent_j, sent_j) in enumerate(all_sentences):
            if j == i or agent_j == agent_i:
                continue
            if _token_overlap(sent_i, sent_j) > 0.3:
                is_similar_to_another = True
                break
        if not is_similar_to_another:
            dissenting_sentences.append(sent_i)

    # Build consensus text: if we found consensus sentences use them,
    # otherwise fall back to the longest answer
    if consensus_sentences:
        consensus = " ".join(consensus_sentences)
    else:
        consensus = max(answers.values(), key=len) if answers else ""

    # Deduplicate dissenting (keep unique ones that differ from consensus)
    seen: set[str] = set()
    unique_dissenting: list[str] = []
    for s in dissenting_sentences:
        key = s.lower()[:80]
        if key not in seen:
            seen.add(key)
            unique_dissenting.append(s)

    return consensus, unique_dissenting


def multi_agent_debate(
    question: str,
    passages: list,
    *,
    personas: list[Persona] | None = None,
    max_rounds: int = 2,
    answerer_fn=None,
) -> DebateResult:
    """Run multi-agent debate.

    If personas is None: use [SKEPTIC, SYNTHESIZER, CONTRARIAN].
    If answerer_fn is None: use default echo (lambda q, p, s: q[:100]).

    Algorithm:
    1. Round 0: each persona answers independently.
    2. Rounds 1..max_rounds-1: each persona sees others' answers + critiques → refine.
    3. Synthesize consensus from final round answers.
    4. Compute confidence = _agreement_score(final_answers).
    5. Return DebateResult.
    """
    if personas is None:
        personas = [SKEPTIC, SYNTHESIZER, CONTRARIAN]

    if answerer_fn is None:
        answerer_fn = lambda q, p, s: q[:100]

    rounds: list[DebateRound] = []
    prior_answers: dict[str, str] | None = None

    for round_idx in range(max_rounds):
        debate_round = run_debate_round(
            question=question,
            personas=personas,
            passages=passages,
            answerer_fn=answerer_fn,
            round_num=round_idx,
            prior_answers=prior_answers,
        )
        rounds.append(debate_round)
        prior_answers = debate_round.agent_answers

    # Synthesize from final round answers
    final_answers = rounds[-1].agent_answers
    consensus, dissenting = _synthesize(final_answers, question, answerer_fn)

    confidence = _agreement_score(final_answers)
    # Clamp to [0, 1]
    confidence = max(0.0, min(1.0, confidence))

    personas_used = [p.name for p in personas]

    return DebateResult(
        question=question,
        consensus=consensus,
        dissenting=dissenting,
        confidence=confidence,
        rounds=rounds,
        personas_used=personas_used,
    )
