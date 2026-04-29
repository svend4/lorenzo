"""Декларативный chain-of-providers с failover."""
import time
from dataclasses import dataclass, field

from docstoolkit.rag.answerer import get_answerer


@dataclass
class ModelHop:
    """Один узел chain'а: какой answerer + model + параметры retry."""
    answerer: str = "echo"
    model: str = ""
    max_retries: int = 0            # ретраи до перехода к next hop
    retry_backoff_s: float = 0.5
    timeout_s: float = 60.0         # информационно, реально не enforced


@dataclass
class ModelChain:
    """Упорядоченный список hops для попыток."""
    name: str
    hops: list[ModelHop] = field(default_factory=list)
    description: str = ""


@dataclass
class RouteResult:
    """Результат routing'а с трассировкой попыток."""
    answer: str = ""
    tokens: int = 0
    cost: float = 0.0
    hop_used: int = -1               # индекс hop'а, который сработал
    hop_answerer: str = ""           # удобный alias
    hop_model: str = ""
    hops_tried: int = 0
    errors: list[str] = field(default_factory=list)
    duration_ms: int = 0

    @property
    def ok(self) -> bool:
        return self.hop_used >= 0


class ModelRouter:
    """Маршрутизатор: вызывает answerer'ы по chain'у, fallback на ошибку."""

    def __init__(self, *, on_hop_attempt=None, budget_check=None):
        """on_hop_attempt(chain_name, hop_idx, hop) — callback для tracing.
        budget_check(scope) — функция возвращающая True если можно тратить."""
        self.on_hop_attempt = on_hop_attempt
        self.budget_check = budget_check

    def invoke(self, chain: ModelChain, *, system: str, user: str,
               budget_scope: str = "") -> RouteResult:
        t0 = time.time()
        result = RouteResult()

        for i, hop in enumerate(chain.hops):
            result.hops_tried += 1
            if self.on_hop_attempt:
                try:
                    self.on_hop_attempt(chain.name, i, hop)
                except Exception:
                    pass

            # budget guard
            if self.budget_check and budget_scope:
                try:
                    ok = self.budget_check(budget_scope)
                except Exception:
                    ok = True
                if not ok:
                    result.errors.append(
                        f"hop[{i}] {hop.answerer}: budget blocked for {budget_scope}"
                    )
                    continue

            attempt = 0
            last_err = ""
            while attempt <= hop.max_retries:
                try:
                    a = get_answerer(hop.answerer)
                    text, toks, cost = a.answer(system, user, hop.model)
                    result.answer = text
                    result.tokens = toks
                    result.cost = cost
                    result.hop_used = i
                    result.hop_answerer = hop.answerer
                    result.hop_model = hop.model or "default"
                    result.duration_ms = int((time.time() - t0) * 1000)
                    return result
                except Exception as e:
                    last_err = f"{type(e).__name__}: {str(e)[:120]}"
                    attempt += 1
                    if attempt <= hop.max_retries:
                        time.sleep(hop.retry_backoff_s * attempt)

            result.errors.append(f"hop[{i}] {hop.answerer}/{hop.model}: {last_err}")

        result.duration_ms = int((time.time() - t0) * 1000)
        return result


# ---- built-in chains ----

BUILTIN_CHAINS: dict[str, ModelChain] = {
    "cheap": ModelChain(
        name="cheap",
        description="Дешёвый: Haiku → Echo",
        hops=[
            ModelHop(answerer="anthropic", model="claude-haiku-4-5-20251001",
                     max_retries=1),
            ModelHop(answerer="echo"),
        ],
    ),
    "fast": ModelChain(
        name="fast",
        description="Быстрый: Haiku → OpenAI mini → Echo",
        hops=[
            ModelHop(answerer="anthropic", model="claude-haiku-4-5-20251001"),
            ModelHop(answerer="openai", model="gpt-4o-mini"),
            ModelHop(answerer="echo"),
        ],
    ),
    "high-quality": ModelChain(
        name="high-quality",
        description="Лучший: Sonnet → GPT-4o → Haiku",
        hops=[
            ModelHop(answerer="anthropic", model="claude-sonnet-4-6",
                     max_retries=1),
            ModelHop(answerer="openai", model="gpt-4o"),
            ModelHop(answerer="anthropic", model="claude-haiku-4-5-20251001"),
            ModelHop(answerer="echo"),
        ],
    ),
    "balanced": ModelChain(
        name="balanced",
        description="Sonnet → Haiku → OpenAI → Echo",
        hops=[
            ModelHop(answerer="anthropic", model="claude-sonnet-4-6"),
            ModelHop(answerer="anthropic", model="claude-haiku-4-5-20251001"),
            ModelHop(answerer="openai", model="gpt-4o-mini"),
            ModelHop(answerer="echo"),
        ],
    ),
    "echo-only": ModelChain(
        name="echo-only",
        description="Только echo (для тестов)",
        hops=[ModelHop(answerer="echo")],
    ),
}


def get_chain(name: str) -> ModelChain | None:
    """Берёт built-in chain по имени."""
    return BUILTIN_CHAINS.get(name)
