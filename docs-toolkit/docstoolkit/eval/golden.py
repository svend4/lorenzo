"""Golden Q&A dataset + scoring."""
import re
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class GoldenItem:
    """Один golden Q&A: вопрос + ожидаемый ответ + ожидаемые источники."""
    question: str
    expected_answer_contains: list[str] = field(default_factory=list)
    expected_doc_ids: list[str] = field(default_factory=list)
    forbidden_phrases: list[str] = field(default_factory=list)
    weight: float = 1.0
    notes: str = ""


@dataclass
class GoldenSet:
    """Набор golden Q&A."""
    name: str
    items: list[GoldenItem] = field(default_factory=list)
    description: str = ""


@dataclass
class EvalItemResult:
    """Результат eval'а одного item'а."""
    question: str
    actual_answer: str = ""
    actual_doc_ids: list[str] = field(default_factory=list)
    answer_score: float = 0.0       # 0-100, по совпадению keywords
    citation_precision: float = 0.0
    citation_recall: float = 0.0
    citation_f1: float = 0.0
    forbidden_violated: list[str] = field(default_factory=list)
    weight: float = 1.0
    error: str = ""
    duration_ms: int = 0

    @property
    def overall(self) -> float:
        """Взвешенное среднее: 60% answer + 40% citation_f1."""
        if self.error:
            return 0.0
        return self.answer_score * 0.6 + self.citation_f1 * 100 * 0.4


@dataclass
class EvalResult:
    """Результат прогона всего eval set."""
    golden_set: str
    config: dict
    items: list[EvalItemResult] = field(default_factory=list)
    started_ts: str = field(default_factory=lambda: datetime.now().isoformat(timespec='seconds'))
    duration_ms: int = 0

    @property
    def overall_score(self) -> float:
        """Взвешенный overall."""
        if not self.items:
            return 0.0
        total_w = sum(i.weight for i in self.items) or 1.0
        return sum(i.overall * i.weight for i in self.items) / total_w

    @property
    def avg_answer_score(self) -> float:
        if not self.items:
            return 0.0
        return sum(i.answer_score for i in self.items) / len(self.items)

    @property
    def avg_citation_f1(self) -> float:
        if not self.items:
            return 0.0
        return sum(i.citation_f1 for i in self.items) / len(self.items)

    @property
    def errors(self) -> int:
        return sum(1 for i in self.items if i.error)

    def report(self) -> str:
        """Markdown отчёт."""
        lines = [f"# Eval: {self.golden_set}\n"]
        lines.append(f"**Config:** `{self.config}`")
        lines.append(f"**Started:** {self.started_ts}")
        lines.append(f"**Duration:** {self.duration_ms}ms")
        lines.append(f"**Items:** {len(self.items)} ({self.errors} errors)\n")

        lines.append(f"## Overall: {self.overall_score:.1f}/100\n")
        lines.append(f"- Avg answer score: {self.avg_answer_score:.1f}/100")
        lines.append(f"- Avg citation F1: {self.avg_citation_f1*100:.1f}%\n")

        lines.append("## Per-item\n")
        lines.append("| # | Question | Answer | Citations | Overall |")
        lines.append("|--:|----------|-------:|----------:|--------:|")
        for i, item in enumerate(self.items, 1):
            q = item.question[:40] + ("…" if len(item.question) > 40 else "")
            if item.error:
                lines.append(f"| {i} | {q} | — | — | ERR: {item.error[:30]} |")
            else:
                lines.append(
                    f"| {i} | {q} | {item.answer_score:.0f} | "
                    f"P{item.citation_precision*100:.0f}/R{item.citation_recall*100:.0f}"
                    f"/F{item.citation_f1*100:.0f} | "
                    f"**{item.overall:.0f}** |"
                )

        # Forbidden violations
        violations = [i for i in self.items if i.forbidden_violated]
        if violations:
            lines.append("\n## Forbidden phrase violations\n")
            for item in violations:
                lines.append(f"- `{item.question[:60]}`: "
                             f"{', '.join(item.forbidden_violated)}")

        return "\n".join(lines)


# ---- scoring ----

