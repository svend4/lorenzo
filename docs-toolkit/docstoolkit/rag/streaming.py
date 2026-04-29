"""Streaming RAG: token-by-token output через generator.

Все answerers могут опционально streaming (yield chunks).
Если answerer не поддерживает stream — yield весь ответ один раз.
"""
import time
from dataclasses import dataclass
from typing import Iterator

from docstoolkit.rag.assembler import assemble_prompt
from docstoolkit.rag.retriever import Retriever
from docstoolkit.rag.types import Passage, AnswerResult


@dataclass
class StreamChunk:
    """Один chunk потока."""
    type: str          # passages_retrieved | token | done | error
    data: dict
    ts: float = 0.0


def stream_rag(question: str, *,
               top_k: int = 5,
               method: str = "hybrid",
               answerer: str = "echo",
               model: str = "claude-haiku-4-5-20251001") -> Iterator[StreamChunk]:
    """Yields StreamChunk по событиям:
       - passages_retrieved: {count, passages: [{title, path, score}]}
       - token: {text} — для streaming-capable answerer'ов
       - done: {answer, citations, tokens, cost, duration_ms}
       - error: {msg}
    """
    t0 = time.time()

    # Retrieve
    try:
        retriever = Retriever(method=method, model=model)
        passages = retriever.search(question, top_k=top_k)
    except Exception as e:
        yield StreamChunk("error", {"msg": f"retrieve: {e}"}, time.time())
        return

    yield StreamChunk("passages_retrieved", {
        "count": len(passages),
        "passages": [
            {"title": p.title, "path": p.doc_id, "score": p.score}
            for p in passages
        ],
    }, time.time())

    if not passages:
        yield StreamChunk("done", {
            "answer": "Корпус пуст или релевантных пассажей нет.",
            "citations": [],
            "tokens": 0, "cost": 0.0,
            "duration_ms": int((time.time() - t0) * 1000),
        }, time.time())
        return

    # Assemble
    system, user = assemble_prompt(question, passages)

    # Stream from answerer
    if answerer == "echo":
        # EchoAnswerer не настоящий stream — но эмулируем chunked output
        yield from _echo_stream(question, passages, t0)
        return

    if answerer == "anthropic":
        try:
            yield from _anthropic_stream(system, user, model, passages, t0)
            return
        except Exception as e:
            yield StreamChunk("error", {"msg": f"anthropic: {e}"}, time.time())
            return

    if answerer == "openai":
        try:
            yield from _openai_stream(system, user, model, passages, t0)
            return
        except Exception as e:
            yield StreamChunk("error", {"msg": f"openai: {e}"}, time.time())
            return

    # Fallback на не-streaming через get_answerer + один chunk
    from docstoolkit.rag.answerer import get_answerer
    a = get_answerer(answerer)
    try:
        text, tokens, cost = a.answer(system, user, model)
    except Exception as e:
        yield StreamChunk("error", {"msg": str(e)}, time.time())
        return

    yield StreamChunk("token", {"text": text}, time.time())
    yield StreamChunk("done", {
        "answer": text,
        "citations": _make_citations(passages),
        "tokens": tokens, "cost": cost,
        "duration_ms": int((time.time() - t0) * 1000),
    }, time.time())


def _make_citations(passages: list[Passage]) -> list[dict]:
    return [
        {"n": i + 1, "doc_id": p.doc_id, "title": p.title, "score": p.score}
        for i, p in enumerate(passages)
    ]


def _echo_stream(question: str, passages: list[Passage],
                  t0: float) -> Iterator[StreamChunk]:
    """Эмулирует token-by-token: разбивает первый passage на chunks."""
    if not passages:
        yield StreamChunk("done", {"answer": "Нет данных", "citations": []}, time.time())
        return

    p = passages[0]
    answer = (f"[Echo] Top-1: **{p.title}** ({p.doc_id})\n\n"
              f"{p.text[:500]}")

    # Эмулируем streaming: chunk по 20 символов с задержкой
    chunk_size = 20
    for i in range(0, len(answer), chunk_size):
        yield StreamChunk("token", {"text": answer[i:i + chunk_size]}, time.time())
        time.sleep(0.01)  # имитация модели

    yield StreamChunk("done", {
        "answer": answer,
        "citations": _make_citations(passages),
        "tokens": len(answer) // 3,
        "cost": 0.0,
        "duration_ms": int((time.time() - t0) * 1000),
    }, time.time())


def _anthropic_stream(system: str, user: str, model: str,
                       passages: list[Passage], t0: float) -> Iterator[StreamChunk]:
    """Real streaming через Anthropic SDK."""
    import os
    try:
        import anthropic
    except ImportError:
        yield StreamChunk("error", {"msg": "pip install anthropic"}, time.time())
        return

    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    full_text = []
    in_tok = out_tok = 0

    with client.messages.stream(
        model=model,
        max_tokens=1500,
        system=system,
        messages=[{"role": "user", "content": user}],
    ) as stream:
        for event in stream.text_stream:
            full_text.append(event)
            yield StreamChunk("token", {"text": event}, time.time())

        msg = stream.get_final_message()
        in_tok = msg.usage.input_tokens
        out_tok = msg.usage.output_tokens

    pricing = {"input": 1.0, "output": 5.0}  # Haiku 4.5
    cost = (in_tok * pricing["input"] + out_tok * pricing["output"]) / 1_000_000

    yield StreamChunk("done", {
        "answer": "".join(full_text),
        "citations": _make_citations(passages),
        "tokens": in_tok + out_tok,
        "cost": cost,
        "duration_ms": int((time.time() - t0) * 1000),
    }, time.time())


def _openai_stream(system: str, user: str, model: str,
                    passages: list[Passage], t0: float) -> Iterator[StreamChunk]:
    """Real streaming через OpenAI SDK."""
    import os
    try:
        import openai
    except ImportError:
        yield StreamChunk("error", {"msg": "pip install openai"}, time.time())
        return

    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    full_text = []

    response = client.chat.completions.create(
        model=model or "gpt-4o-mini",
        max_tokens=1500,
        stream=True,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    for chunk in response:
        delta = chunk.choices[0].delta
        if delta and delta.content:
            full_text.append(delta.content)
            yield StreamChunk("token", {"text": delta.content}, time.time())

    text = "".join(full_text)
    yield StreamChunk("done", {
        "answer": text,
        "citations": _make_citations(passages),
        "tokens": len(text) // 3,  # rough
        "cost": 0.0,  # streaming не отдаёт точные usage
        "duration_ms": int((time.time() - t0) * 1000),
    }, time.time())
