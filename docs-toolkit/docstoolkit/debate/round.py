"""Debate round — one iteration of answer generation + cross-critique."""
from dataclasses import dataclass, field

from docstoolkit.debate.persona import Persona


@dataclass
class DebateRound:
    round_num: int                            # 0-based
    agent_answers: dict[str, str]             # {persona_name: answer}
    critiques: dict[str, dict[str, str]]      # {critic_name: {target_name: critique}}


def _generate_answer(
    question: str,
    persona: Persona,
    passages: list,
    answerer_fn,
) -> str:
    """Generate one persona's answer using answerer_fn."""
    return answerer_fn(question, passages, persona.system_prompt)


def _generate_critique(
    critic: Persona,
    target_name: str,
    target_answer: str,
    answerer_fn,
) -> str:
    """Critique another agent's answer."""
    critique_prompt = f"Critique this answer as {critic.name}: {target_answer[:200]}"
    return answerer_fn(critique_prompt, [], critic.system_prompt)


def run_debate_round(
    question: str,
    personas: list[Persona],
    passages: list,
    answerer_fn,
    round_num: int = 0,
    prior_answers: dict[str, str] | None = None,
) -> DebateRound:
    """Run one debate round.

    1. Each persona generates an answer.
       If prior_answers given, the previous round's answers are included in
       the question context so each persona can refine its position.
    2. Each persona critiques all other personas' answers (cross-critique).
    3. Return DebateRound.

    answerer_fn signature: (question: str, passages: list, system_prompt: str) -> str
    """
    # Build context-enriched question when prior answers are available
    if prior_answers:
        prior_block = "\n\n".join(
            f"[{name}]: {answer}" for name, answer in prior_answers.items()
        )
        enriched_question = (
            f"{question}\n\n"
            f"Previous round answers for context:\n{prior_block}\n\n"
            f"Please refine your answer taking the above into account."
        )
    else:
        enriched_question = question

    # Step 1: each persona answers
    agent_answers: dict[str, str] = {}
    for persona in personas:
        agent_answers[persona.name] = _generate_answer(
            enriched_question, persona, passages, answerer_fn
        )

    # Step 2: cross-critique — each persona critiques all others
    critiques: dict[str, dict[str, str]] = {}
    for critic in personas:
        critic_critiques: dict[str, str] = {}
        for target in personas:
            if target.name == critic.name:
                continue
            critic_critiques[target.name] = _generate_critique(
                critic, target.name, agent_answers[target.name], answerer_fn
            )
        critiques[critic.name] = critic_critiques

    return DebateRound(
        round_num=round_num,
        agent_answers=agent_answers,
        critiques=critiques,
    )