def score_answer(actual: str, expected_contains: list[str]) -> float:
    """0-100: доля expected_contains, найденных в actual (case-insensitive)."""
    if not expected_contains:
        return 100.0  # nothing to check
    actual_low = actual.lower()
    found = sum(1 for kw in expected_contains if kw.lower() in actual_low)
    return found / len(expected_contains) * 100


def score_citations(actual: list[str], expected: list[str]) -> tuple[float, float, float]:
    """Возвращает (precision, recall, f1) для doc_ids."""
    if not expected:
        return (1.0, 1.0, 1.0) if not actual else (0.0, 1.0, 0.0)
    actual_set = set(_normalize(d) for d in actual)
    expected_set = set(_normalize(d) for d in expected)

    if not actual_set:
        return 0.0, 0.0, 0.0

    tp = len(actual_set & expected_set)
    precision = tp / len(actual_set)
    recall = tp / len(expected_set)
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
    return precision, recall, f1


def _normalize(doc_id: str) -> str:
    """Нормализует doc_id: basename без расширения, lower."""
    s = doc_id.split("/")[-1].lower()
    if "." in s:
        s = s.rsplit(".", 1)[0]
    return s


# ---- runner ----

def run_eval(gset: GoldenSet, retriever_config: dict | None = None) -> EvalResult:
    """Прогоняет gset через rag.ask и считает scores."""
    from docstoolkit.rag import ask
    import time

    cfg = dict(retriever_config or {})
    cfg.setdefault("answerer", "echo")
    cfg.setdefault("method", "hybrid")
    cfg.setdefault("top_k", 5)

    result = EvalResult(golden_set=gset.name, config=cfg)
    t0 = time.time()

    for item in gset.items:
        ir = EvalItemResult(question=item.question, weight=item.weight)
        t_item = time.time()
        try:
            ans = ask(
                item.question,
                top_k=cfg.get("top_k", 5),
                method=cfg.get("method", "hybrid"),
                answerer=cfg.get("answerer", "echo"),
                model=cfg.get("model", "claude-haiku-4-5-20251001"),
            )
            ir.actual_answer = ans.answer
            ir.actual_doc_ids = [c.get("doc_id", "") for c in ans.citations]
            ir.answer_score = score_answer(ans.answer, item.expected_answer_contains)
            p, r, f = score_citations(ir.actual_doc_ids, item.expected_doc_ids)
            ir.citation_precision = p
            ir.citation_recall = r
            ir.citation_f1 = f
            # Forbidden phrases
            ans_low = ans.answer.lower()
            ir.forbidden_violated = [
                ph for ph in item.forbidden_phrases if ph.lower() in ans_low
            ]
        except Exception as e:
            ir.error = str(e)[:200]
        ir.duration_ms = int((time.time() - t_item) * 1000)
        result.items.append(ir)

    result.duration_ms = int((time.time() - t0) * 1000)
    return result


def load_golden_from_yaml(path: str) -> GoldenSet:
    """Загружает GoldenSet из YAML.

    Формат:
        name: rag-baseline
        description: ...
        items:
          - question: ...
            expected_answer_contains: [a, b]
            expected_doc_ids: [doc1.md]
    """
    from docstoolkit.frontmatter import parse_yaml
    from pathlib import Path
    text = Path(path).read_text(encoding="utf-8")
    data = parse_yaml(text)
    items_raw = data.get("items", []) or []
    # YAML parser limitation: list of dicts not supported; используется flat
    # представление (если items — list[str], считаем что это вопросы без gt)
    items = []
    for x in items_raw:
        if isinstance(x, str):
            items.append(GoldenItem(question=x))
        elif isinstance(x, dict):
            items.append(GoldenItem(
                question=x.get("question", ""),
                expected_answer_contains=x.get("expected_answer_contains", []),
                expected_doc_ids=x.get("expected_doc_ids", []),
                forbidden_phrases=x.get("forbidden_phrases", []),
                weight=float(x.get("weight", 1.0)),
                notes=x.get("notes", ""),
            ))
    return GoldenSet(name=data.get("name", "unnamed"),
                     items=items,
                     description=data.get("description", ""))
